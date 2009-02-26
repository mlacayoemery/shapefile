import sys, shapefile

def NewAOI(outName,shapeType):
    if shapeType=="point":
        shapeType=1
    elif shapeType=="line":
        shapeType=3
    else:
        shapeType=5
        
    s=shapefile.Shapefile(shapeType)
    s.writeFile(outName[:outName.rfind(".")])

if __name__=="__main__":
    outName=sys.argv[1]
    shapeType=sys.argv[2]
    NewAOI(outName,shapeType)