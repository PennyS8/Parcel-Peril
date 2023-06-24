import pygame
from csv import reader
from os import walk
from settings import *

def import_csv_layout(path):
    terrain_map = []
    with open(path) as level_map:
        layout = reader(level_map, delimiter = ',')
        for row in layout:
            terrain_map.append(list(row))
        return terrain_map
    
# print(import_csv_layout('graphics/maps/conveyor_hell/Blocks.csv'))

def import_folder(path):
    surface_list = []

    for _,__,img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)

    return surface_list

# creates a list of sprite frames from a sprite sheet
# sprite sheet must have a transparent background and frames must be adjacent
def import_sprite_sheet(full_path, sprite_width, sprite_height, margin_x, margin_y):
    frames = []

    sheet = pygame.image.load(full_path).convert_alpha()

    # loops through each frame in the sheet
    for row in range(0, int((sheet.get_height() - margin_y) / sprite_height)):
        for col in range(0, int((sheet.get_width() - margin_x) / sprite_width)):
            # gets the sprite cordinates on the sheet
            frame_x = col * sprite_width + margin_x
            frame_y = row * sprite_height + margin_y

            frame = pygame.Surface((sprite_width, sprite_height)).convert_alpha()
            frame.blit(sheet, (0, 0), (frame_x, frame_y, sprite_width, sprite_height))

            frame.set_colorkey((255, 0, 255))

            frames.append(frame)

    if len(frames) == 0:
        print('ERROR: No frames found in sprite sheet: ' + full_path)

    return frames