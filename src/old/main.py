import os
from calibration_biplane import DicomData
from segment_vessel_image import predict_image, load_prediction
# from epipolar_projection import projected_epipolar_line
from render_epipolar_geometry import render

# prepare dicom dataset
[data1, data2] = DicomData.call_test_data()

# object segmentation
prediction = 0
if prediction == 1:
    modelPath = './../whole_model.h5'
    predict_image(data1, data2, modelPath)
predictImgs1=load_prediction(data1.path)
predictImgs2=load_prediction(data2.path)

# extract center lines
data1.img = predictImgs1[2]

# render epipolar geometry
targetPoint = [120, 112]
render(data1, data2, targetPoint)

# reconstruction