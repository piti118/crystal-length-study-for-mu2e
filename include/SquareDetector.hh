#ifndef SquareDetector_h
#define SquareDetector_h 1

#include "Detector.hh"
#include "globals.hh"
#include <vector>
#include <cstdlib>
#include <utility>
#include "G4ThreeVector.hh"
class G4Box;
class G4LogicalVolume;
class G4VPhysicalVolume;
class G4Material;
class G4UniformMagField;
class DetectorMessenger;

/**
* This class represents array of square 3x3x13 cm crystal
**/

class SquareDetector : public Detector
{
  public:
  
    SquareDetector(int size=9);//numrow numcol
   ~SquareDetector();
   virtual const char* getName(){return "square";}
    class SquarePosition{
    public:
      int l;
      int k;
      int ringno;
      int segmentno;
      std::pair<double,double> toXY(double scale) const{
        double x = l*scale;
        double y = k*scale;
        return std::make_pair(x,y);
      }
    };
    
    G4VPhysicalVolume* Construct();
    G4ThreeVector randPos();
    virtual bool inDetector(int id){
      int order = id - idoffset;
      return order>=0,order<posmap.size();
    }

    //l represents row number
    //k represents column
    //0,0 is the center
    //row run from -numcol/2 to +numcol/2
    virtual int calorL(int id){return posmap[id-idoffset].l;}
    virtual int calorK(int id){return posmap[id-idoffset].k;}
    virtual double calorX(int id){return posmap[id-idoffset].toXY(crystal_x+gap_x).first;}
    virtual double calorY(int id){return posmap[id-idoffset].toXY(crystal_y+gap_y).second;}
    virtual int ringno(int id){return posmap[id-idoffset].ringno;}
    virtual int segmentno(int id){return posmap[id-idoffset].segmentno;}
    //this should return a list of crystal id
    virtual std::vector<int> crystalList(){
      std::vector<int> v;
      for(int i=0;i<posmap.size();i++){v.push_back(idoffset+i);}
      return v;
    }
    
    virtual void setCrystalLength(double length){
        crystal_z = length;
    }
  private:
    
    std::vector<SquarePosition> posmap;
    
    int nring;
    
    unsigned int numrow;
    unsigned int numcol;
    unsigned int centerrow;
    unsigned int centercol;
    
    unsigned int idoffset;
    
    G4double crystal_x;
    G4double crystal_y;
    G4double crystal_z;
    
    G4double gap_x;
    G4double gap_y;
    
    G4double offset_x;
    G4double offset_y;
    G4double offset_z;
    
    G4double padding_x;
    G4double padding_y;
    G4double padding_z;
    
    G4double total_crystal_x;
    G4double total_crystal_y;
    
    G4Material* LYSO;
    G4Material* Air;
    
    G4Box* world_box;
    G4LogicalVolume* world_log;
    G4VPhysicalVolume* world_pv;
    
    std::vector<G4Box*> calor_box;
    std::vector<G4LogicalVolume*> calor_log;
    std::vector<G4VPhysicalVolume*> calor_pv; 
    
    void DefineMaterials();
    void initPosMap();
    G4VPhysicalVolume* ConstructWorld();
    G4VPhysicalVolume* ConstructCalorimeter(int ibox, const SquarePosition& sq);  
};

#endif

