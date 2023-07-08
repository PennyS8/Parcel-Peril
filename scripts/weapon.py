import pygame
from support import rotate_center
from settings import *
from pygame import Vector2

class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)
        
        # graphics
        full_path = f'graphics/weapons/{player.weapon_equipped}.png'
        self.orig_image = pygame.image.load(full_path).convert_alpha()
        self.image = self.orig_image # this will be used to avoid image quality loss
        self.rect = self.image.get_rect(center = player.rect.center)

        # weapon status
        self.position = Vector2(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        self.mouse_pos = Vector2(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        self.rotation = 0

        self.set_status(player.rect.center, player.status_aim_angle, player.rect.center, player.weapon_equipped)

    def draw(self, angle):

        if self.mouse_pos[0] >= SCREEN_WIDTH/2: # direction == 'right'
            rotated = rotate_center(self.orig_image, angle, self.position[0] + 10, self.position[1])
        else: # direction == 'left'
            # flip on the x-axis
            flipped_img = pygame.transform.flip(self.orig_image, True, False)
            flipped_angle = angle - 180
            rotated = rotate_center(flipped_img, flipped_angle, self.position[0] - 10, self.position[1])
        rotated_img = rotated[0]
        rotated_rect = rotated[1]

        return rotated_img, rotated_rect
    
    def switch_weapon(self, weapon):
        full_path = f'graphics/weapons/{weapon}.png'
        self.orig_image = pygame.image.load(full_path).convert_alpha()

    def set_status(self, aim_angle, mouse_pos, player_pos, weapon_equipped):
        # match weapon image to weapon_equipped
        self.switch_weapon(weapon_equipped)

        # placement and rotation vars
        self.position = player_pos
        self.rotation = aim_angle
        self.mouse_pos = mouse_pos

    def update(self):
        # calculate rotated image and rect
        rotated = self.draw(self.rotation)
        self.image = rotated[0]
        self.rect = rotated[1]