#include <array>
#include <bit>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <set>
#include <string>
#include <vector>

namespace {

constexpr int kDimension = 9;
constexpr int kVertexCount = 1 << kDimension;

const std::array<const char*, 104> kWords = {
    "000000011", "000000111", "000001001", "000001110", "000010000", "000011010",
    "000100001", "000100100", "000101010", "000101100", "000110110", "000111011",
    "000111101", "001000100", "001000111", "001001010", "001010010", "001011100",
    "001011101", "001100000", "001100110", "001101101", "001110001", "001110101",
    "001111000", "001111111", "010000010", "010001101", "010010100", "010010101",
    "010011001", "010100011", "010100100", "010101000", "010101111", "010110000",
    "010110111", "010111110", "011000001", "011000110", "011001000", "011001011",
    "011010011", "011010100", "011011111", "011100100", "011100101", "011101011",
    "011110010", "011111001", "011111010", "011111100", "100000010", "100000101",
    "100001111", "100010001", "100010110", "100011100", "100011111", "100100000",
    "100100111", "100101001", "100110011", "100111010", "100111110", "101001001",
    "101001100", "101001111", "101010000", "101010011", "101011011", "101100011",
    "101100110", "101110011", "101110100", "101110101", "101111010", "101111101",
    "110000001", "110000100", "110000111", "110001000", "110001010", "110010010",
    "110011011", "110011100", "110100010", "110101101", "110110101", "110111001",
    "110111110", "111000010", "111000111", "111001101", "111010101", "111011000",
    "111011110", "111100001", "111101000", "111101011", "111101110", "111110000",
    "111110110", "111111111",
};

int parse_word(const std::string& word) {
    assert(word.size() == kDimension);
    int value = 0;
    for (char bit : word) {
        assert(bit == '0' || bit == '1');
        value = 2 * value + (bit - '0');
    }
    return value;
}

int distance(int first, int second) {
    return std::popcount(static_cast<unsigned>(first ^ second));
}

}  // namespace

int main() {
    std::vector<int> code;
    std::array<bool, kVertexCount> is_code{};
    for (const char* word : kWords) {
        const int value = parse_word(word);
        assert(!is_code[value]);
        is_code[value] = true;
        code.push_back(value);
    }
    assert(code.size() == 104);

    // Deliberately use direct Hamming-distance comparisons rather than the
    // XOR-neighborhood/set-intersection method of the Python checker.
    std::set<std::vector<int>> signatures;
    std::array<int, kDimension + 2> signature_counts{};
    std::int64_t incidence_count = 0;
    for (int vertex = 0; vertex < kVertexCount; ++vertex) {
        if (is_code[vertex]) continue;
        std::vector<int> signature;
        for (int codeword : code) {
            if (distance(vertex, codeword) <= 1) signature.push_back(codeword);
        }
        assert(!signature.empty());
        assert(signatures.insert(signature).second);
        ++signature_counts[signature.size()];
        incidence_count += static_cast<std::int64_t>(signature.size());
    }
    assert(signatures.size() == 408);

    std::array<int, kDimension + 1> distance_counts{};
    for (std::size_t first = 0; first < code.size(); ++first) {
        for (std::size_t second = first + 1; second < code.size(); ++second) {
            ++distance_counts[distance(code[first], code[second])];
        }
    }
    int pair_count = 0;
    for (int count : distance_counts) pair_count += count;
    assert(pair_count == 104 * 103 / 2);
    assert(incidence_count + 104 + 2 * distance_counts[1] == 10 * 104);

    constexpr int numerator = 9 * 9 * 1024;
    constexpr int denominator = 9 * 9 * 9 + 2 * 9 * 9 + 3 * 9 - 2;
    static_assert(numerator == 82944 && denominator == 916);
    static_assert((numerator + denominator - 1) / denominator == 91);

    std::cout << "verified: 104-word locating-dominating code in Q_9\n"
              << "non-codewords: 408; distinct nonempty signatures: 408\n"
              << "signature sizes:";
    for (int size = 1; size < static_cast<int>(signature_counts.size()); ++size) {
        if (signature_counts[size] != 0) std::cout << ' ' << size << ':' << signature_counts[size];
    }
    std::cout << "\npair distances:";
    for (int value = 1; value <= kDimension; ++value) {
        std::cout << ' ' << value << ':' << distance_counts[value];
    }
    std::cout << "\nincidence check: " << incidence_count << " + 104 + 2*"
              << distance_counts[1] << " = 10*104 = 1040\n"
              << "certified interval: 91 <= gamma^LD(Q_9) <= 104\n";
}
