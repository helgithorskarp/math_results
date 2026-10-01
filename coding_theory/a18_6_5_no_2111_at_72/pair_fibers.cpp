// Exact two-star compatibility in seven-point mapping fibers.
// Pruned mode tests forbidden mapped triples; literal mode enumerates all
// 7! bijections and compares full quadruple intersections directly.
#include <algorithm>
#include <array>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <iostream>
#include <set>
#include <stdexcept>
#include <string>
#include <vector>

using Clock = std::chrono::steady_clock;
using Mask = std::uint32_t;
constexpr std::array<int, 8> FACT = {1, 1, 2, 6, 24, 120, 720, 5040};

struct Fiber {
    int index;
    std::array<Mask, 17> first{}, second{};
    std::array<int, 16> fixed{};
};

void validate_words(const std::array<Mask, 17>& words) {
    std::set<Mask> unique(words.begin(), words.end());
    std::array<std::array<bool, 16>, 16> pairs{};
    if (unique.size() != 17) throw std::runtime_error("repeated input word");
    for (Mask w : words) {
        if (w >= (1U << 16) || __builtin_popcount(w) != 4)
            throw std::runtime_error("invalid input word");
        for (int u=0; u<16; ++u) if (w & (1U << u))
            for (int v=u+1; v<16; ++v) if (w & (1U << v)) {
                if (pairs[u][v]) throw std::runtime_error("input pair repeated");
                pairs[u][v] = true;
            }
    }
}

class Search {
    const Fiber& fiber;
    std::uint64_t cap;
    double seconds;
    Clock::time_point started;
    std::array<int, 16> image;
    std::vector<int> source_free, target_free;
    std::array<bool, 16> used{};
    std::array<Mask, 17> partial{};
    std::array<std::vector<int>, 16> through;
    std::array<bool, 65536> bad{};
public:
    std::uint64_t nodes = 0;
    std::vector<int> accepted;
    Search(const Fiber& f, std::uint64_t limit, double duration)
        : fiber(f), cap(limit), seconds(duration), started(Clock::now()), image(f.fixed) {
        for (int u=0; u<16; ++u) {
            if (image[u] == -1) source_free.push_back(u);
            else if (image[u] < 0 || image[u] >= 16 || used[image[u]])
                throw std::runtime_error("invalid fixed point map");
            else used[image[u]] = true;
        }
        for (int v=0; v<16; ++v) if (!used[v]) target_free.push_back(v);
        if (source_free.size() != 7 || target_free.size() != 7)
            throw std::runtime_error("exactly nine fixed and seven free points required");
        for (int w=0; w<17; ++w) {
            for (int u=0; u<16; ++u) if (fiber.second[w] & (1U << u)) {
                through[u].push_back(w);
                if (image[u] != -1) partial[w] |= (1U << image[u]);
            }
        }
    }
    double elapsed() const {
        return std::chrono::duration<double>(Clock::now()-started).count();
    }
    void guard() const {
        if (nodes > cap || elapsed() > seconds)
            throw std::runtime_error("INCOMPLETE mapping fiber node/time guard");
    }
    int rank() const {
        int result = 0;
        for (int i=0; i<7; ++i) {
            int smaller = 0;
            for (int j=i+1; j<7; ++j)
                if (image[source_free[j]] < image[source_free[i]]) ++smaller;
            result += smaller * FACT[6-i];
        }
        return result;
    }
    void descend(int depth) {
        ++nodes;
        if ((nodes & 127U) == 0 || nodes > cap) guard();
        if (depth == 7) { accepted.push_back(rank()); return; }
        const int u = source_free[depth];
        for (int v : target_free) if (!used[v]) {
            const Mask bit = 1U << v;
            bool allowed = true;
            for (int w : through[u]) if (bad[partial[w] | bit]) { allowed = false; break; }
            if (!allowed) continue;
            image[u] = v;
            used[v] = true;
            for (int w : through[u]) partial[w] |= bit;
            descend(depth+1);
            for (int w : through[u]) partial[w] ^= bit;
            used[v] = false;
            image[u] = -1;
        }
    }
    void pruned() {
        for (Mask w : fiber.first)
            for (int u=0; u<16; ++u) if (w & (1U << u))
                for (int v=u+1; v<16; ++v) if (w & (1U << v))
                    for (int z=v+1; z<16; ++z) if (w & (1U << z)) {
                        const Mask triple = (1U << u) | (1U << v) | (1U << z);
                        bad[triple] = true;
                        for (int q=0; q<16; ++q) bad[triple | (1U << q)] = true;
                    }
        bool allowed = true;
        for (Mask w : partial) if (bad[w]) allowed = false;
        if (allowed) descend(0); else nodes = 1;
        guard();
        std::sort(accepted.begin(), accepted.end());
    }
    void literal() {
        auto permutation = target_free;
        int ordinal = 0;
        do {
            ++nodes;
            if ((nodes & 127U) == 0 || nodes > cap) guard();
            for (int u=0; u<7; ++u) image[source_free[u]] = permutation[u];
            bool allowed = true;
            for (Mask w : fiber.second) {
                Mask mapped = 0;
                for (int u=0; u<16; ++u) if (w & (1U << u)) mapped |= (1U << image[u]);
                for (Mask old : fiber.first) if (__builtin_popcount(mapped & old) >= 3) {
                    allowed = false; break;
                }
                if (!allowed) break;
            }
            if (allowed) accepted.push_back(ordinal);
            ++ordinal;
        } while (std::next_permutation(permutation.begin(), permutation.end()));
        if (ordinal != 5040 || nodes != 5040) throw std::runtime_error("literal domain differs");
        guard();
    }
};

