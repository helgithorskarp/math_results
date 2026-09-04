#include <algorithm>
#include <array>
#include <bit>
#include <cstdint>
#include <iostream>
#include <map>
#include <stdexcept>
#include <tuple>
#include <unordered_map>
#include <vector>

namespace {

constexpr unsigned kOrder = 43;
constexpr unsigned kVariables = 22;
constexpr std::uint32_t kStates = std::uint32_t{1} << kVariables;
constexpr std::uint32_t kFull = kStates - 1;
using Edge = std::pair<unsigned, unsigned>;

Edge image(Edge edge, unsigned first_cycle) {
    auto advance = [first_cycle](unsigned vertex) {
        if (vertex < first_cycle) {
            return (vertex + 1) % first_cycle;
        }
        const unsigned second = kOrder - first_cycle;
        return first_cycle + (vertex - first_cycle + 1) % second;
    };
    edge = {advance(edge.first), advance(edge.second)};
    if (edge.first > edge.second) {
        std::swap(edge.first, edge.second);
    }
    return edge;
}

std::pair<std::vector<Edge>, std::map<Edge, unsigned>> explicit_edge_orbits(
    unsigned first_cycle
) {
    const unsigned second_cycle = kOrder - first_cycle;
    const unsigned action_order = first_cycle * second_cycle;
    std::vector<Edge> representatives;
    std::map<Edge, Edge> edge_to_representative;
    for (unsigned x = 0; x < kOrder; ++x) {
        for (unsigned y = x + 1; y < kOrder; ++y) {
            const Edge edge{x, y};
            Edge current = edge;
            Edge representative = edge;
            for (unsigned step = 0; step < action_order; ++step) {
                representative = std::min(representative, current);
                current = image(current, first_cycle);
            }
            if (current != edge) {
                throw std::logic_error("permutation orbit failed to close");
            }
            edge_to_representative[edge] = representative;
            representatives.push_back(representative);
        }
    }
    std::sort(representatives.begin(), representatives.end());
    representatives.erase(std::unique(representatives.begin(), representatives.end()), representatives.end());
    if (representatives.size() != kVariables) {
        throw std::logic_error("expected exactly 22 edge orbits");
    }
    std::map<Edge, unsigned> edge_to_variable;
    for (const auto& [edge, representative] : edge_to_representative) {
        const auto found = std::lower_bound(representatives.begin(), representatives.end(), representative);
        edge_to_variable[edge] = static_cast<unsigned>(found - representatives.begin());
    }
    return {representatives, edge_to_variable};
}

struct WeightedMask {
    std::uint32_t mask;
    std::uint32_t weight;
};

std::vector<WeightedMask> direct_mask_frequencies(unsigned first_cycle) {
    const auto [representatives, edge_to_variable] = explicit_edge_orbits(first_cycle);
    (void)representatives;
    std::unordered_map<std::uint32_t, std::uint32_t> frequencies;
    frequencies.reserve(4096);
    std::uint64_t total = 0;
    for (unsigned a = 0; a < kOrder; ++a) {
        for (unsigned b = a + 1; b < kOrder; ++b) {
            for (unsigned c = b + 1; c < kOrder; ++c) {
                for (unsigned d = c + 1; d < kOrder; ++d) {
                    for (unsigned e = d + 1; e < kOrder; ++e) {
                        const unsigned vertices[5]{a, b, c, d, e};
                        std::uint32_t mask = 0;
                        for (unsigned i = 0; i < 5; ++i) {
                            for (unsigned j = i + 1; j < 5; ++j) {
                                mask |= std::uint32_t{1}
                                    << edge_to_variable.at({vertices[i], vertices[j]});
                            }
                        }
                        ++frequencies[mask];
                        ++total;
                    }
                }
            }
        }
    }
    if (total != 962598) {
        throw std::logic_error("five-set count mismatch");
    }
    std::vector<WeightedMask> result;
    result.reserve(frequencies.size());
    for (const auto& [mask, weight] : frequencies) {
        result.push_back({mask, weight});
    }
    std::sort(result.begin(), result.end(), [](const auto& left, const auto& right) {
        if (left.weight != right.weight) {
            return left.weight > right.weight;
        }
        if (std::popcount(left.mask) != std::popcount(right.mask)) {
            return std::popcount(left.mask) < std::popcount(right.mask);
        }
        return left.mask < right.mask;
    });
    return result;
}

void classify(unsigned first_cycle) {
    const auto masks = direct_mask_frequencies(first_cycle);
    std::uint32_t best = 962599;
    std::uint64_t minimizing_count = 0;
    std::map<unsigned, std::uint64_t> size_histogram;
    std::map<std::pair<std::uint32_t, std::uint32_t>, std::uint64_t> color_histogram;

    // Fix variable zero red.  Color complementation supplies the other member
    // of each pair and is restored in all reported counts.
    for (std::uint32_t red = 1; red < kStates; red += 2) {
        std::uint32_t red_fives = 0;
        std::uint32_t blue_fives = 0;
        for (const auto& item : masks) {
            const std::uint32_t intersection = red & item.mask;
            if (intersection == item.mask) {
                red_fives += item.weight;
            } else if (intersection == 0) {
                blue_fives += item.weight;
            }
            if (red_fives + blue_fives > best) {
                break;
            }
        }
        const std::uint32_t objective = red_fives + blue_fives;
        if (objective > best) {
            continue;
        }
        if (objective < best) {
            best = objective;
            minimizing_count = 0;
            size_histogram.clear();
            color_histogram.clear();
        }
        minimizing_count += 2;
        ++size_histogram[std::popcount(red)];
        ++size_histogram[kVariables - std::popcount(red)];
        ++color_histogram[{red_fives, blue_fives}];
        ++color_histogram[{blue_fives, red_fives}];
    }

    std::cout << "cycle_type=" << first_cycle << '+' << kOrder - first_cycle
              << " distinct_masks=" << masks.size() << " minimum_K5=" << best
              << " minimizers=" << minimizing_count << " minimum_red_edge_orbits=";
    for (const auto& [size, count] : size_histogram) {
        std::cout << size << '^' << count << ',';
    }
    std::cout << " minimum_red_blue_K5=";
    for (const auto& [counts, count] : color_histogram) {
        std::cout << counts.first << '+' << counts.second << '^' << count << ',';
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
