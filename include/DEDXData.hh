#ifndef DEDXDATA
#define DEDXDATA 1
// #include "mongo/client/dbclient.h"
#include <map>
#include <G4UnitsTable.hh>
#include <iostream>
#include <ostream>
// #include "BSONInterface.hh"
#include <vector>
#include <TTree.h>
#include <TFile.h>

struct hitmap{
    int eventno;
    int runno;
    int l;
    int k;
    float E;//in MeV
    void branch(TTree& tree){
        tree.Branch("eventno",&eventno,"eventno/I");
        tree.Branch("runno",&runno,"runno/I");
        tree.Branch("l",&l,"l/I");
        tree.Branch("k",&k,"k/I");
        tree.Branch("E",&E,"E/F");
    }
};

struct EventInfo{
    int eventno;
    int runno;
    float angle;
    float beamx;
    float beamy;
    void branch(TTree& tree){
        tree.Branch("eventno",&eventno,"eventno/I");
        tree.Branch("runno",&runno,"runno/I");
        tree.Branch("angle",&angle,"angle/F");
        tree.Branch("beamx",&beamx,"beamx/F");
        tree.Branch("beamy",&beamy,"beamy/F");
    }
};

class DEDXData{//} public BSONInterface{
public:
  int eventno;
  int runno;
  double angle;
  double beamx;
  double beamy;
  std::map<int, double> dedx;//map from calorid to dedx 
  virtual ~DEDXData(){}
  void setup(int runno, int eventno, double angle, double beamx, double beamy);
  
  void accumulate(int calorId,double dedxval);
  
  void reset();
  double sumE() const;
  void trim(){
      std::map<int, double>::iterator it = dedx.begin();
      while (it != dedx.end())
      {
        if (it->second<1e-7)
        {
          std::map<int, double>::iterator toerase = it;
          ++it;
          dedx.erase(toerase);
        }
        else{
          ++it;
        }
      }
  }
  std::vector<hitmap> hm();
  EventInfo getEventInfo();
  //mongo::BSONObj toBSON();
  
};

class DEDXDatabase{
public:
  static std::vector<DEDXData> data;
  static void saveroot(const std::string& fname);
  //static void save(const std::string& host="localhost",const std::string& db="crystal",const std::string& coll="raw");
};
#endif
