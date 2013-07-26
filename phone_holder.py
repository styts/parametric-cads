import os

from solid import circle, square, hull, linear_extrude
from solid.utils import *

SEGMENTS = 20

phone_thickness = 13.2
phone_width = 60.4

radius = phone_width / 4
screw_hole_radius = 3  # 3mm screws hold the layers together
screw_hole_shift = radius / 1.5
layer_length = phone_width - radius / 2

material_height = 6
layer_gap = 0.1

top_layers = 3


def phone_hole():
    hole = square([phone_width, phone_thickness])
    x_offset = (layer_length - phone_width) / 2
    return right(x_offset)(back(phone_thickness / 2)(hole))


def layer():
    # streched oval
    body = hull()(circle(radius) + right(layer_length)(circle(radius)))

    # used to hold the layers together
    screw_holes = [
        left(screw_hole_shift)(circle(screw_hole_radius)),
        right(screw_hole_shift + layer_length)(circle(screw_hole_radius))
    ]
    body = body - screw_holes

    # phone slides into this hole
    body = body - phone_hole()

    # 2D -> 3D
    body = linear_extrude(height=material_height)(body)
    return body


def assembly():
    layers = []
    for i in xrange(top_layers):
        layers.append(
            up(i * (material_height + layer_gap))(layer())
        )
    return union()(layers)

if __name__ == '__main__':
    out_dir = os.path.join(os.curdir, 'output')
    file_out = os.path.join(out_dir, '%s.scad' % __file__[:-3])
    a = assembly()
    print "SCAD file written to: %s" % file_out
    scad_render_to_file(a, file_out, file_header='$fn = %s;' % SEGMENTS)

# :autocmd BufWritePost * silent! !make
