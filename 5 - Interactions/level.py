import pygame, sys 
from tiles import Tile, StaticTile, Coin, Crate, Palm
from decoration import Sky, Water, Clouds
from enemy import Enemy
from particles import ParticleEffect
from player import Player
import support
from gui import UI
from random import randint
from settings import *

class Level:
	def __init__(self,level_data,surface,pos_index,load_map,tile_size = 64):
		self.tile_size = tile_size
		self.world_shift = 0
		self.current_x = None
		self.screen_width = screen_width
		self.screen_height = screen_height
		self.main_surface = surface
		
		# player setup
		player_layout = support.import_csv_layout(level_data['player'])
		self.player = pygame.sprite.GroupSingle()
		self.goal = pygame.sprite.GroupSingle()
		self.player_setup(player_layout)
		self.ui = UI()
		
		# dust 
		self.dust_sprite = pygame.sprite.GroupSingle()
		self.player_on_ground = False
		self.get_player_on_ground()

		# overworld connection
		self.pos_index = pos_index
		self.unlock_id = level_data['unlock']
		self.load_map = load_map

		# audio setup
		self.music = pygame.mixer.Sound('../audio/level_music.wav')
		self.music.play(loops = -1)


		self.stomp_sound = pygame.mixer.Sound('../audio/effects/stomp.wav')
		self.coin_sound = pygame.mixer.Sound('../audio/effects/coin.wav')

		# terrain setup
		terrain_layout = support.import_csv_layout(level_data['terrain'])
		self.terrain_sprites = self.create_tile_group(terrain_layout,'terrain')
		
		# objects setup 
		fg_palm_layout = support.import_csv_layout(level_data['fg palms'])
		self.fg_palm_sprites = self.create_tile_group(fg_palm_layout,'fg palms')
		
		# bg palm setup
		bg_palm_layout = support.import_csv_layout(level_data['bg palms'])
		self.bg_palm_sprites = self.create_tile_group(bg_palm_layout,'bg palms')

		# crate setup
		crate_layout = support.import_csv_layout(level_data['crates'])
		self.crate_sprites = self.create_tile_group(crate_layout,'crates')

		# coin setup
		coin_layout = support.import_csv_layout(level_data['coins'])
		self.coin_sprites = self.create_tile_group(coin_layout,'coins')

		# grass setup
		grass_layout = support.import_csv_layout(level_data['grass'])
		self.grass_sprites = self.create_tile_group(grass_layout,'grass')

		# enemy setup
		enemy_layout = support.import_csv_layout(level_data['enemies'])
		self.enemy_sprites = self.create_tile_group(enemy_layout,'enemies')
		self.particle_explosion = pygame.sprite.Group()

		# constraint 
		constraint_layout = support.import_csv_layout(level_data['constraints'])
		self.constraint_sprites = self.create_tile_group(constraint_layout,'constraints')

		# decoration
		self.sky = Sky(8)
		level_width = len(terrain_layout[0]) * tile_size
		self.water = Water(680,level_width)
		self.clouds = Clouds(500,20,level_width)

	def create_tile_group(self,layout,type):
		sprite_group = pygame.sprite.Group()

		for row_index, row in enumerate(layout):
			for col_index, cell in enumerate(row):
				if cell != '-1':
					x = col_index * self.tile_size
					y = row_index * self.tile_size

					if type == 'terrain':
						terrain_graphic_list = support.import_cut_graphic('../graphics/terrain/terrain_tiles.png')
						surface = terrain_graphic_list[int(cell)]
						sprite = StaticTile(self.tile_size,x,y,surface)	
					
					if type == 'coins':
						if cell == '0': 
							sprite = Coin(self.tile_size,x,y,5,'../graphics/coins/gold')
						elif cell == '1': 
							sprite = Coin(self.tile_size,x,y,1,'../graphics/coins/silver') 
					
					if type == 'fg palms':
						if cell == '1':
							sprite = Palm(self.tile_size,x,y,'../graphics/terrain/palm_small',38)
						if cell == '2':
							sprite = Palm(self.tile_size,x,y,'../graphics/terrain/palm_large',64)
					
					if type == 'bg palms':
						sprite = Palm(self.tile_size,x,y,'../graphics/terrain/palm_bg',64)
					if type == 'crates':		
						surface = pygame.image.load('../graphics/terrain/crate.png').convert_alpha()
						sprite = Crate(self.tile_size,x,y,surface)

					if type == 'enemies':
						sprite = Enemy(self.tile_size, x, y, '../graphics/enemy/run',randint(3,5))
					if type == 'constraints': 
						sprite = Tile(self.tile_size,x,y)

					if type == 'grass':
						grass_surface_list = support.import_cut_graphic('../graphics/decoration/grass/grass.png')
						surface = grass_surface_list[int(cell)]
						sprite = StaticTile(self.tile_size,x,y,surface)
					
					sprite_group.add(sprite)

		return sprite_group

	def enemy_collision_reverse(self):
		for enemy in self.enemy_sprites.sprites():
			if pygame.sprite.spritecollide(enemy,self.constraint_sprites, False):
				enemy.reverse()

	def player_setup(self,layout):
		for row_index, row in enumerate(layout):
			for col_index, cell in enumerate(row):
				if cell == '0':
					x = col_index * self.tile_size
					y = row_index * self.tile_size
					sprite = Player((x,y),100,self.main_surface,self.create_jump_dust)
					self.player.add(sprite)
				if cell == '1':
					x = col_index * self.tile_size
					y = row_index * self.tile_size
					surface = pygame.image.load('../graphics/character/hat.png').convert_alpha()
					sprite = StaticTile(10,x,y,surface)
					self.goal.add(sprite)

	def player_collision_x(self):
		player = self.player.sprite
		player.rect.x += player.direction.x * player.speed
		collision_sprites = self.terrain_sprites.sprites() + self.crate_sprites.sprites() + self.fg_palm_sprites.sprites()
		for sprite in collision_sprites:
			if sprite.rect.colliderect(player.rect):
				if player.direction.x < 0:
					player.rect.left = sprite.rect.right
					player.on_left = True
					self.current_x = player.rect.left
				elif player.direction.x > 0:
					player.rect.right = sprite.rect.left
					player.on_right = True
					self.current_x = player.rect.right

		if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0) :
			player.on_left = False
		if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
			player.on_right = False

	def player_collision_y(self):
		player = self.player.sprite
		
		player.apply_gravity()
		player.rect.y += player.direction.y

		collision_sprites = self.terrain_sprites.sprites() + self.crate_sprites.sprites() + self.fg_palm_sprites.sprites()
		for sprite in collision_sprites:
			if sprite.rect.colliderect(player.rect):
				if player.direction.y >= 0:
					player.on_ground = True
					player.rect.bottom = sprite.rect.top
					player.direction.y = 0
				elif player.direction.y < 0:
					player.rect.top = sprite.rect.bottom
					player.direction.y = 0
					player.on_ceiling = True
		
		if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
			player.on_ground = False
		if player.on_ceiling and player.direction.y > 0.1:
			player.on_ceiling = False

	def create_jump_dust(self,pos):
		if self.player.sprite.facing_right:
			pos -= pygame.math.Vector2(10,5)
		else:
			pos += pygame.math.Vector2(10,-5)
		jump_dust_sprite = ParticleEffect(pos,'jump')
		self.dust_sprite.add(jump_dust_sprite)

	def get_player_on_ground(self):
		if self.player.sprite.on_ground:
			self.player_on_ground = True
		else:
			self.player_on_ground = False

	def create_land_dust(self):
		if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
			if self.player.sprite.facing_right: 
				offset = pygame.math.Vector2(10,15)
			else: 
				offset = pygame.math.Vector2(-10,15)
			fall_dust_sprite = ParticleEffect(self.player.sprite.rect.midbottom - offset,'fall')
			self.dust_sprite.add(fall_dust_sprite)

	def level_scroll_x(self):
		player = self.player.sprite
		player_x = player.rect.centerx
		direction_x = player.direction.x

		if player_x < self.screen_width / 4 and direction_x < 0:
			self.world_shift = 8
			player.speed = 0
		elif player_x > self.screen_width - (self.screen_width / 3) and direction_x > 0:
			self.world_shift = -8
			player.speed = 0
		else:
			player.speed = 8
			self.world_shift = 0

	def check_death(self):
		player_y = self.player.sprite.rect.top
		if player_y > self.screen_height + 50:
			self.load_map(self.pos_index,0)
			self.music.stop()
		if self.player.sprite.current_health <= 0:
			self.load_map(self.pos_index,0)
			self.music.stop()

	def win_level(self):
		if pygame.sprite.spritecollide(self.player.sprite,self.goal,True):
			self.load_map(self.pos_index,self.unlock_id)
			self.music.stop()

	def check_player_collision(self):
		enemy_collisions = pygame.sprite.spritecollide(self.player.sprite,self.enemy_sprites,False)

		if enemy_collisions:
			for enemy in enemy_collisions:
				if enemy.rect.top - 8 <= self.player.sprite.rect.bottom <= enemy.rect.top + 12 and self.player.sprite.direction.y > 0:
					self.stomp_sound.play()
					self.player.sprite.direction.y = -15
					explosion_sprite = ParticleEffect(enemy.rect.center,'explosion',0.5)
					self.particle_explosion.add(explosion_sprite)
					enemy.kill()

				else:
					if enemy.rect.centerx > self.player.sprite.rect.centerx:
						self.player.sprite.get_damage(10)
					else:
						self.player.sprite.get_damage(10)

	def check_coin_collisions(self):
		collided_coins = pygame.sprite.spritecollide(self.player.sprite,self.coin_sprites,True)
		if collided_coins:
			self.coin_sound.play()
			for coin in collided_coins:
				self.player.sprite.coins += coin.value

	def run(self):
		self.sky.draw(self.main_surface)
		self.clouds.draw(self.main_surface,self.world_shift)

		self.grass_sprites.update(self.world_shift)
		self.grass_sprites.draw(self.main_surface)

		self.bg_palm_sprites.update(self.world_shift)
		self.bg_palm_sprites.draw(self.main_surface)

		self.dust_sprite.update(self.world_shift)
		self.dust_sprite.draw(self.main_surface)

		self.crate_sprites.update(self.world_shift)
		self.crate_sprites.draw(self.main_surface)

		self.enemy_sprites.update(self.world_shift)
		self.constraint_sprites.update(self.world_shift)
		self.enemy_sprites.draw(self.main_surface)
		self.enemy_collision_reverse()
		
		self.terrain_sprites.update(self.world_shift)
		self.terrain_sprites.draw(self.main_surface)
	
		self.coin_sprites.update(self.world_shift)	
		self.coin_sprites.draw(self.main_surface)

		self.fg_palm_sprites.update(self.world_shift)
		self.fg_palm_sprites.draw(self.main_surface)

		self.particle_explosion.update(self.world_shift)
		self.particle_explosion.draw(self.main_surface)

		self.player.update()
		self.player_collision_x()
		self.get_player_on_ground()
		self.player_collision_y()
		self.create_land_dust()
		self.level_scroll_x()
		self.player.draw(self.main_surface)
		
		self.ui.show_health(self.main_surface,self.player.sprite.current_health,self.player.sprite.max_health)
		self.ui.show_coins(self.main_surface,self.player.sprite.coins)
		self.check_coin_collisions()

		self.check_death()
		self.win_level()
		self.goal.update(self.world_shift)
		self.goal.draw(self.main_surface)
		self.check_player_collision()

		self.water.draw(self.main_surface,self.world_shift)
