import SimpleITK as sitk
import numpy as np
from tkinter.filedialog import askopenfilenames
import cv2

def global_line_from_image_point(point, Data):
    [u,v]=[point[0]-256, 256-point[1]]
    coef1=np.array([[u*Data.PS[0], v*Data.PS[1], Data.SID]])
    coef2=np.array([[0, 0, -Data.SOD]])
    # print(coef2)
    gradient3d=np.matmul(np.linalg.inv(Data.rot[0:3][:]),coef1.T)
    point3d=np.matmul(np.linalg.inv(Data.rot[0:3][:]),(coef2.T-Data.tls[0:3]))
    # print((coef2.T-Data.tls[0:3]))
    
    return gradient3d, point3d

def line_projection(gradient3d, point3d, Data):
    point1=np.matmul(Data.P, np.vstack([Data.SOD/Data.SID*gradient3d+point3d, 1]))
    point2=np.matmul(Data.P, np.vstack([1/2*gradient3d+point3d, 1]))
    point1/=point1[2]
    point2/=point2[2]
    point1=point1.T[0][0:2]
    point2=point2.T[0][0:2]
    point1[1]=512-point1[1]
    point2[1]=512-point2[1]
    if np.array_equal(point1,point2):
        point1_img=point1
        point2_img=point2
    elif point1[0] is point2[0]:
        point1_img=np.array([point1[0], 0])
        point1_img=np.array([point1[0], 511])
    else:
        point1_img=np.array([0, point1[1]-(point2[1]-point1[1])/(point2[0]-point1[0])*point1[0]])
        point2_img=np.array([511, point1[1]+(point2[1]-point1[1])/(point2[0]-point1[0])*(511-point1[0])])
    # return point1[0:2], point2[0:2]
    return point1_img, point2_img    

def projected_epipolar_line(point, Data_from, Data_to):
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
    coef_img=np.array([coef_img[0]*Data_to.PS[0],-coef_img[1]*Data_to.PS[1],coef_img[2]-256*(coef_img[0]*Data_to.PS[0]-coef_img[1]*Data_to.PS[1])])
    
    return coef_img
    
def pt3d_from_pt2d(point,Data):
    return np.matmul(np.linalg.inv(Data.rot[0:3][:]),np.array([[(point[0]-256)*Data.PS[0], (256-point[1])*Data.PS[1], Data.SID-Data.SOD]]).T-Data.tls[0:3])
