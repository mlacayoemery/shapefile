import sys, shapefile

def hull(inName,outName):
    inFile=shapefile.Shapefile(1)
    outFile=shapefile.Shapefile(5)
    
    inFile.readFile(inName[:inName.rfind(".")])
    perimeter=shapefile.GrahamScan(map(list,inFile.shapes))
    outFile.add(perimeter)

    outFile.writeFile(outName[:outName.rfind(".")])
                
if __name__=="__main__":
    inName=sys.argv[1]
    outName=sys.argv[2]
    hull(inName,outName)