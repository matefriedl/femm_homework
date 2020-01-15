import femm

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