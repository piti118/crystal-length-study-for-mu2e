#include "SquareDetector.hh"

#include "G4Material.hh"
#include "G4NistManager.hh"

#include "G4Box.hh"
#include "G4LogicalVolume.hh"
#include "G4PVPlacement.hh"
#include "G4PVReplica.hh"
#include "G4UniformMagField.hh"
#include "G4SubtractionSolid.hh"
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
#include <algorithm>
#include <cstdlib>
#include <cassert>
#include "util.hh"
SquareDetector::SquareDetector(int nring):
  nring(nring),
  posmap(),
  numrow(nring*2+1),numcol(nring*2+1),
  centerrow(0),centercol(0),//int div
  idoffset(10000),
  crystal_x(3*cm),crystal_y(3*cm),crystal_z(13*cm), //crystal dimension
  gap_x(0.2*mm),gap_y(0.2*mm), //gap
  wrapping_w(0.1*mm),//wrapping width (just making sure they don't intersect 0.1*mm-epsilon)
  offset_x(0*mm),offset_y(0*mm),offset_z(0*mm), //offset
  padding_x(1*cm),padding_y(1*cm),padding_z(1*cm), //padding
  total_crystal_x(0),total_crystal_y(0),
  LYSO(0),Air(0),world_box(0),world_log(0),world_pv(0),
  calor_box(),calor_log(),calor_pv()
{ 
  total_crystal_x = (numrow*crystal_x + (numrow-1)*gap_x);
  total_crystal_y = (numcol*crystal_y + (numcol-1)*gap_y);
  assert(nring>0);
  DefineMaterials();
  wrapping_mat = CarbonFiber;
  initPosMap();
}

void SquareDetector::initPosMap(){
  posmap.clear();
  using std::max;
  using std::abs;
  for(int l=-1*nring;l<=nring;l++){
    for(int k=-1*nring;k<=nring;k++){
      SquarePosition sq;
      sq.l=l;sq.k=k;
      int r = max(abs(l),abs(k));
      sq.ringno = r;
      //segment 0 is the top right corner
      //for l>=k it's (l-r)+(k-r)
      //for l<=k it's 2r+(l+r)+(k+r)
      int segoffset = l>=k?0:2*r;
      int segadd = l>=k?((r-l)+(r-k)):((l+r)+(k+r));
      sq.segmentno = segoffset+segadd;
      posmap.push_back(sq);
    }
  }
  PT_ASSERTEQ(posmap.size(),(2*nring+1)*(2*nring+1));
}

SquareDetector::~SquareDetector(){ 
    //do nothing
}

G4ThreeVector SquareDetector::randPos(){
  //shift back to center
  G4double x=((double)std::rand()/(double)RAND_MAX)*crystal_x-crystal_x/2;
  G4double y=((double)std::rand()/(double)RAND_MAX)*crystal_y-crystal_y/2;
  G4double z=0.;
  G4ThreeVector toReturn(x,y,z);
  return toReturn;
}

G4VPhysicalVolume* SquareDetector::Construct(){
  ConstructWorld();
  for(unsigned int ibox=0;ibox<posmap.size();ibox++){
    ConstructCalorimeter(ibox,posmap[ibox]);
  }
  ConstructAluminumSheet();
  return world_pv;
}

void SquareDetector::DefineMaterials(){ 
  G4NistManager* nistManager = G4NistManager::Instance();
  G4Element* Lu = nistManager->FindOrBuildElement("Lu");
  G4Element* Y = nistManager->FindOrBuildElement("Y");
  G4Element* Si = nistManager->FindOrBuildElement("Si");
  G4Element* O = nistManager->FindOrBuildElement("O");
  G4Element* Ce = nistManager->FindOrBuildElement("Ce");
  G4Element* C = nistManager->FindOrBuildElement("C");
  G4Element* H = nistManager->FindOrBuildElement("H");
    
  LYSO = new G4Material("LYSO", 7.1*g/cm3, 5, kStateSolid);
  LYSO->AddElement(Lu, 71.43*perCent);
  LYSO->AddElement(Y, 4.03*perCent);
  LYSO->AddElement(Si, 6.37*perCent);
  LYSO->AddElement(O, 18.14*perCent);
  LYSO->AddElement(Ce, 0.02*perCent);
  
  CarbonFiber = new G4Material("Carbon Fiber", 1.69*g/cm3, 3, kStateSolid);
  CarbonFiber->AddElement(C,10);
  CarbonFiber->AddElement(H,6);
  CarbonFiber->AddElement(O,1);
  
  Tyvek = new G4Material("Tyvek",0.96*g/cm3,2,kStateSolid);
  Tyvek->AddElement(C,1);
  Tyvek->AddElement(H,2);
  
  Mylar = nistManager->FindOrBuildMaterial("G4_MYLAR");
  /*
  new G4Material("Mylar", density= 1.397*g/cm3, ncomponents=3);
  Myl->AddElement(C, natoms=10);
  Myl->AddElement(H, natoms= 8);
  Myl->AddElement(O, natoms= 4);
  */
  
  Air = nistManager->FindOrBuildMaterial("G4_AIR");
  Aluminum = nistManager->FindOrBuildMaterial("G4_Al");
}

