#include <algorithm>
#include <array>
#include <bit>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <stdexcept>
#include <string>
#include <unordered_set>
#include <vector>

namespace {

std::vector<std::uint32_t> load_code(const std::string& path) {
    std::ifstream input(path);
    if (!input) {
        throw std::runtime_error("cannot open code file");
    }
    std::vector<std::uint32_t> words;
    std::string line;
    int line_number = 0;
    while (std::getline(input, line)) {
        ++line_number;
        if (!line.empty() && line.back() == '\r') {
            line.pop_back();
        }
        if (line.empty()) {
            continue;
        }
        if (line.size() != 32) {
            throw std::runtime_error("line length is not 32 at line " + std::to_string(line_number));
        }
        std::uint32_t word = 0;
        for (int coordinate = 0; coordinate < 32; ++coordinate) {
            if (line[static_cast<std::size_t>(coordinate)] == '1') {
                word |= std::uint32_t{1} << coordinate;
            } else if (line[static_cast<std::size_t>(coordinate)] != '0') {
                throw std::runtime_error("nonbinary character at line " + std::to_string(line_number));
            }
        }
        words.push_back(word);
    }
    return words;
}

}  // namespace

int main(int argc, char** argv) {
    try {
        if (argc != 2) {
            std::cerr << "usage: " << argv[0] << " CODE\n";
            return 2;
        }
        const std::vector<std::uint32_t> code = load_code(argv[1]);
        if (code.size() != 1668) {
            throw std::runtime_error("code size is not 1668");
        }
        std::unordered_set<std::uint32_t> distinct;
        distinct.reserve(code.size());
        for (std::uint32_t word : code) {
            if (std::popcount(word) != 8) {
                throw std::runtime_error("word weight is not eight");
            }
            if (!distinct.insert(word).second) {
                throw std::runtime_error("duplicate codeword");
            }
        }

        int minimum_distance = 33;
        std::map<int, std::uint64_t> histogram;
        std::uint64_t pairs = 0;
        for (std::size_t first = 0; first < code.size(); ++first) {
            for (std::size_t second = first + 1; second < code.size(); ++second) {
                const int distance = std::popcount(code[first] ^ code[second]);
                minimum_distance = std::min(minimum_distance, distance);
                ++histogram[distance];
                ++pairs;
            }
        }
        if (minimum_distance < 8 || pairs != 1'390'278) {
            throw std::runtime_error("distance verification failed");
        }

        std::cout << "constructed_size=" << code.size() << '\n';
        std::cout << "distinct_words=" << distinct.size() << '\n';
        std::cout << "constant_weight=8\n";
        std::cout << "pairs_checked=" << pairs << '\n';
        std::cout << "minimum_distance=" << minimum_distance << '\n';
        std::cout << "distance_histogram=";
        bool first_entry = true;
        for (const auto& [distance, count] : histogram) {
            if (!first_entry) {
                std::cout << ',';
            }
            first_entry = false;
            std::cout << distance << ':' << count;
        }
        std::cout << '\n';
        std::cout << "verification=PASS\n";
        return 0;
    } catch (const std::exception& error) {
        std::cerr << "error: " << error.what() << '\n';
        return 1;
    }
}
