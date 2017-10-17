import vtk
import numpy as np
from vtk.util.vtkImageImportFromArray import vtkImageImportFromArray  
from DICOMImage import readDICOMImage
import cv2

def createQuad(imageData):
    p0 = [0.0, 0.0, 0.0]
    p1 = [1.0, 0.0, 0.0]
    p2 = [1.0, 1.0, 0.0]
    p3 = [0.0, 1.0, 0.0]
    points = vtk.vtkPoints()
    points.InsertNextPoint(p0)
    points.InsertNextPoint(p1)
    points.InsertNextPoint(p2)
    points.InsertNextPoint(p3)
    quad = vtk.vtkQuad()
    quad.GetPointIds().SetNumberOfIds(4)
    quad.GetPointIds().SetId(0,0)
    quad.GetPointIds().SetId(1,1)
    quad.GetPointIds().SetId(2,2)
    quad.GetPointIds().SetId(3,3)
    quads = vtk.vtkCellArray()
    quads.InsertNextCell(quad)

    polydata = vtk.vtkPolyData()
    polydata.SetPoints(points)
    polydata.SetPolys(quads)

    textureCoordinates = vtk.vtkFloatArray()
    textureCoordinates.SetNumberOfComponents(2)
    textureCoordinates.InsertNextTuple2(0.0, 0.0)
    textureCoordinates.InsertNextTuple2(1.0, 0.0)
    textureCoordinates.InsertNextTuple2(1.0, 1.0)
    textureCoordinates.InsertNextTuple2(0.0, 1.0)
    polydata.GetPointData().SetTCoords(textureCoordinates)

    # Read the image data from a file
    reader = vtkImageImportFromArray()
    reader.SetArray(imageData)
    # reader = vtk.vtkPNGReader()
    # reader.SetFileName(imagefile)

    # Create texture object
    texture = vtk.vtkTexture()
    if vtk.VTK_MAJOR_VERSION <= 5:
        texture.SetInput(reader.GetOutput())
    else:
        texture.SetInputConnection(reader.GetOutputPort())

    mapper = vtk.vtkPolyDataMapper()
    if vtk.VTK_MAJOR_VERSION <= 5:
        mapper.SetInput(polydata)
    else:
        mapper.SetInputData(polydata)

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.SetTexture(texture)

    return actor

def render(file1, file2):
    # Create a render window
    ren = vtk.vtkRenderer()
    ren.SetBackground(.1, .2, .5)
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)
    renWin.SetSize(480,480)
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    scale = 300

    img1, metadata1 = readDICOMImage(file1)
    img2, metadata2 = readDICOMImage(file2)

    cv2.line(img2,(0,0),(511,511),(255,0,0),5)

    transform1 = vtk.vtkTransform()
    
    RAO = np.rad2deg(metadata1['PA'])
    CRAU = np.rad2deg(metadata1['SA'])
    transform1.RotateY(-RAO)
    transform1.RotateX(CRAU)
    transform1.Translate(0, 0, metadata1['SID'] - metadata1['SOD'])
    transform1.Scale(scale,scale,scale)

    transform2 = vtk.vtkTransform()
    RAO = np.rad2deg(metadata2['PA'])
    CRAU = np.rad2deg(metadata2['SA'])
    transform2.RotateY(-RAO)
    transform2.RotateX(CRAU)
    transform2.Translate(0, 0, metadata2['SID'] - metadata2['SOD'])
    transform2.Scale(scale,scale,scale)

    actor1 = createQuad(img1)
    actor1.SetUserTransform(transform1)

    actor2 = createQuad(img2)
    actor2.SetUserTransform(transform2)

    axes = vtk.vtkAxesActor()
    transform = vtk.vtkTransform()
    transform.Scale(100, 100, 100)
    axes.SetUserTransform(transform)

    ren.AddActor(actor1)
    ren.AddActor(actor2)
    ren.AddActor(axes)

    iren.Initialize()
    renWin.Render()
    iren.Start()
