from textwrap import dedent
import b_slice_writer as writer

# millimeters to points
PPMM = 360.0 / 127.0


class PsWriter(writer.Writer):
    def write_header(self):
        self.f.write(dedent("""\
          %!PS-Adobe-2.0
          %%Creator: stl_slicer 0.1
          %%Title: {name}
          %%Pages: {layers}
          %%PageOrder: Ascend
          %%BoundingBox: 0 0 {width} {height}
          %%EndComments
          %%BeginSetup
          <</PageSize [{width} {height}]>> setpagedevice
          0 {height} translate
          /mt /moveto load def
          /moveto {{ neg mt }} bind def
          /lt /lineto load def
          /lineto {{ neg lt }} bind def
          /Courier 12 selectfont
          1 0 0 setrgbcolor
          0.1 setlinewidth
          %%EndSetup
          """).format(name=self.f.name,
                      layers=self.layers,
                      width=self.width * PPMM,
                      height=self.height * PPMM))


    def write_footer(self):
        self.f.write('\n%%EOF\n')

    def write_layer_paths(self, paths, number):
        if not len(paths):
            return
        self.f.write(dedent("""\
          %%Page: page {}
          save
          newpath
          """).format(number))
    
        for path in paths:
            x_avg = sum(d[0] for d in path[1:]) / (len(path)-1) * PPMM
            y_avg = sum(d[1] for d in path[1:]) / (len(path)-1) * PPMM
            self.f.write('0 0 1 setrgbcolor\n')
            self.f.write('%f %f moveto ' % (x_avg, y_avg))
            self.f.write('(%s) dup stringwidth pop 2 div neg 0 rmoveto false charpath\n' % (number))
        self.f.write('closepath\nstroke\nrestore\nsave\nnewpath\n')
    
        for path in paths:
            self.f.write('%f %f moveto\n' % (path[0][0] * PPMM, path[0][1] * PPMM))
            for point in path[1:]:
                self.f.write('%f %f lineto ' % (point[0] * PPMM, point[1] * PPMM))
            self.f.write('\n')
        self.f.write('closepath\nstroke\nshowpage\nrestore\n')
