#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <set>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

using Code = std::uint32_t;
using Map = std::array<std::uint8_t, 16>;
using Count = std::uint64_t;

static int vector_rank(const std::vector<int>& values) {
    std::array<int, 4> basis{};
    int rank = 0;
    for (int x : values) {
        for (int bit = 3; bit >= 0 && x; --bit) {
            if (!((x >> bit) & 1)) continue;
            if (basis[bit]) x ^= basis[bit];
            else { basis[bit] = x; ++rank; break; }
        }
    }
    return rank;
}

static int multiplicity(Code code, int x) {
    return static_cast<int>((code >> (2 * (x - 1))) & 3U);
}

static int weight(Code code) {
    int result = 0;
    for (int x = 1; x < 16; ++x) result += multiplicity(code, x);
    return result;
}

static int support_rank(Code code) {
    std::vector<int> values;
    for (int x = 1; x < 16; ++x)
        if (multiplicity(code, x)) values.push_back(x);
    return vector_rank(values);
}

static Code transform(Code code, const Map& image) {
    Code result = 0;
    for (int x = 1; x < 16; ++x)
        result |= static_cast<Code>(multiplicity(code, x))
                  << (2 * (image[x] - 1));
    return result;
}

static int dot(int x, int y) {
    return __builtin_popcount(static_cast<unsigned>(x & y)) & 1;
}

static std::string category(Code code) {
    if (weight(code) == 19) return "zero_row";
    bool full_double = true;
    for (int x = 1; x < 16; ++x)
        full_double &= multiplicity(code, x) == 1 || multiplicity(code, x) == 2;
    if (full_double) return "known_profile_guard";
    for (int u = 1; u < 16; ++u) {
        bool affine = true;
        for (int x = 1; x < 16; ++x)
            if (multiplicity(code, x) && !dot(u, x)) affine = false;
        if (affine) return "affine_rows";
    }
    return "ordinary";
}

int main(int argc, char** argv) {
    try {
        if (argc != 2) throw std::runtime_error("usage: orbit_check row_cover.tsv");

        // Unlike the reviewed checker, enumerate all 2^16 matrices and retain
        // the invertible ones, instead of generating ordered bases recursively.
        std::vector<Map> group;
        std::set<Map> unique;
        for (unsigned matrix = 0; matrix < 65536; ++matrix) {
            std::vector<int> columns(4);
            for (int k = 0; k < 4; ++k) columns[k] = (matrix >> (4 * k)) & 15U;
            if (vector_rank(columns) != 4) continue;
            Map image{};
            for (int x = 1; x < 16; ++x)
                for (int k = 0; k < 4; ++k)
                    if ((x >> k) & 1) image[x] ^= columns[k];
            group.push_back(image);
            unique.insert(image);
        }
        if (group.size() != 20160 || unique.size() != group.size())
            throw std::runtime_error("GL(4,2) enumeration failed");

        std::ifstream input(argv[1]);
        if (!input) throw std::runtime_error("cannot open cover table");
        std::string header;
        std::getline(input, header);
        if (header != "code\tzero\torbit_size\tsupport\ttriples")
            throw std::runtime_error("wrong table header");

        Count rows = 0, checks = 0;
        std::array<Count, 2> mass{};
        std::map<std::string, Count> categories;
        std::map<int, Count> stabilizers;
        Code previous = 0;
        bool first = true;
        for (std::string line; std::getline(input, line); ) {
            std::istringstream parser(line);
            Count large_code, orbit;
            int zero, support, triples;
            std::string extra;
            if (!(parser >> large_code >> zero >> orbit >> support >> triples) ||
                (parser >> extra) || large_code >= (Count{1} << 30))
                throw std::runtime_error("malformed table row");
            Code code = static_cast<Code>(large_code);
            if ((!first && code <= previous) || weight(code) < 19 || weight(code) > 20)
                throw std::runtime_error("row order or weight");
            first = false;
            previous = code;
            if (zero != 20 - weight(code) || support_rank(code) != 4)
                throw std::runtime_error("zero count or span");
            int actual_support = 0, actual_triples = 0;
            for (int x = 1; x < 16; ++x) {
                actual_support += multiplicity(code, x) > 0;
                actual_triples += multiplicity(code, x) == 3;
            }
            if (support != actual_support || triples != actual_triples)
                throw std::runtime_error("metadata mismatch");

            Code minimum = code;
            Count stabilizer = 0;
            for (const auto& image : group) {
                Code moved = transform(code, image);
                if (moved < minimum) minimum = moved;
                stabilizer += moved == code;
                ++checks;
            }
            if (minimum != code || !stabilizer || 20160 % stabilizer ||
                orbit != 20160 / stabilizer)
                throw std::runtime_error("canonicality or orbit-size mismatch");
            ++rows;
            mass[weight(code) - 19] += orbit;
            ++categories[category(code)];
            ++stabilizers[static_cast<int>(stabilizer)];
        }
        if (!input.eof()) throw std::runtime_error("table read failure");
        if (rows != 10959 || mass != std::array<Count, 2>{71475180, 83372457})
            throw std::runtime_error("table coverage mismatch");
        const std::map<std::string, Count> expected_categories{
            {"affine_rows", 5}, {"known_profile_guard", 4},
            {"ordinary", 5841}, {"zero_row", 5109}
        };
        if (categories != expected_categories) throw std::runtime_error("category mismatch");

        std::cout << "{\"canonical_map_checks\":" << checks
                  << ",\"category_counts\":{";
        bool comma = false;
        for (const auto& [name, count] : categories) {
            if (comma) std::cout << ',';
            comma = true;
            std::cout << '\"' << name << "\":" << count;
        }
        std::cout << "},\"group_order\":" << group.size()
                  << ",\"matrix_candidates\":65536,\"profile_mass\":["
                  << mass[0] << ',' << mass[1] << "],\"table_rows\":" << rows
                  << ",\"status\":\"VERIFIED_INDEPENDENT_ORBIT_TABLE\"}\n";
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
