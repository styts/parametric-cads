import os

from solid import circle, hull
from solid.utils import scad_render_to_file, right

SEGMENTS = 20

radius = 20
length = 3 * radius


def layer():
    body = hull()(circle(r=radius) + right(length)(circle(r=radius)))
    hole_radius = radius / 4
    holes = [
        circle(hole_radius),
        right(length)(circle(hole_radius))
    ]
    return body - holes


def assembly():
    return layer()

if __name__ == '__main__':
    out_dir = os.path.join(os.curdir, 'output')
    file_out = os.path.join(out_dir, '%s.scad' % __file__[:-3])
    a = assembly()
    print "SCAD file written to: %s" % file_out
    scad_render_to_file(a, file_out, file_header='$fn = %s;' % SEGMENTS)

# :autocmd BufWritePost * silent! !make
