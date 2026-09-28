#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <vector>

// Independent three-colour hypergraph solver. Each edge forbids a constant
// colour on all of its two or three distinct vertices.
struct Solver {
    int n;
    std::vector<std::vector<int>> edges, incident;
    std::uint64_t nodes = 0;

    bool propagate(std::vector<unsigned char>& domain, std::vector<int>& pending) {
        while (!pending.empty()) {
            int v = pending.back();
            pending.pop_back();
            unsigned char bit = domain[v];
            if (bit != 1 && bit != 2 && bit != 4) return false;
            for (int e : incident[v]) {
                bool satisfied = false;
                int last = -1, unfixed = 0;
                for (int w : edges[e]) {
                    if (!(domain[w] & bit)) { satisfied = true; break; }
                    if (domain[w] != bit) { last = w; ++unfixed; }
                }
                if (satisfied || unfixed > 1) continue;
                if (unfixed == 0) return false;
                domain[last] &= static_cast<unsigned char>(~bit);
                if (!domain[last]) return false;
                if (domain[last] == 1 || domain[last] == 2 || domain[last] == 4)
                    pending.push_back(last);
            }
        }
        return true;
    }

    bool solve(std::vector<unsigned char> domain, std::vector<int> pending) {
        ++nodes;
        if (!propagate(domain, pending)) return false;
        int choice = -1;
        for (int v = 0; v < n; ++v) {
            if (domain[v] == 1 || domain[v] == 2 || domain[v] == 4) continue;
            if (choice < 0 || __builtin_popcount(domain[v]) < __builtin_popcount(domain[choice]) ||
                (__builtin_popcount(domain[v]) == __builtin_popcount(domain[choice]) &&
                 (incident[v].size() > incident[choice].size() ||
                  (incident[v].size() == incident[choice].size() && v > choice)))) choice = v;
        }
        if (choice < 0) {
            for (const auto& edge : edges) {
                unsigned char common = 7;
                for (int v : edge) common &= domain[v];
                if (common) return false;
            }
            return true;
        }
        for (unsigned char bit : {1, 2, 4}) {
            if (!(domain[choice] & bit)) continue;
            auto next = domain;
            next[choice] = bit;
            if (solve(next, {choice})) return true;
        }
        return false;
    }
};

int main() {
    int cases;
    if (!(std::cin >> cases)) return 2;
    for (int i = 0; i < cases; ++i) {
        int n, m, root;
        std::cin >> n >> m >> root;
        if (!std::cin || n < 1 || m < 0 || root < 0 || root >= n) return 2;
        Solver s{n, {}, std::vector<std::vector<int>>(n)};
        for (int e = 0; e < m; ++e) {
            int size; std::cin >> size;
            if (size < 2 || size > 3) return 2;
            std::vector<int> edge(size);
            for (int& v : edge) {
                std::cin >> v;
                if (!std::cin || v < 0 || v >= n) return 2;
                s.incident[v].push_back(e);
            }
            s.edges.push_back(edge);
        }
        std::vector<unsigned char> domain(n, 7);
        domain[root] = 1; // All three colours are symmetric.
        bool sat = s.solve(domain, {root});
        std::cout << i << ' ' << (sat ? "SAT" : "UNSAT") << ' ' << s.nodes << '\n';
    }
}
