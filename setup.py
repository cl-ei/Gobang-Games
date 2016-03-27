from cx_Freeze import setup, Executable
import os
base = "Win32GUI"

setup(
name = "hello",
version = "0.1",
description = "the typical 'Hello, world!'",
executables = [Executable("main.py",base = base,icon="./gobang.ico")])
