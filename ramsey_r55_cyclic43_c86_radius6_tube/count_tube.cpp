#include <algorithm>
#include <array>
#include <bit>
#include <cstdint>
#include <iostream>
#include <vector>

namespace {

constexpr int kOrder = 43;
constexpr int kAmbientEdges = 903;
constexpr int kRadius = 6;
constexpr std::uint64_t kMask = (std::uint64_t{1} << kOrder) - 1;

std::uint64_t rotate43(std::uint64_t value, int shift) {
    shift %= kOrder;
    if (shift == 0) {
        return value & kMask;
    }
    return ((value << shift) | (value >> (kOrder - shift))) & kMask;
}

std::uint64_t canonical_rotation(std::uint64_t value) {
    std::uint64_t canonical = value;
    for (int shift = 1; shift < kOrder; ++shift) {
        canonical = std::min(canonical, rotate43(value, shift));
    }
    return canonical;
}

void emit_errors(
    std::uint64_t center,
    int remaining,
    int next,
    std::uint64_t error,
    std::vector<std::uint64_t>& records
) {
    if (remaining == 0) {
        const auto key = canonical_rotation(center ^ error);
        records.push_back((key << 3) | static_cast<std::uint64_t>(std::popcount(error)));
        return;
    }
    for (int bit = next; bit <= kOrder - remaining; ++bit) {
        emit_errors(center, remaining - 1, bit + 1, error | (std::uint64_t{1} << bit), records);
    }
}

std::uint64_t binomial(int n, int k) {
    if (k < 0 || k > n) {
        return 0;
    }
    k = std::min(k, n - k);
    std::uint64_t result = 1;
    for (int i = 1; i <= k; ++i) {
        result = result * static_cast<unsigned>(n - k + i) / static_cast<unsigned>(i);
    }
    return result;
}

}  // namespace

int main() {
    // Red-to-blue length-one flips in the primary optimum-two coloring.
    constexpr std::array<int, 18> primary_positions{
        0, 1, 2, 8, 9, 10, 11, 17, 18, 19, 25, 26, 27, 28, 34, 35, 36, 37
    };
    std::uint64_t even_center = 0;
    for (const int position : primary_positions) {
        even_center |= std::uint64_t{1} << position;
    }
    const std::uint64_t odd_center = even_center ^ (std::uint64_t{1} << 42);

    std::size_t reserve = 0;
    for (int distance = 0; distance <= kRadius; ++distance) {
        reserve += 2 * static_cast<std::size_t>(binomial(kOrder, distance));
    }
    std::vector<std::uint64_t> records;
    records.reserve(reserve);
    for (const auto center : {even_center, odd_center}) {
        for (int distance = 0; distance <= kRadius; ++distance) {
            emit_errors(center, distance, 0, 0, records);
        }
    }
    if (records.size() != reserve) {
        return 2;
    }
    std::sort(records.begin(), records.end());

    std::array<unsigned long long, kRadius + 1> inner_layers{};
    for (std::size_t first = 0; first < records.size();) {
        const std::uint64_t key = records[first] >> 3;
        int minimum = static_cast<int>(records[first] & 7);
        std::size_t last = first + 1;
        while (last < records.size() && (records[last] >> 3) == key) {
            minimum = std::min(minimum, static_cast<int>(records[last] & 7));
            ++last;
        }
        if (key == 0 || key == kMask) {
            // These are the only rotation-fixed 43-bit words.  Neither can
            // occur in radius six of the centers (weights 18 and 19).
            return 3;
        }
        inner_layers[minimum] += kOrder;
        first = last;
    }

    std::array<std::uint64_t, kRadius + 1> ambient_layers{};
    std::uint64_t closed_volume = 0;
    for (int distance = 0; distance <= kRadius; ++distance) {
        for (int outside = 0; outside <= distance; ++outside) {
            ambient_layers[distance] +=
                binomial(kAmbientEdges - kOrder, outside) *
                inner_layers[distance - outside];
        }
        closed_volume += ambient_layers[distance];
    }

    std::cout << "generated_records=" << records.size() << '\n';
    std::cout << "inner_exact_layers=";
    for (int distance = 0; distance <= kRadius; ++distance) {
        if (distance) {
            std::cout << ',';
        }
        std::cout << inner_layers[distance];
    }
    std::cout << '\n';
    std::cout << "ambient_exact_layers=";
    for (int distance = 0; distance <= kRadius; ++distance) {
        if (distance) {
            std::cout << ',';
        }
        std::cout << ambient_layers[distance];
    }
    std::cout << '\n';
    std::cout << "closed_radius6_volume=";
    std::cout << closed_volume;
    std::cout << '\n';
}
