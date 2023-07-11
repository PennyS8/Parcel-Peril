import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import *
from pygame import image
from ui import UI
from enemy import Enemy

class Level:
    def __init__(self):

        # get the display surface
        self.display_surface = pygame.display.get_surface()

        # sprite group setup
        self.visable_sprites = YSortCameraGroup()
        self.obstacles_sprites = pygame.sprite.Group()

        # attack sprites
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        # sprite setup
        self.create_map()

        # user interface
        self.ui = UI()

    def create_map(self):
        layout = {
            'boundry': import_csv_layout('graphics/maps/conveyor_hell/boundry.csv'),
            'block': import_csv_layout('graphics/maps/conveyor_hell/blocks.csv'),
            'entities': import_csv_layout('graphics/maps/conveyor_hell/entities.csv')
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

                    if style == 'entities':
                        if col == '4': # this number is from the 'tiled' index of the player entity
                            self.player = Player((x, y), [self.visable_sprites], self.obstacles_sprites)
                        elif col == '10': # this number is from the 'tiled' index of the enemy entity
                            Enemy(
                                'tall_flat', 
                                (x, y), 
                                [self.visable_sprites, self.attackable_sprites], 
                                self.obstacles_sprites,
                                self.damadge_player)

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                # this creates a list of all collisions between attack_sprites and attackable_sprites
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collision_sprites is not None:
                    for target_sprite in collision_sprites:
                    # you can create destoryables in the level here by checking for sprite_type of target_sprite
                        target_sprite.get_damage(self.player, attack_sprite.sprite_type)

    def damadge_player(self, amount, attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            # TODO: spawn particles

    def run(self):
        # update and draw the game
        self.visable_sprites.custom_draw(self.player)
        self.visable_sprites.update()
        self.visable_sprites.enemy_update(self.player)
        self.player_attack_logic()
        self.ui.display(self.player)

################################################################

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

    def enemy_update(self, player):
        enemy_sprites = [
            sprite for sprite in self.sprites() 
                if hasattr(sprite,'sprite_type') 
                and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)