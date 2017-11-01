import SimpleITK as sitk
import numpy as np
import os

# def get_best_image(images):
#     return images[26]    
reader=sitk.ImageFileReader()

def parsing_dicom(filepath):
    if filepath is 'temp1':
        filepath = os.getenv('HOME')+'/workspace/BVR/resource/Data/P2PGS/DCM/I0000003'
    elif filepath is 'temp2':
        filepath = os.getenv('HOME')+'/workspace/BVR/resource/Data/P2PGS/DCM/I0000004'
    reader.SetFileName(filepath)
    data=reader.Execute()
    metadata={}
    images=[]

    metadata['SID'] = float(data.GetMetaData('0018|1110'))
    metadata['SOD'] = float(data.GetMetaData('0018|1111'))
    metadata['PA'] = np.deg2rad(float(data.GetMetaData('0018|1510')))
    metadata['SA'] = np.deg2rad(float(data.GetMetaData('0018|1511')))
    metadata['PS'] = np.array(data.GetMetaData('0018|1164').split('\\')).astype(float)
    # metadata['tls'] = np.array([[0.0],[0.0],[0.0],[1.0]])
    metadata['skew'] = 0.0
    if data.GetMetaData('0020|0013')=='2 ':
        metadata['plane'] = 'B'
        print(filepath+' : Plane B')
    else:
        metadata['plane'] = 'A'          
        print(filepath+' : Plane A')

    images = sitk.GetArrayFromImage(data)

    return metadata, images
        

class DicomData():
    __count=0
    dicomArray=[]
    reader=sitk.ImageFileReader()
    def __init__(self, filepath):
        self.path=filepath
        DicomData.reader.SetFileName(self.path)
        self.dicomImage=DicomData.reader.Execute()
        if self.dicomImage.HasMetaDataKey('0008|0070') is not True:
            print('not DICOM image, '+type(self.dicomImage))
        elif self.dicomImage.GetMetaData('0008|0070')!='Siemens ':
            print('not Siemens, but '+self.dicomImage.GetMetaData('0008|0070'))
        else:
            DicomData.dicomArray.append(self)
            self.order=DicomData.__count
            DicomData.__count+=1
            self.SID=float(self.dicomImage.GetMetaData('0018|1110'))
            self.SOD=float(self.dicomImage.GetMetaData('0018|1111'))
            # self.mag=float(dicomImage.GetMetaData('0018|1114'))
            self.PA=float(self.dicomImage.GetMetaData('0018|1510'))
            self.PA = np.deg2rad(self.PA)
            self.SA=float(self.dicomImage.GetMetaData('0018|1511'))
            self.SA = np.deg2rad(self.SA)
            self.PS=np.array(self.dicomImage.GetMetaData('0018|1164').split('\\')).astype(float)
            self.images = sitk.GetArrayFromImage(self.dicomImage)
            # self.img = get_best_image(self.images) 
            self.tls=np.array([[0.0],[0.0],[0.0],[1.0]])
            self.skew=0.0
            if self.dicomImage.GetMetaData('0020|0013')=='2 ':
                self.plane='B'
                print(self.path+' : Plane B')
            else:
                self.plane='A'          
                print(self.path+' : Plane A')
            self.compute_transform_matrix()      
            
    
    def info(self):
        print('Dicom file', self.order, ': angles', [self.PA, self.SA], 'has', len(self.images), 'images')

    def compute_transform_matrix(self):
        # self.roty=np.array([[np.cos(self.PA),0.0,-np.sin(self.PA)],[0.0,1.0,0.0],[np.sin(self.PA),0.0,np.cos(self.PA)]])
        # self.rotx=np.array([[1.0,0.0,0.0],[0.0,np.cos(self.SA),-np.sin(self.SA)],[0.0,np.sin(self.SA),np.cos(self.SA)]])
        self.roty=np.array([[np.cos(self.PA),0.0,-np.sin(self.PA)],[0.0,1.0,0.0],[np.sin(self.PA),0.0,np.cos(self.PA)]])
        if self.plane is 'B':
            self.rotz=np.array([[np.cos(self.SA),np.sin(self.SA),0.0],[-np.sin(self.SA),np.cos(self.SA),0.0],[0.0,0.0,1.0]])
            self.rot=np.matmul(self.rotz,self.roty)
        else:
            self.rotx=np.array([[1.0,0.0,0.0],[0.0,np.cos(self.SA),-np.sin(self.SA)],[0.0,np.sin(self.SA),np.cos(self.SA)]])
            self.rot=np.matmul(self.rotx,self.roty)
                
        self.rot=np.vstack((self.rot,[0.0,0.0,0.0]))
        self.K=np.array([[self.SID/(self.PS[0]),self.SID/(self.PS[1])*self.skew,256,self.SOD*256],[0,-self.SID/(self.PS[1]),256,self.SOD*256],[0,0,1,self.SOD]])
        self.P=np.matmul(self.K,np.concatenate((self.rot,self.tls),axis=1))
    
    def call_test_data():
        print('Test dataset returned')
        folder=os.getenv('HOME')+'/workspace/BVR/resource/Data/P2PGS/DCM/'
        filepath=[folder+'I0000003', folder+'I0000004']
        data1=DicomData(filepath[0])
        data2=DicomData(filepath[1])
        return data1, data2