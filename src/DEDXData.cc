#include "DEDXData.hh"
#include <vector>
#include "Simulation.hh"
std::vector< DEDXData > DEDXDatabase::data;

void DEDXData::setup(int runno, int eventno, double angle, double beamx, double beamy){
  this->runno = runno;
  this->eventno = eventno;
  this->angle = angle;
  this->beamx = beamx;
  this->beamy = beamy;
  dedx.clear();
  reset();
}

void DEDXData::accumulate(int calorId,double dedxval){
  if(dedx.find(calorId)==dedx.end()){
    dedx[calorId]=0.;
  }
  dedx[calorId]+=dedxval;
  //std::cout << "accumulate" << " " << calorId << std::endl;
}

void DEDXData::reset(){
  using std::map;
  using std::vector;
  vector<int> clist = Simulation::getInstance()->detector->crystalList();
  for(int i=0;i<clist.size();i++){
    dedx[clist[i]]=0.;
  }
}

double DEDXData::sumE() const{
  using std::map;
  double sum = 0;
  for(map<int,double>::const_iterator it = dedx.begin();it!=dedx.end();++it){
    sum += it->second;
  }
  return sum;
}


// 
// mongo::BSONObj DEDXData::toBSON() {
//  using mongo::BSONObjBuilder;
//  using mongo::BSONArrayBuilder;
//  using mongo::BSONObj;
//  using std::map;
//  BSONObjBuilder b;
//  b << "runno" << runno;
//  b << "eventno" << eventno;
//  b << "angle" << angle;
//  b << "beamx" << beamx/cm;
//  b << "beamy" << beamy/cm;
//  Detector* det = Simulation::getInstance()->detector;
//  BSONArrayBuilder dedxlist;
//  for(map<int,double>::const_iterator it = dedx.begin(); it!=dedx.end(); ++it){
//    int calorId = it->first;
//    double thisDEDx = it->second;
//    BSONObjBuilder calor;
//    calor << "calorId" << calorId;
//    calor << "y" << det->calorY(calorId)/cm;
//    calor << "x" << det->calorX(calorId)/cm;
//    calor << "ringno" << det->ringno(calorId);
//    calor << "iseg" << det->segmentno(calorId);
//    calor << "l" << det->calorL(calorId);
//    calor << "k" << det->calorK(calorId);
//    calor << "dedx" << thisDEDx/MeV;
//    dedxlist << calor.obj();
//  }
//  //BSONObj arr = dedxlist.done();
//  b << "dedx" << dedxlist.arr();
//  b << "total" << sumE()/MeV;
//  return b.obj(); 
// }
EventInfo DEDXData::getEventInfo(){
    EventInfo ret;
    ret.eventno = eventno;
    ret.runno = runno;
    ret.angle = angle;
    ret.beamx = beamx/cm;
    ret.beamy = beamy/cm;
    return ret;
}
std::vector<hitmap> DEDXData::hm(){
    using namespace std;
    vector<hitmap> ret;
    Detector* det = Simulation::getInstance()->detector;
    hitmap tmp;
    tmp.runno = runno;
    tmp.eventno = eventno;
    for(map<int,double>::const_iterator it = dedx.begin(); it!=dedx.end(); ++it){
        int calorId = it->first;
        double thisDEDx = it->second;
        tmp.l = det->calorL(calorId);
        tmp.k = det->calorK(calorId);
        tmp.E = thisDEDx/MeV;
        if(tmp.E > 1e-7){
            ret.push_back(tmp);
        }
    }
    return ret;
}

void DEDXDatabase::saveroot(const std::string& fname){
    using namespace std;
    TFile f(fname.c_str(),"RECREATE");
    TTree EventInfoTree("eventinfo","eventinfo");
    TTree HitMapTree("hitmap","hitmap");
    
    EventInfo tmpEInfo; tmpEInfo.branch(EventInfoTree);
    hitmap tmpHm; tmpHm.branch(HitMapTree);
    for(int i=0;i<data.size();++i){
        vector<hitmap> hms =  data[i].hm();
        EventInfo einfo = data[i].getEventInfo();
        //fill hitmaptree
        for(int ihm=0;ihm<hms.size();ihm++){
            tmpHm = hms[ihm];
            HitMapTree.Fill();
        }
        //and event info
        tmpEInfo = einfo;
        EventInfoTree.Fill();
    }
    f.Write();
    f.Close();
}

// void DEDXDatabase::save(const std::string& host,const std::string& db,const std::string& coll){
//   mongo::DBClientConnection c;
//   c.connect(host);
//   std::string ns = db+"."+coll;
//   c.dropCollection(ns);
//   for(unsigned int i=0;i<data.size();++i){
//     mongo::BSONObj obj = data[i].toBSON();
//     if(i%10000==0){std::cout << "Inserting "<< i << "/" << data.size() <<std::endl;}
//     c.insert(ns,obj);
//   }
// }
