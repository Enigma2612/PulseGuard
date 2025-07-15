from .utils import *
from .movement_functions import *


#GoodBullet --> Shot by the core: Good
#BadBullet --> Enemy projectile: Bad

class Bullet:
    def __init__(self, pos, size, speed, move_func, health, damage, color='white'):
        self.pos = vec(pos)
        self.size = size
        self.speed = speed
        self.color = color
        self.move_func = move_func
        self.health = health
        self.damage = damage
        self.btype = 'normal'
        self.types = []

        self.alive = True
    
    def move(self, *args, **kwargs):
        dx, dy = self.move_func(*args, **kwargs)
        self.pos += vec(dx, dy)
    
    def render(self, screen):
        pygame.draw.aacircle(screen, self.color, self.pos, self.size)

    def circle_collision(self, center, rad):
        return circle_to_circle_collision(self.pos, center, self.size, rad)

    def kill(self):
        self.alive = False
    
    def bullet_collision(self, other):
        if self.circle_collision(other.pos, other.size):
            if not (other.alive and self.alive):
                return False
            
            diff = min(other.health, self.health)
            if self.btype in ['normal', 'bad']:
                other.health -= diff
            if other.btype in ['normal', 'bad']:
                self.health -= diff
            
            self.update_life()
            other.update_life()

            return True
            
    def update_life(self):
        if self.health <= 0: self.alive = False

class GoodBullet(Bullet):
    def __init__(self, core, health):
        self.core = core
        super().__init__(self.core.shoot_pos, self.core.bullet_size, self.core.bullet_speed, radially_outward, health, self.core.damage, self.core.color)
        self.angle = self.core.shoot_angle
        self.type = 'good'

class BadBullet(Bullet):
    def __init__(self, pos, size, speed, move_func, health, damage, color = 'green'):
        super().__init__(pos, size, speed, move_func, health, damage, color)
        self.btype = 'bad'
    
class PowerUp(Bullet):
    def __init__(self, pos, size, speed, move_func, health, damage, color):
        super().__init__(pos, size, speed, move_func, health, damage, color)
        self.btype = 'powerup'
        self.types = ['powerup']
    

class ExtraShield(PowerUp):
    def __init__(self, pos, size, speed, move_func = radially_outward, health = 1, damage = 0, color = 'red'):
        super().__init__(pos, size, speed, move_func, 1, 0, color)
        self.btype = 'extra shield'
        self.types = ['extra shield', 'powerup']

        self.glow_rad = self.size
        self.max_glow_rad = self.size * 1.5
        self.min_glow_rad = self.size // 2
        self.freq = 0.5

        self.amplitude = (self.max_glow_rad - self.min_glow_rad)/2
        self.base_glow_rad = (self.max_glow_rad + self.min_glow_rad)/2

        self.glows = True
        self.glow_color = self.color
        self.timer = 0

    def impart_goodness(self, core):
        if not self.alive:
            return
        
        core.add_shield()
    
    def render(self, screen):
        super().render(screen)
        self.render_glow(screen)
    
    def render_glow(self, screen):
        glow_surf = pygame.Surface(((self.size + self.glow_rad)*2, (self.size + self.glow_rad)*2), pygame.SRCALPHA)
        glow_surf.fill('black')
        glow_surf.set_colorkey('black')
        glow_rad = int(self.glow_rad)
        pygame.draw.aacircle(glow_surf, self.glow_color, (glow_rad + self.size, glow_rad + self.size), (glow_rad + self.size))
        glow_surf.set_alpha(120)
        screen.blit(glow_surf, glow_surf.get_frect(center = self.pos))

    def update_glow(self, dt):
        self.timer += dt
        self.glow_rad = self.base_glow_rad + self.amplitude * math.sin(2 * math.pi * self.freq * self.timer + math.pi/2)

TYPES_DICT = {'normal': BadBullet, 'extra shield': ExtraShield}
POWERUP_LIS = ['extra shield', 'powerup', 'larger shield']

def spawn_circle_enemy(pos = None, color=None, btype = 'normal'):

    if isinstance(pos, type(None)):
        if random.random() <= 0.5:
            pos = (random.choice([0,W]), random.randint(0,H))
        else:
            pos = (random.randint(0,W), random.choice([0,H]))
    
    if color == None:
        return TYPES_DICT[btype](pos, 10, enemy_base_speed, track, 1, 1)
    else:
        return TYPES_DICT[btype](pos, 10, enemy_base_speed, track, 1, 1, color=color)
         