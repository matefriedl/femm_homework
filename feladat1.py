
import femm
import matplotlib.pyplot as plt

class Params:
    Wd = 1.01
    Gd = 0.02
    Dd = 0.2
    Td = 0.01
    DT = 0.19
    DTL = 0.15
    WGND = 0
    WT = 0.24
    DDT = 0
    EpsilonR = 4.4

def draw_rectangle(origin_x, origin_y, width, height):
    femm.ei_drawrectangle(origin_x, origin_y, origin_x + width, origin_y + height)

# The package must be initialized with the openfemm command.
femm.openfemm()

# We need to create a new Electrostatic (ei) document to work on.
femm.newdocument(1)

# Define the problem type. Units of mm; Axisymmetric; 
# Precision of 10^(-8) for the linear solver; a placeholder of 0 for 
# the depth dimension, and an angle constraint of 30 degrees
femm.ei_probdef('millimeters', 'planar', 1.e-8, 0, 30)

# Draw a rectangle for the copper GND
draw_rectangle(0, 0, Params.Wd, Params.Gd)

# Draw a rectangle for the dielectric;
draw_rectangle(0, Params.Gd, Params.Wd, Params.Dd)
# Draw a rectangle for the smol copper conductor;
draw_rectangle(Params.DT, Params.Gd + Params.Dd, Params.WT, Params.Td)
# Draw a rectangle for the other smol copper conductor;
draw_rectangle(Params.DT + Params.WT + Params.DTL, Params.Gd + Params.Dd, Params.WT, Params.Td)


# Now, the finished input geometry can be displayed.
femm.ei_zoomnatural()

# We have to give the geometry a name before we can analyze it.
femm.ei_saveas('feladat1.fem')



# When the analysis is completed, FEMM can be shut down.
femm.closefemm()


