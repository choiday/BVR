#%%
import dicom
import SimpleITK as sitk
import numpy as np
from tkinter import messagebox

'''
from tkinter.filedialog import askopenfilenames
Files=askopenfilenames(initialdir="/home/rtv/workspace/BVR/resource/Data/")
while len(Files) is not 2:
	messagebox.showerror(title='error',message='Two images are necessary')
	Files=askopenfilenames(initialdir="/home/rtv/workspace/BVR/resource/Data/")
'''

from tkinter.filedialog import askdirectory
import glob
# dcmdir=askdirectory(initialdir='/home/rtv/workspace/BVR/resource/Data/')
dcmdir='/home/rtv/workspace/BVR/resource/Data/P5YNJ/DCM/'
dcms=sorted(glob.glob(dcmdir+"/I00*"))
while len(dcms) is 0:
	messagebox.showerror(title='error',message='no DICOM FILE')
	dcmdir=askdirectory(initialdir='/home/rtv/workspace/BVR/resource/Data/')
	dcms=sorted(glob.glob(dcmdir+"/I00*"))
reader=sitk.ImageFileReader()
#%%
#Metacode='0028|0008' #No. of Frames
#Metacode='0008|0070' #Manufacturer
#Metacode='0018|1510' #primary angle
#Metacode2='0018|1511' #Secondary angle
# Metacode='0018|1164' #pixel spacing
#Metacode='0018|1110' #SID
# Metacode='0018|1111' #SOD
# Metacode='0018|1114' #magnification
# Metacode='0020|0020' #magnification
# Metacode='0008|0008' #image type
#Metacode='0020|0030' #Image Position
# Metacode='0020|0013' #image type
# Metacode='0020|0012' #Acquisition Number
Metacode='0008|0031' # Series time
# Metacode='0008|0018' # UID
#
for i in range(len(dcms)):
	#ds=dicom.read_file(dcms[0])
	reader.SetFileName(dcms[i])
	ds=reader.Execute()
	if ds.HasMetaDataKey(Metacode):
		Mdata=ds.GetMetaData(Metacode)
		# Mdata2=ds.GetMetaData(Metacode2)
		print(Mdata)
		# print(Mdata+', '+Mdata2)
	else:
		print('None')

