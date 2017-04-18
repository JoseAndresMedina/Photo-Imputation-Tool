import pandas as pd, import numpy as np
def main():
    radius = 1
    df = pd.read_table("test.txt", sep = "\t", header=None)
    rows, cols = df.shape
    
    for x in cols:
        for y in rows:
            pixel = df.iloc[y,x]
            if pixel is np.nan: impute(df,x,y,radius)
    #print some logging information
    #write output
def impute(df, x, y, radius):
    neightbors = list()
    #gather neighbor pixel values
    for i in range(x-radius, x+radius+1): #upper bound is exclusive
        for j in range(y-radius, y+radius+1):
            if x < 0 or y < 0 or x >= df.shape[1] or y >= df.shape[0]: #check bound
                continue
            elif i == x and j == y: #missing pixel
                continue
            else: 
                neighbors.append(parse(df.iloc[j,i]))
    #get modes
    listNeighbors = [list(x) for x in neighbors]
    rgbTable = pd.DataFrame(listNeighbors)
    rgbTable.columns = ["r","g","b"]
    print rgbTable
    modes = rgbTable.mode()
    print modes
    #if a value is nan, use rgbTable.mean() instead, print something or log
    #pix = new parsed tuple
    #df.iloc[y,x] = pix
    #return
def parse(x):
    strNoParen = x[1:-1]
    #print strNoParen
    strNoComma = strNoParen.replace(","," ")
    strList = strNoComma.split()
    numList = map(lambda x: int(x), strList)
    return tuple(numList)              

if __name__ == "__main__":
    main()
