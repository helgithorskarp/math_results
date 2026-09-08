#include <algorithm>
#include <array>
#include <bit>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <queue>
#include <stdexcept>
#include <string>
#include <vector>

using Graph = std::vector<std::uint16_t>;

static Graph decode_graph6(const std::string &line, int expected_order) {
    if (expected_order < 1 || expected_order > 15 || line.empty() ||
        static_cast<unsigned char>(line[0]) - 63 != expected_order) {
        throw std::runtime_error("bad graph6 header");
    }
    const int edge_bits = expected_order * (expected_order - 1) / 2;
    const int payload = (edge_bits + 5) / 6;
    if (static_cast<int>(line.size()) != payload + 1) {
        throw std::runtime_error("bad graph6 length");
    }
    Graph adjacency(expected_order, 0);
    int bit_index = 0;
    for (int j = 1; j < expected_order; ++j) {
        for (int i = 0; i < j; ++i, ++bit_index) {
            int value = static_cast<unsigned char>(line[1 + bit_index / 6]) - 63;
            if (value < 0 || value >= 64) throw std::runtime_error("bad graph6 character");
            if ((value >> (5 - bit_index % 6)) & 1) {
                adjacency[i] |= std::uint16_t(1U << j);
                adjacency[j] |= std::uint16_t(1U << i);
            }
        }
    }
    const int spare = 6 * payload - edge_bits;
    int last = static_cast<unsigned char>(line.back()) - 63;
    if (spare && (last & ((1 << spare) - 1))) throw std::runtime_error("nonzero graph6 padding");
    return adjacency;
}

static bool contains_k23(const Graph &a) {
    for (int u = 0; u < static_cast<int>(a.size()); ++u) {
        for (int v = u + 1; v < static_cast<int>(a.size()); ++v) {
            if (std::popcount(static_cast<unsigned>(a[u] & a[v])) >= 3) return true;
        }
    }
    return false;
}

static std::vector<int> canonical_cycle(std::vector<int> cycle) {
    std::vector<int> best;
    const int n = static_cast<int>(cycle.size());
    for (int reversal = 0; reversal < 2; ++reversal) {
        if (reversal) std::reverse(cycle.begin(), cycle.end());
        for (int shift = 0; shift < n; ++shift) {
            std::vector<int> candidate;
            for (int i = 0; i < n; ++i) candidate.push_back(cycle[(i + shift) % n]);
            if (best.empty() || candidate < best) best = candidate;
        }
    }
    return best;
}

static bool neighbourhoods_bipartite(const Graph &a, int &bad_center,
                                     std::vector<int> &odd_cycle) {
    const int n = static_cast<int>(a.size());
    for (int center = 0; center < n; ++center) {
        const std::uint16_t neighbours = a[center];
        std::array<int, 16> colour, parent;
        colour.fill(-1); parent.fill(-1);
        for (int root = 0; root < n; ++root) {
            if (!((neighbours >> root) & 1) || colour[root] >= 0) continue;
            std::queue<int> queue;
            colour[root] = 0; queue.push(root);
            while (!queue.empty()) {
                const int u = queue.front(); queue.pop();
                std::uint16_t pending = a[u] & neighbours;
                while (pending) {
                    const int v = std::countr_zero(static_cast<unsigned>(pending));
                    pending &= pending - 1;
                    if (colour[v] < 0) {
                        colour[v] = colour[u] ^ 1; parent[v] = u; queue.push(v);
                    } else if (colour[v] == colour[u]) {
                        std::vector<int> up, vp;
                        for (int x = u; x >= 0; x = parent[x]) up.push_back(x);
                        for (int x = v; x >= 0; x = parent[x]) vp.push_back(x);
                        int i = static_cast<int>(up.size()) - 1;
                        int j = static_cast<int>(vp.size()) - 1;
                        while (i >= 0 && j >= 0 && up[i] == vp[j]) { --i; --j; }
                        std::vector<int> cycle;
                        for (int k = 0; k <= i + 1; ++k) cycle.push_back(up[k]);
                        for (int k = j; k >= 0; --k) cycle.push_back(vp[k]);
                        bad_center = center;
                        odd_cycle = canonical_cycle(cycle);
                        return false;
                    }
                }
            }
        }
    }
    return true;
}

struct Counts { std::uint64_t total = 0, k23_free = 0, locally_admissible = 0; };
struct Exception { int order, edges, center; std::string graph6; std::vector<int> cycle; };

int main(int argc, char **argv) try {
    if (argc != 2) throw std::runtime_error("usage: scan CATALOG_DIRECTORY");
    const std::string root = argv[1];
    const std::array<int, 8> orders = {5, 7, 8, 9, 10, 11, 12, 13};
    std::map<int, Counts> results;
    std::vector<Exception> exceptions;
    for (int order : orders) {
        std::ifstream source(root + "/crit_" + std::to_string(order) + "_5.g6");
        if (!source) throw std::runtime_error("missing catalog for order " + std::to_string(order));
        std::string line;
        while (std::getline(source, line)) {
            if (!line.empty() && line.back() == '\r') line.pop_back();
            if (line.empty()) continue;
            Graph graph = decode_graph6(line, order);
            ++results[order].total;
            if (contains_k23(graph)) continue;
            ++results[order].k23_free;
            int center = -1; std::vector<int> cycle;
            if (!neighbourhoods_bipartite(graph, center, cycle)) {
                int twice_edges = 0;
                for (auto row : graph) twice_edges += std::popcount(static_cast<unsigned>(row));
                exceptions.push_back({order, twice_edges / 2, center, line, cycle});
                continue;
            }
            ++results[order].locally_admissible;
        }
    }
    std::cout << "{\n  \"status\": \"NO_LOCALLY_ADMISSIBLE_EDGE_5_CRITICAL_GRAPH_THROUGH_13\",\n";
    std::cout << "  \"orders\": {\n";
    for (std::size_t k = 0; k < orders.size(); ++k) {
        int n = orders[k]; const auto &r = results[n];
        std::cout << "    \"" << n << "\": {\"total\": " << r.total
                  << ", \"k23_free\": " << r.k23_free
                  << ", \"locally_admissible\": " << r.locally_admissible << "}"
                  << (k + 1 == orders.size() ? "\n" : ",\n");
    }
    std::cout << "  },\n  \"k23_free_exceptions\": [\n";
    for (std::size_t k = 0; k < exceptions.size(); ++k) {
        const auto &e = exceptions[k];
        std::cout << "    {\n      \"order\": " << e.order << ",\n      \"graph6\": \""
                  << e.graph6 << "\",\n      \"edges\": " << e.edges
                  << ",\n      \"odd_neighbourhood\": {\n        \"center\": " << e.center
                  << ",\n        \"cycle\": [";
        for (std::size_t i = 0; i < e.cycle.size(); ++i)
            std::cout << (i ? ", " : "") << e.cycle[i];
        std::cout << "]\n      }\n    }" << (k + 1 == exceptions.size() ? "\n" : ",\n");
    }
    std::cout << "  ]\n}\n";
    return 0;
} catch (const std::exception &error) {
    std::cerr << error.what() << '\n'; return 2;
}
