#ifndef EventAction_h
#define EventAction_h 1

#include "G4UserEventAction.hh"
#include "globals.hh"
#include "DEDXData.hh"
#include "PrimaryGeneratorAction.hh"
class EventActionMessenger;
class DEDXData;
class EventAction : public G4UserEventAction
{
public:
  EventAction();
  virtual ~EventAction();

  void  BeginOfEventAction(const G4Event*);
  void    EndOfEventAction(const G4Event*);
    
  void AddAbs(G4double de, G4double dl) {EnergyAbs += de; TrackLAbs += dl;};
  void AddGap(G4double de, G4double dl) {EnergyGap += de; TrackLGap += dl;};
                     
  void SetPrintModulo(G4int    val)  {printModulo = val;};

  DEDXData dedx; 
private:
   
   G4double  EnergyAbs, EnergyGap;
   G4double  TrackLAbs, TrackLGap;
                     
   G4int     printModulo;
                             
   EventActionMessenger*  eventMessenger;
};

#endif

    
