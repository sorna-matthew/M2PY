def readFacet(f):
    line = f.readline().strip()
    if line != 'outer loop':
        raise ValueError('Expected "outer loop", got "%s"' % line)

    facet = []
#    facetnormal = []
    line = f.readline().strip()
    while line != 'endloop':
        parts = line.split()
        if parts[0] != 'vertex':
            raise ValueError('Expected "vertex x y z", got "%s"' % line)
        facet.append(tuple([float(num) for num in parts[1:]]))

        line = f.readline().strip()
    line = f.readline().strip()
    if line != 'endfacet':
        raise ValueError('Expected "endfacet", got "%s"' % line)
#    return (facet, facetnormal)
    return facet

# for ASCII files
def parseText(f):
    line = f.readline().strip()
    parts = line.split()
    if parts[0] != 'solid':
        raise ValueError('Expected "solid ...", got "%s"' % line)
    name = ' '.join(parts[1:])

    facets = []
    line = f.readline().strip()
    while line.startswith('facet'):
        facets.append(readFacet(f))
        line = f.readline().strip()
    if line != ('endsolid %s' % name):
        # Check STL file -- add file name to the very last line!
        raise ValueError('Expected "endsolid %s", got "%s". Check .stl file.' % (name, line))
    return facets

# for BINARY files
def parseBin(f):
    import struct
    header = f.read(80)
    print 'HEADER:', header
    (count,) = struct.unpack('<I', f.read(4))
    print 'COUNT:', count
    facets = []
    for i in range(count):
        normal = struct.unpack('<fff', f.read(12))
        points = []
        for i in range(3):
            points.append(struct.unpack('<fff', f.read(12)))
        facets.append(points)
        attribute_byte_count = f.read(2)
    return facets

def parse(f):
    line = f.readline().strip()
    f.seek(0)
    if line.startswith('solid'):
        return parseText(f) #ASCII
    else:
        return parseBin(f)  # BIN

if __name__ == '__main__':
    import sys
    facets = parse(open(sys.argv[1], 'rb'))
    print facets
