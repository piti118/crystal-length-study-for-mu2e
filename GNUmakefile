G4TMP := tmp
G4BIN := bin
name := crystal
#name := test2
G4TARGET := $(name)
G4EXLIB := true
BOOSTDIR := /usr/local
CPPVERBOSE := 1
G4LIB_NO_SHARED := 1
TOPDIR = $(shell pwd)
ifeq ($(G4INSTALL),)
	$(error G4INSTALL not set. Did you source the geant4 env file?)
endif

ROOT_INC = $(shell root-config --cflags)
ROOT_LIB = $(shell root-config --libs)

#on somesystem there is no -mt
BOOSTLIB := -L$(BOOSTDIR)/lib -lboost_thread-mt -lboost_filesystem-mt -lboost_program_options-mt -lboost_system-mt
CPPFLAGS  += -O3 -Ivendor/yaml-cpp/include \
	-Ivendor/mongo-cxx-driver-v2.0/include -D__TOP_DIR__=\"$(TOPDIR)\" $(ROOT_INC)
EXTRALIBS += $(ROOT_LIB)
	#-Lvendor/yaml-cpp/lib -lyaml-cpp \
	#-Lvendor/mongo-cxx-driver-v2.0/lib -lmongoclient \
	#$(BOOSTLIB) $(ROOT_LIB)

ifndef G4INSTALL
  G4INSTALL = ../../..
endif

.PHONY: all vendor yaml-cpp mongo vendorclean
all: lib bin

vendor: yaml-cpp mongo

yaml-cpp:
	cd vendor/yaml-cpp; make -j2
mongo:
	cd vendor/mongo-cxx-driver-v2.0;scons -j2 --prefix . --extrapath $(BOOSTDIR)

include $(G4INSTALL)/config/binmake.gmk

visclean:
	rm -f g4*.prim g4*.eps g4*.wrl
	rm -f .DAWN_*

vendorclean:
	cd vendor/yaml-cpp;make clean
	cd vendor/mongo-cxx-driver-v2.0;scons -c;rm -f .sconsign.* lib/libmongoclient.a ;rm -rf sconf_temp