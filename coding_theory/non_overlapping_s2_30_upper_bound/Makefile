CXX ?= g++
CXXFLAGS ?= -std=c++20 -O3 -Wall -Wextra -Wconversion -Wshadow

.PHONY: all check sanitize proof30 clean

all: quadratic_box_bound

quadratic_box_bound: quadratic_box_bound.cpp
	$(CXX) $(CXXFLAGS) -o $@ $<

check: quadratic_box_bound
	python3 verify.py --binary ./quadratic_box_bound

sanitize:
	$(CXX) -std=c++20 -O1 -g -Wall -Wextra -Wconversion -Wshadow \
		-fsanitize=address,undefined -fno-omit-frame-pointer \
		-o quadratic_box_bound.sanitize quadratic_box_bound.cpp
	./quadratic_box_bound.sanitize 22 4

proof30: quadratic_box_bound
	python3 run_shards.py --binary ./quadratic_box_bound --n 30 \
		--free-layers 4 --shards 12 --expected expected_n30.json

clean:
	rm -f quadratic_box_bound quadratic_box_bound.sanitize
