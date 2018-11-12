from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
import time
import _thread
from math import *

width = 1000
height = 1000
FRAME = 60
DELAY = 0.005

def Init():
	global Bidang
	global BidangAwal

	BidangAwal = np.array([[1.0, 1.0, 1.0], [1.0, 1.0, -1.0], [1.0, -1.0, 1.0], [1.0, -1.0, -1.0], [-1.0, 1.0, 1.0], [-1.0, 1.0, -1.0], [-1.0, -1.0, 1.0], [-1.0, -1.0, -1.0]])
	Bidang = np.copy(BidangAwal)
	glClearColor(1,1,1,1) # warna background
	glClearDepth(1)
	glEnable(GL_DEPTH_TEST)
	glDepthFunc(GL_LEQUAL)
	glShadeModel(GL_SMOOTH)
	glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)

def command():
	global Bidang

	cmd = input().split(" ")
	# try :
	command_action(Bidang, cmd)
	# except ValueError: 
		# print("Error : Wrong command! Use the right command")

	command()

def command_action(Bidang, cmd):
	try:
		if (cmd[0]=='translate'):#udah
			dx = float(cmd[1])/500
			dy = float(cmd[2])/500
			dz = float(cmd[3])/500
			transformation(Bidang,translate,dx,dy,dz)

		elif (cmd[0] =='dilate'):#udah
			k = float(cmd[1])
			transformation(Bidang,dilate,k)

		elif (cmd[0] == 'reflect'):
			if (cmd[1] == 'xy' or cmd[1] == 'yz' or cmd[1] == 'zx'):
				line = cmd[1]
				transformation(Bidang,reflect,line)
			else :
				print("Error : Wrong command! Use the right command")

		elif (cmd[0] == 'rotate'):#udah
			angle = float(cmd[1])
			line = cmd[2]
			transformation(Bidang,rotate,angle,line)

		elif (cmd[0] == 'shear'):#udah
			param = cmd[1]
			k1 = float(cmd[2])/500
			k2 = float(cmd[2])/500
			transformation(Bidang,shear,param,k1,k2)

		elif (cmd[0] == 'stretch'):
			param = cmd[1]
			k = float(cmd[2])
			transformation(Bidang,stretch,param,k)

		elif (cmd[0] =='custom' and not len(cmd[1])==0): #udah
			transformation(Bidang,custom_transform,cmd)

		elif (cmd[0] =='reset'): #udah
			transformation(Bidang,reset)

		elif (cmd[0] =='multiple'): #udah
			n = int(cmd[1])
			multiple_commands(Bidang,n)

		elif (cmd[0] =='exit'):
			glutLeaveMainLoop()
		
		else :
			print("There isn't that command")

	except IndexError : 
		print ("Error : Wrong command! Use the right command")

def transformation(Bidang, func, *args):
	if (func == rotate):
		degreeFRAME = args[0]/FRAME
		for i in range(FRAME):
			Bidang = func(Bidang, degreeFRAME,args[1])
			time.sleep(DELAY)
	else:
		BidangAntara = np.copy(Bidang)
		BidangAkhir = np.array(func(BidangAntara,*args))
		delta = BidangAkhir - Bidang
		delta /= FRAME

		while (not np.allclose(BidangAkhir,Bidang)):
			Bidang += delta
			time.sleep(DELAY)

def translate(Bidang, dx,dy, dz): #udah
	MT = np.array([[1.0,0.0,0.0],[0.0,1.0,0.0],[0.0,0.0,1.0]])
	i = 0
	for point in Bidang:
		v = np.resize(point,(3,1))
		Bidang[i] = np.transpose(np.dot(MT, v) + [[dx],[dy],[dz]])
		i = i + 1

	return Bidang

def dilate(Bidang,k): #udah
	MT = np.array([[k,0.0,0.0],[0.0,k,0.0],[0.0,0.0,k]])
	i = 0
	for point in Bidang:
		v = np.resize(point,(3,1))
		Bidang[i] = np.transpose(np.dot(MT,v))
		i = i + 1
	
	return Bidang

def rotate(Bidang, angle, line): #udah
	angle = radians(angle)
	if line == 'x':
		MT = np.array([[1.0,0.0,0.0],[0.0, cos(angle), -sin(angle)],[0.0, sin(angle), cos(angle)]])
	elif line == 'y' :
		MT = np.array([[cos(angle), 0.0, sin(angle)],[0.0,1.0,0.0],[-sin(angle),0.0,cos(angle)]])
	elif line == 'z':
		MT = np.array([[cos(angle),-sin(angle),0.0],[sin(angle), cos(angle), 0.0],[0.0,0.0,0.1]])

	i = 0
	for point in Bidang:
		v = np.resize(point,(3,1))
		Bidang[i] = np.transpose(np.dot(MT, v))
		i = i + 1

	return Bidang

def shear(Bidang, param, k1, k2): #udah
	if (param == 'x'):
		MT = np.array([[1.0,0.0,0.0],[k1,1.0,0.0],[k2,0.0,1.0]])
	elif (param == 'y'):
		MT = np.array([[1.0,k1,0.0],[0.0,1.0,0.0],[0.0,k2,1.0]])
	elif (param == 'z'):
		MT = np.array([[1.0,0.0,k1],[0.0,1.0,k2],[0.0,0.0,1.0]])

	i = 0
	for point in Bidang:
		v = np.resize(point,(3,1))
		Bidang[i] = np.transpose(np.dot(MT,v))
		i = i + 1

	return Bidang

