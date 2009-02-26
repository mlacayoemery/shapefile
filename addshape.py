import sys
import databasefile
import shapefile


inName="D:/work/uzh/cgis/02/02_01_ap01Ng-All-Data.dbf"
outName="D:/work/uzh/cgis/02/02_01_ap01Ng-All-Data"

d=databasefile.DatabaseFile([],[],[])
d.addFileColumn(inName, "GazePointX")
d.addFileColumn(inName, "GazePointY")
#d.writeFile("D:/work/uzh/cgis/02/shape.dbf")

##s=shapefile.Shapefile()
##
##for x,y in d.records:
##    s.add([(float(x),float(y))])
##shp=open("D:/work/uzh/cgis/02/02_01_ap01Ng-All-Data.shp","wb")
##shx=open("D:/work/uzh/cgis/02/02_01_ap01Ng-All-Data.shx","wb")
##s.write(shp,shx)