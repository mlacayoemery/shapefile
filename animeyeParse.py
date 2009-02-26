import sys, databasefile

def animeyeParse(inName,outName,dynamicSpecs):
    pairColumnIndex=8
    #read in file, remove header, strip and split lines
    inFile=open(inName)
    header=inFile.readline().split("\t")
    #get labels for pair columns and remove from header
    labelA,labelB=header.pop(pairColumnIndex).strip().strip("(").strip(")").split(",")
    #remove excess spacing from cells, and create row
    lines=[l.replace(" ","").strip().split("\t") for l in inFile.readlines()]
    inFile.close()

    #determine maximum cells in a row
    cells=max(map(len,lines))
    #construct header for zones by starting at 1 and adding numbers to labels
    for i in range(1,1+cells-pairColumnIndex):
        header.extend([labelA+str(i),labelB+str(i)])

    #loop over the lines and split the paired fields
    for i in range(len(lines)):
        #get the number of pairs in the row
        l = len(lines[i])-pairColumnIndex
        pad=[""]*((cells-len(lines[i]))*2)
        for j in range(l):
            lines[i].extend(lines[i].pop(pairColumnIndex).strip().strip("(").strip(")").split(","))
        #add empty cells for zone columns in other rows
        lines[i].extend(pad)

    #return header,lines
            
    d=databasefile.DatabaseFile(header,None,lines)

    if dynamicSpecs=="true":
        d.dynamicSpecs()
    else:
        d.staticSpecs()
        
    d.writeFile(outName)    
    
if __name__=="__main__":
    inName=sys.argv[1]
    outName=sys.argv[2]
    dynamicSpecs=sys.argv[3]
    animeyeParse(inName,outName,dynamicSpecs)