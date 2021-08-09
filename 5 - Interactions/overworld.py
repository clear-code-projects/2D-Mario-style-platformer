import pygame,sys 
from pygame.math import Vector2
import support
import game_data
from random import choice, randint
from decoration import Sky
from settings import *

class Node(pygame.sprite.Sprite):
	def __init__(self,pos,path):
		super().__init__()
		self.pos = pos 
		self.frames = support.import_folder(path)
		self.frame_index = 0
		self.image = self.frames[self.frame_index]
		self.rect = self.image.get_rect(center = pos)

		self.detection_zone = pygame.Rect(pos[0] - 2,pos[1] - 2,8,8)

	def animate(self):
		self.frame_index += 0.2
		if self.frame_index >= len(self.frames):
			self.frame_index = 0
		self.image = self.frames[int(self.frame_index)]

	def update(self,status):
		if status == 'available':
			self.animate()
		else:
			tint_surf = self.image.copy()
			tint_surf.fill((0,0,0),None,pygame.BLEND_RGBA_MULT)
			self.image.blit(tint_surf,(0,0))

class OverWorld:
	def __init__(self,nodes,start_id,load_level,max_level,surface):
		self.nodes = pygame.sprite.Group()
		for node in nodes: 
			node_sprite = Node(node[0],node[1])
			self.nodes.add(node_sprite)
		
		self.bg = BG(surface,12,6)

		self.current_id = start_id
		self.moving = False
		self.move_direction = Vector2(0,0)
		self.speed = 6
		self.max_level = max_level
		self.load_level = load_level
		self.surface = surface	

		# icon graphics
		self.icon_pos = self.nodes.sprites()[self.current_id].pos
		self.y_offset = 30
		self.icon_surf = pygame.image.load('../graphics/overworld/hat.png').convert_alpha()
		self.icon_rect = self.icon_surf.get_rect(midbottom = (self.icon_pos[0],self.icon_pos[1] - self.y_offset))	

		# audio setup
		self.music = pygame.mixer.Sound('../audio/overworld_music.wav')
		self.music.play(loops = -1)

	def draw_nodes(self):
		for index, node in enumerate(self.nodes.sprites()):
			if index <= self.max_level:	
				node.update('available')
			else:
				node.update('locked')
		self.nodes.draw(self.surface)

	def draw_path(self):
		if self.max_level > 0:
			points = [node.pos for index, node in enumerate(self.nodes) if index <= self.max_level]
			pygame.draw.lines(self.surface,'#a04f45',False,points,5)

	def draw_icon(self):
		x = self.icon_pos[0]
		y = self.icon_pos[1] - self.y_offset
		self.icon_rect.center = (x,y)
		self.surface.blit(self.icon_surf,self.icon_rect)
		#pygame.draw.circle(screen,'#F24B59',self.icon_pos,12)

	def update_icon_pos(self):
		if self.moving and self.move_direction:
			self.icon_pos += self.move_direction * self.speed
			target_node = self.nodes.sprites()[self.current_id]
			if target_node.detection_zone.collidepoint(self.icon_pos):
				self.moving = False
				self.move_direction = Vector2(0,0)
		else:
			self.icon_pos = self.nodes.sprites()[self.current_id].pos

	def get_movement_data(self,target):
		start = Vector2(self.nodes.sprites()[self.current_id].pos)

		if target == 'next':
			end = Vector2(self.nodes.sprites()[self.current_id + 1].pos)
		else:
			end = Vector2(self.nodes.sprites()[self.current_id - 1].pos)

		return (end - start).normalize()

	def get_input(self):
		keys = pygame.key.get_pressed()

		if not self.moving:
			if keys[pygame.K_RIGHT] and self.current_id < len(self.nodes) - 1 and self.current_id < self.max_level:
				self.move_direction = self.get_movement_data('next')
				self.current_id += 1
				self.moving = True
			elif keys[pygame.K_LEFT] and self.current_id > 0: 
				self.move_direction = self.get_movement_data('previous')
				self.current_id -= 1
				self.moving = True
			elif keys[pygame.K_SPACE]:
				self.load_level(game_data.levels[self.current_id],self.current_id)
				self.music.stop()

	def run(self):
		self.bg.draw()
		self.get_input()
		self.update_icon_pos()
		self.draw_path()
		self.draw_nodes()
		self.draw_icon()

class BG:
	def __init__(self,surface,palm_num,cloud_num):
		self.surface = surface
		self.sky = Sky(8)

		self.horizon = screen_width / 2

		palm_surfaces = support.import_folder('../graphics/overworld/palms')
		self.random_palms = [choice(palm_surfaces) for path in range(palm_num)]
		self.palm_rects = []
		for surface in self.random_palms:
			x = randint(0,self.surface.get_size()[0])
			y = self.horizon + randint(0,100)
			rect = surface.get_rect(midbottom = (x,y))
			self.palm_rects.append(rect)

		cloud_surfaces = support.import_folder('../graphics/overworld/clouds')
		self.random_clouds = [choice(cloud_surfaces) for path in range(cloud_num)]
		self.cloud_rects = []
		for surface in self.random_clouds:
			x = randint(0,self.surface.get_size()[0])
			y = randint(0,int(self.horizon - 50))
			rect = surface.get_rect(midbottom = (x,y))
			self.cloud_rects.append(rect)

	def draw_palms(self):
		for index in range(len(self.random_palms)):
			self.surface.blit(self.random_palms[index],self.palm_rects[index])

	def draw_clouds(self):
		for index in range(len(self.random_clouds)):
			self.surface.blit(self.random_clouds[index],self.cloud_rects[index])

	def draw(self):
		self.surface.fill('#ddc6a1')
		self.sky.draw(self.surface)
		self.draw_palms()
		self.draw_clouds()
