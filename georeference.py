import sys

def worldFile(inName,xScale,yScale,xRotation,yRotation,xTranslation,yTranslation):
    outFile=open(inName+"w","w")
    outFile.write("\n".join((xScale,yScale,xRotation,yRotation,xTranslation,yTranslation)))
    outFile.close()

if __name__=="__main__":
    inName=sys.argv[1]
    xScale=sys.argv[2]
    yScale=sys.argv[3]
    xRotation=sys.argv[4]
    yRotation=sys.argv[5]
    xTranslation=sys.argv[6]
    yTranslation=sys.argv[7]
    worldFile(inName,xScale,yScale,xRotation,yRotation,xTranslation,yTranslation)