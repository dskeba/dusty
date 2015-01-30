
import pygame
import pyganim
import math
import os
from Inventory import Inventory
from Item import Item

class Player(pygame.sprite.Sprite):

	STANDING = 0
	WALKING = 1
	RUNNING = 2
	ROTATING = 3
	BACKSTEPPING = 4
	PRIMARY_ROCK = 10
	
	NONE = 0
	PRIMARY = 1
	SECONDARY = 2

	def __init__(self, game):
		pygame.sprite.Sprite.__init__(self)
		self.width = 80
		self.height = 80
		self.game = game
		self.sound_manager = self.game.sound_manager
		self.screen = self.game.screen
		self.map_x = 500
		self.old_map_x = 0
		self.map_y = 500
		self.old_map_y = 0
		self.rect = pygame.Rect(self.width, self.height, 0, 0)
		self.start_angle = 180
		self.angle = 0
		self.speed = 0
		self.state = self.STANDING
		self.inventory = Inventory()
		self.inventory.add_active(Item('rock'))
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
		self.running_stone_anim = pyganim.PygAnimation([('sprites/man_running_stone_1.png', 0.1),
												  ('sprites/man_running_stone_2.png', 0.1),
												  ('sprites/man_running_stone_3.png', 0.1),
												  ('sprites/man_running_stone_4.png', 0.1),
												  ('sprites/man_running_stone_5.png', 0.1),
												  ('sprites/man_running_stone_6.png', 0.1)])
		self.primary_stone_anim = pyganim.PygAnimation([('sprites/man_primary_stone_1.png', 0.2),
												  ('sprites/man_primary_stone_2.png', 0.2),
												  ('sprites/man_primary_stone_3.png', 0.2),
												  ('sprites/man_primary_stone_4.png', 0.2),
												  ('sprites/man_primary_stone_5.png', 0.2)])
		self.current_anim = self.walking_anim
		self.action_step = 0
		self.footsteps = self.sound_manager.load('sounds/footstep.wav')
		
	def simulate(self):
		if self.state == Player.RUNNING:
			self.current_anim.pause()
			if self.inventory.is_holding_item():
				if self.inventory.get_holding_item().type == 'rock':
					self.current_anim = self.running_stone_anim
			else:
				self.current_anim = self.running_anim
			self.current_anim.play()
			self.sound_manager.set_volume(self.footsteps, 0.4)
			self.sound_manager.play(self.footsteps, True)
		elif self.state == Player.WALKING:
			self.current_anim.pause()
			if self.inventory.is_holding_item():
				if self.inventory.get_holding_item().type == 'rock':
					self.current_anim = self.running_stone_anim
			else:
				self.current_anim = self.walking_anim
			self.current_anim.play()
			self.sound_manager.set_volume(self.footsteps, 0.2)
			self.sound_manager.play(self.footsteps, True)
		elif self.state == Player.STANDING:
			self.current_anim.pause()
			if self.inventory.is_holding_item():
				if self.inventory.get_holding_item().type == 'rock':
					self.current_anim = self.running_stone_anim
			else:
				self.current_anim = self.walking_anim
			self.current_anim.stop()
			self.sound_manager.stop(self.footsteps, True)
		elif self.state == Player.BACKSTEPPING:
			self.current_anim.pause()
			if self.inventory.is_holding_item():
				if self.inventory.get_holding_item().type == 'rock':
					self.current_anim = self.running_stone_anim
			else:
				self.current_anim = self.walking_anim
			self.current_anim.play()
			self.sound_manager.set_volume(self.footsteps, 0.2)
			self.sound_manager.play(self.footsteps, True)
		elif self.state == Player.ROTATING:
			self.current_anim.pause()
			if self.inventory.is_holding_item():
				if self.inventory.get_holding_item().type == 'rock':
					self.current_anim = self.running_stone_anim
			else:
				self.current_anim = self.walking_anim
			self.current_anim.stop()
			self.sound_manager.stop(self.footsteps, True)
		elif self.state == Player.PRIMARY_ROCK:
			self.action_step = self.action_step + 1
			if self.action_step > 60:
				self.action_step = 0
				self.current_anim.stop()
			else:
				self.current_anim.pause()
				self.current_anim = self.primary_stone_anim
				self.current_anim.play()
			
	def set_holding_slot(self, slot):
		self.action_step = 0
		if self.inventory.get_holding_slot() == slot:
			self.inventory.set_holding_slot(-1)
		else:
			self.inventory.set_holding_slot(slot)
			
	def set_action(self, action):
		if self.action_step > 0:
			return
		if self.inventory.is_holding_item():
			if self.inventory.get_holding_item().type == 'rock':
				if action == Player.PRIMARY:
					self.state = Player.PRIMARY_ROCK
					self.action_step = 1
					self.speed = 0
			
	def set_state(self, state):
		if self.action_step > 0:
			return
		if state == Player.RUNNING:
			self.state = Player.RUNNING
			self.speed = 3
		elif state == Player.WALKING:
			self.state = Player.WALKING
			self.speed = 2
		elif state == Player.BACKSTEPPING:
			self.state = Player.BACKSTEPPING
			self.speed = -2
		elif state == Player.STANDING:
			self.state = Player.STANDING
			self.speed = 0
			
	def get_state(self):
		return self.state
			
	def set_angle(self, angle):
		if (angle != self.angle) & (self.state == Player.STANDING):
			self.state = Player.ROTATING
		self.angle = angle
			
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
		
		