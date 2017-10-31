import os
from calibration_biplane import DicomData
from segment_vessel_image import predict_image, save_prediction, load_prediction
from epipolar_projection import projected_epipolar_line
from render_epipolar_geometry import render

folder=os.getenv('HOME')+'/workspace/BVR/resource/Data/P2PGS/DCM/'
filepath1=folder+'I0000003'
filepath2=folder+'I0000004'
Data1=DicomData(filepath1)
Data2=DicomData(filepath2)
Data1.compute_transform_matrix()
Data2.compute_transform_matrix()

# object segmentation
prediction = 0
if prediction == 1:
    from keras.models import Model, load_model
    model_path = './../whole_model.h5'
    model = load_model(model_path)
    Predict_images1=predict_image(Data1.images, model)
    Predict_images2=predict_image(Data2.images, model)
    save_prediction(Predict_images1, filepath1)
    save_prediction(Predict_images2, filepath2)
else:
    Predict_images1=load_prediction(filepath1)
    Predict_images2=load_prediction(filepath2)

# extract center lines

# reconstruction
target_point = [120, 112]
render(Data1, Data2, target_point)