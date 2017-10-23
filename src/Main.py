from Render3D import render
# from ProjectionMatrix import projected_epipolar_line
# import cv2

filepath1='/home/rtv/workspace/BVR/resource/Data/P2PGS/DCM/I0000003'
filepath2='/home/rtv/workspace/BVR/resource/Data/P2PGS/DCM/I0000004'

# object segmentation

# extract center lines

# reconstruction
target_point = [120, 112]
render(filepath1, filepath2, target_point)

# visualize 3d object

