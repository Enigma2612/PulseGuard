from .utils import *
from .particles import *


class Animation:
    def __init__(self, game, *objects):
        self.game = game
        self.objects = objects

        self.step = 0
        self.total_steps = 1
        self.done = False
    
    def update(self):
        if self.step == self.total_steps:
            self.done = True
    
    def reset(self):
        self.step = 0
        self.done = False

class CoreExplosion(Animation):
    def __init__(self, game, core):
        super().__init__(game, core)
        self.core = core
        self.shield = self.game.shield
        self.total_steps = 2            #shrinking, exploding
        self.core_decay_time = 0.5       #seconds
        self.core_explosion_time = 1.5    #seconds
        self.og_core_size = self.core.size
        self.og_shield_angle = self.shield.span

        self.particle_num = 100
        self.particle_speed = 300
        self.initiated_explosion = False
        self.particles : list[ExplodedBall] = []
    
    def update(self, dt):
        super().update()
        if self.step == 0:
            self.step_0(dt)
        if self.step == 1:
            self.step_1(dt)
    
    def step_0(self, dt):
        if self.core.size <= 0:
            self.step += 1
        else:
            self.core.size -= dt / self.core_decay_time * self.og_core_size
            self.core.shoot_rad -= dt / self.core_decay_time * self.og_core_size
            self.core.bullets = []
            self.core.ammo = 0
            self.core.enabled = False
            self.core.can_shoot = False
            self.shield.span -= dt / self.core_decay_time * self.og_shield_angle

            self.shield.span = max(self.shield.span, 2)
    
    def step_1(self, dt):
        if self.initiated_explosion and self.particles == []:
            self.step += 1
        
        self.shield.rendered = False
        self.game.enemies.clear()
        if not self.initiated_explosion:
            #todo: spawn exploded particles
            for i in range(self.particle_num):
                angle = random.random() * 360
                speed = random.randint(self.particle_speed//2, self.particle_speed*2)
                vel = vec(cos(angle)*speed, sin(angle)*speed)
                particle = ExplodedBall(self.core.pos, self.og_core_size//3, self.core.color, (0,255,255,60), 10, self.core_explosion_time, vel)
                self.particles.append(particle)
            
            self.initiated_explosion = True
        
        self.update_particles(dt)

    def update_particles(self, dt):
        for particle in self.particles:
            particle.update(dt)
            particle.render(self.game.display)
        
        self.particles = [particle for particle in self.particles if particle.alive]

class MainMenuCore(Animation):
    def __init__(self, menu):
        super().__init__(menu)
        self.core = menu.core
        self.shield = menu.shield

        self.total_steps = 2

        self.req_core_rad = self.core.size
        self.req_shoot_rad = self.core.shoot_rad
        self.core.size = 0
        self.core.shoot_rad = 0
        self.core_growth_time = 2       #seconds
        
        self.req_shield_angle = self.shield.span
        self.shield.span = 2


        self.spinning_freq = 0.2
    
    def update(self, dt):
        super().update()

        if self.step == 0:
            self.step_0(dt)
        
        if self.step == 1:
            self.step_1(dt)

    
    def step_0(self, dt):
        if self.core.size == self.req_core_rad:
            self.step += 1
        else:
            self.core.size = min(self.core.size + self.req_core_rad * dt / self.core_growth_time, self.req_core_rad)
            self.core.shoot_rad = min(self.core.shoot_rad + self.req_shoot_rad * dt / self.core_growth_time, self.req_shoot_rad)
            self.shield.span = min(self.shield.span + self.req_shield_angle * dt / self.core_growth_time, self.req_shield_angle)
            

    def step_1(self, dt):
        #moving shield
        angle_change = 360 * dt * self.spinning_freq * 1
        self.shield.angle += angle_change

class FadeIn(Animation):
    def __init__(self, game, objects, fade_in_time = 2, bg_color = 'black'):
        super().__init__(game, *objects)
        self.screen: pygame.Surface = self.game.display
        self.fade_in_time = fade_in_time
        self.bg_color = bg_color
        self.alpha = 255
        self.total_steps = 1
        self.dec = 0.5
        self.dec_rate = 0.5
        self.og_dec = self.dec

    
    def update(self, dt):
        super().update()

        if self.step == 0:
            self.step_0(dt)
    
    def step_0(self, dt):
        if self.alpha <= 0:
            self.step += 1

        for obj in self.objects:

            cover = pygame.Surface((obj.width, obj.height))
            cover.fill(self.bg_color)
            cover.set_alpha(self.alpha)

            self.screen.blit(cover, cover.get_rect(center = obj.center))

        self.alpha -= dt / self.fade_in_time * 255 * self.dec
        self.dec += dt / self.dec_rate * self.og_dec

class FadeOut(Animation):
    def __init__(self, game, objects, fade_in_time = 2, bg_color = 'black'):
        super().__init__(game, *objects)
        self.screen: pygame.Surface = self.game.display
        self.fade_in_time = fade_in_time
        self.bg_color = bg_color
        self.alpha = 0
        self.total_steps = 1
        self.inc = 2
        self.inc_rate = 1
        self.og_inc = self.inc

    
    def update(self, dt):
        super().update()
        if self.step == 0:
            self.step_0(dt)
    
    def step_0(self, dt):
        if self.alpha >= 255:
            self.step += 1

        for obj in self.objects:

            cover = pygame.Surface((obj.width, obj.height))
            cover.fill(self.bg_color)
            cover.set_alpha(self.alpha)

            self.screen.blit(cover, cover.get_rect(center = obj.center))

        self.alpha += dt / self.fade_in_time * 255 * self.inc
        self.inc += dt / self.inc_rate * self.og_inc
