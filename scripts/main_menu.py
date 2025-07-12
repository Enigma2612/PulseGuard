from .utils import *
from .Shield_Core import *
from .animation import *

class MainMenu:
    
    def __init__(self, manager):
        self.manager = manager
        self.display = self.manager.display

        self.enemies = []

        self.game_button = pygame.FRect(0,0,200,80)
        self.game_button.center = (W//2, H*0.8)
        self.game_button_color = 'red'

        self.quit_button = pygame.FRect(0,0,200,80)
        self.quit_button.center = (W//2, H*0.9)
        self.quit_button_color = 'blue'

        self.shield = Shield((W//2, H//2), 200, 45, 0.7, width=15)
        self.core = Core(self, (W//2, H//2), 40, 1, self.shield) 

        self.title = draw_text(self.display, "Pulseguard", title_font, 'cyan', center = (W//2, H*0.15), draw = False)[1]

        self.shield.enabled = False
        self.core.enabled = False

        self.play_pressed = False

        self.center_animation = MainMenuCore(self)   

        self.fade_in = FadeIn(self, [self.game_button, self.quit_button, self.title])
        self.fade_out = FadeOut(self, [self.game_button, self.quit_button, self.title])

    def draw_buttons(self):
        pygame.draw.rect(self.display, self.game_button_color, self.game_button, 3, 6)
        pygame.draw.rect(self.display, self.quit_button_color, self.quit_button, 3, 6)

        draw_text(self.display, "Pulseguard", title_font, 'cyan', center = (W//2, H*0.15))
        draw_text(self.display, "Play", button_font, 'white', center = self.game_button.center)
        draw_text(self.display, "Quit", button_font, 'white', center = self.quit_button.center)
  

    def reset(self):
        self.display = self.manager.display

        self.enemies = []

        self.game_button = pygame.FRect(0,0,200,80)
        self.game_button.center = (W//2, H*0.8)
        self.game_button_color = 'red'

        self.quit_button = pygame.FRect(0,0,200,80)
        self.quit_button.center = (W//2, H*0.9)
        self.quit_button_color = 'blue'

        self.shield = Shield((W//2, H//2), 200, 45, 0.7, width=15)
        self.core = Core(self, (W//2, H//2), 40, 1, self.shield) 

        self.shield.enabled = False
        self.core.enabled = False

        self.play_pressed = False

        self.center_animation = MainMenuCore(self)         
        self.fade_in = FadeIn(self, [self.game_button, self.quit_button, self.title])
        self.fade_out = FadeOut(self, [self.game_button, self.quit_button, self.title])

    def run(self, dt):
        self.display.fill('black')
        mpos = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_button.collidepoint(mpos):
                    self.play_pressed = True
                if self.quit_button.collidepoint(mpos):
                    pygame.quit(); sys.exit()




        if not self.play_pressed:
            self.draw_buttons()
            self.center_animation.update(dt)
            self.shield.update(keys, dt)
            self.core.update(dt)

        self.shield.render(self.display)
        self.core.render(self.display)

        self.fade_in.update(dt)

        if self.play_pressed:
            if self.fade_out.step == 0:
                self.draw_buttons()
            if not self.fade_out.done:
                self.fade_out.update(dt)
            if self.fade_out.done:
                self.manager.scenes['Game'].reset()
                self.manager.scenes['Game'].shield.angle = self.shield.angle
                self.manager.change_scene_to('Game')

