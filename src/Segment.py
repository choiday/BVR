import numpy as np

def segment(images, model):
    images=np.expand_dims(images, axis=3)
    images=images/255
    return model.predict(images, batch_size=2, verbose=1)