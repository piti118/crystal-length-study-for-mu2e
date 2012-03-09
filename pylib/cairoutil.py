import cairo
import math
from math import sin, cos, sqrt,pi
class unit:
 cm = 50*2/3 #point/cm
 mm = 50*2/3/19 #point/mm

def square_corners(center,width):
    #width here is half length of side
    #which is the same as radius of largest circle inside the square
    return poly_corners(center,4,width)

def hex_corners(center,width):
    #width here is the radius of the largest circle inside the hex
   return poly_corners(center,6,width)

def draw_poly(ctx,corners,color=(0,1.0,0),alpha=0.75):
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

def draw_square(ctx,center,width,color=(0,0,1.0),alpha=0.75):
    corners = square_corners(center,width)
    return dray_poly(ctx,corners,color,alpha)
def drawhex(ctx,center,width,color=(0,0,1.0),alpha=0.75):
    corners = hexcorners(center,width)
    return draw_poly(ctx,corners,color,alpha)

def draw_circle(ctx,center,r,color=(1.0,0,0)):
    ctx.set_source_rgb(*color)
    ctx.arc(center[0],center[1],r,0,2*math.pi)
    ctx.close_path()
    ctx.stroke()

