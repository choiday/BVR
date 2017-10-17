import SimpleITK as sitk
import numpy as np

def getBestImage(images):
    return images[48]

def readDICOMImage(filename):
    reader=sitk.ImageFileReader()
    reader.SetFileName(filename)
    dicomImage=reader.Execute()

    if dicomImage.HasMetaDataKey('0008|0070') is not True:
        print('not DICOM image, '+type(dicomImage))
    elif dicomImage.GetMetaData('0008|0070')!='Siemens ':
        print('not Siemens, but '+dicomImage.GetMetaData('0008|0070'))
    else:
        # print('return Transform Matrix')
        SID=float(dicomImage.GetMetaData('0018|1110'))
        SOD=float(dicomImage.GetMetaData('0018|1111'))
        # mag=float(dicomImage.GetMetaData('0018|1114'))
        angle1=float(dicomImage.GetMetaData('0018|1510'))
        angle1 = np.deg2rad(angle1)
        angle2=float(dicomImage.GetMetaData('0018|1511'))
        angle2 = np.deg2rad(angle2)
        pixel_spacing=np.array(dicomImage.GetMetaData('0018|1164').split('\\')).astype(float)

    images = sitk.GetArrayFromImage(dicomImage)
    image = getBestImage(images)

    return image, {'SID':SID, 'SOD':SOD, 'PA':angle1, 'SA':angle2, 'PS':pixel_spacing}
