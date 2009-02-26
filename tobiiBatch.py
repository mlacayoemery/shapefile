import sys
import os
import tobiiParse

def tobiiBatch(infolder,infiles,prefix="",filestem=True,enum=False,outfolder="",dynamicSpecs=False):
    for id,f in enumerate(infiles):
        outfile=""
        if outfolder=="":
            outfile=infolder
        else:
            outfile=outfolder
        outfile=outfile+"\\"+prefix
        if filestem:
            outfile=outfile+f[:f.rfind(".")]
        if enum:
            outfile=outfile+str(id)
        outfile=outfile+".dbf"
        tobiiParse.tobiiParse(infolder+"\\"+f,outfile,dynamicSpecs)
        

if __name__=="__main__":
    infolder=sys.argv[1]
    infiles=os.listdir(infolder)
    if sys.argv[2]=="#":
        prefix=""
    else:
        prefix=sys.argv[2]
    if sys.argv[3]=="true":
        filestem=True
    else:
        filestem=False
    if sys.argv[4]=="true":
        enum=True
    else:
        enum=False
    if sys.argv[5]=="#":
        folder=""
    else:
        folder=sys.argv[5]
    if sys.argv[6]=="true":
        dynamicSpecs=True
    else:
        dynamicSpecs=False
        
    tobiiBatch(infolder,infiles,prefix,filestem,enum,folder,dynamicSpecs)