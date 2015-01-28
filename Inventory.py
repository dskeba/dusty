
import pygame

class Inventory():

	def __init__(self, active_slots_max = 4, inactive_slots_max = 12):
		self.holding_slot = -1
		self.active_slots_max = active_slots_max
		self.inactive_slots_max = inactive_slots_max
		self.active_slots = 0
		self.inactive_slots = 0
		self.active = []
		for i in range(0, self.active_slots_max):
			self.active.append(None)
		self.inactive = []
		for i in range(0, self.inactive_slots_max):
			self.inactive.append(None)
		
	def add_active(self, item):
		if self.active_slots >= self.active_slots_max:
			return -1
		for i in range(0, self.active_slots_max):
			if self.active[i] == None:
				self.active[i] = item
				return i
		
	def add_inactive(self, item):
		if self.inactive_slots >= self.inactive_slots_max:
			return -1
		for i in range(0, self.inactive_slots_max):
			if self.inactive[i] == None:
				self.inactive[i] = item
				return i
				
	def remove_active(self, slot):
		if self.active[slot] == None:
			return None
		item = self.active[slot]
		self.active.remove(slot)
		return item
		
	def remove_inactive(self, slot):
		if self.inactive[slot] == None:
			return None
		item = self.inactive[slot]
		self.inactive.remove(slot)
		return item
		
	def set_holding_slot(self, slot):
		if self.active[slot] != None:
			self.holding_slot = slot
		else:
			self.holding_slot = -1
		
	def get_holding_slot(self):
		return self.holding_slot
		
	def get_holding_item(self):
		return self.active[self.holding_slot]
		
	def is_holding_item(self):
		if self.holding_slot > -1:
			return True
		else:
			return False
		
	def get_active(self, slot):
		return self.active[slot]
		
	def get_inactive(self, slot):
		return self.inactive[slot]