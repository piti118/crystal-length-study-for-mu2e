import clusterutil as cu
from cairoutil import unit
import cairoutil
import cairo
from util import Struct
from pprint import pprint
from itertools import imap,izip
from matplotlib import pyplot as plt
import util
def count_in_disc(r_in, r_out, lklist, shape, width, gap, offset=(0.,0.)):
    scale = 2*width+gap
    def in_ring(lkpos):
        xypos = shape.lk2xy(lkpos,scale)
        corners = shape.corners(xypos,width)
        out_inner_ring = cu.count_vertex_out_circle(corners,offset,r_in)
        in_outer_ring = cu.count_vertex_in_circle(corners,offset,r_out)
        return (out_inner_ring,in_outer_ring)
    return map(in_ring,lklist)

def draw_ring(ctx, shape, width, gap, nring=30):
    lklist, ringno = shape.ring(nring)
    lk2xy = shape.lk2xy_functor(2*width+gap)
    xylist = map(lk2xy,lklist)
    for xy in xylist:
        #pprint(xy)
        shape.draw(ctx,xy,width)

def pass_side_req(n_in_disc,side_req):
    return n_in_disc[0] >= side_req and n_in_disc[1] >= side_req

def autolabel(ax,rects,numbers,format='%d'):
    # attach some text labels
    for rect,number in izip(rects,numbers):
        x=rect.get_x()
        y=rect.get_y()
        h = rect.get_height()
        w = rect.get_width()
        ax.text( x+w+20,y+h/2, format%number,
                ha='left', va='center')

def make_summary_plot(name,summary_list):
    summary_list = map(lambda x: Struct(**x),summary_list)#make the code easier to read
    def extract(i,x):
        bottom = 2*i+1
        data = x.n
        label = x.cname +'-'+ x.req
        color = x.color
        return (bottom,data,label,color)
    bottom, data, label, color = zip(*[ extract(i,x) for i,x in enumerate(summary_list) ])  
    fig = plt.figure()
    #ax = fig.add_subplot(111,xmargin=0.5)
    ax = fig.add_axes([0.2,0.05,0.7,0.9])
    ax.set_title('Number of Crystals used in '+name)
    rects = ax.barh(bottom,data,height=1.0,color=color,align='center')
    ax.set_yticks(bottom)
    ax.set_yticklabels(label)
    ax.set_ylim(top = max(bottom)+2)
    ax.set_xlim(right=1.10*max(data))
    ax.grid(True)
    autolabel(ax,rects,data)
    fig.savefig(util.cleanup_for_file_name(name)+'.pdf')

def centroid_in_disc(xy,c,r_in,r_out):
    return cu.in_circle(xy,c,r_out) and cu.out_circle(xy,c,r_in)

def pass_n_vertex_functor(nvertex):
    def f(xy,n_in_disc_cache):
        return pass_side_req(n_in_disc_cache,nvertex)
    return f

def controid_in_disc_functor(c,r_in,r_out):
    return lambda xy,n: centroid_in_disc(xy,c,r_in,r_out)

def make_alg_list(config,disc):
    alglist = [ ('vertex'+str(i),pass_n_vertex_functor(i)) for i in xrange(1,config.shape.n_side+1) ]
    alglist.append(('centroid',controid_in_disc_functor((0,0),disc.r_in,disc.r_out)))
    return alglist
    
def main():
    square = Struct(name='square',shape=cu.SquareShape,width=1.5*unit.cm,gap=0.1*unit.mm,nring=30,color='#E3319D')
    hexbig = Struct(name='hexbig',shape=cu.HexShape,width=1.5*unit.cm,gap=0.1*unit.mm,nring=30,color='#736AFF')
    hexsmall = Struct(name='hexsmall',shape=cu.HexShape,width=1.3*unit.cm,gap=0.1*unit.mm,nring=35,color='#7E2217')
    hexarea = Struct(name='hexarea',shape=cu.HexShape,width=1.612*unit.cm,gap=0.1*unit.mm,nring=35,color='#387C44')
    
    bigdisc = Struct(name='bigdisc',r_in=36*unit.cm,r_out=70*unit.cm)
    smalldisc = Struct(name='smalldisc',r_in=36*unit.cm,r_out=60*unit.cm)
    
    c_size = 6200
    
    summary = {'bigdisc':[],'smalldisc':[]}
    for config in [square,hexarea,hexbig,hexsmall]:#crystal dimension
        lk_list, ring_no_list = config.shape.ring(config.nring)
        for disc in [bigdisc,smalldisc]:#disc
            n_in_disc_list = count_in_disc(disc.r_in,disc.r_out,
                                        lk_list,
                                        config.shape,config.width,config.gap)
            alglist = make_alg_list(config,disc)
            for req_name, pass_req in alglist:
                fname = config.name+'_'+disc.name+'_'+req_name+'.pdf'
                surface = cairo.PDFSurface(fname,c_size,c_size)
                surface.set_device_offset(c_size/2,c_size/2) #center at 0,0
                ctx = cairo.Context(surface)
                lk2xy = config.shape.lk2xy_functor(2*config.width+config.gap)
                xy_list = map(lk2xy,lk_list)
                for xy,rno,n_in_disc in izip(xy_list,ring_no_list,n_in_disc_list):
                    #full opacity if pass requirement in disc 0.25 otherwise
                    #if rno > 20 and rno%10==0 : pprint((xy,rno,n_in_disc))
                    alpha = 1.0 if pass_req(xy,n_in_disc) else 0.05
                    color = (0,1.0,0) if rno%2==1 else (0,0.8,0)
                    color = (0,0.6,0) if rno%10==0 else color
                    if rno==0:#show the center
                        color =(0,0,1.0)
                        alpha =1.0
                    config.shape.draw(ctx,xy,config.width,color,alpha)
                n_crystal_in_ring = sum(( (1 if pass_req(xy,n) else 0) for xy,n in izip(xy_list,n_in_disc_list)))
                
                cairoutil.draw_circle(ctx, (0,0), disc.r_in)
                cairoutil.draw_circle(ctx, (0,0), disc.r_out)
                
                ctx.set_font_size(100)
                ctx.set_source_rgba(0,0,0,1)
                ctx.move_to(c_size/2*0.5,-c_size/2*0.7)
                ctx.show_text(config.name+' '+disc.name+' '+req_name+' : '+str(n_crystal_in_ring))
                ctx.stroke()
                
                ctx.move_to(0,0)
                ctx.line_to(1.5*unit.cm,0)
                ctx.stroke()
                this_summary = {'n':n_crystal_in_ring,'cname':config.name,'req':req_name,'color':config.color}
                summary[disc.name].append(this_summary)
                print "Writing "+fname
                surface.finish()
            ##side_req
        ##disc
    ##config
    make_summary_plot('big disc',summary['bigdisc'])
    make_summary_plot('small disc',summary['smalldisc'])                
if __name__ == '__main__':
  main()