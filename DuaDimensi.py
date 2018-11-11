# 2D.py
# Berisikan primitif untuk penggambaran 2D
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
import time
import _thread
import math


width = 1000
height = 1000
FRAME = 60
DELAY = 0.01

def Init():
	global BidangAwal
	global Bidang
	global N

	BidangAwal = []
	N = int(input("How many sides? : "))
	if (N > 2):
		i = 0
		while i < N:
			try :
				point = input("(X,Y) = ").split(",")
				BidangAwal = np.append(BidangAwal,[float(point[0]), float(point[1])])
				i = i + 1
			except :
				print("Error : Wrong input format! Use (X,Y) format without brackets")
		
		BidangAwal.resize(N,2)
		Bidang = np.array(BidangAwal)
	else:
		print("N should greater than 2")
		Init()

def command():
	global Bidang
	cmd = input().split(" ")
	try :
		command_action(Bidang, cmd)
	except ValueError: 
		print("Error : Wrong command! Use the right command")

	command()

def transformation(Bidang, func, *args):
	if (func == rotate):
		degreeFRAME = args[0]/FRAME
		for i in range(FRAME):
			Bidang = func(Bidang, degreeFRAME,args[1],args[2])
			time.sleep(DELAY)
	else:
		BidangAntara = np.copy(Bidang)
		BidangAkhir = np.array(func(BidangAntara,*args))
		delta = BidangAkhir - Bidang
		delta /= FRAME

		while (not np.allclose(BidangAkhir,Bidang)):
			Bidang += delta
			time.sleep(DELAY)

def translate(Bidang, dx,dy):
	for point in Bidang:
		point += [dx,dy]

	return Bidang

def dilate(Bidang,k):
	Bidang*=k
	return Bidang

def reflectline(Bidang, line):
	tempx = []
	tempy = []
	tempx = np.append(tempx,Bidang[:,0])
	tempy = np.append(tempy,Bidang[:,1])
	if (line=='y=x'):
		Bidang[:,0] = tempy
		Bidang[:,1] = tempx
	elif (line=='y=-x'):
		Bidang[:,0] = -1*tempy
		Bidang[:,1] = -1*tempx
	elif (line=='x'):
		Bidang[:,1] *= -1
	elif (line=='y'):
		Bidang[:,0] *= -1
	return Bidang

def rotate(Bidang, angle, pointA, pointB):
	tempx = []
	tempy = []
	tempx = np.append(tempx,Bidang[:,0])
	tempy = np.append(tempy,Bidang[:,1])
	angle = math.radians(angle)
	Bidang[:,0] = ((tempx-pointA)*math.cos(angle))-((tempy-pointB)*math.sin(angle))
	Bidang[:,1] = ((tempx-pointA)*math.sin(angle))+((tempy-pointB)*math.cos(angle))
	return Bidang

def shear(Bidang, param, k):
	if (param == 'x'):
		Bidang[:,0] += k*Bidang[:,1];
	elif (param == 'y'):
		Bidang[:,1] += k*Bidang[:,0];
	return Bidang

def stretch(Bidang, param, k):
	if (param == 'x'):
		Bidang[:,0] *= k
	elif (param == 'y'):
		Bidang[:,1] *= k
	return Bidang

def custom_transform(Bidang,command):
	matrix = []
	for i in range(1,len(command)):
		p  = float(command[i])
		matrix = np.append(matrix,p)
	matrix.resize(2,2)

	Bidang = np.dot(Bidang,matrix)
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

	for command in command_list:
		try:
			command_action(Bidang, command)
		except ValueError:
			print ("Error : Wrong command! Use the right command\n")

def reset(Bidang):
	Bidang = np.copy(BidangAwal)
	return Bidang

def reflectpoint(Bidang, dx, dy):
	Bidang[:,0] = 2*dx - Bidang[:,0]
	Bidang[:,1] = 2*dy - Bidang[:,1]
	return Bidang

def command_action(Bidang, cmd):
	try:
		if (cmd[0]=='translate'):
			dx = float(cmd[1])
			dy = float(cmd[2])
			transformation(Bidang,translate,dx,dy)

		elif (cmd[0] =='dilate'):
			k = float(cmd[1])
			transformation(Bidang,dilate,k)

		elif (cmd[0] == 'reflect'):
			if (cmd[1] == 'y=x' or cmd[1] == 'y=-x' or cmd[1] == 'x' or cmd[1] == 'y'):
				line = cmd[1]
				transformation(Bidang,reflectline, line)
			else:
				point = cmd[1].split(",")
				dx = float(point[0].replace('(', ''))
				dy = float(point[1].replace(')', ''))
				transformation(Bidang,reflectpoint,dx,dy)

		elif (cmd[0] == 'rotate'):
			angle = float(cmd[1])
			a = float(cmd[2])
			b = float(cmd[3])
			transformation(Bidang,rotate,angle,a,b)

		elif (cmd[0] == 'shear'):
			param = cmd[1]
			k = float(cmd[2])
			transformation(Bidang,shear,param,k)

		elif (cmd[0] == 'stretch'):
			param = cmd[1]
			k = float(cmd[2])
			transformation(Bidang,stretch,param,k)

		elif (cmd[0] =='custom' and not len(cmd[1])==0):
			transformation(Bidang,custom_transform,cmd)

		elif (cmd[0] =='reset'):
			transformation(Bidang,reset)

		elif (cmd[0] =='multiple'):
			n = int(cmd[1])
			multiple_cmds(Bidang,n)

		elif (cmd[0] =='exit'):
			glutLeaveMainLoop()
		
		else :
			print("There isn't that command")

	except IndexError : 
		print ("Error : Wrong command! Use the right command")


def setup_world(width, height):
	glLoadIdentity()
	glViewport(0, 0, width, height)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	glOrtho(-1*(width/2), width/2, -1*(height/2), height/2, 0.0, 1.0)
	glMatrixMode (GL_MODELVIEW)
	glLoadIdentity()

def draw_layout():
	#Draw Grid
	glColor3f(0.9,0.9,0.9)
	glLineWidth(0.1)
	glBegin(GL_LINES)
	for i in range(-height,height,50):
		glVertex2f(width,i)
		glVertex2f(-width,i)
	for i in range(-width,width,50):
		glVertex2f(i,-height)
		glVertex2f(i,height)
	glEnd()

	#Draw Axis
	glColor3f(0,0,0)
	glBegin(GL_LINES)                                
	glVertex2f(0, height)                                  
	glVertex2f(0, -1*height)                          
	glVertex2f(width, 0)                  
	glVertex2f(-1 * width, 0)                          
	glEnd()

def draw_bidang(Bidang):
	glBegin(GL_POLYGON)
	for point in Bidang:
		glVertex2f(point[0],point[1])
	glEnd()

def display():
	glClearColor(1,1,1,1)
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	setup_world(width, height)
	draw_layout()

	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
	glEnable(GL_BLEND)
	glColor4f(1.0,0.0,0.0,0.9)
	draw_bidang(Bidang)

	glutSwapBuffers()




