#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

using Mask = std::uint32_t;

static bool balanced(const std::vector<Mask>& adj, Mask removed) {
    const int n = static_cast<int>(adj.size());
    const int cutoff = n / 2;
    Mask unseen = ((Mask{1} << n) - 1) & ~removed;
    while (unseen) {
        Mask frontier = unseen & -unseen;
        unseen ^= frontier;
        int size = 0;
        while (frontier) {
            Mask bit = frontier & -frontier;
            frontier ^= bit;
            if (++size > cutoff) return false;
            int u = __builtin_ctz(bit);
            Mask fresh = adj[u] & unseen;
            frontier |= fresh;
            unseen &= ~fresh;
        }
    }
    return true;
}

static bool has_four_cut(const std::vector<Mask>& adj) {
    const int n = static_cast<int>(adj.size());
    for (int a = 0; a < n; ++a)
        for (int b = a + 1; b < n; ++b)
            for (int c = b + 1; c < n; ++c)
                for (int d = c + 1; d < n; ++d)
                    if (balanced(adj, (Mask{1} << a) | (Mask{1} << b) |
                                      (Mask{1} << c) | (Mask{1} << d)))
                        return true;
    return false;
}

static bool diameter_at_most_three(const std::vector<Mask>& adj) {
    const int n = static_cast<int>(adj.size());
    const Mask all = (Mask{1} << n) - 1;
    for (int s = 0; s < n; ++s) {
        Mask seen = Mask{1} << s, frontier = seen;
        for (int step = 0; step < 3 && frontier; ++step) {
            Mask next = 0;
            while (frontier) {
                Mask bit = frontier & -frontier;
                frontier ^= bit;
                next |= adj[__builtin_ctz(bit)];
            }
            frontier = next & ~seen;
            seen |= frontier;
        }
        if (seen != all) return false;
    }
    return true;
}

int main(int argc, char** argv) {
    try {
        if (argc != 2) throw std::runtime_error("usage: no4-d3-filter ORDER");
        const int n = std::stoi(argv[1]);
        if (n < 1 || n > 30) throw std::runtime_error("order outside 1..30");
        std::uint64_t total = 0, no_four = 0, selected = 0;
        std::string line;
        while (std::getline(std::cin, line)) {
            const int bits = n * (n - 1) / 2;
            if (line.size() != static_cast<std::size_t>(1 + (bits + 5) / 6) ||
                static_cast<unsigned char>(line[0]) != n + 63)
                throw std::runtime_error("bad graph6 record");
            std::vector<Mask> adj(n, 0);
            int k = 0;
            for (int v = 1; v < n; ++v)
                for (int u = 0; u < v; ++u, ++k) {
                    const int byte = static_cast<unsigned char>(line[1 + k / 6]);
                    if (byte < 63 || byte > 126) throw std::runtime_error("bad byte");
                    if (((byte - 63) >> (5 - k % 6)) & 1) {
                        adj[u] |= Mask{1} << v;
                        adj[v] |= Mask{1} << u;
                    }
                }
            for (; k < 6 * (static_cast<int>(line.size()) - 1); ++k)
                if (((static_cast<unsigned char>(line[1 + k / 6]) - 63) >>
                     (5 - k % 6)) & 1)
                    throw std::runtime_error("nonzero padding");
            int degree_sum = 0;
            for (Mask row : adj) degree_sum += __builtin_popcount(row);
            if (degree_sum != 2 * (3 * n - 6))
                throw std::runtime_error("non-triangulation edge count");
            ++total;
            if (!has_four_cut(adj)) {
                ++no_four;
                if (diameter_at_most_three(adj)) {
                    ++selected;
                    std::cout << line << '\n';
                    if (!std::cout) throw std::runtime_error("output failure");
                }
            }
        }
        if (!std::cin.eof()) throw std::runtime_error("input failure");
        if (n == 15 && (total != 2406841 || no_four != 96159 || selected != 90540))
            throw std::runtime_error("hard-stream count mismatch");
        std::cerr << "{\"total\":" << total << ",\"no_four_cut\":"
                  << no_four << ",\"no_four_cut_diameter_at_most_three\":"
                  << selected << "}\n";
        return 0;
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
