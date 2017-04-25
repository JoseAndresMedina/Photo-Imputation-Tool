from PIL import Image
from random import randint
import numpy as np
import sys
import pandas as pd
################
tearColor = (255, 255, 255, 0)
radius = 3
maxTearLength = 250
percentage = .1
################


def main():
    #load input
    infile = sys.argv[1]
    im = Image.open(infile).convert("RGBA")
    pix = im.load()

    #tear
    tornImg = tear(im, pix) #may need to do a deep copy or something
    tornPix = tornImg.load()

    outFile = infile.replace(".jpg", "Torn.jpg")
    tornImg.save(outFile, "JPEG", quality=95, optimize=True, progressive=True)

    width, height = im.size
    totalMissing = 0
    for x in range(width):
        for y in range(height):
            if tornPix[x,y] == tearColor:
                totalMissing += 1
    print (totalMissing, " missing pixels")

    for x in range(width):
        for y in range(height):
            if tornPix[x,y] == tearColor:
                tornPix[x,y] = impute(tornImg, tornPix, x, y)

    newMissing = 0
    for x in range(width):
        for y in range(height):
            if tornPix[x,y] == tearColor:
                newMissing += 1
    print(newMissing, " missing pixels after imputation")

    outFile = infile.replace(".jpg", "Fixed.jpg")
    tornImg.save(outFile, "JPEG", quality=95, optimize=True, progressive=True)


def impute(img, pix, x, y):
    width, height = img.size
    neighbors = list()
    #gather neighbor pixel values
    for i in range(x-radius, x+radius+1): #upper bound is exclusive
        for j in range(y-radius, y+radius+1):
            if i < 0 or j < 0 or i >= width or j >= height: #check bound
                continue
            elif pix[i,j] == tearColor: #missing pixel
                continue
            else:
                neighbors.append(pix[i,j])
    #get modes
    listNeighbors = [list(x) for x in neighbors]
    rgbTable = pd.DataFrame(listNeighbors)
    rgbTable.columns = ["r", "g", "b", "a"]
    #print rgbTable
    modes = rgbTable.mode()
    means = rgbTable.mean()
    #print modes
    values = modes.iloc[0].values
    #print values
    pixelList = list()
    i = 0
    for v in values:
        if np.isnan(v):
            #print "no mode, will use mean at pixel ", x, " ", y
            #index = values.index(v)
            mean = int(means.iloc[i])
            pixelList.append(mean)
        else:
            pixelList.append(int(v))
        i += 1
    newPixel = tuple(pixelList)
    # print(newPixel)
    return newPixel


def tear(im, pix):
    width, height = im.size

    threshold = percentage * width * height
    length = 0

    while length < threshold:
        print("----------NEW LINE STARTED----------")
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

        print( start)

        # print("{0} \t {1}".format(start_x,start_y))

        while ( inter_length < maxTearLength ) and ( length < threshold ):
            # print(length)
            pix[x,y] = tearColor
            while True:
                nextMove = randint(1, 3)
                next_y = y
                next_x = x

                if start == 1:
                     # 1-left  2-down   3-right
                    if nextMove == 1:
                        next_y += 1
                        next_x -= 1
                    elif nextMove == 2:
                        next_y += 1
                    elif nextMove == 3:
                        next_x += 1
                        next_y += 1

                elif start == 2:
                     # 1-up  2-left   3-down
                    if nextMove == 1:
                        next_y -= 1
                        next_x -= 1
                    elif nextMove == 2:
                        next_x -= 1
                    elif nextMove == 3:
                        next_y += 1
                        next_x -= 1

                elif start == 3:
                      # 1-left  2-up   3-right
                    if nextMove == 1:
                        next_y -= 1
                        next_x -= 1
                    elif nextMove == 2:
                        next_y -= 1
                    elif nextMove == 3:
                        next_y -= 1
                        next_x += 1

                elif start == 4:
                     # 1-up   2-right   3-down
                    if nextMove == 1:
                        next_y -= 1
                        next_x += 1
                    elif nextMove == 2:
                        next_x += 1
                    elif nextMove == 3:
                        next_y += 1
                        next_x += 1

                if (0 <= next_x < width) and (0 <= next_y < height):
                    x = next_x;
                    y = next_y
                    inter_length += 1;
                    break

            length += 1

    return im


if __name__ == "__main__":
    main()
