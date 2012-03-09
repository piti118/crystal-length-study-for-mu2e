"""
Show how to modify the coordinate formatter to report the image "z"
value of the nearest pixel given x and y
"""
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import pymongo
from subprocess import call
profile = pymongo.Connection().crystal.profile
profile.create_index([('angle',pymongo.ASCENDING),('row',pymongo.ASCENDING),('col',pymongo.ASCENDING)])
for angle in xrange(90):
  X = np.zeros((9,9))
  print "Working on angle= "+str(angle)
  for row in xrange(9):
    for col in xrange(9):
      d = profile.find_one({'angle':angle,'row':row,'col':col})
      X[row][col] = d['mean']
  fig = plt.figure()
  ax = fig.add_subplot(111)
  cmap = cm.get_cmap('jet', 100)
  ax.imshow(X, cmap=cmap, interpolation='nearest')
  plt.grid(True)
  numrows, numcols = X.shape
  def format_coord(x, y):
      col = int(x+0.5)
      row = int(y+0.5)
      if col>=0 and col<numcols and row>=0 and row<numrows:
          z = X[row,col]
          return 'x=%1.4f, y=%1.4f, z=%1.4f'%(x, y, z)
      else:
          return 'x=%1.4f, y=%1.4f'%(x, y)

  ax.format_coord = format_coord
  fig.text(0.9,0.8,str(angle))
  #plt.colorbar()
  plt.savefig("profile"+str(angle)+".png")
f = [ 'profile'+str(angle)+'.png' for angle in range(90)]
call(['convert','-delay','20','-loop','0']+f+['out.gif'])