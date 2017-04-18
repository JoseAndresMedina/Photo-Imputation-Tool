from PIL import Image
from random import randint
import numpy as np

#######################################################
infile = "blackSquare.jpg"
tearColor = (np.nan, np.nan, np.nan)
tearLength = 150
#######################################################

im = Image.open(infile)
pix = im.load()

width, height = im.size

x = 0  #randint(0, width - (1+tearLength) )
y = randint(0, height-1)

# print("{0} \t {1}".format(start_x,start_y))

length = 0
while length != tearLength:
    print(x, "\t", y)
    pix[x,y] = tearColor

    while True:
        nextMove = randint(1, 3)  # 1-up   2-right   3-down
        if nextMove == 1:
            y += 1
            x += 1
        elif nextMove == 2:
            x += 1
        elif nextMove == 3:
            y -= 1
            x += 1

        if (0 <= x < width) and (0 <= y < height):
            break

    length += 1

outFile = infile.replace(".jpg", "_TORN.jpg")
im.save(outFile, "JPEG", quality=95, optimize=True, progressive=True)