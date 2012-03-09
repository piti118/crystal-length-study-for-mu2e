import pymongo
from pprint import pprint
from math import sqrt, floor
import util


def summarize():
  db = pymongo.Connection().crystal
  coll = db.raw
  coll.create_index('angle')
  angles = [i for i in coll.distinct('angle')]
  angles.sort()
  resolutions = {}
  db.summary.remove()
  for angle in angles:
    allData = coll.find({'angle':angle})
    evSums = (
      { 
        'dedx':sum(x['dedx'] for x in data['dedx'].values()),
        'r3x3':data['r3x3'],
        'x3x3':data['x3x3'],
        'y3x3':data['y3x3'],
        'e3x3':data['e3x3'],
        'r5x5':data['r5x5'],
        'x5x5':data['x5x5'],
        'y5x5':data['y5x5'],
        'e5x5':data['e5x5']
      }
      for data in allData)
    
    stat = util.dstat(evSums)
    stat['angle']=angle
    print "Summarizing angle = "+str(angle)
    db.summary.insert(stat)
    #for data in allData: #for 1 event
    #   calorEs = map(lambda x: x['dedx'],data['dedx'])
    #   evSums.append(sum(calorEs))
    # summary={}
    #     summary['angle'] = angle
    #     summary['mean'] = mean = stat.mean
    #     summary['sqmean'] = stat.sqmean
    #     summary['sd'] = sd = stat.sd
    #     summary['resolution'] = stat.res
    #     summary['n'] = n = stat.n
    #     db.summary.insert(summary)

if __name__ == '__main__':
  summarize()