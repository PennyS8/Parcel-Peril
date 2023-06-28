import pygame 
from settings import *
from support import import_sprite_sheet

class Player(pygame.sprite.Sprite):
	def __init__(self, pos, groups, obstacle_sprites):
		super().__init__(groups)
		self.image = pygame.image.load('graphics/player/poppy/poppy_init.png').convert_alpha()
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.inflate(-14, -16)

		# graphics setup
		self.import_player_assets()
		self.status_action = 'idle'
		self.status_direction = 'right'
		self.frame_index = 0
		self.animation_speed = 0.15

		# movement 
		self.direction = pygame.math.Vector2()

		self.busy = False
		self.busy_time = None
		self.busy_cooldown = 400

		self.attacking = False
		self.attack_time = None 
		self.attack_cooldown = 400

		self.obstacle_sprites = obstacle_sprites

		# stats
		self.stats = {'health': 100, 'speed': 5, 'attack': 10}
		self.health = self.stats['health']
		self.exp = 123
		self.speed = self.stats['speed']

	def import_player_assets(self):
		character_path = 'graphics/player/poppy/'
		self.animations = {
			'left_walk': [], 	'left_idle':[], 	'left_attack':[], 	'left_interact':[],
			'right_walk': [], 	'right_idle':[], 	'right_attack':[], 	'right_interact':[]}

		for animation in self.animations.keys():
			full_path = character_path + animation + '.png'
			self.animations[animation] = import_sprite_sheet(full_path, 32, 35, 0, 5)

	def input(self):
		if not self.attacking:
			keys = pygame.key.get_pressed()

			# movement input
			if keys[pygame.K_UP] or keys[pygame.K_w]:
				self.direction.y = -1
				# self.status_direction = 'up'
				self.status_action = 'walk'

			elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
				self.direction.y = 1
				# self.status_direction = 'down'
				self.status_action = 'walk'

			else:
				self.direction.y = 0

			if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
				self.direction.x = 1
				self.status_direction = 'right'
				self.status_action = 'walk'

			elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
				self.direction.x = -1
				self.status_direction = 'left'
				self.status_action = 'walk'

			else:
				self.direction.x = 0

			# attack input 
			if keys[pygame.K_f]:
				if not self.attacking and not self.busy:
					self.attacking = True
					self.attack_time = pygame.time.get_ticks()
					print('attack')	
			
			# interact input
			if keys[pygame.K_e]:
				if not self.attacking and not self.busy:
					self.busy = True
					self.busy_time = pygame.time.get_ticks()
					print('interact')

	def get_status_action(self):
		# idle status
		if self.direction.x == 0 and self.direction.y == 0:
			if not self.attacking and not self.busy:
				self.status_action = 'idle'

		if self.attacking:
			self.direction.x = 0
			self.direction.y = 0
			self.status_action = 'attack'

		if self.busy:
			self.direction.x = 0
			self.direction.y = 0
			self.status_action = 'interact'

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

		# other input cooldowns like interact
		if self.busy:
			if current_time - self.busy_time >= self.busy_cooldown:
				self.busy = False
		# attack cooldowns
		if self.attacking:
			if current_time - self.attack_time >= self.attack_cooldown:
				self.attacking = False

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