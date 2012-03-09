#include "HexDetector.hh"

#include "G4Material.hh"
#include "G4NistManager.hh"

#include "G4Box.hh"
#include "G4LogicalVolume.hh"
#include "G4PVPlacement.hh"
#include "G4PVReplica.hh"
#include "G4UniformMagField.hh"

#include "G4GeometryManager.hh"
#include "G4PhysicalVolumeStore.hh"
#include "G4LogicalVolumeStore.hh"
#include "G4SolidStore.hh"
#include "G4UnitsTable.hh"
#include "G4VisAttributes.hh"
#include "G4Colour.hh"
#include "G4NistManager.hh"
#include <string>
#include <vector>
#include <iostream>
#include "G4Polyhedra.hh"
#include <cmath>
HexDetector::HexDetector(const char* name, int nring, double hexsize):
  name(name),
  nring(nring),posmap(),hexsize(hexsize),gap(0.1*mm),
  LYSO(0),Air(0),world_box(0),world_log(0),world_pv(0),
  calor_box(),calor_log(),calor_pv()
{
  DefineMaterials();
  initPosMap();
  //and do nothing...
}

void HexDetector::initPosMap(){
  HexPositionGenerator hpg;
  posmap = hpg.generate(nring);
}

HexDetector::~HexDetector(){ 
    //do nothing
}

G4VPhysicalVolume* HexDetector::Construct()
{
  
  return ConstructCalorimeter();
}

void HexDetector::DefineMaterials()
{ 
  G4NistManager* nistManager = G4NistManager::Instance();
  G4Element* Lu = nistManager->FindOrBuildElement("Lu");
  G4Element* Y = nistManager->FindOrBuildElement("Y");
  G4Element* Si = nistManager->FindOrBuildElement("Si");
  G4Element* O = nistManager->FindOrBuildElement("O");
  G4Element* Ce = nistManager->FindOrBuildElement("Ce");
  
  LYSO = new G4Material("LYSO", 7.1*g/cm3, 5, kStateSolid);
  LYSO->AddElement(Lu, 71.43*perCent);
  LYSO->AddElement(Y, 4.03*perCent);
  LYSO->AddElement(Si, 6.37*perCent);
  LYSO->AddElement(O, 18.14*perCent);
  LYSO->AddElement(Ce, 0.02*perCent);
  
  Air = nistManager->FindOrBuildMaterial("G4_AIR");
}

G4VPhysicalVolume* HexDetector::ConstructCalorimeter()
{
  using std::string;
  using std::vector;
  using std::cout;
  using std::endl;
  double pi = atan(1)*4;
  G4double offset_x = 0*mm;
  G4double offset_y = 0*mm;
  G4double offset_z = 0*mm;
  
  G4double crystal_depth = 13*cm;
  G4double padding_x = 0.1*mm;
  G4double padding_y = 0.1*mm;
  G4double padding_z = 0.1*mm;
  G4double worldsize_x = (2*nring+1)*(hexsize+gap)*2/std::cos(pi/6)+2*padding_x;
  G4double worldsize_y = (2*nring+1)*(hexsize+gap)*2/std::cos(pi/6)+2*padding_y;
  G4double worldsize_z = 2*(crystal_depth+padding_z);

  world_box = new G4Box("world_box",worldsize_x/2,worldsize_y/2,worldsize_z/2);
  world_log = new G4LogicalVolume(world_box,Air,"world_log");
  //world_log->SetVisAttributes (G4VisAttributes::Invisible);
  world_pv = new G4PVPlacement(
      0, //no rotation
      G4ThreeVector(), //at origin
      world_log,
      "world_pv",
      0,
      false, //no boolean
      0); //copy number
   
  //zplanes rinner and router define hexagon
  G4double zplanes[2];
  zplanes[0]=0*cm;zplanes[1]=crystal_depth;
  G4double rinner[2];
  rinner[0]=0*cm;rinner[1]=0*cm;
  G4double router[2];
  router[0]=hexsize;router[1]=hexsize;
  
  for(unsigned int ic=0;ic<posmap.size();++ic){
    HexPosition thispos = posmap[ic];
    char temp[100];
    sprintf(temp,"crystal_%d_%d",thispos.ringno,thispos.segmentno);
    string thisname(temp);
    std::pair<double,double> xy = thispos.toXY(2*hexsize+gap);
    double x = offset_x + xy.first;
    double y = offset_y + xy.second;
    
    std::cout << thispos.l << "," << thispos.k << ":" << x << "," << y << std::endl;
    
    double z = 0;
    G4Polyhedra* thishex = new G4Polyhedra(
      thisname.c_str(),
      0+pi/3,2*pi+pi/3, // phistart, totalphi
      6,//numside
      2,//numzplane
      zplanes,
      rinner,
      router
    );
    G4RotationMatrix* rot = new G4RotationMatrix();rot->rotateZ(pi/6);
    G4LogicalVolume* thislog = new G4LogicalVolume(thishex,LYSO,(thisname+"_log").c_str());
    G4PVPlacement* thispv = new G4PVPlacement(
      rot,
      G4ThreeVector(x,y,z),
      thislog,
      (thisname+"_pv").c_str(),
      world_log,
      false,
      ic+idoffset
      );
  }

  return world_pv;
}
