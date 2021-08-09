import pygame 
import support

class Tile(pygame.sprite.Sprite):
	def __init__(self,size,x,y):
		super().__init__()
		self.image = pygame.Surface((size,size))
		self.rect = self.image.get_rect(topleft = (x,y))

	def update(self,shift):
		self.rect.x += shift

class StaticTile(Tile):
	def __init__(self,size,x,y,surface):
		super().__init__(size,x,y)
		self.image = surface 

class Crate(StaticTile):
	def __init__(self,size,x,y,surface):
		super().__init__(size,x,y,surface)
		offset_y = y + size
		self.rect = self.image.get_rect(bottomleft = (x,offset_y))

class AnimatedTile(Tile):
	def __init__(self,size,x,y,path):
		super().__init__(size,x,y)
		self.frames = support.import_folder(path)
		self.frame_index = 0
		self.image = self.frames[self.frame_index]

	def animate(self):
		self.frame_index += 0.15
		if self.frame_index >= len(self.frames):
			self.frame_index = 0
		self.image = self.frames[int(self.frame_index)]

	def update(self,shift):
		self.rect.x += shift
		self.animate()

class Coin(AnimatedTile):
	def __init__(self,size,x,y,value,path):
		super().__init__(size,x,y,path)
		center_x = x + int(size / 2)
		center_y = y + int(size / 2)
		self.rect = self.image.get_rect(center = (center_x,center_y))
		self.value = value

class Palm(AnimatedTile):
	def __init__(self,size,x,y,path,offset):
		super().__init__(size,x,y,path)
		y_offset = y - offset
		self.rect.topleft = (x,y_offset)




