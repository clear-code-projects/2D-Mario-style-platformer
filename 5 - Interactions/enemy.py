import pygame
from tiles import AnimatedTile
from support import import_folder

class Enemy(AnimatedTile):
	def __init__(self,size,x,y,path,speed):
		super().__init__(size,x,y,path)
		self.rect.y += self.rect.height - self.image.get_size()[1]
		self.speed = speed

	def move(self):
		self.rect.x += self.speed

	def reverse(self):
		self.speed *= -1

	def reverse_image(self):
		if self.speed > 0:
			self.image = pygame.transform.flip(self.image,True,False) 

	def update(self,shift):
		self.animate()
		self.move()
		self.reverse_image()
		self.rect.x += shift
