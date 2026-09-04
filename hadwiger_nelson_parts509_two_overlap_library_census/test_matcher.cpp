#include "witness_masks.hpp"
#include <iostream>

static bool brute(const std::vector<Colouring>& large,
                  const std::vector<Colouring>& small,
                  const Constraints& overlaps, const Constraints& edges) {
    for (const auto& l : large) {
        for (const auto& s : small) {
            std::array<std::uint8_t, 4> p{0, 1, 2, 3};
            do {
                bool works = true;
                for (auto [a, b] : overlaps) works &= l[a] == p[s[b]];
                for (auto [a, b] : edges) works &= l[a] != p[s[b]];
                if (works) return true;
            } while (std::next_permutation(p.begin(), p.end()));
        }
    }
    return false;
}

int main() {
    std::vector<Constraints> lists(1);
    for (std::size_t p = 0; p < 4; ++p) {
        for (std::size_t q = 0; q < 4; ++q) lists.push_back({{p, q}});
    }
    for (std::size_t first = 1; first <= 16; ++first) {
        for (std::size_t second = 1; second <= 16; ++second) {
            lists.push_back({lists[first][0], lists[second][0]});
        }
    }
    const std::vector<Colouring> large{{0, 1, 2, 3}, {0, 1, 0, 1}, {0, 0, 0, 0}};
    const std::vector<Colouring> pool{
        {0, 1, 2, 3}, {0, 0, 1, 2}, {0, 1, 0, 1}, {0, 1, 2, 0},
        {0, 0, 0, 0}, {0, 0, 1, 1}, {0, 1, 1, 2}, {0, 1, 2, 2}
    };
    std::uint64_t checked = 0, positive = 0, negative = 0;
    for (const std::size_t count : {1U, 3U, 8U}) {
        const std::vector<Colouring> small(pool.begin(), pool.begin() + count);
        const WitnessMasks masks(small);
        for (const auto& overlaps : lists) {
            for (const auto& edges : lists) {
                const auto actual = masks.find(large, overlaps, edges);
                const bool expected = brute(large, small, overlaps, edges);
                if (actual.has_value() != expected) {
                    throw std::runtime_error("mask/reference mismatch");
                }
                ++checked;
                if (expected) ++positive; else ++negative;
            }
        }
    }
    const std::vector<Colouring> singleton{{0, 1, 2, 3}};
    const WitnessMasks masks(singleton);
    const Constraints fixed{{0, 0}, {1, 1}, {2, 2}, {3, 3}};
    Constraints many(128, {0, 1});
    if (!masks.find(singleton, fixed, many)) throw std::runtime_error("long positive case");
    many.push_back({0, 0});
    if (masks.find(singleton, fixed, many)) throw std::runtime_error("late negative case");
    std::cout << "exhaustive_interface_cases=" << checked << '\n'
              << "positive=" << positive << " negative=" << negative << '\n'
              << "long_constraint_boundary_cases=2\n"
                 "mask_matcher_equals_explicit_permutations=true\n";
}
