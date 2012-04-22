#ifndef MATERIALS_H
#define MATERIALS_H
class G4Material;
class Materials{
public:
    G4Material* Air;
    G4Material* LYSO;
    G4Material* Tyvek;
    G4Material* Mylar;
    G4Material* CarbonFiber;
    Materials();
};
#endif