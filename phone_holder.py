from solid import circle, square, hull, linear_extrude, color
from solid.utils import left, right, forward, back, up, union

from utils import write_scads

# rendering parameters
layer_z_gap = 0.1  # > 0 to visualize layer breaks
layer_y_gap = 11  # spacing for flat forward movement

# customizable model parameters
phone_thickness = 13.2
phone_width = 60.4

# constraints
radius = phone_width / 7  # curvature left/right
screw_hole_radius = 1.5  # 3mm screws hold the layers together
screw_hole_shift = radius / 2

# what height layers to laser-cut
material_height = 6


class Layer(object):
    color = "yellow"

    def screw_holes(self):
        return [
            left(screw_hole_shift)(circle(screw_hole_radius)),
            right(screw_hole_shift + phone_width)(circle(screw_hole_radius))
        ]

    def __init__(self):
        # stretched oval
        body = hull()(circle(radius) + right(phone_width)(circle(radius)))

        # used to hold the layers together
        body = body - self.screw_holes()

        # set self
        self.body = body

        # proper X-axis alignment
        self.body = right(radius)(body)

        # cut possible hole
        if self.hole:
            self.body -= self.hole.make_hole()


class Hole(object):
    def make_hole(self):
        body = square([self.width, self.height])
        layer_width = (phone_width + 2 * radius)
        moved_right = right(layer_width / 2 - self.width / 2)(body)
        moved_down = back(self.height / 2 + self.y_adjust)(moved_right)
        return moved_down

    def __init__(self, width, height, y_adjust=0):
        self.width = width
        self.height = height
        self.y_adjust = y_adjust


class TopLayer(Layer):
    hole = Hole(phone_width, phone_thickness)


class MidLayer(Layer):
    hole = Hole(10.8, 7.2)
    color = "blue"


class BottomLayer(Layer):
    hole = Hole(3.5, radius + 5, y_adjust=-3)
    color = "green"


ls = [
    BottomLayer,
    MidLayer,
    MidLayer,
    MidLayer,
    MidLayer,
    MidLayer,
    TopLayer,
    TopLayer,
    TopLayer,
    TopLayer
]


def assembly():
    print "adapter needs height 32mm and we have %smm" % (5 * material_height)
    print "phone needs height 32mm and we have %smm" % (5 * material_height)
    print "total height %smm" % (len(ls) * material_height)
    layers = []
    for i, l in enumerate(ls):
        l_inst = l()
        layer = linear_extrude(height=material_height)(l_inst.body)
        layer = up(i * (material_height + layer_z_gap))(layer)
        layer = color(l_inst.color)(layer)
        layers.append(layer)

    return union()(layers)


def flat():
    def offset(i, break_after=5):
        x = 0 if i < break_after else phone_width + layer_y_gap + radius
        y = i * (radius + layer_y_gap)
        y = y - break_after * (radius + layer_y_gap) if x > 0 else y
        return x, y

    layers = []
    for i, l in enumerate(ls):
        x, y = offset(i)
        l_inst = l()
        layer = l_inst.body
        layer = color(l_inst.color)(layer)
        layers.append(right(x)(forward(y)(layer)))

    return union()(layers)


if __name__ == '__main__':
    write_scads(assembly=assembly(), flat=flat(), filename=__file__)

# :autocmd BufWritePost * silent! !make
