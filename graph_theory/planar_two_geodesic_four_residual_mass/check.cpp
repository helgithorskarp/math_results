// Exact four-residual geodesic-pair checker for hard order-16 triangulations.
// Input: graph6 records selected by ../planar_two_geodesic_edge_deletion15/filter_hard.cpp.
// Standard C++17; no solver or external library.
#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

namespace {
constexpr int N = 16;
constexpr int PAIRS = N * (N - 1) / 2;
using Adj = std::array<std::uint16_t, N>;
using Dist = std::array<std::array<unsigned char, N>, N>;

Adj decode_graph6(const std::string& line) {
    if (line.size() != 1 + (PAIRS + 5) / 6 ||
        static_cast<unsigned char>(line[0]) != N + 63)
        throw std::runtime_error("invalid graph6 order or length");
    Adj adj{};
    int bit = 0;
    for (int v = 1; v < N; ++v)
        for (int u = 0; u < v; ++u, ++bit) {
            const int byte = static_cast<unsigned char>(line[1 + bit / 6]);
            if (byte < 63 || byte > 126)
                throw std::runtime_error("invalid graph6 byte");
            if (((byte - 63) >> (5 - bit % 6)) & 1) {
                adj[u] |= static_cast<std::uint16_t>(1u << v);
                adj[v] |= static_cast<std::uint16_t>(1u << u);
            }
        }
    for (; bit < 6 * (static_cast<int>(line.size()) - 1); ++bit)
        if (((static_cast<unsigned char>(line[1 + bit / 6]) - 63) >>
             (5 - bit % 6)) & 1)
            throw std::runtime_error("nonzero graph6 padding");
    int degree_sum = 0;
    for (auto row : adj) degree_sum += __builtin_popcount(row);
    if (degree_sum != 2 * (3 * N - 6))
        throw std::runtime_error("wrong triangulation edge count");
    return adj;
}

Dist distances(const Adj& adj) {
    Dist dist{};
    for (auto& row : dist) row.fill(255);
    for (int s = 0; s < N; ++s) {
        std::uint16_t seen = static_cast<std::uint16_t>(1u << s);
        std::uint16_t frontier = seen;
        dist[s][s] = 0;
        for (int step = 1; step <= 3 && frontier; ++step) {
            std::uint16_t next = 0;
            while (frontier) {
                const auto bit = static_cast<std::uint16_t>(frontier & -frontier);
                frontier ^= bit;
                next |= adj[__builtin_ctz(static_cast<unsigned>(bit))];
            }
            frontier = static_cast<std::uint16_t>(next & ~seen);
            seen |= frontier;
            std::uint16_t fresh = frontier;
            while (fresh) {
                const auto bit = static_cast<std::uint16_t>(fresh & -fresh);
                fresh ^= bit;
                dist[s][__builtin_ctz(static_cast<unsigned>(bit))] =
                    static_cast<unsigned char>(step);
            }
        }
        if (seen != 0xffffu)
            throw std::runtime_error("input is not connected with diameter at most three");
    }
    return dist;
}

std::vector<std::uint16_t> geodesics(const Adj& adj, const Dist& dist) {
    std::vector<std::uint16_t> paths;
    paths.reserve(500);
    for (int s = 0; s < N; ++s)
        paths.push_back(static_cast<std::uint16_t>(1u << s));
    for (int s = 0; s < N; ++s)
        for (int t = s + 1; t < N; ++t) {
            if (dist[s][t] == 1) {
                paths.push_back(static_cast<std::uint16_t>((1u << s) | (1u << t)));
            } else if (dist[s][t] == 2) {
                std::uint16_t middle = adj[s] & adj[t];
                while (middle) {
                    const auto bit = static_cast<std::uint16_t>(middle & -middle);
                    middle ^= bit;
                    paths.push_back(static_cast<std::uint16_t>((1u << s) | bit | (1u << t)));
                }
            } else if (dist[s][t] == 3) {
                std::uint16_t first = adj[s];
                while (first) {
                    const auto abit = static_cast<std::uint16_t>(first & -first);
                    first ^= abit;
                    const int a = __builtin_ctz(static_cast<unsigned>(abit));
                    std::uint16_t second = adj[a] & adj[t];
                    while (second) {
                        const auto bbit = static_cast<std::uint16_t>(second & -second);
                        second ^= bbit;
                        paths.push_back(static_cast<std::uint16_t>(
                            (1u << s) | abit | bbit | (1u << t)));
                    }
                }
            }
        }
    std::sort(paths.begin(), paths.end(), [](std::uint16_t x, std::uint16_t y) {
        return __builtin_popcount(x) > __builtin_popcount(y);
    });
    return paths;
}

bool four_residual(const Adj& adj, std::uint16_t removed) {
    std::uint16_t unseen = static_cast<std::uint16_t>(0xffffu & ~removed);
    while (unseen) {
        std::uint16_t frontier = static_cast<std::uint16_t>(unseen & -unseen);
        unseen ^= frontier;
        int size = 0;
        while (frontier) {
            const auto bit = static_cast<std::uint16_t>(frontier & -frontier);
            frontier ^= bit;
            if (++size > 4) return false;
            const int u = __builtin_ctz(static_cast<unsigned>(bit));
            const auto fresh = static_cast<std::uint16_t>(adj[u] & unseen);
            frontier |= fresh;
            unseen ^= fresh;
        }
    }
    return true;
}
}  // namespace

int main(int argc, char** argv) {
    try {
        if (argc != 1 && argc != 2)
            throw std::runtime_error("usage: check [expected-record-count]");
        const std::uint64_t expected = argc == 2 ? std::stoull(argv[1]) : 537814;
        std::uint64_t records = 0;
        std::string line;
        while (std::getline(std::cin, line)) {
            const Adj adj = decode_graph6(line);
            const Dist dist = distances(adj);
            const auto paths = geodesics(adj, dist);
            bool found = false;
            for (std::size_t i = 0; i < paths.size() && !found; ++i)
                for (std::size_t j = i; j < paths.size(); ++j)
                    if (four_residual(adj, paths[i] | paths[j])) {
                        found = true;
                        break;
                    }
            if (!found) {
                std::cerr << "NO_FOUR_RESIDUAL_PAIR " << line << '\n';
                return 2;
            }
            ++records;
        }
        if (!std::cin.eof() || records != expected)
            throw std::runtime_error("incomplete hard stream or count mismatch");
        std::cout << "{\"hard_roots\":" << records << ",\"failures\":0}\n";
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
