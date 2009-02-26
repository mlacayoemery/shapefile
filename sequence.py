import sys, databasefile

def Sequence(inName,aoiField,outName,format,userField="#",timeField="#"):
    """
    Sequence goes through a shapefile table and creates a sequence by appending the values in a cloumn.
    An user id field and a time field can be provided.
    """
    #read in data
    d=databasefile.DatabaseFile([],[],[])
    d.readFile(inName[:inName.rfind(".")]+".dbf")

    #setup variables for sequence
    fieldnames=[]
    fieldspecs=[]
    records=[]

    #add AOI field name to field name list and get index
    fieldnames.append(aoiField)
    aoiFieldIndex=d.fieldnames.index(aoiField)

    #rotate data table
    records=apply(zip,d.records)

    if userField =="#":
        #if no user field or time field specified
        if timeField=="#":
            #data contains single sequence in order in AOI column, just append all values
            records=[["".join(map(str,apply(zip,d.records)[aoiFieldIndex]))]]

        #if only time field specified
        else:
            #data contains single sequqence, but needs order by time field
            #join AOI column with time column, sort and append all values
            timeFieldIndex=d.fieldnames.index(timeField)
            records=zip(records[timeFieldIndex],records[aoiFieldIndex])
            records.sort()
            records=[["".join(map(str,apply(zip,records)[1]))]]

    #if only a user field specified
    elif timeField=="#":
        #user sequences, no time field
        fieldnames=[userField]+fieldnames
        userFieldIndex=d.fieldnames.index(userField)
        users=set(records[userFieldIndex])
        records=dict(zip(users,[""]*len(users)))
        for r in d.records:
            records[r[userFieldIndex]]+=str(r[aoiFieldIndex])
        records=zip(map(str,records.keys()),map(records.get,records.keys()))

    #if both a user field and time field specified
    else:
        #user sequences and time field
        #add user id field name to field names and get data index and create user set
        fieldnames=[userField]+fieldnames
        userFieldIndex=d.fieldnames.index(userField)
        users=list(set(records[userFieldIndex]))
        users.sort()

        #setup variables to store records and get time field index
        records=[]
        timeFieldIndex=d.fieldnames.index(timeField)
        recordsDict=dict(zip(users,[{}]*len(users)))

        #loop over each record in the data table and construct a dictioanry using the user and time for keys
        for r in d.records:
            recordsDict[r[userFieldIndex]][r[timeFieldIndex]]=r[aoiFieldIndex]

        #loop over each user and create sequence
        for k in users:
            #get list of times for user and setup variable for sequence
            times=recordsDict[k].keys()
            times.sort()
            line=[]

            #loop over times for user and create sequence            
            for t in times:
                line.append(recordsDict[k][t])

            #append user id with sequence to data table                
            records.append([k,"".join(line)])

    if format=="Comma Separated Values":
        outFile=open(outName,'w')
        #join all cells in rows by commas
        #add field names to begining of records table
        #join all rows by end or line characters
        outFile.write('\n'.join([",".join(fieldnames)]+map(",".join,records)))
        outFile.close()

    elif format=="Clustal G":
        lineWidth=72
        outFile=open(outName,'w')
        #write user id followed by rows of the sequence of no more than lineWidth characters.
        for r in records:
            outFile.write("> "+r[0]+"\r\n")
            temp=r[1]
            for i in range(int(round(float(len(temp)/lineWidth)))):
                outFile.write(temp[:lineWidth]+"\r\n")
                temp=temp[lineWidth:]
        outFile.close()
                    
    elif format=="Dbase IV":
        databasefile.DatabaseFile(fieldnames,fieldspecs,records).writeFile(outName)    

if __name__=="__main__":
    inName=sys.argv[1]
    userField=sys.argv[2]
    timeField=sys.argv[3]
    aoiField=sys.argv[4]
    outName=sys.argv[5]
    format=sys.argv[6]

    Sequence(inName,aoiField,outName,format,userField,timeField)