// Exact ternary-marker prefix enumeration; one process, one thread.
#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <map>
#include <utility>
#include <vector>

int main() {
    unsigned n, m;
    if (!(std::cin >> n >> m) || n != 13 || m != 24) return 2;
    std::vector<std::pair<unsigned, unsigned>> gates(m);
    for (auto &p : gates) {
        if (!(std::cin >> p.first >> p.second) || p.first >= p.second || p.second >= n)
            return 2;
    }
    struct Entry { unsigned deleted, witness; };
    std::map<unsigned, Entry> maxima;
    unsigned inputs = 1;
    for (unsigned i = 0; i < n; ++i) inputs *= 3;
    unsigned considered = 0;
    for (unsigned code = 0; code < inputs; ++code) {
        unsigned rest = code, high = 0;
        std::array<unsigned char, 13> row{};
        for (unsigned i = 0; i < n; ++i) {
            row[i] = rest % 3;
            rest /= 3;
            high += row[i] == 2;
        }
        if (high < 2) continue;
        ++considered;
        unsigned deleted = 0;
        for (const auto &p : gates) {
            deleted += row[p.first] != 1 || row[p.second] != 1;
            if (row[p.first] > row[p.second]) std::swap(row[p.first], row[p.second]);
        }
        if (row[11] != 2 || row[12] != 2) return 3;
        unsigned x = 0, y = 0;
        for (unsigned i = 0; i < 11; ++i) {
            x |= (row[i] == 2) << i;
            y |= (row[i] != 0) << i;
        }
        const unsigned key = x | (y << 11);
        const auto it = maxima.find(key);
        if (it == maxima.end() || it->second.deleted < deleted)
            maxima[key] = Entry{deleted, code};
    }
    std::cout << "# inputs " << considered << " states " << maxima.size() << '\n';
    for (const auto &kv : maxima)
        std::cout << (kv.first & 2047) << ' ' << (kv.first >> 11) << ' '
                  << kv.second.deleted << ' ' << kv.second.witness << '\n';
}
