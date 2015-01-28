
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
		self.key_down = {}
		self.key_down[pygame.K_1] = False
		self.key_down[pygame.K_2] = False
		self.key_down[pygame.K_w] = False
		self.key_down[pygame.K_s] = False
		self.key_down[pygame.K_LSHIFT] = False
		self.key_down[pygame.K_ESCAPE] = False
		self.key_down[pygame.K_SPACE] = False
		self.key_up = {}
		self.key_up[pygame.K_1] = False
		self.key_up[pygame.K_2] = False
		self.key_up[pygame.K_w] = False
		self.key_up[pygame.K_s] = False
		self.key_up[pygame.K_LSHIFT] = False
		self.key_up[pygame.K_ESCAPE] = False
		self.key_up[pygame.K_SPACE] = False
		self.mouse_down = {}
		self.mouse_down[1] = False
		self.mouse_down[3] = False
		self.mouse_up = {}
		self.mouse_up[1] = False
		self.mouse_up[3] = False
		
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
		for key in self.key_up:
			self.key_up[key] = False
		for button in self.mouse_up:
			self.mouse_up[button] = False
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.KEYDOWN:
				self.key_down[event.key] = True
			elif event.type == pygame.KEYUP:
				self.key_up[event.key] = True
				self.key_down[event.key] = False
			elif event.type == pygame.MOUSEBUTTONDOWN:
				self.mouse_down[event.button] = True
			elif event.type == pygame.MOUSEBUTTONUP:
				self.mouse_up[event.button] = True
				self.mouse_down[event.button] = False
		self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
		
	def simulate(self):
		# Check for game quit
		if self.key_down[pygame.K_ESCAPE]:
			self.running = False
		# Check for inventory keys
		if self.key_up[pygame.K_1]:
			self.player.set_holding_slot(0)
		elif self.key_up[pygame.K_2]:
			self.player.set_holding_slot(1)
		# Check for movement keys
		if self.key_down[pygame.K_w] & self.key_down[pygame.K_LSHIFT]:
			self.player.set_state(Player.RUNNING)
		elif self.key_down[pygame.K_w]:
			self.player.set_state(Player.WALKING)
		elif self.key_down[pygame.K_s]:
			self.player.set_state(Player.BACKSTEPPING)
		else:
			self.player.set_state(Player.STANDING)
		# check for mouse buttons
		if self.mouse_down[1]:
			self.player.set_action(Player.PRIMARY)
		elif self.mouse_down[3]:
			self.player.set_action(Player.SECONDARY)
		# calculate player direction from mouse coordinates
		dx = self.mouse_x - self.screen_center_x
		dy = self.mouse_y - self.screen_center_y
		angle = (math.atan2(dx, dy) * 180) / math.pi
		self.player.set_angle(angle)
		self.player.simulate()
		
	def update(self):
		self.map.update()
		
	def draw(self):
		self.screen.fill((0, 0, 0))
		if (self.player.get_state() == Player.ROTATING) | (self.player.get_state() == Player.PRIMARY_ROCK):
			print("not center")
			self.map.draw(self.screen)
		else:
			print("center")
			self.map.draw(self.screen, self.player.rect.center)
		pygame.display.flip()
		
	def tick(self):
		self.clock.tick(self.fps)
	
	def cleanup(self):
		pygame.quit()