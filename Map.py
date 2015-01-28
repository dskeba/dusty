
import pygame
import pytmx
import pyscroll
import math

class Map():
	
	def __init__(self, filename, screen):
		self.tmx_data = pytmx.load_pygame(filename)
		self.load_objects(self.tmx_data)
		map_data = pyscroll.data.TiledMapData(self.tmx_data)
		self.map_layer = pyscroll.BufferedRenderer(map_data, screen.get_size())
		self.screen = screen
		self.screen_x = 0
		self.screen_y = 0
		self.group = pyscroll.PyscrollGroup(map_layer = self.map_layer, default_layer = 2)
		
	def load_objects(self, tmx_data):
		self.objects = list()
		for object in tmx_data.objects:
			self.objects.append(object)
	
	def add_sprite(self, sprite):
		self.group.add(sprite)
		
	def update(self):
		self.group.update(0)
		for sprite in self.group.sprites():
			for object in self.objects:
				if object.type == 'tree':
					tree_rect = pygame.Rect(object.x, object.y, object.width, object.height)
					if tree_rect.collidepoint(sprite.rect.center):
						sprite.move_back()
				elif object.type == 'collide':
					collide_rect = pygame.Rect(object.x, object.y, object.width, object.height)
					if collide_rect.collidepoint(sprite.rect.center):
						sprite.move_back()

	def draw(self, surface, center = None):
		if center:
			self.group.center(center)
		self.group.draw(surface)