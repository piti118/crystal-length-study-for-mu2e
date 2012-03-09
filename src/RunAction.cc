#include "RunAction.hh"
#include <fstream>
#include "G4Run.hh"
#include "G4RunManager.hh"
#include "G4UnitsTable.hh"
#include <iostream>

RunAction::RunAction()
{}

RunAction::~RunAction()
{}

void RunAction::BeginOfRunAction(const G4Run* aRun)
{ 
  G4cout << "### Run " << aRun->GetRunID() << " start." << G4endl;

  //inform the runManager to save random number seed
  G4RunManager::GetRunManager()->SetRandomNumberStore(true);
  runno = aRun->GetRunID();
  //out << YAML::BeginSeq;
}

void RunAction::EndOfRunAction(const G4Run* aRun)
{
  // using std::ofstream;
  //   using std::endl;
  //   using std::cout;
  //   using std::string;
  //   string fname("output.yaml");
  //   ofstream fout(fname.c_str());
  //   
  // 
  //   out << YAML::EndSeq;
  //   cout << "Writing to " << fname << "...";
  //   fout << out.c_str() << endl;
  //   cout << "Done." << endl;
  //   fout.close();
  //   assert(out.good());  
}
