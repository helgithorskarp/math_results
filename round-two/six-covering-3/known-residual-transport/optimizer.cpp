// Exact known-residual four-top-resource budget. Author: six-covering-3, researcher, 2026-10-01.
// The input and arithmetic bounds are specified in README.md. No threading.
#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <limits>
#include <numeric>
#include <stdexcept>
#include <string>
#include <vector>

using Integer = std::int64_t;
constexpr Integer absent = -(Integer{1} << 60);
constexpr std::array<int, 4> divisors = {1, 5, 7, 35};

void require(bool condition, const char* message) {
    if (!condition) throw std::runtime_error(message);
}

int charge(int mask) {
    int a = 0, c = 0, d = 0;
    for (int column = 0; column < 3; ++column) {
        bool even = false, odd = false;
        for (int j = 0; j < 6; ++j) {
            if (j % 3 == column && (mask & (1 << j)) != 0) {
                if (j % 2 == 0) even = true; else odd = true;
            }
        }
        a += even && !odd;
        c += odd && !even;
        d += even && odd;
    }
    return 2 * d + std::max(0, 2 * std::max(a, c) - 3);
}

struct Assignment {
    std::array<int, 4> j{};
    int base=0, row=0, col=0, both=0;
    std::array<std::array<int, 2>, 4> singleton_masks{};
};

std::array<std::vector<Assignment>, 16> assignments() {
    std::array<std::vector<Assignment>, 16> result;
    for (int mask = 0; mask < 16; ++mask) {
        std::vector<int> members;
        for (int i = 0; i < 4; ++i)
            if ((mask & (1 << i)) != 0) members.push_back(i);
        int count = 1;
        for (std::size_t i = 0; i < members.size(); ++i) count *= 6;
        for (int code = 0; code < count; ++code) {
            Assignment entry;
            int rest = code;
            for (int i : members) { entry.j[i] = rest % 6; rest /= 6; }
            const int base = (mask & 1) != 0 ? (1 << entry.j[0]) : 0;
            const int row = base | ((mask & 2) != 0 ? (1 << entry.j[1]) : 0);
            const int col = base | ((mask & 4) != 0 ? (1 << entry.j[2]) : 0);
            entry.base = base; entry.row = row; entry.col = col; entry.both = row | col;
            for (int flags = 0; flags < 4; ++flags) {
                int at_s = base;
                if ((flags & 1) != 0 && (mask & 2) != 0) at_s |= 1 << entry.j[1];
                if ((flags & 2) != 0 && (mask & 4) != 0) at_s |= 1 << entry.j[2];
                const int with_s = at_s | ((mask & 8) != 0 ? (1 << entry.j[3]) : 0);
                entry.singleton_masks[flags] = {at_s, with_s};
            }
            result[mask].push_back(entry);
        }
    }
    return result;
}

using Classes = std::vector<std::vector<int>>;
using Matrix = std::vector<std::array<Integer, 35>>;
struct Profile {
    std::array<Integer,64> base{};
    std::array<std::array<Integer,5>,64> row{};
    std::array<std::array<Integer,7>,64> col{};
    std::array<std::array<Integer,35>,64> point{};
};

Classes coordinate_classes(int p, const Matrix& u, const Matrix& v, const Matrix& known,
                           const std::array<int, 4>& fixed_r,
                           const std::array<std::array<int, 7>, 5>& crt) {
    std::array<bool, 7> singleton{};
    const int index = p == 5 ? 1 : 2;
    if (fixed_r[index] >= 0) singleton[fixed_r[index]] = true;
    if (fixed_r[3] >= 0) singleton[fixed_r[3] % p] = true;
    auto identical = [&](int a, int b) {
        for (const auto* matrix : {&u, &v, &known}) for (const auto& row : *matrix)
            for (int h = 0; h < (p == 5 ? 7 : 5); ++h) {
                const int za = p == 5 ? crt[a][h] : crt[h][a];
                const int zb = p == 5 ? crt[b][h] : crt[h][b];
                if (row[za] != row[zb]) return false;
            }
        return true;
    };
    Classes result;
    for (int a = 0; a < p; ++a) {
        bool placed = false;
        if (!singleton[a]) for (auto& group : result) {
            if (!singleton[group.front()] && identical(a, group.front())) {
                group.push_back(a); placed = true; break;
            }
        }
        if (!placed) result.push_back({a});
    }
    return result;
}

std::vector<std::pair<int, int>> ordered_pair_representatives(const Classes& classes) {
    std::vector<std::pair<int, int>> result;
    for (std::size_t i = 0; i < classes.size(); ++i)
        for (std::size_t j = 0; j < classes.size(); ++j) {
            result.emplace_back(classes[i].front(), classes[j].front());
            if (i == j && classes[i].size() >= 2)
                result.emplace_back(classes[i][0], classes[i][1]);
        }
    return result;
}

