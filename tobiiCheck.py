import sys, string

def tobiiCheck(inName,outName):
    inFile=open(inName)
    outFile=open(outName,'w')
    for i in range(24):
        outFile.write(inFile.readline())
    header=inFile.readline().strip().split("\t")
    print header
    #translate the header to be character compliant
    charmap=string.maketrans(string.punctuation+string.whitespace,"_"*39)
    header=[f.translate(charmap) for f in header]

    outFile.write("\t".join(header)+"\n")
    outFile.write(inFile.read().strip())

    inFile.close()
    outFile.close()

if __name__=="__main__":
    inName=sys.argv[1]
    outName=sys.argv[2]
    tobiiCheck(inName,outName)