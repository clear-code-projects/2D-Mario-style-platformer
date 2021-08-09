import pygame
from support import import_folder

class ParticleEffect(pygame.sprite.Sprite):
	def __init__(self,pos,type,speed = 0.5):
		super().__init__()
		if type == 'explosion':
			self.frames = import_folder('../graphics/enemy/explosion')
		if type == 'jump':
			self.frames = import_folder('../graphics/character/dust_particles/jump')
		if type == 'fall':
			self.frames = import_folder('../graphics/character/dust_particles/land')
		self.frame_index = 0
		self.speed = speed
		self.image = self.frames[self.frame_index]
		self.rect = self.image.get_rect(center = pos)

	def animate(self):
		self.frame_index += self.speed
		if self.frame_index >= len(self.frames):
			self.kill()
		else:
			self.image = self.frames[int(self.frame_index)]

	def update(self,shift):
		self.animate()
		self.rect.x += shift