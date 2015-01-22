
import pygame
import pytmx
import pyscroll
import math

class map():
	
	def __init__(self, filename, screen):
		tmx_data = pytmx.load_pygame(filename)
		self.__load_walls(tmx_data)
		map_data = pyscroll.data.TiledMapData(tmx_data)
		self.map_layer = pyscroll.BufferedRenderer(map_data, screen.get_size())
		self.screen_x = 0
		self.screen_y = 0
		self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer,default_layer=2)
		
	def __load_walls(self, tmx_data):
		self.walls = list()
		for object in tmx_data.objects:
			print("adding object w/ x: " + str(object.x) + " y:" + str(object.y))
			self.walls.append(pygame.Rect(object.x, object.y, object.width, object.height))
	
	def add_sprite(self, sprite):
		self.group.add(sprite)
		
	def update(self):
		self.group.update(0)
		for sprite in self.group.sprites():
			for wall in self.walls:
				if wall.collidepoint(sprite.rect.center):
					sprite.move_back()
					
			#idx = sprite.rect.collidelist(self.walls)
			#if idx > -1:
			#	print("sprite left: " + str(sprite.rect.left) + " top: " + str(sprite.rect.top))
			#	print("COLLISION! w/ x: " + str(self.walls[idx].x) + " y:" + str(self.walls[idx].y))

	def draw(self, surface, center = None):
		#rect = surface.get_rect()
		#rect.left = self.screen_x
		#rect.top = self.screen_y
		if center:
			self.group.center(center)
		self.group.draw(surface)