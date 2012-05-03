import sys
from itertools import product
from os.path import isfile
def main():
    prefix = ''
    if 'qsub' in sys.argv:
        prefix ='qsubb -V -l "nodes=1:sl5"'
    binname = 'bin/Linux-g++/crystal'
    if isfile('bin/Darwin-g++/crystal'):
        binname = 'bin/Darwin-g++/crystal'
    
    lengths = [11,12,13]
    wrappings = ['carbonfiber','tyvek','mylar','none']
    althicknesses = [0,1,2,3]
    
    for l,w,t in product(lengths,wrappings,althicknesses):
        outname = 'output/%(w)s_%(l)d_%(t)d.root'%locals()
        command = '%(prefix)s %(binname)s square %(l)d %(w)s %(outname)s %(t)d'%locals()
        print command.strip()
    
if __name__ == '__main__':
    main()
