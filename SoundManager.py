
import pygame

class SoundManager():
	
	def __init__(self, enabled = True):
		self.enabled = enabled
		if self.enabled:
			pygame.mixer.pre_init()
		self.sounds = []
		self.channels = []
		self.num_channels = pygame.mixer.get_num_channels()
		for i in range(0, self.num_channels):
			self.channels.append(pygame.mixer.Channel(i))

	def load(self, filename):
		if self.enabled == False:
			return 0
		self.sounds.append(pygame.mixer.Sound(filename))
		return len(self.sounds) - 1
		
	def play(self, sound_id = 0, skip_busy = True, loops = 0, max_time = 0, fade_ms = 0):
		if self.enabled == False:
			return
		if skip_busy:
			if self.get_channel(sound_id):
				return
		self.sounds[sound_id].play(loops, max_time, fade_ms)
	
	def stop(self, sound_id = 0, fade_ms = 0):
		if self.enabled == False:
			return
		if fade_ms > 0:
			self.sounds[sound_id].fadeout(fade_ms)
		else:
			self.sounds[sound_id].stop()
	
	def get_channel(self, sound_id):
		if self.enabled == False:
			return 0
		for channel in self.channels:
			if channel.get_sound() == self.sounds[sound_id]:
				return channel
		return 0
	
	def get_volume(self, sound_id = 0):
		if self.enabled == False:
			return
		return self.sounds[sound_id].get_volume()
		
	def set_volume(self, sound_id = 0, value = 1.0):
		if self.enabled == False:
			return
		return self.sounds[sound_id].set_volume(value)
		
	def stop_all(self, fade_ms = 0):
		if self.enabled == False:
			return
		for sound in self.sounds:
			if fade_ms > 0:
				pygame.mixer.fadeout(fade_ms)
			else:
				pygame.mixer.stop()
				
	def quit(self):
		if self.enabled == False:
			return
		for sound in self.sounds:
			sound = None
		pygame.mixer.quit()