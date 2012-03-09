from itertools import izip
from pprint import pprint
from math import log,exp,sqrt,pi,sin,cos
from util import average
from cairoutil import draw_poly
def lk2xy(lk,scale,ltheta,ktheta):
    l,k = lk
    x = scale*(l*cos(ltheta) + k*cos(ktheta))
    y = scale*(l*sin(ltheta) + k*sin(ktheta))
    return(x,y)

def poly_corners(center,nside,width):
    #width here is the the side of largest circle inside the polygon
    cx,cy = center
    corners = []
    half_step = pi/nside
    step = 2*pi/nside
    r = width / cos(half_step)
    for iside in xrange(nside):
        theta = iside*step+half_step
        x = cx+r*cos(theta)
        y = cy+r*sin(theta)
        corners.append((x,y))
    return corners

class Shape:
    def __init__(self,n_side,ring_step, move_list, side_size, lk2xy):
        self.n_side = n_side
        self.ring_step = ring_step
        self.move_list = move_list
        self.side_size = side_size
        self.lk2xy = lk2xy
    def ring(self,ringsize,center=(0,0)):
        return ring(center, ringsize, self.move_list, self.side_size, self.ring_step)
    def lk2xy_functor(self,scale):
        return lambda x: self.lk2xy(x,scale)
    def corners(self,xycenter,width):
        return poly_corners(xycenter,self.n_side,width)
    def draw(self,ctx,xycenter,width,color,alpha):
        corners = self.corners(xycenter,width)
        return draw_poly(ctx,corners,color,alpha)
    def adj(self,center):
        ring,ringno=self.ring(1,center)
        ring.pop(0)
        return ring
hex_ring_step = (1,0)
hex_move_list = [(0,1),(-1,0),(-1,-1),(0,-1),(1,0),(1,1)]
hex_side_size = lambda x: x+1 #this measure how many step we should walk
hex_lk2xy = lambda lk,scale=1.0: lk2xy(lk,scale,pi/3,-pi/3)
HexShape = Shape(6,hex_ring_step, hex_move_list, hex_side_size, hex_lk2xy)

sq_ring_step = (1,1)
sq_move_list = [(0,-1),(-1,0),(0,1),(1,0)]
sq_side_size = lambda x: 2*x + 1
sq_lk2xy = lambda lk,scale=1.0: lk2xy(lk,scale,0,pi/2)
SquareShape = Shape(4,sq_ring_step,sq_move_list,sq_side_size,sq_lk2xy)
traverse_depth_max = 1000 # don't traverse more than this
def traverse(start,shape,f,acc=None,history=None):
    if acc is None: acc = []
    if history is None: history = set()
    #this line is mainly for first call
    history.add(start) #note for set adding duplicate will do nothing
    if f(start):
        acc.append(start)
        adjs = shape.adj(start)
        #filter out adj in history
        adjs = filter(lambda x: x not in history,adjs)
        #add all adj to history to make sure it doesn't get considered again
        for adj in adjs:
            history.add(adj)
        for adj in adjs: #for all adjacent
            if len(history)>200: raise Exception("traverse too dep")
            traverse(adj,shape,f,acc,history)
    else:
        pass
    
    return acc
    
def cluster_expansion(clist,shape,minE=0,cutoff=0.0001):
    #a more advance cluster finding algorithm where it find the bump
    #and them traverse(recursively) the adjacent crystal to find 
    #bump that is more than certain percent of the highest bump
    bump = find_bump(clist)
    #index it
    cmap = { (x['l'],x['k']):x for x in clist }
    seed = (bump['l'],bump['k'])
    ebump = bump['dedx']
    def f(lk):
        if cmap.has_key(lk):
            crys = cmap[lk]
            return crys['dedx'] > minE and crys['dedx'] > cutoff*ebump
        else:
            return False #out of bound
    ringset = set(traverse(seed,shape,f))
    toReturn = filter(lambda x: tuple([x['l'],x['k']]) in ringset,clist)
    return toReturn
    

#return list of l and k for ring size of ringsize and center at center and list of ring no
def ring(center, ringsize, move_list,side_size,ring_step):
    #ringlist = [(0,0)]
    ringlist = [center]
    ring_no_list = [0]
    for iring in xrange(1,ringsize+1):
        #build it ring by ring
        cp = tuple(iring*x+y for x,y in izip(ring_step,center))
        for step in move_list:
            #walks along move_list
            for i in xrange(1,side_size(iring)): 
                #walks only n-1 step corner is taken care off
                np = tuple(x+y for x,y in izip(step,cp))
                ringlist.append(np)
                ring_no_list.append(iring)
                cp = np
    #pprint(ringlist)
    return ringlist,ring_no_list

def hex_ring(center,ringsize):
    return ring(center,ringsize,hex_move_list,hex_side_size,hex_ring_step)

def square_ring(center,ringsize):
    return ring(center,ringsize,sq_move_list,sq_side_size,sq_ring_step)

def find_bump(clist):
    #return crystal with the highest deposited energy
    return max(clist,key=lambda x:x['dedx'])
    pass

def ring_cluster(clist,shape,ringsize=2):
    #return list of crystal to be used in cluster finding
    #this is a very simple where it find a bump and them expand around it for 2 rings
    bump = find_bump(clist) #find crystal with highest dedx
    bump_center = tuple([bump['l'],bump['k']])
    ringset = set(shape.ring(ringsize,bump_center)[0])
    #note: ignoring out of bound ring
    toReturn = filter(lambda x: tuple([x['l'],x['k']]) in ringset,clist)
    return toReturn

def sqr_pos(clist):
    xlist = (x['x'] for x in clist)
    elist = [sqrt(x['dedx']) for x in clist]
    x = average( xlist, elist )
    ylist = (y['y'] for y in clist)
    y = average( ylist, elist )
    return (x,y)
    
def lin_pos(clist):
    xlist = (x['x'] for x in clist)
    elist = [x['dedx'] for x in clist]
    x = average( xlist, elist )
    ylist = (y['y'] for y in clist)
    y = average( ylist, elist )
    return (x,y)
    
def log_pos(clist,a=4.0):
    #return tuple of x,y
    bump = find_bump(clist)
    E_bump = bump['dedx']
    E_cutoff = E_bump*exp(-1*a)
    wlist = []
    for c in clist:
        E = c['dedx']
        #this is to avoid log of 0 evaluation
        #also there are some event with energy less than 1.0
        w = 0 if E < E_cutoff or E_bump < 10.0 else a+log(E/E_bump)
        wlist.append(w)
    x = average((x['x'] for x in clist), wlist)
    y = average((y['y'] for y in clist), wlist)
    return (x,y)
    
def totalE(clist):
    return sum(c['dedx'] for c in clist)
    
def distance(a,b):
    return sqrt((a[0]-b[0])**2+(a[1]-b[1])**2) 

def in_circle((x,y),(cx,cy),r):#point in circle
  return (x-cx)**2+(y-cy)**2 < r**2

def out_circle((x,y),(cx,cy),r):
  return (x-cx)**2+(y-cy)**2 > r**2

def count_vertex_in_circle(vertices,center,r):
  return sum( (1 if in_circle(p,center,r) else 0 ) for p in vertices )

def count_vertex_out_circle(vertices,center,r):
  return sum( (1 if out_circle(p,center,r) else 0 ) for p in vertices )
