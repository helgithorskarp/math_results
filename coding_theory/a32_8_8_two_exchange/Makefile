CXX ?= g++
CXXFLAGS ?= -std=c++20 -O3 -march=native -Wall -Wextra -Wpedantic -Wconversion -Wshadow

BUILD_DIR := build
PROGRAM := $(BUILD_DIR)/exchange_profile
SANITIZED := $(BUILD_DIR)/exchange_profile_san

.PHONY: all check sanitize clean

all: $(PROGRAM)

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

$(PROGRAM): exchange_profile.cpp | $(BUILD_DIR)
	$(CXX) $(CXXFLAGS) $< -o $@

check: $(PROGRAM)
	$(PROGRAM) --self-test
	$(PROGRAM) --analyze incumbent_1667.txt $(BUILD_DIR)/low_candidates.tsv > $(BUILD_DIR)/analysis.txt 2> $(BUILD_DIR)/analysis.stderr.txt
	cmp expected_analysis.txt $(BUILD_DIR)/analysis.txt
	cmp low_candidates.tsv $(BUILD_DIR)/low_candidates.tsv
	python3 verify_exchange.py incumbent_1667.txt low_candidates.tsv > $(BUILD_DIR)/verification.txt
	cmp expected_verification.txt $(BUILD_DIR)/verification.txt
	sha256sum -c SHA256SUMS

$(SANITIZED): exchange_profile.cpp | $(BUILD_DIR)
	$(CXX) -std=c++20 -O1 -g -Wall -Wextra -Wpedantic -Wconversion -Wshadow \
		-fsanitize=address,undefined -fno-omit-frame-pointer $< -o $@

sanitize: $(SANITIZED)
	$(SANITIZED) --self-test
	$(SANITIZED) --analyze incumbent_1667.txt $(BUILD_DIR)/low_candidates_san.tsv > $(BUILD_DIR)/analysis_san.txt 2> $(BUILD_DIR)/analysis_san.stderr.txt
	cmp expected_analysis.txt $(BUILD_DIR)/analysis_san.txt
	cmp low_candidates.tsv $(BUILD_DIR)/low_candidates_san.tsv

clean:
	rm -rf $(BUILD_DIR)
