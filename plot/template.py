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
summaries = db.summary.find()
t = ((x['x3x3']['mean'],x['angle']) for x in summaries)
fig, ax = plotapp.radplot(t=t,write=False,display=False,label='xres')#,rtrans=invp)
summaries = db.summary.find()
t = ((x['y3x3']['mean'],x['angle']) for x in summaries)
plotapp.radplot(t=t,fig=fig,ax=ax,write=False,display=False,color='red',label='yres')#,rtrans=invp)
summaries = db.summary.find()
t = ((x['r3x3']['mean'],x['angle']) for x in summaries)
plotapp.radplot(t=t,fig=fig,ax=ax,color='blue',label='rres')#,rtrans=invp)