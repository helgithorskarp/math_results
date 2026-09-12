CXX ?= g++
CXXFLAGS ?= -O3 -DNDEBUG -std=c++20 -Wall -Wextra -Wpedantic -Werror
CADICAL_ROOT ?=
BUILD := build
PRODUCER := $(BUILD)/cegis

.PHONY: all check sanitize verify42 calibration pilot clean

all: $(PRODUCER)

$(PRODUCER): cegis.cpp
	@test -f "$(CADICAL_ROOT)/src/cadical.hpp" || (echo "set CADICAL_ROOT to a CaDiCaL 1.9.5 source/build tree"; exit 2)
	@test -f "$(CADICAL_ROOT)/build/libcadical.a" || (echo "build libcadical.a under CADICAL_ROOT first"; exit 2)
	mkdir -p $(BUILD)
	$(CXX) $(CXXFLAGS) -I$(CADICAL_ROOT)/src $< \
		$(CADICAL_ROOT)/build/libcadical.a -pthread -o $@

verify42:
	python3 -B verify.py --graph6 fixtures/good42.g6 --expect good

calibration: $(PRODUCER)
	python3 -B check_calibration.py $(PRODUCER)

check: $(PRODUCER)
	$(PRODUCER) --cardinality-self-test
	python3 -B controls.py
	python3 -B -O controls.py
	python3 -B check_calibration.py $(PRODUCER)
	python3 -B resume_control.py $(PRODUCER)
	sha256sum -c SHA256SUMS

sanitize: cegis.cpp
	@test -f "$(CADICAL_ROOT)/src/cadical.hpp" || (echo "set CADICAL_ROOT"; exit 2)
	@test -f "$(CADICAL_ROOT)/build/libcadical.a" || (echo "build CaDiCaL first"; exit 2)
	mkdir -p $(BUILD)
	$(CXX) -O1 -g -std=c++20 -Wall -Wextra -Wpedantic -Werror \
		-fsanitize=address,undefined -fno-omit-frame-pointer \
		-I$(CADICAL_ROOT)/src $< $(CADICAL_ROOT)/build/libcadical.a \
		-pthread -o $(BUILD)/cegis-sanitize
	ASAN_OPTIONS=detect_leaks=1 $(BUILD)/cegis-sanitize --cardinality-self-test
	ASAN_OPTIONS=detect_leaks=1 $(BUILD)/cegis-sanitize 20 20 40 50 1000

pilot: $(PRODUCER)
	@test -n "$(WORK)" || (echo "set WORK to a new directory outside the checkout"; exit 2)
	python3 -B run_portfolio.py $(PRODUCER) "$(WORK)" --rounds 120 --jobs 4
	python3 -B check_target_pilot.py "$(WORK)/summary.json" target_pilot.json

clean:
	$(RM) -r $(BUILD)
