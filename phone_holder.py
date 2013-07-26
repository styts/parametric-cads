import os

from solid import circle, square, hull, linear_extrude
from solid.utils import left, right, back, up, union, scad_render_to_file

# rendering parameters
SEGMENTS = 50  # increase for more smoothness
layer_gap = 0.0  # > 0 to visualize layer breaks

phone_thickness = 13.2
phone_width = 60.4

radius = phone_width / 4  # curvature left/right
screw_hole_radius = 3  # 3mm screws hold the layers together
screw_hole_shift = radius / 1.5

material_height = 6


class Layer(object):
    def make_hole(self):
        try:
            getattr(self, 'hole')
        except:
            return

        ho = square([self.hole.x, self.hole.y])
        body = right(self.hole.x_offset)(back(self.hole.y_offset())(ho))
        body = linear_extrude(height=material_height)(body)
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
        self.body = linear_extrude(height=material_height)(body)

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
        return 0


class CenteredHole(Hole):
    def y_offset(self):
        return self.y / 2


class TopLayer(Layer):
    hole = CenteredHole(phone_width / 4, phone_width, phone_thickness)


class MidLayer(Layer):
    hole = CenteredHole(phone_width / 2 + 10.8, 10.8, 7.2)


class BottomLayer(Layer):
    hole = Hole(phone_width / 2 + radius, 3, radius)


def assembly():
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
    print "adapter needs height 32mm and we have %smm" % (5 * material_height)
    print "phone needs height 32mm and we have %smm" % (5 * material_height)
    print "total height %smm" % (len(ls) * material_height)
    layers = []
    for i, l in enumerate(ls):
        l_inst = l()
        layers.append(
            up(i * (material_height + layer_gap))(l_inst.get_body())
        )

    return union()(layers)

if __name__ == '__main__':
    out_dir = os.path.join(os.curdir, 'output')
    file_out = os.path.join(out_dir, '%s.scad' % __file__[:-3])
    a = assembly()
    print "SCAD file written to: %s" % file_out
    scad_render_to_file(a, file_out, file_header='$fn = %s;' % SEGMENTS)

# :autocmd BufWritePost * silent! !make
