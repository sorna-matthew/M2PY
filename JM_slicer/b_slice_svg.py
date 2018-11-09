from textwrap import dedent
import b_slice_writer as writer

class SvgWriter(writer.Writer):
    def write_header(self):
        self.f.write(dedent("""\
          <svg xmlns="http://www.w3.org/2000/svg"
               xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
               xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape">
            <sodipodi:namedview units="mm" />
        """))

        self.offset = 0

    def write_footer(self):
        self.f.write('</svg>\n')

    def write_layer_paths(self, paths, number):
        max_x = 0
        self.f.write(dedent("""\
          <g inkscape:groupmode="layer" inkscape:label="Layer {0}" id="{0}">
            <g transform="translate({1})">
          """).format(number, self.offset))
    
        for path in paths:
            self.f.write('<g>\n')
            x_avg = sum(d[0] for d in path) / len(path)
            y_avg = sum(d[1] for d in path) / len(path)
            self.f.write(dedent("""\
              <text text-anchor="middle" font-size="2" fill="none"
                    stroke-width="0.1" stroke="blue" x="{}" y="{}">{}</text>
              """).format(x_avg, y_avg, number))
    
            self.f.write('<path fill="none" stroke-width="0.1" stroke="red" d="M %f %f' % path[0])
            for point in path[1:]:
                self.f.write(' L %f %f' % point)
                max_x = max(max_x, point[0])
            self.f.write('" />\n')
            self.f.write('</g>\n')
        self.offset += max_x
        self.f.write('</g>\n</g>\n')
