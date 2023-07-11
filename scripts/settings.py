# game setup
SCREEN_WIDTH    = 512
SCREEN_HEIGHT   = 448
FPS             = 60
TILESIZE        = 32

# ui
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ITEM_BOX_SIZE = 80
UI_FONT = 'graphics/font/joystix.ttf'
UI_FONT_SIZE = 18

# general colors
WATER_COLOR = '#71DDDEE'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'

# ui colors
HEALTH_COLOR = 'red'
UI_BORDER_COLOR_ACTIVE = 'gold'

# graphics 'green' screen (i.e. image.set_colorkey(GREEN_SCREEN_COLOR))
GREEN_SCREEN_COLOR = (255, 0, 255)

# players weapons
weapon_data = {
    'scanner': {'cooldown': 800, 'damage': 10, 'type': 'one_hand', 'graphic': 'graphics/weapons/scanner.png'},
    'tape_roller': {'cooldown': 500, 'damage': 10, 'type': 'two_hands', 'graphic': 'graphics/weapons/tape_roller.png'}
    # 'box_cutter': {'cooldown': 300, 'damage': 5, 'type': 'one_hand', 'graphic': 'graphics/weapons/box_cutter.png'},
    # 'label_gun': {'cooldown': 200, 'damage': 2, 'type': 'two_hands', 'graphic': 'graphics/weapons/label_gun.png'},
    # 'stamp': {'cooldown': 200, 'damage': 2, 'type': 'two_hands', 'graphic': 'graphics/weapons/label_gun.png'}
}

# enemy
monster_data = {
    'small_cube': {'health': 100, 'exp': 100, 'damage': 10, 'attack_type': 'melee', 'speed': 3, 'resistance': 3, 'attack_radius':80, 'alert_radius': 360},
    'large_cube': {'health': 300, 'exp': 100, 'damage': 10, 'attack_type': 'melee', 'speed': 3, 'resistance': 3, 'attack_radius':80, 'alert_radius': 360},
    'crate_cube': {'health': 500, 'exp': 100, 'damage': 10, 'attack_type': 'melee', 'speed': 3, 'resistance': 3, 'attack_radius':80, 'alert_radius': 360},
}