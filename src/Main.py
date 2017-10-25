import numpy as np
import os
from Render3D import render
from DICOMImage import DicomData
from Segment import *

# from ProjectionMatrix import projected_epipolar_line
# import cv2

folder='/home/rtv/workspace/BVR/resource/Data/P2PGS/DCM/'
filepath1=folder+'I0000003'
filepath2=folder+'I0000004'
Data1=DicomData(filepath1)
Data2=DicomData(filepath2)
Data1.compute_initial_transform_matrix()
Data2.compute_initial_transform_matrix()

# object segmentation
# prediction = 1
# if prediction == 1:
#     from keras.models import Model, load_model
#     model_path = './../whole_model.h5'
#     model = load_model(model_path)
#     Predict_images1=segment(Data1.images, model)
#     Predict_images2=segment(Data2.images, model)
#     np.save(folder+'predict'+filepath1[-3:]+'.npy',Predict_images1)
#     np.save(folder+'predict'+filepath2[-3:]+'.npy',Predict_images2)
# else:
#     Predict_images1=np.load(folder+'predict'+filepath1[-3:]+'.npy')
#     Predict_images2=np.load(folder+'predict'+filepath2[-3:]+'.npy')

# extract center lines


# reconstruction
target_point = [120, 112]
render(Data1, Data2, target_point)

# visualize 3d object

