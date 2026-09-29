// Independent exact checker: explicit pairs, ternary word tables, square list.
// No Python bit masks, Euler exponentiation, solver, or external certificate.
#include <array>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <stdexcept>
#include <utility>
#include <vector>

constexpr int p = 617;
constexpr int k = 7;
constexpr int max_d = 28;
using Word = std::array<std::int8_t, p>;
using AP = std::pair<int, int>;

void require(bool condition, const char* message) {
    if (!condition) throw std::runtime_error(message);
}

int main() {
    try {
        for (int d = 2; d * d <= p; ++d) require(p % d != 0, "not prime");
        Word qr{};
        qr.fill(1);
        qr[0] = -1;
        for (int x = 1; x < p; ++x) qr[(x * x) % p] = 0;
        std::array<Word, p> words{};
        for (int s = 0; s < p; ++s)
            for (int x = 0; x < p; ++x) words[s][x] = qr[(x + s) % p];

        std::vector<AP> aps;
        for (int d = 1; d <= max_d; ++d)
            for (int a = p - 6 * d; a < p; ++a) aps.emplace_back(a, d);
        // -1 means a pole or two colors occur in this half; otherwise 0 or 1.
        std::vector<Word> left(aps.size()), right(aps.size());
        for (std::size_t z = 0; z < aps.size(); ++z) {
            const auto [a, d] = aps[z];
            for (int s = 0; s < p; ++s) {
                for (int half = 0; half != 2; ++half) {
                    int color = -2;
                    for (int j = 0; j < k; ++j) {
                        const int x = a + j * d;
                        if ((x < p) != (half == 0)) continue;
                        const int b = words[s][x % p];
                        if (b < 0 || (color >= 0 && color != b)) {
                            color = -1;
                            break;
                        }
                        color = b;
                    }
                    require(color != -2, "empty half");
                    (half == 0 ? left : right)[z][s] =
                        static_cast<std::int8_t>(color);
                }
            }
        }

        std::uint64_t tested = 0, excluded = 0, survived = 0;
        std::uint64_t first_witness_at_28 = 0;
        for (int s = 0; s < p; ++s) {
            std::vector<std::size_t> useful;
            for (std::size_t z = 0; z < aps.size(); ++z)
                if (left[z][s] >= 0) useful.push_back(z);
            for (int t = 0; t < p; ++t) {
                for (int e = 0; e != 2; ++e) {
                    ++tested;
                    bool obstruction = false;
                    for (const auto z : useful) {
                        if (right[z][t] < 0 ||
                            (right[z][t] ^ e) != left[z][s]) continue;
                        // Recheck every term of each chosen witness directly.
                        const auto [a, d] = aps[z];
                        if (d == 28) {
                            require(e == 1 &&
                                    ((s == 154 && t == 463) ||
                                     (s == 155 && t == 464)),
                                    "unexpected sharp horizon pair");
                            ++first_witness_at_28;
                        }
                        for (int j = 0; j < k; ++j) {
                            const int x = a + j * d;
                            const int b = x < p ? words[s][x] : words[t][x - p];
                            require(b >= 0, "witness uses a pole");
                            require((b ^ (x < p ? 0 : e)) == left[z][s],
                                    "witness is not monochromatic");
                        }
                        obstruction = true;
                        break;
                    }
                    require(obstruction == !(s == t && e == 0),
                            "surviving pair differs from asserted diagonal");
                    if (obstruction) ++excluded;
                    else ++survived;
                }
            }
        }
        require(first_witness_at_28 == 2, "sharp horizon cases missing");
        // Independent definition-level cyclic and forcing checks.
        std::uint64_t modular = 0;
        for (int a = 0; a < p; ++a) {
            for (int d = 1; d < p; ++d) {
                int colors = 0;
                for (int j = 0; j < k; ++j) {
                    const int b = qr[(a + j * d) % p];
                    if (b >= 0) colors |= 1 << b;
                }
                require(colors == 3, "modular partial pattern is not safe");
                ++modular;
            }
        }
        for (int r = 1; r < p; ++r) {
            const int d = r * 47 % p;
            for (int j = 1; j < k; ++j) {
                const int x = ((r - j * d) % p + p) % p;
                require(qr[x] == 1 - qr[r], "forcing bridge failed");
            }
        }
        std::cout << "{\n  \"crossing_progressions\": " << aps.size()
                  << ",\n  \"tested_normalized_pairs\": " << tested
                  << ",\n  \"excluded_normalized_pairs\": " << excluded
                  << ",\n  \"surviving_normalized_pairs\": " << survived
                  << ",\n  \"first_witness_at_difference_28\": " << first_witness_at_28
                  << ",\n  \"modular_progressions_checked\": " << modular
                  << ",\n  \"forcing_multiplier_cases\": " << p - 1 << "\n}\n";
        return EXIT_SUCCESS;
    } catch (const std::exception& e) {
        std::cerr << e.what() << '\n';
        return EXIT_FAILURE;
    }
}
