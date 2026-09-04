#include <algorithm>
#include <array>
#include <bit>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <stdexcept>
#include <vector>

namespace {

constexpr unsigned kOrder = 43;
using Parts = std::array<unsigned, 3>;

std::vector<unsigned> internal_degrees(unsigned length) {
    std::vector<unsigned> result;
    if (length % 2 == 0) {
        for (unsigned degree = 0; degree < length; ++degree) {
            result.push_back(degree);
        }
    } else {
        for (unsigned degree = 0; degree < length; degree += 2) {
            result.push_back(degree);
        }
    }
    return result;
}

bool reaches_degree_window(unsigned cross, unsigned length) {
    for (const unsigned internal : internal_degrees(length)) {
        if (18 <= cross + internal && cross + internal <= 24) {
            return true;
        }
    }
    return false;
}

bool degree_feasible(const Parts& parts) {
    const unsigned g01 = std::gcd(parts[0], parts[1]);
    const unsigned g02 = std::gcd(parts[0], parts[2]);
    const unsigned g12 = std::gcd(parts[1], parts[2]);
    for (unsigned k01 = 0; k01 <= g01; ++k01) {
        for (unsigned k02 = 0; k02 <= g02; ++k02) {
            for (unsigned k12 = 0; k12 <= g12; ++k12) {
                const unsigned d0 = k01 * parts[1] / g01 + k02 * parts[2] / g02;
                const unsigned d1 = k01 * parts[0] / g01 + k12 * parts[2] / g12;
                const unsigned d2 = k02 * parts[0] / g02 + k12 * parts[1] / g12;
                if (reaches_degree_window(d0, parts[0])
                    && reaches_degree_window(d1, parts[1])
                    && reaches_degree_window(d2, parts[2])) {
                    return true;
                }
            }
        }
    }
    return false;
}

unsigned predicted_edge_orbits(const Parts& parts) {
    return parts[0] / 2 + parts[1] / 2 + parts[2] / 2
        + std::gcd(parts[0], parts[1])
        + std::gcd(parts[0], parts[2])
        + std::gcd(parts[1], parts[2]);
}

unsigned advance(unsigned vertex, const Parts& parts) {
    unsigned start = 0;
    for (const unsigned length : parts) {
        if (vertex < start + length) {
            return start + (vertex - start + 1) % length;
        }
        start += length;
    }
    throw std::logic_error("vertex outside cycle partition");
}

std::array<std::array<unsigned, kOrder>, kOrder> edge_orbit_map(const Parts& parts) {
    std::array<std::array<unsigned, kOrder>, kOrder> orbit{};
    for (auto& row : orbit) {
        row.fill(999);
    }
    unsigned next_orbit = 0;
    for (unsigned x = 0; x < kOrder; ++x) {
        for (unsigned y = x + 1; y < kOrder; ++y) {
            if (orbit[x][y] != 999) {
                continue;
            }
            unsigned u = x;
            unsigned v = y;
            do {
                orbit[u][v] = next_orbit;
                orbit[v][u] = next_orbit;
                u = advance(u, parts);
                v = advance(v, parts);
                if (u > v) {
                    std::swap(u, v);
                }
            } while (u != x || v != y);
            ++next_orbit;
        }
    }
    if (next_orbit != predicted_edge_orbits(parts)) {
        throw std::logic_error("edge-orbit formula mismatch");
    }
    return orbit;
}

struct Classification {
    unsigned variables;
    std::uint64_t states;
    std::uint32_t distinct_masks;
    std::uint32_t minimum;
    std::uint64_t minimizers;
    std::uint32_t first_minimizer;
};

std::uint32_t direct_objective(
    const std::array<std::array<unsigned, kOrder>, kOrder>& orbit,
    std::uint32_t red
) {
    std::uint32_t monochromatic = 0;
    for (unsigned a = 0; a < kOrder; ++a) {
        for (unsigned b = a + 1; b < kOrder; ++b) {
            for (unsigned c = b + 1; c < kOrder; ++c) {
                for (unsigned d = c + 1; d < kOrder; ++d) {
                    for (unsigned e = d + 1; e < kOrder; ++e) {
                        const unsigned vertices[5]{a, b, c, d, e};
                        std::uint32_t mask = 0;
                        for (unsigned i = 0; i < 5; ++i) {
                            for (unsigned j = i + 1; j < 5; ++j) {
                                mask |= std::uint32_t{1} << orbit[vertices[i]][vertices[j]];
                            }
                        }
                        if ((red & mask) == 0 || (red & mask) == mask) {
                            ++monochromatic;
                        }
                    }
                }
            }
        }
    }
    return monochromatic;
}

Classification classify(const Parts& parts) {
    const unsigned variables = predicted_edge_orbits(parts);
    if (variables > 25) {
        throw std::invalid_argument("low-orbit classifier received more than 25 variables");
    }
    const std::uint32_t states = std::uint32_t{1} << variables;
    const std::uint32_t full = states - 1;
    auto orbit = edge_orbit_map(parts);
    std::vector<std::uint32_t> zeta(states, 0);
    std::uint64_t five_count = 0;
    for (unsigned a = 0; a < kOrder; ++a) {
        for (unsigned b = a + 1; b < kOrder; ++b) {
            for (unsigned c = b + 1; c < kOrder; ++c) {
                for (unsigned d = c + 1; d < kOrder; ++d) {
                    for (unsigned e = d + 1; e < kOrder; ++e) {
                        const unsigned vertices[5]{a, b, c, d, e};
                        std::uint32_t mask = 0;
                        for (unsigned i = 0; i < 5; ++i) {
                            for (unsigned j = i + 1; j < 5; ++j) {
                                mask |= std::uint32_t{1} << orbit[vertices[i]][vertices[j]];
                            }
                        }
                        ++zeta[mask];
                        ++five_count;
                    }
                }
            }
        }
    }
    if (five_count != 962598) {
        throw std::logic_error("five-set count mismatch");
    }
    const std::uint32_t distinct = static_cast<std::uint32_t>(std::count_if(
        zeta.begin(), zeta.end(), [](std::uint32_t value) { return value != 0; }
    ));
    for (unsigned bit = 0; bit < variables; ++bit) {
        const std::uint32_t flag = std::uint32_t{1} << bit;
        for (std::uint32_t mask = 0; mask < states; ++mask) {
            if ((mask & flag) != 0) {
                zeta[mask] += zeta[mask ^ flag];
                if (zeta[mask] > five_count) {
                    throw std::overflow_error("zeta entry exceeds five-set count");
                }
            }
        }
    }
    std::uint32_t minimum = 962599;
    std::uint64_t minimizers = 0;
    std::uint32_t first_minimizer = 0;
    for (std::uint32_t red = 0; red < states; ++red) {
        const std::uint32_t objective = zeta[red] + zeta[full ^ red];
        if (objective < minimum) {
            minimum = objective;
            minimizers = 1;
            first_minimizer = red;
        } else if (objective == minimum) {
            ++minimizers;
        }
    }
    if (direct_objective(orbit, first_minimizer) != minimum) {
        throw std::logic_error("direct minimizer recount mismatch");
    }
    return {variables, states, distinct, minimum, minimizers, first_minimizer};
}

}  // namespace

