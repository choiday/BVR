import vtk
import numpy as np
from vtk.util.vtkImageImportFromArray import vtkImageImportFromArray  
from ProjectionMatrix import *
from DICOMImage import DicomData
import cv2

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

def render(file1, file2):
    # Create a render window
    ren = vtk.vtkRenderer()
    ren.SetBackground(.1, .2, .5)
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)
    renWin.SetSize(1024,1024)
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    scale = 512

    point=[120,120]

    Data1=DicomData(file1)
    Data2=DicomData(file2)
    Data1.compute_initial_transform_matrix()
    Data2.compute_initial_transform_matrix()
    img1=Data1.img.copy()
    img2=Data2.img.copy()

    # coef_img = projected_epipolar_line(point, Data1, Data2)
    [gradient3d, point3d] = global_line_from_image_point(point, Data1)
    [epi_point1, epi_point2] = line_projection(gradient3d, point3d, Data2)

    cv2.circle(img1,(point[0],point[1]),10,(255,0,0),-1)
    cv2.line(img2,(int(epi_point1[0]), int(epi_point1[1])),(int(epi_point2[0]), int(epi_point2[1])),(255,0,0),5)

    cv2.putText(img1,str(int(np.rad2deg(Data1.PA)))+', '+str(int(np.rad2deg(Data1.SA))),(10, 100),1,4,(255,255,255),2,cv2.LINE_AA)
    cv2.putText(img2,str(int(np.rad2deg(Data2.PA)))+', '+str(int(np.rad2deg(Data2.SA))),(10, 100),1,4,(255,255,255),2,cv2.LINE_AA)

    img1_position=pt3d_from_pt2d([256.0,256.0],Data1)
    img2_position=pt3d_from_pt2d([256.0,256.0],Data2)
    source1_position=np.matmul(np.linalg.inv(Data1.rot[0:3][:]),np.array([[0.0, 0.0,-Data1.SOD]]).T-Data1.tls[0:3])
    source2_position=np.matmul(np.linalg.inv(Data2.rot[0:3][:]),np.array([[0.0, 0.0,-Data2.SOD]]).T-Data2.tls[0:3])
    target_position=pt3d_from_pt2d(point,Data1)
    # epi_point1=[0,-coef_img[2]/coef_img[1]]
    # epi_point2=[511,-(511*coef_img[0]+coef_img[2])/coef_img[1]]
    epi_position1=pt3d_from_pt2d(epi_point1,Data2)
    epi_position2=pt3d_from_pt2d(epi_point2,Data2)
        
    # draw 3d lines
    pts = vtk.vtkPoints()
    # pts.InsertNextPoint([0.0, 0.0, 0.0])
    # pts.InsertNextPoint([1000.0, 0.0, 0.0])
    # pts.InsertNextPoint([0.0, 1000.0, 0.0])
    pts.InsertNextPoint(img1_position)
    pts.InsertNextPoint(source1_position)   
    pts.InsertNextPoint(img2_position)
    pts.InsertNextPoint(source2_position)
    pts.InsertNextPoint(target_position)
    # pts.InsertNextPoint(gradient3d+point3d)
    # pts.InsertNextPoint(point3d)   
    pts.InsertNextPoint(epi_position1)
    pts.InsertNextPoint(epi_position2)    
    

    red = [255, 0, 0]
    green = [0, 255, 0]
    white = [255, 255, 255]

    colors = vtk.vtkUnsignedCharArray()
    colors.SetNumberOfComponents(3)
    colors.SetName("Colors")
    colors.InsertNextTuple(red)
    colors.InsertNextTuple(green)
    colors.InsertNextTuple(white)
    colors.InsertNextTuple(white)
    colors.InsertNextTuple(white)
    colors.InsertNextTuple(white)

    line0 = vtk.vtkLine()
    line0.GetPointIds().SetId(0,0) # the second 0 is the index of the Origin in the vtkPoints
    line0.GetPointIds().SetId(1,1) # the second 1 is the index of P0 in the vtkPoints
    line1 = vtk.vtkLine()
    line1.GetPointIds().SetId(0,2) # the second 0 is the index of the Origin in the vtkPoints
    line1.GetPointIds().SetId(1,3) # 2 is the index of P1 in the vtkPoints
    line2 = vtk.vtkLine()
    line2.GetPointIds().SetId(0,1) 
    line2.GetPointIds().SetId(1,4) 
    line3 = vtk.vtkLine()
    line3.GetPointIds().SetId(0,3) 
    line3.GetPointIds().SetId(1,5) 
    line4 = vtk.vtkLine()
    line4.GetPointIds().SetId(0,3) 
    line4.GetPointIds().SetId(1,6) 
    line5 = vtk.vtkLine()
    line5.GetPointIds().SetId(0,5) 
    line5.GetPointIds().SetId(1,6) 
    
    lines = vtk.vtkCellArray()
    lines.InsertNextCell(line0)
    lines.InsertNextCell(line1)
    lines.InsertNextCell(line2)
    lines.InsertNextCell(line3)
    lines.InsertNextCell(line4)
    lines.InsertNextCell(line5)

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
    ren.AddActor(actor)

    transform1 = vtk.vtkTransform()
    
    RAO = np.rad2deg(Data1.PA)
    CRAU = np.rad2deg(Data1.SA)
    transform1.Translate(img1_position)
    transform1.RotateY(RAO)
    transform1.RotateX(-CRAU)
    transform1.Scale(img1.shape[0]*Data1.PS[0],img1.shape[1]*Data1.PS[1],1)

    transform2 = vtk.vtkTransform()
    RAO = np.rad2deg(Data2.PA)
    CRAU = np.rad2deg(Data2.SA)
    transform2.Translate(img2_position)
    transform2.RotateY(RAO)
    transform2.RotateX(-CRAU)
    transform2.Scale(img2.shape[0]*Data2.PS[0],img2.shape[1]*Data2.PS[1],1)

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
