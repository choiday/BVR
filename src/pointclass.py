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

def SaveVessel():
    pass