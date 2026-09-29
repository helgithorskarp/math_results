// Author: six-vdw-3. Deterministic certificate generation, not a checker.
#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

namespace {
constexpr int p = 617;
constexpr int length = 2 * p;
constexpr int bound = 44;
constexpr int cases_per_phase = 2 * p - 1;
using Clock = std::chrono::steady_clock;
struct AP {
    std::uint16_t a, d;
    std::array<std::uint16_t, 7> points;
};

int integer(const char* arg) {
    std::size_t used = 0;
    const std::string text(arg);
    const int value = std::stoi(text, &used);
    if (used != text.size()) throw std::runtime_error("invalid integer argument");
    return value;
}

void little(std::ostream& out, std::uint32_t value, int bytes) {
    for (int j = 0; j < bytes; ++j) {
        out.put(static_cast<char>(value & 255U));
        value >>= 8;
    }
}
}

int main(int argc, char** argv) {
    try {
        if (argc != 4) throw std::runtime_error("usage: generate BEGIN END OUTPUT.bin");
        const int begin = integer(argv[1]), end = integer(argv[2]);
        if (!(0 <= begin && begin < end && end <= p))
            throw std::runtime_error("phase range must satisfy 0 <= BEGIN < END <= 617");
        const std::filesystem::path target(argv[3]);
        const std::filesystem::path partial(target.string() + ".partial");
        if (std::filesystem::exists(target) || std::filesystem::exists(partial))
            throw std::runtime_error("output or partial output already exists");

        const auto start = Clock::now();
        std::array<std::int8_t, p> q{};
        q.fill(1);
        q[0] = -1;
        for (int x = 1; x < p; ++x) q[(x * x) % p] = 0;

        // Ascending (d,a) order, for every crossing AP in [0,1234).
        std::vector<AP> aps;
        for (int d = 1; 6 * d < length; ++d) {
            for (int a = std::max(0, p - 6 * d);
                 a < std::min(p, length - 6 * d); ++a) {
                AP ap{static_cast<std::uint16_t>(a), static_cast<std::uint16_t>(d), {}};
                for (int j = 0; j < 7; ++j)
                    ap.points[j] = static_cast<std::uint16_t>(a + j * d);
                aps.push_back(ap);
            }
        }
        const std::size_t m = aps.size();
        if (m != 63448) throw std::runtime_error("unexpected crossing AP count");
        std::vector<std::int8_t> left(static_cast<std::size_t>(p) * m, -1);
        std::vector<std::int8_t> right(static_cast<std::size_t>(p) * m, -1);
        for (int phase = 0; phase < p; ++phase) {
            auto* lp = left.data() + static_cast<std::size_t>(phase) * m;
            auto* rp = right.data() + static_cast<std::size_t>(phase) * m;
            for (std::size_t z = 0; z < m; ++z) {
                int colors[2] = {0, 0};
                bool pole[2] = {false, false};
                for (const auto x : aps[z].points) {
                    const int half = x >= p;
                    const int color = q[(x + phase) % p];
                    if (color < 0) pole[half] = true;
                    else colors[half] |= 1 << color;
                }
                if (!pole[0] && (colors[0] == 1 || colors[0] == 2))
                    lp[z] = static_cast<std::int8_t>(colors[0] - 1);
                if (!pole[1] && (colors[1] == 1 || colors[1] == 2))
                    rp[z] = static_cast<std::int8_t>(colors[1] - 1);
            }
        }
        std::cerr << "tables_ready crossing_aps=" << m << '\n';
        std::ofstream out(partial, std::ios::binary);
        if (!out) throw std::runtime_error("cannot create partial output");
        out.write("QRS617P1", 8);
        little(out, p, 2); little(out, 7, 2); little(out, bound, 2);
        little(out, static_cast<std::uint32_t>(begin), 2);
        little(out, static_cast<std::uint32_t>(end), 2);
        little(out, static_cast<std::uint32_t>((end - begin) * cases_per_phase), 4);

        std::array<std::uint64_t, 2> successes{};
        std::uint64_t cases = 0;
        for (int s = begin; s < end; ++s) {
            const auto* lp = left.data() + static_cast<std::size_t>(s) * m;
            std::vector<std::size_t> useful;
            for (std::size_t z = 0; z < m; ++z) if (lp[z] >= 0) useful.push_back(z);
            for (int t = 0; t < p; ++t) {
                const auto* rp = right.data() + static_cast<std::size_t>(t) * m;
                for (int e = 0; e < 2; ++e) {
                    if (s == t && e == 0) continue;
                    std::array<std::size_t, bound> chosen{};
                    bool certified = false;
                    for (int order = 0; order < 2; ++order) {
                        std::array<std::uint64_t, 20> occupied{};
                        int count = 0;
                        for (std::size_t j = 0; j < useful.size(); ++j) {
                            const auto z = useful[order ? useful.size() - 1 - j : j];
                            if (rp[z] < 0 || (rp[z] ^ e) != lp[z]) continue;
                            bool free = true;
                            for (const auto x : aps[z].points) {
                                if ((occupied[x / 64] >> (x % 64)) & 1U) {
                                    free = false;
                                    break;
                                }
                            }
                            if (!free) continue;
                            for (const auto x : aps[z].points)
                                occupied[x / 64] |= std::uint64_t{1} << (x % 64);
                            chosen[static_cast<std::size_t>(count++)] = z;
                            if (count == bound) break;
                        }
                        if (count == bound) {
                            certified = true;
                            ++successes[static_cast<std::size_t>(order)];
                            break;
                        }
                    }
                    if (!certified) {
                        throw std::runtime_error("NOT_CERTIFIED at (s,t,e)=(" +
                            std::to_string(s) + "," + std::to_string(t) + "," +
                            std::to_string(e) + "); search failure proves no exclusion");
                    }
                    std::array<char, 4 * bound> buffer{};
                    for (int j = 0; j < bound; ++j) {
                        const auto& ap = aps[chosen[static_cast<std::size_t>(j)]];
                        const auto offset = static_cast<std::size_t>(4 * j);
                        buffer[offset] = static_cast<char>(ap.a & 255U);
                        buffer[offset + 1] = static_cast<char>(ap.a >> 8);
                        buffer[offset + 2] = static_cast<char>(ap.d & 255U);
                        buffer[offset + 3] = static_cast<char>(ap.d >> 8);
                    }
                    out.write(buffer.data(), static_cast<std::streamsize>(buffer.size()));
                    if (!out) throw std::runtime_error("output write failed");
                    ++cases;
                }
            }
            if ((s - begin) % 50 == 0)
                std::cerr << "phase=" << s << " cases=" << cases << '\n';
        }
        if (cases != static_cast<std::uint64_t>((end - begin) * cases_per_phase))
            throw std::runtime_error("case coverage mismatch");
        out.close();
        if (!out) throw std::runtime_error("output close failed");
        std::filesystem::rename(partial, target);
        std::cout << "{\"status\":\"GENERATED\",\"begin\":" << begin
                  << ",\"end\":" << end << ",\"cases\":" << cases
                  << ",\"packing_bound\":" << bound << ",\"crossing_aps\":" << m
                  << ",\"order_successes\":[" << successes[0] << ',' << successes[1]
                  << "],\"seconds\":"
                  << std::chrono::duration<double>(Clock::now() - start).count() << "}\n";
    } catch (const std::exception& ex) {
        std::cerr << ex.what() << '\n';
        return EXIT_FAILURE;
    }
}
