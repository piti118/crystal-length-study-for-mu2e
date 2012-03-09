from matplotlib import pyplot as plt
import pymongo
def main():
    fig = plt
    angles = range(0,90,20)
    clus,alg,a = 'adj','log',4
    param = 4.0
    dbnames = ['hexarea','hexbig','square','hexsmall']
    conn = pymongo.Connection()
    fig = plt.figure()
    ax = { key:fig.add_subplot(2,2,i) for i,key in enumerate(dbnames)}
    for dbname in dbnames:
        col = conn[dbname]['cluster']
        for angle in angles:
            cond = {'alg':alg,'a':a,'clus':clus,'angle':angle}
            #cond = {'alg':'log'}
            print cond
            E = [ x['E'] for x in col.find(cond) ]
            print len(E)
            ax[dbname].hist(E,bins=50,range=(60,110),histtype='step',lw=2,label=str(angle))
        ax[dbname].legend(loc='upper left')
        ax[dbname].grid(True,which='major',axis='y')
        ax[dbname].minorticks_on()
        ax[dbname].grid(True,which='both',axis='x')
        ax[dbname].set_xlim(xmin=60)
        ax[dbname].set_ylim(ymin=0)

        ax[dbname].set_title(dbname)
    plt.show()
    
if __name__ == '__main__':
    main()
