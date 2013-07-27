import os

from solid import circle, square, hull, linear_extrude, color
from solid.utils import left, right, forward, back, up, union
from solid.utils import scad_render_to_file

# rendering parameters
SEGMENTS = 50  # increase for more smoothness
layer_z_gap = 0.1  # > 0 to visualize layer breaks
layer_y_gap = 20  # spacing for flat forward movement

# customizable model parameters
phone_thickness = 13.2
phone_width = 60.4

# constraints
radius = phone_width / 4  # curvature left/right
screw_hole_radius = 3  # 3mm screws hold the layers together
screw_hole_shift = radius / 1.5

# what height layers to laser-cut
material_height = 6


class Layer(object):
    color = "yellow"

    def make_hole(self):
        try:
            getattr(self, 'hole')
        except:
            return

        ho = square([self.hole.x, self.hole.y])
        body = right(self.hole.x_offset)(back(self.hole.y_offset())(ho))
        return body

    def __init__(self):
        # stretched oval
        body = hull()(circle(radius) + right(phone_width)(circle(radius)))

        # used to hold the layers together
        screw_holes = [
            left(screw_hole_shift)(circle(screw_hole_radius)),
            right(screw_hole_shift + phone_width)(circle(screw_hole_radius))
        ]
        body = body - screw_holes

        # proper X-axis alignment
        body = right(radius)(body)

        # 2D -> 3D
        self.body = body

        # possible hole
        self.body -= self.make_hole()

    def get_body(self):
        return self.body


class Hole(object):
    def __init__(self, x_offset, x, y):
        self.x = x
        self.y = y
        self.x_offset = x_offset

    def y_offset(self):
        return 4


class CenteredHole(Hole):
    def y_offset(self):
        return self.y / 2


class TopLayer(Layer):
    hole = CenteredHole(phone_width / 4, phone_width, phone_thickness)


class MidLayer(Layer):
    hole = CenteredHole(phone_width / 2 + 10.8, 10.8, 7.2)
    color = "blue"


class BottomLayer(Layer):
    hole = Hole(phone_width / 2 + radius, 3, radius + 5)
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
        layer = linear_extrude(height=material_height)(l_inst.get_body())
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
        layer = l_inst.get_body()
        layer = color(l_inst.color)(layer)
        layers.append(right(x)(forward(y)(layer)))

    return union()(layers)


if __name__ == '__main__':
    out_dir = os.path.join(os.curdir, 'output')

    a_3d = assembly()
    a_lc = flat()

    file_out = os.path.join(out_dir, '%s_3d.scad' % __file__[:-3])
    print "3D SCAD file written to: %s" % file_out
    scad_render_to_file(a_3d, file_out, file_header='$fn = %s;' % SEGMENTS)

    file_out = os.path.join(out_dir, '%s_2d.scad' % __file__[:-3])
    print "LaserCut SCAD file written to: %s" % file_out
    scad_render_to_file(a_lc, file_out, file_header='$fn = %s;' % SEGMENTS)

# :autocmd BufWritePost * silent! !make
