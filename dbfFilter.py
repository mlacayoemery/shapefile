import databasefile

def filterTable(inName,outName,field,keep=True,equal="#",minimum="#",maximum="#",retype=False):
    filterTableFile(inName,open(outName,"wb"),field,keep,equal,minimum,maximum,retype)

def filterTableFile(inName,outFile,field,keep=True,equal="#",minimum="#",maximum="#",retype=False):
    d=databasefile.DatabaseFile([],[],[],inName)
    fieldIndex=d.fieldnames.index(field)
    fieldType=databasefile.specType(d.fieldspecs[fieldIndex])

    if equal !="#":
        for i in range(len(d.records)-1,-1,-1):
            if fieldType(d.records[i][fieldIndex].strip())==fieldType(equal.strip()):
                if not keep:
                    d.records.pop(i)
            elif keep:
                d.records.pop(i)                    
    if minimum !="#":
        for i in range(len(d.records)-1,-1,-1):
            if fieldType(d.records[i][fieldIndex].strip())<fieldType(minimum.strip()):
                if not keep:
                    d.records.pop(i)
            elif keep:
                d.records.pop(i)
    if maximum !="#":
        for i in range(len(d.records)-1,-1,-1):
            if fieldType(d.records[i][fieldIndex].strip())>fieldType(maximum.strip()):
                if not keep:
                    d.records.pop(i)
            elif keep:
                d.records.pop(i)

    if retype:
        d.refreshSpecs()
        
    d.write(outFile)                