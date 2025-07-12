from .utils import *


class Particle:

    def __init__(self):
        self.alive = True
        self.current_lifespan = 0
    
    def update(self, dt, lifetime):
        self.current_lifespan += dt

        if self.current_lifespan >= lifetime:
            self.kill()
    
    def render(self):
        ...

    def kill(self):
        self.alive = False


class ExplodedBall(Particle):
    def __init__(self, pos, size, col_1, col_2, cover_rad, lifetime, vel):
        super().__init__()
        
        self.radius = size
        self.pos = vec(pos)
        self.color = col_1
        self.cover_color = col_2
        self.cover_radius = cover_rad
        self.lifetime = lifetime
        self.velocity = vec(vel)

        self.og_radius = self.radius
        self.og_cover_radius = self.cover_radius

        self.current_lifespan = 0
    
    def update(self, dt):
        super().update(dt, self.lifetime)
        self.pos += self.velocity * dt
        self.radius -= dt / self.lifetime * self.og_radius
        self.cover_radius -= dt / self.lifetime * self.og_cover_radius * 0.8
        

    def render(self, screen):
        pygame.draw.aacircle(screen, self.color, self.pos, self.radius)
        cover_surf = pygame.Surface([(self.cover_radius + self.radius)*2]*2, pygame.SRCALPHA)
        cover_surf.fill((0,0,0,0))
        pygame.draw.aacircle(cover_surf, self.cover_color, [(self.cover_radius + self.radius)]*2, (self.cover_radius + self.radius), width = int(self.cover_radius))
        screen.blit(cover_surf, cover_surf.get_rect(center = self.pos))

