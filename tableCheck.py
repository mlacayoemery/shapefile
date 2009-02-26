import sys, string

def tableCheck(inName,outName):
    inFile=open(inName)
    header=inFile.readline().strip().split("\t")
    charmap=string.maketrans(string.punctuation+string.whitespace,"_"*39)
    header=[f.translate(charmap) for f in header]

    outFile=open(outName,'w')
    outFile.write("\t".join(header)+"\n")
    outFile.write(inFile.read().strip())

    inFile.close()
    outFile.close()

if __name__=="__main__":
    inName=sys.argv[1]
    outName=sys.argv[2]
    tableCheck(inName,outName)