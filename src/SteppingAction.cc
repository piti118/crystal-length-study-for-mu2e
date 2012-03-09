#include "Simulation.hh"
#include "SteppingAction.hh"
#include "EventAction.hh"

#include "G4Step.hh"
#include <iostream>


SteppingAction::SteppingAction()			 
{ }

SteppingAction::~SteppingAction()
{ }

void SteppingAction::UserSteppingAction(const G4Step* aStep)
{
  using std::cout;
  using std::endl;
  
  G4StepPoint* preStepPoint = aStep->GetPreStepPoint();
  G4TouchableHandle theTouchable = preStepPoint->GetTouchableHandle();
  G4int copyNo = theTouchable->GetCopyNumber();
  G4double edep = aStep->GetTotalEnergyDeposit();
  //std::cout << Simulation::getInstance()->detector->touchableInDetector(theTouchable) << std::endl;
   if(Simulation::getInstance()->detector->touchableInDetector(theTouchable)){
    Simulation::getInstance()->eventaction->dedx.accumulate(copyNo,edep);
  }
}
