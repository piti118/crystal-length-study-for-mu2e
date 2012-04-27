#include "G4RunManager.hh"
#include "G4UImanager.hh"

#include "Randomize.hh"
#include "PhysicsList.hh"
#include "PrimaryGeneratorAction.hh"
#include "RunAction.hh"
#include "EventAction.hh"
#include "SteppingAction.hh"

#ifdef G4VIS_USE
#include "G4VisExecutive.hh"
#endif

#ifdef G4UI_USE
#include "G4UIExecutive.hh"
#endif
#include <iostream>
#include "HexPosition.hh"
#include "HexDetector.hh"
#include "SquareDetector.hh"
#include "OriginalPhysics.hh"
#include "Materials.hh"
#include <sstream>
int main(int argc,char** argv){
    using namespace std;
    G4RunManager * runManager = new G4RunManager();
    Materials materials;
    double default_length = 13;
    Detector* detector=0;
    std::string dbname("default_db");
    if(argc < 2){
        std::cout << "Specify detector [hexarea|hexbig|hexsmall|square]" << std::endl;
        std::exit(1);
    }else{
        int numring = 10;
        std::string det(argv[1]);
        if(det.compare("hexbig")==0){
            detector = new HexDetector("hexbig",numring,1.5*cm);
        }else if(det.compare("hexsmall")==0){
            detector = new HexDetector("hexsmall",numring,1.3*cm);
        }else if(det.compare("square")==0){
            detector = new SquareDetector(numring);  
        }else if(det.compare("hexarea")==0){
            detector = new HexDetector("hexarea",numring,1.612*cm);
        }else{
            std::cout << "unknown detector type" << det << std::endl;
            std::exit(1);
        }
    }

    //see if user specify length
    if(argc>=3){
        double length;
        std::stringstream ss(argv[2]);
        ss >> length;
        default_length=length;
        dbname = dbname + "_" + ss.str();
    }
    //material
    if(argc>=4){
        std::string wmat(argv[3]);
        if(wmat=="carbonfiber"){
            detector->setWrappingMaterial(materials.CarbonFiber);
        }else if(wmat=="tyvek"){
            detector->setWrappingMaterial(materials.Tyvek);
        }else if (wmat=="mylar"){//12 micron mylar
            detector->setWrappingMaterial(materials.Mylar);
            detector->setWrappingThickness(0.012*mm);
            detector->setGap(0.025*mm);
        }else if (wmat=="none"){//absolutely nothing in between(very thin layer of air)
            detector->setWrappingMaterial(materials.Air);
            detector->setWrappingThickness(0.00001*mm);
            detector->setGap(0.00003*mm);            
        }else{
            std::cout << "unknown wrapping material" << wmat << std::endl;
            std::exit(1);
        }
    }
    string outfile;
    if(argc>=5){
        outfile = argv[4];
    }
    
    detector->setCrystalLength(default_length*cm);

  // Set mandatory initialization classes
  //
    Simulation::getInstance()->detector = detector;
    runManager->SetUserInitialization(detector);
  // Physics list
  // PhysicsList* physics = new PhysicsList();
  // runManager->SetUserInitialization(physics);
    OriginalPhysics* physics = new OriginalPhysics();
    runManager->SetUserInitialization(physics);

  // Set user action classes
  //
    PrimaryGeneratorAction* gen_action = new PrimaryGeneratorAction();
    Simulation::getInstance()->pgaction = gen_action;
    runManager->SetUserAction(gen_action);

  //
    RunAction* run_action = new RunAction;  
    Simulation::getInstance()->runaction = run_action;
    runManager->SetUserAction(run_action);
  //
    EventAction* event_action = new EventAction();
    Simulation::getInstance()->eventaction = event_action;
    runManager->SetUserAction(event_action);
  //
    SteppingAction* stepping_action =
        new SteppingAction();
    runManager->SetUserAction(stepping_action);

  // Initialize G4 kernel
  //
    runManager->Initialize();

#ifdef G4VIS_USE
  // Initialize visualization
    G4VisManager* visManager = new G4VisExecutive;
  // G4VisExecutive can take a verbosity argument - see /vis/verbose guidance.
  // G4VisManager* visManager = new G4VisExecutive("Quiet");
    visManager->Initialize();
#endif

  // Get the pointer to the User Interface manager
    G4UImanager* UImanager = G4UImanager::GetUIpointer();

//batch mode
    if (argc <= 5){
        for(int deg=0;deg<90;deg+=5){
            gen_action->SetAngle(deg);
            runManager->BeamOn(100000);
        }
        if(outfile!="") DEDXDatabase::saveroot(outfile);
    }else{
                    // interactive mode : define UI session  
#ifdef G4UI_USE
        G4UIExecutive* ui = new G4UIExecutive(argc, argv);
#ifdef G4VIS_USE
        UImanager->ApplyCommand("/control/execute " __TOP_DIR__ "/macro/vis.mac"); 
#endif
        if (ui->IsGUI())
            UImanager->ApplyCommand("/control/execute gui.mac");
        ui->SessionStart();
        delete ui;
#endif
    }

  // Job termination
  // Free the store: user actions, physics_list and detector_description are
  //                 owned and deleted by the run manager, so they should not
  //                 be deleted in the main() program !
#ifdef G4VIS_USE
    delete visManager;
#endif
    delete runManager;

    return 0;
}

