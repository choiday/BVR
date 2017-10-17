import SimpleITK as sitk
import numpy as np

def getBestImage(images):
    return images[40]


class DicomData():
    __count=0
    Dicom_array=[]
    reader=sitk.ImageFileReader()
    def __init__(self, filename):
        DicomData.reader.SetFileName(filename)
        dicomImage=DicomData.reader.Execute()
        if dicomImage.HasMetaDataKey('0008|0070') is not True:
            print('not DICOM image, '+type(dicomImage))
        elif dicomImage.GetMetaData('0008|0070')!='Siemens ':
            print('not Siemens, but '+dicomImage.GetMetaData('0008|0070'))
        else:
            DicomData.Dicom_array.append(self)
            self.order=DicomData.__count
            DicomData.__count+=1
            self.SID=float(dicomImage.GetMetaData('0018|1110'))
            self.SOD=float(dicomImage.GetMetaData('0018|1111'))
            # self.mag=float(dicomImage.GetMetaData('0018|1114'))
            self.PA=float(dicomImage.GetMetaData('0018|1510'))
            self.PA = np.deg2rad(self.PA)
            self.SA=float(dicomImage.GetMetaData('0018|1511'))
            self.SA = np.deg2rad(self.SA)
            self.PS=np.array(dicomImage.GetMetaData('0018|1164').split('\\')).astype(float)
            self.images = sitk.GetArrayFromImage(dicomImage)
            self.img = getBestImage(self.images)
            
    
    def info(self):
        print('Dicom file '+str(self.order)+' : angles ('+str(self.PA)+', '+str(self.SA)+' has '+len(self.images)+' images')

    def compute_initial_transform_matrix(self):
        self.skew=0
        self.tls=np.array([[0.0],[0.0],[0.0],[1.0]])

        self.roty=np.array([[np.cos(self.PA),0.0,-np.sin(self.PA)],[0.0,1.0,0.0],[np.sin(self.PA),0.0,np.cos(self.PA)]])
        self.rotx=np.array([[1.0,0.0,0.0],[0.0,np.cos(self.SA),-np.sin(self.SA)],[0.0,np.sin(self.SA),np.cos(self.SA)]])

        self.rot=np.matmul(self.rotx,self.roty)
        self.rot=np.vstack((self.rot,[0.0,0.0,0.0]))

        self.K=np.array([[self.SID/(self.PS[0]),self.SID/(self.PS[1])*self.skew,256,self.SOD*256],[0,self.SID/(self.PS[1]),256,self.SOD*256],[0,0,1,self.SOD]])

        self.P=np.matmul(self.K,np.concatenate((self.rot,self.tls),axis=1))
        