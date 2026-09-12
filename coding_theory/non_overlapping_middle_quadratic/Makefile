CXX ?= g++
CXXFLAGS ?= -std=gnu++20 -O3 -DNDEBUG -Wall -Wextra -Wconversion -Wshadow
SANITIZE_FLAGS = -std=gnu++20 -O1 -g -Wall -Wextra -Wconversion -Wshadow \
	-fsanitize=address,undefined -fno-omit-frame-pointer

.PHONY: all check sanitize clean

all: middle_quadratic

middle_quadratic: middle_quadratic.cpp
	$(CXX) $(CXXFLAGS) $< -o $@

middle_quadratic.sanitize: middle_quadratic.cpp
	$(CXX) $(SANITIZE_FLAGS) $< -o $@

check: middle_quadratic
	python3 verify.py --binary ./middle_quadratic

sanitize: middle_quadratic.sanitize
	./middle_quadratic.sanitize 20 >/dev/null

clean:
	rm -f middle_quadratic middle_quadratic.sanitize
