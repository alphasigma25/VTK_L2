import math

import vtkmodules.vtkRenderingOpenGL2
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonCore import (
    vtkDoubleArray,
    vtkPoints, vtkLookupTable
)
from vtkmodules.vtkCommonDataModel import vtkStructuredGrid
from vtkmodules.vtkFiltersHybrid import vtkRenderLargeImage
from vtkmodules.vtkIOImage import vtkPNGWriter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkDataSetMapper, vtkWindowToImageFilter
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


def main(values):
    nx = len(values)
    ny = len(values[0])

    if nx != ny:
        return

    colors = vtkNamedColors()

    point_values = vtkDoubleArray()
    point_values.SetNumberOfComponents(1)
    point_values.SetNumberOfTuples(nx * ny)

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
            theta = math.radians(90 + d_angle*y)
            cart_x = -r * math.sin(phi) * math.cos(theta)
            cart_z = r * math.sin(phi) * math.sin(theta)
            cart_y = r * math.cos(phi)
            min_h = min(min_h, current)
            max_h = max(max_h, current)

            lac = True
            if 0 < x < nx - 1 and 0 < y < ny - 1:
                for i in range(x-1, x+2):
                    for j in range(y-1, y+2, 2):
                        if abs(values[i][j] - values[x][y]) != 0:
                            lac = False
            else:
                lac = False

            if lac:
                point_values.SetValue(y * nx + x, 0)
            else:
                point_values.SetValue(y*nx+x, current)

            points.InsertNextPoint(cart_x, cart_y, cart_z)

    struct_grid = vtkStructuredGrid()
    struct_grid.SetDimensions(nx, ny, 1)
    struct_grid.SetPoints(points)
    struct_grid.GetPointData().SetScalars(point_values)

    lut = vtkLookupTable()

    lut.SetBelowRangeColor(0.529, 0.478, 1.000, 1.0)
    lut.UseBelowRangeColorOn()
    lut.SetHueRange(0.33, 0)
    lut.SetValueRange(0.63, 1)
    lut.SetSaturationRange(0.48, 0)
    lut.Build()

    mapper = vtkDataSetMapper()
    mapper.SetInputData(struct_grid)
    mapper.SetLookupTable(lut)
    mapper.SetScalarRange(min_h, 2000)
    mapper.ScalarVisibilityOn()

    actor = vtkActor()
    actor.SetMapper(mapper)

    ren = vtkRenderer()
    ren.SetBackground(colors.GetColor3d("SlateGray"))

    ren.AddActor(actor)

    ren_win = vtkRenderWindow()
    ren_win.AddRenderer(ren)
    ren_win.SetSize(600, 600)

    # pour enregistrer en image png
    '''w2if = vtkWindowToImageFilter()
    w2if.SetInput(ren_win)
    ren_win.Render()
    w2if.Update()

    writer = vtkPNGWriter()
    writer.SetFileName("screenshot.png")
    writer.SetInputData(w2if.GetOutput())
    writer.Write()'''

    iren = vtkRenderWindowInteractor()
    iren.SetRenderWindow(ren_win)

    style = vtkInteractorStyleTrackballCamera()
    iren.SetInteractorStyle(style)

    iren.Initialize()
    iren.Start()


if __name__ == "__main__":

    file1 = open('altitudes.txt', 'r')
    Lines = file1.readlines()
    Lines = Lines[1:]
    Valeurs = []
    for line in Lines:
        # Supprimer l'espace a la fin
        line = line[:-2]
        Valeurs.append([float(el) for el in line.split(' ')])

    main(Valeurs)
