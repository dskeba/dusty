
import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"], "excludes": [], "include_files": ['icon.png',
																					'sprites',
																					'maps',
																					'sounds',
																					'images']}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "pygame",
        version = "0.13a",
        description = "pygame",
        options = {"build_exe": build_exe_options},
        executables = [Executable("main.py", base=base)])
		