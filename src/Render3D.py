import vtk
import numpy as np
from vtk.util.vtkImageImportFromArray import vtkImageImportFromArray  
from ProjectionMatrix import *
from DICOMImage import DicomData
import cv2
import tkinter as tk

def createQuad(imageData):
    p0 = [-0.5, 0.5, 0.0]
    p1 = [0.5, 0.5, 0.0]
    p2 = [0.5, -0.5, 0.0]
    p3 = [-0.5, -0.5, 0.0]
    
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

def add_3dline(lines, pts, idx1, idx2, colors, color):

    if color is 'r':
        RGB = [255, 0, 0]
    elif color is 'g':
        RGB = [0, 255, 0]
    elif color is 'b':
        RGB = [0, 0, 255]
    else:
        RGB = [255, 255, 255]    
    
    colors.InsertNextTuple(RGB)
    line = vtk.vtkLine()
    line.GetPointIds().SetId(0,idx1) 
    line.GetPointIds().SetId(1,idx2)
    lines.InsertNextCell(line)

def epigeometry_points(pts, point, Data1, Data2):
    [gradient3d, point3d] = global_line_from_image_point(point, Data1)
    [epi_point1, epi_point2] = line_projection(gradient3d, point3d, Data2)

    img1_position=pt3d_from_pt2d([256.0,256.0],Data1)
    img2_position=pt3d_from_pt2d([256.0,256.0],Data2)
    source1_position=np.matmul(np.linalg.inv(Data1.rot[0:3][:]),np.array([[0.0, 0.0,-Data1.SOD]]).T-Data1.tls[0:3])
    source2_position=np.matmul(np.linalg.inv(Data2.rot[0:3][:]),np.array([[0.0, 0.0,-Data2.SOD]]).T-Data2.tls[0:3])
    target_position=pt3d_from_pt2d(point,Data1)
    epi_position1=pt3d_from_pt2d(epi_point1,Data2)
    epi_position2=pt3d_from_pt2d(epi_point2,Data2)
    
    pts.InsertNextPoint(img1_position)
    pts.InsertNextPoint(source1_position)   
    pts.InsertNextPoint(img2_position)
    pts.InsertNextPoint(source2_position)
    pts.InsertNextPoint(target_position)
    pts.InsertNextPoint(epi_position1)
    pts.InsertNextPoint(epi_position2)

    return img1_position, img2_position, epi_point1, epi_point2 

class CustomInteractor(vtk.vtkInteractorStyleTrackballCamera):
    
    def __init__(self, renderer, renWin):
        self.AddObserver('LeftButtonPressEvent', self.OnLeftButtonDown)
        self.AddObserver('LeftButtonReleaseEvent', self.OnLeftButtonRelease)
        self.AddObserver('MouseMoveEvent', self.OnMouseMove)

        self.renderer = renderer
        self.chosenPiece = None
        self.renWin = renWin

    def OnLeftButtonRelease(self, obj, eventType):
        self.chosenPiece = None
        vtk.vtkInteractorStyleTrackballCamera.OnLeftButtonUp(self)

    def OnLeftButtonDown(self, obj, eventType):
        clickPos = self.GetInteractor().GetEventPosition()

        picker = vtk.vtkPropPicker()
        picker.Pick(clickPos[0], clickPos[1], 0, self.renderer)
        actor = picker.GetActor2D()

        self.chosenPiece = actor

        vtk.vtkInteractorStyleTrackballCamera.OnLeftButtonDown(self)

    def OnMouseMove(self, obj, eventType):
        if self.chosenPiece is not None:

            mousePos = self.GetInteractor().GetEventPosition()

            self.chosenPiece.SetPosition(mousePos[0], mousePos[1])

            self.renWin.Render()
        else :
            vtk.vtkInteractorStyleTrackballCamera.OnMouseMove(self)

def ImageActor(img):
    reader = vtkImageImportFromArray()
    reader.SetArray(img)

    textureCoordinates = vtk.vtkFloatArray()
    textureCoordinates.SetNumberOfComponents(2)
    textureCoordinates.InsertNextTuple2(0.0, 1.0)
    textureCoordinates.InsertNextTuple2(1.0, 1.0)
    textureCoordinates.InsertNextTuple2(1.0, 0.0)
    textureCoordinates.InsertNextTuple2(0.0, 0.0)

    texture = vtk.vtkTexture()
    if vtk.VTK_MAJOR_VERSION <= 5:
        texture.SetInput(reader.GetOutput())
    else:
        texture.SetInputConnection(reader.GetOutputPort())
    
    mapper=vtk.vtkImageMapper()
    mapper.SetInputConnection(reader.GetOutputPort())
    actor=vtk.vtkImageActor()
    # actor.SetMapper(mapper)
    actor.SetInputData(reader.GetOutput())
    
    return actor


