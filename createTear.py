from PIL import Image
from random import randint
import numpy as np

#######################################################
infile = "books.jpg"
tearColor = (300, 300, 300)
maxTearLength = 250
percentage = .003
#######################################################

im = Image.open(infile)
pix = im.load()

width, height = im.size

threshold = percentage * width * height
print(threshold)
print(width)
print(height)
length = 0

while length < threshold:

    inter_length = 0
    start = randint(1,4) # 1-top   2-right   3-bottom   4-left

    if start == 1:
        x = randint(0, width-1)
        y = 0
    elif start == 2:
        x = width-1
        y = randint(0, height-1)
    elif start == 3:
        x = randint(0, width-1)
        y = height-1
    elif start == 4:
        x = 0
        y = randint(0, height-1)

    # print("{0} \t {1}".format(start_x,start_y))

    while ( inter_length != maxTearLength ) and ( length < threshold ):
        print(length)
        pix[x,y] = tearColor

        while True:
            nextMove = randint(1, 5)

            if start == 1:
                 # 1-left  2-down   3-right
                if nextMove == 1 or nextMove == 2:
                    y += 1
                    x -= 1
                elif nextMove == 3:
                    y += 1
                elif nextMove == 4 or nextMove == 5:
                    y += 1
                    x += 1

            elif start == 2:
                 # 1-up  2-left   3-down
                if nextMove == 1 or nextMove == 2:
                    y -= 1
                    x -= 1
                elif nextMove == 3:
                    x -= 1
                elif nextMove == 4 or nextMove == 5:
                    y += 1
                    x -= 1

            elif start == 3:
                  # 1-left  2-up   3-right
                if nextMove == 1 or nextMove == 2:
                    y -= 1
                    x -= 1
                elif nextMove == 3:
                    y -= 1
                elif nextMove == 4 or nextMove == 5:
                    y -= 1
                    x += 1

            elif start == 4:
                 # 1-up   2-right   3-down
                if nextMove == 1 or nextMove == 2:
                    y -= 1
                    x += 1
                elif nextMove == 3:
                    x += 1
                elif nextMove == 4 or nextMove == 5 :
                    y += 1
                    x += 1

            if (0 <= x < width) and (0 <= y < height):
                break

        length += 1
        inter_length += 1

print(length)
outFile = infile.replace(".jpg", "_TORN.jpg")
im.save(outFile, "JPEG", quality=95, optimize=True, progressive=True)