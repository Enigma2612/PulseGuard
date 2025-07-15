from .utils import *
from .projectiles import *

class Shield:
    def __init__(self, pos, rad, span, freq, img=None, width = 10):
        if not img:
            self.image = None
            self.color = 'red'
        else:
            self.image = img
        
        self.cpos = vec(pos)
        self.radius = rad
        self.angle = 0 #angle in degrees
        self.span = span #angle in degrees
        self.width = width
        self.speed = freq
        self.lower_angle, self.upper_angle = self.angle - self.span//2, self.angle + self.span//2
        self.lower_angle, self.upper_angle = self.lower_angle % 360, self.upper_angle % 360
        self.bounding_rect = pygame.FRect(0,0, self.radius*2, self.radius*2)
        self.bounding_rect.center = self.cpos

        self.inner_rad = self.radius - self.width

        self.enabled = True
        self.rendered = True

    def move(self, keys, dt):
        if not self.enabled:
            return
        
        direction = (int(keys[pygame.K_a] or keys[pygame.K_LEFT]) - int(keys[pygame.K_d] or keys[pygame.K_RIGHT]))
        angle_change = 360 * dt * self.speed * direction

        self.angle += angle_change
        
    def smooth_render(self, screen):
        draw_aa_arc(screen, self.bounding_rect, math.radians(self.lower_angle), math.radians(self.upper_angle), self.width, self.color)

    def crude_render(self, screen):
        pygame.draw.arc(screen, self.color, self.bounding_rect.inflate(-2,-2), math.radians(self.lower_angle), math.radians(self.upper_angle), self.width-2)

    def render(self, screen):
        self.render_orbit(screen)
        if self.rendered:
            self.smooth_render(screen)
    def update(self, keys, dt):
        self.move(keys, dt)
        self.lower_angle, self.upper_angle = (self.angle - self.span//2) % 360, (self.angle + self.span//2) % 360

        self.angle = self.angle % 360
    
    def point_is_colliding(self, point):
        return check_arc_collision(self.lower_angle, self.upper_angle, self.radius, self.inner_rad, self.cpos, point)

    def circle_is_colliding(self, rad, center):
        eff_out_rad = self.radius + rad
        eff_in_rad = self.inner_rad - rad

        add_on_angle = math.degrees(math.atan2(rad, self.radius)) % 360
        
        eff_upper_angle = (self.upper_angle + add_on_angle) % 360
        eff_lower_angle = (self.lower_angle - add_on_angle) % 360

        return check_arc_collision(eff_lower_angle, eff_upper_angle, eff_out_rad, eff_in_rad, self.cpos, center)

    def render_orbit(self, screen):
        num = 120
        angle = 360 / num
        rect = pygame.FRect(0,0,(self.radius + self.inner_rad), (self.radius + self.inner_rad))
        rect.center = self.cpos
        color = (100,100,100)
        width = 4


        for i in range(0, num, 3):
            pygame.draw.arc(screen, color, rect, math.radians(angle*(i-1)), math.radians(angle*i), width)
            # draw_aa_arc(screen, rect, math.radians(angle*(i-1)), math.radians(angle*i), width, color)

        # pygame.draw.aacircle(screen, color, self.cpos, (self.radius + self.inner_rad)/2, width)

        # for i in range(0,num):
        #     if not i%3: continue
        #     pygame.draw.arc(screen, 'black', rect.inflate(3,3), math.radians(angle*(i-1)), math.radians(angle*i), width + 4)
        #     # draw_aa_arc(screen, rect, math.radians(angle*(i-1)), math.radians(angle*i), 4, color)

class Core:

    def __init__(self, game, pos, size, max_health, shield: Shield, color = (0, 191, 255)):
        self.game = game
        self.pos = vec(pos)
        self.size = size
        self.max_health = max_health
        self.health = max_health
        self.color = color

        self.alive = True
        self.exploded = False

        self.shields = [shield]

        self.shield = self.shields[0]

        for shield in self.shields: shield.cpos = self.pos

        self.hitbox_rad = self.size//2

        self.bullet_size = 10
        self.bullet_speed = 200

        self.shoot_rad = self.size - self.bullet_size
        self.ammo_rad = self.size + self.bullet_size*3

        self.ammo_rend_angle = 0
        self.ammo_spin_freq = 0.2
        self.ammo_color = (0, 191, 255, 80)

        self.shoot_angle = self.shield.angle
        self.shoot_pos = vec(self.shoot_rad * cos(self.shoot_angle), self.shoot_rad * sin(self.shoot_angle)) + self.pos

        self.ammo = 0
        self.max_ammo = 8
        self.damage = 1  #more power can destroy bigger bullets

        self.bullets : list[GoodBullet] = []

        self.enabled = True
        self.can_shoot = True

    def render(self, screen):

        for bullet in self.bullets:
            bullet.render(screen)
        
        if self.can_shoot and self.enabled:
            self.render_ammo(screen)
        
        pygame.draw.aacircle(screen, self.color, self.pos, self.size)
        self.render_shooter(screen)
    
    def render_shooter(self, screen):
        bounding_box = pygame.FRect(0,0,self.shoot_rad*2, self.shoot_rad*2)
        bounding_box.center = self.pos
        shooter_col = 'cyan'
        # pygame.draw.arc(screen, shooter_col, bounding_box, math.radians(self.shield.lower_angle), math.radians(self.shield.upper_angle), 8)
     
        draw_aa_arc(screen, bounding_box, math.radians(self.shield.lower_angle), math.radians(self.shield.upper_angle), 8, shooter_col, bgcolor=self.color)

    def render_ammo(self, screen):
        surf = pygame.Surface((W,H), pygame.SRCALPHA)
        for i in range(self.ammo):
            angle = (360 / self.max_ammo)* i + self.ammo_rend_angle
            pos = vec(self.ammo_rad * cos(angle), self.ammo_rad * sin(angle)) + self.pos

            pygame.draw.aacircle(surf, self.ammo_color, pos, round(self.bullet_size*0.75))
        
        screen.blit(surf, (0,0))

    
    def update_ammo_rendering(self, dt):
        self.ammo_rend_angle += dt * self.ammo_spin_freq * 360
        self.ammo_rend_angle = self.ammo_rend_angle % 360

    def shoot(self, angle = None, point = None):
        if not (self.enabled and self.can_shoot):
            return
        
        if isinstance(angle, type(None)):
            angle = self.shoot_angle

        if isinstance(point, type(None)):
            point = self.shoot_pos
            
        if self.ammo:
            bullet = GoodBullet(self, 1)
            bullet.angle = angle
            bullet.pos = point.copy()
            self.bullets.append(bullet)
            self.ammo -= 1
    
    def update(self, dt):
        self.check_damage(self.game.enemies, self.game.powerups)
        if self.health <= 0:
            self.alive = False
        else:
            self.shoot_angle = self.shield.angle
            self.shoot_pos = vec(self.shoot_rad * cos(self.shoot_angle), self.shoot_rad * sin(self.shoot_angle)) + self.pos
        
            for bullet in self.bullets:
                if bullet.move_func == radially_outward:
                    bullet.move(bullet.speed, bullet.angle, dt)
            
            for bullet in self.bullets:
                if bullet.pos.distance_to(bullet.core.pos) >= 0.5*math.sqrt(W**2 + H**2):
                    bullet.kill()
            
            self.bullets = [bullet for bullet in self.bullets if bullet.alive]

            self.update_ammo_rendering(dt)

    def handle_bullets(self, enemy_lis: list[BadBullet]):
        for bullet in self.bullets:
            for enemy in enemy_lis:
                bullet.bullet_collision(enemy)
    
    def check_damage(self, enemy_lis: list[BadBullet], powerup_lis: list[PowerUp | ExtraShield]):
        if not self.enabled:
            return
        for enemy in enemy_lis:
            if circle_to_circle_collision(enemy.pos, self.pos, enemy.size, self.hitbox_rad):
                self.health -= 1
                enemy.kill()

        for powerup in powerup_lis:
            if circle_to_circle_collision(powerup.pos, self.pos, powerup.size, self.hitbox_rad):
                powerup.impart_goodness(self)
                powerup.kill()

    def update_shields(self):
        num_shields = len(self.shields)
        angle = 360/num_shields
        for i in range(1, num_shields):
            self.shields[i].angle = self.shield.angle + angle*i
        
    
    def add_shield(self):
        shield = Shield(self.pos, self.shield.radius, self.shield.span, self.shield.speed, self.shield.image, self.shield.width)
        shield.angle = self.shield.angle + 360/(len(self.shields)+1) * (len(self.shields))
        self.shields.append(shield)
        self.update_shields()
    
    def render_shields(self, screen):
        for i,shield in enumerate(self.shields):
            if not i:
                shield.render_orbit(screen)
            
            if shield.rendered:
                shield.smooth_render(screen)

  