def closeto(x,tl=0.0000001):
    return {'$lt':x+tl,'$gt':x-tl}
