import os.path
import os
import argparse
import shutil

def convert(from_dir, to_dir, zoom, minx, maxx, miny, maxy):
    print(from_dir, to_dir, zoom, minx, maxx, miny, maxy)
    max_value = pow(2, int(zoom))
    x_range = range(minx, maxx + 1)
    for x in x_range:
        y_range = range(miny, maxy + 1)
        for y in y_range:
            f = "%s.png" % (y)
            from_file = os.path.join(from_dir, str(zoom), str(x), f)
            to_y = "%s.png" % (max_value - 1 - y)
            to_file = os.path.join(to_dir, str(zoom), str(x), to_y)
            shutil.copyfile(from_file, to_file)
            print(from_file, to_file)

class TMS2XYZ(object):
    def __init__(self, from_dir, to_dir):
        self.from_dir = os.path.abspath(from_dir)
        self.to_dir = os.path.abspath(to_dir)
        zooms = []
        with os.scandir(self.from_dir) as it:
            for entry in it:
                if entry.is_dir():
                    zooms.append(entry.name)
        zooms = list(map((lambda z: int(z)), zooms))
        self.zooms = zooms
        print(self.zooms)

    def __prepare(self):
        os.makedirs(self.to_dir)
        for z in self.zooms:
            zdir = os.path.join(self.to_dir, str(z))
            os.mkdir(zdir)
            with os.scandir(os.path.join(self.from_dir, str(z))) as it:
                for entry in it:
                    xdir = os.path.join(zdir, str(entry.name))
                    os.mkdir(xdir)

    def __get_range(self, zoom):
        zdir = os.path.join(self.from_dir, str(zoom))
        xs = []
        with os.scandir(zdir) as it:
            for entry in it:
                if entry.is_dir():
                    xs.append(entry.name)
        x = xs[0]
        xdir = os.path.join(zdir, x)
        yfiles = []
        with os.scandir(xdir) as it:
            for entry in it:
                if entry.is_file():
                    yfiles.append(entry.name)
        ys = []
        for y in yfiles:
            sp = os.path.splitext(y)
            print(sp)
            if sp[1] == ".png":
                ys.append(int(sp[0]))
        xs = list(map((lambda t: int(t)), xs))
        minx = min(xs)
        maxx = max(xs)
        miny = min(ys)
        maxy = max(ys)
        return minx, maxx, miny, maxy

    def __execute(self):
        for z in self.zooms:
            print(z)
            minx, maxx, miny, maxy = self.__get_range(z)
            convert(self.from_dir, self.to_dir, z, minx, maxx, miny, maxy)
        print("finish running")

    def run(self):
        self.__prepare()
        self.__execute()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Convert from TMS to WMTS")
    parser.add_argument('from_dir', metavar="from_dir",
                        help='TMS directory')
    parser.add_argument('output_dir', metavar='output_dir',
                        help="output directory")

    args = parser.parse_args()
    t = TMS2XYZ(args.from_dir, args.output_dir)
    t.run()
