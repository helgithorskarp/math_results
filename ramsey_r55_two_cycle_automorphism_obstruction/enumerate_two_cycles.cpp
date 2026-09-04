#include <algorithm>
#include <bit>
#include <cstdint>
#include <iostream>
#include <map>
#include <stdexcept>
#include <vector>

namespace {

constexpr unsigned kOrder = 43;
constexpr unsigned kVariables = 22;
constexpr std::uint32_t kStates = std::uint32_t{1} << kVariables;
constexpr std::uint32_t kFull = kStates - 1;

unsigned orbit_index(unsigned x, unsigned y, unsigned first_cycle) {
    const unsigned second_cycle = kOrder - first_cycle;
    const unsigned first_internal = first_cycle / 2;
    if (x < first_cycle && y < first_cycle) {
        const unsigned difference = y - x;
        return std::min(difference, first_cycle - difference) - 1;
    }
    if (x >= first_cycle && y >= first_cycle) {
        const unsigned local_x = x - first_cycle;
        const unsigned local_y = y - first_cycle;
        const unsigned difference = local_y - local_x;
        return first_internal + std::min(difference, second_cycle - difference) - 1;
    }
    return kVariables - 1;
}

std::uint32_t five_mask(
    unsigned a,
    unsigned b,
    unsigned c,
    unsigned d,
    unsigned e,
    unsigned first_cycle
) {
    const unsigned vertices[5]{a, b, c, d, e};
    std::uint32_t mask = 0;
    for (unsigned i = 0; i < 5; ++i) {
        for (unsigned j = i + 1; j < 5; ++j) {
            mask |= std::uint32_t{1} << orbit_index(vertices[i], vertices[j], first_cycle);
        }
    }
    return mask;
}

void classify(unsigned first_cycle) {
    const unsigned second_cycle = kOrder - first_cycle;
    if (first_cycle < 19 || first_cycle > 21) {
        throw std::invalid_argument("this exact scan is intended for first cycle 19, 20, or 21");
    }
    std::vector<std::uint32_t> zeta(kStates, 0);
    std::uint64_t total = 0;
    for (unsigned a = 0; a < kOrder; ++a) {
        for (unsigned b = a + 1; b < kOrder; ++b) {
            for (unsigned c = b + 1; c < kOrder; ++c) {
                for (unsigned d = c + 1; d < kOrder; ++d) {
                    for (unsigned e = d + 1; e < kOrder; ++e) {
                        ++zeta[five_mask(a, b, c, d, e, first_cycle)];
                        ++total;
                    }
                }
            }
        }
    }
    if (total != 962598) {
        throw std::logic_error("five-set count mismatch");
    }
    const auto distinct = std::count_if(zeta.begin(), zeta.end(), [](std::uint32_t x) {
        return x != 0;
    });
    for (unsigned bit = 0; bit < kVariables; ++bit) {
        const std::uint32_t flag = std::uint32_t{1} << bit;
        for (std::uint32_t mask = 0; mask < kStates; ++mask) {
            if ((mask & flag) != 0) {
                zeta[mask] += zeta[mask ^ flag];
                if (zeta[mask] > total) {
                    throw std::overflow_error("zeta entry exceeds total five-set count");
                }
            }
        }
    }
    std::uint32_t minimum = static_cast<std::uint32_t>(total + 1);
    std::vector<std::uint32_t> minimizers;
    for (std::uint32_t red = 0; red < kStates; ++red) {
        const std::uint32_t objective = zeta[red] + zeta[kFull ^ red];
        if (objective < minimum) {
            minimum = objective;
            minimizers.assign(1, red);
        } else if (objective == minimum) {
            minimizers.push_back(red);
        }
    }
    std::map<unsigned, std::uint64_t> size_histogram;
    std::map<std::pair<std::uint32_t, std::uint32_t>, std::uint64_t> color_histogram;
    for (const auto mask : minimizers) {
        ++size_histogram[std::popcount(mask)];
        ++color_histogram[{zeta[mask], zeta[kFull ^ mask]}];
    }

    std::cout << "cycle_type=" << first_cycle << '+' << second_cycle
              << " distinct_masks=" << distinct << " minimum_K5=" << minimum
              << " minimizers=" << minimizers.size();
    std::cout << " minimum_red_edge_orbits=";
    for (const auto& [size, count] : size_histogram) {
        std::cout << size << '^' << count << ',';
    }
    std::cout << " minimum_red_blue_K5=";
    for (const auto& [counts, multiplicity] : color_histogram) {
        std::cout << counts.first << '+' << counts.second << '^' << multiplicity << ',';
    }
    std::cout << '\n';
}

}  // namespace

int main() {
    try {
        for (const unsigned first_cycle : {19U, 20U, 21U}) {
            classify(first_cycle);
        }
        std::cout << "PASS complete two-cycle automorphism classification\n";
        return 0;
    } catch (const std::exception& error) {
        std::cerr << "ERROR: " << error.what() << '\n';
        return 1;
    }
}
