"""
utility lambdas
"""
import math
import rhinoscriptsyntax as rs
import System.Drawing.Color as color
import itertools

binary = lambda v: 1 if v > 0 else 0

tanh = lambda v: math.tanh(v)

relu = lambda v: v if v > 0 else 0
# https://www.gstatic.com/education/formulas2/553212783/en/sigmoid_function.svg
sigmoid = lambda v: 1/(1+(math.e)**(-v))

# frange in python
# https://stackoverflow.com/questions/7267226/range-for-floats
frange = lambda vFloatStep,vJumps : itertools.imap(lambda x: x * vFloatStep, range(-vJumps,+vJumps,1))

multiplier = 1
ptVizLst_sG = []
ptVizLst_rL = []
ptVizLst_tH = []
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
    y_current_tH = tanh(x_current)
    
    #pt_sG = rs.AddPoint(x_current,y_current_sG*multiplier)
    #rs.ObjectColor(pt_sG,color.Orange)
    #pt_rL = rs.AddPoint(x_current,y_current_rL*multiplier)
    #rs.ObjectColor(pt_rL,color.Blue)
    
    pt_tH = rs.AddPoint(x_current,y_current_tH*multiplier)
    rs.ObjectColor(pt_tH,color.Pink)
    
    
    #ptVizLst_sG.append(pt_sG)
    #ptVizLst_rL.append(pt_rL)
    ptVizLst_tH.append(pt_tH)
    
    # default input data along X-axis
    pt_Xsolo_current = rs.AddPoint(x_current,0)
    ptXInput.append(pt_Xsolo_current)

#rs.AddObjectsToGroup(ptVizLst_sG,rs.AddGroup())
#rs.AddObjectsToGroup(ptVizLst_rL,rs.AddGroup())
rs.AddObjectsToGroup(ptVizLst_tH,rs.AddGroup())
rs.AddObjectsToGroup(ptXInput,rs.AddGroup())

#rs.AddInterpCurve(ptVizLst_sG)
#rs.AddPolyline(ptVizLst_rL)
rs.AddInterpCurve(ptVizLst_tH)