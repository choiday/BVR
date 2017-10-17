import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import askopenfilenames

class PeeredCanvas(tk.Canvas):
    '''A class that duplicates all objects on one or more peer canvases'''
    def __init__(self, *args, **kwargs):
        self.peers = []
        tk.Canvas.__init__(self, *args, **kwargs)

    def add_peer(self, peer):
        if self.peers is None:
            self.peers = []
        self.peers.append(peer)

    def move(self, *args, **kwargs):
        tk.Canvas.move(self, *args, **kwargs)
        for peer in self.peers:
            peer.move(*args, **kwargs)

    def itemconfigure(self, *args, **kwargs):
        tk.Canvas.itemconfigure(self, *args, **kwargs)
        for peer in self.peers:
            peer.itemconfigure(*args, **kwargs)

    def delete(self, *args, **kwargs):
        tk.Canvas.delete(self, *args)
        for peer in self.peers:
            peer.delete(*args)

    def create_oval(self, *args, **kwargs):
        tk.Canvas.create_oval(self, *args, **kwargs)
        for peer in self.peers:
            peer.create_oval(*args, **kwargs)

            
Files=askopenfilenames()
while len(Files) is not 2:
	messagebox.showerror(title='error',message='Two images are necessary')
	Files=askopenfilenames()
img0=tk.PhotoImage(file=Files[0])
img1=tk.PhotoImage(file=Files[1])

root=tk.Toplevel()
#oot.withdraw()
root.title('Finding points')
points1=[]
points2=[]
spline=1

c1=tk.Canvas(root,width=1024, height=1024)
c2=tk.Canvas(root,width=1024,height=1024)
c1.configure(cursor="crosshair")
c1.create_image(0,0,image=img0,anchor="nw")
c1.pack()
c2.pack()
#c1.pack(side='top',anchor'ne',expand=True,fill='x')

root.mainloop()