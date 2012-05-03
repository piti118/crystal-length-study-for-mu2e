#include "EventAction.hh"

#include "RunAction.hh"
#include "PrimaryGeneratorAction.hh"
#include "G4Event.hh"
#include "G4UnitsTable.hh"

#include "Randomize.hh"
#include <iomanip>
#include <iostream>
#include "DEDXData.hh"
#include "Simulation.hh"
EventAction::EventAction()
:dedx(),printModulo(1),eventMessenger(0)
{

}

EventAction::~EventAction()
{
}

void EventAction::BeginOfEventAction(const G4Event* evt)
{
  int eventno = evt->GetEventID();
  if (eventno%100==0){
    G4cout << "### Event " << evt->GetEventID() << " start." << G4endl;
  }
  Simulation* sim = Simulation::getInstance();
  sim->pgaction->rand();//randomize positon
  dedx.setup(
    sim->runaction->runno,
    evt->GetEventID(),
    sim->pgaction->GetAngle(),
    sim->pgaction->xPos(),
    sim->pgaction->yPos());  
}

void EventAction::EndOfEventAction(const G4Event* evt)
{
  int eventno = evt->GetEventID();
  if (eventno%10000==0){
    G4cout << "### Event " << evt->GetEventID() << " Done." << G4endl;
  }
  dedx.trim();
  DEDXDatabase::data.push_back(dedx);
}  

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
