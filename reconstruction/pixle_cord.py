#%%
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import askopenfilenames
#from PIL import Image
'''
def getCord(image):
	root=Tk()
	coor=[]
	#background_label=Label(root,image=image)
	#background_label.place(0,0,width=512,height=512)
	
	def callback(event):
		coor.append([event.x,event.y])
		print("clicked at",event.x,event.y)
	
	
	frame=Frame(root,width=512,height=512)
	frame.bind("<Button-1>",callback)
	frame.pack()
	
	root.mainloop()
	return coor
'''	
	

Files=askopenfilenames()
while len(Files) is not 2:
	messagebox.showerror(title='error',message='Two images are necessary')
	Files=askopenfilenames()
img0=tk.PhotoImage(file=Files[0])
img1=tk.PhotoImage(file=Files[1])
#%%
img=img0.zoom(x=2,y=2)
#pts=getCord(File)
root=tk.Toplevel()
points = []
spline = 1
tag1 = "theline"
	

def point(event):
	c.create_oval(event.x-1, event.y-1, event.x+1, event.y+1, fill="black")
	points.append(event.x)
	points.append(event.y)
	return points

def canxy(event):
	print (event.x, event.y)
	
	
def graph(event):
	global theline
	c.create_line(points,fill="red",width=2, tags="theline")
	
def toggle(event):
	global spline
	if spline == 0:
		c.itemconfigure(tag1, smooth=1)
		spline = 1
	elif spline == 1:
		c.itemconfigure(tag1, smooth=0)
		spline = 0
	return spline
	

c=tk.Canvas(root,width=2*img.width(),height=2*img.height())
c.configure(cursor="crosshair")
c.create_image(0,0,image=img,anchor="nw")
c.pack()

#canv.create_line(0,0,512,512,fill='red',width=3)
#canv.create_line(0,512,512,0,fill='red',width=3)
#for i in range(len(coor)-1):
#	canv.create_line(coor[i][0],coor[i][1],coor[i+1][0],coor[i+1][1],fill='red',width=3)

#canv.create_polygon(np.reshape(coor,(np.size(coor))))
#canv.create_polygon(np.reshape(coor,(np.size(coor))),fill="red",width=2)
c.bind("<Button-1>",point)

c.bind("<Button-3>", graph)

c.bind("<Button-2>", toggle)

	
root.mainloop()
coor=[(int(x/2), int(y/2))for (x,y) in coor]
	
