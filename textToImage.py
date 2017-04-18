from PIL import Image, ImageDraw
from numpy import genfromtxt
import pandas as pd
import sys
#temp = genfromtxt("test.txt", delimiter = ",")
def main():
    temp = pd.read_table(sys.argv[1], sep = "\t", header=None)#.as_matrix()
    #print temp
    im = Image.new(mode="RGB",size=temp.shape)
    pix = im.load()
    rows, cols = im.size
    for x in range(cols):
        for y in range(rows):
            #print temp.iloc[y,x]
            #print type(temp.iloc[y,x])
            #print x, y
            rgb = parse(temp.iloc[y,x])
            #print rgb
            pix[y,x] = rgb
    im.save(sys.argv[2])

def parse(x):
    strNoParen = x[1:-1]
    #print strNoParen
    strNoComma = strNoParen.replace(","," ")
    strList = strNoComma.split()
    numList = map(lambda x: int(x), strList)
    return tuple(numList)

if __name__ == "__main__":
    main()
