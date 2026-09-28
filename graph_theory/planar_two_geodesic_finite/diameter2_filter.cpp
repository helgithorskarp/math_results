// Streaming graph6 filter: retain exactly graphs of diameter at most two.
// C++17; vertices are 0,...,n-1 and fit in uint64_t masks (n <= 62).
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

int main(int argc, char** argv) {
    try {
        if (argc != 2) throw std::runtime_error("usage: diameter2_filter ORDER");
        const int expected = std::stoi(argv[1]);
        if (expected < 1 || expected > 62) throw std::runtime_error("order outside 1..62");
        std::uint64_t total = 0, selected = 0;
        std::string line;
        while (std::getline(std::cin, line)) {
            if (line.compare(0, 10, ">>graph6<<") == 0) line.erase(0, 10);
            if (line.empty()) throw std::runtime_error("empty graph6 record");
            const int n = static_cast<unsigned char>(line[0]) - 63;
            if (n != expected) throw std::runtime_error("wrong graph order");
            const int m = n * (n - 1) / 2;
            if (line.size() != static_cast<std::size_t>(1 + (m + 5) / 6))
                throw std::runtime_error("wrong graph6 length");
            std::vector<std::uint64_t> adj(n, 0);
            int index = 0;
            auto getbit = [&]() {
                const unsigned char c = static_cast<unsigned char>(line[1 + index / 6]);
                if (c < 63 || c > 126) throw std::runtime_error("bad graph6 byte");
                const int bit = ((c - 63) >> (5 - index % 6)) & 1;
                ++index;
                return bit;
            };
            for (int v = 1; v < n; ++v) {
                for (int u = 0; u < v; ++u) {
                    if (getbit()) {
                        adj[u] |= std::uint64_t{1} << v;
                        adj[v] |= std::uint64_t{1} << u;
                    }
                }
            }
            while (index < ((m + 5) / 6) * 6) {
                if (getbit()) throw std::runtime_error("nonzero graph6 padding");
            }
            bool diameter2 = true;
            for (int v = 1; v < n && diameter2; ++v) {
                for (int u = 0; u < v; ++u) {
                    if ((adj[u] & (std::uint64_t{1} << v)) == 0 &&
                        (adj[u] & adj[v]) == 0) {
                        diameter2 = false;
                        break;
                    }
                }
            }
            ++total;
            if (diameter2) {
                ++selected;
                std::cout << line << '\n';
                if (!std::cout) throw std::runtime_error("output failure");
            }
        }
        if (!std::cin.eof()) throw std::runtime_error("input failure");
        if (total == 0) throw std::runtime_error("empty input");
        std::cerr << "{\"filter_total\":" << total << ",\"diameter_at_most_2\":" << selected << "}\n";
        return 0;
    } catch (const std::exception& e) {
        std::cerr << "diameter2_filter: " << e.what() << '\n';
        return 1;
    }
}
