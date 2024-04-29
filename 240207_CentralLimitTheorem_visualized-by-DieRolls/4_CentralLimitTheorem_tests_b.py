import statistics as st
import random as rnd

# ---------------------------------------------------------------- VIZ UTILITIES

def plotAsTable(numLst):
    hSepStr = "---------------"
    print hSepStr
    for i,j in enumerate(numLst):
        print "| ", i+1, " | ", j, " |"
    print hSepStr
    return None


#random = rnd.random

#print(range(1,7,1))
randomChoiceFromLst = lambda : rnd.randrange(1,7,1)
#print(randomChoiceFromLst())

# 5 dice rolls & their mean
#rollCnt = 5
#meanFiveRolls = st.mean([randomChoiceFromLst() for i in range(rollCnt)])
#print(meanFiveRolls)

rollCnt = 5 # vInnerLoop
meanXRolls = lambda vOuterXloop,vInnerLoop : [st.mean([randomChoiceFromLst() for i in range(vInnerLoop)]) for x in range(vOuterXloop)]

loopedMeanLst = meanXRolls(10,5)
plotAsTable(loopedMeanLst)
