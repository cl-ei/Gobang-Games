import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "packages": ["os"],
    "excludes": ["tkinter"]
}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = 'Win32GUI'


setup(
    name="retrosnaker",
    author="caoliang",
    author_email="i@caoliang.net",
    version="1.0.0",
    description="a tiny game.",
    install_requires=[
        "pygames",
    ],
    options={
        "build_exe": {
            "include_files": ["cl.ttf", "head.png"]
        }
    },
    executables=[
        Executable('main.py', base=base, icon='snake.ico')
    ],
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
)
