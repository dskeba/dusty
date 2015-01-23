
try: #python3
	import tkinter as tkinter
except: #python2
	import Tkinter as tkinter
	
class Launcher():
	
	def __init__(self, callback):
		self.callback = callback
		self.gui = tkinter.Tk()
		self.gui.title("DUSTY")
		logo_photo = tkinter.PhotoImage(file = "images/dusty.gif")
		logo_label = tkinter.Label(image = logo_photo)
		logo_label.pack()
		settings_frame = tkinter.Frame(height = 2, bd = 1, relief = tkinter.GROOVE)
		settings_frame.pack(fill = tkinter.X, padx = 5, pady = 5)
		resolution_label = tkinter.Label(settings_frame, text = "Resolution:")
		resolution_label.pack()
		self.resolution_var = tkinter.StringVar()
		self.resolution_var.set("1280 x 720 (16:9)")
		resolution_options = tkinter.OptionMenu(settings_frame, self.resolution_var, 
											   "800 x 600 (4:3)", 
											   "1024 x 768 (4:3)",
											   "1152 x 864 (4:3)", 
											   "1400 x 1050 (4:3)", 
											   "1280 x 720 (16:9)", 
											   "1366 x 768 (16:9)", 
											   "1600 x 900 (16:9)", 
											   "1920 x 1080 (16:9)")
		resolution_options.pack()
		fps_label = tkinter.Label(settings_frame, text="FPS Limit:")
		fps_label.pack()
		self.fps_var = tkinter.StringVar()
		self.fps_var.set("60")
		fps_options = tkinter.OptionMenu(settings_frame, self.fps_var, 
											   "30", 
											   "60",
											   "120",
											   "240")
		fps_options.pack()
		self.windowed_var = tkinter.StringVar()
		self.windowed_var.set(0)
		windowed_checkbutton = tkinter.Checkbutton(settings_frame, text = "Windowed", variable = self.windowed_var)
		windowed_checkbutton.pack()
		self.double_buffered_var = tkinter.IntVar()
		self.double_buffered_var.set(1)
		double_buffered_checkbutton = tkinter.Checkbutton(settings_frame, text = "Double Buffered", variable = self.double_buffered_var)
		double_buffered_checkbutton.pack()
		self.sound_enabled_var = tkinter.IntVar()
		self.sound_enabled_var.set(1)
		sound_enabled_checkbutton = tkinter.Checkbutton(settings_frame, text = "Sound Enabled", variable = self.sound_enabled_var)
		sound_enabled_checkbutton.pack()
		play_button = tkinter.Button(settings_frame, text = "Play", command = self.play)
		play_button.pack()
		self.gui.mainloop()
		
	def play(self):
		self.destroy()
		if self.windowed_var.get() == '1':
			windowed = True
		else:
			windowed = False
		self.callback(self.resolution_var.get(), float(self.fps_var.get()), windowed, self.double_buffered_var.get(), self.sound_enabled_var.get())
		
	def destroy(self):
		self.gui.destroy()