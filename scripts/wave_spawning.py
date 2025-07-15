from .utils import *
from .projectiles import *


class Wave:
    def __init__(self, weighted_types, time_interval, enemies_per_interval, span, span_type = 'time', spawn_on_start = False, enemy_colors=[None]):
        #span type: time - wave runs for 'span' seconds, span type: number - wave has 'span' number of enemies
        self.enemy_types: dict = weighted_types
        self.interval = time_interval
        self.total_span = span
        self.span_type = span_type
        self.spawn_per_interval = enemies_per_interval
        self.enemy_colors= enemy_colors
    
        if spawn_on_start:
            self.timer = time_interval
        else:
            self.timer = 0
        self.current_span = 0

        self.over = False

    def update(self, dt, elis, plis):
        self.timer += dt
        if self.span_type == 'time':
            self.current_span += dt
        
        if self.timer >= self.interval:
            self.spawn_enemies(elis, plis)
            self.timer = 0

        if self.current_span >= self.total_span:
            self.over = True

    def spawn_enemies(self, enemy_lis, powerup_lis):
        if self.span_type == 'number':
            spawn_num = min(self.spawn_per_interval, self.total_span - self.current_span)
            self.current_span += spawn_num
        else:
            spawn_num = self.spawn_per_interval
        
        
        for _ in range(spawn_num):
            enemy = random.choices(list(self.enemy_types), weights = list(self.enemy_types.values()))[0]
            pos = (W//2 + ((random.random()/2 + 0.5)*random.choice([-1,1]))*W, H//2 + ((random.random()/2 + 0.5)*random.choice([-1,1]))*H)
            if enemy == 'normal':
                enemy_lis.append(spawn_circle_enemy(pos, color=random.choice(self.enemy_colors)))
            elif enemy in POWERUP_LIS:
                powerup_lis.append(spawn_circle_enemy(pos, color=None, btype=enemy))

