#ifndef BSONINTERFACE
#define BSONINTERFACE value
#include "mongo/client/dbclient.h"
class BSONInterface{
public: 
  virtual ~BSONInterface(){}
  virtual mongo::BSONObj toBSON()=0;
};
#endif
