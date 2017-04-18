import sys
from PIL import Image

im = Image.open(sys.argv[1])
pix = im.load()

width, height = im.size

with open(sys.argv[2],"w+") as f:
    for x in range(width):
        for y in range(height):
            r = pix[x,y][0]
            g = pix[x,y][1]
            b = pix[x,y][2]
            if y == height-1:
                f.write("({0},{1},{2})".format(r,g,b))
            else:
                f.write("({0},{1},{2})\t".format(r,g,b))

        f.write("\n")
