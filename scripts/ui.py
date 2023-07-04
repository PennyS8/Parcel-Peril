import pygame
from settings import *

class UI:
    def __init__(self):
        # general
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # bar setup
        self.health_bar_rect = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)

        # convert weapon dictionary
        self.weapon_graphics = []
        for weapon in weapon_data.values():
            path = weapon['graphic'].split('.')[0] + '_icon.png'
            weapon = pygame.image.load(path).convert()
            self.weapon_graphics.append(weapon)

    def show_bar(self, current, max_amount, bg_rect, color):
        # draw background
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

        # converting stats to pixels
        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        # drawing the bar
        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

    def show_exp(self, exp):
        text_surf = self.font.render('EXP: ' + str(int(exp)), False, TEXT_COLOR)
        x = SCREEN_WIDTH - 20
        y = SCREEN_HEIGHT - 20
        text_rect = text_surf.get_rect(bottomright = (x, y))

        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20, 20))
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(20, 20), 3)

    def selection_box(self, left, top, has_switched):
        bg_rect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        if not has_switched:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR_ACTIVE, bg_rect, 3)
        else:
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

        return bg_rect

    def weapon_overlay(self, weapon_index, has_switched):
        self.selection_box(10, SCREEN_HEIGHT - ITEM_BOX_SIZE - 10, has_switched)
        bg_rect = self.selection_box(10, SCREEN_HEIGHT - 90, has_switched)
        weapon_surface = self.weapon_graphics[weapon_index]
        weapon_rect = weapon_surface.get_rect(center = bg_rect.center)
        
        self.display_surface.blit(weapon_surface, weapon_rect)

    def crosshair(self, mouse_x, mouse_y):
        crosshair_surface = pygame.image.load('graphics/other/crosshair.png').convert_alpha()
        crosshair_surface.set_colorkey(GREEN_SCREEN_COLOR)
        crosshair_rect = crosshair_surface.get_rect(center = (mouse_x, mouse_y))
        self.display_surface.blit(crosshair_surface, crosshair_rect)

    def display(self, player):
        self.show_bar(player.health, player.stats['health'], self.health_bar_rect, HEALTH_COLOR)
        
        self.show_exp(player.exp)

        self.weapon_overlay(player.weapon_index, player.can_switch_weapon)

        self.crosshair(player.mouse_pos[0], player.mouse_pos[1])
