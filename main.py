
import pygame
import math
import pyganim

class Map():
	
	def __init__(self):
		pass

class Person(pygame.sprite.Sprite):

	STANDING = 0
	WALKING = 1
	RUNNING = 2

	def __init__(self, center_x, center_y):
		pygame.sprite.Sprite.__init__(self)
		width = 80
		height = 150
		self.center_x = center_x
		self.center_y = center_y
		self.rect = pygame.Rect(width, height, self.center_x - (width / 2), self.center_y - (height / 2))
		self.start_angle = 180
		self.angle = 0
		self.speed = 0
		self.action = self.STANDING
		self.walking_anim = pyganim.PygAnimation([('man_walking_1.png', 0.2),
												  ('man_walking_2.png', 0.2),
												  ('man_walking_3.png', 0.2),
												  ('man_walking_4.png', 0.2),
												  ('man_walking_5.png', 0.2),
												  ('man_walking_6.png', 0.2)])
		self.running_anim = pyganim.PygAnimation([('man_running_1.png', 0.1),
												  ('man_running_2.png', 0.1),
												  ('man_running_3.png', 0.1),
												  ('man_running_4.png', 0.1),
												  ('man_running_5.png', 0.1),
												  ('man_running_6.png', 0.1)])
		self.current_anim = self.walking_anim
		
	def simulate(self):
		if self.action == Person.RUNNING:
			self.speed = 10
			self.walking_anim.pause()
			self.running_anim.play()
			self.current_anim = self.running_anim
		elif self.action == Person.WALKING:
			self.speed = 5
			self.walking_anim.play()
			self.running_anim.pause()
			self.current_anim = self.walking_anim
		elif self.action == Person.STANDING:
			self.speed = 0
			self.walking_anim.stop()
			self.running_anim.stop()
			self.current_anim = self.walking_anim
			
	def update(self, dest):
		self.image = pygame.transform.rotate(self.current_anim.getCurrentFrame(), (self.angle + self.start_angle))
		self.rect.width = self.image.get_width()
		self.rect.height = self.image.get_height()
		self.rect.left = self.center_x - (self.rect.width / 2)
		self.rect.top = self.center_y - (self.rect.height / 2)
		dest.blit(self.image, self.rect)
		
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
		self.player = Person(self.screen_center_x, self.screen_center_y)
		
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
			self.render()
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
			self.player.action = Person.RUNNING
		elif self.key_down[pygame.K_w]:
			self.player.action = Person.WALKING
		else:
			self.player.action = Person.STANDING
		dx = self.mouse_x - self.screen_center_x
		dy = self.mouse_y - self.screen_center_y
		self.player.angle = (math.atan2(dx, dy) * 180) / math.pi
		self.player.simulate()
		
	def render(self):
		self.screen.fill((0, 0, 0))
		self.player.update(self.screen)
		pygame.display.flip()
		
	def tick(self):
		self.clock.tick(self.fps)
		print("FPS: " + str(self.clock.get_fps()))
	
	def cleanup(self):
		pygame.quit()
			
def main():
	game = Game(1600, 900, True, 60)
	game.run()

if __name__ == '__main__':
	main()