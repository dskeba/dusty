
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
		self.x = 0
		self.y = 0
		self.angle = 0
		self.speed = 0
		self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer,default_layer=2)
		
	def __load_walls(self, tmx_data):
		self.walls = list()
		for object in tmx_data.objects:
			print("adding object w/ x: " + str(object.x) + " y:" + str(object.y))
			self.walls.append(pygame.Rect(object.x, object.y,object.width, object.height))
	
	def add_sprite(self, sprite):
		self.group.add(sprite)
		
	def update(self):
		for sprite in self.group.sprites():
			index = sprite.rect.collidelist(self.walls)
			if index > -1:
				print("COLLISION! w/ x: " + str(self.walls[index].x) + " y:" + str(self.walls[index].y))
			else:
				delta_x = math.cos(self.angle) * self.speed
				delta_y = math.sin(self.angle) * self.speed
				self.x = self.x + delta_x
				self.y = self.y - delta_y

	def draw(self, surface):
		rect = surface.get_rect()
		rect.left = self.x
		rect.top = self.y
		self.map_layer.draw(surface, rect)