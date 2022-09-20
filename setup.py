import sys
import os
from cx_Freeze import setup, Executable

# ADD FILES
files = ['icon.ico','projet\modules','DATA','Doc-render','Doc-template','Graphic','prodect_list.db']

# TARGET
target = Executable(
    script="projet\main.py",
    base="Win32GUI",
    icon="icon.ico"
)


# SETUP CX FREEZE
setup(
    name = "EMHSMART",
    version = "1.0",
    description = "Modern GUI for Python applications",
    author = "Wanderson M. Pimenta",
    options = {'build_exe' : {'include_files' : files}},
    executables = [target]
    
)
