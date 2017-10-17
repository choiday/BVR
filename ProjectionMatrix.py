import SimpleITK as sitk
import numpy as np
from tkinter.filedialog import askopenfilenames
import cv2

def global_line_from_image_point(point,Data):
    [u,v]=point
    coef1=np.array([[u/Data.K[0][0], v/Data.K[1][1], 1.0]])
    coef2=Data.K[2][3]*np.array([[u/Data.K[0][0], v/Data.K[1][1], 0.0]])
    # print(coef2)
    coef1_global=np.matmul(np.linalg.inv(Data.rot[0:3][:]),coef1.T)
    coef2_global=np.matmul(np.linalg.inv(Data.rot[0:3][:]),(coef2.T-Data.tls[0:3]))
    # print((coef2.T-Data.tls[0:3]))
    
    return coef1_global, coef2_global
    

def projected_epipolar_line(point,Data_from,Data_to):
    [coef1_global, coef2_global]=global_line_from_image_point(point,Data_from)
    coef1=np.matmul(Data_to.rot[0:3][:],coef1_global)
    coef2=np.matmul(Data_to.rot[0:3][:],coef2_global)+Data_to.tls[0:3]
    coef1=np.vstack([coef1,1])
    coef2=np.vstack([coef2,1])
    # print(coef1_global)
    pixel1=np.matmul(Data_to.P,coef2)
    pixel1/=pixel1[2]
    pixel2=np.matmul(Data_to.P,coef1+coef2)
    pixel2/=pixel2[2]
    coef_img=np.array([pixel2[1]-pixel1[1], pixel1[0]-pixel2[0], pixel2[0]*pixel1[1]-pixel1[0]*pixel2[1]])
    
    return coef_img
    
def pt3d_from_pt2d(point,Data):
    return np.matmul(Data.rot[0:3][:],Data.tls[0:3]+np.array([[point[0]*Data.PS[0], point[1]*Data.PS[1], Data.SID-Data.SOD]]).T)
