import pygame
from Settings import *
from Tile import Tile
from Player import Player
from Debug import dubug


class Level:
    def __init__(self):

        #get display surface
        self.display_surface = pygame.display.get_surface()
        # sprite group
        self.visible_sprites = YsortCameraGroup()
        self.obstacles_sprites = pygame.sprite.Group()

        #sprite setup
        self.create_map()

    def create_map(self):
        for row_index, row in enumerate(WORLD_MAP):
          for col_index, col in enumerate(row):
            x = col_index * TILESIZE
            y = row_index * TILESIZE
            if col == 'x':
               Tile((x,y),[self.visible_sprites,self.obstacles_sprites])
            if col == 'p':
                self.player = Player((x,y),[self.visible_sprites],self.obstacles_sprites)

    def run(self):
    #update game
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        dubug(self.player.direction)



class YsortCameraGroup(pygame.sprite.Group):
    def __init__(self):
       
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
    
    def custom_draw(self,Player):

        self.offset.x = Player.rect.centerx - self.half_width
        self.offset.y = Player.rect.centery - self.half_height

        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image,offset_pos)