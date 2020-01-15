
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
    coil_gap = 0.05
    air_margin = 1
    ExcitationCurrent = 3
    CoreMaterial = "M-15 Steel"
    CoilMaterial = "Copper"

Params.core_gap.sort()

femm.openfemm()
femm.newdocument(ProblemType.MagnetoStatic.value)
Rectangle.problemType = ProblemType.MagnetoStatic
femm.mi_probdef(0, 'centimeters', 'planar', 1.e-8, Params.Depth, 30)

femm.mi_getmaterial(Params.CoreMaterial)
femm.mi_getmaterial(Params.CoilMaterial)
femm.mi_getmaterial('Air')

femm.mi_addcircprop('Circuit', Params.ExcitationCurrent, 1) # 0 = paralel, 1 = series

# name, A0, A1, A2, Phi, Mu, Sig, c0, c1, BdryFormat, ia, oa
femm.mi_addboundprop('Boundary', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

# define air around everything

air_width = 2 * Params.D4 + Params.D1 + Params.coil_gap * 2 + 2 * Params.air_margin
air_height = 2 * Params.air_margin + Params.D7 + Params.core_gap[-1] + Params.D2
air_rectangle = Rectangle(0 - Params.D4 - Params.coil_gap - Params.air_margin, 
                          0 - Params.core_gap[-1] - Params.D7 - Params.air_margin,
                          air_width,
                          air_height)
air_rectangle.assign_material('Air', 0, 0, Point(Params.D1/2, 0 - Params.core_gap[-1] - Params.D7 - Params.air_margin/2))
air_rectangle.assign_boundary('Boundary')


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

# define coil parts
coil_origin_y = Params.D2 - Params.D8 - Params.D3
coil_origins = [
    Point(0 - Params.D4 - Params.coil_gap, coil_origin_y),
    Point(Params.D5 + Params.coil_gap, coil_origin_y),
    Point(Params.D1 - Params.coil_gap - Params.D4 - Params.D5, coil_origin_y),
    Point(Params.D1 + Params.coil_gap, coil_origin_y),
    ]
for coil_origin in coil_origins:
    coil = Rectangle(coil_origin.x, coil_origin.y, Params.D4, Params.D3)
    coil.assign_material(Params.CoilMaterial, Params.Turns, 'Circuit')

# Now, the finished input geometry can be displayed.
femm.mi_zoomnatural()

# We have to give the geometry a name before we can analyze it.
femm.mi_saveas('feladat2.fem')

move_vectors = []
for previous, current in zip(Params.core_gap, Params.core_gap[1:]):
    move_vectors.append(Point(0, previous - current))

forces = {}
for core_gap, move_vector in zip(Params.core_gap, move_vectors):
    femm.mi_analyze()
    femm.mi_loadsolution()
    bottom_part.select_block()
    forces[core_gap] = femm.mo_blockintegral(19)
    bottom_part.move(move_vector.x, move_vector.y)
    print(f'In case of {core_gap}, force is {forces[core_gap]}')

femm.closefemm()
