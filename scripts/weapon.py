import pygame

class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)
        direction = player.status_direction

        # graphic
        full_path = f'graphics/weapons/{player.weapon}/{direction}.png'
        self.image = pygame.image.load(full_path).convert_alpha()
        self.image.set_colorkey((255, 0, 255))
        
        # placement
        if direction == 'right':
            self.rect = self.image.get_rect(midleft = player.rect.midright - pygame.math.Vector2(6, 2))
        else: # left
            self.rect = self.image.get_rect(midright = player.rect.midleft + pygame.math.Vector2(6, -2))