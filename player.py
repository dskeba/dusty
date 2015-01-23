
import pygame
import pyganim
import math
import os

class player(pygame.sprite.Sprite):

	STANDING = 0
	WALKING = 1
	RUNNING = 2
	ROTATING = 3
	BACKSTEPPING = 4

	def __init__(self, screen):
		pygame.sprite.Sprite.__init__(self)
		self.width = 80
		self.height = 80
		self.screen = screen
		self.map_x = 500
		self.old_map_x = 0
		self.map_y = 500
		self.old_map_y = 0
		self.rect = pygame.Rect(self.width, self.height, 0, 0)
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
		pygame.mixer.pre_init()
		self.channel = pygame.mixer.Channel(0)
		self.channel.set_volume(0.25)
		self.footsteps = pygame.mixer.Sound('sounds/footstep.wav')
		
	def simulate(self):
		if self.action == player.RUNNING:
			self.walking_anim.pause()
			self.running_anim.play()
			self.current_anim = self.running_anim
			if not self.channel.get_busy():
				self.channel.play(self.footsteps)
		elif self.action == player.WALKING:
			self.walking_anim.play()
			self.running_anim.pause()
			self.current_anim = self.walking_anim
			if not self.channel.get_busy():
				self.channel.play(self.footsteps)
		elif self.action == player.STANDING:
			self.walking_anim.stop()
			self.running_anim.stop()
			self.current_anim = self.walking_anim
			self.channel.stop()
		elif self.action == player.BACKSTEPPING:
			self.walking_anim.play()
			self.running_anim.pause()
			self.current_anim = self.walking_anim
			if not self.channel.get_busy():
				self.channel.play(self.footsteps)
			
	def move_back(self):
		self.map_x = self.old_map_x
		self.map_y = self.old_map_y
		self.rect.left = self.map_x - (self.rect.width/2)
		self.rect.top = self.map_y - (self.rect.height/2)
			
	def update(self, dt):
		self.image = pygame.transform.rotate(self.current_anim.getCurrentFrame(), (self.angle + self.start_angle))
		self.rect.width = self.image.get_width()
		self.rect.height = self.image.get_height()
		radians = math.radians(self.angle - 90) 
		delta_x = math.cos(radians) * self.speed
		delta_y = math.sin(radians) * self.speed
		self.old_map_x = self.map_x
		self.old_map_y = self.map_y
		self.map_x = self.map_x + delta_x
		self.map_y = self.map_y - delta_y
		self.rect.left = self.map_x - (self.rect.width/2)
		self.rect.top = self.map_y - (self.rect.height/2)
		
		