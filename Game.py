
import pygame
import Player
import Map

class Game():

	def __init__(self, screen_width = 1024, screen_height = 768, fullscreen = True, fps = 60):
		self.running = False
		self.screen_width = screen_width
		self.screen_height = screen_height
		self.screen_center_x = self.screen_width / 2
		self.screen_center_y = self.screen_height / 2
		self.screen_size = (self.screen_width, self.screen_height)
		self.fullscreen = fullscreen
		self.fps = fps
		self.mouse_x = 0
		self.mouse_y = 0
		self.key_down = {}
		pygame.init()
		self.init_keys()
		self.clock = pygame.time.Clock()
		if self.fullscreen:
			pygame_options = pygame.HWSURFACE | pygame.FULLSCREEN
		else:
			pygame_options = pygame.HWSURFACE
		self.screen = pygame.display.set_mode(self.screen_size, pygame_options)
		self.set_icon('icon.png')
		self.player = Player.Player(self.screen_center_x, self.screen_center_y)
		self.group = pygame.sprite.Group(self.player)
		
	def set_icon(self, image):
		self.icon_surface = pygame.image.load(image)
		pygame.display.set_icon(self.icon_surface)
		
	def init_keys(self):
		self.key_down[pygame.K_w] = False
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
		elif self.key_down[pygame.K_w]:
			self.player.action = Player.WALKING
		else:
			self.player.action = Player.STANDING
		dx = self.mouse_x - self.screen_center_x
		dy = self.mouse_y - self.screen_center_y
		self.player.angle = (math.atan2(dx, dy) * 180) / math.pi
		self.player.simulate()
		
	def update(self):
		self.group.update()
		
	def draw(self):
		self.screen.fill((0, 0, 0))
		self.group.draw(self.screen)
		pygame.display.flip()
		
	def tick(self):
		self.clock.tick(self.fps)
		print("FPS: " + str(self.clock.get_fps()))
	
	def cleanup(self):
		pygame.quit()