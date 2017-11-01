import vtk
import numpy as np
from vtk.util.vtkImageImportFromArray import vtkImageImportFromArray  
# from calibration_biplane import *
from epipolar_projection import *
# from extract_centerline import *
import cv2 

def create_3dquad_imageactor(image):
    w=image.shape[0]
    h=image.shape[1]
    p0 = [-w/2, h/2, 0.0]
    p1 = [w/2, h/2, 0.0]
    p2 = [w/2, -h/2, 0.0]
    p3 = [-w/2, -h/2, 0.0]
    
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
    
    reader = vtkImageImportFromArray()
    reader.SetArray(image)

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

def epigeometry_points(pts, point, data1, data2):
    [gradient3d, point3d] = global_line_from_image_point(point, data1)
    [epipoint1, epipoint2] = line_projection(gradient3d, point3d, data2)

    camPosition1=pt3d_from_pt2d([256.0,256.0],data1)
    camPosition2=pt3d_from_pt2d([256.0,256.0],data2)
    source1=point3d
    source2=np.matmul(np.linalg.inv(data2.rot[0:3][:]),np.array([[0.0, 0.0,-data2.SOD]]).T-data2.tls[0:3])
    targetPoint3D=pt3d_from_pt2d(point,data1)
    epipoint3d1=pt3d_from_pt2d(epipoint1,data2)
    epipoint3d2=pt3d_from_pt2d(epipoint2,data2)
    
    pts.InsertNextPoint(camPosition1)
    pts.InsertNextPoint(source1)   
    pts.InsertNextPoint(camPosition2)
    pts.InsertNextPoint(source2)
    pts.InsertNextPoint(targetPoint3D)
    pts.InsertNextPoint(epipoint3d1)
    pts.InsertNextPoint(epipoint3d2)

    return camPosition1, camPosition2, epipoint1, epipoint2 


def render(data1, data2, point):

    ren = vtk.vtkRenderer()
    ren.SetBackground(.1, .2, .5)
    ren2dimg1 = vtk.vtkRenderer()
    ren2dimg2= vtk.vtkRenderer()
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)
    renWin.AddRenderer(ren2dimg1)
    renWin.AddRenderer(ren2dimg2)
    renWin.SetSize(1536,1024)
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    pts = vtk.vtkPoints()

    [camPosition1, camPosition2, epipoint1, epipoint2] = epigeometry_points(pts, point, data1, data2)    

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
    lineactor = vtk.vtkActor()
    lineactor.SetMapper(mapper)

    img1=data1.images[26].copy()
    img2=data2.images[26].copy()
    # img1=get_center_line(data1.images[26])
    # img2=get_center_line(data2.images[26])

    cv2.circle(img1,(point[0],point[1]),10,(255,0,0),-1)
    cv2.line(img2,(int(epipoint1[0]), int(epipoint1[1])),(int(epipoint2[0]), int(epipoint2[1])),(255,0,0),5)
    cv2.putText(img1,str(int(np.rad2deg(data1.PA)))+', '+str(int(np.rad2deg(data1.SA))),(10, 100),1,4,(255,255,255),2,cv2.LINE_AA)
    cv2.putText(img2,str(int(np.rad2deg(data2.PA)))+', '+str(int(np.rad2deg(data2.SA))),(10, 100),1,4,(255,255,255),2,cv2.LINE_AA)
    
    reader1=vtkImageImportFromArray()
    reader1.SetArray(img1)
    reader1.Update()
    fliper1=vtk.vtkImageFlip()
    fliper1.SetFilteredAxis(1)
    fliper1.SetInputConnection(reader1.GetOutputPort())
    fliper1.Update()
    
    reader2=vtkImageImportFromArray()
    reader2.SetArray(img2)
    reader2.Update()
    fliper2=vtk.vtkImageFlip()
    fliper2.SetFilteredAxis(1)
    fliper2.SetInputConnection(reader2.GetOutputPort())
    fliper2.Update()

    planeAactor = create_3dquad_imageactor(img1)
    planeAactor.SetPosition(camPosition1)
    planeAactor.SetScale(data1.PS[0],data1.PS[1],1)
    planeAactor.RotateY(np.rad2deg(data1.PA))
    planeAactor.RotateX(-np.rad2deg(data1.SA))
    # planeA_actor.SetUserTransform(transform1)

    planeBactor = create_3dquad_imageactor(img2)
    planeBactor.SetPosition(camPosition2)
    planeBactor.SetScale(data2.PS[0],data2.PS[1],1)
    planeBactor.RotateY(np.rad2deg(data2.PA))
    planeBactor.RotateZ(-np.rad2deg(data2.SA))
    # planeB_actor.SetUserTransform(transform2)

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

    ren.AddActor(lineactor)
    ren.AddActor(planeAactor)
    ren.AddActor(planeBactor)
    ren.AddActor(axes)
    ren.AddViewProp(textActor)
    ren.SetViewport([0.0, 0.0, 2/3, 1.0])

    mapper2d1=vtk.vtkImageMapper()
    mapper2d1.SetInputConnection(fliper1.GetOutputPort())
    mapper2d1.SetColorWindow(255)
    mapper2d1.SetColorLevel(127.5)
    actor2d1=vtk.vtkActor2D()
    actor2d1.SetMapper(mapper2d1)
    ren2dimg1.AddActor2D(actor2d1)
    ren2dimg1.SetViewport([2/3,0.5,1.0,1.0])

    mapper2d2=vtk.vtkImageMapper()
    mapper2d2.SetInputConnection(fliper2.GetOutputPort())
    mapper2d2.SetColorWindow(255)
    mapper2d2.SetColorLevel(127.5)
    actor2d2=vtk.vtkActor2D()
    actor2d2.SetMapper(mapper2d2)
    ren2dimg2.AddActor2D(actor2d2)
    ren2dimg2.SetViewport([2/3,0.0,1.0,0.5])

    iren.Initialize()
    renWin.Render()
    iren.Start()