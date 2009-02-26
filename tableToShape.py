import sys
import shapefile
import databasefile

def TableToShape(inName,xField,yField,outName,quadrant,shape,eventField,eventString,changeTypes):
    #read in data table
    inFile=databasefile.DatabaseFile([],[],[])
    inFile.readFile(inName)

    #get index for coordinate fields    
    xIndex=inFile.fieldnames.index(xField)
    yIndex=inFile.fieldnames.index(yField)
              
    #filter out rows that match the criteria
    if eventField!="#":
        eventIndex=inFile.fieldnames.index(eventField)
        if eventString=="#":
            eventString=""
        for i in range(len(inFile.records)-1,-1,-1):
            if inFile.records[i][eventIndex].strip()!=eventString:
                inFile.records.pop(i)

    if changeTypes:
        inFile.refreshSpecs()

    #set the scaling for the quadrant
    if quadrant=="1":
        xScale=1
        yScale=1
    elif quadrant=="2":
        xScale=-1
        yScale=1
    elif quadrant=="3":
        xScale=-1
        yScale=-1
    else:
        xScale=1
        yScale=-1

    #create geometry
    if shape=="point":
        #add points to shapefile
        s=shapefile.Shapefile(shapeType=1)
        for l in inFile.records:
            s.add([[float(l[xIndex])*xScale,float(l[yIndex])*yScale]])

        #append data table to geometry            
        s.table.extend(inFile)
        
    else:
        #create geometry
        s=shapefile.Shapefile(shapeType=3)
        if len(inFile.records):
            inFile.records=apply(zip,inFile.records)
            inFile.records=zip(map(float,inFile.records[xIndex]),map(float,inFile.records[yIndex]))
            inFile.records=[(float(x)*xScale,float(y)*yScale) for x,y in inFile.records]
            s.add(inFile.records)

    s.writeFile(outName[:outName.rfind(".")])
    
if __name__ == "__main__":
    inName=sys.argv[1]
    xField=sys.argv[2]
    yField=sys.argv[3]
    outName=sys.argv[4]
    quadrant=sys.argv[5]
    shape=sys.argv[6]
    eventField=sys.argv[7]
    eventString=sys.argv[8]
    if sys.argv[9]=="true":
        changeTypes=True
    else:
        changeTypes=False
        
    TableToShape(inName,xField,yField,outName,quadrant,shape,eventField,eventString,changeTypes=True)