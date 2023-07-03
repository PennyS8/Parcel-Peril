# game setup
SCREEN_WIDTH    = 1280
SCREEN_HEIGHT   = 720
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

# note: weapon sprite imgs are centered at the shoulder, then we can rotate around the center of the img an not need to
# translate them to keep the sholder matching with the player body
weapon_data = {
    'scanner': {'cooldown': 800, 'damage': 10, 'type': 'one_hand', 'graphic': 'graphics/weapons/scanner.png'}
    # 'tape_roller': {'cooldown': 500, 'damage': 10, 'type': 'two_hands', 'graphic': 'graphics/weapons/tape_gun.png'},
    # 'box_cutter': {'cooldown': 300, 'damage': 5, 'type': 'one_hand', 'graphic': 'graphics/weapons/box_cutter.png'},
    # 'label_gun': {'cooldown': 200, 'damage': 2, 'type': 'two_hands', 'graphic': 'graphics/weapons/label_gun.png'},
    # 'stamp': {'cooldown': 200, 'damage': 2, 'type': 'two_hands', 'graphic': 'graphics/weapons/label_gun.png'}
}
