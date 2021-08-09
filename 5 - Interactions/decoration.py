import pygame 
import support
from tiles import StaticTile, AnimatedTile
from random import randint, choice
from settings import * 

class Sky:
	def __init__(self,horizon):
		self.top = pygame.image.load('../graphics/decoration/sky/sky_top.png').convert()
		self.bottom = pygame.image.load('../graphics/decoration/sky/sky_bottom.png').convert()
		self.middle = pygame.image.load('../graphics/decoration/sky/sky_middle.png').convert()

		self.tile_h = self.top.get_size()[1]
		self.total_y_tiles = int(screen_height / self.tile_h)
		self.horizon_line = horizon

		# Stretch 
		self.top = pygame.transform.scale(self.top,(screen_width,self.tile_h))
		self.bottom = pygame.transform.scale(self.bottom,(screen_width,self.tile_h))
		self.middle = pygame.transform.scale(self.middle,(screen_width,self.tile_h))
		
	def draw(self,surface):
		for row in range(self.total_y_tiles):
			y = row * self.tile_h
			if row < self.horizon_line: 
				surface.blit(self.top,(0,y))
			elif row == self.horizon_line: 
				surface.blit(self.middle,(0,y))
			else:
				surface.blit(self.bottom,(0,y))

class Water:
	def __init__(self,top,level_width):
		water_start = -screen_width
		water_tile_width = 192 
		tile_x_amount = int(((level_width + 400) - water_start) / water_tile_width)
		self.water_sprites = pygame.sprite.Group()
		
		for tile in range(tile_x_amount):
			x = tile * water_tile_width + water_start
			y = top
			sprite = AnimatedTile(192,x,y,'../graphics/decoration/water')
			self.water_sprites.add(sprite)

	def draw(self,surface,shift):
		self.water_sprites.update(shift)
		self.water_sprites.draw(surface)

class Clouds:
	def __init__(self,horizon,cloud_number,level_width):
		cloud_surf_list = support.import_folder('../graphics/decoration/clouds')
		min_x = -200
		max_x = level_width
		min_y = 0
		max_y = horizon
		self.cloud_sprites = pygame.sprite.Group()

		for cloud in range(cloud_number):
			cloud = choice(cloud_surf_list)
			x = randint(min_x,max_x)
			y = randint(min_y,max_y)
			sprite = StaticTile(0,x,y,cloud)
			self.cloud_sprites.add(sprite)


	def draw(self,surface,shift):
		self.cloud_sprites.update(shift)
		self.cloud_sprites.draw(surface)


