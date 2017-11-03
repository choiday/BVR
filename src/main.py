#%%
import os, sys
sys.path.append(os.getenv('HOME')+'/workspace/BVR/src')
import matplotlib.pyplot as plt
from calibration_biplane import parse_dicom
from segment_vessel_image import ImageSelector
from extract_centerline import get_center_line

metadata1, images1 = parse_dicom('temp1')
metadata2, images2 = parse_dicom('temp2')

imageSelector = ImageSelector(images1, images2, metadata1['path'], metadata2['path'])
[selectedImage1, selectedImage2] = imageSelector.select()

skeltonizedImage1 = get_center_line((selectedImage1*255).astype('uint8'))
skeltonizedImage2 = get_center_line((selectedImage2*255).astype('uint8'))

# pointMatcher = PointMatcher(skeltonizedImage1, skeltonizedImage2, metadata1, metadata2)
# matchingPoints = pointMatcher.match()
# optimize

# triangulate

#%%
show_image_sequence()

#%%
show_frames()

#%%
plt.figure(figsize=(13,13))
plt.imshow(skeltonizedImage1,cmap='gray')

#%%
def show_image_sequence():
    showimages = [[],[],[]]
    showimages[0].append(images1[imageSelector.selected])
    showimages[0].append(images2[imageSelector.selected])
    showimages[1].append((selectedImage1*255).astype('uint8'))
    showimages[1].append((selectedImage2*255).astype('uint8'))
    showimages[2].append(skeltonizedImage1)
    showimages[2].append(skeltonizedImage2)

    [_, axes] = plt.subplots(len(showimages),len(showimages[0]),figsize=(14,21))
    for i in range(len(showimages)):
        for j in range(len(showimages[0])):
            axes[i][j].imshow(showimages[i][j],cmap='gray')
            axes[i][j].set_xticklabels([])
            axes[i][j].set_yticklabels([])
    plt.subplots_adjust(wspace=0, hspace=0.03)

def show_frames():
    frames=len(imageSelector.predictedImages1)
    [_, axes] = plt.subplots(frames,2,figsize=(14,7*frames))
    for i in range(frames):
        axes[i][0].imshow(imageSelector.predictedImages1[i,:,:,0],cmap='gray')
        axes[i][1].imshow(imageSelector.predictedImages2[i,:,:,0],cmap='gray')
        axes[i][0].set_xticklabels([])
        axes[i][0].set_yticklabels([])
        axes[i][1].set_xticklabels([])
        axes[i][1].set_yticklabels([])
    plt.subplots_adjust(wspace=0, hspace=0.03)
