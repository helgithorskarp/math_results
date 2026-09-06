#include <algorithm>
#include <array>
#include <bit>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <numeric>
#include <set>
#include <stdexcept>
#include <string>
#include <tuple>
#include <vector>

namespace {

using Mask = std::uint32_t;

struct CoreRecord {
    Mask canonical;
    int orbit_size;
    int central_deficit;
    std::array<int, 7> exceptional_deficits;
};

[[noreturn]] void fail(const std::string& message) {
    throw std::runtime_error(message);
}

void require(bool condition, const std::string& message) {
    if (!condition) fail(message);
}

std::vector<std::pair<int, int>> pairs_on(int n) {
    std::vector<std::pair<int, int>> pairs;
    for (int u = 0; u < n; ++u)
        for (int v = u + 1; v < n; ++v)
            pairs.emplace_back(u, v);
    return pairs;
}

const std::vector<std::pair<int, int>> PAIRS7 = pairs_on(7);

std::array<int, 7> deficits(Mask mask) {
    std::array<int, 7> out{};
    for (int v = 0; v < 7; ++v) {
        int weighted = 0;
        for (int bit = 0; bit < 21; ++bit) {
            auto [u, w] = PAIRS7[bit];
            if (((mask >> bit) & 1U) == 0 || (u != v && w != v)) continue;
            int neighbor = u == v ? w : u;
            weighted += neighbor < 2 ? 2 : 1;
        }
        out[v] = weighted - (v < 2 ? 5 : 4);
    }
    return out;
}

bool has_monochromatic_five_set(Mask mask) {
    for (unsigned subset = 0; subset < (1U << 7); ++subset) {
        if (std::popcount(subset) != 5) continue;
        int red = 0;
        for (int bit = 0; bit < 21; ++bit) {
            auto [u, v] = PAIRS7[bit];
            if (((subset >> u) & 1U) && ((subset >> v) & 1U))
                red += static_cast<int>((mask >> bit) & 1U);
        }
        if (red == 0 || red == 10) return true;
    }
    return false;
}

bool valid_core(Mask mask) {
    auto s = deficits(mask);
    if (*std::min_element(s.begin(), s.end()) < 0) return false;
    if (std::accumulate(s.begin(), s.end(), 0) > 2) return false;
    return !has_monochromatic_five_set(mask);
}

std::vector<std::array<int, 7>> degree_preserving_group() {
    std::vector<std::array<int, 7>> group;
    std::array<int, 5> e{2, 3, 4, 5, 6};
    do {
        for (int swap = 0; swap < 2; ++swap) {
            std::array<int, 7> p{};
            p[0] = swap ? 1 : 0;
            p[1] = swap ? 0 : 1;
            std::copy(e.begin(), e.end(), p.begin() + 2);
            group.push_back(p);
        }
    } while (std::next_permutation(e.begin(), e.end()));
    require(group.size() == 240, "wrong group order");
    return group;
}

Mask image(Mask mask, const std::array<int, 7>& p) {
    int index[7][7];
    for (int i = 0; i < 7; ++i)
        for (int j = 0; j < 7; ++j)
            index[i][j] = -1;
    for (int bit = 0; bit < 21; ++bit) {
        auto [u, v] = PAIRS7[bit];
        index[u][v] = index[v][u] = bit;
    }
    Mask out = 0;
    for (int bit = 0; bit < 21; ++bit) {
        if (((mask >> bit) & 1U) == 0) continue;
        auto [u, v] = PAIRS7[bit];
        out |= Mask{1} << index[p[u]][p[v]];
    }
    return out;
}

void check_numeric_buckets() {
    std::vector<std::array<int, 3>> actual;
    for (int eta = 0; eta <= 1; ++eta) {
        for (int b = 0; b <= 10; ++b) {
            for (int e = 0; e <= 10; ++e) {
                int core_deficit = 4 * eta + 3 * b + 2 * e - 30;
                if (b < 10 - 4 * eta || b + e < 10) continue;
                if (0 <= core_deficit && core_deficit <= 2)
                    actual.push_back({eta, b, e});
            }
        }
    }
    const std::vector<std::array<int, 3>> expected{
        {0, 10, 0}, {0, 10, 1}, {1, 6, 4},
        {1, 6, 5}, {1, 7, 3}, {1, 8, 2}
    };
    require(actual == expected, "numerical bucket derivation mismatch");
}

void check_small_ramsey_controls() {
    const auto p6 = pairs_on(6);
    for (Mask mask = 0; mask < (Mask{1} << 15); ++mask) {
        bool monochromatic_triangle = false;
        for (int a = 0; a < 6; ++a)
            for (int b = a + 1; b < 6; ++b)
                for (int c = b + 1; c < 6; ++c) {
                    int colors = 0;
                    for (int bit = 0; bit < 15; ++bit) {
                        auto [u, v] = p6[bit];
                        if ((u == a && v == b) || (u == a && v == c) ||
                            (u == b && v == c))
                            colors += static_cast<int>((mask >> bit) & 1U);
                    }
                    monochromatic_triangle |= colors == 0 || colors == 3;
                }
        require(monochromatic_triangle, "R(3,3)<=6 control failed");
    }

    const auto p5 = pairs_on(5);
    int equality_count = 0;
    for (Mask mask = 0; mask < (Mask{1} << 10); ++mask) {
        bool triangle = false;
        for (int a = 0; a < 5; ++a)
            for (int b = a + 1; b < 5; ++b)
                for (int c = b + 1; c < 5; ++c) {
                    int present = 0;
                    for (int bit = 0; bit < 10; ++bit) {
                        auto [u, v] = p5[bit];
                        if ((u == a && v == b) || (u == a && v == c) ||
                            (u == b && v == c))
                            present += static_cast<int>((mask >> bit) & 1U);
                    }
                    triangle |= present == 3;
                }
        if (triangle) continue;
        int edges = std::popcount(mask);
        require(edges <= 6, "triangle-free five-vertex edge bound failed");
        if (edges != 6) continue;
        bool is_k23 = false;
        for (unsigned side = 0; side < (1U << 5); ++side) {
            if (std::popcount(side) != 2) continue;
            Mask cross = 0;
            for (int bit = 0; bit < 10; ++bit) {
                auto [u, v] = p5[bit];
                if (((side >> u) & 1U) != ((side >> v) & 1U))
                    cross |= Mask{1} << bit;
            }
            is_k23 |= cross == mask;
        }
        require(is_k23, "six-edge equality graph is not K2,3");
        ++equality_count;
    }
    require(equality_count == 10, "wrong labeled K2,3 equality count");

    int alternating_patterns = 0;
    for (int x : {2, 3})
        for (int y : {2, 3})
            for (int z : {2, 3})
                alternating_patterns += (x != y && y != z && z != x);
    require(alternating_patterns == 0, "two labels alternated on a triangle");
}

std::vector<CoreRecord> claimed_table() {
    return {
        {4094, 10, 0, {0, 0, 1, 1, 0, 0, 0}},
        {40573, 60, 1, {1, 0, 0, 0, 0, 0, 0}},
        {65209, 60, 0, {0, 0, 0, 0, 0, 1, 1}},
        {111865, 30, 2, {0, 0, 0, 0, 0, 0, 0}},
        {111989, 60, 2, {0, 0, 0, 0, 0, 0, 0}},
        {113913, 60, 0, {0, 0, 1, 1, 0, 0, 0}},
        {114037, 120, 0, {0, 0, 1, 1, 0, 0, 0}},
        {128249, 120, 0, {0, 0, 1, 0, 0, 0, 1}},
        {128373, 240, 0, {0, 0, 1, 0, 0, 0, 1}},
        {380153, 120, 0, {0, 0, 0, 1, 0, 0, 1}},
        {380277, 240, 0, {0, 0, 0, 1, 0, 0, 1}},
        {451059, 120, 0, {0, 0, 2, 0, 0, 0, 0}},
        {451061, 120, 0, {0, 0, 0, 2, 0, 0, 0}},
        {451431, 120, 0, {0, 0, 2, 0, 0, 0, 0}}
    };
}

}  // namespace

