#%%
import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import askopenfilenames

class point():
    __count=0
    __branch_count=0
    __curved_count=0
    def __init__(self,coord,type):
        point.__count+=1
        self.coord=coord
        self.type=type
        if type=='b':
            point.__branch_count+=1
        elif type=='c':
            point.__curved_count+=1

    def __repr__(self):
        return "node type : " +self.type+", position : "+str(self.coord)

    @classmethod
    def total(cls):
        return cls.__count
    @classmethod
    def branch(cls):
        return cls.__branch_count
    @classmethod
    def curved(cls):
        return cls.__curved_count


class vessel():
    __count=0
    vs_array=[]
    def __init__(self,parent):
        vessel.vs_array.append(self)
        self.order=vessel.__count
        vessel.__count+=1
        self.points=[]
        self.parent_vs=[]
        self.child_vs=[]
        if parent==None:
            self.parent_vs=None
        else:
            self.parent_vs.append(parent.order)
            parent.child_vs.append(self.order)
    
    
    #def __repr__(self):

    def info(self):
        print('vessel no :'+str(self.order)+ \
    ' \nParent vessel : ' + str(self.parent_vs) + \
    '\nChild vessel :' + str(self.child_vs))

    @classmethod
    def total(cls):
        return cls.__count

class manual_points(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        #self.canvas1=PeeredCanvas(self,width=512,height=512,border=1,relief="sunken")
        #self.canvas2=PeeredCanvas(self,width=512,height=512,border=1,relief="sunken")
        self.canvas1=tk.Canvas(self,width=512,height=512,border=1,relief="sunken")
        self.canvas2=tk.Canvas(self,width=512,height=512,border=1,relief="sunken")
        #self.canvas1.add_peer(self.canvas2)
        toolbar=tk.Frame(self)
        button1=tk.Button(self, text="Refresh",command=self.refresh)
        button1.pack(in_=toolbar,side="left")
        toolbar.pack(side="top",fill="x")
        self.canvas1.pack(side="left",fill="both",expand=True)
        self.canvas2.pack(side="left",fill="both",expand=True)
        self.points1 = []
        self.points2 = []

        def point(event,cv,pnts):
            pnts.append([event.x, event.y])
            if len(pnts)==1:
                cv.create_oval(pnts[0][0]-1,pnts[0][1]-1,pnts[0][0]+1,pnts[0][1],fill="black",tags="thepoint")
            elif len(pnts)>1:
                cv.create_line(pnts,fill="red",width=2,tags="theline")
                cv.create_oval(pnts[0][0]-1,pnts[0][1]-1,pnts[0][0]+1,pnts[0][1],fill="black",tags="thepoint")
            
        def point_remove(event,cv,pnts):
            if len(pnts) is not 0:
                pnts.remove(pnts[-1])
            cv.delete("theline","thepoint")
            if len(pnts)==1:
                cv.create_oval(pnts[0][0]-1,pnts[0][1]-1,pnts[0][0]+1,pnts[0][1],fill="black",tags="thepoint")
            elif len(pnts)>1:
                cv.create_line(pnts,fill="red",width=2,tags="theline")
                cv.create_oval(pnts[0][0]-1,pnts[0][1]-1,pnts[0][0]+1,pnts[0][1],fill="black",tags="thepoint")
            
        self.canvas1.bind("<Button-1>",lambda event, cv=self.canvas1, pnts=self.points1 :point(event,cv,pnts))
        self.canvas2.bind("<Button-1>",lambda event, cv=self.canvas2, pnts=self.points2 :point(event,cv,pnts))
        self.canvas1.bind("<Button-3>",lambda event, cv=self.canvas1, pnts=self.points1 :point_remove(event,cv,pnts))
        self.canvas2.bind("<Button-3>",lambda event, cv=self.canvas2, pnts=self.points2 :point_remove(event,cv,pnts))

    def refresh(self, count=100):
        '''Redraw 'count' random circles'''
        self.canvas1.delete("all")
        self.Files=askopenfilenames()
        while len(self.Files) is not 2:
            messagebox.showerror(title='error',message='Two images are necessary')
            self.Files=askopenfilenames()
        self.img0=tk.PhotoImage(file=self.Files[0])
        self.img1=tk.PhotoImage(file=self.Files[1])
        width=self.img0.width()
        height=self.img0.height()
        self.canvas1.create_image(0,0,image=self.img0,anchor="nw")
        self.canvas2.create_image(0,0,image=self.img1,anchor="nw")

        #print(self.event.x,',',self.event.y)
        #self.canvas1.create_oval(event.x-1, event.y-1, event.x+1, event.y+1, fill="black")
        
        #self.points.append(event.x)
        #self.points.append(event.y)
        #return self.points


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

#%%
def SaveVessel():
    pass
#%%
app = manual_points()
app.mainloop()