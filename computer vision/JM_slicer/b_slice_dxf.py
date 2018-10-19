from textwrap import dedent
import b_slice_writer as writer
from dxfwrite import DXFEngine as dxf

RED = 1
BLUE = 5

class DxfWriter(writer.Writer):
    def open(self, filename):
        return dxf.drawing(filename)

    def close(self):
        self.f.save()

    def write_header(self):
        self.f.add_layer('LINES')
        self.f.add_layer('NUMBERS')

    def write_footer(self):
        pass

    def write_layer_paths(self, paths, number):
        #for path in paths:
        #    x_avg = sum(d[0] for d in path[1:]) / (len(path)-1) * PPMM
        #    y_avg = sum(d[1] for d in path[1:]) / (len(path)-1) * PPMM
        #    self.f.write('0 0 1 setrgbcolor\n')
        #    self.f.write('%f %f moveto ' % (x_avg, y_avg))
        #    self.f.write('(%s) dup stringwidth pop 2 div neg 0 rmoveto false charpath\n' % (number))
        #self.f.write('closepath\nstroke\nrestore\nsave\nnewpath\n')
    
        for path in paths:
            pline = dxf.polyline(points=path, layer='LINES', color=RED)
            self.f.add(pline)

