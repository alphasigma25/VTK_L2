import math

import vtkmodules.vtkRenderingOpenGL2
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonCore import (
    vtkDoubleArray,
    vtkPoints, vtkLookupTable
)
from vtkmodules.vtkCommonDataModel import vtkStructuredGrid
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkDataSetMapper
)
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer
)
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer
)

# https://kitware.github.io/vtk-examples/site/Cxx/StructuredGrid/StructuredGrid/

angle = 2.5
r_terre = 6352800

def find_coord(x, y, values, points, point_values, h_extr, islake=False):
    d_angle = angle / (len(values)-1)
    current = values[x][y]
    r = r_terre + current
    phi = math.radians(45 + d_angle*x)
    theta = math.radians(5 + d_angle*y)
    cart_x = r * math.sin(phi) * math.cos(theta)
    cart_y = r * math.sin(phi) * math.sin(theta)
    cart_z = r * math.cos(phi)
    points.InsertNextPoint(cart_x, cart_y, cart_z)
    h_min = min(h_extr[0], current)
    h_max = max(h_extr[1], current)
    if islake:
        point_values.SetValue(y*len(values)+x, 0)
    else:
        point_values.SetValue(y*len(values)+x, current)
    return (h_min, h_max)

def main(values):
    nx = len(values)
    ny = len(values[0])

    if nx != ny:
        return

    colors = vtkNamedColors()

    point_values = vtkDoubleArray()
    point_values.SetNumberOfComponents(1)
    point_values.SetNumberOfTuples(nx * ny)

    points = vtkPoints()
    islake = False
    min_h = math.inf
    max_h = 0.0

    min_h, max_h = find_coord(0,0,values, points, point_values, (min_h,max_h), islake)
    min_h, max_h = find_coord(0,ny-1,values, points, point_values, (min_h,max_h), islake)
    min_h, max_h = find_coord(nx-1,ny-1,values, points, point_values, (min_h,max_h), islake)
    min_h, max_h = find_coord(nx-1,0,values, points, point_values, (min_h,max_h), islake)

    for x in range(1,nx-1):
        min_h, max_h = find_coord(x,0,values, points, point_values, (min_h,max_h), islake)
        min_h, max_h = find_coord(x,ny-1,values, points, point_values, (min_h,max_h), islake)

    for y in range(1,ny-1):
        min_h, max_h = find_coord(0,y,values, points, point_values, (min_h,max_h), islake)
        min_h, max_h = find_coord(nx-1,y,values, points, point_values, (min_h,max_h), islake)

    for y in range(1, ny-1):
        for x in range(1, nx-1):
            err = 0
            for i in range(-1, 2):
                for j in range(-1, 2):
                    err = abs(values[i][j] - values[x][y])
            h_extr = find_coord(x, y, values, points, point_values, (min_h, max_h), False)
            min_h = h_extr[0]
            max_h = h_extr[1]
        #if y%30 == 0: print(y//30)

    print('ok')
    struct_grid = vtkStructuredGrid()
    struct_grid.SetDimensions(nx, ny, 1)
    struct_grid.SetPoints(points)
    struct_grid.GetPointData().SetScalars(point_values)
    print('ok2')

    lut = vtkLookupTable()
    lut.SetNumberOfTableValues(9)

    lut.SetBelowRangeColor(0.529, 0.478, 1.000, 1.0)
    #lut.SetBelowRangeColor(0.0, 0.0, 0.000, 1.0)
    lut.UseBelowRangeColorOn()
    lut.SetTableValue(0, 0.612, 0.757, 0.443, 1.0)
    lut.SetTableValue(1, 0.545, 0.741, 0.412, 1.0)
    lut.SetTableValue(2, 0.737, 0.812, 0.522, 1.0)
    lut.SetTableValue(3, 0.725, 0.800, 0.510, 1.0)
    lut.SetTableValue(4, 0.831, 0.831, 0.616, 1.0)
    lut.SetTableValue(5, 0.882, 0.835, 0.725, 1.0)
    lut.SetTableValue(6, 0.925, 0.859, 0.800, 1.0)
    lut.SetTableValue(7, 0.949, 0.882, 0.867, 1.0)
    lut.SetTableValue(8, 1.000, 1.000, 1.000, 1.0)
    lut.Build()
    print('ok3')

    print(min_h)
    mapper = vtkDataSetMapper()
    mapper.SetInputData(struct_grid)
    mapper.SetLookupTable(lut)
    mapper.SetScalarRange(min_h, max_h)
    mapper.ScalarVisibilityOn()

    print('ok4')
    actor = vtkActor()
    actor.SetMapper(mapper)

    print('ok5')

    ren = vtkRenderer()
    ren.SetBackground(colors.GetColor3d("SlateGray"))

    ren.AddActor(actor)

    ren_win = vtkRenderWindow()
    ren_win.AddRenderer(ren)
    ren_win.SetSize(300, 300)

    iren = vtkRenderWindowInteractor()
    iren.SetRenderWindow(ren_win)

    style = vtkInteractorStyleTrackballCamera()
    iren.SetInteractorStyle(style)

    print('ok6')
    iren.Initialize()
    print('ok7')
    iren.Start()
    print('ok8')


if __name__ == "__main__":
    # https://kitware.github.io/vtk-examples/site/Cxx/StructuredGrid/StructuredGrid/

    file1 = open('altitudes.txt', 'r')
    Lines = file1.readlines()
    Lines = Lines[1:]
    Valeurs = []
    for line in Lines:
        # Supprimer l'espace a la fin
        line = line[:-2]
        Valeurs.append([float(el) for el in line.split(' ')])

    main(Valeurs)