def stretch(Bidang, param, k): #beloman
	if (param == 'x'):
		MT = np.array([[k, 0.0, 0.0],[0.0,1.0,0.0],[0.0,0.0,1.0]])
	elif (param == 'y'):
		MT = np.array([[1.0, 0.0, 0.0],[0.0,k,0.0],[0.0,0.0,1.0]])
	elif (param == 'z'):
		MT = np.array([[1.0, 0.0, 0.0],[0.0,1.0,0.0],[0.0,0.0,k]])

	i = 0
	for point in Bidang:
		v = np.resize(point,(3,1))
		Bidang[i] = np.transpose(np.dot(MT,v))
		i = i + 1

	return Bidang

def custom_transform(Bidang,command):
	matrix = []
	for i in range(1,len(command)):
		p  = float(command[i])
		matrix = np.append(matrix,p)
	matrix.resize(3,3)

	i = 0
	for point in Bidang:
		v = np.resize(point,(3,1))
		Bidang[i] = np.transpose(np.dot(matrix, v))
		i = i + 1

	return Bidang

def multiple_commands(Bidang,n):
	command_list=[]
	i=0
	while (i<n):
		Bidang_command = input().split(" ")
		if (not (Bidang_command[0] == 'multiple' or Bidang_command[0] == 'reset' or Bidang_command[0] == 'exit')):
			command_list.append(Bidang_command)
			i+=1
		else :
			print ("Ulangi input")

	try : 
		for command in command_list:
			command_action(Bidang, command)
	except ValueError:
		print ("Error : Wrong command! Use the right command\n")

def reset(Bidang):
	Bidang = np.copy(BidangAwal)
	return Bidang

def reflect(Bidang, line): #udah
	if (line == 'xy'):
		MT = np.array([[1.0,0.0,0.0],[0.0,1.0,0.0],[0.0,0.0,-1.0]])
	elif (line == 'yz'):
		MT = np.array([[-1.0,0.0,0.0],[0.0,1.0,0.0],[0.0,0.0,1.0]])
	elif (line == 'zx'):
		MT = np.array([[1.0,0.0,0.0],[0.0,-1.0,0.0],[0.0,0.0,1.0]])

	i = 0
	for point in Bidang:
		v = np.resize(point,(3,1))
		Bidang[i] = np.transpose(np.dot(MT,v))
		i = i + 1

	return Bidang

def draw_layout():
	glEnable( GL_LINE_SMOOTH )
	glLineWidth( 0.5 )
	glBegin(GL_LINES)
	glColor3f(1.0, 0.0, 0.0)
	glVertex3f(-500.0, 0, 0)
	glVertex3f(500, 0, 0)

	glColor3f(0.0, 1.0, 0.0)
	glVertex3f(0, -500, 0)
	glVertex3f(0, 500, 0)

	glColor3f(0.0, 0.0, 1.0)
	glVertex3f(0, 0, 500)
	glVertex3f(0, 0, -500)
	glEnd()


def display():
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
	gluLookAt(5.0,5.0,10.0, 0.0,0.0,0.0, 0.0,1.0, 0.0)

	glBegin(GL_QUADS)             
	glColor3f(0.0, 0.5, 0.0)
	glVertex3f(Bidang[1][0], Bidang[1][1], Bidang[1][2])
	glVertex3f(Bidang[5][0], Bidang[5][1], Bidang[5][2])
	glVertex3f(Bidang[4][0], Bidang[4][1], Bidang[4][2])
	glVertex3f(Bidang[0][0], Bidang[0][1], Bidang[0][2])
 
	glColor3f(1.0, 0.5, 0.0)
	glVertex3f(Bidang[2][0], Bidang[2][1], Bidang[2][2])
	glVertex3f(Bidang[6][0], Bidang[6][1], Bidang[6][2])
	glVertex3f(Bidang[7][0], Bidang[7][1], Bidang[7][2])
	glVertex3f(Bidang[3][0], Bidang[3][1], Bidang[3][2])

	glColor3f(1.0, 0.0, 0.0)
	glVertex3f(Bidang[0][0], Bidang[0][1], Bidang[0][2])
	glVertex3f(Bidang[4][0], Bidang[4][1], Bidang[4][2])
	glVertex3f(Bidang[6][0], Bidang[6][1], Bidang[6][2])
	glVertex3f(Bidang[2][0], Bidang[2][1], Bidang[2][2])
 
	glColor3f(1.0, 1.0, 0.0)
	glVertex3f(Bidang[3][0], Bidang[3][1], Bidang[3][2])
	glVertex3f(Bidang[7][0], Bidang[7][1], Bidang[7][2])
	glVertex3f(Bidang[5][0], Bidang[5][1], Bidang[5][2])
	glVertex3f(Bidang[1][0], Bidang[1][1], Bidang[1][2])

	glColor3f(0.0, 0.0, 1.0)
	glVertex3f(Bidang[4][0], Bidang[4][1], Bidang[4][2])
	glVertex3f(Bidang[5][0], Bidang[5][1], Bidang[5][2])
	glVertex3f(Bidang[7][0], Bidang[7][1], Bidang[7][2])
	glVertex3f(Bidang[6][0], Bidang[6][1], Bidang[6][2])

	glColor3f(1.0, 0.0, 1.0)
	glVertex3f(Bidang[1][0], Bidang[1][1], Bidang[1][2])
	glVertex3f(Bidang[0][0], Bidang[0][1], Bidang[0][2])
	glVertex3f(Bidang[2][0], Bidang[2][1], Bidang[2][2])
	glVertex3f(Bidang[3][0], Bidang[3][1], Bidang[3][2])
	glEnd()

	glViewport(0, 0, width, height)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(45.0, 1.0, 0.1, 100.0)

	draw_layout() 

	glutSwapBuffers()