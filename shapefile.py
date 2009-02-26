#Martin Lacayo-Emery
#12/11/2008

import sys, struct
import databasefile
import math

def convexHull(inName,outName):
    inShapefile=Shapefile(1)
    inShapefile.readFile(inName)
    outShapefile=Shapefile(5)
    outShapefile.add(GrahamScan(inShapefile.shapes))

def rightTurn(p1,p2,p3):
    r1,theta1=polar(p1[0],p1[1],p2[0],p2[1])
    r2,theta2=polar(p3[0],p3[1],p2[0],p2[1])

    if theta1-theta2>=math.pi:
        return True
    else:
        return False
    #return math.atan((((p2[0]-p3[0])**2+(p2[1]-p2[1])**2)**0.5)/(((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)**0.5))
    #return (((p2[0] - p1[0])*(p3[1] - p1[1])) - ((p3[0] - p1[0])*(p2[1] - p1[1])))

def polarDeg(x,y):
    r,theta=polar(x,y)
    return r,180*theta/math.pi

def polar(x,y,originX=0,originY=0):
    x=x-originX
    y=y-originY
    
    if x==0:
        if y==0:
            return(0,0)
        elif y>0:
            return (y,math.pi/2)
        else:
            return (abs(y),3*math.pi/2)
    elif x>0:
        if y==0:
            return(x,0)
        elif y>0:
            return ((x**2+y**2)**0.5,math.atan(y/x))
        else:
            return ((x**2+y**2)**0.5,(2*math.pi)+math.atan(y/x))
    else:
        if y==0:
            return (abs(x),math.pi)
        elif y>0:
            return ((x**2+y**2)**0.5,math.pi+math.atan(y/x))
        else:
            return ((x**2+y**2)**0.5,math.pi+math.atan(y/x))
        

def rPolar(x,y,originX=0,originY=0):
    r,theta=polar(x,y,originX,originY)
    return theta,r

def relative(p1,p2):
    return p2[0]-p1[0],p2[1]-p1[0]

def GrahamScan(points):
    #get smallest y, choose smallest x if tie
    map(lambda x: x.reverse(),points)
    points.sort()
    map(lambda x: x.reverse(),points)    
    perimeter=[points.pop(0)]

    #sort by tangent with origin, choose smallest as second point
    points.sort(lambda a,b: cmp(rPolar(a[0],a[1],perimeter[0][0],perimeter[0][1]),rPolar(b[0],b[1],perimeter[0][0],perimeter[0][1])))
    t=Shapefile(3)
    for p in points:
        t.add([perimeter[0],p])
    t.writeFile("C:/order")
    
    perimeter.append(points.pop(0))
    points.append(perimeter[0])

    for p in points:
        if not rightTurn(perimeter[-2],perimeter[-1],p):
            perimeter.pop(-1)
            perimeter.append(p)
        else:
            perimeter.append(p)

    return perimeter            


def buffer(x1,y1,x2,y2,r):
    """
    """
    x1=float(x1)
    offsetX=r*math.cos(math.atan((y1-y2)/(x1-x2)))
    offsetY=r*math.sin(math.atan((y1-y2)/(x1-x2)))
    points=[(x1-offsetX,y1+offsetY),(x2-offsetX,y2+offsetY),
            (x2+offsetX,y2-offsetY),(x1+offsetX,y1-offsetY),
            (x1-offsetX,y1+offsetY)]
    return points

def circle(x,y,r=1/(3**0.5),n=6,theta=-1*math.pi/2):
    """
    """
    points=[]
    for i in range(n):
        points.append((x+(r*math.cos(-1*(theta+(i*2*math.pi/n)))),y+(r*math.sin(-1*(theta+(i*2*math.pi/n))))))
    points.append((x+(r*math.cos(-1*theta)),y+(r*math.sin(-1*theta))))
    return points

def rectangle(x,y,r):
    """
    returns the coordinates for a closed set of points forming a rectangle.
    The rectangle is centered at (x,y) and has a width of r
    """
    return [(x,y),(x,y+r),(x+r,y+r),(x+r,y),(x,y)]