int main(int argc, char** argv) {
    try {
        if (argc != 6) throw std::runtime_error("usage: mode start end nodes seconds < matrix");
        const std::string mode = argv[1];
        const int begin = std::stoi(argv[2]), end = std::stoi(argv[3]);
        const auto cap = std::stoull(argv[4]);
        const double seconds = std::stod(argv[5]);
        if ((mode != "prune" && mode != "literal") || cap == 0 || cap > 200000
                || !std::isfinite(seconds) || seconds <= 0 || seconds > 10)
            throw std::runtime_error("invalid mode or guard; maximum200000 nodes/ten seconds");
        std::string magic;
        int count = 0;
        if (!(std::cin >> magic >> count) || magic != "PAIR2111_V1" || count < 1 || count > 10000
                || begin < 0 || end < begin || end > count)
            throw std::runtime_error("invalid mapping matrix header/range");
        for (int index=0; index<count; ++index) {
            Fiber f{};
            if (!(std::cin >> f.index) || f.index != index) throw std::runtime_error("invalid fiber index");
            for (Mask& w : f.first) if (!(std::cin >> w)) throw std::runtime_error("truncated first star");
            for (Mask& w : f.second) if (!(std::cin >> w)) throw std::runtime_error("truncated second star");
            for (int& v : f.fixed) if (!(std::cin >> v)) throw std::runtime_error("truncated point map");
            validate_words(f.first);
            validate_words(f.second);
            Search search(f, cap, seconds);
            if (index < begin || index >= end) continue;
            try {
                if (mode == "prune") search.pruned(); else search.literal();
                std::cout << "{\"index\":" << index << ",\"status\":\"COMPLETE\",\"nodes\":"
                          << search.nodes << ",\"seconds\":" << search.elapsed() << ",\"accepted\":[";
                for (std::size_t i=0; i<search.accepted.size(); ++i) {
                    if (i) std::cout << ',';
                    std::cout << search.accepted[i];
                }
                std::cout << "]}\n" << std::flush;
            } catch (const std::runtime_error& e) {
                std::cout << "{\"index\":" << index << ",\"status\":\"INCOMPLETE\",\"nodes\":"
                          << search.nodes << "}\n" << std::flush;
                throw;
            }
        }
        std::string trailing;
        if (std::cin >> trailing) throw std::runtime_error("trailing mapping matrix input");
        return 0;
    } catch (const std::exception& e) {
        std::cerr << e.what() << '\n';
        return 2;
    }
}
