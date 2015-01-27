
from Game import Game
from Launcher import Launcher

def main():
	menu = Launcher(play)

def play(resolution, fps, windowed, double_buffered, sound_enabled):
	res_width = 800
	res_height = 600
	if resolution == "800 x 600 (4:3)":
		res_width, res_height = 800, 600
	elif resolution == "1024 x 768 (4:3)":
		res_width, res_height = 1024, 768
	elif resolution == "1152 x 864 (4:3)":
		res_width, res_height = 1152, 864
	elif resolution == "1400 x 1050 (4:3)":
		res_width, res_height = 1400, 1050
	elif resolution == "1280 x 720 (16:9)":
		res_width, res_height = 1280, 720
	elif resolution == "1366 x 768 (16:9)":
		res_width, res_height = 1366, 768
	elif resolution == "1600 x 900 (16:9)":
		res_width, res_height = 1600, 900
	elif resolution == "1920 x 1080 (16:9)":
		res_width, res_height = 1920, 1080
	app = Game(res_width, res_height, windowed, fps, double_buffered, sound_enabled)
	app.run()
	
if __name__ == '__main__':
	main()