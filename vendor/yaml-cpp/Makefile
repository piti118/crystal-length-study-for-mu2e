SRCS = $(wildcard src/*.cpp)
OBJS = ${SRCS:.cpp=.o}

.PHONY: all lib test
all: lib

$(OBJS): %.o: %.cpp
	g++ -O3 -Iinclude -o $@ -c $< 
lib: $(OBJS)
	ar rcs lib/libyaml-cpp.a $^	
	ranlib lib/libyaml-cpp.a
clean::
	rm -f $(OBJS)
	rm -f lib/libyaml-cpp.a