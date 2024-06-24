import pygame, sys
from Settings import *
from Level import Level
import os
# fixes problem with file directory not found
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class Game:
    def __init__(self):


        pygame.init()
        self.screen= pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption("The Legend of Slime")
        self.clock = pygame.time.Clock()

        self.level = Level()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.screen.fill('black')
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.run()
  