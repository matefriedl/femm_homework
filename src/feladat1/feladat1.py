
import femm
from myfemm.geo import Rectangle, ProblemType

Rectangle.problemType = ProblemType.ElectroStatic

class Params:
    Wd = 1.01
    Gd = 0.02
    Dd = 0.2
    Td = 0.01
    DT = 0.19
    DTL = 0.15
    WT = 0.24
    EpsilonR = 4.4


# The package must be initialized with the openfemm command.
femm.openfemm()

# We need to create a new Electrostatic (ei) document to work on.
femm.newdocument(ProblemType.ElectroStatic.value)

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

femm.ei_analyze()
femm.ei_loadsolution()

voltage, stored_charge = femm.eo_getconductorproperties('Positive')
capacitance_calcd_from_charge = stored_charge / voltage
print(f'Capacitance calculated from charge: {capacitance_calcd_from_charge * 10**12} pF')

femm.eo_selectblock(dielectric.get_midpoint().x, dielectric.get_midpoint().y)
stored_energy = femm.eo_blockintegral(0)[0]
capacitance_calcd_from_energy = 2 * stored_energy / (voltage*voltage)
print(f'Capacitance calculated from energy: {capacitance_calcd_from_energy * 10**12} pF')

# When the analysis is completed, FEMM can be shut down.
femm.closefemm()


