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

    def selectsegment(self, x, y):
        return femm.callfemm(f'{self.prefix}selectsegment(' + femm.numc(x) + femm.num(y) + ')')

    def draw(self):
        femm.ei_drawrectangle(self.origin_x, self.origin_y, self.origin_x + self.width, self.origin_y + self.height)

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