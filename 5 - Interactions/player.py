import pygame, sys 
import imghdr
import os
import support
from math import sin
from particles import ParticleEffect

class Player(pygame.sprite.Sprite):
	def __init__(self,pos,health,surface,create_jump_dust):
		super().__init__()
		# setup
		self.import_main_assets()
		self.frame_index = 0
		self.animation_speed = 0.15
		self.image = self.animations['idle'][self.frame_index]
		self.rect = self.image.get_rect(center = pos)
		
		# dust particles 
		self.surface = surface
		self.import_dust_particles()
		self.dust_frame_index = 0
		self.create_jump_dust = create_jump_dust

		# movement
		self.direction = pygame.math.Vector2(0,0)
		self.speed = 8
		self.gravity = 0.8
		self.jump_speed = -16
		
		# status information
		self.status = 'idle'
		self.on_ground = False
		self.on_ceiling = False
		self.on_left   = False
		self.on_right  = False
		self.facing_right = False

		# game stats
		self.current_health = health
		self.max_health = health
		self.coins = 10
		self.invincible = False
		self.invincibility_duration = 500
		self.hurt_time = 0

		# audio 
		self.jump_sound = pygame.mixer.Sound('../audio/effects/jump.wav')
		self.jump_sound.set_volume(0.5)
		self.hit_sound = pygame.mixer.Sound('../audio/effects/hit.wav')

		

	def import_main_assets(self):
		character_path = '../graphics/character/'
		self.animations = {'idle': [],'run': [],'jump': [], 'fall': []}

		for animation in self.animations.keys():
			full_path = character_path + animation
			self.animations[animation] =  support.import_folder(full_path)

	def import_dust_particles(self):
		dust_path = '../graphics/character/dust_particles/'
		self.dust_animations = {'jump':[],'land': [],'run':[]}

		for animation in self.dust_animations.keys():
			full_path = dust_path + animation
			self.dust_animations[animation] = support.import_folder(full_path)

	def get_input(self):
		keys = pygame.key.get_pressed()

		if keys[pygame.K_RIGHT]: 
			self.direction.x = 1
			self.facing_right = True
		elif keys[pygame.K_LEFT]: 
			self.direction.x = -1
			self.facing_right = False
		else: self.direction.x = 0

		if keys[pygame.K_SPACE] and self.on_ground:
			self.jump_sound.play()
			self.jump()
			self.on_ground = False
			self.create_jump_dust(self.rect.midbottom)

	def jump(self):
		#
		self.direction.y = self.jump_speed

	def apply_gravity(self):
		#
		self.direction.y += self.gravity

	def get_status(self):
		if self.direction.y < 0:
			self.status = 'jump'
		elif self.direction.y > 1:
			self.status = 'fall'
		else: 
			if self.direction.x != 0:
				self.status = 'run'
			else:
				self.status = 'idle'

	def animate(self):
		animation = self.animations[self.status]

		# loop over frame index 
		self.frame_index += self.animation_speed
		if self.frame_index >= len(animation):
			self.frame_index = 0
		
		# set the image 
		image = animation[int(self.frame_index)]
		if self.facing_right: 
			self.image = image
		else: 
			flipped_image = pygame.transform.flip(image,True,False)
			self.image = flipped_image

		if self.invincible:
			alpha = self.sine_value()
			self.image.set_alpha(alpha)
		else:
			self.image.set_alpha(255)

		# set the rect 
		if self.on_ground and self.on_right:
			self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
		elif self.on_ground and self.on_left:
			self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
		elif self.on_ground:
			self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
		elif self.on_ceiling and self.on_right:
			self.rect = self.image.get_rect(topright = self.rect.topright)
		elif self.on_ceiling and self.on_left:
			self.rect = self.image.get_rect(topleft = self.rect.topleft)
		elif self.on_ceiling:
			self.rect = self.image.get_rect(midtop = self.rect.midtop)

	def dust_animation(self):
		if self.status == 'run' and self.on_ground:
			animation = self.dust_animations['run']
			self.dust_frame_index += self.animation_speed
			if self.dust_frame_index >= len(animation):
				self.dust_frame_index = 0
			dust_particle = animation[int(self.dust_frame_index)]
			if self.facing_right:
				self.surface.blit(dust_particle,self.rect.bottomleft - pygame.math.Vector2(6,10))
			else:
				dust_particle = pygame.transform.flip(dust_particle,True,False)
				self.surface.blit(dust_particle,self.rect.bottomright - pygame.math.Vector2(6,10))

	def sine_value(self):
		val = int(sin(pygame.time.get_ticks()) * 2)
		if val < 0: val = 0
		return val * 100

	def get_damage(self,amount):
		if not self.invincible:
			self.hit_sound.play()
			self.current_health -= amount
			self.invincible = True
			self.hurt_time = pygame.time.get_ticks()

	def invincibility_timer(self):
		if self.invincible:
			current_time = pygame.time.get_ticks()
			if current_time - self.hurt_time >= self.invincibility_duration:
				self.invincible = False

	def update(self):
		self.get_input()
		self.get_status()
		self.animate()
		self.dust_animation()
		self.invincibility_timer()

