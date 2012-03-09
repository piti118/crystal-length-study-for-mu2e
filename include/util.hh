#include <ostream>
#include <iostream>
#define PT_DEBUG(x) do{\
  std::cout << __FILE__ << ":" << __LINE__ << " | " << #x << " = " << x << std::endl;\
} while(false)
#define PT_ASSERTEQ(x,y) do{\
  if(x!=y){\
    std::cout << "Assertion equal failed " << __FILE__ << ":" << __LINE__ << std::endl;\
    std::cout << #x << " = " << x << std::endl;\
    std::cout << #y << " = " << y << std::endl;\
    std::exit(1);\
  } \
} while(false)

template<class T> inline std::ostream& operator << (std::ostream &os, const std::vector<T>& vec)
{
    os << "[ ";
	for(unsigned int i=0;i<vec.size();i++){
    	  os << vec.at(i);
          if(i!=vec.size()-1){
        	  os << " , " << std::endl;
          }
	}
	os << " ]";
    return os;
}