def hexagonCentroid(x,y,originX=0,originY=0,r=1):
    if (y+2)%2:
        return (originX+((x+0.5)*r),originY-(y*r*(0.75**0.5)))
    else:
        return (originX+(x*r),originY-(y*r*(0.75**0.5)))
    

def hexagonCentroids(startX,endX,startY,endY,r):
    """
    returns a list of the centorids for a hexagonal grid with spacing r
    """
    deltaY=r*(0.75**0.5)
    deltaX=float(r)

    #set the orgin
    hexX=startX
    hexY=startY

    points=[]
    for y in range(startY,endY):
        if (y-startY+2)%2:
            hexX=startX+(0.5*deltaX)
        else:
            hexX=startX
        for x in range(startX,endX):
            points.append((hexX,hexY))
            hexX+=deltaX
        hexY-=deltaY

    return points        

def hexagon(x,y,r):
    """
    returns the coordinates for a closed set of points froming a hexagon.
    The hexagon is centered at (x,y) and has a width of r
    """
    offset1=r/(3**0.5)
    offset2=r
    offset3=2*offset1
    return [(x,y+offset3),(x+offset2,y+offset1),
            (x+offset2,y-+offset1),(x,y-offset3),
            (x-offset2,y-offset1),(x-offset2,y+offset1),
            (x,y+offset3)]

class Shapefile:
    """
    Shapefile class supporting single point and single part polygon shapes.
    Shapes are passed in as a list of points.
    """
    def __init__(self,shapeType=1):
        Xmin=0
        Ymin=0
        Xmax=0
        Ymax=0
        Zmin=0
        Zmax=0
        Mmin=0
        Mmax=0
        shapes=[]
        fieldnames=[]
        fieldspecs=[]
        records=[]

        self.fileCode=9994
        self.version=1000
        #number of 16-bit words
        self.size=50

        self.shapeType=shapeType
        self.Xmin=Xmin
        self.Ymin=Ymin
        self.Xmax=Xmax
        self.Ymax=Ymax
        self.Zmin=Zmin
        self.Zmax=Zmax
        self.Mmin=Mmin
        self.Mmax=Mmax

        if len(shapes)!=len(records):
            raise ValueError, "The number of shapes and table records must match."
        
        self.shapes=shapes
        self.table=databasefile.DatabaseFile(["ID"]+fieldnames,[('N', 6, 0)]+fieldspecs,records)
        

    def add(self,shape,record=None):
        """
        Adds a shape object to the shapefile. Adding records not currently supported.
        """
        #adjust the bound box minmums and maximums
        for p in shape:
            if p[0]<self.Xmin:
                self.Xmin=p[0]
            elif p[0]>self.Xmax:
                self.Xmax=p[0]
            if p[1]<self.Ymin:
                self.Ymin=p[1]
            elif p[1]>self.Ymax:
                self.Ymax=p[1]

        #adjust the known file size accordingly
        if self.shapeType==1:
            self.size+=10
            self.shapes.append(shape.pop())
        elif self.shapeType==5 or self.shapeType==3:
            self.size+=28+(8*len(shape))
            self.shapes.append(shape)

        #assign the passed in record, or generate an id
        if record:
            raise ValueError, "Passing in table records is not currently supported"
        else:
            self.table.addRow([len(self.shapes)])

    def readFile(self,inName):
        inShp=open(inName+".shp",'rb')
        self.readShp(inShp)
        inShp.close()
        
        self.table=databasefile.DatabaseFile([],[],[]).readFile(inName+".dbf")

    def readShp(self,inShp):
        #shp file header
        #byte 0, File Code
        self.fileCode,=struct.unpack('>i',inShp.read(4))
        inShp.seek(24)   
        #byte 24, File Length, total length of file in 16-bit words
        size,=struct.unpack('>i',inShp.read(4))
        #byte 28, Version, integer
        self.version,=struct.unpack('<i',inShp.read(4))
        #byte 32, shape type
        self.shapeType,=struct.unpack('<i',inShp.read(4))
        #byte 36, Bounding Box Xmin
        self.Xmin,=struct.unpack('<d',inShp.read(8))
        #byte 44 Bounding Box Ymin
        self.Ymin,=struct.unpack('<d',inShp.read(8))
        #byte 52 Bounding Box Xmax
        self.Xmax,=struct.unpack('<d',inShp.read(8))
        #byte 60 Bounding Box Ymax
        self.Ymax,=struct.unpack('<d',inShp.read(8))
        #byte 68* Bounding Box Zmin
        self.Zmin,=struct.unpack('<d',inShp.read(8))
        #byte 76* Bounding Box Zmax
        self.Zmax,=struct.unpack('<d',inShp.read(8))
        #byte 84* Bounding Box Mmin
        self.Mmin,=struct.unpack('<d',inShp.read(8))
        #byte 92* Bounding Box Mmax
        self.Mmax,=struct.unpack('<d',inShp.read(8))

        #read shapes
        if self.shapeType==1:
            for i in range((size-50)/10):
                id,=struct.unpack('>i',inShp.read(4))
                length,=struct.unpack('>i',inShp.read(4))
                shapeType,=struct.unpack('<i',inShp.read(4))
                x,=struct.unpack('<d',inShp.read(8))
                y,=struct.unpack('<d',inShp.read(8))
                self.add([(x,y)])
                               
        elif self.shapeType==5 or self.shapeType==3:
            raise ValueError, "Sorry only poiny reading is currently supported."
