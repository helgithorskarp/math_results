// Independent matching layer for the submitted exact geometric census.
//
// The production matcher fixes a large-gadget colouring and represents all
// colour permutations of the small library by bits.  This checker reverses
// those roles: it fixes a small-gadget colouring and represents all colour
// permutations of the large library.  Applying the inverse permutation to
// both sides proves that the two searches decide the same compatibility
// predicate.

#define WitnessMasks SubmittedWitnessMasks
#include "../hadwiger_nelson_parts509_two_overlap_library_census/witness_masks.hpp"
#undef WitnessMasks

class WitnessMasks {
    struct LargeEntry {
        Colouring colours;
        std::size_t original_row{};
    };

    std::vector<Colouring> small_;
    mutable bool ready_{};
    mutable std::size_t large_words_{};
    mutable std::vector<LargeEntry> large_entries_;
    mutable std::vector<std::array<std::vector<std::uint64_t>, 4>> large_equal_;

    void prepare_large(const std::vector<Colouring>& large) const {
        if (ready_) return;
        if (large.empty() || large.front().empty()) {
            throw std::runtime_error("empty large colour library");
        }
        for (std::size_t row = 0; row < large.size(); ++row) {
            if (large[row].size() != large.front().size()) {
                throw std::runtime_error("inconsistent large colour rows");
            }
            std::array<std::uint8_t, 4> permutation{0, 1, 2, 3};
            do {
                LargeEntry entry;
                entry.original_row = row;
                for (auto colour : large[row]) {
                    if (colour > 3) throw std::runtime_error("invalid large colour");
                    entry.colours.push_back(permutation[colour]);
                }
                large_entries_.push_back(std::move(entry));
            } while (std::next_permutation(permutation.begin(), permutation.end()));
        }
        large_words_ = (large_entries_.size() + 63) / 64;
        large_equal_.resize(large.front().size());
        for (auto& vertex : large_equal_) {
            for (auto& colour : vertex) colour.resize(large_words_);
        }
        for (std::size_t row = 0; row < large_entries_.size(); ++row) {
            for (std::size_t vertex = 0; vertex < large_entries_[row].colours.size(); ++vertex) {
                const auto colour = large_entries_[row].colours[vertex];
                large_equal_[vertex][colour][row / 64] |= UINT64_C(1) << (row % 64);
            }
        }
        ready_ = true;
    }

    bool valid_reverse(std::size_t large_row, std::size_t small_row,
                       const Constraints& overlaps, const Constraints& edges) const {
        const auto& large = large_entries_.at(large_row).colours;
        const auto& small = small_.at(small_row);
        for (const auto& [p, q] : overlaps) {
            if (large.at(p) != small.at(q)) return false;
        }
        for (const auto& [p, q] : edges) {
            if (large.at(p) == small.at(q)) return false;
        }
        return true;
    }

public:
    // census_all.cpp checks these two compatibility-layer dimensions.  They
    // retain their production meanings, although this checker does not use
    // the expanded-small rows for its decision.
    std::vector<Colouring> expanded;
    std::size_t words{};

    explicit WitnessMasks(const std::vector<Colouring>& small) : small_(small) {
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
                    if (colour > 3) throw std::runtime_error("invalid small colour");
                    renamed.push_back(permutation[colour]);
                }
                expanded.push_back(std::move(renamed));
            } while (std::next_permutation(permutation.begin(), permutation.end()));
        }
        words = (expanded.size() + 63) / 64;
    }

    std::optional<std::pair<std::size_t, std::size_t>> find(
        const std::vector<Colouring>& large, const Constraints& overlaps,
        const Constraints& edges
    ) const {
        prepare_large(large);
        for (std::size_t small_row = 0; small_row < small_.size(); ++small_row) {
            const auto& small = small_[small_row];
            for (std::size_t word = 0; word < large_words_; ++word) {
                std::uint64_t candidates = ~UINT64_C(0);
                if (word + 1 == large_words_ && large_entries_.size() % 64) {
                    candidates = (UINT64_C(1) << (large_entries_.size() % 64)) - 1;
                }
                for (const auto& [p, q] : overlaps) {
                    candidates &= large_equal_.at(p).at(small.at(q))[word];
                    if (!candidates) break;
                }
                if (!candidates) continue;
                for (const auto& [p, q] : edges) {
                    candidates &= ~large_equal_.at(p).at(small.at(q))[word];
                    if (!candidates) break;
                }
                if (!candidates) continue;
                const std::size_t large_row = 64 * word + std::countr_zero(candidates);
                if (!valid_reverse(large_row, small_row, overlaps, edges)) {
                    throw std::runtime_error("decoded reverse witness fails constraints");
                }
                return std::pair{large_entries_[large_row].original_row, small_row};
            }
        }
        return std::nullopt;
    }
};

#include "../hadwiger_nelson_parts509_two_overlap_library_census/census_all.cpp"
