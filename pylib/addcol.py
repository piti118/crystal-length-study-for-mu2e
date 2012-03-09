import util
import pymongo
from math import sqrt
def addcol():
  db = pymongo.Connection().crystal
  col = db.raw
  col.create_index('angle')
  idata = 0;
  for data in col.find(sort=[('angle', 1)]):
    linpos = util.linearPosition(data['dedx'],1)
    data['x3x3'] = linpos.x
    data['y3x3'] = linpos.y
    data['r3x3'] = linpos.r
    data['e3x3'] = linpos.totalE
    linpos = util.linearPosition(data['dedx'],2)
    data['x5x5'] = linpos.x
    data['y5x5'] = linpos.y
    data['r5x5'] = linpos.r
    data['e5x5'] = linpos.totalE
    if data['eventno']%100==0: print '{angle}:{eventno}'.format(**data) 
    col.save(data)
  
if __name__ == '__main__':
  addcol()