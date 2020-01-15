
import femm
from myfemm.geo import Rectangle

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
    ExcitationCurrent = 3
    CoreMaterial = "M-15 Steel"


femm.openfemm()
femm.newdocument(0)
femm.mi_probdef(0, 'millimeters', 'axi', 1.e-8, 0, 30);










# Now, the finished input geometry can be displayed.
femm.mi_zoomnatural()

# We have to give the geometry a name before we can analyze it.
femm.mi_saveas('feladat2.fem')

femm.closefemm()
