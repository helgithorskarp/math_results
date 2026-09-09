// Reviewer-owned exact check of the three centred 3+1+1 probabilities.
//
// This implementation regenerates every two-block palette by literal K5
// tests.  It then groups pairs of centre-neighbour type profiles by the
// physical closing-edge mask they force to blue and directly scans every
// closing matrix for every distinct mask.  It uses neither the producer's
// subset-zeta table nor the submitted C++ checker's type-permission table.
#include <array>
#include <bit>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <stdexcept>
#include <string>
#include <vector>

using u64 = std::uint64_t;

static std::array<std::array<unsigned, 8>, 8> pair_index{};
static std::vector<u64> five_edge_masks;

static void require(bool ok, const std::string& why) {
    if (!ok) throw std::runtime_error(why);
}

static void initialize_literal_masks() {
    unsigned answer = 0;
    for (unsigned u = 0; u < 8; ++u) {
        for (unsigned v = u + 1; v < 8; ++v, ++answer)
            pair_index[u][v] = pair_index[v][u] = answer;
    }
    require(answer == 28, "pair count");
    for (unsigned five = 0; five < 256; ++five) {
        if (std::popcount(five) != 5) continue;
        u64 edges = 0;
        for (unsigned u = 0; u < 8; ++u) {
            for (unsigned v = u + 1; v < 8; ++v) {
                if (((five >> u) & 1U) && ((five >> v) & 1U))
                    edges |= u64{1} << pair_index[u][v];
            }
        }
        five_edge_masks.push_back(edges);
    }
    require(five_edge_masks.size() == 56, "five-set count");
}

static bool contains_monochromatic_five(unsigned cross,
                                         unsigned first_colour,
                                         unsigned second_colour) {
    u64 red = 0;
    for (unsigned u = 0; u < 4; ++u) {
        for (unsigned v = u + 1; v < 4; ++v) {
            if (first_colour) red |= u64{1} << pair_index[u][v];
            if (second_colour) red |= u64{1} << pair_index[4 + u][4 + v];
        }
    }
    for (unsigned u = 0; u < 4; ++u) {
        for (unsigned v = 0; v < 4; ++v) {
            if ((cross >> (4 * u + v)) & 1U)
                red |= u64{1} << pair_index[u][4 + v];
        }
    }
    for (u64 edges : five_edge_masks) {
        const u64 overlap = red & edges;
        if (overlap == 0 || overlap == edges) return true;
    }
    return false;
}

static std::vector<unsigned> palette(unsigned first_colour,
                                     unsigned second_colour) {
    std::vector<unsigned> out;
    for (unsigned matrix = 0; matrix < 65536; ++matrix) {
        if (!contains_monochromatic_five(matrix, first_colour, second_colour))
            out.push_back(matrix);
    }
    return out;
}

static unsigned profile_code(unsigned matrix) {
    unsigned code = 0;
    unsigned place = 1;
    for (unsigned column = 0; column < 4; ++column) {
        unsigned mask = 0;
        for (unsigned row = 0; row < 4; ++row)
            mask |= ((matrix >> (4 * row + column)) & 1U) << row;
        require(mask != 15, "four centre-colour neighbours in pair palette");
        unsigned type = 0;
        if (std::popcount(mask) == 3) type = std::countr_zero((~mask) & 15U) + 1;
        code += place * type;
        place *= 5;
    }
    return code;
}

static std::array<unsigned, 4> decode_profile(unsigned code) {
    std::array<unsigned, 4> answer{};
    for (unsigned i = 0; i < 4; ++i) {
        answer[i] = code % 5;
        code /= 5;
    }
    require(code == 0, "profile overflow");
    return answer;
}

static std::array<u64, 625> histogram(const std::vector<unsigned>& domain) {
    std::array<u64, 625> answer{};
    for (unsigned matrix : domain) ++answer[profile_code(matrix)];
    return answer;
}

static unsigned forced_mask(unsigned left_code, unsigned right_code) {
    const auto left = decode_profile(left_code);
    const auto right = decode_profile(right_code);
    unsigned mask = 0;
    for (unsigned j = 0; j < 4; ++j) {
        for (unsigned k = 0; k < 4; ++k) {
            if (left[j] != 0 && left[j] == right[k])
                mask |= 1U << (4 * j + k);
        }
    }
    return mask;
}

struct Count {
    u64 allowed;
    u64 total;
    std::size_t masks;
};

static Count count_case(const std::array<u64, 625>& left,
                        const std::array<u64, 625>& right,
                        const std::vector<unsigned>& closing) {
    std::map<unsigned, u64> pair_weight;
    u64 left_total = 0, right_total = 0;
    for (unsigned a = 0; a < 625; ++a) left_total += left[a];
    for (unsigned b = 0; b < 625; ++b) right_total += right[b];
    for (unsigned a = 0; a < 625; ++a) {
        if (left[a] == 0) continue;
        for (unsigned b = 0; b < 625; ++b) {
            if (right[b] == 0) continue;
            pair_weight[forced_mask(a, b)] += left[a] * right[b];
        }
    }
    u64 answer = 0;
    for (const auto& [mask, weight] : pair_weight) {
        u64 permitted = 0;
        for (unsigned matrix : closing) permitted += ((matrix & mask) == 0);
        answer += weight * permitted;
    }
    return {answer, left_total * right_total * closing.size(), pair_weight.size()};
}

static void emit(std::ostream& out, const char* name, const Count& value,
                 bool trailing_comma) {
    out << "    \"" << name << "\": {\"allowed\": " << value.allowed
        << ", \"total\": " << value.total << ", \"mask_classes\": "
        << value.masks << "}" << (trailing_comma ? "," : "") << "\n";
}

int main(int argc, char** argv) {
    try {
        require(argc == 2, "usage: independent_check OUTPUT.json");
        initialize_literal_masks();
        const auto rr = palette(1, 1);
        const auto rb = palette(1, 0);
        const auto bb = palette(0, 0);
        require(rr.size() == 37823 && rb.size() == 35714 && bb.size() == 37823,
                "literal palette cardinalities");
        const auto hrr = histogram(rr);
        const auto hrb = histogram(rb);
        const Count same = count_case(hrr, hrr, rr);
        const Count majority = count_case(hrr, hrb, rb);
        const Count minority = count_case(hrb, hrb, bb);
        std::ofstream out(argv[1]);
        require(static_cast<bool>(out), "cannot open output");
        out << "{\n  \"status\": \"REVIEWER_LITERAL_MASK_SCAN_COMPLETE\",\n"
            << "  \"domains\": {\"RR\": " << rr.size() << ", \"RB\": "
            << rb.size() << ", \"BB\": " << bb.size() << "},\n"
            << "  \"probabilities\": {\n";
        emit(out, "same", same, true);
        emit(out, "majority", majority, true);
        emit(out, "minority", minority, false);
        out << "  }\n}\n";
        require(static_cast<bool>(out), "output write failed");
        std::cout << "REVIEWER_LITERAL_MASK_SCAN_COMPLETE\n";
        return 0;
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
