# main.py
# Membuat transformasi 2D

import DuaDimensi
import TigaDimensi
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import _thread
import numpy as np

width = 1000
height = 1000

print("Welcome to 2D and 3D Linear Transformation Simulation")
print("-----------------------------------------------------")
print("1. 2D Graphic")
print("2. 3D Graphic")
op = int(input())

if op == 1:
	glutInit([])
	glutInitWindowSize(width, height)
	glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
	DuaDimensi.Init()
	_thread.start_new_thread(DuaDimensi.command,())
	glutCreateWindow("2D and 3D Linear Transformation Simulation")
	glutDisplayFunc(DuaDimensi.display)
	glutIdleFunc(DuaDimensi.display)
	glutMainLoop()

elif op == 2:
	glutInit([])
	glutInitWindowSize(width, height)
	glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
	glutCreateWindow("2D and 3D Linear Transformation Simulation")
	TigaDimensi.Init()
	_thread.start_new_thread(TigaDimensi.command,())
	glutDisplayFunc(TigaDimensi.display)
	glutIdleFunc(TigaDimensi.display)

	glutMainLoop()
	
