
class Writer(object):
    def __init__(self, filename, width, height, layers):
        """ Open the file and write headers """
        self.f = self.open(filename)
        self.width = width
        self.height = height
        self.layers = layers
        self.write_header()

    def open(self, filename):
        return open(filename, 'wb')

    def close(self):
        self.f.close()

    def finish(self):
        self.write_footer()
        self.close()

    def write_header(self):
        """ write the file header, if any """
        raise NotImplementedError

    def write_footer(self):
        """ write the file footer, if any """
        raise NotImplementedError

    def write_layer_paths(self, paths, number):
        """ Write the paths for a layer, including numbers """
        raise NotImplementedError
