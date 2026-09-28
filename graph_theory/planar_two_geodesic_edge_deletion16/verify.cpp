// Exact finite certificate for all planar graphs through order 16.
// Input: graph6 stream of all simple planar triangulations on 16 vertices
// produced by plantri 5.8 -g 15. Standard C++17, no external library.
#include <array>
#include <bitset>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <stdexcept>
#include <string>
#include <unordered_set>
#include <utility>
#include <vector>

namespace {
constexpr int N = 16;
constexpr int PAIRS = N * (N - 1) / 2;
using Adj = std::array<std::uint16_t, N>;
using Dist = std::array<std::array<unsigned char, N>, N>;
using EdgeSet = std::bitset<PAIRS>;

struct AdjHash {
    std::size_t operator()(const Adj& adj) const noexcept {
        std::uint64_t hash = 1469598103934665603ULL;
        for (std::uint16_t row : adj) {
            hash ^= row;
            hash *= 1099511628211ULL;
        }
        return static_cast<std::size_t>(hash);
    }
};

struct Path {
    std::uint16_t vertices;
    EdgeSet edges;
};

struct Counts {
    std::uint64_t records = 0;
    std::uint64_t initial_four_cut = 0;
    std::uint64_t initial_large_diameter = 0;
    std::uint64_t initial_hard = 0;
    std::uint64_t states = 0;
    std::uint64_t terminal_four_cut = 0;
    std::uint64_t terminal_large_diameter = 0;
    std::uint64_t internal = 0;
    int max_depth = 0;
};

std::vector<std::uint16_t> four_sets;
std::unordered_set<Adj, AdjHash> proven;
Counts counts;

int edge_id(int u, int v) {
    if (u > v) std::swap(u, v);
    return v * (v - 1) / 2 + u;
}

Adj delete_edge(Adj adj, int u, int v) {
    adj[u] &= static_cast<std::uint16_t>(~(1u << v));
    adj[v] &= static_cast<std::uint16_t>(~(1u << u));
    return adj;
}

bool balanced(const Adj& adj, std::uint16_t removed) {
    std::uint16_t unseen = static_cast<std::uint16_t>(((1u << N) - 1) & ~removed);
    while (unseen) {
        std::uint16_t frontier = static_cast<std::uint16_t>(unseen & -unseen);
        unseen ^= frontier;
        int size = 0;
        while (frontier) {
            std::uint16_t bit = static_cast<std::uint16_t>(frontier & -frontier);
            frontier ^= bit;
            if (++size > N / 2) return false;
            int u = __builtin_ctz(static_cast<unsigned>(bit));
            std::uint16_t fresh = adj[u] & unseen;
            frontier |= fresh;
            unseen ^= fresh;
        }
    }
    return true;
}

bool has_four_cut(const Adj& adj) {
    for (std::uint16_t removed : four_sets)
        if (balanced(adj, removed)) return true;
    return false;
}

bool distances_at_most_three(const Adj& adj, Dist& dist) {
    for (auto& row : dist) row.fill(255);
    for (int s = 0; s < N; ++s) {
        std::uint16_t seen = static_cast<std::uint16_t>(1u << s);
        std::uint16_t frontier = seen;
        dist[s][s] = 0;
        for (int step = 1; step <= 3 && frontier; ++step) {
            std::uint16_t next = 0;
            while (frontier) {
                std::uint16_t bit = static_cast<std::uint16_t>(frontier & -frontier);
                frontier ^= bit;
                next |= adj[__builtin_ctz(static_cast<unsigned>(bit))];
            }
            frontier = static_cast<std::uint16_t>(next & ~seen);
            seen |= frontier;
            std::uint16_t fresh = frontier;
            while (fresh) {
                std::uint16_t bit = static_cast<std::uint16_t>(fresh & -fresh);
                fresh ^= bit;
                dist[s][__builtin_ctz(static_cast<unsigned>(bit))] =
                    static_cast<unsigned char>(step);
            }
        }
        if (seen != (1u << N) - 1) return false;
    }
    return true;
}

Adj decode_graph6(std::string line) {
    if (line.compare(0, 10, ">>graph6<<") == 0) line.erase(0, 10);
    if (line.size() != 1 + (PAIRS + 5) / 6 ||
        static_cast<unsigned char>(line[0]) != N + 63)
        throw std::runtime_error("invalid graph6 length or order");
    Adj adj{};
    int bit = 0;
    for (int v = 1; v < N; ++v) {
        for (int u = 0; u < v; ++u, ++bit) {
            int byte = static_cast<unsigned char>(line[1 + bit / 6]);
            if (byte < 63 || byte > 126) throw std::runtime_error("invalid graph6 byte");
            if (((byte - 63) >> (5 - bit % 6)) & 1) {
                adj[u] |= static_cast<std::uint16_t>(1u << v);
                adj[v] |= static_cast<std::uint16_t>(1u << u);
            }
        }
    }
    for (; bit < 6 * (static_cast<int>(line.size()) - 1); ++bit)
        if (((static_cast<unsigned char>(line[1 + bit / 6]) - 63) >>
             (5 - bit % 6)) & 1)
            throw std::runtime_error("nonzero graph6 padding");
    int degree_sum = 0;
    for (std::uint16_t row : adj) degree_sum += __builtin_popcount(row);
    if (degree_sum != 2 * (3 * N - 6))
        throw std::runtime_error("non-triangulation edge count");
    return adj;
}

std::vector<Path> all_geodesics(const Adj& adj, const Dist& dist) {
    std::vector<Path> paths;
    paths.reserve(500);
    for (int u = 0; u < N; ++u)
        paths.push_back({static_cast<std::uint16_t>(1u << u), {}});
    for (int s = 0; s < N; ++s) {
        for (int t = s + 1; t < N; ++t) {
            if (dist[s][t] == 1) {
                EdgeSet edges;
                edges.set(edge_id(s, t));
                paths.push_back({static_cast<std::uint16_t>((1u << s) | (1u << t)), edges});
            } else if (dist[s][t] == 2) {
                std::uint16_t middle = adj[s] & adj[t];
                while (middle) {
                    std::uint16_t bit = static_cast<std::uint16_t>(middle & -middle);
                    middle ^= bit;
                    int a = __builtin_ctz(static_cast<unsigned>(bit));
                    EdgeSet edges;
                    edges.set(edge_id(s, a));
                    edges.set(edge_id(a, t));
                    paths.push_back({static_cast<std::uint16_t>((1u << s) | bit | (1u << t)), edges});
                }
            } else if (dist[s][t] == 3) {
                std::uint16_t first = adj[s];
                while (first) {
                    std::uint16_t abit = static_cast<std::uint16_t>(first & -first);
                    first ^= abit;
                    int a = __builtin_ctz(static_cast<unsigned>(abit));
                    std::uint16_t second = adj[a] & adj[t];
                    while (second) {
                        std::uint16_t bbit = static_cast<std::uint16_t>(second & -second);
                        second ^= bbit;
                        int b = __builtin_ctz(static_cast<unsigned>(bbit));
                        EdgeSet edges;
                        edges.set(edge_id(s, a));
                        edges.set(edge_id(a, b));
                        edges.set(edge_id(b, t));
                        paths.push_back({static_cast<std::uint16_t>((1u << s) | abit | bbit |
                                                                    (1u << t)), edges});
                    }
                }
            }
        }
    }
    return paths;
}

bool find_witness(const Adj& adj, const Dist& dist, const EdgeSet& easy,
                  EdgeSet& witness) {
    const auto paths = all_geodesics(adj, dist);
    std::size_t best_hard = 7, best_total = 7;
    bool found = false;
    for (std::size_t i = 0; i < paths.size(); ++i) {
        for (std::size_t j = i; j < paths.size(); ++j) {
            EdgeSet edges = paths[i].edges | paths[j].edges;
            std::size_t hard = (edges & ~easy).count();
            std::size_t total = edges.count();
            if (hard > best_hard || (hard == best_hard && total >= best_total))
                continue;
            if (!balanced(adj, paths[i].vertices | paths[j].vertices))
                continue;
            witness = edges;
            best_hard = hard;
            best_total = total;
            found = true;
            if (hard == 0) return true;
        }
    }
    return found;
}

bool certify(const Adj& adj, int depth) {
    if (proven.find(adj) != proven.end()) return true;
    ++counts.states;
    if (depth > counts.max_depth) counts.max_depth = depth;
    Dist dist{};
    if (!distances_at_most_three(adj, dist)) {
        ++counts.terminal_large_diameter;
        proven.insert(adj);
        return true;
    }
    if (has_four_cut(adj)) {
        ++counts.terminal_four_cut;
        proven.insert(adj);
        return true;
    }
    EdgeSet easy;
    for (int u = 0; u < N; ++u) {
        for (int v = u + 1; v < N; ++v) {
            if (!(adj[u] & (1u << v))) continue;
            Adj child = delete_edge(adj, u, v);
            Dist child_dist{};
            if (proven.find(child) != proven.end() ||
                !distances_at_most_three(child, child_dist) || has_four_cut(child))
                easy.set(edge_id(u, v));
        }
    }
    EdgeSet witness;
    if (!find_witness(adj, dist, easy, witness)) return false;
    ++counts.internal;
    EdgeSet hard = witness & ~easy;
    for (int u = 0; u < N; ++u) {
        for (int v = u + 1; v < N; ++v) {
            if (hard.test(edge_id(u, v)) &&
                !certify(delete_edge(adj, u, v), depth + 1))
                return false;
        }
    }
    proven.insert(adj);
    return true;
}

void make_four_sets() {
    for (int a = 0; a < N; ++a)
        for (int b = a + 1; b < N; ++b)
            for (int c = b + 1; c < N; ++c)
                for (int d = c + 1; d < N; ++d)
                    four_sets.push_back(static_cast<std::uint16_t>((1u << a) |
                        (1u << b) | (1u << c) | (1u << d)));
}
} // namespace

