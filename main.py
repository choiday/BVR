#%%
from PIL import Image
import cv2
import numpy as np
from matplotlib import pyplot as plt
from skimage.exposure import histogram
from scipy import ndimage as ndi

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

img1 = np.asarray(Image.open("/home/rtv/workspace/BVR/test/test_Prediction10.png"))
img2 = np.asarray(Image.open("/home/rtv/workspace/BVR/test/test_Prediction13.png"))
#img1 = np.asarray(Image.open("/home/rtv/workspace/BVR/resource/IMGC/training/labels/img7.gif"))
#img2 = np.asarray(Image.open("/home/rtv/workspace/BVR/resource/IMGC/training/labels/img8.gif"))

#thresh_min1 = threshold_minimum(img1)
#b_mask1 = np.asarray((img1 > thresh_min1)*255, dtype = np.uint8)
#thresh_min2 = threshold_minimum(img2)
#b_mask2 = np.asarray((img2 > thresh_min2)*255, dtype = np.uint8)

#b_mask1 = cv2.cvtColor(b_mask1, cv2.CV_8UC1)

sift = cv2.xfeatures2d.SIFT_create()
# find the keypoints and descriptors with SIFT
#kp1, des1 = sift.detectAndCompute(img1,mask=b_mask1)
#kp2, des2 = sift.detectAndCompute(img2,mask=b_mask2)
kp1, des1 = sift.detectAndCompute(img1,None)
kp2, des2 = sift.detectAndCompute(img2,None)

# FLANN parameters
FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks=50)
flann = cv2.FlannBasedMatcher(index_params,search_params)
matches = flann.knnMatch(des1,des2,k=2)
good = []
pts1 = []
pts2 = []
# ratio test as per Lowe's paper
for i,(m,n) in enumerate(matches):
    if m.distance < 0.8*n.distance:
        good.append(m)
        pts2.append(kp2[m.trainIdx].pt)
        pts1.append(kp1[m.queryIdx].pt)

plt.figure(figsize=(20,20))
plt.subplot(211),plt.imshow(img1, cmap='gray')
plt.scatter(*zip(*pts1),color=['red','green','blue'])
plt.subplot(212),plt.imshow(img2, cmap='gray')
plt.scatter(*zip(*pts2),color=['red','green','blue'])

#%%
pts1 = np.int32(pts1)
pts2 = np.int32(pts2)
F, mask = cv2.findFundamentalMat(pts1,pts2,cv2.FM_LMEDS)
# We select only inlier points
pts1 = pts1[mask.ravel()==1]
pts2 = pts2[mask.ravel()==1]

def drawlines(img1,img2,lines,pts1,pts2):
    ''' img1 - image on which we draw the epilines for the points in img2
        lines - corresponding epilines '''
    r,c = img1.shape
    img1 = cv2.cvtColor(img1,cv2.COLOR_GRAY2BGR)
    img2 = cv2.cvtColor(img2,cv2.COLOR_GRAY2BGR)
    for r,pt1,pt2 in zip(lines,pts1,pts2):
        color = tuple(np.random.randint(0,255,3).tolist())
        x0,y0 = map(int, [0, -r[2]/r[1] ])
        x1,y1 = map(int, [c, -(r[2]+r[0]*c)/r[1] ])
        img1 = cv2.line(img1, (x0,y0), (x1,y1), color,1)
        img1 = cv2.circle(img1,tuple(pt1),5,color,-1)
        img2 = cv2.circle(img2,tuple(pt2),5,color,-1)
    return img1,img2

# Find epilines corresponding to points in right image (second image) and
# drawing its lines on left image
lines1 = cv2.computeCorrespondEpilines(pts2.reshape(-1,1,2), 2,F)
lines1 = lines1.reshape(-1,3)
img5,img6 = drawlines(img1,img2,lines1,pts1,pts2)
# Find epilines corresponding to points in left image (first image) and
# drawing its lines on right image
lines2 = cv2.computeCorrespondEpilines(pts1.reshape(-1,1,2), 1,F)
lines2 = lines2.reshape(-1,3)
img3,img4 = drawlines(img2,img1,lines2,pts2,pts1)
plt.subplot(121),plt.imshow(img5)
plt.subplot(122),plt.imshow(img3)
plt.show()