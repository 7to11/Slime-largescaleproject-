import pygame
from Settings import *
from Tile import Tile
from Player import Player
from Debug import dubug
from Player2 import Player2
from Support import *
import os
from random import choice
os.chdir(os.path.dirname(os.path.abspath(__file__)))
class Level:
    def __init__(self):
        # Get display surface
        self.display_surface = pygame.display.get_surface()
        
        # Sprite groups
        self.visible_sprites = YsortCameraGroup()
        self.obstacles_sprites = pygame.sprite.Group()

        # Sprite setup
        self.create_map()

    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('../map/map_FloorBlocks.csv'),
            'grass': import_csv_layout('../map/map_Grass.csv'),
            'object': import_csv_layout('../map/map_Objects.csv'),
        }
        graphics = {
            'grass' : import_folder ('../graphics/Grass'),
            'objects': import_folder('../graphics/objects'),
        }
        
        for style,layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x,y),[self.obstacles_sprites],'invisible')
                        if style == 'grass':
                            random_grass_image = choice(graphics['grass'])
                            Tile((x,y),[self.visible_sprites,self.obstacles_sprites],'grass',random_grass_image)
                        if style == 'object':
                            surf = graphics['objects'][int(col)]
                            Tile((x,y),[self.visible_sprites,self.obstacles_sprites],'object',surf)

        self.player = Player((2000, 1430), [self.visible_sprites], self.obstacles_sprites)
        self.player2 = Player2((2000, 1430), [self.visible_sprites], self.obstacles_sprites)
    def run(self):
        # Update game
        self.visible_sprites.update()
        self.visible_sprites.custom_draw([self.player, self.player2])
    

class YsortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        #floor
        self.floor_surf = pygame.image.load('../graphics/tilemap/ground.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft= (0,0))


    def custom_draw(self, players):
        if players:
            # Calculate average center position
            centerx = sum(player.rect.centerx for player in players) // len(players)
            centery = sum(player.rect.centery for player in players) // len(players)

            self.offset.x = centerx - self.half_width
            self.offset.y = centery - self.half_height

            floor_offset_pos = self.floor_rect.topleft - self.offset
            self.display_surface.blit(self.floor_surf,floor_offset_pos)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)