int main() {
    try {
        make_four_sets();
        std::string line;
        while (std::getline(std::cin, line)) {
            Adj adj = decode_graph6(line);
            ++counts.records;
            if (has_four_cut(adj)) {
                ++counts.initial_four_cut;
                continue;
            }
            Dist dist{};
            if (!distances_at_most_three(adj, dist)) {
                ++counts.initial_large_diameter;
                continue;
            }
            ++counts.initial_hard;
            if (!certify(adj, 0)) {
                std::cerr << "UNCERTIFIED graph6: " << line << '\n';
                return 2;
            }
            if (counts.initial_hard % 10000 == 0)
                std::cerr << "checked hard roots: " << counts.initial_hard << '\n';
        }
        if (!std::cin.eof() || counts.records == 0)
            throw std::runtime_error("incomplete or empty graph6 stream");
        if (counts.records != 17490241 ||
            counts.initial_four_cut != 16875528 ||
            counts.initial_large_diameter != 76899 ||
            counts.initial_hard != 537814 ||
            counts.states != 1995878 || counts.internal != 1995878 ||
            counts.terminal_four_cut != 0 ||
            counts.terminal_large_diameter != 0 ||
            counts.max_depth != 9)
            throw std::runtime_error("order-16 census counts differ from certified run");
        std::cout << "{\"records\":" << counts.records
                  << ",\"initial_four_cut\":" << counts.initial_four_cut
                  << ",\"initial_large_diameter\":" << counts.initial_large_diameter
                  << ",\"initial_hard\":" << counts.initial_hard
                  << ",\"states\":" << counts.states
                  << ",\"terminal_four_cut\":" << counts.terminal_four_cut
                  << ",\"terminal_large_diameter\":" << counts.terminal_large_diameter
                  << ",\"internal\":" << counts.internal
                  << ",\"max_depth\":" << counts.max_depth << "}\n";
        return 0;
    } catch (const std::exception& error) {
        std::cerr << "verify: " << error.what() << '\n';
        return 1;
    }
}
