from Render3D import render
from ProjectionMatrix import projected_epipolar_line
from DICOMImage import readDICOMImage
import cv2

filepath1='/home/rtv/workspace/BVR/resource/Data/P2PGS/DCM/I0000004'
filepath2='/home/rtv/workspace/BVR/resource/Data/P2PGS/DCM/I0000005'

render(filepath1, filepath2)