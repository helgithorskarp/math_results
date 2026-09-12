CXX ?= g++
CXXFLAGS ?= -std=c++20 -O3 -march=native -Wall -Wextra -Wpedantic -Wconversion -Wshadow

BUILD_DIR := build
CPP_VERIFY := $(BUILD_DIR)/verify_cpp

.PHONY: all check sanitize clean

all: $(CPP_VERIFY)

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

$(CPP_VERIFY): verify.cpp | $(BUILD_DIR)
	$(CXX) $(CXXFLAGS) $< -o $@

check: all
	python3 construct.py > $(BUILD_DIR)/constructed.txt
	cmp code_32_8_8_1668.txt $(BUILD_DIR)/constructed.txt
	python3 verify.py ../a32_8_8_four_exchange/incumbent_1667.txt code_32_8_8_1668.txt exchange.json > $(BUILD_DIR)/python.txt
	cmp expected_python.txt $(BUILD_DIR)/python.txt
	$(CPP_VERIFY) code_32_8_8_1668.txt > $(BUILD_DIR)/cpp.txt
	cmp expected_cpp.txt $(BUILD_DIR)/cpp.txt
	sha256sum -c SHA256SUMS

sanitize: | $(BUILD_DIR)
	$(CXX) -std=c++20 -O1 -g -Wall -Wextra -Wpedantic -Wconversion -Wshadow -fsanitize=address,undefined -fno-omit-frame-pointer verify.cpp -o $(BUILD_DIR)/verify_san
	$(BUILD_DIR)/verify_san code_32_8_8_1668.txt > $(BUILD_DIR)/sanitized.txt
	cmp expected_cpp.txt $(BUILD_DIR)/sanitized.txt

clean:
	rm -rf $(BUILD_DIR)