G4VPhysicalVolume* SquareDetector::ConstructWorld(){
  
  G4double worldsize_x = total_crystal_x+2*padding_x+2*offset_x;
  G4double worldsize_y = total_crystal_y+2*padding_y+2*offset_y;
  G4double worldsize_z = 2*crystal_z + 2*padding_z+2*offset_z;
  
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
  G4VisAttributes* worldVisAtt= new G4VisAttributes(G4Colour(0,0,1.0));
  worldVisAtt->SetVisibility(true);
  world_log->SetVisAttributes(worldVisAtt);
  return world_pv; 
}

G4VPhysicalVolume* SquareDetector::ConstructAluminumSheet(){
    if(offset_z>0.000001*mm){
        G4double al_x = total_crystal_x;
        G4double al_y = total_crystal_y;
        G4double al_z = offset_z;
        //al face at z=0
        G4double al_zloc = offset_z/2;
        G4Box* albox = new G4Box("al_box",al_x/2,al_y/2,al_z/2);
        G4LogicalVolume* allog = new G4LogicalVolume(albox,Aluminum,"al_log");
        G4PVPlacement* alpv = new G4PVPlacement(
            0,
            G4ThreeVector(0,0,al_zloc),
            allog,
            "al_pv",
            world_log,
            false,
            10
          );
        G4VisAttributes* simpleBoxVisAtt= new G4VisAttributes(G4Colour(0.0,1.0,1.0));
        simpleBoxVisAtt->SetVisibility(true);
        allog->SetVisAttributes(simpleBoxVisAtt);
        return alpv;
    }
    return NULL;
}

G4VPhysicalVolume* SquareDetector::ConstructCalorimeter(int ibox,const SquarePosition& sq){
  using std::string;
  using std::vector;
  using std::cout;
  using std::endl;

  char temp[100];
  char wtemp[100];
  sprintf(temp,"crystal_%d_%d",sq.l,sq.k);
  sprintf(wtemp,"wrap_%d_%d",sq.l,sq.k);
  string thisname(temp);
  string wname(wtemp);
  
  G4double thisx = sq.toXY(crystal_x+gap_x).first+offset_x;
  G4double thisy = sq.toXY(crystal_y+gap_y).second+offset_y;
  //shift by half crystal so the face is at 0,0,0
  G4double thisz = crystal_z/2+offset_z;
  
  G4Box* thisbox = new G4Box(thisname.c_str(), crystal_x/2,crystal_y/2,crystal_z/2);
  G4LogicalVolume* thislog = new G4LogicalVolume(thisbox, LYSO,(thisname+"_log").c_str());

  G4PVPlacement* thispv = new G4PVPlacement(
      0,
      G4ThreeVector(thisx,thisy,thisz),
      thislog,
      (thisname+"_pv").c_str(),
      world_log,
      false,
      idoffset+ibox
    );
  
  G4Box* crys_and_wrap = new G4Box(thisname.c_str(), crystal_x/2+wrapping_w,crystal_y/2+wrapping_w,crystal_z/2+wrapping_w);
  G4SubtractionSolid* wrapping_box = new G4SubtractionSolid(wname.c_str(), crys_and_wrap, thisbox);
  G4LogicalVolume* wrappinglog = new G4LogicalVolume(wrapping_box, wrapping_mat, (wname+"_log").c_str());
  G4PVPlacement* wrappv = new G4PVPlacement(
      0,
      G4ThreeVector(thisx,thisy,thisz),
      wrappinglog,
      (wname+"_pv").c_str(),
      world_log,
      false,
      idoffset*3+ibox
    );

  calor_box.push_back(thisbox);
  calor_log.push_back(thislog);
  calor_pv.push_back(thispv);
  
  G4VisAttributes* simpleBoxVisAtt= new G4VisAttributes(G4Colour(1.0,0,1.0));
  simpleBoxVisAtt->SetVisibility(true);
  thislog->SetVisAttributes(simpleBoxVisAtt);
  
  G4VisAttributes* wrappingVisAtt= new G4VisAttributes(G4Colour(1.0,0,0));
  wrappingVisAtt->SetVisibility(true);
  wrappinglog->SetVisAttributes(wrappingVisAtt);
  
  return thispv;
}
