from math import ceil
from solid import circle, square, hull
from solid.utils import right, forward, union, rotate

from utils import write_scads

length = 200
height = 100

radius = 10
y_offset = 2.5 * radius
back_bend_degrees = 10
x_offset = 2 * radius
step = 3 * radius


def assembly():
    return flat()


def slit():
    return rotate(a=back_bend_degrees)(
        forward(y_offset)(
            union()(hull()(
                circle(r=radius) + forward(height)(circle(r=radius))))))


def flat():
    body = square(size=[length, height])
    holes = []
    num_cutouts = int(ceil(length / step))
    for i in xrange(num_cutouts + 1):
        holes.append(right((i + 1) * step)(slit()))
    body -= union()(holes)
    return body


if __name__ == '__main__':
    write_scads(assembly=assembly(), flat=flat(), filename=__file__)

# :autocmd BufWritePost * silent! !make lid_rack
