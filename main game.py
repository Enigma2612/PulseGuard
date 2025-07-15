from scripts.utils import *
from scripts.main_menu import *
from scripts.game import Game

class GameManager:

    def __init__(self):
        self.scenes = {}
        self.display = pygame.display.set_mode((W,H))
        pygame.display.set_caption('Pulseguard')

        self.setup()
    
    def setup(self):
        self.scenes['Game'] = Game(self)
        self.scenes['Main Menu'] = MainMenu(self)

        self.change_scene_to('Main Menu')

    def change_scene_to(self, scene, reset = False):
        if reset:
            self.scenes[scene].reset()
        self.current_scene = self.scenes[scene]

    def update(self):
        last_time = time.time()
        while True:
            dt = time.time() - last_time
            last_time = time.time()
            self.current_scene.run(dt)

            debug(1/dt if dt else 0)      #displaying fps
            pygame.display.update()


GameManager().update()  