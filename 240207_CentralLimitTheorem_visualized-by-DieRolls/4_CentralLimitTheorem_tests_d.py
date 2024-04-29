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
lnYBarsID = map(scriptcontext.doc.ActiveDoc.Objects.AddLine,lnYBars)
xAxisLnID = scriptcontext.doc.ActiveDoc.Objects.AddLine(xAxisLn)

lnYBarsID.append(xAxisLnID)
#rs.AddObjectsToGroup(lnYBarsID,rs.AddGroup())

endPts = [i.PointAt(1) for i in lnYBars]
crvRC = rg.Curve.CreateInterpolatedCurve(endPts,3)
crvID = scriptcontext.doc.ActiveDoc.Objects.AddCurve(crvRC)
#rs.AddObjectsToGroup([crvID,lnYBarsID],rs.AddGroup())

#rs.ObjectColor(crvID,color.DarkGoldenrod)
colRandom = lambda : color.FromArgb(rnd.randint(0,254),rnd.randint(0,254),rnd.randint(0,254))
lnYBarsID.append(crvID)
rs.AddObjectsToGroup(lnYBarsID,rs.AddGroup())
rs.ObjectColor(lnYBarsID,colRandom())



