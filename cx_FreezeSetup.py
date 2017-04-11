#! python3

#make sure to have the freesansbold.ttf file in the same directory as the other files when attempting to create the executable
#it can be found at C://path//to//python//Lib//Site-packages//pygame

import cx_Freeze
import os
import sys

os.environ['TCL_LIBRARY'] = 'C:\\path\\to\\python\\tcl\\tcl8.6'
os.environ['TK_LIBRARY'] = 'C:\\path\\to\\python\\tcl\\tk8.6'

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

executables = [cx_Freeze.Executable('RiskMain.py', base = base)]

cx_Freeze.setup(
    name='Risk Simulation',
    version = '2.0',
    author= 'Alex Nash',
    description = 'Risk simulation built in Python',
    options={'build_exe': {'packages':['pygame'],
                           'include_files':['Map.gif', 'RedR.png',
                                            'freesansbold.ttf', 'README.txt']}},
    executables = executables
    )

