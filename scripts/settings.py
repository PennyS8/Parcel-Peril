# game setup
SCREEN_WIDTH    = 1280
SCREEN_HEIGHT   = 720
FPS             = 60
TILESIZE        = 32


# note: weapon sprite imgs are centered at the shoulder, then we can rotate around the center of the img an not need to
# translate them to keep the sholder matching with the player body
weapon_data = {
    'weaponless': {'cooldown': 400, 'damage': 10, 'type': 'unarmed', 'graphic': 'graphics/weapons/weaponless.png'},
    'scanner': {'cooldown': 800, 'damage': 10, 'type': 'one_hand', 'graphic': 'graphics/weapons/scanner.png'}
    # 'tape_roller': {'cooldown': 500, 'damage': 10, 'type': 'two_hands', 'graphic': 'graphics/weapons/tape_gun.png'},
    # 'box_cutter': {'cooldown': 300, 'damage': 5, 'type': 'one_hand', 'graphic': 'graphics/weapons/box_cutter.png'},
    # 'label_gun': {'cooldown': 200, 'damage': 2, 'type': 'two_hands', 'graphic': 'graphics/weapons/label_gun.png'},
    # 'stamp': {'cooldown': 200, 'damage': 2, 'type': 'two_hands', 'graphic': 'graphics/weapons/label_gun.png'}
}