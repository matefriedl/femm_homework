
import femm
import matplotlib.pyplot as plt

class Params:
    Wd = 1.01
    Gd = 0.02
    Dd = 0.2
    Td = 0.01
    DT = 0.19
    DTL = 0.15
    WT = 0.24
    EpsilonR = 4.4

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Rectangle:
    def __init__(self, origin_x, origin_y, width, height):
        self.origin_x = origin_x
        self.origin_y = origin_y
        self.width = width
        self.height = height

        self.draw()

    def draw(self):
        femm.ei_drawrectangle(self.origin_x, self.origin_y, self.origin_x + self.width, self.origin_y + self.height)

    def get_midpoint(self):
        midpoint =  Point(self.origin_x + self.width/2, self.origin_y + self.height/2)
        return midpoint

    def assign_conductor(self, conductor):
        midpoint = self.get_midpoint()
        femm.ei_selectsegment(self.origin_x, midpoint.y)
        femm.ei_selectsegment(self.origin_x + self.width, midpoint.y)
        femm.ei_selectsegment(midpoint.x, self.origin_y)
        femm.ei_selectsegment(midpoint.x, self.origin_y + self.height)
        femm.ei_setsegmentprop('<None>', 0, 1, 0, 0, conductor)
        femm.ei_clearselected()

    def assign_material(self, material):
        midpoint = self.get_midpoint()
        femm.ei_addblocklabel(midpoint.x, midpoint.y)
        femm.ei_selectlabel(midpoint.x, midpoint.y)
        femm.ei_setblockprop(material, 1, 0, 0)
        femm.ei_clearselected()


# The package must be initialized with the openfemm command.
femm.openfemm()

# We need to create a new Electrostatic (ei) document to work on.
femm.newdocument(1)

# Define the problem type. Units of mm; Axisymmetric; 
# Precision of 10^(-8) for the linear solver; a placeholder of 0 for 
# the depth dimension, and an angle constraint of 30 degrees
femm.ei_probdef('millimeters', 'planar', 1.e-8, 0, 30)

# Define materials
femm.ei_addmaterial('Dielectric', Params.EpsilonR, Params.EpsilonR, 0) # todo not sure
femm.ei_addmaterial('Conductor', 1, 1, 0) # todo even less sure
femm.ei_addmaterial('GND', 1, 1, 0) # todo even less sure
femm.ei_addmaterial('Air', 1, 1, 0)

# Define conductors
femm.ei_addconductorprop('GND', 0, 0, 1)
femm.ei_addconductorprop('Positive', 1, 0, 1)

# Draw a rectangle for the copper GND
gnd = Rectangle(0, 0, Params.Wd, Params.Gd)
gnd.assign_conductor('GND')
gnd.assign_material('GND')
# Draw a rectangle for the dielectric;
dielectric = Rectangle(0, Params.Gd, Params.Wd, Params.Dd)
dielectric.assign_material('Dielectric')
# Draw a rectangle for the smol copper conductor;
left_conductor = Rectangle(Params.DT, Params.Gd + Params.Dd, Params.WT, Params.Td)
left_conductor.assign_conductor('Positive')
left_conductor.assign_material('Conductor')
# Draw a rectangle for the other smol copper conductor;
right_conductor = Rectangle(Params.DT + Params.WT + Params.DTL, Params.Gd + Params.Dd, Params.WT, Params.Td)
right_conductor.assign_conductor('Positive')
right_conductor.assign_material('Conductor')


# Now, the finished input geometry can be displayed.
femm.ei_zoomnatural()

# We have to give the geometry a name before we can analyze it.
femm.ei_saveas('feladat1.fee')



# When the analysis is completed, FEMM can be shut down.
femm.closefemm()


