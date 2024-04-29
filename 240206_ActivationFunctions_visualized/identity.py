"""
utility lambdas
"""
import math
import rhinoscriptsyntax as rs
import System.Drawing.Color as color
import itertools

# f(x) = x, this is the identity function
identity = lambda v: v

binary = lambda v: 1 if v > 0 else 0

tanh = lambda v: math.tanh(v)

relu = lambda v: v if v > 0 else 0
# https://www.gstatic.com/education/formulas2/553212783/en/sigmoid_function.svg
sigmoid = lambda v: 1/(1+(math.e)**(-v))

# frange in python
# https://stackoverflow.com/questions/7267226/range-for-floats
frange = lambda vFloatStep,vJumps : itertools.imap(lambda x: x * vFloatStep, range(-vJumps,+vJumps,1))

multiplier = 1
ptVizLst_Func = []
ptXInput = []

x = 75
domain1 = range(-x,+x,1)
domain2 = frange(0.15,x)
#inputDomain = domain1
inputDomain = domain2
for i,j in enumerate(inputDomain):
    x_current = j
    y_current = identity(x_current)
    pt_Func = rs.AddPoint(x_current,y_current*multiplier)
    rs.ObjectColor(pt_Func,color.Red)
    
    ptVizLst_Func.append(pt_Func)
    
    # default input data along X-axis
    pt_Xsolo_current = rs.AddPoint(x_current,0)
    ptXInput.append(pt_Xsolo_current)

rs.AddObjectsToGroup(ptVizLst_Func,rs.AddGroup())
rs.AddObjectsToGroup(ptXInput,rs.AddGroup())

#rs.AddPolyline(ptVizLst_rL)
rs.AddInterpCurve(ptVizLst_Func)