##            while inShp.tell()<(size*2):
##                id,=struct.unpack('>i',inShp.read(4))
##                length,=struct.unpack('>i',inShp.read(4))
##                shapeType,=struct.unpack('<i',inShp.read(4))
##                Xmin,=struct.unpack('<d',inShp.read(8))
##                Ymin,=struct.unpack('<d',inShp.read(8))
##                Xmax,=struct.unpack('<d',inShp.read(8))
##                Ymax,=struct.unpack('<d',inShp.read(8))
##                numParts,=struct.unpack('<i',inShp.read(4))
##                numPoints,=struct.unpack('<i',inShp.read(4))
##
##                numParts+=1
##                if numParts==1:
##                    raise ValueError, "Sorry multipart shapes are not supported."
##
##                parts=[]
##                print "Here"
##                for i in range(numParts):
##                    parts.append(struct.unpack('<i',inShp.read(4)))
##
##                points=[]
##                for i in range(numPoints):
##                    x,=struct.unpack('<d',inShp.read(8))
##                    y,=struct.unpack('<d',inShp.read(8))
##                    points.append((x,y))
##                print points
##                self.add(points)
                    
        
    def writeFile(self,outName):
        outShp=open(outName+".shp",'wb')
        outShx=open(outName+".shx",'wb')
        outDbf=open(outName+".dbf",'wb')
        self.table.write(outDbf)
        outDbf.close()
        self.write(outShp,outShx)
        outShp.close()
        outShx.close()

    def write(self,shp,shx):
        
        #shp file header
        #byte 0, File Code
        shp.write(struct.pack('>i', self.fileCode))
        #byte 4, Unused
        shp.write(struct.pack('>i', 0))
        #byte 8, Unused
        shp.write(struct.pack('>i', 0))
        #byte 12, Unused
        shp.write(struct.pack('>i', 0))
        #byte 16, Unused
        shp.write(struct.pack('>i', 0))
        #byte 20, Unused
        shp.write(struct.pack('>i', 0))
        #byte 24, File Length, total length of file in 16-bit words
        #this must be determined after file creation.
        shp.write(struct.pack('>i', self.size))
        #byte 28, Version, integer
        shp.write(struct.pack('<i', self.version))
        #byte 32, shape type
        shp.write(struct.pack('<i',self.shapeType))
        #byte 36, Bounding Box Xmin
        shp.write(struct.pack('<d',self.Xmin))
        #byte 44 Bounding Box Ymin
        shp.write(struct.pack('<d',self.Ymin))
        #byte 52 Bounding Box Xmax
        shp.write(struct.pack('<d',self.Xmax))
        #byte 60 Bounding Box Ymax
        shp.write(struct.pack('<d',self.Ymax))
        #byte 68* Bounding Box Zmin
        shp.write(struct.pack('<d',self.Zmin))
        #byte 76* Bounding Box Zmax
        shp.write(struct.pack('<d',self.Zmax))
        #byte 84* Bounding Box Mmin
        shp.write(struct.pack('<d',self.Mmin))
        #byte 92* Bounding Box Mmax
        shp.write(struct.pack('<d',self.Mmax))

        #shx file header
        #byte 0, File Code
        shx.write(struct.pack('>i', self.fileCode))
        #byte 4, Unused
        shx.write(struct.pack('>i', 0))
        #byte 8, Unused
        shx.write(struct.pack('>i', 0))
        #byte 12, Unused
        shx.write(struct.pack('>i', 0))
        #byte 16, Unused
        shx.write(struct.pack('>i', 0))
        #byte 20, Unused
        shx.write(struct.pack('>i', 0))
        #byte 24, File Length, total length of file in 16-bit words
        shx.write(struct.pack('>i', 50+(4*len(self.shapes))))
        #byte 28, Version, integer
        shx.write(struct.pack('<i', self.version))
        #byte 32, shape type
        shx.write(struct.pack('<i',self.shapeType))
        #byte 36, Bounding Box Xmin
        shx.write(struct.pack('<d',self.Xmin))
        #byte 44 Bounding Box Ymin
        shx.write(struct.pack('<d',self.Ymin))
        #byte 52 Bounding Box Xmax
        shx.write(struct.pack('<d',self.Xmax))
        #byte 60 Bounding Box Ymax
        shx.write(struct.pack('<d',self.Ymax))
        #byte 68* Bounding Box Zmin
        shx.write(struct.pack('<d',self.Zmin))
        #byte 76* Bounding Box Zmax
        shx.write(struct.pack('<d',self.Zmax))
        #byte 84* Bounding Box Mmin
        shx.write(struct.pack('<d',self.Mmin))
        #byte 92* Bounding Box Mmax
        shx.write(struct.pack('<d',self.Mmax))

        #write shapes
        if self.shapeType==1:
            contentLength=10
            for id,p in enumerate(self.shapes):
                #record header
                #record numbers start at 1
                shp.write(struct.pack('>i',id))
                #content length
                shp.write(struct.pack('>i',contentLength))

                #record contents
                #print float(i[0]),float(i[1])
                shp.write(struct.pack('<i',self.shapeType))
            
                shp.write(struct.pack('<d',p[0]))
                shp.write(struct.pack('<d',p[1]))

                #writing index records
                #size=record header+content length
                shx.write(struct.pack('>i',50+((contentLength+4)*id)))
                shx.write(struct.pack('>i',contentLength))
                               
        elif self.shapeType==5 or self.shapeType==3:
            totalLength=50
            for id,s in enumerate(self.shapes):
                contentLength=24+(8*len(s))
                #record header
                #record numbers start at 1
                shp.write(struct.pack('>i',id))
                #content length
                shp.write(struct.pack('>i',contentLength))

                #record contents
                shp.write(struct.pack('<i',self.shapeType))

                #bound box for polygon
                temp=apply(zip,s)
                box=map(min,temp)+map(max,temp)
                for m in box:
                    shp.write(struct.pack('<d',m))

                #number of parts        
                shp.write(struct.pack('<i',1))
                #number of points
                shp.write(struct.pack('<i',len(s)))
                #parts index
                shp.write(struct.pack('<i',0))

                #points
                for p in s:
                    #shape type for point
                    #x coordinate
                    shp.write(struct.pack('<d',float(p[0])))
                    #y coordinate
                    shp.write(struct.pack('<d',float(p[1])))

                #writing index records
                #size=record header+content length
                shx.write(struct.pack('>i',totalLength))
                shx.write(struct.pack('>i',contentLength))
                totalLength+=contentLength+4


if __name__=="__main__":
    s=Shapefile(1)
    for p in hexagonCentroids(0,7,0,5,1):
        s.add([p])
    s.writeFile("C:/grid")

