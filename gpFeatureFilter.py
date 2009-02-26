import sys, arcgisscripting

def Filter(inName,field,minimum,maximum,outName):
    gp = arcgisscripting.create()

    if minimum !="#":
        if maximum !="#":
            expression="\""+field+"\" >= "+minimum+" AND "+"\""+field+"\" <= "+maximum
        else:
            expression="\""+field+"\" >= "+minimum
    elif maximum !="#":
        expression="\""+field+"\" <= "+maximum
    else:
        expression=""

    gp.Select_analysis(inName, outName, expression)

if __name__=="__main__":
    inName=sys.argv[1]
    field=sys.argv[2]
    minimum=sys.argv[3]
    maximum=sys.argv[4]
    outName=sys.argv[5]
    Filter(inName,field,minimum,maximum,outName)