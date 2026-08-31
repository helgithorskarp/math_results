#include <algorithm>
#include <array>
#include <bit>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <set>
#include <string>
#include <vector>

namespace {

constexpr int kDimension = 8;
constexpr int kVertexCount = 1 << kDimension;

const std::array<const char*, 56> kWords = {
    "00000000", "00000011", "00001111", "00010101", "00010110", "00011001", "00011100",
    "00100110", "00101001", "00101010", "00110000", "00111011", "00111101", "01000110",
    "01001011", "01001101", "01010000", "01011010", "01011111", "01100010", "01100100",
    "01100111", "01101001", "01110001", "01110101", "01111000", "01111110", "10000010",
    "10000101", "10001000", "10001110", "10010001", "10010100", "10011111", "10100011",
    "10100101", "10101011", "10101100", "10110010", "10110111", "10111000", "10111111",
    "11000001", "11000101", "11000111", "11001000", "11010011", "11011010", "11011100",
    "11011101", "11100000", "11101101", "11101110", "11110000", "11110110", "11111011",
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
    assert(code.size() == 56);

    // This implementation deliberately constructs signatures by direct
    // Hamming-distance comparisons, rather than by intersecting precomputed
    // XOR neighborhoods as the Python checker does.
    std::set<std::vector<int>> seen;
    std::array<int, kDimension + 2> signature_counts{};
    std::int64_t incidence_count = 0;
    for (int vertex = 0; vertex < kVertexCount; ++vertex) {
        if (is_code[vertex]) continue;
        std::vector<int> signature;
        for (int codeword : code) {
            if (distance(vertex, codeword) <= 1) signature.push_back(codeword);
        }
        assert(!signature.empty());
        assert(seen.insert(signature).second);
        ++signature_counts[signature.size()];
        incidence_count += static_cast<std::int64_t>(signature.size());
    }
    assert(seen.size() == 200);
    assert(signature_counts[1] == 48);
    assert(signature_counts[2] == 95);
    assert(signature_counts[3] == 46);
    assert(signature_counts[4] == 9);
    assert(signature_counts[5] == 2);

    std::array<int, kDimension + 1> distance_counts{};
    for (std::size_t first = 0; first < code.size(); ++first) {
        for (std::size_t second = first + 1; second < code.size(); ++second) {
            ++distance_counts[distance(code[first], code[second])];
        }
    }
    const std::array<int, kDimension + 1> expected = {0, 13, 156, 405, 399, 321, 198, 44, 4};
    assert(distance_counts == expected);
    assert(incidence_count == 422);
    assert(incidence_count + 56 + 2 * distance_counts[1] == 9 * 56);

    // Exact integer form of ceil((8^2*2^9)/(8^3+2*8^2+3*8-2)) = 50.
    constexpr int numerator = 8 * 8 * 512;
    constexpr int denominator = 512 + 2 * 64 + 3 * 8 - 2;
    static_assert((numerator + denominator - 1) / denominator == 50);

    std::cout << "verified: 56-word locating-dominating code in Q_8\n"
              << "non-codewords: 200; distinct nonempty signatures: 200\n"
              << "signature sizes: 1:48 2:95 3:46 4:9 5:2\n"
              << "pair distances: 1:13 2:156 3:405 4:399 5:321 6:198 7:44 8:4\n"
              << "incidence check: 422 + 56 + 2*13 = 9*56 = 504\n"
              << "certified interval: 50 <= gamma^LD(Q_8) <= 56\n";
}
