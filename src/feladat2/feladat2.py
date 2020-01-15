
import femm
from myfemm.geo import Rectangle, Point, ProblemType

class Params:
    D1 = 13.2
    D2 = 11
    D3 = 5.7
    D4 = 1.5
    D5 = 2
    D6 = 2.2
    D7 = 2
    D8 = 3.75
    D9 = 3.6
    D10 = 2
    Depth = 4
    Turns = 210
    core_gap = [0.1, 0.5, 1, 2]
    ExcitationCurrent = 3
    CoreMaterial = "M-15 Steel"


femm.openfemm()
femm.newdocument(ProblemType.MagnetoStatic.value)
Rectangle.problemType = ProblemType.MagnetoStatic
femm.mi_probdef(0, 'centimeters', 'planar', 1.e-8, Params.Depth, 30)

femm.mi_getmaterial(Params.CoreMaterial)

# define metal core 
core_parts = []

side_part_origins = [Point(0,0), Point(Params.D1-Params.D5, 0)]
for origin in side_part_origins:
    rect = Rectangle(origin.x, origin.y, Params.D5, Params.D2-Params.D6)
    core_parts.append(rect)
    rect.assign_material(Params.CoreMaterial, 0, 0)

middle_part = Rectangle(Params.D9 + Params.D5, 0, Params.D10, Params.D2-Params.D6)
core_parts.append(middle_part)

top_part = Rectangle(0, Params.D2 - Params.D6, Params.D1, Params.D6)
core_parts.append(top_part)

bottom_part = Rectangle(0, 0 - Params.core_gap[0] - Params.D7, Params.D1, Params.D7)
core_parts.append(bottom_part)



for core in core_parts:
    core.assign_material(Params.CoreMaterial, 0, 0)

# Now, the finished input geometry can be displayed.
femm.mi_zoomnatural()

# We have to give the geometry a name before we can analyze it.
femm.mi_saveas('feladat2.fem')

femm.closefemm()
