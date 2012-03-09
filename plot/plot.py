from matplotlib import pyplot as plt
import math
from math import radians
import pymongo
from pprint import pprint
from matplotlib.transforms import Affine2D

import mpl_toolkits.axisartist.floating_axes as floating_axes
import  mpl_toolkits.axisartist.angle_helper as angle_helper
from matplotlib.projections import PolarAxes
from mpl_toolkits.axisartist.grid_finder import FixedLocator, MaxNLocator, \
     DictFormatter
def initdb():
    dbs={}
    dbs['square'] = pymongo.Connection().square
    dbs['hexbig'] = pymongo.Connection().hexbig
    dbs['hexsmall'] = pymongo.Connection().hexsmall
    dbs['hexarea'] = pymongo.Connection().hexarea
    return dbs

def closeto(x,tl=0.000001): return {'$lt':x+tl,'$gt':x-tl}
def key_cl_alg_a(cl,alg,a):return {'clus':cl,'alg':alg,'a':closeto(a)}
def sort_angle(): return [('angle',1)]
def f_Emean(x): return (x['E']['fitmu'],x['angle'])
def f_Eres(x): return (x['E']['fitstd']/x['E']['fitmu']*100,x['angle'])
def f_rmean(x): return (x['dis']['fitmu'],x['angle'])
def f_rsd(x): return (x['dis']['fitstd']/x['dis']['fitmu'],x['angle'])

def mongoplot(ax,f,cur,label,marker='',alpha=1.0):
    #f(x) should return tuple of r and theta(in radians)
    r,theta = zip(*[f(x) for x in cur])
    #print label,r[:5]
    ax.plot(theta,r,label=label,marker=marker,alpha=alpha)

#TODO: make rmin and do it correctly
def add_first_quardrant_polar(fig,rect,rmax,thetamax=90,title=""):
 
    # scale degree to radians this make the title looks really nice
    tr_scale = Affine2D().scale(math.pi/180., 1.)

    #tr = tr_rotate + tr_scale + PolarAxes.PolarTransform()
    tr = tr_scale + PolarAxes.PolarTransform()
    #tr = PolarAxes.PolarTransform()
    grid_locator1 = angle_helper.LocatorD(9)
    tick_formatter1 = angle_helper.FormatterDMS()

    grid_locator2 = MaxNLocator(10)

    ra0, ra1 = 0, thetamax
    cz0, cz1 = 0, rmax
    grid_helper = floating_axes.GridHelperCurveLinear(tr,
                                        extremes=(ra0, ra1, cz0, cz1),
                                        grid_locator1=grid_locator1,
                                        grid_locator2=grid_locator2,
                                        tick_formatter1=tick_formatter1,
                                        tick_formatter2=None,
                                        )

    ax1 = floating_axes.FloatingSubplot(fig, rect, grid_helper=grid_helper)
    ax1.grid(True)
    fig.add_subplot(ax1)

    # adjust axis
    ax1.axis["left"].set_axis_direction("bottom")
    ax1.axis["right"].set_axis_direction("top")

    ax1.axis["bottom"].set_visible(False)
    ax1.axis["top"].set_axis_direction("bottom")
    ax1.axis["top"].toggle(ticklabels=True, label=True)
    ax1.axis["top"].major_ticklabels.set_axis_direction("top")
    ax1.axis["top"].label.set_axis_direction("top")

    # create a parasite axes whose transData in RA, cz
    aux_ax = ax1.get_aux_axes(tr)

    aux_ax.patch = ax1.patch # for aux_ax to have a clip path as in ax
    ax1.patch.zorder=0.9 # but this has a side effect that the patch is
                        # drawn twice, and possibly over some other
                        # artists. So, we decrease the zorder a bit to
                        # prevent this.
    ax1.set_title(title)
    return aux_ax
    #return ax1, aux_ax

def setup_axis(fig):
    ax={}
    ax['E_mean'] = add_first_quardrant_polar(fig,221,105,90,'mean E(MeV)')
    ax['E_res'] = add_first_quardrant_polar(fig,222,4,90,'resoluiton(%)')
    ax['r_mean'] = add_first_quardrant_polar(fig,223,5,90,'Mean Shift(cm)')
    ax['r_sd'] = add_first_quardrant_polar(fig,224,0.75,90,'Shift RMS(cm)')
    return ax

def decorate_ax(ax):
    #do nothing
    pass
    
def make_legend(ax):
    ax['r_sd'].legend(loc='lower right',prop={'size':8})
    
def plot_by_det(dbs):
    for key,db in dbs.items():
        col = db.cluster_sum
        plt.rc('font',size=8)
        fig = plt.figure(figsize=(10,10))
        fig.suptitle(key,fontsize=15)
        ax=setup_axis(fig)
        alglist = col.distinct('alg')
        for cl in ['adj']:
            for alg in alglist:
                alist = col.find({'alg':alg}).distinct('a')
                for a in alist:
                    marker={'ring':'','adj':'x'}[cl]
                    alhpa={'ring':0.5,'adj':1.0}[cl]
                    cur = [ x for x in col.find(key_cl_alg_a(cl,alg,a)).sort(sort_angle()) ]
                    label = cl+'_'+alg+'_'+str(a)
                    #print key,len(cur),cl,alg,a
                    
                    mongoplot(ax['E_mean'],f_Emean,cur,label=label,marker=marker)
                    mongoplot(ax['E_res'],f_Eres,cur,label=label,marker=marker)
                    mongoplot(ax['r_mean'],f_rmean,cur,label=label,marker=marker)
                    mongoplot(ax['r_sd'],f_rsd,cur,label=label,marker=marker)
            ###
        ###
        decorate_ax(ax)
        make_legend(ax)
        fig.savefig(key+'.pdf')

def comparedet(dbs):
    plt.rc('font',size=8)
    fig = plt.figure(figsize=(10,10))
    fig.suptitle('Compare by crystal shape',fontsize=15)
    ax=setup_axis(fig)
    clus = 'adj'
    for key,db in dbs.items():
        col = db.cluster_sum
        keyy = key_cl_alg_a(clus,'log',4)
        cur = [x for x in col.find(keyy).sort(sort_angle())]
        mongoplot(ax['E_mean'],f_Emean,cur,label=key)
        mongoplot(ax['E_res'],f_Eres,cur,label=key)
        mongoplot(ax['r_mean'],f_rmean,cur,label=key)
        mongoplot(ax['r_sd'],f_rsd,cur,label=key)
    decorate_ax(ax)
    make_legend(ax)
    
    fig.savefig('bydet.pdf')
def crystalused(dbs):
    plt.rc('font',size=10)
    fig = plt.figure(figsize=(5,5))
    fig.suptitle('Number of crystal used in each geometry')
    cluses = ['adj']
    ax = add_first_quardrant_polar(fig,111,30,thetamax=90,title="") 
    for key,db in dbs.items():
        for clus in cluses:
            col = db.cluster_sum
            keyy = key_cl_alg_a(clus,'log',2)
            cur = [(x['clsize']['mean'],x['angle']) for x in col.find(keyy).sort(sort_angle())]
            r,theta = zip(*cur)
            #print r[:5]
            ax.plot(theta,r,label=clus+'_'+key)
            ax.legend(loc='lower right',prop={'size':8})
    fig.savefig('ncrystal.pdf')
    
def main():
    dbs = initdb()
    plot_by_det(dbs)
    comparedet(dbs)
    crystalused(dbs)

    

if __name__ == '__main__':
    main()