"""
LINEAR REGRESSION | StatQuest with Josh Starmer
(https://www.youtube.com/watch?v=nk2CQITm_eo)

3 most important concepts around Linear Regression
    1. Use Least Squares to Fit a line to the data
    2. Calculate R^2 (r-squared)
    3. Calculate a P value for R^2
    (REFER: https://youtu.be/nk2CQITm_eo?t=62)

16:05 03/01/2024
"""

import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import scriptcontext
import Rhino
tol = Rhino.RhinoDoc.ActiveDoc.ModelAbsoluteTolerance
angTol = Rhino.RhinoDoc.ActiveDoc.ModelAngleToleranceDegrees
import itertools
import math
import System.Drawing.Color as color

ptID = rs.GetObjects("sel pts to fit a line!", rs.filter.point)
ptRC = map(rs.coerce3dpoint,ptID)

EXTENSION_FACTOR = 100
global EXTENSION_FACTOR

extendCrv = lambda vCrv, vLength: vCrv.Extend(rg.CurveEnd.Both, vLength, rg.CurveExtensionStyle.Line)

xCol = [i.X for i in ptRC]
yCol = [i.Y for i in ptRC]

ptCentroid = lambda vPtLst : rg.Point3d(sum(map(lambda v: v.X,vPtLst))/len(vPtLst), sum(map(lambda v: v.Y,vPtLst))/len(vPtLst), sum(map(lambda v: v.Z,vPtLst))/len(vPtLst))
#scriptcontext.doc.ActiveDoc.Objects.AddPoint(ptCentroid(ptRC))

# --------------------------------------------------------------- INITIALIZATION
ptC = ptCentroid(ptRC)
lnInit = rg.Line(rg.Point3d(0,0,0),ptC)
BBInit = rg.BoundingBox(ptRC)
lnInit.ExtendThroughBox(BBInit)
lnCrv = lnInit.ToNurbsCurve()
lnCrv2 = extendCrv(lnCrv,EXTENSION_FACTOR)
simplifyCrv = lambda vCrv : vCrv.Simplify(rg.CurveSimplifyOptions.RebuildLines,tol,angTol)
lnCrv3 = simplifyCrv(lnCrv2)
rebuildLineByEndPt = lambda vCrv: rg.Line(vCrv.PointAtStart,vCrv.PointAtEnd).ToNurbsCurve()
lnCrv4 = rebuildLineByEndPt(lnCrv3)
lnCrv4_ID = scriptcontext.doc.ActiveDoc.Objects.AddCurve(lnCrv4)

# ---------------------------------------------- VERTICAL PROJECTION IN 2D PLANE
lnVerticalPlaneByEndPts = lambda vCrv: rg.Plane(vCrv.PointAtStart,vCrv.PointAtEnd-vCrv.PointAtStart,rg.Plane.WorldXY.ZAxis)
vPln = lnVerticalPlaneByEndPts(lnCrv4)

yAxis = rg.Plane.WorldXY.YAxis
yTr = rg.Transform.ProjectAlong(vPln,yAxis)

ptProj = map(rg.Point3d,ptRC)       #localCopy
map(lambda vPt: vPt.Transform(yTr),ptProj)
ptProjID = map(scriptcontext.doc.ActiveDoc.Objects.AddPoint,ptProj)
rs.AddObjectsToGroup(ptProjID,rs.AddGroup())

# ------------------------------------------ SSD CALC (SUM OF SQUARED RESIDUALS)
D = map(lambda v1,v2: v1.DistanceTo(v2),*[ptRC,ptProj])     # RESIDUAL in StatQuest terms
#### print("R (the redisual list): ",D) 
SSD_calculate = lambda dLst: sum(map(lambda v: v**2,dLst))   # SSD = Square each distance & then add them up
SSD = SSD_calculate(D)
#### print("SSR for this instance: ", str(SSD))

# -------------------------------------------------------- FINDING LEAST SQUARES

# ITERATIVE SSR COLLECTION

# numpy style cumsum for Python 2.7
def cumsum(lis):
    # accumu
    # https://stackoverflow.com/questions/15889131/how-to-find-the-cumulative-sum-of-numbers-in-a-list
    total = 0
    for x in lis:
        total += x
        yield total

