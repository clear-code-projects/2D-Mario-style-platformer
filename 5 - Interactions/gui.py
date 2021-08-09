import pygame 

class UI:
	def __init__(self):
		# health 
		self.start = pygame.image.load('../graphics/ui/ui_start.png').convert_alpha()
		self.middle = pygame.image.load('../graphics/ui/ui_middle.png').convert_alpha()
		self.end = pygame.image.load('../graphics/ui/ui_end.png').convert_alpha()
		self.health_bar_color = '#dc4949'
		self.bar_rect_topleft = (54,38)
		self.bar_max_with = 152
		self.bar_height = 4

		# coins
		self.coin_surf = pygame.image.load('../graphics/ui/coin.png').convert_alpha()
		self.coin_rect = self.coin_surf.get_rect(topleft = (50,60))
		self.font = pygame.font.Font('../graphics/ui/ARCADEPI.ttf',30)
		self.font_color = '#33323d'

	def draw_health_bg(self,surface):
		surface.blit(self.start,(20,10))
		surface.blit(self.middle,(84,10))
		surface.blit(self.end,(84 + 64,10))

	def health_bar(self,surface,current,full):
		current_health_ratio = current / full
		current_bar_width = self.bar_max_with * current_health_ratio
		pygame.draw.rect(surface,self.health_bar_color,pygame.Rect(self.bar_rect_topleft,(current_bar_width,self.bar_height)))

	def show_health(self,surface,current,full):
		self.draw_health_bg(surface)
		self.health_bar(surface,current,full)

	def show_coins(self,surface,amount):
		surface.blit(self.coin_surf,self.coin_rect)
		coin_amount_surf = self.font.render(str(amount),False,self.font_color)
		coin_amount_rect = coin_amount_surf.get_rect(midleft = (self.coin_rect.right + 4,self.coin_rect.centery))
		surface.blit(coin_amount_surf,coin_amount_rect)

