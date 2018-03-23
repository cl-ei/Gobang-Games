"""
This script is writen for generation an executable file
for windows operation system by cxFreeze.

"""

import os
from cx_Freeze import setup, Executable


base = "Win32GUI"
setup(
    name="hello",
    version="0.1",
    description="the typical 'Hello, world!'",
    executables=[
        Executable("main.py", base=base, icon="./sourcefile/gobang.ico")
    ]
)
