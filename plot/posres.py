import sys
import matplotlib
batchmode = '-w' not in sys.argv
matplotlib.use('Agg') if batchmode else None
from matplotlib.pyplot import figure, show, rc, grid
import plotapp
import pymongo
import numpy as np

import math

def invp(x): return 100*(1-x)

db = pymongo.Connection().crystal

summaries = db.summary.find(sort=[('angle',1)])
t = ((x['x3x3']['mean'],x['angle']) for x in summaries)
fig, ax = plotapp.radplot(t=t,label='x 3x3 linear',title='Mean Shift(cm)',subplot=121,width=14,height=7)
summaries = db.summary.find(sort=[('angle',1)])
t = ((x['y3x3']['mean'],x['angle']) for x in summaries)
plotapp.radplot(t=t,fig=fig,ax=ax,label='y 3x3 linear',ls='--')
summaries = db.summary.find(sort=[('angle',1)])
t = ((x['r3x3']['mean'],x['angle']) for x in summaries)
plotapp.radplot(t=t,fig=fig,ax=ax,label='r 3x3 linear',legendloc='lower right',ls='-.')

summaries = db.summary.find(sort=[('angle',1)])
t = ((x['x5x5']['mean'],x['angle']) for x in summaries)
plotapp.radplot(t=t,fig=fig,ax=ax,label='x 5x5 linear',color='red')
summaries = db.summary.find(sort=[('angle',1)])
t = ((x['y5x5']['mean'],x['angle']) for x in summaries)
plotapp.radplot(t=t,fig=fig,ax=ax,label='y 5x5 linear',ls='--',color='red')
summaries = db.summary.find(sort=[('angle',1)])
t = ((x['r5x5']['mean'],x['angle']) for x in summaries)
plotapp.radplot(t=t,fig=fig,ax=ax,label='r 5x5 linear',legendloc='lower right',ls='-.',color='red')

summaries = db.summary.find(sort=[('angle',1)])
t = ((x['x3x3']['sd'],x['angle']) for x in summaries)
fig, ax = plotapp.radplot(t=t,fig=fig,label='x 3x3 linear',title='RMS of Shift(cm)',subplot=122)
summaries = db.summary.find(sort=[('angle',1)])
t = ((x['y3x3']['sd'],x['angle']) for x in summaries)
plotapp.radplot(t=t,fig=fig,ax=ax,label='y 3x3 linear',ls='--')
summaries = db.summary.find(sort=[('angle',1)])
t = ((x['r3x3']['sd'],x['angle']) for x in summaries)
plotapp.radplot(t=t,fig=fig,ax=ax,label='r 3x3 linear',legendloc='lower right',ls='-.')

summaries = db.summary.find(sort=[('angle',1)])
t = ((x['x5x5']['sd'],x['angle']) for x in summaries)
plotapp.radplot(t=t,fig=fig,ax=ax,label='x 5x5 linear',color='red')
summaries = db.summary.find(sort=[('angle',1)])
t = ((x['y5x5']['sd'],x['angle']) for x in summaries)
plotapp.radplot(t=t,fig=fig,ax=ax,label='y 5x5 linear',ls='--',color='red')
summaries = db.summary.find(sort=[('angle',1)])
t = ((x['r5x5']['sd'],x['angle']) for x in summaries)
plotapp.radplot(t=t,fig=fig,ax=ax,label='r 5x5 linear',legendloc='lower right',ls='-.',color='red',write=True,display=True)

