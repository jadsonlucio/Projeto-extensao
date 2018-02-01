import sys
import os
import scipy
from cx_Freeze import setup, Executable



os.environ['TCL_LIBRARY'] = r'C:\Users\Pain panda\AppData\Local\Programs\Python\Python36\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Users\Pain panda\AppData\Local\Programs\Python\Python36\tcl\tk8.6'

packages = ['matplotlib.backends.backend_tkagg',"os","sys","ctypes","win32con"]
addtional_mods = ['numpy.core._methods', 'numpy.lib.format','tkinter.filedialog','numpy.matlib','timeit']
include_files  = ['ico.ico']

include_files.append(r'C:\Users\Pain panda\AppData\Local\Programs\Python\Python36\tcl\tcl8.6')
include_files.append(r'C:\Users\Pain panda\AppData\Local\Programs\Python\Python36\tcl\tk8.6')
setup(
    name = "Extensão  2017",
    version = "0.0.1",
    description = "Program of Analysis of Time Series Meteorological Measures in Ufal Campus Arapiraca",
    author='Jadson Lucio',
    author_email='jadsonaluno@hotmail.com',
    url='https://github.com/jamsavio/extension_project',
    options = {'build_exe': {'packages':packages,'includes': addtional_mods,'include_files':include_files,'include_msvcr': True}},
    executables = [Executable("main.py", base = "Win32GUI",targetName="main.exe",icon='ico.ico')]
)
