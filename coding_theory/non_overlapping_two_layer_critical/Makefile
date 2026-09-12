CXX ?= g++
CXXFLAGS ?= -std=c++20 -O3 -Wall -Wextra -Wconversion -Wshadow

.PHONY: all check sanitize clean

all: two_layer_critical

two_layer_critical: two_layer_critical.cpp
	$(CXX) $(CXXFLAGS) -o $@ $<

check: two_layer_critical
	python3 verify.py --binary ./two_layer_critical

sanitize:
	$(CXX) -std=c++20 -O1 -g -Wall -Wextra -Wconversion -Wshadow \
		-fsanitize=address,undefined -fno-omit-frame-pointer \
		-o two_layer_critical.sanitize two_layer_critical.cpp
	./two_layer_critical.sanitize 18

clean:
	rm -f two_layer_critical two_layer_critical.sanitize
