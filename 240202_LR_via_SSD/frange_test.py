import itertools

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



print frange(0,300,1000)