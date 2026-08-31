#include <algorithm>
#include <array>
#include <cassert>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <tuple>
#include <vector>

namespace {

constexpr int kRadius = 7;
constexpr int kMaximumSphereSize = 344;
constexpr int kMaximumOrder = 6 * kMaximumSphereSize;
constexpr int kMaximumThreeTorusOrder = kMaximumOrder / 2;

int cycle_distance(int value, int modulus) {
    return std::min(value, modulus - value);
}

int sphere_size(int first, int second, int third) {
    int result = 0;
    for (int x = 0; x < first; ++x) {
        for (int y = 0; y < second; ++y) {
            for (int z = 0; z < third; ++z) {
                const int base_distance = cycle_distance(x, first)
                                        + cycle_distance(y, second)
                                        + cycle_distance(z, third);
                result += (base_distance == kRadius);
                result += (base_distance + 1 == kRadius);
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

    int dimension_triples = 0;
    int eligible_dimension_triples = 0;
    int four_center_candidates = 0;
    int six_center_candidates = 0;
    std::vector<std::tuple<int, int, int, int, int>> candidates;

    for (int first = 3; first * first * first <= kMaximumThreeTorusOrder; ++first) {
        for (int second = first;
             first * second * second <= kMaximumThreeTorusOrder;
             ++second) {
            for (int third = second;
                 first * second * third <= kMaximumThreeTorusOrder;
                 ++third) {
                ++dimension_triples;
                const int order = 2 * first * second * third;
                if (order % 4 != 0 && order % 6 != 0) continue;
                ++eligible_dimension_triples;
                const int size = sphere_size(first, second, third);
                for (int centers : {4, 6}) {
                    if (centers * size != order) continue;
                    candidates.emplace_back(centers, first, second, third, size);
                    output << centers << ' ' << first << ' ' << second << ' '
                           << third << ' ' << size << '\n';
                    if (centers == 4) {
                        ++four_center_candidates;
                    } else {
                        ++six_center_candidates;
                    }
                }
            }
        }
    }

    const std::vector<std::tuple<int, int, int, int, int>> expected = {
        {6, 4, 9, 9, 108},
        {6, 6, 7, 11, 154},
        {6, 6, 9, 10, 180},
        {6, 8, 9, 9, 216},
    };
    assert(dimension_triples == 1106);
    assert(eligible_dimension_triples == 1074);
    assert(candidates == expected);
    assert(four_center_candidates == 0);
    assert(six_center_candidates == 4);

    std::cout << "radius=" << kRadius << '\n';
    std::cout << "maximum_group_order=" << kMaximumOrder << '\n';
    std::cout << "dimension_triples=" << dimension_triples << '\n';
    std::cout << "eligible_dimension_triples=" << eligible_dimension_triples << '\n';
    std::cout << "four_center_counting_candidates=" << four_center_candidates << '\n';
    std::cout << "six_center_counting_candidates=" << six_center_candidates << '\n';
}
