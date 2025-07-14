from scripts.utils import *
from scripts.Shield_Core import *
from scripts.wave_spawning import *
from scripts.animation import *


class Game:
    def __init__(self, manager):
        self.manager = manager
        self.display = self.manager.display
        self.game_over = False
        self.paused = False

        self.shield = Shield((W//2, H//2), 200, 45, 0.7, width=15)

        self.core = Core(self, (W//2, H//2), 40, 1, self.shield)

        self.enemies : list[BadBullet]= []

        self.enemy_waves = [Wave({'normal':1}, 8, 2, 30, spawn_on_start = True),
                       Wave({'normal':1}, 6, 3, 30, span_type='number', enemy_colors=['yellow']),
                       Wave({'normal':1}, 6, 2, 30, enemy_colors=['coral', 'orange']),
                       Wave({'normal':1}, 3, 4, 120, enemy_colors=['maroon', 'darkblue'])]

        # self.enemy_waves = [Wave({'normal':1}, 3, 4, 120, enemy_colors=['maroon', 'darkblue'])]
        self.wave_index = 0
        self.total_waves = len(self.enemy_waves)
        self.current_wave = self.enemy_waves[self.wave_index]



        self.explosion_animation = CoreExplosion(self, self.core)
    
    def handle_enemies(self, dt):
        for enemy in self.enemies:
            if enemy.move_func == track:
                enemy.move(enemy.pos, self.core.pos, enemy.speed, dt)
                
        for enemy in self.enemies[:]:

            for shield in self.core.shields:
                if shield.circle_is_colliding(enemy.size, enemy.pos):
                    enemy.kill()
                    self.core.ammo = min(self.core.ammo + 1, self.core.max_ammo)
        
        self.enemies = [enemy for enemy in self.enemies if enemy.alive]
        
    def shoot_good_bullets(self, jkeys):
        if jkeys[pygame.K_SPACE]:
            self.core.shoot()
        
        #hexa shot
        if jkeys[pygame.K_s]:
            for i in range(6):
                angle = i*360//6
                self.core.shoot(angle, self.core.pos)
            
    def spawn_enemy(self, pos):
        self.enemies.append(spawn_circle_enemy(pos))

    def render_enemies(self):
        [enemy.render(self.display) for enemy in self.enemies]

    def reset(self):
        self.game_over = False
        self.paused = False

        self.shield = Shield((W//2, H//2), 200, 45, 0.7, width=15)

        self.core = Core(self, (W//2, H//2), 40, 1, self.shield)

        self.enemies : list[BadBullet]= []

        self.enemy_waves = [Wave({'normal':1}, 8, 2, 30, spawn_on_start = True),
                       Wave({'normal':1}, 6, 3, 30, span_type='number', enemy_colors=['yellow']),
                       Wave({'normal':1}, 6, 2, 30, enemy_colors=['coral', 'orange']),
                       Wave({'normal':1}, 3, 4, 120, enemy_colors=['maroon', 'darkblue'])]
        
        # self.enemy_waves = [Wave({'normal':1}, 3, 4, 120, enemy_colors=['maroon', 'darkblue'])]
        self.wave_index = 0
        self.total_waves = len(self.enemy_waves)
        self.current_wave = self.enemy_waves[self.wave_index]

        self.explosion_animation = CoreExplosion(self, self.core)

    def run(self, dt):
        self.display.fill('black') 

        keys = pygame.key.get_pressed()
        jkeys = pygame.key.get_just_pressed()
        kmouse = pygame.mouse.get_pressed()
        jmouse = pygame.mouse.get_just_pressed()
        mpos = pygame.mouse.get_pos()

        if jkeys[pygame.K_p]:
            self.paused = not self.paused

        if jkeys[pygame.K_g]:
            self.core.alive = False
        
        if jkeys[pygame.K_h]:
            self.core.ammo += 1

        if jkeys[pygame.K_r]:
            self.core.add_shield()

        #going back to the main menu
        if jkeys[pygame.K_ESCAPE]:
            menu = self.manager.scenes['Main Menu']
            anim = menu.center_animation
            menu.reset()
            anim.step = 3
            menu.shield.angle = self.shield.angle
            menu.shield.span = self.shield.span
            menu.core.size = self.core.size
            menu.core.shoot_rad = self.core.shoot_rad

            self.manager.change_scene_to('Main Menu')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()   

        if not self.paused:
            #updating all
            if not self.game_over:

                for shield in self.core.shields:
                    shield.update(keys, dt)
            
                self.core.update(dt)
                self.core.handle_bullets(self.enemies)
        
            #handling enemies
            self.handle_enemies(dt)
            if not self.game_over:
                self.shoot_good_bullets(jkeys)

                if jkeys[pygame.K_LSHIFT]:
                    self.spawn_enemy(None)

            #handling waves
            
            if self.current_wave.over:
                if self.wave_index == self.total_waves-1:
                    pass
                else:
                    self.wave_index += 1
                    self.current_wave = self.enemy_waves[self.wave_index]
            else:
                self.current_wave.update(dt, self.enemies)
            
            if not self.core.alive:
                self.game_over = True


        #rendering all
        self.core.render_shields(self.display)
        self.render_enemies()
        self.core.render(self.display)


        if self.game_over:
            if self.explosion_animation.done:
                time.sleep(0.5)
                self.manager.scenes['Main Menu'].reset()
                # self.manager.scenes['Main Menu'].shield.angle = self.shield.angle
                self.manager.change_scene_to("Main Menu")
            else:
                self.shield.enabled = False
                self.explosion_animation.update(dt)
                self.shield.update(keys, dt)

        debug(self.core.shields.__len__())
        # debug((len(self.enemies), self.core.health, self.explosion_animation.step))
    