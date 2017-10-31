import vtk
import numpy as np
from vtk.util.vtkImageImportFromArray import vtkImageImportFromArray  
from calibration_biplane import *
from epipolar_projection import *
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

def epigeometry_points(pts, point, Data1, Data2):
    [gradient3d, point3d] = global_line_from_image_point(point, Data1)
    [epi_point1, epi_point2] = line_projection(gradient3d, point3d, Data2)

    img1_position=pt3d_from_pt2d([256.0,256.0],Data1)
    img2_position=pt3d_from_pt2d([256.0,256.0],Data2)
    source1_position=point3d
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


def render(Data1, Data2, point):

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

    [img1_position, img2_position, epi_point1, epi_point2] = epigeometry_points(pts, point, Data1, Data2)    

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

    img1=Data1.img.copy()
    img2=Data2.img.copy()

    cv2.circle(img1,(point[0],point[1]),10,(255,0,0),-1)
    cv2.line(img2,(int(epi_point1[0]), int(epi_point1[1])),(int(epi_point2[0]), int(epi_point2[1])),(255,0,0),5)
    cv2.putText(img1,str(int(np.rad2deg(Data1.PA)))+', '+str(int(np.rad2deg(Data1.SA))),(10, 100),1,4,(255,255,255),2,cv2.LINE_AA)
    cv2.putText(img2,str(int(np.rad2deg(Data2.PA)))+', '+str(int(np.rad2deg(Data2.SA))),(10, 100),1,4,(255,255,255),2,cv2.LINE_AA)
    
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

    planeA_actor = create_3dquad_imageactor(img1)
    planeA_actor.SetPosition(img1_position)
    planeA_actor.SetScale(Data1.PS[0],Data1.PS[1],1)
    planeA_actor.RotateY(np.rad2deg(Data1.PA))
    planeA_actor.RotateX(-np.rad2deg(Data1.SA))
    # planeA_actor.SetUserTransform(transform1)

    planeB_actor = create_3dquad_imageactor(img2)
    planeB_actor.SetPosition(img2_position)
    planeB_actor.SetScale(Data2.PS[0],Data2.PS[1],1)
    planeB_actor.RotateY(np.rad2deg(Data2.PA))
    planeB_actor.RotateZ(-np.rad2deg(Data2.SA))
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
    ren.AddActor(planeA_actor)
    ren.AddActor(planeB_actor)
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