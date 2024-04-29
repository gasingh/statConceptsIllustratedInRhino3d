import statistics as st
import random as rnd

from collections import Counter
#input =  ['a', 'a', 'b', 'b', 'b']
#c = Counter( input )
#print( c.items() )


# ---------------------------------------------------------------- VIZ UTILITIES

def plotAsTable(numLst):
    hSepStr = "---------------"
    print hSepStr
    for i,j in enumerate(numLst):
        print "| ", i+1, " | ", j, " |"
    print hSepStr
    return None

#print(range(1,7,1))
randomChoiceFromLst = lambda : rnd.randrange(1,7,1)

rollCnt = 5 # vInnerLoop
meanXRolls = lambda vOuterXloop,vInnerLoop : [st.mean([randomChoiceFromLst() for i in range(vInnerLoop)]) for x in range(vOuterXloop)]

loopedMeanLst = meanXRolls(10,5)
plotAsTable(loopedMeanLst)

# PREP FOR VISUALIZING AS A HISTOGRAM FOR CLT
cntr = (Counter(loopedMeanLst))
print cntr.items()
x,y = zip(*cntr.items())
#print x
#print y
x_sorted,y_sorted = zip(*sorted(zip(x,y)))
print x_sorted
print y_sorted

# SAMPLING DISTRIBUTION PLOTTER 
#def plotAsHistogram(
#xptLst = 
