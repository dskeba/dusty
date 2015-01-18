
import pygame
import pyganim

class player(pygame.sprite.Sprite):

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
		self.walking_anim = pyganim.PygAnimation([('sprites/man_walking_1.png', 0.2),
												  ('sprites/man_walking_2.png', 0.2),
												  ('sprites/man_walking_3.png', 0.2),
												  ('sprites/man_walking_4.png', 0.2),
												  ('sprites/man_walking_5.png', 0.2),
												  ('sprites/man_walking_6.png', 0.2)])
		self.running_anim = pyganim.PygAnimation([('sprites/man_running_1.png', 0.1),
												  ('sprites/man_running_2.png', 0.1),
												  ('sprites/man_running_3.png', 0.1),
												  ('sprites/man_running_4.png', 0.1),
												  ('sprites/man_running_5.png', 0.1),
												  ('sprites/man_running_6.png', 0.1)])
		self.current_anim = self.walking_anim
		
	def simulate(self):
		if self.action == player.RUNNING:
			self.speed = 10
			self.walking_anim.pause()
			self.running_anim.play()
			self.current_anim = self.running_anim
		elif self.action == player.WALKING:
			self.speed = 5
			self.walking_anim.play()
			self.running_anim.pause()
			self.current_anim = self.walking_anim
		elif self.action == player.STANDING:
			self.speed = 0
			self.walking_anim.stop()
			self.running_anim.stop()
			self.current_anim = self.walking_anim
			
	def update(self):
		self.image = pygame.transform.rotate(self.current_anim.getCurrentFrame(), (self.angle + self.start_angle))
		self.rect.width = self.image.get_width()
		self.rect.height = self.image.get_height()
		self.rect.left = self.center_x - (self.rect.width / 2)
		self.rect.top = self.center_y - (self.rect.height / 2)