int main(int argc, char** argv) {
    try {
        std::string stream_path;
        if (argc == 3 && std::string(argv[1]) == "--stream") stream_path = argv[2];
        else if (argc != 1) fail("usage: independent_check [--stream PATH]");

        const int red_edges = (2 * 19 + 5 * 20 + 36 * 21) / 2;
        const int red_cap_sum = 2 * 85 + 5 * 93 + 36 * 100;
        const int blue_cap_sum = 2 * 115 + 5 * 107 + 36 * 100;
        const int degree_wedges = 2 * 19 * 23 + 5 * 20 * 22 + 36 * 21 * 21;
        const int triple_count = 43 * 42 * 41 / 6;
        const int monochromatic_triangle_incidence =
            3 * (triple_count - degree_wedges / 2);
        require(red_edges == 447, "red handshaking total");
        require(red_cap_sum == 4235 && blue_cap_sum == 4365,
                "triangle cap totals");
        require(monochromatic_triangle_incidence == 8598,
                "mixed-triangle identity total");
        require(red_cap_sum + blue_cap_sum - monochromatic_triangle_incidence == 2,
                "global deficit total");
        require(red_cap_sum % 3 == 2 && blue_cap_sum % 3 == 0,
                "triangle divisibility residue");

        check_numeric_buckets();
        check_small_ramsey_controls();

        std::vector<Mask> valid;
        for (Mask mask = 0; mask < (Mask{1} << 21); ++mask)
            if (valid_core(mask)) valid.push_back(mask);
        require(valid.size() == 1480, "literal census size");

        if (!stream_path.empty()) {
            std::ofstream stream(stream_path, std::ios::binary);
            require(static_cast<bool>(stream), "cannot create literal stream");
            for (Mask mask : valid) stream << mask << '\n';
            require(static_cast<bool>(stream), "cannot finish literal stream");
        }

        const auto group = degree_preserving_group();
        const std::set<Mask> valid_set(valid.begin(), valid.end());
        std::map<Mask, std::set<Mask>> orbits;
        for (Mask mask : valid) {
            Mask canonical = mask;
            for (const auto& p : group) canonical = std::min(canonical, image(mask, p));
            orbits[canonical].insert(mask);
        }
        require(orbits.size() == 14, "orbit census size");

        const auto expected = claimed_table();
        require(expected.size() == orbits.size(), "claimed table size");
        int table_labeled_total = 0;
        int blue_pair_count = 0;
        int remaining_orbits = 0;
        std::map<int, int> roots_by_central_deficit;
        int central_placements = 0;
        for (const auto& record : expected) {
            auto found = orbits.find(record.canonical);
            require(found != orbits.end(), "missing claimed canonical core");
            std::set<Mask> generated;
            for (const auto& p : group) generated.insert(image(record.canonical, p));
            require(generated == found->second, "orbit expansion mismatch");
            require(generated.size() == static_cast<std::size_t>(record.orbit_size),
                    "orbit size mismatch");
            require(std::includes(valid_set.begin(), valid_set.end(),
                                  generated.begin(), generated.end()),
                    "orbit contains an invalid core");
            auto s = deficits(record.canonical);
            require(s == record.exceptional_deficits, "exceptional deficit vector mismatch");
            require(2 - std::accumulate(s.begin(), s.end(), 0) == record.central_deficit,
                    "central deficit mismatch");
            table_labeled_total += record.orbit_size;
            if ((record.canonical & 1U) == 0) {
                blue_pair_count += record.orbit_size;
                require(record.canonical == 4094, "more than one blue-pair orbit");
            } else {
                ++remaining_orbits;
                int roots = record.central_deficit == 2 ? 2 : 1;
                roots_by_central_deficit[record.central_deficit] += roots;
                if (record.central_deficit == 0) central_placements += 1;
                if (record.central_deficit == 1) central_placements += 36;
                if (record.central_deficit == 2) central_placements += 36 + 36 * 35 / 2;
            }
        }
        require(table_labeled_total == 1480, "orbit table does not partition census");
        require(blue_pair_count == 10 && remaining_orbits == 13,
                "blue-pair branch or retained orbit count");
        require(roots_by_central_deficit == std::map<int, int>{{0, 10}, {1, 1}, {2, 4}},
                "fifteen-root distribution");
        require(central_placements == 1378, "central-defect placement count");
        require(43 * 42 / 2 == 903 && 903 - 21 == 882,
                "full/free edge-variable count");

        std::pair<Mask, std::array<int, 7>> transported{
            Mask{1} << 21, std::array<int, 7>{}
        };
        for (const auto& p : group)
            transported = std::min(transported, std::make_pair(image(901619, p), p));
        require(transported.first == 380277,
                "h2731 core does not map to the claimed retained core");
        require(transported.second == std::array<int, 7>{1, 0, 6, 5, 3, 4, 2},
                "h2731 transport permutation mismatch");

        // The forced-edge contradiction has the exact numerical endpoint claimed.
        const int forced_A_edges = 85 - 1 - 2 * 14;
        const int regular_neighborhood_total = (5 * 4 / 2) - 56 + 8 * 8;
        require(forced_A_edges == 56 && regular_neighborhood_total == 18,
                "fourteen-vertex obstruction arithmetic");

        std::cout << "STATUS=INDEPENDENTLY_VERIFIED_M216_INTRINSIC_PARTITION\n";
        std::cout << "red_edges=447 cap_sums=4235,4365 actual_triangle_incidence=8598 deficit=2\n";
        std::cout << "numeric_buckets=6 literal_cores=1480 core_orbits=14 blue_pair_cores=10 retained_orbits=13\n";
        std::cout << "roots_by_central_deficit=0:10,1:1,2:4 complete_roots=15 central_placements=1378\n";
        std::cout << "edge_variables=903 fixed_core_bits=21 remaining_bits=882\n";
        std::cout << "small_controls=K6:32768,K5:1024,K23_equalities:10,label_patterns:8\n";
        std::cout << "forced_A_edges=56 regular_neighborhood_triangle_total=18 h2731_core=380277\n";
        std::cout << "canonical_orbits=";
        for (std::size_t i = 0; i < expected.size(); ++i) {
            if (i) std::cout << ',';
            std::cout << expected[i].canonical << ':' << expected[i].orbit_size
                      << ':' << expected[i].central_deficit;
        }
        std::cout << '\n';
    } catch (const std::exception& error) {
        std::cerr << "ERROR=" << error.what() << '\n';
        return 1;
    }
    return 0;
}