# numpy style frange for Python 2.7
def frange(x, y, num):
    """ 
    ensures the output lenght is the same as the requested num
    23:39 24/06/2021, 23:54 24/06/2021, 00:17 25/06/2021, 00:46 25/06/2021
    """
    num = num-1 
    # internally making the request 1 unit smaller as a division procedsure will 
    # increase the num of total elements by 1.
    # So we take care of this internally.
    
    #print "num: ", num
    #jump = float(Decimal((y-x)/num))
    jump = float((y-x)/num)
    ##############print "jump: ", jump
    ##############print x * jump
    
    #print y-x
    #print jump*num
    
    """
    while x <= y:
        #yield x
        frangeColl.append(x)
        x += jump
    """
    counter = itertools.count(start=0, step=jump)
    frangeColl = [x + next(counter) for i in range(num+1)]
    
    ##############print "frangeColl: ", frangeColl
    ##############print "len(frangeColl): ", len(frangeColl), "_ _ _ _"
    ##############print "frangeColl[0]: ", frangeColl[0]
    ##############print "frangeColl[-1]: ", frangeColl[-1]
    
    return frangeColl

epochs = 1000
# We solve for 1000 rotations around the centroid....
#incrLst = range(0,1000,fullCircleRadian)
incrLst = frange(0,360,epochs)
#print incrLst
incrLstRad = map(Rhino.RhinoMath.ToRadians,incrLst)
#print incrLstRad
incrLstCumSum = list(cumsum(incrLstRad))
#print(len(incrLst))
initialLnMidPt = lnCrv4.PointAt(0.5)
trRotLst = map(lambda vAngRad : rg.Transform.Rotation(vAngRad,initialLnMidPt),incrLstCumSum)
#rg.Transform.Rotation(
crvLstRot = [lnCrv4.DuplicateCurve() for i in range(1000)]     # these are 1000 rotatable copies
map(lambda vCrv, vTr: vCrv.Transform(vTr),*[crvLstRot,trRotLst])

# map(scriptcontext.doc.ActiveDoc.Objects.AddCurve,crvLstRot)

def getSSR(crv,ptLst):
    
    # ---------------------------------------------- VERTICAL PROJECTION IN 2D PLANE
    lnVerticalPlaneByEndPts = lambda vCrv: rg.Plane(vCrv.PointAtStart,vCrv.PointAtEnd-vCrv.PointAtStart,rg.Plane.WorldXY.ZAxis)
    vPln = lnVerticalPlaneByEndPts(crv)
    
    yAxis = rg.Plane.WorldXY.YAxis
    yTr = rg.Transform.ProjectAlong(vPln,yAxis)
    
    ptProj = map(rg.Point3d,ptLst)       #localCopy
    map(lambda vPt: vPt.Transform(yTr),ptProj)
    # ptProjID = map(scriptcontext.doc.ActiveDoc.Objects.AddPoint,ptProj)
    # rs.AddObjectsToGroup(ptProjID,rs.AddGroup())
    
    # ------------------------------------------ SSD CALC (SUM OF SQUARED RESIDUALS)
    D = map(lambda v1,v2: v1.DistanceTo(v2),*[ptLst,ptProj])     # RESIDUAL in StatQuest terms
    # print("R (the redisual list): ",D) 
    SSD_calculate = lambda dLst: sum(map(lambda v: v**2,dLst))   # SSD = Square each distance & then add them up
    SSD = SSD_calculate(D)
    # print("SSR for this instance: ", str(SSD))
    return SSD

SSR_map = map(lambda v: getSSR(v,ptRC),crvLstRot)
SSR_map_sorted, crvLstRot_sorted = zip(*sorted(zip(SSR_map,crvLstRot)))

print SSR_map_sorted[0]
print SSR_map_sorted[-1]

SSR_line = crvLstRot_sorted[0]
SSR_line_ID = scriptcontext.doc.ActiveDoc.Objects.AddCurve(SSR_line)

rs.ObjectColor(lnCrv4_ID,color.LightGray)
rs.ObjectColor(ptProjID,color.LightGray)
rs.ObjectColor(SSR_line_ID ,color.DarkBlue)