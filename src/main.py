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

plt.figure(figsize=(18,9))
plt.imshow((selectedImage1[:,:,0]*255).astype('uint8'), cmap = 'gray')
plt.imshow((selectedImage2[:,:,0]*255).astype('uint8'), cmap = 'gray')

#%%
skeltonizedImage1 = get_center_line((selectedImage1[:,:,0]*255).astype('uint8'))
skeltonizedImage2 = get_center_line((selectedImage2[:,:,0]*255).astype('uint8'))

plt.figure(figsize=(18,9))
plt.imshow(skeltonizedImage1, cmap = 'gray')
plt.imshow(skeltonizedImage2, cmap = 'gray')

# pointMatcher = PointMatcher(skeltonizedImage1, skeltonizedImage2, metadata1, metadata2)
# matchingPoints = pointMatcher.match()
# optimize

# triangulate