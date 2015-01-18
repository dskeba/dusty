
import pygame
import pytmx
import pyscroll
import math

class map():
	
	def __init__(self, filename, screen):
		tmx_data = pytmx.load_pygame(filename)
		map_data = pyscroll.data.TiledMapData(tmx_data)
		self.map_layer = pyscroll.BufferedRenderer(map_data, screen.get_size())
		self.x = 0
		self.y = 0
		self.angle = 0
		self.speed = 0

	def update(self):
		delta_x = math.cos(self.angle) * self.speed
		delta_y = math.sin(self.angle) * self.speed
		self.x = self.x + delta_x
		self.y = self.y - delta_y

	def draw(self, surface):
		rect = surface.get_rect()
		rect.left = self.x
		rect.top = self.y
		self.map_layer.draw(surface, rect)