#include "HexPosition.hh"
#include <cassert>
//#include "util.hh"
#include <iostream>
std::vector<HexPosition> HexPositionGenerator::generate(int nring){
  using std::cout;using std::endl;
  std::vector<HexPosition> toReturn;
  //cout << step.size() << endl;
  assert(nring>=0);
  HexPosition center(0,0,0,0);
  toReturn.push_back(center);
  
  for(int iring=1;iring<nring;iring++){//for eachring
    LK cp(iring,iring);
    //walking along step
    int segno = 0;
    for(unsigned int istep =0;istep<step.size();istep++){
      //walks iring steps for each side
      
      for(unsigned int iseg=0;iseg<iring;iseg++){
        cp+=step[istep];
        HexPosition thisPos(cp.l,cp.k,iring,segno);
        toReturn.push_back(thisPos);
        ++segno;
      }//end seg
    }//end step
  }//end ring
  //std::cout << toReturn << std::endl;
  assert(toReturn.size()==1+nring*(nring-1)/2*6);

  return toReturn;
} 
