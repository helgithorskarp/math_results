#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <map>
#include <numeric>
#include <set>
#include <utility>
#include <vector>

namespace {

constexpr std::array<int, 9> base{560, 70, 20, 10, 8, 10, 20, 70, 560};
constexpr std::array<int, 9> u{1, -7, 21, -35, 35, -21, 7, -1, 0};
constexpr std::array<int, 9> v{0, 1, -7, 21, -35, 35, -21, 7, -1};
constexpr std::array<int, 8> h{1, -7, 21, -35, 35, -21, 7, -1};

bool direct_link_check(int a, const std::array<int, 8>& c) {
    std::array<int, 9> by_size{};
    for (int mask = 0; mask < 256; ++mask) {
        int size = 0;
        int sum = 0;
        for (int i = 0; i < 8; ++i) {
            if ((mask >> i) & 1) {
                ++size;
                sum += c[i];
            }
        }
        const int sign = size % 2 == 0 ? -1 : 1;
        const int cell = base[size] + sign * (sum - a);
        if (cell < 0) return false;
        by_size[size] += cell;
    }
    const int sum_c = std::accumulate(c.begin(), c.end(), 0);
    const int b = sum_c - a;
    for (int size = 0; size <= 8; ++size) {
        const int expected = 560 + a * u[size] + b * v[size];
        assert(by_size[size] == expected);
    }
    return true;
}

void check_face_identities() {
    // Summing over the two omitted coordinates gives the required exact
    // six-coordinate marginal.  Check the particular solution numerically.
    for (int r = 0; r <= 6; ++r) {
        int factorial_part = 1;
        for (int i = 2; i <= r; ++i) factorial_part *= i;
        for (int i = 2; i <= 6 - r; ++i) factorial_part *= i;
        assert(base[r] + 2 * base[r + 1] + base[r + 2] == factorial_part);
    }

    // Check cancellation of every two-face for a basis of the nine-dimensional
    // homogeneous family: a=1 and each individual c_i=1.
    for (int basis = 0; basis < 9; ++basis) {
        const int a = basis == 0 ? 1 : 0;
        std::array<int, 8> c{};
        if (basis > 0) c[basis - 1] = 1;
        for (int i = 0; i < 8; ++i) {
            for (int j = i + 1; j < 8; ++j) {
                const int free_mask = (1 << i) | (1 << j);
                for (int fixed = 0; fixed < 256; ++fixed) {
                    if (fixed & free_mask) continue;
                    int face_sum = 0;
                    for (int bits = 0; bits < 4; ++bits) {
                        int mask = fixed;
                        if (bits & 1) mask |= 1 << i;
                        if (bits & 2) mask |= 1 << j;
                        int size = 0;
                        int sum = 0;
                        for (int x = 0; x < 8; ++x) {
                            if ((mask >> x) & 1) {
                                ++size;
                                sum += c[x];
                            }
                        }
                        const int sign = size % 2 == 0 ? -1 : 1;
                        face_sum += sign * (sum - a);
                    }
                    assert(face_sum == 0);
                }
            }
        }
    }
}

std::set<std::pair<int, int>> independently_deletion_admissible() {
    std::set<std::pair<int, int>> answer;
    // Nonnegativity at positions 0,1,7,8 in (3) implies the complete
    // feasible polygon is contained in this square (in fact much more tightly).
    for (int a = -560; a <= 560; ++a) {
        for (int b = -560; b <= 560; ++b) {
            std::array<int, 9> d{};
            bool nonnegative = true;
            for (int j = 0; j < 9; ++j) {
                d[j] = 560 + a * u[j] + b * v[j];
                if (d[j] < 0) nonnegative = false;
            }
            if (!nonnegative) continue;

            std::vector<int> compatible;
            for (int c = -18; c <= 18; ++c) {
                int delta = 0;
                bool ok = true;
                for (int k = 0; k < 8; ++k) {
                    const int deleted = 630 + c * h[k];
                    delta += deleted - d[k];
                    if (delta < 0 || delta > deleted) ok = false;
                }
                if (ok) compatible.push_back(c);
            }
            if (compatible.empty()) continue;
            for (std::size_t i = 1; i < compatible.size(); ++i)
                assert(compatible[i] == compatible[i - 1] + 1);
            const int row_sum = a + b;
            if (8 * compatible.front() <= row_sum &&
                row_sum <= 8 * compatible.back()) {
                answer.emplace(a, b);
            }
        }
    }
    return answer;
}

}  // namespace

int main() {
    check_face_identities();

    std::array<int, 8> c{};
    std::map<int, std::uint64_t> profiles_by_a;
    std::set<std::pair<int, int>> position_types;
    std::uint64_t link_profiles = 0;

    auto visit = [&]() {
        std::array<int, 9> prefix{};
        for (int i = 0; i < 8; ++i) prefix[i + 1] = prefix[i] + c[i];

        // For even size, only the largest subset sum matters; for odd size,
        // only the smallest subset sum matters because c is sorted.
        int lower = -560;
        int upper = 560;
        for (int size = 0; size <= 8; ++size) {
            if (size % 2 == 0) {
                const int largest = prefix[8] - prefix[8 - size];
                lower = std::max(lower, largest - base[size]);
            } else {
                const int smallest = prefix[size];
                upper = std::min(upper, smallest + base[size]);
            }
        }
        for (int a = lower; a <= upper; ++a) {
            assert(direct_link_check(a, c));
            ++link_profiles;
            ++profiles_by_a[a];
            const int b = prefix[8] - a;
            position_types.emplace(a, b);
        }
    };

    auto enumerate = [&](auto&& self, int position, int least) -> void {
        if (position == 8) {
            visit();
            return;
        }
        for (int value = least; value <= 18; ++value) {
            c[position] = value;
            self(self, position + 1, value);
        }
    };
    enumerate(enumerate, 0, -18);

    const auto deletion_types = independently_deletion_admissible();
    std::vector<std::pair<int, int>> excluded;
    std::set_difference(deletion_types.begin(), deletion_types.end(),
                        position_types.begin(), position_types.end(),
                        std::back_inserter(excluded));
    assert(link_profiles == 243545);
    assert(position_types.size() == 1695);
    assert(deletion_types.size() == 1769);
    assert(excluded.size() == 74);

    std::cout << "metric\tvalue\n";
    std::cout << "symmetry_reduced_point_link_profiles\t" << link_profiles << '\n';
    std::cout << "induced_position_types\t" << position_types.size() << '\n';
    std::cout << "independent_deletion_types\t" << deletion_types.size() << '\n';
    std::cout << "newly_excluded_position_types\t" << excluded.size() << '\n';
    std::cout << "[profiles_by_a]\n";
    for (const auto& [a, count] : profiles_by_a)
        std::cout << a << '\t' << count << '\n';
    std::cout << "[position_types]\n";
    for (const auto& [a, b] : position_types)
        std::cout << a << '\t' << b << '\n';
    std::cout << "[newly_excluded_position_types]\n";
    for (const auto& [a, b] : excluded)
        std::cout << a << '\t' << b << '\n';
}
