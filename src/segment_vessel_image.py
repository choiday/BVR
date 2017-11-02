# from tkinter import messagebox
# from tkinter.filedialog import askopenfilename
import sys, os
import numpy as np

class ImageSelector():
    def __init__(self, images1, images2, filepath1, filepath2):
        self.images1 = images1
        self.images2 = images2
        self.filepath1 = filepath1
        self.filepath2 = filepath2
        self.modelpath = './../whole_model.h5'
        
    def select(self):
        if os.path.exists(self.filepath1[0:self.filepath1.rfind('/')+1] +'predict'+ self.filepath1[-3:] + '.npy') is False:
            from keras.models import load_model
            model = load_model(self.modelpath)
            self.tempImages1=np.expand_dims(self.images1, axis=3)
            self.tempImages1=self.tempImages1/255
            self.tempImages2=np.expand_dims(self.images2, axis=3)
            self.tempImages2=self.tempImages2/255
            self.predictedImages1 = model.predict(self.tempImages1, batch_size=2, verbose=1)
            self.predictedImages2 = model.predict(self.tempImages2, batch_size=2, verbose=1)
            save_prediction(self.predictedImages1, self.filepath1)
            save_prediction(self.predictedImages2, self.filepath2)
        else:
            self.predictedImages1 = load_prediction(self.filepath1)
            self.predictedImages2 = load_prediction(self.filepath2)

        selected=26
        return [self.predictedImages1[selected,:,:,0], self.predictedImages2[selected,:,:,0]]

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