void print_classes(const Classes& classes) {
    std::cout << '[';
    for (std::size_t i = 0; i < classes.size(); ++i) {
        if (i != 0) std::cout << ',';
        std::cout << '[';
        for (std::size_t j = 0; j < classes[i].size(); ++j) {
            if (j != 0) std::cout << ',';
            std::cout << classes[i][j];
        }
        std::cout << ']';
    }
    std::cout << ']';
}

int main(int argc, char** argv) {
    try {
        const bool use_orbits = argc == 2 && std::string(argv[1]) == "--orbits";
        require(argc == 1 || use_orbits, "unknown command argument");
        int B = 0, b = 0;
        require(static_cast<bool>(std::cin >> B >> b), "missing B,b");
        require(B >= 6 && B <= 432 && B % 6 == 0, "B out of implementation range");
        int rest = B;
        for (int p : {2, 3}) while (rest % p == 0) rest /= p;
        require(rest == 1, "B prime support must be {2,3}");
        const int T = B / 6;
        require(b >= 1 && T % b == 0, "b must divide B/6");
        std::array<int, 4> fixed_t{}, fixed_r{};
        for (int i = 0; i < 4; ++i) {
            require(static_cast<bool>(std::cin >> fixed_t[i] >> fixed_r[i]), "missing fixed phases");
            require((fixed_t[i] == -1 && fixed_r[i] == -1) ||
                    (fixed_t[i] >= 0 && fixed_t[i] < B && fixed_r[i] >= 0 &&
                     fixed_r[i] < divisors[i]), "invalid fixed top phase");
        }
        std::vector<std::array<Integer, 35>> u(static_cast<std::size_t>(B));
        std::vector<std::array<Integer, 35>> v(static_cast<std::size_t>(b));
        for (auto* matrix : {&u, &v}) for (auto& row : *matrix) for (auto& weight : row) {
            require(static_cast<bool>(std::cin >> weight), "incomplete weight array");
            require(weight >= 0 && weight <= 1000000000, "weight out of integer bounds");
        }
        Matrix known(static_cast<std::size_t>(T));
        for (auto& row : known) for (auto& mask : row) {
            require(static_cast<bool>(std::cin >> mask), "incomplete known point masks");
            require(mask >= 0 && mask < 64, "known point mask outside 0..63");
        }
        std::cin >> std::ws;
        require(std::cin.peek() == std::char_traits<char>::eof(), "trailing input");
        for (int i = 0; i < 4; ++i) if (fixed_t[i] >= 0)
            for (int z = fixed_r[i]; z < 35; z += divisors[i])
                require(u[fixed_t[i]][z] == 0, "u positive on prescribed top");
        std::array<std::vector<Integer>, 4> U;
        for (int i = 0; i < 4; ++i) {
            U[i].resize(static_cast<std::size_t>(B * divisors[i]));
            for (int t = 0; t < B; ++t) for (int z = 0; z < 35; ++z)
                U[i][t * divisors[i] + z % divisors[i]] += u[t][z];
        }
        std::array<int,64> mass{};
        for (int h=0; h<64; ++h) mass[h]=6-charge(63 ^ h);
        std::vector<Profile> profiles(static_cast<std::size_t>(T));
        for (int q=0; q<T; ++q) for (int h=0; h<64; ++h) for (int z=0; z<35; ++z) {
            const int residual = static_cast<int>(known[q][z]);
            const Integer value = (mass[residual]-mass[residual & ~h]) * v[q % b][z];
            profiles[q].base[h] += value;
            profiles[q].row[h][z % 5] += value;
            profiles[q].col[h][z % 7] += value;
            profiles[q].point[h][z] = value;
        }
        std::array<std::array<int, 7>, 5> intersection{};
        for (int z = 0; z < 35; ++z) intersection[z % 5][z % 7] = z;
        const auto local_assignments = assignments();
        std::array<std::vector<int>, 4> cofactor_choices;
        for (int i = 0; i < 4; ++i) {
            if (fixed_r[i] >= 0) cofactor_choices[i].push_back(fixed_r[i]);
            else for (int r = 0; r < divisors[i]; ++r) cofactor_choices[i].push_back(r);
        }
        const std::uint64_t complete_tuple_count = cofactor_choices[1].size()
            * cofactor_choices[2].size() * cofactor_choices[3].size();
        Classes classes5, classes7;
        std::vector<std::array<int, 4>> cofactor_tuples;
        if (use_orbits) {
            classes5 = coordinate_classes(5, u, v, known, fixed_r, intersection);
            classes7 = coordinate_classes(7, u, v, known, fixed_r, intersection);
            const auto reps5 = ordered_pair_representatives(classes5);
            const auto reps7 = ordered_pair_representatives(classes7);
            for (const auto& p5 : reps5) for (const auto& p7 : reps7) {
                const std::array<int, 4> rs = {0, p5.first, p7.first,
                                              intersection[p5.second][p7.second]};
                bool legal = true;
                for (int i = 1; i < 4; ++i)
                    if (fixed_r[i] >= 0 && fixed_r[i] != rs[i]) legal = false;
                if (legal) cofactor_tuples.push_back(rs);
            }
            std::sort(cofactor_tuples.begin(), cofactor_tuples.end());
        } else {
            for (int r5 : cofactor_choices[1]) for (int r7 : cofactor_choices[2])
                for (int s : cofactor_choices[3]) cofactor_tuples.push_back({0, r5, r7, s});
        }
        require(!cofactor_tuples.empty(), "empty legal cofactor quotient");
        Integer maximum = absent;
        std::array<int, 4> best_t{}, best_r{};
        std::uint64_t tuple_count = 0, local_visits = 0;
        // d=1's only cofactor residue is always zero.
        for (const auto& rs : cofactor_tuples) {
            ++tuple_count;
            const int r5 = rs[1], r7 = rs[2], s = rs[3];
            const int flags = (s % 5 == r5 ? 1 : 0) | (s % 7 == r7 ? 2 : 0);
            std::vector<std::array<Integer, 16>> tables(static_cast<std::size_t>(T));
            std::vector<std::array<std::array<int, 4>, 16>> witnesses(static_cast<std::size_t>(T));
            for (int q = 0; q < T; ++q) {
                auto& table = tables[q];
                table.fill(absent);
                table[0] = 0;
                const auto& profile = profiles[q];
                const int cross = intersection[r5][r7];
                for (int mask = 1; mask < 16; ++mask) {
                    bool legal_label = true;
                    for (int i = 0; i < 4; ++i) if ((mask & (1 << i)) != 0 && fixed_t[i] >= 0)
                        if (fixed_t[i] % T != q) legal_label = false;
                    if (!legal_label) continue;
                    for (const auto& entry : local_assignments[mask]) {
                        bool legal_points = true;
                        Integer value = 0;
                        ++local_visits;
                        for (int i = 0; i < 4; ++i) if ((mask & (1 << i)) != 0) {
                            if (fixed_t[i] >= 0 && fixed_t[i] / T != entry.j[i]) {
                                legal_points = false; break;
                            }
                            value += U[i][(q + T * entry.j[i]) * divisors[i] + rs[i]];
                        }
                        if (!legal_points) continue;
                        const int a=entry.base, r=entry.row, c=entry.col, both=entry.both;
                        const int e=entry.singleton_masks[flags][0], f=entry.singleton_masks[flags][1];
                        value += profile.base[a] + profile.row[r][r5] - profile.row[a][r5]
                            + profile.col[c][r7] - profile.col[a][r7]
                            + profile.point[both][cross] - profile.point[r][cross]
                            - profile.point[c][cross] + profile.point[a][cross]
                            + profile.point[f][s] - profile.point[e][s];
                        if (value > table[mask]) {
                            table[mask] = value;
                            witnesses[q][mask] = entry.j;
                        }
                    }
                }
            }
            std::array<Integer, 16> dp{};
            dp.fill(absent);
            dp[0] = 0;
            std::vector<std::array<int, 16>> groups(static_cast<std::size_t>(T + 1));
            for (int q = 0; q < T; ++q) {
                std::array<Integer, 16> next{};
                next.fill(absent);
                for (int used = 0; used < 16; ++used) if (dp[used] != absent) {
                    const int remaining = 15 ^ used;
                    int group = remaining;
                    while (true) {
                        if (tables[q][group] != absent) {
                            const Integer value = dp[used] + tables[q][group];
                            const int target = used | group;
                            if (value > next[target]) {
                                next[target] = value;
                                groups[q + 1][target] = group;
                            }
                        }
                        if (group == 0) break;
                        group = (group - 1) & remaining;
                    }
                }
                dp = next;
            }
            require(dp[15] != absent, "no legal full top assignment");
            if (dp[15] > maximum) {
                maximum = dp[15]; best_r = rs;
                int used = 15;
                for (int q = T; q >= 1; --q) {
                    const int group = groups[q][used];
                    for (int i = 0; i < 4; ++i) if ((group & (1 << i)) != 0)
                        best_t[i] = q - 1 + T * witnesses[q - 1][group][i];
                    used ^= group;
                }
                require(used == 0, "incomplete witness reconstruction");
            }
        }
        std::cout << "{\"B\":" << B << ",\"C\":35,\"b\":" << b
                  << ",\"value\":" << maximum << ",\"cofactor_tuples\":" << tuple_count
                  << ",\"local_candidate_visits\":" << local_visits << ",\"phases\":[";
        for (int i = 0; i < 4; ++i) {
            if (i != 0) std::cout << ',';
            std::cout << '[' << divisors[i] << ',' << best_t[i] << ',' << best_r[i] << ']';
        }
        std::cout << ']';
        if (use_orbits) {
            std::cout << ",\"complete_cofactor_tuples\":" << complete_tuple_count
                      << ",\"classes5\":";
            print_classes(classes5);
            std::cout << ",\"classes7\":";
            print_classes(classes7);
        }
        std::cout << "}\n";
        return 0;
    } catch (const std::exception& error) {
        std::cerr << "Incomplete or invalid computation: " << error.what() << '\n';
        return 1;
    }
}
