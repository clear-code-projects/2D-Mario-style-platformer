import pygame, sys
from settings import *
from level import Level
import game_data
from overworld import OverWorld

class Game:
	def __init__(self,game_data):
		self.max_level = 5
		self.get_nodes(game_data)
		self.overworld = OverWorld(self.nodes,0,self.load_level,self.max_level,screen)
		self.status = 'overworld'

	def get_nodes(self,levels):
		self.nodes = []
		for level in levels.values():
			self.nodes.append(level['node'])

	def load_level(self,level_data,pos_index):
		self.level = Level(level_data,screen,pos_index,self.load_map) 
		self.status = 'level'

	def load_map(self,pos_index,new_max):
		if new_max >= self.max_level: self.max_level = new_max
		self.overworld = OverWorld(self.nodes,pos_index,self.load_level,self.max_level,screen)
		self.status = 'overworld'

	def run(self):
		if self.status == 'overworld':
			self.overworld.run()
		elif self.status == 'level':
			self.level.run()

if __name__ == '__main__':
	pygame.init()
	screen = pygame.display.set_mode((screen_width,screen_height))
	clock = pygame.time.Clock()
	game = Game(game_data.levels)

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
		
		game.run()
		pygame.display.update()
		clock.tick(60)
