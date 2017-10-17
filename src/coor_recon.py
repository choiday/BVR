#%%
import SimpleITK as sitk
import numpy as np
from tkinter.filedialog import askopenfilenames

filepath1='/home/rtv/workspace/BVR/resource/Data/P1KOR/DCM/I0000006'
filepath2='/home/rtv/workspace/BVR/resource/Data/P1KOR/DCM/I0000007'
'''
Files=askopenfilenames()
while len(Files) is not 2:
	messagebox.showerror(title='error',message='Two images are necessary')
	Files=askopenfilenames()
'''
reader=sitkImageFileReader()

reader.SetFileName(filepath2)
Data1=reader.Execute()

reader.SetFileName(filepath2)
Data2=reader.Execute()

SID1=Data1.GetMetaData('0018|1110')
angle11=Data1.GetMetaData('0018|1510')
angle12=Data1.GetMetaData('0018|1511')
pixel_spacing1=Data1.GetMetaData('0028|0030')

SID2=Data2.GetMetaData('0018|1110')
angle21=Data2.GetMetaData('0018|1510')
angle22=Data2.GetMetaData('0018|1511')
pixel_spacing2=Data2.GetMetaData('0028|0030')

trans=Data1.GetMetaData('0018|5212')
trans

#%%
K1=np.matrix([[SID1,0,256],[0,SID1,256],[0,0,1]],dtype='float64')
K2=np.matrix([[SID2,0,256],[0,SID2,256],[0,0,1]],dtype='float64')
R1=np.identity(3,dtype='float64')
t1=np.zeros((3,1),dtype='float64')
P1=np.matmul(K1_i,np.hstack([R1,t1]))