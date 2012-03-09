#ifndef HexDetector_h
#define HexDetector_h 1

#include "G4VUserDetectorConstruction.hh"
#include "globals.hh"
#include <vector>
#include "Detector.hh"
#include "HexPosition.hh"
#include "G4Polyhedra.hh"
#include <cmath>
class G4Box;
class G4LogicalVolume;
class G4VPhysicalVolume;
class G4Material;
class G4UniformMagField;
class DetectorMessenger;

class HexDetector : public Detector
{
  public:
    HexDetector(const char* name,int nring,double hexsize);
    ~HexDetector();
    const char* name;
    int nring;
    double hexsize;
    double gap;
    double crystal_length;
    std::vector<HexPosition> posmap;
    static const unsigned int idoffset = 10000;
    virtual const char* getName(){return name;}
    G4VPhysicalVolume* Construct();
    G4ThreeVector randPos(){
        G4double x=((double)std::rand()/(double)RAND_MAX)*2*hexsize-hexsize;
        G4double y=((double)std::rand()/(double)RAND_MAX)*2*hexsize-hexsize;
        G4double z=0.;
        G4ThreeVector toReturn(x,y,z);
        return toReturn;
    }
    
    inline unsigned int calorRing(int id){return posmap[id-idoffset].ringno;}
    inline unsigned int calorSeg(int id){return posmap[id-idoffset].segmentno;}
    
    bool inDetector(int id){
      int order = id - idoffset;
      return order >=0 && order < posmap.size();
    }
    void initPosMap();
    
    virtual int calorL(int id){return posmap[id-idoffset].l;}
    virtual int calorK(int id){return posmap[id-idoffset].k;}
    //TODO: fix this
    virtual double calorX(int id){
      return posmap[id-idoffset].toXY(2*hexsize+gap).first;
    }
    virtual double calorY(int id){
      return posmap[id-idoffset].toXY(2*hexsize+gap).second;
    }
    virtual int ringno(int id){return posmap[id-idoffset].ringno;}
    virtual int segmentno(int id){return posmap[id-idoffset].segmentno;}
    virtual std::vector<int> crystalList(){
      std::vector<int> v;
      for(int i=0;i<posmap.size();i++){
        v.push_back(i+idoffset);
      }
      return v;
    }
    virtual void setCrystalLength(double length){
        crystal_length=length;
    }
  private:
    
    G4Material* LYSO;
    G4Material* Air;
    
    G4Box* world_box;
    G4LogicalVolume* world_log;
    G4VPhysicalVolume* world_pv;
    
    std::vector<G4Polyhedra*> calor_box;
    std::vector<G4LogicalVolume*> calor_log;
    std::vector<G4VPhysicalVolume*> calor_pv; 
    inline double hexsize2r(double hexsize) const {double pi =  std::atan(1)*4;return hexsize/std::cos(pi/6);}
  private:
    
     void DefineMaterials();
     G4VPhysicalVolume* ConstructCalorimeter();     
};

#endif

