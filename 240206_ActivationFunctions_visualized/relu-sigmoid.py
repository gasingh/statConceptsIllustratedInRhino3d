"""
utility lambdas
"""
import math
import rhinoscriptsyntax as rs
import System.Drawing.Color as color
import itertools

relu = lambda v: v if v > 0 else 0
# https://www.gstatic.com/education/formulas2/553212783/en/sigmoid_function.svg
sigmoid = lambda v: 1/(1+(math.e)**(-v))

# frange in python
# https://stackoverflow.com/questions/7267226/range-for-floats
##frange = lambda vFloatStep,vJumps : [x * vFloatStep for x in range(vJumps)] # [x * .5 for x in range(10)]
frange = lambda vFloatStep,vJumps : itertools.imap(lambda x: x * vFloatStep, range(-vJumps,+vJumps,1))

#print(relu(-4))
#print(relu(1))
#print(sigmoid(55))
#print(sigmoid(-55))

multiplier = 1
ptVizLst_sG = []
ptVizLst_rL = []
ptXInput = []

x = 75
domain1 = range(-x,+x,1)
domain2 = frange(0.15,x)
#inputDomain = domain1
inputDomain = domain2
for i,j in enumerate(inputDomain):
    x_current = j
    y_current_sG = sigmoid(x_current)
    y_current_rL = relu(x_current)
    #ptVizLst.append(rs.AddPoint(x_current,y_current))
    #ptVizLst.append(rs.AddPoint(x_current,(y_current)*multiplier))
    pt_sG = rs.AddPoint(x_current,y_current_sG*multiplier)
    rs.ObjectColor(pt_sG,color.Orange)
    pt_rL = rs.AddPoint(x_current,y_current_rL*multiplier)
    rs.ObjectColor(pt_rL,color.Blue)
    
    #ptVizLst_sigmoid.append(rs.AddPoint(x_current,(y_current_sG)*multiplier))
    #ptVizLst_relu.append(rs.AddPoint(x_current,(y_current_rL)*multiplier))
    
    ptVizLst_sG.append(pt_sG)
    ptVizLst_rL.append(pt_rL)
    
    pt_Xsolo_current = rs.AddPoint(x_current,0)
    
    ptXInput.append(pt_Xsolo_current)

rs.AddObjectsToGroup(ptXInput,rs.AddGroup())
rs.AddObjectsToGroup(ptVizLst_sG,rs.AddGroup())
rs.AddObjectsToGroup(ptVizLst_rL,rs.AddGroup())
rs.AddInterpCurve(ptVizLst_sG)
#rs.AddInterpCurve(ptVizLst_rL)
rs.AddPolyline(ptVizLst_rL)
