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
t = ((x['e3x3']['mean'],x['angle']) for x in summaries)
fig, ax = plotapp.radplot(t=t,label='3x3',title='Mean Energy Deposited(MeV)',subplot=131,width=21, height=7)#,rtrans=invp)
summaries = db.summary.find(sort=[('angle',1)])
t = ((x['e5x5']['mean'],x['angle']) for x in summaries)
plotapp.radplot(t=t,fig=fig,ax=ax,color='red',label='5x5')
summaries = db.summary.find(sort=[('angle',1)])
t = ((x['dedx']['mean'],x['angle']) for x in summaries)
plotapp.radplot(t=t,fig=fig,ax=ax,color='blue',label='all',legendloc='lower right')#,rtrans=invp)

summaries = db.summary.find(sort=[('angle',1)])
t = ((x['e3x3']['sd'],x['angle']) for x in summaries)
fig, ax = plotapp.radplot(t=t,fig=fig,label='3x3',title='RMS Energy Deposited(MeV)',subplot=132)#,rtrans=invp)
summaries = db.summary.find(sort=[('angle',1)])
t = ((x['e5x5']['sd'],x['angle']) for x in summaries)
plotapp.radplot(t=t,fig=fig,ax=ax,color='red',label='5x5')
summaries = db.summary.find(sort=[('angle',1)])
t = ((x['dedx']['sd'],x['angle']) for x in summaries)
plotapp.radplot(t=t,fig=fig,ax=ax,color='blue',label='all',legendloc='lower right')

summaries = db.summary.find(sort=[('angle',1)])
t = ((x['e3x3']['res'],x['angle']) for x in summaries)
fig, ax = plotapp.radplot(t=t,fig=fig,label='3x3',title='1-Energy Resolution(%)',subplot=133,rtrans=invp)
summaries = db.summary.find(sort=[('angle',1)])
t = ((x['e5x5']['res'],x['angle']) for x in summaries)
plotapp.radplot(t=t,fig=fig,ax=ax,color='red',label='5x5',rtrans=invp)
summaries = db.summary.find(sort=[('angle',1)])
t = ((x['dedx']['res'],x['angle']) for x in summaries)
plotapp.radplot(t=t,fig=fig,ax=ax,color='blue',label='all',legendloc='lower right',write=True,display=True,rtrans=invp)