int main() {
    try {
        std::vector<Parts> partitions;
        unsigned infeasible = 0;
        unsigned feasible_high_orbit = 0;
        for (unsigned a = 1; a <= 14; ++a) {
            for (unsigned b = a; a + 2 * b <= kOrder; ++b) {
                const unsigned c = kOrder - a - b;
                if (b > c) {
                    continue;
                }
                const Parts parts{a, b, c};
                if (!degree_feasible(parts)) {
                    ++infeasible;
                } else if (predicted_edge_orbits(parts) <= 25) {
                    partitions.push_back(parts);
                } else {
                    ++feasible_high_orbit;
                }
            }
        }
        if (infeasible != 79 || partitions.size() != 26 || feasible_high_orbit != 49) {
            throw std::logic_error("three-cycle sieve census mismatch");
        }
        std::cout << "three_cycle_types=154 degree_infeasible=79 low_orbit_exact=26 high_orbit_open=49\n";
        for (const Parts& parts : partitions) {
            const Classification result = classify(parts);
            std::cout << "cycle_type=" << parts[0] << '+' << parts[1] << '+' << parts[2]
                      << " edge_orbits=" << result.variables
                      << " colorings=" << result.states
                      << " distinct_masks=" << result.distinct_masks
                      << " minimum_K5=" << result.minimum
                      << " minimizers=" << result.minimizers
                      << " first_minimizer=" << result.first_minimizer << '\n';
            std::cout.flush();
            if (result.minimum == 0) {
                std::cout << "TARGET_FOUND cycle_type=" << parts[0] << '+' << parts[1] << '+' << parts[2]
                          << " red_orbit_mask=" << result.first_minimizer << '\n';
                return 10;
            }
        }
        std::cout << "PASS all 26 low-orbit three-cycle types have positive minimum\n";
        return 0;
    } catch (const std::exception& error) {
        std::cerr << "ERROR: " << error.what() << '\n';
        return 1;
    }
}
