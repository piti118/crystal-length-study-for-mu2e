import cairo
import math
class unit:
 cm = 50*2/3 #point/cm

def hexcorners(center,width):
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
  return corners

def drawhex(ctx,center,width,color=(0,0,1.0),alpha=0.75):
  corners = hexcorners(center,width)
  ctx.move_to(*corners[-1])
  for corner in corners:
    ctx.line_to(*corner)
  ctx.close_path()
  ctx.set_source_rgba(0,0,0,alpha)
  ctx.set_line_width(2)
  ctx.stroke_preserve()
  color=color+tuple([alpha])
  ctx.set_source_rgba(*color)
  ctx.fill()
  return corners

def drawcircle(ctx,center,r,color=(1.0,0,0)):
  ctx.set_source_rgb(*color)
  ctx.arc(center[0],center[1],r,0,2*math.pi)
  ctx.close_path()
  ctx.stroke()

def in_circle((x,y),(cx,cy),r):#point in circle
  return (x-cx)**2+(y-cy)**2 < r**2

def out_circle((x,y),(cx,cy),r):
  return (x-cx)**2+(y-cy)**2 > r**2

def count_vertex_in_circle(vertices,center,r):
  return sum( (1 if in_circle(p,center,r) else 0 ) for p in vertices )

def count_vertex_out_circle(vertices,center,r):
  return sum( (1 if out_circle(p,center,r) else 0 ) for p in vertices )


def hexlist(numring):#todo: make this a generator
  walkingvector = [
    (-1,0), #down left
    (-1,-1), #left
    (0,-1), #up left
    (1,0), #up right
    (1,1), #right
    (0,1), #down right
  ]
  print numring
  #generate set of vector
  ringvec = []
  center = (0,0)
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
  return ringvec

def lk2xy(lk):
  l,k = lk
  x = (l+k)*math.cos(math.pi/3)
  y = (l-k)*math.sin(math.pi/3)
  return (x,y)

def dohex(cornerreq=4,output='hex',innerradius =36*unit.cm,outterradius=60*unit.cm,crystalradius=1.5*unit.cm):
  numring = 30
  ssize = 6200
  surface = cairo.PDFSurface(output+'.pdf',ssize,ssize)
  #surface = cairo.PSSurface(output+'.eps',ssize,ssize)
  #surface.set_eps(True)
  #surface = cairo.SVGSurface(output+'.svg',ssize,ssize)
  ctx = cairo.Context(surface)
  
  center = (ssize/2,ssize/2)
  hlist = hexlist(numring)
  hexsize = 1.5*unit.cm;gap = 0.001*unit.cm
  r = 2*hexsize+gap
  
  color = [tuple([1-(x+1)*0.02])*3 for x in xrange(10)]
  iring = 0
  innerradius = 36*unit.cm
  outerradius = 70*unit.cm
  
  numcrys = 0
  
  for clist in hlist:
    for c in clist:

      newc = tuple((r*x)+cx for x,cx in zip(lk2xy(c),center))

      thiscolor = (0,0.86,0) if iring%2==0 else (0,1,0)
      thiscolor = (0,0.74,0) if iring%10==0 else thiscolor

      #print newc
      corners = hexcorners(newc,hexsize)
      num_out_circle = count_vertex_out_circle(corners,center,innerradius)
      num_in_circle = count_vertex_in_circle(corners,center,outerradius)
      inside_ring =  num_out_circle >= cornerreq and num_in_circle >= cornerreq 
      alpha = 1.0 if inside_ring else 0.08
      if inside_ring: numcrys+=1
      drawhex(ctx,newc,hexsize,color=thiscolor,alpha=alpha)

    iring=iring+1
  
  drawcircle(ctx,center,36*unit.cm)
  drawcircle(ctx,center,70*unit.cm)
  drawcircle(ctx,center,60*unit.cm)  
  
  ctx.move_to(0.8*ssize,0.2*ssize)
  ctx.set_source_rgb(0,0,1)
  ctx.set_font_size(150)
  ctx.show_text(str(numcrys))
  #draw circles
  # for i in xrange(50):
  #     ctx.set_source_rgb(1.0,0,0)
  #     ctx.arc(center[0],center[1],2*r*i,0,2*math.pi)
  #     ctx.stroke()
  surface.finish()

def main():
  for i in xrange(5):
    hl = hexlist(i)
    print[len(x) for x in hl]
  print [1+x*(x+1)/2*6 for x in xrange(5)]
  # innerradius = 36*unit.cm
  # smallouterradius = 60*unit.cm
  # bigoutterradius = 70*unit.cm
  # 
  # crystalwidthinner = 1.5*unit.cm
  # crystalwidtharea = 3.22/2*unit.cm
  # crystalwidthouter = 1.5*math.cos(math.pi/6) 
  # 
  # for i in range(6):
  #   dohex(i+1,'hexbig-'+str(i)) 

if __name__ == '__main__':
  main()