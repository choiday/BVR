#%%
import SimpleITK as sitk
import numpy as np
from tkinter.filedialog import askopenfilenames
import cv2


filepath1='/home/rtv/workspace/BVR/resource/Data/P2PGS/DCM/I0000004'
filepath2='/home/rtv/workspace/BVR/resource/Data/P2PGS/DCM/I0000005'

imgno=48

# reader=sitk.ImageFileReader()

# reader.SetFileName(filepath1)
# Data1=reader.Execute()

# reader.SetFileN ame(filepath2)
# Data2=reader.Execute()

# if Data1.HasMetaDataKey('0018|1164') is not True:
#     Data2.SetMetaData('0018|1164',Data1.GetMetaData('0018|1164'))
# if Data2.HasMetaDataKey('0018|1164') is not True:
#     Data1.SetMetaData('0018|1164',Data2.GetMetaData('0018|1164'))
    

#%%
DEGTORAD = np.pi / 180.0

def Initial_transform_Matrix(Self, Data):
    if type(Data) is sitk.SimpleITK.Image:
        DicomData=Data
    elif type(Data) is str:
        reader=sitk.ImageFileReader()
        reader.SetFileName(Data)
        DicomData=reader.Execute()

    if DicomData.HasMetaDataKey('0008|0070') is not True:
        print('not DICOM image, '+type(DicomData))
    elif DicomData.GetMetaData('0008|0070')!='Siemens ':
        print('not Siemens, but '+Data1.GetMetaData('0008|0070'))
    else:
        # print('return Transform Matrix')
        SID=float(DicomData.GetMetaData('0018|1110'))
        SOD=float(DicomData.GetMetaData('0018|1111'))
        # mag=float(DicomData.GetMetaData('0018|1114'))
        angle1=float(DicomData.GetMetaData('0018|1510'))*DEGTORAD
        angle2=float(DicomData.GetMetaData('0018|1511'))*DEGTORAD
        skew=0

        ''' if DicomData.HasMetaDataKey('0018|1164') is not True:
            pixel_spacing=([0.278875,  0.278875])
            
        else:
            pixel_spacing=np.array(DicomData.GetMetaData('0018|1164').split('\\')).astype(float) '''
        pixel_spacing=np.array(DicomData.GetMetaData('0018|1164').split('\\')).astype(float)
        roty=np.array([[np.cos(angle1),0.0,np.sin(angle1)],[0.0,1,0.0],[-np.sin(angle1),0.0,-np.cos(angle1)]])
        rotx=np.array([[1.0,0.0,0.0],[0.0,np.cos(angle2),-np.sin(angle2)],[0.0,np.sin(angle2),np.cos(angle2)]])

        rot=np.matmul(rotx,roty)

        rot=np.vstack((rot,[0.0,0.0,0.0]))
        # print(rot)

        # K=np.array([[mag/(pixel_spacing[0]),mag/(pixel_spacing[1])*skew,0],[0,mag/(pixel_spacing[1]),0],[0,0,1]])
        K=np.array([[SID/(pixel_spacing[0]),SID/(pixel_spacing[1])*skew,256,SOD*256],[0,SID/(pixel_spacing[1]),256,SOD*256],[0,0,1,SOD]])
        # tls=np.zeros([3,1])
        tls=np.array([[0.0],[0.0],[0.0],[1.0]])
        print('angle is '+str(angle1/DEGTORAD)+','+str(angle2/DEGTORAD))

        P=np.matmul(K,np.concatenate((rot,tls),axis=1))
        return P, K, rot, tls

#%%
# [P1 , K1, rot1, tls1] =Initial_transform_Matrix(Data1)
[P1 , K1, rot1, tls1] =Initial_transform_Matrix(filepath1)
print(P1,rot1)

# [P2 , K2, rot2, tls2] =Initial_transform_Matrix(Data2)
[P2 , K2, rot2, tls2] =Initial_transform_Matrix(filepath2)
print(P2)


#%%
def line_par_frompoinrt(self, parameter_list):
    pass


#%%


#%%
print(np.matmul(P1,[100,0,0,1])/np.matmul(P1[2][:],[100,0,0,1]))
print(np.matmul(P1,[0,100,0,1])/np.matmul(P1[2][:],[0,100,0,1]))
print(np.matmul(P1,[0,0,100,1])/np.matmul(P1[2][:],[0,0,100,1]))
print(np.matmul(P2,[100,0,0,1])/np.matmul(P2[2][:],[100,0,0,1]))
print(np.matmul(P2,[0,100,0,1])/np.matmul(P2[2][:],[0,100,0,1]))
print(np.matmul(P2,[0,0,100,1])/np.matmul(P2[2][:],[0,0,100,1]))