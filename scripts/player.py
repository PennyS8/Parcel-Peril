import pygame 
from settings import *
from support import import_sprite_sheet
from pygame import Vector2
from debug import debug

class Player(pygame.sprite.Sprite):
	def __init__(self, pos, groups, obstacle_sprites, create_weapon, destroy_weapon):
		super().__init__(groups)
		self.image = pygame.image.load('graphics/player/poppy/poppy_init.png').convert_alpha()
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.inflate(-14, -16)

		# graphics setup
		self.import_player_assets()
		self.status_action = 'idle'
		self.status_direction = 'left'
		self.frame_index = 0
		self.animation_speed = 0.15

		# movement 
		self.direction = pygame.math.Vector2()

		self.attacking = False
		self.attack_time = None 
		self.attack_cooldown = 150

		# weapon
		self.create_weapon = create_weapon
		self.destroy_weapon = destroy_weapon
		self.weapon_index = 0
		self.weapon = list(weapon_data.keys())[self.weapon_index]
		self.can_switch_weapon = True
		self.weapon_switch_time = None
		self.switch_duration_cooldown = 200

		# stats
		self.stats = {'health': 100, 'speed': 5, 'attack': 10}
		self.health = self.stats['health']
		self.exp = 123
		self.speed = self.stats['speed']

		# point and click
		self.mouse_pos = Vector2(self.rect.centerx, self.rect.centery)
		self.status_aim_angle = 0

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
				self.status_direction = 'right'

			elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
				self.direction.x = -1
				self.status_action = 'walk'
				self.status_direction = 'left'

			else:
				self.direction.x = 0

			# attack input 
			if clicks[0]:
				if not self.attacking:
					self.attacking = True
					self.attack_time = pygame.time.get_ticks()
					self.create_weapon()
					print('attack')	

					if self.mouse_pos[0] < SCREEN_WIDTH/2:
						self.status_direction = 'left'
					else:
						self.status_direction = 'right'

			# rotate weapons
			if keys[pygame.K_r]:
				if not self.attacking and self.can_switch_weapon:
					self.can_switch_weapon = False
					self.weapon_switch_time = pygame.time.get_ticks()
					self.weapon_index += 1
					if self.weapon_index >= len(list(weapon_data.keys())):
						self.weapon_index = 0
					print('weapon_index: ' + str(self.weapon_index))
					self.weapon = list(weapon_data.keys())[self.weapon_index]

	def get_status_action(self):
		self.mouse_pos = pygame.mouse.get_pos()

		# idle status
		if self.direction.x == 0 and self.direction.y == 0:
			if not self.attacking:
				self.status_action = 'idle'

		if self.attacking:
			self.direction.x = 0
			self.direction.y = 0
			self.status_action = 'attack'

		# get status aim angle
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

	def move(self, speed):
		if self.direction.magnitude() != 0:
			self.direction = self.direction.normalize()

		self.hitbox.x += self.direction.x * speed
		self.collision('horizontal')
		self.hitbox.y += self.direction.y * speed
		self.collision('vertical')
		self.rect.center = self.hitbox.center

	def collision(self, direction):
		if direction == 'horizontal':
			for sprite in self.obstacle_sprites:
				if sprite.hitbox.colliderect(self.hitbox):
					if self.direction.x > 0: # moving right
						self.hitbox.right = sprite.hitbox.left
					if self.direction.x < 0: # moving left
						self.hitbox.left = sprite.hitbox.right

		if direction == 'vertical':
			for sprite in self.obstacle_sprites:
				if sprite.hitbox.colliderect(self.hitbox):
					if self.direction.y > 0: # moving down
						self.hitbox.bottom = sprite.hitbox.top
					if self.direction.y < 0: # moving up
						self.hitbox.top = sprite.hitbox.bottom

	def cooldowns(self):
		current_time = pygame.time.get_ticks()
		
		# attack cooldowns
		if self.attacking:
			if current_time - self.attack_time >= self.attack_cooldown:
				self.attacking = False
				self.destroy_weapon()

		if not self.can_switch_weapon:
			if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
				self.can_switch_weapon = True

	def animate(self):
		animation = self.animations[self.status_direction + '_' + self.status_action]

		# loop over the frame index 
		self.frame_index += self.animation_speed
		if self.frame_index >= len(animation):
			self.frame_index = 0

		# set the image
		self.image = animation[int(self.frame_index)]
		self.rect = self.image.get_rect(center = self.hitbox.center)

	def update(self):
		self.input()
		self.cooldowns()
		self.get_status_action()
		self.animate()
		self.move(self.speed)