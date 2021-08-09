import pygame
from os import walk
from csv import reader

def import_folder(path):
	surface_list = []

	for _, __, img_files in walk(path): 
		for image in img_files:
			full_path = path + '/' + image
			image_surf = pygame.image.load(full_path).convert_alpha()
			surface_list.append(image_surf)

	return surface_list		

def import_csv_layout(path):
	terrain_map = []
	with open(path) as map:
		level = reader(map,delimiter = ',')
		for row in level:
			terrain_map.append(list(row))
		return terrain_map

def import_cut_graphic(path, tile_width = 64, tile_height = 64):
	surface = pygame.image.load(path).convert_alpha()
	tile_num_x = int(surface.get_size()[0] / tile_width)
	tile_num_y = int(surface.get_size()[1] / tile_height)
	cut_tiles = []

	for row in range(tile_num_y):
		for col in range(tile_num_x):
			x = col * tile_width
			y = row * tile_height
			new_surf = pygame.Surface((tile_width,tile_height),flags = pygame.SRCALPHA)
			new_surf.blit(surface,(0,0),pygame.Rect(x,y,64,64))
			cut_tiles.append(new_surf)
	return cut_tiles