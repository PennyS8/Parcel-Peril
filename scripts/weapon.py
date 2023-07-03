import pygame
from support import rotate_center
from support import blit_rotate_center

class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)
        direction = player.status_direction
        rot_angle = player.status_aim_angle

        # graphics
        # TODO: edit sprites so that arm weapon img overlays with the player image cohesively
        full_path = f'graphics/player/poppy/weapons/{player.weapon}.png'
        self.image = pygame.image.load(full_path).convert()

        # position and rotation
        if direction == 'right':
            rotated_img = rotate_center(self.image, rot_angle, player.rect.centerx, player.rect.centery)
        else: # direction == 'left'
            flipped_img = pygame.transform.flip(self.image, True, False)
            flipped_rot_angle = rot_angle - 180
            rotated_img = rotate_center(flipped_img, flipped_rot_angle, player.rect.centerx, player.rect.centery)

        self.image = rotated_img[0]
        self.rect = rotated_img[1]
