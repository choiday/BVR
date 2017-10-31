# from tkinter import messagebox
# from tkinter.filedialog import askopenfilename
import sys
import numpy as np

def predict_image(images, model):
    # while modelpath is not 'None':
    #     modelpath = askopenfilename()
    #     if modelpath == 'None':
    #         messagebox.showerror(title='error',message='Two images are necessary')
    # if 'keras.models' not in sys.modules :
    #     from keras.models import Model, load_model
    # model = load_model(modelpath)
    images=np.expand_dims(images, axis=3)
    images=images/255
    predicted_images = model.predict(images, batch_size=2, verbose=1)
    return predicted_images

def save_prediction(predicted_images, filepath):
    np.save(filepath[0:filepath.rfind('/')+1] +'predict'+ filepath[-3:] + '.npy', predicted_images)
    print('predicted images are saved')

def load_prediction(filepath):
    predicted_images = np.load(filepath[0:filepath.rfind('/')+1] + 'predict' + filepath[-3:] + '.npy')
    return predicted_images

def find_vessels(image):
    pass

def match_points(image1, image2, Data1, Data2):
    pass

