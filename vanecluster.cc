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
#include <sstream>
int main(int argc,char** argv)
{

  G4RunManager * runManager = new G4RunManager();
  double default_length = 13;
  Detector* detector=0;
  std::string dbname("default_db");
  if(argc < 2){
    std::cout << "Specify detector [hexarea|hexbig|hexsmall|square]" << std::endl;
    std::exit(1);
  }else{
    std::string det(argv[1]);
    if(det.compare("hexbig")==0){
      detector = new HexDetector("hexbig",6,1.5*cm);
    }else if(det.compare("hexsmall")==0){
      detector = new HexDetector("hexsmall",6,1.3*cm);
    }else if(det.compare("square")==0){
      detector = new SquareDetector(5);  
    }else if(det.compare("hexarea")==0){
      detector = new HexDetector("hexarea",6,1.612*cm);
    }else{
      std::cout << "unknown detector type" << det << std::endl;
      std::exit(1);
    }
    dbname = det;
  }
  
  //see if user specify length
  if(argc>=3){
      double length;
      std::stringstream ss(argv[2]);
      ss >> length;
      default_length=length;
      dbname = dbname + "_" + ss.str();
  }
  detector->setCrystalLength(default_length*cm);
  
  // Set mandatory initialization classes
  //
  Simulation::getInstance()->detector = detector;
  runManager->SetUserInitialization(detector);
  // Physics list
  PhysicsList* physics = new PhysicsList();
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

  
  if (argc <= 3)   // batch mode
    {
      for(int deg=0;deg<90;deg++){
        gen_action->SetAngle(deg);
        runManager->BeamOn(4000);
      }
      //DEDXDatabase::save("localhost",Simulation::getInstance()->detector->getName());
      DEDXDatabase::save("localhost",dbname);
        
    }
  else
    {  // interactive mode : define UI session
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
