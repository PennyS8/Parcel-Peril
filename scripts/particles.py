import pygame
from support import import_folder
from settings import *

class AnimationPlayer:
    def __init__(self):
        # TODO: create a dictionary for each type of particle animation
        self.frames = {
            # eating food / heal

            # monster deaths

            # enemy attack types

            # player attacks

            # level interactables

        }

    def reflect_images(self, frames):
        new_frames = []

        for frame in frames:
            flipped_frame = pygame.transform.flip(frame, True, False)
            new_frames.append(flipped_frame)

        return new_frames

class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, pos, animation_frames, groups) -> None:
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = ANIMATION_SPEED
        self.frames = animation_frames
        self.image = self.image.get_rect[self.frame_index]
        self.rect = self.image.get_rect(center = pos)

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self):
        self.animate()