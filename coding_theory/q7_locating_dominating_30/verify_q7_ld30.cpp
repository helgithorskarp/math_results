#include <algorithm>
#include <array>
#include <cassert>
#include <iostream>
#include <map>
#include <set>
#include <vector>

int main() {
    constexpr int n = 7;
    const std::array<int, 30> listed = {
        0, 6, 11, 19, 21, 26, 29, 34, 37, 40,
        47, 48, 55, 57, 60, 66, 71, 73, 76, 85,
        86, 88, 95, 97, 100, 107, 110, 119, 122, 125,
    };
    const std::set<int> code(listed.begin(), listed.end());
    assert(code.size() == 30);

    std::set<std::vector<int>> signatures;
    std::map<int, int> signature_sizes;
    for (int vertex = 0; vertex < (1 << n); ++vertex) {
        if (code.count(vertex) != 0) continue;
        std::vector<int> signature;
        for (int coordinate = 0; coordinate < n; ++coordinate) {
            const int neighbor = vertex ^ (1 << coordinate);
            if (code.count(neighbor) != 0) signature.push_back(neighbor);
        }
        assert(!signature.empty());
        std::sort(signature.begin(), signature.end());
        assert(signatures.insert(signature).second);
        ++signature_sizes[static_cast<int>(signature.size())];
    }
    assert(signatures.size() == 98);
    const std::map<int, int> expected_sizes = {
        {1, 22}, {2, 54}, {3, 15}, {4, 6}, {5, 1},
    };
    assert(signature_sizes == expected_sizes);

    std::map<int, int> pair_distances;
    for (std::size_t first = 0; first < listed.size(); ++first)
        for (std::size_t second = first + 1; second < listed.size(); ++second)
            ++pair_distances[__builtin_popcount(
                static_cast<unsigned>(listed[first] ^ listed[second]))];
    const std::map<int, int> expected_distances = {
        {1, 3}, {2, 73}, {3, 156}, {4, 98}, {5, 66}, {6, 39},
    };
    assert(pair_distances == expected_distances);

    const int numerator = n * n * (1 << (n + 1));
    const int denominator = n * n * n + 2 * n * n + 3 * n - 2;
    assert(numerator == 12544);
    assert(denominator == 460);
    const int lower_ceiling = (numerator + denominator - 1) / denominator;
    assert(lower_ceiling == 28);

    std::cout << "code size: " << code.size() << '\n'
              << "non-codeword signatures: " << signatures.size()
              << " distinct, 0 empty\n"
              << "signature-size distribution: 1:22 2:54 3:15 4:6 5:1\n"
              << "unordered pair-distance distribution: "
              << "1:3 2:73 3:156 4:98 5:66 6:39\n"
              << "published lower-bound ceiling at n=7: " << lower_ceiling << '\n'
              << "verified: 28 <= gamma^LD(Q_7) <= 30\n";
}
