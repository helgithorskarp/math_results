#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <unordered_set>
#include <vector>

using Mask = std::array<std::uint64_t, 3>;

struct State {
    Mask remaining;
    std::uint8_t capacity;
    bool operator==(const State& other) const {
        return remaining == other.remaining && capacity == other.capacity;
    }
};

struct StateHash {
    std::size_t operator()(const State& state) const {
        std::uint64_t value = state.remaining[0] ^
            (state.remaining[1] + 0x9e3779b97f4a7c15ULL +
             (state.remaining[0] << 6) + (state.remaining[0] >> 2));
        value ^= state.remaining[2] + 0x9e3779b97f4a7c15ULL +
                 (value << 6) + (value >> 2);
        value ^= static_cast<std::uint64_t>(state.capacity) *
                 0x94d049bb133111ebULL;
        return static_cast<std::size_t>(value);
    }
};

int width;
std::vector<Mask> singletons;
std::vector<Mask> pairs;
std::vector<std::vector<int>> singleton_hits;
std::vector<std::vector<int>> pair_hits;
std::vector<int> singleton_order;
std::vector<int> pair_order;
std::unordered_set<State, StateHash> failed;
std::uint64_t calls = 0;
std::uint64_t cache_hits = 0;

bool empty(const Mask& mask) {
    return mask[0] == 0 && mask[1] == 0 && mask[2] == 0;
}

bool contains(const Mask& mask, int bit) {
    return ((mask[bit / 64] >> (bit % 64)) & 1U) != 0;
}

Mask remove(const Mask& remaining, const Mask& covered) {
    return {remaining[0] & ~covered[0], remaining[1] & ~covered[1],
            remaining[2] & ~covered[2]};
}

bool singleton_cover(const Mask& remaining, int capacity) {
    ++calls;
    if (empty(remaining)) {
        return true;
    }
    if (capacity == 0) {
        return false;
    }
    State state{remaining, static_cast<std::uint8_t>(capacity)};
    if (capacity > 1 && failed.find(state) != failed.end()) {
        ++cache_hits;
        return false;
    }
    int pivot = -1;
    for (int bit : singleton_order) {
        if (contains(remaining, bit)) {
            pivot = bit;
            break;
        }
    }
    if (pivot < 0) {
        return true;
    }
    for (int index : singleton_hits[pivot]) {
        if (singleton_cover(remove(remaining, singletons[index]), capacity - 1)) {
            return true;
        }
    }
    if (capacity > 1) {
        failed.insert(state);
    }
    return false;
}

int main(int argc, char** argv) {
    if (argc != 2) {
        return 2;
    }
    std::ifstream input(argv[1]);
    int singleton_count;
    int pair_count;
    input >> width >> singleton_count >> pair_count;
    if (!input || width < 1 || width > 192 || singleton_count < 0 || pair_count < 0) {
        return 3;
    }
    singletons.resize(singleton_count);
    pairs.resize(pair_count);
    for (Mask& mask : singletons) {
        input >> mask[0] >> mask[1] >> mask[2];
    }
    for (Mask& mask : pairs) {
        input >> mask[0] >> mask[1] >> mask[2];
    }
    if (!input) {
        return 4;
    }
    singleton_hits.resize(width);
    pair_hits.resize(width);
    for (int index = 0; index < singleton_count; ++index) {
        for (int bit = 0; bit < width; ++bit) {
            if (contains(singletons[index], bit)) {
                singleton_hits[bit].push_back(index);
            }
        }
    }
    for (int index = 0; index < pair_count; ++index) {
        for (int bit = 0; bit < width; ++bit) {
            if (contains(pairs[index], bit)) {
                pair_hits[bit].push_back(index);
            }
        }
    }
    singleton_order.resize(width);
    pair_order.resize(width);
    for (int bit = 0; bit < width; ++bit) {
        singleton_order[bit] = pair_order[bit] = bit;
    }
    std::sort(singleton_order.begin(), singleton_order.end(), [](int a, int b) {
        return std::pair<std::size_t, int>{singleton_hits[a].size(), a} <
               std::pair<std::size_t, int>{singleton_hits[b].size(), b};
    });
    std::sort(pair_order.begin(), pair_order.end(), [](int a, int b) {
        return std::pair<std::size_t, int>{pair_hits[a].size(), a} <
               std::pair<std::size_t, int>{pair_hits[b].size(), b};
    });
    Mask full{~std::uint64_t(0), ~std::uint64_t(0), ~std::uint64_t(0)};
    if (width < 192) {
        full[2] = width <= 128 ? 0 : (std::uint64_t(1) << (width - 128)) - 1;
    }
    if (width < 128) {
        full[1] = width <= 64 ? 0 : (std::uint64_t(1) << (width - 64)) - 1;
    }
    if (width < 64) {
        full[0] = (std::uint64_t(1) << width) - 1;
    }

    bool feasible = singleton_cover(full, 6);
    for (int first = 0; !feasible && first < pair_count; ++first) {
        feasible = singleton_cover(remove(full, pairs[first]), 4);
    }
    std::uint64_t pair_pair_cases = 0;
    for (int first = 0; !feasible && first < pair_count; ++first) {
        for (int second = 0; !feasible && second < first; ++second) {
            ++pair_pair_cases;
            feasible = singleton_cover(remove(remove(full, pairs[first]), pairs[second]), 2);
        }
    }
    std::uint64_t third_pair_candidates = 0;
    for (int first = 0; !feasible && first < pair_count; ++first) {
        for (int second = 0; !feasible && second < first; ++second) {
            Mask residual = remove(remove(full, pairs[first]), pairs[second]);
            if (empty(residual)) {
                feasible = true;
                break;
            }
            int pivot = -1;
            for (int bit : pair_order) {
                if (contains(residual, bit)) {
                    pivot = bit;
                    break;
                }
            }
            for (int third : pair_hits[pivot]) {
                if (third >= second) {
                    continue;
                }
                ++third_pair_candidates;
                if (empty(remove(residual, pairs[third]))) {
                    feasible = true;
                    break;
                }
            }
        }
    }
    std::cout << (feasible ? "SAT" : "UNSAT") << ' ' << singleton_count << ' '
              << pair_count << ' ' << calls << ' ' << failed.size() << ' '
              << cache_hits << ' ' << pair_pair_cases << ' '
              << third_pair_candidates << '\n';
    return feasible ? 10 : 0;
}
