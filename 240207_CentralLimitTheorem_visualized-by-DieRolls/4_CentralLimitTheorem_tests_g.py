import statistics as st
import random as rnd

from collections import Counter
#input =  ['a', 'a', 'b', 'b', 'b']
#c = Counter( input )
#print( c.items() )

import rhinoscriptsyntax as rs
import Rhino.Geometry as rg
import scriptcontext
import System.Drawing.Color as color

# ---------------------------------------------------------------- VIZ UTILITIES

def plotAsTable(numLst):
    hSepStr = "---------------"
    print hSepStr
    for i,j in enumerate(numLst):
        print "| ", i+1, " | ", j, " |"
    print hSepStr
    return None
#plotAsTable(loopedMeanLst

# dual list to printable text

def plotDualLstAsTable_str(numLst1,numLst2):
    hSepStr = "---------------"
    #print hSepStr
    strMega = ""
    for i,j in enumerate(numLst1):
        strLocal = "| " + str(i+1) + " | " + str(j) +  " | " + str(numLst2[i]) + " |"
        strMega = strMega + "\n" + strLocal
    #print hSepStr
    return strMega



# ------------------------------------------------------------------------------
print(range(1,7,1))
randomChoiceFromLst = lambda : rnd.randrange(1,7,1)

rollCnt = 5 # vInnerLoop
meanXRolls = lambda vOuterXloop,vInnerLoop : [st.mean([randomChoiceFromLst() for i in range(vInnerLoop)]) for x in range(vOuterXloop)]

# 100 sets of 5 die rolls.
loopedMeanLst = meanXRolls(100,5)
####plotAsTable(loopedMeanLst)

# PREP FOR VISUALIZING AS A HISTOGRAM FOR CLT
cntr = (Counter(loopedMeanLst))
#####print cntr.items()
x,y = zip(*cntr.items())
#print x
#print y
x_sorted,y_sorted = zip(*sorted(zip(x,y)))
#####print x_sorted
#####print y_sorted

# SAMPLING DISTRIBUTION PLOTTER 
#def plotAsHistogram(
#xptLst = 
xAxisLn = rg.Line(rg.Point3d(0,0,0),rg.Point3d(max(x_sorted),0,0))
ptsOnXAxisLn = [rg.Point3d(i,0,0) for i in x_sorted]

vecLst = [rg.Plane.WorldXY.YAxis for i in y_sorted]
[i.Unitize() for i in vecLst]
vecLst2 = [rg.Vector3d.Multiply(y_sorted[i],vecLst[i]) for i in range(len(vecLst))]

lnYBars = [rg.Line(j,rg.Point3d.Add(vecLst2[i],j)) for i,j in enumerate(ptsOnXAxisLn)]
lnYBarsID2 = map(scriptcontext.doc.ActiveDoc.Objects.AddLine,lnYBars)
xAxisLnID = scriptcontext.doc.ActiveDoc.Objects.AddLine(xAxisLn)

lnYBarsID = []
lnYBarsID.append(xAxisLnID)
# independent vertical ln Group to show as black!
rs.AddObjectsToGroup(lnYBarsID2,rs.AddGroup())
rs.ObjectColor(lnYBarsID2,color.Black)

endPts = [i.PointAt(1) for i in lnYBars]
crvRC = rg.Curve.CreateInterpolatedCurve(endPts,3)
crvID = scriptcontext.doc.ActiveDoc.Objects.AddCurve(crvRC)
#rs.AddObjectsToGroup([crvID,lnYBarsID],rs.AddGroup())

#rs.ObjectColor(crvID,color.DarkGoldenrod)
colRandom = lambda : color.FromArgb(rnd.randint(0,254),rnd.randint(0,254),rnd.randint(0,254))
lnYBarsID.append(crvID)
#rs.AddObjectsToGroup(lnYBarsID,rs.AddGroup())
#rs.ObjectColor(lnYBarsID,colRandom())

# reporting processed values
txtRC = plotDualLstAsTable_str(x_sorted, y_sorted)
BB = rs.BoundingBox(lnYBarsID)
midPt = lambda v1,v2: [(v1[0]+v2[0])/2, (v1[1]+v2[1])/2, (v1[2]+v2[2])/2]
#ptTxt = BB[2]
ptTxt = midPt(BB[1], BB[2])
move = 5
ptTxt = [ptTxt[0]+move,ptTxt[1],ptTxt[2]]
txtDotID = rs.AddTextDot(txtRC,ptTxt)
lnYBarsID.append(txtDotID)
#rs.AddObjectsToGroup(lnYBarsID,rs.AddGroup())
#rs.ObjectColor(lnYBarsID,colRandom())

yAxisLn = rs.AddLine([0,0,0],[0,max(y_sorted),0])
lnYBarsID.append(yAxisLn)
#rs.AddObjectsToGroup(lnYBarsID,rs.AddGroup())
#rs.ObjectColor(lnYBarsID,colRandom())

# add a fill inside the created shape
#print(lnYBars[0].PointAt(0.0))      # 1.4,0,0   # frickin trivial....why-tf is it not outputting a rhinoCommon Point....LOL

btmLnRC = rg.Line(rg.Point3d(lnYBars[0].PointAt(0.0)),rg.Point3d(lnYBars[-1].PointAt(0.0)))
#print(btmLnRC)

brpRC = rg.Brep.CreateEdgeSurface([lnYBars[0].ToNurbsCurve(), btmLnRC.ToNurbsCurve(), lnYBars[-1].ToNurbsCurve(),crvRC])
brpID = scriptcontext.doc.ActiveDoc.Objects.AddBrep(brpRC)
lnYBarsID.append(brpID)
rs.AddObjectsToGroup(lnYBarsID,rs.AddGroup())
rs.ObjectColor(lnYBarsID,colRandom())

