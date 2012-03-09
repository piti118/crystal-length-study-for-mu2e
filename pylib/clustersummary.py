import util
import pymongo
import argparse
from mongoutil import closeto
from clusterutil import *
from fittool import fitandshow, fitgaussx2, median_quartile
from pprint import pprint
import sys
import numpy
import pylab
def go(dbname,type_):
    db = pymongo.Connection()[dbname]
    col = db.cluster
    col.create_index('angle')
    col.create_index('alg')
    col.create_index([('alg',pymongo.ASCENDING),('clus',pymongo.ASCENDING),('a',pymongo.ASCENDING),('angle',pymongo.ASCENDING)])
    db.cluster_sum.drop()
    angles = [x for x in col.distinct('angle')]
    algs = [x for x in col.distinct('alg')]
    tl = 0.001#tolerance
    i = 0
    clus_list = ['adj','ring']
    for clus in clus_list:
        algs = col.find({'clus':clus}).distinct('alg')
        for alg in algs:
            alist = col.find({'alg':alg,'clus':clus}).distinct('a')
            for a in alist:
                angles = col.find({'alg':alg,'clus':clus,'a':a}).distinct('angle')
                for angle in angles:
                    print 'working on',dbname,clus,alg,angle,a
                    key = {'alg':alg,'clus':clus,'a':closeto(a),'angle':closeto(angle)}
                    rlist = numpy.array([x['dis'] for x in col.find(key)])
                    rlist.sort()
                    #print 'rlist',numpy.median(rlist),rlist[:int(rlist.size*0.9)].std()
                    #fitandshow(rlist[:int(rlist.size*0.8)],mu=numpy.median(rlist),sigma=rlist[:int(rlist.size*0.9)].std())
                    #sys.exit(0)
                    rmu,rsigma = fitgaussx2(rlist[:int(rlist.size*0.8)],mu=numpy.median(rlist))#fit first 60%
                    #rmu,rsigma = 0.9,0.
                    sr = util.stat(rlist)
                    elist = numpy.array([x['E'] for x in col.find(key)])
                    elist.sort()
                    #print 'elist',elist.mean(),elist[int(elist.size*0.1):].std()
                    #fitandshow(elist[int(elist.size*0.5):])
                    #sys.exit(0)
                    emu,esigma = fitgaussx2(elist[int(elist.size*0.5):])#fit last 60%
                    #emu,els,esigma = median_quartile(elist)
                    se = util.stat(elist)
                    clsize = [x['clsize'] for x in col.find(key)]
                    scl = util.stat(clsize)
                    print (dbname,clus,alg,angle,a,rmu,rsigma,emu,esigma)                    
                    m = {}
                    m['dis'] = sr.tomap()
                    m['dis']['fitmu'] = rmu
                    m['dis']['fitstd'] = rsigma
                    m['E'] = se.tomap()
                    m['E']['fitmu'] = emu
                    m['E']['fitstd'] = esigma
                    m['angle']=angle
                    m['a']=a
                    m['alg']=alg
                    m['clus']=clus
                    m['clsize']=scl.tomap()
                    #pprint(m)
                    db.cluster_sum.insert(m)
                    i+=1
                    if i%10==0: print (alg,angle,a,rmu,rsigma,emu,esigma)
def main():
    parser = argparse.ArgumentParser(description='do cluster finding')
    parser.add_argument('--db', action="store", help='database name',required=True)
    parser.add_argument('--type', action="store",default=None, help='type[hex|square]')
    arg = parser.parse_args()

    arg.type = 'hex' if arg.type is None and 'hex' in arg.db else arg.type
    
    arg.type = 'square' if arg.type is None and 'square' in arg.db else arg.type
    if arg.type not in ['hex','square']:
        print 'Specify type [hex|square]'    
    print arg
    go(arg.db,arg.type)
if __name__ == '__main__':
    main()