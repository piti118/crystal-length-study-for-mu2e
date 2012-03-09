from Tkinter import *
import math
from pprint import pprint
def createhex(canvas,width,center,fill="blue",outline="black"):
  cx,cy = center
  deg30 = math.pi/6
  deg60 = math.pi/3
  r = width/math.cos(deg30)
  corners = []
  for iside in range(6):
    theta = iside*deg60+deg30
    x = cx+r*math.cos(theta)
    y = cy+r*math.sin(theta)
    corners.append((x,y))
  canvas.create_polygon(*corners,fill=fill,outline=outline)
    
class Vector(object):
  def __init__(self,x,y):
    self.x = x
    self.y = y
  def __add__(self,v): return Vector(self.x+v.x,self.y+v.y)
  def __mul__(self,n): return Vector(self.x*n,self.y*n)
  def tuple(self): return tuple(self.x,self.y)
def eadd(x,y):
  print x
  return tuple(a+b for a,b in zip(x,y))
def lk2xy(lk):
  l,k = lk
  x = (l+k)*math.cos(math.pi/3)
  y = (l-k)*math.sin(math.pi/3)
  return (x,y)
def main():
  master = Tk()
  wsize = 1000
  w = Canvas(master, width=wsize, height=wsize)
  w.pack()
  #createhex(w,50,(300,300))
  #ring 1
  color = ['red','blue','green','white'] 
  walkingvector = [
    (-1,0), #down left
    (-1,-1), #left
    (0,-1), #up left
    (1,0), #up right
    (1,1), #right
    (0,1), #down right
  ]
  #generate set of vector
  ringvec = []
  center = (0,0)
  numring = 100
  for iring in xrange(numring):
    if iring==0:
      ringvec.append([center])
      continue
    veclist = []
    prevcenter = (iring,iring)
    for iside in xrange(6):
      currentstep = walkingvector[iside]
      for iseg in xrange(iring):
        thiscenter = tuple(map(lambda x,y: x+y,prevcenter,currentstep))
        veclist.append(thiscenter)
        prevcenter = thiscenter
    ringvec.append(veclist)
  
  size = 20; gap =1
  r = 2*size+gap
  iring = 0
  #pprint(ringvec)
  for clist in ringvec:
    for center in clist:
      #print w.winfo_width()
      center = tuple(r*x+wsize/2 for x in lk2xy(center))
      createhex(w,size,center,fill=color[iring%len(color)])
    iring=iring+1
  w.update()
  w.postscript(file="circles.eps")
  
  #mainloop()
  

if __name__ == '__main__':
  main()