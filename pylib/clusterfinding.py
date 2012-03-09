from itertools import izip
from pprint import pprint
from math import log,exp,sqrt
from util import average
import argparse
import pymongo
from clusterutil import *

def writecluster(col,alg,clus,evt,pos, E, cluster_size, a=0):
    beam_center = (evt['beamx'],evt['beamy'])
    dis = distance( beam_center, pos)
    col.insert({
        'clus':clus,
        'alg':alg,
        'a':a,
        'x':pos[0],
        'y':pos[1],
        'E':E,
        'clsize': cluster_size,
        'dis':dis,
        'bx':evt['beamx'],
        'by':evt['beamy'],
        'angle': evt['angle'],
        'evt':evt['_id']})  
    
def go(dbname,type_):
    db = pymongo.Connection()[dbname]
    i=0
    db.drop_collection("cluster")
    col = db.cluster

    shape = {'hex':HexShape,'square':SquareShape}[type_]
    #cluster_finder = {'ring':ring_cluster,'adj':cluster_expansion}
    cluster_finder = {'adj':cluster_expansion}
    
    for evt in db.raw.find():
        clist = evt['dedx']
        for cf_name, cf in cluster_finder.items():
            cluster = cf(clist,shape)
            cluster_size = len(cluster)
            if cluster_size>0: #ignore cluster that shot right betwen the gap
                #linear
                lin_center = lin_pos(cluster)
                E = totalE(cluster)
                cluster_size = len(cluster)
                writecluster(col, 'lin', cf_name, evt, lin_center, E, cluster_size)
                #sqr
                sqr_center = sqr_pos(cluster)
        
                writecluster(col, 'sqr', cf_name, evt,sqr_center, E, cluster_size)
                #log
                alist = [1.0,2.0,4.0]
                for a in alist:
                    log_center = log_pos(cluster,a=a)
                    writecluster(col, 'log', cf_name, evt,log_center, E, cluster_size, a)
                i+=1
                if(i%1000==0): print i
    print 'creating index'
    col.create_index([('alg',pymongo.ASCENDING),('a',pymongo.ASCENDING)])

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
  