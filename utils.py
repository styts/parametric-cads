import os
from solid.utils import scad_render_to_file

SEGMENTS = 50  # increase for more smoothness


def write_scads(assembly, flat, filename):
    out_dir = os.path.join(os.curdir, 'output')
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    file_out = os.path.join(out_dir, '%s_3d.scad' % filename[:-3])
    print "3D SCAD file written to: %s" % file_out
    scad_render_to_file(assembly, file_out, file_header='$fn = %s;' % SEGMENTS)

    file_out = os.path.join(out_dir, '%s_2d.scad' % filename[:-3])
    print "LaserCut SCAD file written to: %s" % file_out
    scad_render_to_file(flat, file_out, file_header='$fn = %s;' % SEGMENTS)
