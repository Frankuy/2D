# main.py
# Membuat transformasi 2D

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
import time
import _thread
import math
import DuaDimensi

width = 1000
height = 1000
FRAME = 60
DELAY = 0.01

print("Welcome to 2D and 3D Linear Transformation Simulation")
print("-----------------------------------------------------")
print("1. 2D Graphic")
print("2. 3D Graphic")
op = int(input())

if op == 1:
	DuaDimensi.Init()
	glutInit([])
	glutInitWindowSize(width, height)
	glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
	_thread.start_new_thread(DuaDimensi.command,())
	glutCreateWindow("DuaDimensi and 3D Linear Transformation Simulation")
	glutDisplayFunc(DuaDimensi.display)
	glutIdleFunc(DuaDimensi.display)
	glutMainLoop()

elif op == 2:
	None
