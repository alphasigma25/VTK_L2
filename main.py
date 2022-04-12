import math

# noinspection PyUnresolvedReferences
import vtkmodules.vtkInteractionStyle
# noinspection PyUnresolvedReferences
import vtkmodules.vtkRenderingOpenGL2
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonCore import (
    vtkDoubleArray,
    vtkMath,
    vtkPoints
)
from vtkmodules.vtkCommonDataModel import vtkStructuredGrid
from vtkmodules.vtkFiltersCore import vtkHedgeHog
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
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
def main():
    colors = vtkNamedColors()

    r_min = 0.5
    r_max = 1.0
    dims = [30,20,10]

    # Create the structured grid.
    sgrid = vtkStructuredGrid()
    sgrid.SetDimensions(dims)

    # We also create the points and vectors. The points
    # form a hemi-cylinder of data.
    vectors = vtkDoubleArray()
    vectors.SetNumberOfComponents(3)
    vectors.SetNumberOfTuples(dims[0] * dims[1] * dims[2])
    points = vtkPoints()
    points.Allocate(dims[0] * dims[1] * dims[2])

    delta_z = 2.0 / (dims[2] - 1)
    delta_rad = (r_max - r_min) / (dims[1] - 1)
    x = [0.0] * 3
    v = [0.0] * 3
    for k in range(0, dims[2]):
        x[2] = -1.0 + k * delta_z
        k_offset = k * dims[0] * dims[1]
        for j in range(0, dims[1]):
            radius = r_min + j * delta_rad
            j_offset = j * dims[0]
            for i in range(0, dims[0]):
                theta = i * vtkMath.RadiansFromDegrees(15.0)
                x[0] = radius * math.cos(theta)
                x[1] = radius * math.sin(theta)
                v[0] = -x[1]
                v[1] = x[0]
                offset = i + j_offset + k_offset
                points.InsertPoint(offset, x)
                vectors.InsertTuple(offset, v)
    sgrid.SetPoints(points)
    sgrid.GetPointData().SetVectors(vectors)

    # We create a simple pipeline to display the data.
    hedgehog = vtkHedgeHog()
    hedgehog.SetInputData(sgrid)
    hedgehog.SetScaleFactor(0.1)

    sgrid_mapper = vtkPolyDataMapper()
    sgrid_mapper.SetInputConnection(hedgehog.GetOutputPort())

    sgrid_mapper = vtkDataSetMapper()
    sgrid_mapper.SetInputData(sgrid)

    sgrid_actor = vtkActor()
    sgrid_actor.SetMapper(sgrid_mapper)
    sgrid_actor.GetProperty().SetColor(colors.GetColor3d('Gold'))

    # Create the usual rendering stuff
    renderer = vtkRenderer()
    ren_win = vtkRenderWindow()
    ren_win.AddRenderer(renderer)
    ren_win.SetWindowName('SGrid')

    iren = vtkRenderWindowInteractor()
    iren.SetRenderWindow(ren_win)

    renderer.AddActor(sgrid_actor)
    renderer.SetBackground(colors.GetColor3d('MidnightBlue'))
    renderer.ResetCamera()
    renderer.GetActiveCamera().Elevation(60.0)
    renderer.GetActiveCamera().Azimuth(30.0)
    renderer.GetActiveCamera().Dolly(1.0)
    ren_win.SetSize(640, 480)

    # Interact with the data.
    ren_win.Render()
    iren.Start()


def main2():
    ren = vtkRenderer()
    ren.SetBackground(1, 0.9, 0.9)

    ren_win = vtkRenderWindow()
    ren_win.AddRenderer(ren)
    ren_win.SetSize(300, 300)

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
        line = line[:-2]
        Valeurs.append(line.split(' '))
    main()