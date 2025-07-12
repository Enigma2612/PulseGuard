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
                return
            
            diff = min(other.health, self.health)
            if self.btype in ['normal']:
                other.health -= diff
            if other.btype in ['normal']:
                self.health -= diff
            
            self.update_life()
            other.update_life()
            
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
        self.type = 'bad'
    

def spawn_circle_enemy(pos = None, color=None):

    if isinstance(pos, type(None)):
        if random.random() <= 0.5:
            pos = (random.choice([0,W]), random.randint(0,H))
        else:
            pos = (random.randint(0,W), random.choice([0,H]))
    
    if color == None:
        return BadBullet(pos, 10, enemy_base_speed, track, 1, 1)
    else:
        return BadBullet(pos, 10, enemy_base_speed, track, 1, 1, color=color)
         