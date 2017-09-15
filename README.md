
# Blood Vessel Reconstruction

This is a blood vessel reconstruction project. There is a main goal which can be broadly divided into 3 steps. Firstly, it is needed to process DICOM images. DICOM images have some noise thus, it should be simplified by segmentation algorithm. And then the image can be used to extract the medial axis by skeletonization algoritm. Secondly, ... Finally, the image can be reconstructed in 3D mesh model.

**Prerequisites**

* scikit-learn >= 0.18.1
* SimpleITK >= 1.0.1

