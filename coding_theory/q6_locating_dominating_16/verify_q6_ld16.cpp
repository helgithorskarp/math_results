#include <algorithm>
#include <array>
#include <cassert>
#include <iostream>
#include <map>
#include <set>
#include <vector>

int main() {
    constexpr int n = 6;
    const std::array<int, 16> listed = {
        0, 5, 11, 14, 18, 23, 25, 28,
        34, 36, 41, 47, 51, 53, 56, 62,
    };
    const std::set<int> code(listed.begin(), listed.end());

    // Independently reconstruct the algebraically specified code.
    std::set<int> generated;
    for (int a = 0; a < 2; ++a)
        for (int b = 0; b < 2; ++b)
            for (int c = 0; c < 2; ++c)
                for (int f = 0; f < 2; ++f) {
                    const int e = a ^ b ^ c ^ f;
                    const int d = a ^ c ^ f ^ (a & f) ^ (b & f);
                    generated.insert(a | (b << 1) | (c << 2) |
                                     (d << 3) | (e << 4) | (f << 5));
                }
    assert(generated == code);

    std::set<std::vector<int>> signatures;
    std::map<int, int> size_distribution;
    for (int vertex = 0; vertex < (1 << n); ++vertex) {
        if (code.count(vertex) != 0) continue;
        std::vector<int> signature;
        if (code.count(vertex) != 0) signature.push_back(vertex);
        for (int coordinate = 0; coordinate < n; ++coordinate) {
            const int neighbor = vertex ^ (1 << coordinate);
            if (code.count(neighbor) != 0) signature.push_back(neighbor);
        }
        std::sort(signature.begin(), signature.end());
        assert(!signature.empty());
        assert(signatures.insert(signature).second);
        ++size_distribution[static_cast<int>(signature.size())];
    }
    assert(signatures.size() == 48);
    const std::map<int, int> expected_distribution = {{1, 16}, {2, 16}, {3, 16}};
    assert(size_distribution == expected_distribution);

    const int numerator = n * n * (1 << (n + 1));
    const int denominator = n * n * n + 2 * n * n + 3 * n - 2;
    const int lower_ceiling = (numerator + denominator - 1) / denominator;
    assert(lower_ceiling == 16);

    std::cout << "code size: " << code.size() << '\n'
              << "non-codeword signatures: " << signatures.size()
              << " distinct, 0 empty\n"
              << "signature-size distribution: 1:16 2:16 3:16\n"
              << "published lower-bound ceiling at n=6: " << lower_ceiling << '\n'
              << "verified: gamma^LD(Q_6) = 16\n";
}
