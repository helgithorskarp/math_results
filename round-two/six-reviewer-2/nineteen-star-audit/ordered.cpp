// Independent ordered clique enumeration. No coloring or pivot/maximal recursion.
#include <algorithm>
#include <chrono>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

struct Bits {
    std::uint64_t lo = 0, hi = 0;
    bool any() const { return lo != 0 || hi != 0; }
    int count() const { return __builtin_popcountll(lo) + __builtin_popcountll(hi); }
    void set(int i) { if (i < 64) lo |= UINT64_C(1) << i;
                     else hi |= UINT64_C(1) << (i - 64); }
    bool contains(int i) const { return i < 64 ? (lo >> i & 1U) != 0
                                               : (hi >> (i - 64) & 1U) != 0; }
    int take() {
        if (lo != 0) { int i = __builtin_ctzll(lo); lo &= lo - 1; return i; }
        if (hi == 0) throw std::runtime_error("empty bitset take");
        int i = __builtin_ctzll(hi); hi &= hi - 1; return i + 64;
    }
};
Bits operator&(Bits a, Bits b) { return {a.lo & b.lo, a.hi & b.hi}; }

class Census {
    const std::vector<Bits>& adjacency;
    const int target;
    std::chrono::steady_clock::time_point started = std::chrono::steady_clock::now();
    std::vector<int> chosen;
public:
    std::uint64_t nodes = 0;
    bool larger_clique = false;
    std::vector<std::vector<int>> found;
    Census(const std::vector<Bits>& graph, int size): adjacency(graph), target(size) {}
    void visit(Bits available) {
        ++nodes;
        if (nodes > UINT64_C(2000000)) throw std::runtime_error("INCOMPLETE: node guard");
        if ((nodes & UINT64_C(1023)) == 0 &&
            std::chrono::duration<double>(std::chrono::steady_clock::now() - started).count() > 20.0)
            throw std::runtime_error("INCOMPLETE: time guard");
        int need = target - static_cast<int>(chosen.size());
        if (need == 0) {
            found.push_back(chosen);
            if (available.any()) larger_clique = true;
            return;
        }
        while (available.count() >= need) {
            int vertex = available.take();
            chosen.push_back(vertex);
            visit(available & adjacency[static_cast<std::size_t>(vertex)]);
            chosen.pop_back();
        }
    }
};

int main() {
    try {
        int n = 0, target = 0;
        if (!(std::cin >> n >> target) || n < 1 || n > 128 || target < 1 || target > n)
            throw std::runtime_error("malformed graph header");
        std::vector<Bits> adjacency(static_cast<std::size_t>(n));
        for (int i = 0; i < n; ++i) {
            int degree = 0;
            if (!(std::cin >> degree) || degree < 0 || degree >= n)
                throw std::runtime_error("malformed row size");
            for (int k = 0; k < degree; ++k) {
                int j = 0;
                if (!(std::cin >> j) || j < 0 || j >= n || i == j || adjacency[i].contains(j))
                    throw std::runtime_error("malformed row entry");
                adjacency[i].set(j);
            }
        }
        for (int i = 0; i < n; ++i) for (int j = 0; j < n; ++j)
            if (adjacency[i].contains(j) != adjacency[j].contains(i))
                throw std::runtime_error("asymmetric graph");
        std::string trailing;
        if (std::cin >> trailing) throw std::runtime_error("trailing input after graph");
        Bits available;
        for (int i = 0; i < n; ++i) available.set(i);
        Census census(adjacency, target);
        census.visit(available);
        std::cout << "{\"status\":\"COMPLETE\",\"nodes\":" << census.nodes
                  << ",\"larger_clique\":" << (census.larger_clique ? "true" : "false")
                  << ",\"cliques\":[";
        for (std::size_t i = 0; i < census.found.size(); ++i) {
            if (i != 0) std::cout << ',';
            std::cout << '[';
            for (std::size_t j = 0; j < census.found[i].size(); ++j) {
                if (j != 0) std::cout << ',';
                std::cout << census.found[i][j];
            }
            std::cout << ']';
        }
        std::cout << "]}\n";
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 2;
    }
}
