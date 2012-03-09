import matplotlib
from matplotlib.pyplot import figure, show, rc, grid, savefig, ion
import inspect
import os.path
import sys
import math
from pprint import pprint
def radplot(t=None,r=None,theta=None,degree=True,title=None,label=None,color='#ee8d18',
            maxr=None,rtrans=None,thetatrans=None,subplot=None,
            batchmode=None,display=False,
            output=None,fig=None,ax=None,write=False,
            legendloc=None,width=None,height=None,unit=None,ls=None,
            *arg,**kwarg):
  # radar green, solid grid lines
  if output is None: output =  os.path.splitext(inspect.stack()[-1][1])[0]+'.png'
  batchmode = batchmode if batchmode is not None else '-w' not in sys.argv
  if r is None and theta is None:
    r,theta = zip(*t)
  #transform and convert to radian if necessary
  if rtrans: r = map(rtrans,r)
  if thetatrans: theta = map(thetatrans,theta)
  def d2r(d): return d/180.0*math.pi
  if degree: theta = map(d2r,theta)

  fwidth, fheight = matplotlib.rcParams['figure.figsize']
  width = width or fwidth
  height = height or fheight
  # force square figure and square axes looks better for polar, IMO
  # make a square figure
  fig = fig or figure(figsize=(width, height))
  if ax is None:
    #ax = fig.add_axes([0.1, 0.1, 0.8, 0.8], polar=True, axisbg='#d5de9c')
    ax = fig.add_subplot(subplot or 111, polar=True, axisbg='#d5de9c')
    ax.set_rmax(maxr or 1.05*max(r))
    ax.grid(True,label=unit or '')
    ax.set_title(title or '', fontsize=20)
    #rc('xtick', labelsize=10)
    #rc('ytick', labelsize=10)
  ls = ls or '-'
  ax.plot(theta, r, color=color, lw=2,label=label,ls=ls)
  if label: ax.legend(loc=legendloc or 0)  
  if write: 
    print 'Writing '+output
    savefig(output) 
  show() if not batchmode and display else None
  return (fig,ax)