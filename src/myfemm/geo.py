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
    next_index: int = 0

    def __init__(self, origin_x, origin_y, width, height):
        assert isinstance(self.problemType, ProblemType), f"No problem type specified"

        self.index = Rectangle.next_index
        Rectangle.next_index += 1
        self.origin_x = origin_x
        self.origin_y = origin_y
        self.width = width
        self.height = height

        self.prefix = Prefixes[self.problemType]

        self.draw()
        self.select_periphery()
        if self.problemType is ProblemType.ElectroStatic:
            femm.ei_setsegmentprop('<None>', 0, 1, 0, self.index, '<None>')
        elif self.problemType is ProblemType.MagnetoStatic:
            femm.mi_setsegmentprop('<None>', 0, 1, 0, self.index)
        else:
            assert False
        self.clearselected()

    def callCommandWithPrefix(self, command):
        return femm.callfemm(f'{self.prefix}{command}')

    def selectsegment(self, x, y):
        return self.callCommandWithPrefix(f'selectsegment({x},{y})')

    def addnode(self, x, y):
        return self.callCommandWithPrefix(f'addnode({x},{y})')

    def addsegment(self, start_x, start_y, end_x, end_y):
        return self.callCommandWithPrefix(f'addsegment({start_x},{start_y},{end_x}, {end_y})')

    def addblocklabel(self, x, y):
        return self.callCommandWithPrefix(f'addblocklabel({x},{y})')

    def selectlabel(self, x, y):
        return self.callCommandWithPrefix(f'selectlabel({x},{y})')

    def clearselected(self):
        return self.callCommandWithPrefix(f'clearselected()')

    def selectgroup(self, index):
        return self.callCommandWithPrefix(f'selectgroup({index})')

    def drawline(self, start_x, start_y, end_x, end_y):
        self.addnode(start_x, start_y)
        self.addnode(end_x, end_y)
        self.addsegment(start_x, start_y, end_x, end_y)

    def move(self, dx, dy):
        self.selectgroup(self.index)
        self.callCommandWithPrefix(f'movetranslate({dx},{dy})')
        self.origin_x += dx
        self.origin_y += dy
        self.clearselected()

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
        self.select_periphery()
        femm.ei_setsegmentprop('<None>', 0, 1, 0, 0, conductor)
        self.clearselected()

    # todo can be unified with function above
    def assign_boundary(self, boundary):
        assert self.problemType is ProblemType.MagnetoStatic
        self.clearselected()
        self.select_periphery()
        femm.mi_setsegmentprop('Boundary', 0, 1, 0, 0)
        self.clearselected()

    # always clearselected after calling
    def select_periphery(self):
        self.clearselected()
        midpoint = self.get_midpoint()
        self.selectsegment(self.origin_x, midpoint.y)
        self.selectsegment(self.origin_x + self.width, midpoint.y)
        self.selectsegment(midpoint.x, self.origin_y)
        self.selectsegment(midpoint.x, self.origin_y + self.height)

    def select_block(self):
        midpoint = self.get_midpoint()
        if self.problemType is ProblemType.ElectroStatic:
            femm.eo_selectblock(midpoint.x, midpoint.y)
        elif self.problemType is ProblemType.MagnetoStatic:
            femm.mo_selectblock(midpoint.x, midpoint.y)
        else:
            assert False

    def assign_material(self, material, turns = None, circuit = None, where: Point = None):
        if where is None:
            where = self.get_midpoint()
        self.addblocklabel(where.x, where.y)
        self.selectlabel(where.x, where.y)
        if self.problemType is ProblemType.ElectroStatic:
            femm.ei_setblockprop(material, 1, 0, self.index)
        elif self.problemType is ProblemType.MagnetoStatic:
            assert turns is not None
            assert circuit is not None
            # blockname, automesh, meshsize, incircuit, magdir, group, turns
            femm.mi_setblockprop(material, 1, 0, circuit, 0, self.index, turns)
        self.clearselected()


if __name__ == "__main__":
    femm.openfemm()

    # We need to create a new Electrostatic (ei) document to work on.
    femm.newdocument(ProblemType.ElectroStatic.value)
    femm.ei_addmaterial('Air', 1, 1, 0)

    # Define the problem type. Units of mm; Axisymmetric; 
    # Precision of 10^(-8) for the linear solver; a placeholder of 0 for 
    # the depth dimension, and an angle constraint of 30 degrees
    femm.ei_probdef('centimeters', 'planar', 1.e-8, 0, 30)

    Rectangle.problemType = ProblemType.ElectroStatic
    rectangle = Rectangle(0, 0, 10, 10)
    rectangle.assign_material('Air')
    femm.ei_zoomnatural()
    femm.closefemm()