import numpy as np
import numpy.random
import scipy.stats
from pprint import pprint
import minuit
import inspect
import decorator
import scipy.integrate
import random
from pymongo import Connection
from math import exp,pow
#f is a functor where f(a1,a2)(x) is the value
def makenll(data,f,range_=None):
    umax,umin = range_ or (data.max(),data.min())
    def nll(f,*args,**kwd):
        pdf = f(*args)
        norm = scipy.integrate.quad(pdf,umin,umax)[0]
        vpdf = np.vectorize(pdf)
        pdfval = vpdf(data)/norm
        sum_nll = -1*np.sum(np.log(pdfval))
        return sum_nll
    return decorator.decorator(nll,f)
#maximum likelihood fit
#return (mu,sigma)
def fitgauss(data,mu=None,sigma=None,range_=None):
    if mu is None: mu = data.mean()
    if sigma is None: sigma = data.std()
    def gauss_functor(mu,sigma):
        f = scipy.stats.norm(loc=mu,scale=sigma)
        return f.pdf
    nll = makenll(data,gauss_functor,range_)
    m = minuit.Minuit(nll,mu=mu,sigma=sigma)
    m.migrad()
    m.minos()
    toReturn = m.values["mu"],m.values['sigma']   
    print m.errors
    print m.values
    return toReturn

#optimized chi^2 fit
def fitgaussx2(data,nbins=50,mu=None,sigma=None,range_=None,errors=None):
    if mu is None: mu = data.mean()
    if sigma is None: sigma = data.std()
    N = data.size
    if range_ is None: range_=(data.min(),data.max())
    umin = range_[0]
    umax = range_[1]
    hist,edges = np.histogram(data,bins=nbins)
    err = np.sqrt(hist)
    err = err[hist>1]
    def chi2(mu,sigma):
        
        scipy.stats.norm()
        f = scipy.stats.norm(loc=mu,scale=sigma)
        cdfs = f.cdf(edges) #do the piecewise integral
        expected = N*np.diff(cdfs)/(cdfs[-1]-cdfs[0]) #renormalized
        delta = hist-expected
        #hist_for_error = np.copy(hist)#flip all 0 to 1
        #hist_for_error[hist<0.5] = 1
        delta = delta[hist>1]
        
        x2 = np.sum((delta/err)**2)/(nbins-2) #x^2/ndof
        #print x2
        return x2
    #m.printMode = 1
    #m.up = 1
    
    toReturn = None
    fail = True
    ntry = 0
    maxtry = 30
    newmu = mu
    newsigma = sigma
    while fail and ntry < maxtry :
        m = minuit.Minuit(chi2,mu=newmu,sigma=newsigma,errors=errors,limit_mu=(-1.0,5.0),limit_sigma=(0.5,20.0))
        m.strategy = 2
        fail = False
        try:
            m.migrad()
            m.hesse()
        except minuit.MinuitError as me:
            fail=True

        if m.fval>30.0: 
            print 'fval: ',m.fval
            fail=True
        if fail:
            newmu = random.uniform(-1.0,5.0)
            newsigma=random.uniform(0.0,10.0)
            print 'Minuit fail try again',ntry,newmu,m.fval,m.values["mu"],m.values['sigma']
            ntry += 1
        toReturn = m.values["mu"],m.values['sigma']
    
    #assert(not fail)
    #print m.errors
    #print m.values
    return m
#crystalball function
def cball(x,alpha,n,mu,sigma):
    ret = 0
    if (x-mu)/sigma > -alpha:
        ret = exp(-(x-mu)**2/2.0/sigma**2)
    else:
        A = pow(abs(alpha)/n,-n)*exp(-alpha**2/2.0)
        B = n/abs(alpha)-abs(alpha)
        ret = A*pow(B-(x-mu)/sigma,-n)
    return ret

def normcball(edges,alpha,n,mu,sigma):
    vcball = np.vectorize(cball)
    ret = vcball(edges,alpha,n,mu,sigma)
    cdf = cballcdf(alpha,n,mu,sigma,edges)
    ret/=(cdf[-1]-cdf[0])
    return ret

#unnormalized cdf    
def cballcdf(alpha, n, mu,sigma,edges):
    start = 0
    #print len(edges)
    ret = np.zeros(len(edges))
    cdf = 0.0
    def cballwrapper(x):
        return cball(x,alpha,n,mu,sigma)
    vcball = np.vectorize(cballwrapper)
    val = vcball(edges)
    
    for i,x in enumerate(val):
        thisblock = 0
        if i==0:
            pass
        else:
            thisblock = 0.5*(val[i-1]+val[i])*(edges[i]-edges[i-1])
        cdf += thisblock
        ret[i]=cdf
    return ret
    
    