def render(file1, file2, point):
    
    Data1=DicomData(file1)
    Data2=DicomData(file2)
    Data1.compute_initial_transform_matrix()
    Data2.compute_initial_transform_matrix()

    img1=Data1.img.copy()
    img2=Data2.img.copy()

    # Create a render window
    ren = vtk.vtkRenderer()
    ren.SetBackground(.1, .2, .5)
    ren2dimg1 = vtk.vtkRenderer()
    # ren2dimg1.SetBackground(.1, .2, .5)
    ren2dimg2= vtk.vtkRenderer()
    # ren2dimg2.SetBackground(.1, .2, .5)
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)
    renWin.AddRenderer(ren2dimg1)
    renWin.AddRenderer(ren2dimg2)
    renWin.SetSize(1536,1024)
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    pts = vtk.vtkPoints()

    [img1_position, img2_position, epi_point1, epi_point2] = epigeometry_points(pts, point, Data1, Data2)   

    cv2.circle(img1,(point[0],point[1]),10,(255,0,0),-1)
    cv2.line(img2,(int(epi_point1[0]), int(epi_point1[1])),(int(epi_point2[0]), int(epi_point2[1])),(255,0,0),5)
    cv2.putText(img1,str(int(np.rad2deg(Data1.PA)))+', '+str(int(np.rad2deg(Data1.SA))),(10, 100),1,4,(255,255,255),2,cv2.LINE_AA)
    cv2.putText(img2,str(int(np.rad2deg(Data2.PA)))+', '+str(int(np.rad2deg(Data2.SA))),(10, 100),1,4,(255,255,255),2,cv2.LINE_AA) 

    colors = vtk.vtkUnsignedCharArray()
    colors.SetNumberOfComponents(3)
    colors.SetName("Colors")

    lines = vtk.vtkCellArray()

    add_3dline(lines, pts, 0, 1, colors, 'r')
    add_3dline(lines, pts, 2, 3, colors, 'g')
    add_3dline(lines, pts, 1, 4, colors, 'w')
    add_3dline(lines, pts, 3, 5, colors, 'w')
    add_3dline(lines, pts, 3, 6, colors, 'w')
    add_3dline(lines, pts, 5, 6, colors, 'w')

    linesPolyData = vtk.vtkPolyData()
    linesPolyData.SetPoints(pts)
    linesPolyData.SetLines(lines)
    linesPolyData.GetCellData().SetScalars(colors)

    mapper = vtk.vtkPolyDataMapper()
    if vtk.VTK_MAJOR_VERSION <= 5:
        mapper.SetInput(linesPolyData)
    else:
        mapper.SetInputData(linesPolyData)    
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    transform1 = vtk.vtkTransform()
    transform1.Translate(img1_position)
    transform1.RotateY(np.rad2deg(Data1.PA))
    transform1.RotateX(-np.rad2deg(Data1.SA))
    transform1.Scale(img1.shape[0]*Data1.PS[0],img1.shape[1]*Data1.PS[1],1)

    transform2 = vtk.vtkTransform()
    transform2.Translate(img2_position)
    transform2.RotateY(np.rad2deg(Data2.PA))
    transform2.RotateZ(-np.rad2deg(Data2.SA))
    # transform2.RotateX(-CRAU)
    transform2.Scale(img2.shape[0]*Data2.PS[0],img2.shape[1]*Data2.PS[1],1)

    planeA_actor = createQuad(img1)
    planeA_actor.SetUserTransform(transform1)

    planeB_actor = createQuad(img2)
    planeB_actor.SetUserTransform(transform2)

    axes = vtk.vtkAxesActor()
    transform = vtk.vtkTransform()
    transform.Scale(100, 100, 100)
    axes.SetUserTransform(transform)
    
    textProperty = vtk.vtkTextProperty()
    textProperty.SetFontSize(25)
    textProperty.SetJustificationToCentered()

    textMapper=vtk.vtkTextMapper()
    textActor=vtk.vtkActor2D()
    textMapper.SetInput('Epipolar Geometry')
    textMapper.SetTextProperty(textProperty)
    textActor.SetMapper(textMapper)
    textActor.SetPosition(512,950)

    ren.AddActor(actor)
    ren.AddActor(planeA_actor)
    ren.AddActor(planeB_actor)
    ren.AddActor(axes)
    ren.AddViewProp(textActor)
    ren.SetViewport([0.0, 0.0, 2/3, 1.0])

    img2dactor1=ImageActor(img1)
    ren2dimg1.AddActor(img2dactor1)
    ren2dimg1.SetViewport([2/3,0.5,1.0,1.0])
    
    img2dactor2=ImageActor(img2)
    ren2dimg2.AddActor(img2dactor2)
    ren2dimg2.SetViewport([2/3,0.0,1.0,0.5])

    iren.Initialize()
    renWin.Render()
    iren.Start()
