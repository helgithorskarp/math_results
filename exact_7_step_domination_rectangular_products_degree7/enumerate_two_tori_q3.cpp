#include <algorithm>
#include <bit>
#include <cassert>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <tuple>
#include <vector>

namespace {

constexpr int kRadius = 7;
constexpr int kMaximumSphereSize = 176;
constexpr int kMaximumOrder = 6 * kMaximumSphereSize;
constexpr int kMaximumTorusOrder = kMaximumOrder / 8;

int cycle_distance(int value, int modulus) {
    return std::min(value, modulus - value);
}

int sphere_size(int first, int second) {
    int result = 0;
    for (int x = 0; x < first; ++x) {
        for (int y = 0; y < second; ++y) {
            for (unsigned mask = 0; mask < 8; ++mask) {
                const int distance = cycle_distance(x, first)
                                   + cycle_distance(y, second)
                                   + std::popcount(mask);
                result += (distance == kRadius);
            }
        }
    }
    return result;
}

}  // namespace

int main(int argc, char** argv) {
    if (argc != 2) {
        std::cerr << "usage: enumerator /scratch/candidates.txt\n";
        return 2;
    }
    std::ofstream output(argv[1]);
    if (!output) throw std::runtime_error("cannot open candidate output");

    int dimension_pairs = 0;
    int four_center_candidates = 0;
    int six_center_candidates = 0;
    std::vector<std::tuple<int, int, int, int>> candidates;
    for (int first = 3; first * first <= kMaximumTorusOrder; ++first) {
        for (int second = first; first * second <= kMaximumTorusOrder; ++second) {
            ++dimension_pairs;
            const int order = 8 * first * second;
            const int size = sphere_size(first, second);
            for (int centers : {4, 6}) {
                if (centers * size != order) continue;
                candidates.emplace_back(centers, first, second, size);
                output << centers << ' ' << first << ' ' << second << ' '
                       << size << '\n';
                if (centers == 4) {
                    ++four_center_candidates;
                } else {
                    ++six_center_candidates;
                }
            }
        }
    }

    assert(dimension_pairs == 144);
    const std::vector<std::tuple<int, int, int, int>> expected = {
        {6, 9, 9, 108}
    };
    assert(candidates == expected);
    assert(four_center_candidates == 0);
    assert(six_center_candidates == 1);

    std::cout << "radius=" << kRadius << '\n';
    std::cout << "maximum_group_order=" << kMaximumOrder << '\n';
    std::cout << "dimension_pairs=" << dimension_pairs << '\n';
    std::cout << "four_center_counting_candidates=" << four_center_candidates << '\n';
    std::cout << "six_center_counting_candidates=" << six_center_candidates << '\n';
}
