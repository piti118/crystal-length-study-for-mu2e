import pymongo
import util
import copy
from pprint import pprint

#create db.profile containing statistic about individual crystal
def profile():
  db = pymongo.Connection().crystal
  col = db.crystal
  #TODO: put detector parameter in the database
  print "Clearing profile collection"
  db.profile.remove()
  for angle in xrange(90):
    acc = None
    print "Working on angle = "+str(angle)
    for data in col.find({'angle':angle}):
      t = dict( ((x['row'],x['col']), x['dedx'] ) for x in data["dedx"] )
      if acc is None: acc = dict((key,[]) for key,val in t.items())
      for key,val in t.items(): acc[key].append(val)
    stat = dict( (key,util.statmap(val)) for key,val in acc.items() )
    #flatten stat and insert
    for key,val in stat.items():
      stat[key]['row']=key[0]
      stat[key]['col']=key[1]
      stat[key]['angle']=angle
      db.profile.insert(stat[key])
        
if __name__ == '__main__':
  profile()