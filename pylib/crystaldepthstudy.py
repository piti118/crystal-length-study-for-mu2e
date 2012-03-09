
from fittool import *
from pymongo import Connection
from pylab import *
def main():
    mu=80
    sigma=5
    n=5
    alpha=2
    
    #first build map to databasename
    cry_len_map = {x:'square_'+str(x) for x in range(7,14)}
    
    for clen, dbname in cry_len_map:
        db = Connection()[dbname].cluster
        
        for angle in range(0,90,10):
            res = db.find({'angle':angle})
            E = [x['E'] for x in res]
        
    
if __name__ == '__main__':
    main()