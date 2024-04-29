import statistics as st
import random as rnd

#random = rnd.random

#print(range(1,7,1))
randomChoiceFromLst = lambda : rnd.randrange(1,7,1)
#print(randomChoiceFromLst())

# 5 dice rolls & their mean
meanFiveRolls = st.mean([randomChoiceFromLst() for i in range(5)])

print(meanFiveRolls)
