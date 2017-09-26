import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"], "excludes": ["tkinter"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = 'Win32GUI'

options = {
   'build_exe':{
   'include_files':['cl.ttf','head.png']
   }   
}
executables = [
   Executable('game.py',base=base,icon='snake.ico')
]
setup(  name = "clsnake",
        version = "0.1",
        description = "a tiny game",
        options = options,
        executables = executables
      )