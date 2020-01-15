import femm
from enum import Enum

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class ProblemType(Enum):
    MagnetoStatic = 0
    ElectroStatic = 1

Prefixes = {
    ProblemType.MagnetoStatic : 'mi_',
    ProblemType.ElectroStatic : 'ei_'
}


class Rectangle:
    problemType: ProblemType = None
    prefix: str = None

    def __init__(self, origin_x, origin_y, width, height):
        assert self.problemType, f"No problem type specified"
        self.origin_x = origin_x
        self.origin_y = origin_y
        self.width = width
        self.height = height

        self.prefix = Prefixes[self.problemType]

        self.draw()

    def callCommandWithPrefix(self, command):
        return femm.callfemm(f'{self.prefix}{command}')

    def selectsegment(self, x, y):
        return self.callCommandWithPrefix(f'selectsegment({x},{y})')

    def addnode(self, x, y):
        return self.callCommandWithPrefix(f'addnode({x},{y})')

    def addsegment(self, start_x, start_y, end_x, end_y):
        return self.callCommandWithPrefix(f'addsegment({start_x},{start_y},{end_x}, {end_y})')

    def drawline(self, start_x, start_y, end_x, end_y):
        self.addnode(start_x, start_y)
        self.addnode(end_x, end_y)
        self.addsegment(start_x, start_y, end_x, end_y)

    def draw(self):
        x2 = self.origin_x + self.width
        y2 = self.origin_y + self.height
        self.drawline(self.origin_x, self.origin_y, x2, self.origin_y)
        self.drawline(x2, self.origin_y, x2, y2)
        self.drawline(x2, y2, self.origin_x, y2)
        self.drawline(self.origin_x, y2, self.origin_x, self.origin_y)

    def get_midpoint(self):
        midpoint =  Point(self.origin_x + self.width/2, self.origin_y + self.height/2)
        return midpoint

    def assign_conductor(self, conductor):
        assert self.problemType is ProblemType.ElectroStatic

        midpoint = self.get_midpoint()
        self.selectsegment(self.origin_x, midpoint.y)
        self.selectsegment(self.origin_x + self.width, midpoint.y)
        self.selectsegment(midpoint.x, self.origin_y)
        self.selectsegment(midpoint.x, self.origin_y + self.height)
        femm.ei_setsegmentprop('<None>', 0, 1, 0, 0, conductor)
        femm.ei_clearselected()

    def assign_material(self, material):
        midpoint = self.get_midpoint()
        femm.ei_addblocklabel(midpoint.x, midpoint.y)
        femm.ei_selectlabel(midpoint.x, midpoint.y)
        femm.ei_setblockprop(material, 1, 0, 0)
        femm.ei_clearselected()


if __name__ == "__main__":
    femm.openfemm()

    # We need to create a new Electrostatic (ei) document to work on.
    femm.newdocument(ProblemType.ElectroStatic.value)

    # Define the problem type. Units of mm; Axisymmetric; 
    # Precision of 10^(-8) for the linear solver; a placeholder of 0 for 
    # the depth dimension, and an angle constraint of 30 degrees
    femm.ei_probdef('centimeters', 'planar', 1.e-8, 0, 30)

    Rectangle.problemType = ProblemType.ElectroStatic
    rectangle = Rectangle(0, 0, 10, 10)
    rectangle.addnode(5, 5)
    femm.ei_zoomnatural()
    femm.closefemm()