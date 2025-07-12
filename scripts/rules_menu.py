from .utils import *
from .Shield_Core import *
from .animation import *

big_font = pygame.font.SysFont("Arial", 80)
normal_font = pygame.font.SysFont("Arial", 40)

class RulesMenu:
    rules = [
        "Before time had a meaning, all that existed was a powerful Core of Energy",
        "One instant, this Core, a vibrant ball of light, released most of it's energy, giving rise to the Universe.. Some call it, the Big Bang",
        "All that remained of the Core, was a small orb of Energy.. This orb was as delicate as it was powerful",
        "It's energy had been sustaining the Universe for eons.. But things were about to change",
        "As the Universe kept expanding, it soon stretched thin the fabric of space.. But the Universe showed no sign of stopping",
        "As it grew further, the fabric of space started ripping, and small holes started to form",
        "These holes, devoid of matter or energy, get attracted towards the energy of the Orb",
        "If even one, came into contact with the orb, it would destroy the balance of energy, and send the universe spiralling down to it's doom",
        "These demonic holes are called Hollows"
        
        "You gain consciousness one day, and see nothing but darkness.. But you feel a strange sort of energy pulsating from within you",
        "My words echo through your soul, and you realise.. You ARE the Orb.. Your safety will determine the fate of the universe"
        "You realise the dire task you have ahead of you.. Stay Safe, at all costs. Your determination manifests before you, and materialises into a defender shield",
        "This shield of yours has the power to destroy the Hollows, and orbits around you loyally.. You can control it",
        "You can also repel the hollows by summoning your own spheres of Energy.. The Hallows",
        "But as only Death can pay for Life, a Hallow may only be summoned upon the destruction of a Hollow",


        "Use A and D to control the shield",
        "Press Space to summon a Hallow",
        "Press Escape to go back to the Main Menu"
    ]

    def __init__(self, manager):
        self.manager = manager
        self.display : pygame.Surface = self.manager.display

        #Below code should all be in reset() function as well
        self.full_fade_out = FadeOut(self, self.display.get_rect(), 2) 
        self.exited = False
    
    def reset(self):
        self.full_fade_out = FadeOut(self, self.display.get_rect(), 2) 
        self.exited = False


    def run(self, dt):
        self.display.fill('black')
        
        keys = pygame.key.get_pressed()
        jkeys = pygame.key.get_just_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
        
        if jkeys(pygame.K_ESCAPE):
            self.exited = True
    
        if self.exited:
            if self.full_fade_out.done:
                self.manager.change_scene_to('Main Menu')
            else:
                self.full_fade_out.update(dt)
        
        