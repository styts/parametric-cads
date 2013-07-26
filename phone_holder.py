import os

from solid import cylinder
from solid.utils import scad_render_to_file

SEGMENTS = 43


def piece():
    cyl = cylinder(r=5, h=15, center=True) - cylinder(r=4, h=16, center=True)
    return cyl

if __name__ == '__main__':
    out_dir = os.path.join(os.curdir, 'output')
    file_out = os.path.join(out_dir, '%s.scad' % __file__[:-3])
    a = piece()
    print "SCAD file written to: %s" % file_out
    scad_render_to_file(a, file_out, file_header='$fn = %s;' % SEGMENTS)

# :autocmd BufWritePost * silent! !make
