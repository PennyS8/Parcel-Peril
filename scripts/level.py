import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import *
from pygame import image
from weapon import Weapon

class Level:
    def __init__(self):

        # get the display surface
        self.display_surface = pygame.display.get_surface()

        # sprite group setup
        self.visable_sprites = YSortCameraGroup()
        self.obstacles_sprites = pygame.sprite.Group()

        # attack sprites
        self.current_attack = None

        # sprite setup
        self.create_map()

    def create_map(self):
        layout = {
            'boundry': import_csv_layout('graphics/maps/conveyor_hell/Boundry.csv'),
            'block': import_csv_layout('graphics/maps/conveyor_hell/Blocks.csv')
        }
        graphics = {
            'block': import_folder('graphics/maps/conveyor_hell_tileset')
        }

        for style, layout in layout.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE

                    if style == 'boundry':
                        Tile((x, y), [self.obstacles_sprites], 'invisible')
                    if style == 'block':
                        surf = graphics['block'][int(col)]
                        Tile((x, y), [self.obstacles_sprites, self.visable_sprites], 'block', surf)
                        
        self.player = Player((6 * TILESIZE, 7 * TILESIZE), [self.visable_sprites], self.obstacles_sprites, self.create_attack, self.destroy_attack)

    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visable_sprites])

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def run(self):
        # update and draw the game
        self.visable_sprites.custom_draw(self.player)
        self.visable_sprites.update()
        debug(self.player.status_direction + "_" + self.player.status_action)

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):

        # general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # creating the floor
        self.floor_surf = image.load('graphics/maps/Conveyor_Hell_Floor.png').convert_alpha()
        self.floor_rect = self.floor_surf.get_rect(topleft = (0, 0))

    def custom_draw(self, player):

        # getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        # for sprite in self.sprites():
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
