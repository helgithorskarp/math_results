// Author: six-vdw-3. Independent definition-level transcript checker.
// No AP generation, packing heuristic, half tables, or occupancy bitsets.
#include <array>
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>

namespace {
constexpr int modulus = 617;
constexpr int packing_bound = 18;
constexpr int window_radius = 308;
constexpr int points_per_case = 7 * packing_bound;

int parse(const char* text) {
    std::size_t used = 0;
    const std::string s(text);
    const int value = std::stoi(s, &used);
    if (used != s.size()) throw std::runtime_error("invalid integer argument");
    return value;
}

int modular_power(int base, int exponent) {
    int value = 1;
    while (exponent > 0) {
        if (exponent % 2) value = (value * base) % modulus;
        base = (base * base) % modulus;
        exponent /= 2;
    }
    return value;
}

std::uint32_t little(std::istream& in, int bytes) {
    std::uint32_t result = 0;
    for (int j = 0; j < bytes; ++j) {
        const int c = in.get();
        if (c == std::char_traits<char>::eof()) throw std::runtime_error("truncated header");
        result |= static_cast<std::uint32_t>(c) << (8 * j);
    }
    return result;
}
}

int main(int argc, char** argv) {
    try {
        const auto start = std::chrono::steady_clock::now();
        int expected_begin = 0, expected_end = modulus, first_file = 1;
        if (argc >= 2 && std::string(argv[1]) == "--range") {
            if (argc < 5) throw std::runtime_error("usage: verify --range BEGIN END FILE...");
            expected_begin = parse(argv[2]); expected_end = parse(argv[3]); first_file = 4;
        }
        if (argc <= first_file) throw std::runtime_error("usage: verify [--range BEGIN END] FILE...");
        if (!(0 <= expected_begin && expected_begin < expected_end && expected_end <= modulus))
            throw std::runtime_error("invalid expected phase range");
        for (int factor = 2; factor * factor <= modulus; ++factor)
            if (modulus % factor == 0) throw std::runtime_error("modulus is not prime");

        // Euler criterion; generator instead enumerates nonzero squares.
        std::array<int, modulus> character{};
        character[0] = -1;
        for (int residue = 1; residue < modulus; ++residue) {
            const int symbol = modular_power(residue, (modulus - 1) / 2);
            if (symbol == 1) character[static_cast<std::size_t>(residue)] = 0;
            else if (symbol == modulus - 1) character[static_cast<std::size_t>(residue)] = 1;
            else throw std::runtime_error("invalid Euler symbol");
        }
        std::array<bool, modulus> covered{};
        std::array<std::uint32_t, 2 * modulus> last_case{};
        std::uint32_t cases = 0;
        for (int file = first_file; file < argc; ++file) {
            std::ifstream in(argv[file], std::ios::binary);
            if (!in) throw std::runtime_error("cannot open input");
            std::array<char, 8> magic{};
            in.read(magic.data(), static_cast<std::streamsize>(magic.size()));
            if (!in || std::string(magic.data(), magic.size()) != "QRL617P1")
                throw std::runtime_error("invalid magic");
            const auto p = little(in, 2), terms = little(in, 2), bound = little(in, 2);
            const auto radius = little(in, 2);
            const auto begin = little(in, 2), end = little(in, 2), claimed_cases = little(in, 4);
            if (p != modulus || terms != 7 || bound != packing_bound || radius != window_radius)
                throw std::runtime_error("wrong modulus, progression length, packing bound, or window radius");
            if (!(static_cast<std::uint32_t>(expected_begin) <= begin && begin < end &&
                  end <= static_cast<std::uint32_t>(expected_end)))
                throw std::runtime_error("chunk outside expected range");
            if (claimed_cases != (end - begin) * (2 * modulus - 1))
                throw std::runtime_error("wrong chunk case count");
            for (auto s = begin; s < end; ++s) {
                if (covered[s]) throw std::runtime_error("duplicate phase coverage");
                covered[s] = true;
                for (int t = 0; t < modulus; ++t) {
                    for (int orientation = 0; orientation < 2; ++orientation) {
                        if (static_cast<int>(s) == t && orientation == 0) continue;
                        ++cases;
                        std::array<unsigned char, 4 * packing_bound> bytes{};
                        in.read(reinterpret_cast<char*>(bytes.data()),
                                static_cast<std::streamsize>(bytes.size()));
                        if (!in) throw std::runtime_error("truncated packing");
                        for (int j = 0; j < packing_bound; ++j) {
                            const auto offset = static_cast<std::size_t>(4 * j);
                            const int a = bytes[offset] + 256 * bytes[offset + 1];
                            const int d = bytes[offset + 2] + 256 * bytes[offset + 3];
                            if (!(d > 0 && a >= modulus - window_radius && a < modulus && a + 6 * d >= modulus &&
                                  a + 6 * d < modulus + window_radius))
                                throw std::runtime_error("invalid crossing progression");
                            int common_color = -1;
                            for (int term = 0; term < 7; ++term) {
                                const int x = a + term * d;
                                if (last_case[static_cast<std::size_t>(x)] == cases)
                                    throw std::runtime_error("progressions intersect");
                                last_case[static_cast<std::size_t>(x)] = cases;
                                const bool right_block = x >= modulus;
                                const int local = right_block ? x - modulus : x;
                                const int phase = right_block ? t : static_cast<int>(s);
                                int color = character[static_cast<std::size_t>((local + phase) % modulus)];
                                if (color < 0) throw std::runtime_error("progression contains a pole");
                                if (right_block) color ^= orientation;
                                if (term == 0) common_color = color;
                                else if (color != common_color)
                                    throw std::runtime_error("progression is not monochromatic");
                            }
                        }
                    }
                }
            }
            if (in.get() != std::char_traits<char>::eof())
                throw std::runtime_error("trailing bytes");
            if (!in.eof()) throw std::runtime_error("input read error");
        }
        for (int s = expected_begin; s < expected_end; ++s)
            if (!covered[static_cast<std::size_t>(s)])
                throw std::runtime_error("incomplete phase coverage");
        const auto expected_cases = static_cast<std::uint32_t>(
            (expected_end - expected_begin) * (2 * modulus - 1));
        if (cases != expected_cases) throw std::runtime_error("incomplete case coverage");
        std::cout << "{\"status\":\"VERIFIED\",\"full_domain\":"
                  << (expected_begin == 0 && expected_end == modulus ? "true" : "false")
                  << ",\"begin\":" << expected_begin << ",\"end\":" << expected_end
                  << ",\"cases\":" << cases << ",\"packing_bound\":" << packing_bound
                  << ",\"radius\":" << window_radius
                  << ",\"progressions\":" << static_cast<std::uint64_t>(cases) * packing_bound
                  << ",\"points\":" << static_cast<std::uint64_t>(cases) * points_per_case
                  << ",\"seconds\":"
                  << std::chrono::duration<double>(std::chrono::steady_clock::now() - start).count()
                  << "}\n";
    } catch (const std::exception& ex) {
        std::cerr << ex.what() << '\n';
        return EXIT_FAILURE;
    }
}
