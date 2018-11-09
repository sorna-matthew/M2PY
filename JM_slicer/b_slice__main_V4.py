import os.path
import logging
import math

logging.basicConfig()
logger = logging.getLogger(__name__)

from b_slice_stl import parse
import b_slice_svg as svg
import b_slice_ps as ps

X = 0
Y = 1
Z = 2


def find_line_plane_intersection(a, b, z):
    """ Find where a line between two points intersects a given
    axis-aligned plane
    """
    dx = a[X] - b[X]
    dy = a[Y] - b[Y]
    dz = a[Z] - b[Z]
    z_z0 = z - b[Z]

    xi = z_z0 * (dx / dz) + b[X]
    yi = z_z0 * (dy / dz) + b[Y]
    return (xi, yi)


def tri_above_below(tri, z):
    above = []
    below = []
    for point in tri:
        if point[Z] <= z:
            below.append(point)
        elif point[Z] > z:
            above.append(point)
    return above, below


def slice_shape_at(facets, z):
    lines = []
    for maxz, minz, tri in facets:
        if minz > z:
            continue

        above, below = tri_above_below(tri, z)
        if not above or not below:
            continue

        line = []
        for a in above:
            for b in below:
                line.append(find_line_plane_intersection(a, b, z))
        if LineMap.key(line[0]) != LineMap.key(line[1]):
            lines.append(line)
    return lines


class LineMap(object):
    def __init__(self, lines):
        map = {}
        for line in lines:
            for point in line:
                key = self.key(point)
                line_set = map.setdefault(key, [])
                line_set.append(line)
        self._map = map

    @staticmethod
    def key(point):
        return '{0:.10},{1:.10}'.format(*point)

    def has_lines(self):
        if self._map:
            return True
        else:
            return False

    def _pop_other_line(self, key, line):
        for point in line:
            if self.key(point) == key:
                continue
            other_point = point
            break

        key = self.key(other_point)
        lines = self._map[key]
        lines.remove(line)
        if len(lines) == 0:
            del self._map[key]

        return other_point

    def take_line(self):
        """ Take an arbitrary line out of the internal map
        """
        for key, lines in self._map.iteritems():
            line = lines.pop()
            if len(lines) == 0:
                del self._map[key]

            self._pop_other_line(key, line)
            return line

    def next_point(self, point):
        """ Return the next endpoint of an unused line which starts at
        the given point.

        Also removes the used line from the internal map.
        """
        key = self.key(point)
        lines = self._map.get(key, None)
        if lines is None:
            return None

        line = lines.pop()
        if len(lines) == 0:
            del self._map[key]

        other_point = self._pop_other_line(key, line)

        return other_point


def path_lines(lines):
    """ Convert a list of lines into paths
    """
    unused = LineMap(lines)

    paths = []
    while unused.has_lines():
        path = unused.take_line()

        point = unused.next_point(path[-1])
        while point:
            path.append(point)
            point = unused.next_point(point)
        paths.append(path)
    return paths


def bounding_cube(facets):
    minx, maxx = 99999, -99999
    miny, maxy = 99999, -99999
    minz, maxz = 99999, -99999
    for facet in facets:
        for point in facet:
            minx, maxx = min(minx, point[X]), max(maxx, point[X])
            miny, maxy = min(miny, point[Y]), max(maxy, point[Y])
            minz, maxz = min(minz, point[Z]), max(maxz, point[Z])
    return minx, maxx, miny, maxy, minz, maxz


def scale_to_fit(facets, width, height, scale):
    """ Scale the input facets to fit within the desired width and height.

    Returns the transformed facets.

    Since the end-product can be rotated easily, the width and height
    may be swapped during comparison, depending on whether the model
    better fits into a landscape or portrait layout.

    Also transforms all coordinates to greater than zero.
    """
    minx, maxx, miny, maxy, minz, maxz = bounding_cube(facets)
    xsize, ysize = maxx - minx, maxy - miny

    # If width/height relative proportions don't match, swap width and
    # height settings
    if ((width > height and xsize < ysize) or
        (height > width and xsize > ysize)):
            width, height = height, width

    if scale:
        width, height = xsize * scale, ysize * scale
    else:
        # check the different scales, bigger first
        for scale in sorted((width / xsize, height / ysize), reverse=True):
            if (scale * xsize <= width) and (scale * ysize <= height):
                break

    logger.info('Scaling by %f from %f, %f to %f, %f', scale, xsize, ysize, xsize*scale, ysize*scale)
    scaled_facets = []
    for facet in facets:
        scaled_facets.append([((x - minx) * scale, (y - miny) * scale,
                               (z - minz) * scale)
                              for x, y, z in facet])
        logger.debug('Scaled %r to %r', facet, scaled_facets[-1])
    return width, height, 0, (maxz - minz) * scale, scaled_facets


def z_sort_facets(facets):
    """ Sort facets by maximum Z, and build up a list containing
    tuples of max Z and facets """
    maxz_facets = [(max((f[0][Z], f[1][Z], f[2][Z])), min((f[0][Z], f[1][Z], f[2][Z])), f) for f in facets]
    return sorted(maxz_facets)


def command_line(file, subdir_models, subdir_output, thickness, width, height, scale, svg2, dxf, verbose, quiet):
    dir_file = os.path.dirname(os.path.realpath(__file__)) + "\\" + subdir_models +"\\" + file
    
    if verbose:
        logger.setLevel(logging.DEBUG)
    elif quiet:
        logger.setLevel(0)
    else:
        logger.setLevel(logging.INFO)

    facets = parse(open(dir_file, 'rb'))
    
    logger.info('Read %d facets from %s' % (len(facets), file))
    if scale:
        width, height, minz, maxz, facets = scale_to_fit(facets, 0, 0,
                                                         scale)
    else:
        width, height, minz, maxz, facets = scale_to_fit(facets, width,
                                                         height, scale)
    maxz_facets = z_sort_facets(facets)

    if svg2:
        ext = '.svg'
        writer_class = svg.SvgWriter
    elif dxf:
        import b_slice_dxf as dxf
        ext = '.dxf'
        writer_class = dxf.DxfWriter
    else:
        ext = '.ps'
        writer_class = ps.PsWriter

    out_filename = os.path.splitext(os.path.dirname(os.path.realpath(__file__)) + "\\" + subdir_output +"\\" + os.path.basename(file))[0] + ext
    layers = math.ceil(maxz - minz / thickness)

    writer = writer_class(out_filename, width, height, layers)
    z = minz
    
    layer = 1
    paths_all = []
    while z <= maxz:
        i = 0
        while maxz_facets[i][0] < z:
            i += 1
        maxz_facets = maxz_facets[i:]

        logger.debug('Slicing layer %d', layer)
        lines = slice_shape_at(maxz_facets, z)
        paths = path_lines(lines)
        writer.write_layer_paths(paths, layer)
        paths_all.append(paths)
        z += thickness
        layer += 1
    logger.info('Wrote %d layer(s) to %s' % (layer - 2, out_filename))
    writer.finish()
#    print paths_all
    
    del paths_all[0]
    
    return paths_all

if __name__ == '__main__':
    command_line(file, thickness, width, height, scale, svg2, dxf, verbose, quiet)