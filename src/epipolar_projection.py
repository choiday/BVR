import numpy as np

def global_line_from_image_point(point, data): 
    [u,v]=[(point[0]-256)*data.PS[0], (256-point[1])*data.PS[1]]
    coef1=np.array([[u, v, data.SID]])
    coef2=np.array([[0, 0, -data.SOD]])
    gradient3d=np.matmul(np.linalg.inv(data.rot[0:3][:]),coef1.T)
    point3d=np.matmul(np.linalg.inv(data.rot[0:3][:]),(coef2.T-data.tls[0:3]))
    
    return gradient3d, point3d

def line_projection(gradient3d, point3d, data):
    tempPoint1=np.matmul(data.P, np.vstack([data.SOD/data.SID*gradient3d+point3d, 1]))
    tempPoint2=np.matmul(data.P, np.vstack([1/2*gradient3d+point3d, 1]))
    tempPoint1/=tempPoint1[2]
    tempPoint2/=tempPoint2[2]
    tempPoint1=tempPoint1.T[0][0:2]
    tempPoint2=tempPoint2.T[0][0:2]
    if np.array_equal(tempPoint1,tempPoint2):
        pointOnImg1=tempPoint1
        pointOnImg2=point2
    elif tempPoint1[0] is tempPoint2[0]:
        pointOnImg1=np.array([tempPoint1[0], 0])
        pointOnImg1=np.array([tempPoint1[0], 511])
    else:
        pointOnImg1=np.array([0, tempPoint1[1]-(tempPoint2[1]-tempPoint1[1])/(tempPoint2[0]-tempPoint1[0])*tempPoint1[0]])
        pointOnImg2=np.array([511, tempPoint1[1]+(tempPoint2[1]-tempPoint1[1])/(tempPoint2[0]-tempPoint1[0])*(511-tempPoint1[0])])
        if pointOnImg1[1] > 511:
            pointOnImg1=np.array([(pointOnImg1[1]-511)/(pointOnImg1[1]-tempPoint2[1])*tempPoint2[0], 511])
        elif pointOnImg1[1] < 0:
            pointOnImg1=np.array([tempPoint2[0]*(-pointOnImg1[1])/(tempPoint2[1]-pointOnImg1[1]), 0])
        if pointOnImg2[1] > 511:
            pointOnImg2=np.array([511-(pointOnImg2[1]-511)/(pointOnImg2[1]-tempPoint1[1])*(511-tempPoint1[0]),511])
        elif pointOnImg2[1] < 0:
            pointOnImg2=np.array([511-(511-tempPoint1[0])*(-pointOnImg2[1])/(tempPoint1[1]-pointOnImg2[1]), 0])                
    return pointOnImg1, pointOnImg2    

def projected_epipolar_line(point, data1, data2):
    [coef1_global, coef2_global]=global_line_from_image_point(point,data1)
    coef1=np.matmul(data2.rot[0:3][:],coef1_global)
    coef2=np.matmul(data2.rot[0:3][:],coef2_global)+data2.tls[0:3]
    pixel1=np.matmul(data2.P,np.vstack([coef2,1]))
    pixel1/=pixel1[0:2]/pixel1[2]
    pixel2=np.matmul(data2.P,np.vstack([coef1+coef2,1]))
    pixel2/=pixel2[0:2]/pixel2[2]
    coefImg=np.array([pixel2[1]-pixel1[1], pixel1[0]-pixel2[0], pixel2[0]*pixel1[1]-pixel1[0]*pixel2[1]])

    return coefImg
    
def pt3d_from_pt2d(point,data):
    return np.matmul(np.linalg.inv(data.rot[0:3][:]),np.array([[(point[0]-256)*data.PS[0], (256-point[1])*data.PS[1], data.SID-data.SOD]]).T-data.tls[0:3])
