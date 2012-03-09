#listing all the jobs
import tsub
from pprint import pprint
def main():
    dbs = ['square','hexsmall','hexarea','hexbig']
    cmd = []
    fc=[]
    for db in dbs:
        fc_command = 'python clusterfinding.py --db %s'%db
        fc.append(fc_command)
    #tsub.run(fc)
    cs=[]
    for db in dbs:
        cs_command = 'python clustersummary.py --db %s'%db
        cs.append(cs_command)
    tsub.run(cs)
        
if __name__ == '__main__':
    main()