# -*- coding: utf-8 -*-
# <nbformat>3</nbformat>

# <codecell>

from root_numpy import *
from dist_fit import *
from cithep import *
from h5py import *
sample='air'

# <codecell>

class Hitmap:
    def __init__(self,numrow=21,numcol=21):
        self.hmap = np.zeros([numrow,numcol])
        self.numrow = numrow
        self.numcol = numcol
    def acc(self,l,k,E):
        i,j = self.lk2ij(l,k)
        self.hmap[i,j]+=E
    def lk2ij(self, l,k):
        return l+self.numcol/2,k+self.numrow/2
    def sumE(self,cutoff=None):
        if cutoff is not None:
            return np.sum(np.sum(self.hmap[self.hmap>cutoff]))
        else:
            return np.sum(np.sum(self.hmap))

# <codecell>

hitmap = root2array('%s.root'%sample,'hitmap')
einfo = root2array('%s.root'%sample,'eventinfo')

# <codecell>


# <codecell>

laster = tuple()
thishit = None
result = np.array([],dtype=[('angle',np.double),('E',np.double)])

for hit in hitmap:
    runno = hit['runno']
    eventno = hit['eventno']
    if (runno,eventno) != laster and laster != tuple(): 
        result.resize(len(result)+1)
        result[-1]['angle'] = laster[0]*5.
        result[-1]['E'] = thishit.sumE()
        thishit=None
    laster = (runno,eventno)
    if thishit is None:
        thishit = Hitmap()
    thishit.acc(hit['l'],hit['k'],hit['E'])

if thishit is not None:
    result.resize(len(result)+1)
    result[-1]['angle'] = laster[0]*5.
    result[-1]['E'] = thishit.sumE()
    thishit=None #take care of the last one

# <codecell>

f = File('%s.hdf5'%sample,'w')
f.create_dataset('result',data=result)
f.close()

# <codecell>

f = File('%s.hdf5'%sample,'r')
tmp = f['result']
result = np.array(tmp)
f.close()

# <codecell>

def my_gau(x,g_mu,g_sigma):
    return gaussian(x,g_mu,g_sigma)

# <codecell>

def smear(E):
    w = sqrt(1000.*E)#1000 photon per mev
    ret = randn(len(E))
    ret*=w/1000.
    ret+=E
    return ret

def doOneFit(E,range=(95.,110.),mean=104.,sigma=1.,n=20.,alpha=0.5,N=80000,
        limit_N=(1000,100000),limit_n=(0.1,100.), limit_mean=(90,106), limit_sigma=(0.3,5.),limit_alpha=(0.,5.)):
    #eg = Add2Pdf(my_gau,Normalize(crystalball,range))
    #describe(eg)
    #eg = Normalize(crystalball,range)
    eg = Convolve(Normalize(crystalball,range),my_gau,(-2,2),nbins=40)
    #eeg = eg
    eeg = Extend(eg) 
    print describe(eeg)
    #fit, m = fit_uml(eg,sm,mean=104.5,sigma=1.,n=20.,alpha=0.5, limit_n=(0.1,50.), limit_mean=(90,106), limit_sigma=(0.3,5.),limit_alpha=(0.,2.))
    #try_uml(eg,sm,mean=104.,sigma=1.,n=50.,alpha=0.5)
    fit,m = None,None
    good = False
    itry = 0
    first = True

    while not good and itry<5:
        try:
            if not first:
                mean = 104.5+randn(1)*2.
                alpha=0.5+randn(1)*0.2
            first =False
            fit,m = fit_binpoisson(eeg,E,maxcalls=200000,bins=100,
                        mean=mean,sigma=sigma,n=n,alpha=alpha,N=N,g_mu=0.,g_sigma=0.3,
                        limit_N=limit_N,limit_n=limit_n, limit_mean=limit_mean, limit_sigma=limit_sigma,limit_alpha=limit_alpha,
                        limit_g_mu=(-1,1),limit_g_sigma=(0.001,0.5),
                        quiet=False,throw=False)
            good = True
        except Exception as e:
            print e
            #raise e
            itry+=1
    fit.draw(m)
    l,h = fwhm_f(eeg,range,m.args)
    print m.values
    vertical_highlight(l,h)
    return fit,m,h,l,eeg

# <codecell>

angles = np.linspace(0,90,19)[:-1]
myresult = {}

# <codecell>

arg = {
      0 :{'range':(96.,105.5)},
      1 :{'range':(96.,105.5)},
      2 :{'range':(96.,105.5)},
      3 :{'range':(96.,105.5)},
      4 :{'range':(96.,105.5)},
      5 :{'range':(96.,105.5)},
      6 :{'range':(96.,105.5)},
      7 :{'range':(96.,105.5)},
      8 :{'range':(96.,105.5)},
      9 :{'range':(96.,105.5)},
            
      10:{'range':(96.,105.5)},
      11:{'range':(96.,105.5)},
      12:{'range':(90.,105.5)},
      13:{'range':(90.,105.5)},
      14:{'range':(90.,105.5)},
      15:{'range':(90.,105.5)},
      16:{'range':(80.,105.5)},
      17:{'range':(80.,105.5)},
}
for i,angle in enumerate(angles):
    #if i < 17: continue
    myE = result['E'][(result['angle']>(angle-0.1)) & (result['angle']<(angle+0.1))]
    figure()
    myE = smear(myE)
    emin,emax = 101.,105.5
    if i in arg:
        emin,emax = arg[i]['range']
    myE = myE[(myE>emin) & (myE<emax)]
    myresult[i] = doOneFit(myE,range=(emin,emax),N=len(myE))
    title(str(angle)+' '+str(i))

# <codecell>

#make and save the plot
def make_nice_plot(r):
    fig,axs = subplots(3,3,figsize=(20,12))
    for i in r:
        ii = i%9
        row = ii/3
        col = ii%3
        fit = myresult[i][0]
        m = myresult[i][1]
        fh,fl = myresult[i][2],myresult[i][3]
        fwhm_res = (fh-fl)/2.35
        ax=axs[row,col]
        sca(ax)
        fit.draw(m)
        vertical_highlight(fl,fh)
        title('%s %d deg'%(sample,5*i))
        text(0.5,0.2,r'fwhm/2.35=%3.2f'%(fwhm_res),transform = ax.transAxes)
make_nice_plot(range(9))
savefig('%s_1.pdf'%sample,bbox_inches='tight')
make_nice_plot(range(9,18))
savefig('%s_2.pdf'%sample,bbox_inches='tight')

# <codecell>

fwhm = np.zeros(18)
for i in range(18):  fwhm[i]=(myresult[i][2]-myresult[i][3])/2.35
np.save('fwhm_%s.npy'%sample,fwhm)
x = np.array(range(18))*5.
plot(x,fwhm,'xb')

# <codecell>

hist(result['E'],bins=100,range=(100,110),histtype='step');,

# <codecell>

a = numpy.array([],dtype=[('a',np.double)])
a
a.resize(len(a)+1)
a.resize(len(a)+1)
a

# <codecell>

gdf = df.groupby(['runno','eventno'])

# <codecell>

for k,v in gdf:
    h = Hitmap(10,10)
    for i in xrange(len(v)):
        h.acc(v.l[i],v.k[i],v.E[i])
    print h.hmap
    print h.sumE()
    break

# <codecell>


h = Hitmap(10,10)

# <codecell>

for x in hmap:
    

# <codecell>


