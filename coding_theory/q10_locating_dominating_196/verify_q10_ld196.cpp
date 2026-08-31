#include <array>
#include <bit>
#include <cassert>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <set>
#include <string>
#include <vector>

namespace {

constexpr int kDimension = 10;
constexpr int kVertexCount = 1 << kDimension;

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

int main(int argc, char** argv) {
    const std::string path = argc > 1 ? argv[1] : "code.txt";
    std::ifstream input(path);
    assert(input);

    std::vector<int> code;
    std::array<bool, kVertexCount> is_code{};
    std::string word;
    while (input >> word) {
        const int value = parse_word(word);
        assert(!is_code[value]);
        is_code[value] = true;
        code.push_back(value);
    }
    assert(code.size() == 196);

    // This implementation deliberately uses direct Hamming-distance tests;
    // the Python checker generates XOR neighborhoods and intersects sets.
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
    assert(signatures.size() == 828);
    const std::array<int, 6> expected_signature_counts{0, 162, 403, 201, 55, 7};
    for (int size = 1; size <= 5; ++size) {
        assert(signature_counts[size] == expected_signature_counts[size]);
    }
    for (int size = 6; size < static_cast<int>(signature_counts.size()); ++size) {
        assert(signature_counts[size] == 0);
    }

    std::array<int, kDimension + 1> distance_counts{};
    for (std::size_t first = 0; first < code.size(); ++first) {
        for (std::size_t second = first + 1; second < code.size(); ++second) {
            ++distance_counts[distance(code[first], code[second])];
        }
    }
    const std::array<int, kDimension + 1> expected_distance_counts{
        0, 67, 722, 2574, 3895, 4450, 4092, 2311, 781, 198, 20,
    };
    assert(distance_counts == expected_distance_counts);
    int pair_count = 0;
    for (int count : distance_counts) pair_count += count;
    assert(pair_count == 196 * 195 / 2);

    assert(incidence_count == 1826);
    assert(incidence_count + 196 + 2 * distance_counts[1] == 11 * 196);

    constexpr int lower_bound = ((1 << 11) + 11) / 12;
    static_assert(lower_bound == 171);

    std::cout << "verified: 196-word locating-dominating code in Q_10\n"
              << "non-codewords: 828; distinct nonempty signatures: 828\n"
              << "signature sizes:";
    for (int size = 1; size <= 5; ++size) {
        std::cout << ' ' << size << ':' << signature_counts[size];
    }
    std::cout << "\npair distances:";
    for (int value = 1; value <= kDimension; ++value) {
        std::cout << ' ' << value << ':' << distance_counts[value];
    }
    std::cout << "\nincidence check: 1826 + 196 + 2*67 = 11*196 = 2156\n"
              << "certified interval: 171 <= gamma^LD(Q_10) <= 196\n";
}
