#ifndef SIMULATION_H
#define SIMULATION_H value
#include "Detector.hh"
#include "EventAction.hh"
#include "PrimaryGeneratorAction.hh"
#include "RunAction.hh"
//This class store detector object
//Poor man non-thread safe singleton 

class EventAction;
class PrimaryGeneratorAction;
class RunAction;

class Simulation{
public:
  static Simulation* getInstance(){
    if(!instance){
      instance = new Simulation();
    }
    return instance;
  }
  
  Detector* detector;
  EventAction* eventaction;
  PrimaryGeneratorAction* pgaction;
  RunAction* runaction;
  
  Simulation():detector(0),eventaction(0),pgaction(0),runaction(0){}
  virtual ~Simulation(){}
  
private:
  static Simulation* instance;
};
#endif