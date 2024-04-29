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
scriptcontext.doc.ActiveDoc.Objects.AddCurve(lnCrv4)

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
print("R (the redisual list): ",D) 
SSD_calculate = lambda dLst: sum(map(lambda v: v**2,dLst))   # SSD = Square each distance & then add them up
SSD = SSD_calculate(D)
print("SSR for this instance: ", str(SSD))
