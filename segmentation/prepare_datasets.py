#==========================================================
#
#  This prepare the hdf5 datasets of the IMGC database
#
#============================================================

import os
import h5py
import numpy as np
from PIL import Image
from skimage.exposure import histogram
import numpy as np
from scipy import ndimage as ndi
from skimage.io import *

def threshold_minimum(image, nbins=256, max_iter=10000):
    def find_local_maxima_idx(hist):
        maximum_idxs = list()
        direction = 1

        for i in range(hist.shape[0] - 1):
            if direction > 0:
                if hist[i + 1] < hist[i]:
                    direction = -1
                    maximum_idxs.append(i)
            else:
                if hist[i + 1] > hist[i]:
                    direction = 1

        return maximum_idxs

    hist, bin_centers = histogram(image.ravel(), nbins)

    smooth_hist = np.copy(hist).astype(np.float64)

    for counter in range(max_iter):
        smooth_hist = ndi.uniform_filter1d(smooth_hist, 3)
        maximum_idxs = find_local_maxima_idx(smooth_hist)
        if len(maximum_idxs) < 5:
            break

    # Find lowest point between the maxima
    threshold_idx = np.argmin(smooth_hist[maximum_idxs[0]:maximum_idxs[1] + 1])
    return bin_centers[maximum_idxs[0] + threshold_idx]

def write_hdf5(arr,outfile):
  with h5py.File(outfile,"w") as f:
    f.create_dataset("image", data=arr, dtype=arr.dtype)

#------------Path of the images --------------------------------------------------------------
#train
original_imgs_train = "./resource/IMGC/training/images/"
groundTruth_imgs_train = "./resource/IMGC/training/labels/"

#test
original_imgs_test = "./resource/IMGC/test/images/"
groundTruth_imgs_test = "./resource/IMGC/test/labels/"
#---------------------------------------------------------------------------------------------

Nimgs = 20
height = 512
width = 512
dataset_path = "./IMGC_datasets_training_testing/"

def get_datasets(imgs_dir, groundTruth_dir):
    imgs = np.empty((Nimgs,height,width))
    groundTruth = np.empty((Nimgs,height,width))
    border_masks = np.empty((Nimgs,height,width))
    for path, subdirs, files in os.walk(imgs_dir): #list all files, directories in the path
        for i in range(len(files)):
            #original
            print ("original image: " +files[i])
            img = Image.open(imgs_dir+files[i])
            imgs[i] = np.asarray(img)

            #corresponding ground truth
            groundTruth_name = files[i]
            g_truth = Image.open(groundTruth_dir + groundTruth_name)
            groundTruth[i] = np.asarray(g_truth)

            for j in range(groundTruth.shape[1]):
                for k in range(groundTruth.shape[2]):
                    if groundTruth[i][j][k] > 1:
                        groundTruth[i][j][k] = 1

            #corresponding border masks
            image = imread(imgs_dir+files[i])
            thresh_min = threshold_minimum(image)
            b_mask = image > thresh_min
            imsave(imgs_dir+"/../mask_"+files[i], b_mask*255)
            border_masks[i] = np.asarray(b_mask*255)

    print ("imgs max: " +str(np.max(imgs)))
    print ("imgs min: " +str(np.min(imgs)))

    print ("groundTruth max: " +str(np.max(groundTruth)))
    print ("groundTruth min: " +str(np.min(groundTruth)))

    #reshaping for my standard tensors
    #imgs = np.transpose(imgs,(0,1,2))
    assert(imgs.shape == (Nimgs,height,width))
    imgs = np.reshape(imgs,(Nimgs,1,height,width))
    groundTruth = np.reshape(groundTruth,(Nimgs,1,height,width))
    border_masks = np.reshape(border_masks,(Nimgs,1,height,width))
    return imgs, groundTruth, border_masks

if not os.path.exists(dataset_path):
    os.makedirs(dataset_path)

#getting the training datasets
imgs_train, groundTruth_train, border_masks_train = get_datasets(original_imgs_train,groundTruth_imgs_train)
print ("saving train datasets")
write_hdf5(imgs_train, dataset_path + "IMGC_dataset_imgs_train.hdf5")
write_hdf5(groundTruth_train, dataset_path + "IMGC_dataset_groundTruth_train.hdf5")
write_hdf5(border_masks_train,dataset_path + "IMGC_dataset_borderMasks_train.hdf5")

#getting the testing datasets
imgs_test, groundTruth_test, border_masks_test = get_datasets(original_imgs_test,groundTruth_imgs_test)
print ("saving test datasets")
write_hdf5(imgs_test,dataset_path + "IMGC_dataset_imgs_test.hdf5")
write_hdf5(groundTruth_test, dataset_path + "IMGC_dataset_groundTruth_test.hdf5")
write_hdf5(border_masks_test,dataset_path + "IMGC_dataset_borderMasks_test.hdf5")
