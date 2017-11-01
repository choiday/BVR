# from tkinter import messagebox
# from tkinter.filedialog import askopenfilename
import sys
import numpy as np

class ImageSelector():
    def __init__(self, images1, images2):
        self.images1 = images1
        self.images2 = images2
    
    def select(self):
        selected=26
        return [self.images1[selected], self.images2[selected]]

def predict_image(data1, data2, modelPath):
    from keras.models import load_model
    model = load_model(modelPath)
    images1=np.expand_dims(data1.images, axis=3)
    images1=images1/255
    images2=np.expand_dims(data2.images, axis=3)
    images2=images2/255
    predictImgs1 = model.predict(images1, batch_size=2, verbose=1)
    predictImgs2 = model.predict(images2, batch_size=2, verbose=1)
    save_prediction(predictImgs1, data1.path)
    save_prediction(predictImgs2, data2.path)
    return [predictImgs1, predictImgs2]

def save_prediction(predictImgs, filepath):
    np.save(filepath[0:filepath.rfind('/')+1] +'predict'+ filepath[-3:] + '.npy', predicted_images)
    print('predicted images are saved')

def load_prediction(filepath):
    predictImgs = np.load(filepath[0:filepath.rfind('/')+1] + 'predict' + filepath[-3:] + '.npy')
    return predictImgs

def find_vessels(image):
    pass

def match_points(image1, image2, Data1, Data2):
    pass

