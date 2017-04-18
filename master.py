from PIL import Image
from random import randint
import numpy as np
import sys
import pandas as pd
################
tearColor = (248,248,255)
radius = 2
################

def main():
    #load input
    infile = sys.argv[1]
    im = Image.open(infile)
    pix = im.load()

    #tear
    tornImg = tear(im,pix) #may need to do a deep copy or something
    tornPix = tornImg.load()

    outFile = infile.replace(".jpg", "Torn.jpg")
    tornImg.save(outFile, "JPEG", quality=95, optimize=True, progressive=True)

    width, height = im.size
    totalMissing = 0
    for x in range(width):
        for y in range(height):
            if tornPix[x,y] == tearColor:
                totalMissing += 1
    print totalMissing, " missing pixels"

    for x in range(width):
        for y in range(height):
            if tornPix[x,y] == tearColor:
                tornPix[x,y] = impute(tornImg,tornPix,x,y,radius)

    newMissing = 0
    for x in range(width):
        for y in range(height):
            if tornPix[x,y] == tearColor:
                newMissing += 1
    print newMissing, " missing pixels after imputation"

    outFile = infile.replace(".jpg", "Fixed.jpg")
    tornImg.save(outFile, "JPEG", quality=95, optimize=True, progressive=True)

def impute(img,pix,x,y,rad):
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
    rgbTable.columns = ["r","g","b"]
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
    print newPixel
    return newPixel


def tear(im,pix):
    width, height = im.size
    tearLength = 150

    x = 0  #randint(0, width - (1+tearLength) )
    y = randint(0, height-1)

    # print("{0} \t {1}".format(start_x,start_y))

    length = 0
    while length != tearLength:
        #print(x, "\t", y)
        pix[x,y] = tearColor
        #print(pix[x,y])

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
    return im


if __name__ == "__main__":
    main()
