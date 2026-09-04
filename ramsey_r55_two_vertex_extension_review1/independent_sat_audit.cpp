#include "cadical.hpp"

#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <map>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

namespace {

constexpr int N = 41;
constexpr uint64_t ALL = (uint64_t{1} << N) - 1;

struct Graph {
    std::array<uint64_t, N> nbr{};
};

Graph decode_graph6(const std::string &line) {
    if (line.empty() || static_cast<unsigned char>(line[0]) - 63 != N)
        throw std::runtime_error("expected a small graph6 record of order 41");
    std::vector<unsigned> bits;
    for (std::size_t p = 1; p < line.size(); ++p) {
        unsigned x = static_cast<unsigned char>(line[p]) - 63;
        if (x > 63) throw std::runtime_error("invalid graph6 byte");
        for (int shift = 5; shift >= 0; --shift) bits.push_back((x >> shift) & 1U);
    }
    if (bits.size() < N * (N - 1) / 2) throw std::runtime_error("truncated graph6 record");
    Graph g;
    std::size_t at = 0;
    for (int j = 1; j < N; ++j) {
        for (int i = 0; i < j; ++i) {
            if (bits[at]) {
                g.nbr[i] |= uint64_t{1} << j;
                g.nbr[j] |= uint64_t{1} << i;
            }
            ++at;
        }
    }
    return g;
}

bool clique(const Graph &g, const std::array<int, 4> &v, bool edge) {
    for (int i = 0; i < 4; ++i) {
        for (int j = i + 1; j < 4; ++j) {
            bool present = (g.nbr[v[i]] >> v[j]) & 1U;
            if (present != edge) return false;
        }
    }
    return true;
}

bool has_clique_rec(const std::array<uint64_t, N> &nbr, uint64_t candidates, int left) {
    if (left == 0) return true;
    if (__builtin_popcountll(candidates) < left) return false;
    while (candidates) {
        uint64_t bit = candidates & -candidates;
        int v = __builtin_ctzll(bit);
        candidates ^= bit;
        if (has_clique_rec(nbr, candidates & nbr[v], left - 1)) return true;
    }
    return false;
}

std::array<uint64_t, N> complement_neighbors(const Graph &g) {
    std::array<uint64_t, N> result{};
    for (int v = 0; v < N; ++v) result[v] = ALL & ~(g.nbr[v] | (uint64_t{1} << v));
    return result;
}

bool has_triangle(const std::array<uint64_t, N> &nbr, uint64_t candidates) {
    while (candidates) {
        uint64_t vb = candidates & -candidates;
        int v = __builtin_ctzll(vb);
        candidates ^= vb;
        uint64_t adjacent = candidates & nbr[v];
        while (adjacent) {
            uint64_t wb = adjacent & -adjacent;
            int w = __builtin_ctzll(wb);
            adjacent ^= wb;
            if (candidates & nbr[v] & nbr[w]) return true;
        }
    }
    return false;
}

std::vector<std::vector<uint64_t>> read_models(const std::string &path, std::size_t count) {
    std::ifstream in(path);
    if (!in) throw std::runtime_error("cannot open model certificate");
    std::vector<std::vector<uint64_t>> result;
    std::string line;
    while (std::getline(in, line)) {
        std::istringstream row(line);
        std::size_t index = 0, number = 0;
        char colon = 0;
        if (!(row >> index >> colon >> number) || colon != ':' || index != result.size())
            throw std::runtime_error("malformed certificate row");
        std::vector<uint64_t> models;
        for (std::size_t i = 0; i < number; ++i) {
            std::string token;
            if (!(row >> token)) throw std::runtime_error("missing model token");
            uint64_t model = std::stoull(token, nullptr, 16);
            if (model & ~ALL) throw std::runtime_error("model has an out-of-range bit");
            models.push_back(model);
        }
        std::string extra;
        if (row >> extra) throw std::runtime_error("extra certificate token");
        std::sort(models.begin(), models.end());
        if (std::adjacent_find(models.begin(), models.end()) != models.end())
            throw std::runtime_error("duplicate certificate model");
        result.push_back(std::move(models));
    }
    if (result.size() != count) throw std::runtime_error("certificate row count mismatch");
    return result;
}

void add_clause(CaDiCaL::Solver &solver, const std::array<int, 4> &v, bool positive) {
    for (int x : v) solver.add(positive ? x + 1 : -(x + 1));
    solver.add(0);
}

std::vector<uint64_t> enumerate_with_sat(const Graph &g) {
    CaDiCaL::Solver solver;
    for (int a = 0; a < N; ++a) for (int b = a + 1; b < N; ++b)
    for (int c = b + 1; c < N; ++c) for (int d = c + 1; d < N; ++d) {
        std::array<int, 4> v{a, b, c, d};
        if (clique(g, v, true)) add_clause(solver, v, false);
        if (clique(g, v, false)) add_clause(solver, v, true);
    }

    std::vector<uint64_t> models;
    for (;;) {
        int status = solver.solve();
        if (status == 20) break;
        if (status != 10) throw std::runtime_error("CaDiCaL returned an unexpected status");
        uint64_t model = 0;
        for (int v = 0; v < N; ++v) {
            if (solver.val(v + 1) > 0) model |= uint64_t{1} << v;
        }
        for (int v = 0; v < N; ++v)
            solver.add((model & (uint64_t{1} << v)) ? -(v + 1) : v + 1);
        solver.add(0);
        models.push_back(model);
    }
    std::sort(models.begin(), models.end());
    return models;
}

}  // namespace

int main(int argc, char **argv) try {
    if (argc != 3) {
        std::cerr << "usage: independent_sat_audit CORES.g6 MODELS.txt\n";
        return 2;
    }

    std::ifstream input(argv[1]);
    if (!input) throw std::runtime_error("cannot open graph6 cores");
    std::vector<Graph> graphs;
    std::string line;
    while (std::getline(input, line)) if (!line.empty()) graphs.push_back(decode_graph6(line));
    auto certificate = read_models(argv[2], graphs.size());

    uint64_t total_models = 0, total_pairs = 0;
    std::map<std::size_t, std::size_t> multiplicities;
    for (std::size_t index = 0; index < graphs.size(); ++index) {
        const Graph &g = graphs[index];
        auto nonnbr = complement_neighbors(g);
        if (has_clique_rec(g.nbr, ALL, 5) || has_clique_rec(nonnbr, ALL, 5))
            throw std::runtime_error("core contains a homogeneous five-set");

        auto exact = enumerate_with_sat(g);
        if (exact != certificate[index]) {
            std::ostringstream msg;
            msg << "SAT model mismatch at core " << index;
            throw std::runtime_error(msg.str());
        }

        for (uint64_t x : exact) for (uint64_t y : exact) {
            ++total_pairs;
            if (!has_triangle(g.nbr, x & y))
                throw std::runtime_error("unobstructed present new-new edge");
            if (!has_triangle(nonnbr, ALL & ~(x | y)))
                throw std::runtime_error("unobstructed absent new-new edge");
        }
        total_models += exact.size();
        ++multiplicities[exact.size()];
        if ((index + 1) % 1000 == 0) std::cout << "checked=" << index + 1 << '\n';
    }

    std::cout << "SAT_VERIFIED cores=" << graphs.size()
              << " models=" << total_models
              << " ordered_pairs=" << total_pairs << '\n';
    std::cout << "multiplicities";
    for (const auto &[models, cores] : multiplicities)
        std::cout << ' ' << models << ':' << cores;
    std::cout << '\n';
    return 0;
} catch (const std::exception &e) {
    std::cerr << "error: " << e.what() << '\n';
    return 1;
}
