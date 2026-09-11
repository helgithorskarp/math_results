CXX ?= g++
CXXFLAGS ?= -std=c++20 -O3 -march=native -Wall -Wextra -Wpedantic -Wconversion -Wshadow

BUILD_DIR := build
ANALYSIS3 := $(BUILD_DIR)/blocker_analysis3
PROFILE4 := $(BUILD_DIR)/blocker_profile4
RADIUS4 := $(BUILD_DIR)/enumerate_radius_four

.PHONY: all check sanitize clean

all: $(ANALYSIS3) $(PROFILE4) $(RADIUS4)

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

$(ANALYSIS3): blocker_analysis.cpp | $(BUILD_DIR)
	$(CXX) $(CXXFLAGS) $< -o $@

$(PROFILE4): blocker_analysis.cpp | $(BUILD_DIR)
	$(CXX) $(CXXFLAGS) -DBLOCKER_THRESHOLD=4 $< -o $@

$(RADIUS4): enumerate_radius_four.cpp | $(BUILD_DIR)
	$(CXX) $(CXXFLAGS) $< -o $@

check: all
	$(ANALYSIS3) --self-test
	$(ANALYSIS3) --analyze incumbent_1667.txt $(BUILD_DIR)/low3.tsv > $(BUILD_DIR)/analysis3.txt 2> $(BUILD_DIR)/analysis3.stderr.txt
	cmp expected_analysis3.txt $(BUILD_DIR)/analysis3.txt
	cmp low3_candidates.tsv $(BUILD_DIR)/low3.tsv
	$(PROFILE4) --analyze incumbent_1667.txt $(BUILD_DIR)/low4.tsv > $(BUILD_DIR)/analysis4.txt 2> $(BUILD_DIR)/analysis4.stderr.txt
	cmp expected_analysis4.txt $(BUILD_DIR)/analysis4.txt
	cmp low4_candidates.tsv $(BUILD_DIR)/low4.tsv
	$(RADIUS4) low4_candidates.tsv > $(BUILD_DIR)/radius4.txt 2> $(BUILD_DIR)/radius4.stderr.txt
	cmp expected_radius4.txt $(BUILD_DIR)/radius4.txt
	python3 verify_radius_three.py incumbent_1667.txt low3_candidates.tsv low4_candidates.tsv > $(BUILD_DIR)/verify3.txt
	cmp expected_verify3.txt $(BUILD_DIR)/verify3.txt
	python3 audit_radius_four_sets.py low4_candidates.tsv > $(BUILD_DIR)/audit4.txt 2> $(BUILD_DIR)/audit4.stderr.txt
	cmp expected_audit4.txt $(BUILD_DIR)/audit4.txt
	sha256sum -c SHA256SUMS

sanitize: | $(BUILD_DIR)
	$(CXX) -std=c++20 -O1 -g -Wall -Wextra -Wpedantic -Wconversion -Wshadow -fsanitize=address,undefined -fno-omit-frame-pointer blocker_analysis.cpp -o $(BUILD_DIR)/analysis3_san
	$(CXX) -std=c++20 -O1 -g -Wall -Wextra -Wpedantic -Wconversion -Wshadow -fsanitize=address,undefined -fno-omit-frame-pointer -DBLOCKER_THRESHOLD=4 blocker_analysis.cpp -o $(BUILD_DIR)/profile4_san
	$(CXX) -std=c++20 -O1 -g -Wall -Wextra -Wpedantic -Wconversion -Wshadow -fsanitize=address,undefined -fno-omit-frame-pointer enumerate_radius_four.cpp -o $(BUILD_DIR)/radius4_san
	$(BUILD_DIR)/analysis3_san --self-test
	$(BUILD_DIR)/analysis3_san --analyze incumbent_1667.txt $(BUILD_DIR)/low3_san.tsv > $(BUILD_DIR)/analysis3_san.txt 2> $(BUILD_DIR)/analysis3_san.stderr.txt
	cmp expected_analysis3.txt $(BUILD_DIR)/analysis3_san.txt
	cmp low3_candidates.tsv $(BUILD_DIR)/low3_san.tsv
	$(BUILD_DIR)/profile4_san --analyze incumbent_1667.txt $(BUILD_DIR)/low4_san.tsv > $(BUILD_DIR)/analysis4_san.txt 2> $(BUILD_DIR)/analysis4_san.stderr.txt
	cmp expected_analysis4.txt $(BUILD_DIR)/analysis4_san.txt
	cmp low4_candidates.tsv $(BUILD_DIR)/low4_san.tsv
	$(BUILD_DIR)/radius4_san low4_candidates.tsv > $(BUILD_DIR)/radius4_san.txt 2> $(BUILD_DIR)/radius4_san.stderr.txt
	cmp expected_radius4.txt $(BUILD_DIR)/radius4_san.txt

clean:
	rm -rf $(BUILD_DIR)
