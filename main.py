import math

# noinspection PyUnresolvedReferences
import vtkmodules.vtkInteractionStyle
# noinspection PyUnresolvedReferences
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


def main(values):
    nx = len(values)
    ny = len(values[0])

    if nx != ny:
        return

    colors = vtkNamedColors()

    point_values = vtkDoubleArray()
    point_values.SetNumberOfComponents(1)
    point_values.SetNumberOfTuples(nx * ny)
    for i in range(nx*ny):
        point_values.SetValue(i,2)

    min_h = math.inf
    max_h = 0.0
    angle = 2.5
    r_terre = 6352800
    d_angle = angle / (len(values)-1)
    points = vtkPoints()
    for y in range(ny):
        for x in range(nx):
            current = values[x][y]
            r = r_terre + current
            phi = math.radians(45 + d_angle*x)
            theta = math.radians(5 + d_angle*y)
            cart_x = r * math.sin(phi) * math.cos(theta)
            cart_y = r * math.sin(phi) * math.sin(theta)
            cart_z = r * math.cos(phi)
            #min_h = min(min_h, current)
            #max_h = max(max_h, current)
            #point_values.SetValue(y*nx+x,current)
            points.InsertNextPoint(cart_x, cart_y, cart_z)

    print('ok')
    struct_grid = vtkStructuredGrid()
    struct_grid.SetDimensions(nx, ny, 1)
    struct_grid.SetPoints(points)
    struct_grid.GetPointData().SetScalars(point_values)
    print('ok2')

    lut = vtkLookupTable()
    lut.SetNumberOfTableValues(6)
    lut.SetTableValue(0, colors.GetColor4d("Blue"))
    lut.SetTableValue(1, colors.GetColor4d("Green"))
    lut.SetTableValue(2, colors.GetColor4d("Yellow"))
    lut.SetTableValue(3, colors.GetColor4d("Purple"))
    lut.SetTableValue(4, colors.GetColor4d("Black"))
    lut.SetTableValue(5, colors.GetColor4d("White"))
    lut.Build()
    print('ok3')

    mapper = vtkDataSetMapper()
    mapper.SetInputData(struct_grid)
    mapper.SetLookupTable(lut)
    mapper.SetScalarRange(3, 9)# min_h, max_h)
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
