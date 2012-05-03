
#include "G4NistManager.hh"
#include "Materials.hh"

Materials::Materials(){
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