def fitcballx2(data,nbins=50,alpha=None,n=None,mu=None,sigma=None,range_=None,errors=None):
    

    if mu is None: mu = data.mean()
    if sigma is None: sigma = data.std()
    if n is None: n = 0.5
    if alpha is None: alpha = 1.0
    N = data.size
    if range_ is None: range_=(data.min(),data.max())
    umin = range_[0]
    umax = range_[1]
    hist,edges = np.histogram(data,bins=nbins)
    vcball = np.vectorize(cball)
    def chi2(alpha,n,mu,sigma):
        #print (alpha,n,mu,sigma)
        pdf = vcball(edges,alpha,n,mu,sigma)
        cdfs = cballcdf(alpha,n,mu,sigma,edges)
        expected = N*np.diff(cdfs)/(cdfs[-1]-cdfs[0]) #renormalized
        delta = hist-expected
        hist_for_error = np.copy(hist)#flip all 0 to 1
        hist_for_error[hist<0.5] = 1
        err = np.sqrt(hist_for_error)
        x2 = np.sum((delta/err)**2)/(nbins-2) #x^2/ndof
        #print x2
        return x2
    #m.printMode = 1
    #m.up = 1

    toReturn = None
    fail = True
    ntry = 0
    maxtry = 20
    newmu = mu
    while fail and ntry < maxtry :
        m = minuit.Minuit(chi2,alpha=alpha,n=n,mu=newmu,sigma=sigma,errors=errors,
            limit_alpha=(0.05,8.0),limit_n=(1.0,50.0),limit_sigma=(1.0,50.0),limit_mu=(80,105))
        m.printMode = 1
        m.strategy = 2
        fail = False
        try:
            m.migrad()
            m.hesse()
        except minuit.MinuitError as me:
            fail=True
        if m.fval >5: fail=True#bad one too much chi^2
        if fail:
            newmu = random.uniform(data.min(),data.max())
            #print 'Minuit fail try again',ntry,newmu,m.fval,m.values["mu"],m.values['sigma']
            ntry += 1
            pass
    #assert(not fail)
        #toReturn = m.values

    #print m.errors
    #print m.values
    return m

def fitandshow(data,mu=None,sigma=None):
    import pylab
    usedata = data
    mu,sigma = fitgaussx2(usedata,mu=mu,sigma=sigma)
    print mu,sigma
    val,bins,patch = pylab.hist(usedata,bins=30,normed=True)
    #print bins
    f = scipy.stats.norm(loc=mu,scale=sigma)
    norm = scipy.integrate.quad(f.pdf,usedata.min(),usedata.max())[0]
    
    pylab.plot(bins,f.pdf(bins)/norm)
    pylab.show()
    return mu,sigma
#estimate mean and resolution using median and quartile dont' chop off data
#return med, left sigma, right sigma
def median_quartile(data):
    med = np.median(data)
    left = scipy.stats.scoreatpercentile(data,25)
    right = scipy.stats.scoreatpercentile(data,75)
    return med, (med-left)/0.68, (right-med)/0.68

def midpoints(edges):
    left = edges[1:]
    right = edges[:-1]
    return (left+right)/2.0

#find half max position
def find_hmp(h,edges,step=1):
    #find bin with the maximum
    imax,maxvalue = max((z for z in enumerate(h)),key=lambda x: x[1])
    #start walking right until found bin with less than half
    #now walking right til it finds a half

    hmp = edges[imax+step] #start the edge with the right bin boundary
    thisindex = imax
    found = False
    while(True):
        thisindex+=step
        if thisindex>=len(h) or thisindex<0:
            found = False
            break;
        if h[thisindex]<maxvalue/2.0:
            found =True
            #find the slope to extrapolate
            #do a linear intrapolation here

            thismidpoint = (edges[thisindex+1]+edges[thisindex])/2.0

            slopewidth = (edges[thisindex+step]-edges[thisindex-step])/2.0

            slope = (h[thisindex]-h[thisindex-step])/slopewidth
            #print slope,slopewidth,thismidpoint
            hmp = (maxvalue/2.0-h[thisindex])/slope + thismidpoint
            break;
    #careful of case where it walks out of bound 
    #assert(found)
    if not found:
        hmp = edges[0] if step>0 else edges[-1]
    return hmp

def fwhm(h,edges):
    hml = find_hmp(h,edges,-1)
    hmr = find_hmp(h,edges,+1)
    return hmr-hml

def main():
    import pylab
    # ndata = 4000
    #    data = np.random.normal(100,5,ndata)
    #    data.sort()
    #    #print data[200:]
    #    usedata = data[1000:]
    #    fitandshow(usedata)
    mu=0
    sigma = 1
    n=1
    alpha=1
    x = np.linspace(-10,4,100)
    val = np.array([cball(y,alpha,n,mu,sigma) for y in x])
    cdf = cballcdf(alpha, n, mu,sigma,x)
    pylab.figure(0)
    pylab.plot(x,val)
    pylab.plot(x,cdf)
    pylab.figure(1)
    db = Connection().square_7
    coll = db.cluster.find({'angle':1.0,'alg':'lin'})
    E = np.array([x['E'] for x in coll])
    #E = E[E>80.0]
    h,edges = np.histogram(E,bins=100)
    pylab.errorbar(midpoints(edges),h,yerr=np.sqrt(h),fmt='b.')
    res = fitcballx2(E,nbins=100,mu=100.0,sigma=5.0).values
    #print len(E)
    fit = len(E)*(edges[1]-edges[0])*normcball(edges,res['alpha'],res['n'],res['mu'],res['sigma'])
    #print fit
    #print h
    #print sum(h)
    #print sum(fit)*(edges[-1]-edges[0])/100.0
    pylab.plot(edges,fit,'r')
    pylab.show()
if __name__ == '__main__':
    main()