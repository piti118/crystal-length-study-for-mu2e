#ifndef DETECTOR_H
#define DETECTOR_H value
// #include "mongo/client/dbclient.h"
// #include "BSONInterface.hh"
#include "G4TouchableHandle.hh"
#include "G4VUserDetectorConstruction.hh"
#include "G4Material.hh"
#include <vector>
class Detector:  public G4VUserDetectorConstruction{
public:
  virtual ~Detector(){}

  //determine whether detector part with this id is in this detector
  virtual bool inDetector(int id){return false;}
  virtual const char* getName(){return "generic";}
  //determine wheter touchablehandle with is in this detector
  virtual bool touchableInDetector(const G4TouchableHandle& t){
    return inDetector(t->GetCopyNumber());
  }
  virtual G4ThreeVector randPos(){
    G4ThreeVector toReturn(0,0,0);
    return toReturn;
  }
  //dump detector description to BSONObject
  //virtual mongo::BSONObj toBSON();
  virtual void setCrystalLength(double length)=0;
  virtual int calorL(int id)=0;//{return 0;}
  virtual int calorK(int id)=0;//{return 0;}
  virtual double calorX(int id)=0;//{return 0;}
  virtual double calorY(int id)=0;//{return 0;}
  virtual int ringno(int id)=0;//{return 0;}
  virtual int segmentno(int id)=0;//{return 0;}
  virtual void setWrappingMaterial(G4Material* mat)=0;
  //this should return a list of crystal id
  virtual std::vector<int> crystalList()=0;//{std::vector<int> v;return v;}
};
#endif
