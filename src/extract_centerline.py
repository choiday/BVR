#%%
# from calibration_biplane import DicomData
import numpy as np
# from scipy import ndimage as ndi
import cv2
# from matplotlib import pyplot as plt 
from skimage.morphology import medial_axis

def get_center_line(image):
    # gray=np.expand_dims(image, axis=2)
    blur = cv2.GaussianBlur(image, (5,5), 0)
    ret3,th3 = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    kernel = np.ones((5,5), np.uint8)
    morph = cv2.dilate(th3, kernel, iterations = 1)
    kernel = np.ones((2,2), np.uint8)
    morph2 = cv2.erode(morph, kernel, iterations = 1)
    #morph = cv2.morphologyEx(th3, cv2.MORPH_CLOSE, kernel)

    skel, distance = medial_axis(morph2, return_distance=True)
    distonskel = distance * skel

    ret1,th1 = cv2.threshold(distonskel, 0, 100, cv2.THRESH_BINARY)
    return th1