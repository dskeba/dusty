
import pygame
import math
from Player import Player
from Map import Map
from SoundManager import SoundManager

class Game():

	def __init__(self, screen_width, screen_height, windowed, fps, double_buffered, sound_enabled):
		self.running = False
		self.screen_width = screen_width
		self.screen_height = screen_height
		self.screen_center_x = self.screen_width / 2
		self.screen_center_y = self.screen_height / 2
		self.screen_size = (self.screen_width, self.screen_height)
		self.windowed = windowed
		self.fps = fps
		self.double_buffered = double_buffered
		self.sound_enabled = sound_enabled
		self.mouse_x = 0
		self.mouse_y = 0
		self.key_down = {}
		pygame.init()
		self.init_keys()
		self.clock = pygame.time.Clock()
		if (self.windowed == True) & (self.double_buffered == True):
			pygame_options = pygame.HWSURFACE | pygame.DOUBLEBUF
		elif (self.windowed == True) & (self.double_buffered == False):
			pygame_options = pygame.HWSURFACE
		elif (self.windowed == False) & (self.double_buffered == True):
			pygame_options = pygame.HWSURFACE | pygame.FULLSCREEN | pygame.DOUBLEBUF
		elif (self.windowed == False) & (self.double_buffered == False):
			pygame_options = pygame.HWSURFACE | pygame.FULLSCREEN
		self.screen = pygame.display.set_mode(self.screen_size, pygame_options)
		self.sound_manager = SoundManager(self.sound_enabled)
		self.set_icon('icon.png')
		self.player = Player(self)
		self.map = Map('maps/dusty1/dusty1.tmx', self.screen)
		self.map.add_sprite(self.player)
		pygame.mouse.set_cursor(*pygame.cursors.broken_x)
		
	def set_icon(self, image):
		self.icon_surface = pygame.image.load(image)
		pygame.display.set_icon(self.icon_surface)
		
	def init_keys(self):
		self.key_down[pygame.K_w] = False
		self.key_down[pygame.K_s] = False
		self.key_down[pygame.K_LSHIFT] = False
		self.key_down[pygame.K_ESCAPE] = False
		self.key_down[pygame.K_SPACE] = False
		
	def run(self):
		self.running = True
		while self.running:
			self.input()
			self.simulate()
			self.update()
			self.draw()
			self.tick()
		self.cleanup()
	
	def input(self):
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.KEYDOWN:
				self.key_down[event.key] = True
			elif event.type == pygame.KEYUP:
				self.key_down[event.key] = False
		self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
		
	def simulate(self):
		if self.key_down[pygame.K_ESCAPE]:
			self.running = False
		if self.key_down[pygame.K_w] & self.key_down[pygame.K_LSHIFT]:
			self.player.action = Player.RUNNING
			self.player.speed = 3
		elif self.key_down[pygame.K_w]:
			self.player.action = Player.WALKING
			self.player.speed = 2
		elif self.key_down[pygame.K_s]:
			self.player.action = Player.BACKSTEPPING
			self.player.speed = -2
		else:
			self.player.action = Player.STANDING
			self.player.speed = 0
		dx = self.mouse_x - self.screen_center_x
		dy = self.mouse_y - self.screen_center_y
		angle = (math.atan2(dx, dy) * 180) / math.pi
		if (angle != self.player.angle) & (self.player.action == Player.STANDING):
			self.player.action = Player.ROTATING
		self.player.angle = angle
		self.player.simulate()
		
	def update(self):
		self.map.update()
		
	def draw(self):
		self.screen.fill((0, 0, 0))
		if self.player.action == Player.ROTATING:
			self.map.draw(self.screen)
		else:
			self.map.draw(self.screen, self.player.rect.center)
		pygame.display.flip()
		
	def tick(self):
		self.clock.tick(self.fps)
	
	def cleanup(self):
		pygame.quit()