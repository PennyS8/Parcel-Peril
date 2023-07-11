import pygame 
from settings import *
from support import import_sprite_sheet
from pygame import Vector2
from weapon import Weapon
from entity import Entity

class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
        self.image = pygame.image.load('graphics/player/poppy/poppy_init.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(-14, -16)

        # graphics setup
        self.import_player_assets()
        self.status_action = 'idle'
        self.status_direction = 'left'

        # stats
        self.stats = {'health': 100, 'speed': 4, 'attack': 10}
        self.health = self.stats['health']
        self.exp = 123
        self.speed = self.stats['speed']

        # point and click
        self.mouse_pos = Vector2(self.rect.centerx, self.rect.centery)
        self.status_aim_angle = 0
        self.holding_click = False

        # weapon
        self.weapon_index = 0
        self.weapon_equipped = list(weapon_data.keys())[self.weapon_index]

        self.attacking = False
        self.attack_time = None 
        self.attack_cooldown = 150

        self.can_switch_weapon = True
        self.weapon_switch_time = None
        self.switch_duration_cooldown = 200

        self.weapon_obj = Weapon(self, groups)

        # damage timer
        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability_duration = 500

        self.obstacle_sprites = obstacle_sprites

    def import_player_assets(self):
        character_path = 'graphics/player/poppy/'
        self.animations = {
            'left_walk': [], 	'left_idle':[], 	'left_attack':[],
            'right_walk': [], 	'right_idle':[], 	'right_attack':[]}

        for animation in self.animations.keys():
            full_path = character_path + animation + '.png'
            self.animations[animation] = import_sprite_sheet(full_path, 32, 35, 0, 5)

    def input(self):
        if not self.attacking:
            keys = pygame.key.get_pressed()
            clicks = pygame.mouse.get_pressed()

            # movement input
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.direction.y = -1
                self.status_action = 'walk'

            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.direction.y = 1
                self.status_action = 'walk'

            else:
                self.direction.y = 0

            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.direction.x = 1
                self.status_action = 'walk'
                # self.status_direction = 'right'

            elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.direction.x = -1
                self.status_action = 'walk'
                # self.status_direction = 'left'

            else:
                self.direction.x = 0

            # attack input 
            if clicks[0]:
                if not self.attacking and not self.holding_click:
                    self.attacking = True
                    self.holding_click = True
                    self.attack_time = pygame.time.get_ticks()
                    print('player_attack')	

                    if self.mouse_pos[0] < SCREEN_WIDTH/2:
                        self.status_direction = 'left'
                    else:
                        self.status_direction = 'right'

            # checks that the player is not holding down the attack button,
            # they must click each time to attack
            if not clicks[0]:
                self.holding_click = False

            # rotate weapons
            if keys[pygame.K_r]:
                if not self.attacking and self.can_switch_weapon:
                    self.can_switch_weapon = False
                    self.weapon_switch_time = pygame.time.get_ticks()
                    self.weapon_index += 1
                    if self.weapon_index >= len(list(weapon_data.keys())):
                        self.weapon_index = 0
                    print('weapon_index: ' + str(self.weapon_index))
                    self.weapon_equipped = list(weapon_data.keys())[self.weapon_index]

    def get_status(self):
        self.mouse_pos = pygame.mouse.get_pos()

        # idle status
        if self.direction.x == 0 and self.direction.y == 0:
            if not self.attacking:
                self.status_action = 'idle'

        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            self.status_action = 'attack'

        # get mouse position relative to player position
        # this calc assumes the player is at SCREEN_WIDTH/2, SCREEN_HEIGHT/2
        player_pos = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        normalized_x = self.mouse_pos[0] - player_pos[0]
        normalized_y = self.mouse_pos[1] - player_pos[1]

        # get status aim angle
        # note: angle ranges from [-180 to 180) with angle 0 degrees being negative (i.e. -0.0)
        # this is helpful when calculating how far to rotate the weapon/arm bone sprite
        if normalized_x != 0:
            vector = Vector2(normalized_x, normalized_y)
            # (* -1) is to match the unit circle angles, counterclockwise is positive
            self.status_aim_angle = Vector2(1, 0).angle_to(vector) * -1

        if normalized_x >= 0:
            self.status_direction = 'right'
        else:
            self.status_direction = 'left'

        # if dead
        if self.health == 0:
            # remove the weapon sprite
            if self.current_weapon:
                self.weapon_obj.current_weapon.kill()
                self.current_weapon = None
            # TODO: death animation
            # TODO: "you died" screen

        # updates status of weapon sprite
        self.weapon_obj.set_status(self.status_aim_angle, self.mouse_pos, self.rect.center, self.weapon_equipped)

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        # attack cooldowns
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False

        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                self.can_switch_weapon = True

        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulnerability_duration:
                self.vulnerable = True

    def animate(self):
        animation = self.animations[self.status_direction + '_' + self.status_action]

        # loop over the frame index 
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        # set the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

        # flicker
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.weapon_obj.update()
        self.animate()
        self.move(self.speed)