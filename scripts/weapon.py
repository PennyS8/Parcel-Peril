import pygame
from support import rotate_center
from settings import *

class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)
        rot_angle = player.status_aim_angle

        # graphics
        full_path = f'graphics/weapons/{player.weapon}.png'
        self.image = pygame.image.load(full_path).convert_alpha()

        # position and rotation
        if player.mouse_pos[0] >= SCREEN_WIDTH/2: # direction == 'right'
            rotated_img = rotate_center(self.image, rot_angle, player.rect.centerx, player.rect.centery)
        else: # direction == 'left'
            flipped_img = pygame.transform.flip(self.image, True, False)
            flipped_rot_angle = rot_angle - 180
            rotated_img = rotate_center(flipped_img, flipped_rot_angle, player.rect.centerx, player.rect.centery)

        self.image = rotated_img[0]
        self.rect = rotated_img[1]
