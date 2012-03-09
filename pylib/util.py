from pprint import pprint
from math import sqrt, floor
from itertools import izip,repeat,imap

class Struct:
    def __init__(self, **entries): 
        self.__dict__.update(entries)

class Stat:
    def __init__(self,n,s,s2):
        self.n = n
        self.sum = s
        self.sumsq = s2
        self.mean = s*1.0/n
        self.sqmean = s2*1.0/n
        self.var = self.sqmean-self.mean**2
        self.sd = sqrt(self.var)
        self.res = self.sd/self.mean if self.mean!=0 else -1
    
    def tomap(self):
        return self.__dict__
  
    @staticmethod
    def statmap(n,s,s2):
        return Stat(n,s,s2).__dict__

def cleanup_for_file_name(s):
    return "".join([x for x in s if x.isalpha() or x.isdigit()])

def eadd(x,y):#element wise add for iterable
    if x is None: x = (0,)*len(y)
    return tuple(a+b for (a,b) in izip(x,y))

def teadd(x,y):#tuple of tutple elementwise add
    if x is None: x = (None,)*len(y)
    return tuple(eadd(a,b) for (a,b) in izip(x,y))

def deadd(x,y):#dictionary elementwise add of tuple
    if x is None: x = dict( (key,None) for key in y.keys())
    return dict( (key,eadd(x[key],y[key]) ) for key in y.keys() )

def dstat(it):#stat for dictionary
    #assume key are the same
    result = reduce(lambda x,y: deadd(x, dict( (key,(1,val,val**2)) for key,val in y.items())) , it, None )
    return dict((key,Stat.statmap(*val)) for key,val in result.items())
  
def tstat(it):#stat for generator of tuple of values
    result = reduce(lambda x,y: teadd(x, tuple((1,z,z**2) for z in y) ), it, None )
    toReturn = tuple(Stat(n,s,s2) for (n,s,s2) in result) #n+1 because eadd start at 0 not 1
    return toReturn
  
def stat(it):
    (n,s,s2) = reduce(lambda x,y: eadd(x,(1,y,y**2)), it, None)
    o = Stat(n,s,s2)
    return o    

def statmap(it):
    return stat(it).tomap()

def average(xlist,wlist):
    swx = sum(x*w for x,w in izip(xlist,wlist))
    sw = sum(w for w in wlist)
    return swx/sw if sw!=0 else 0
