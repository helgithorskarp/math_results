#pragma once
#include <algorithm>
#include <array>
#include <bit>
#include <cstdint>
#include <optional>
#include <stdexcept>
#include <utility>
#include <vector>

using Colouring = std::vector<std::uint8_t>;
using Constraints = std::vector<std::pair<std::size_t, std::size_t>>;

// Each bit identifies an actual small-gadget colouring and colour permutation.
class WitnessMasks {
public:
    std::vector<Colouring> expanded;
    std::vector<std::array<std::vector<std::uint64_t>, 4>> equality;
    std::size_t words{};

    explicit WitnessMasks(const std::vector<Colouring>& small) {
        if (small.empty() || small.front().empty()) {
            throw std::runtime_error("empty small colour library");
        }
        for (const auto& row : small) {
            if (row.size() != small.front().size()) {
                throw std::runtime_error("inconsistent small colour rows");
            }
            std::array<std::uint8_t, 4> permutation{0, 1, 2, 3};
            do {
                Colouring renamed;
                for (auto colour : row) {
                    if (colour > 3) throw std::runtime_error("invalid colour");
                    renamed.push_back(permutation[colour]);
                }
                expanded.push_back(std::move(renamed));
            } while (std::next_permutation(permutation.begin(), permutation.end()));
        }
        words = (expanded.size() + 63) / 64;
        equality.resize(small.front().size());
        for (auto& vertex : equality) {
            for (auto& colour : vertex) colour.resize(words);
        }
        for (std::size_t row = 0; row < expanded.size(); ++row) {
            for (std::size_t vertex = 0; vertex < expanded[row].size(); ++vertex) {
                equality[vertex][expanded[row][vertex]][row / 64] |=
                    UINT64_C(1) << (row % 64);
            }
        }
    }

    bool valid(const Colouring& large, std::size_t small_row,
               const Constraints& overlaps, const Constraints& edges) const {
        if (small_row >= expanded.size()) return false;
        const auto& small = expanded[small_row];
        for (const auto& [p, q] : overlaps) {
            if (large.at(p) != small.at(q)) return false;
        }
        for (const auto& [p, q] : edges) {
            if (large.at(p) == small.at(q)) return false;
        }
        return true;
    }

    std::optional<std::pair<std::size_t, std::size_t>> find(
        const std::vector<Colouring>& large, const Constraints& overlaps,
        const Constraints& edges
    ) const {
        for (std::size_t row = 0; row < large.size(); ++row) {
            for (std::size_t word = 0; word < words; ++word) {
                std::uint64_t candidates = ~UINT64_C(0);
                if (word + 1 == words && expanded.size() % 64) {
                    candidates = (UINT64_C(1) << (expanded.size() % 64)) - 1;
                }
                for (const auto& [p, q] : overlaps) {
                    candidates &= equality.at(q).at(large[row].at(p))[word];
                    if (!candidates) break;
                }
                if (!candidates) continue;
                for (const auto& [p, q] : edges) {
                    candidates &= ~equality.at(q).at(large[row].at(p))[word];
                    if (!candidates) break;
                }
                if (!candidates) continue;
                const std::size_t small_row = 64 * word + std::countr_zero(candidates);
                if (!valid(large[row], small_row, overlaps, edges)) {
                    throw std::runtime_error("decoded colouring witness fails constraints");
                }
                return std::pair{row, small_row};
            }
        }
        return std::nullopt;
    }
};
