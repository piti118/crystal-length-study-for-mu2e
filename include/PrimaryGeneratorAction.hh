#ifndef PrimaryGeneratorAction_h
#define PrimaryGeneratorAction_h 1

#include "G4VUserPrimaryGeneratorAction.hh"
#include "G4ParticleGun.hh"
#include "globals.hh"
#define _USE_MATH_DEFINES
#include <cmath>
#include "Simulation.hh"
class G4ParticleGun;
class G4Event;
class PrimaryGeneratorMessenger;
class Simulation;
//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

class PrimaryGeneratorAction : public G4VUserPrimaryGeneratorAction
{
public:
  PrimaryGeneratorAction();    
  virtual ~PrimaryGeneratorAction();

  void GeneratePrimaries(G4Event*);
  void SetAngle(double deg){
    double rad = deg*M_PI/180.;
    angle = deg;
    particleGun->SetParticleMomentumDirection(G4ThreeVector(0.,sin(rad),cos(rad)));
  }
  void rand();
  double xPos(){return particleGun->GetParticlePosition().x();}
  double yPos(){return particleGun->GetParticlePosition().y();}
  double GetAngle(){return angle;}
private:
  G4ParticleGun*           particleGun;	 //pointer a to G4  class
    
  PrimaryGeneratorMessenger* gunMessenger;   //messenger of this class
  G4String                   rndmFlag;	     //flag for a rndm impact point
  double angle;//in deg
};

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

#endif


