import SimpleITK as sitk
import numpy as np
from tkinter.filedialog import askopenfilenames
import cv2
from DICOMImage import readDICOMImage

def Initial_transform_Matrix(Data):
    DEGTORAD = np.pi / 180.0
    img, metadata = readDICOMImage(Data)
    skew=0
    
    SID = metadata['SID']
    SOD = metadata['SOD']
    angle1 = metadata['PA']
    angle2 = metadata['SA']
    pixel_spacing = metadata['PS']

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


def global_line_from_image_point(point,Data):
    [P, K, rot, tls]=Initial_transform_Matrix(Data)
    [u,v]=point
    coef1=np.array([[u/K[0][0], v/K[1][1], 1.0]])
    coef2=K[2][3]*np.array([[u/K[0][0], v/K[1][1], 0.0]])
#     print(coef2)
    coef1_global=np.matmul(np.linalg.inv(rot[0:3][:]),coef1.T)
    coef2_global=np.matmul(np.linalg.inv(rot[0:3][:]),(coef2.T-tls[0:3]))
#     print((coef2.T-tls[0:3]))
    
    return coef1_global, coef2_global
    

def projected_epipolar_line(point,Data_from,Data_to):
    [coef1_global, coef2_global]=global_line_from_image_point(point,Data_from)
    [P, K, rot, tls]=Initial_transform_Matrix(Data_to)
    coef1=np.matmul(rot[0:3][:],coef1_global)
    coef2=np.matmul(rot[0:3][:],coef2_global)+tls[0:3]
    coef1=np.vstack([coef1,1])
    coef2=np.vstack([coef2,1])
    print(coef1_global)
    pixel1=np.matmul(P,coef2)
    pixel1/=pixel1[2]
    pixel2=np.matmul(P,coef1+coef2)
    pixel2/=pixel2[2]
    coef_img=np.array([pixel2[1]-pixel1[1], pixel1[0]-pixel2[0], pixel2[0]*pixel1[1]-pixel1[0]*pixel2[1]])
    
    return coef_img
    

