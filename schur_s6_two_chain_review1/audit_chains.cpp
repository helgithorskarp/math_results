// Independent exact two-chain verifier with a proved interaction cutoff.
#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

constexpr int N = 537;
constexpr int WIDTH = N + 1;
struct Edge { int x, y, z; };
struct Event { std::array<unsigned char, 7> image; int delta; };

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    std::ifstream input(argv[1]);
    std::string word;
    input >> word;
    if (word.size() != N || word.find_first_not_of("123456") != std::string::npos) return 2;
    std::array<unsigned char, WIDTH> base{};
    std::array<int, WIDTH> root{};
    for (int v = 1; v <= N; ++v) {
        base[v] = static_cast<unsigned char>(word[v - 1] - '0');
        int r = v;
        while (!(r & 1)) r /= 2;
        root[v] = r;
    }
    for (int v = 1; 2 * v <= N; ++v) if (base[v] == base[2 * v]) return 3;

    std::vector<Edge> edges;
    std::array<std::vector<int>, WIDTH> incident;
    std::vector<std::vector<int>> cross(WIDTH * WIDTH);
    auto pair_index = [](int a, int b) { return a * WIDTH + b; };
    for (int z = 2; z <= N; ++z) {
        for (int x = 1; x < z - x; ++x) {
            int y = z - x;
            int id = static_cast<int>(edges.size());
            edges.push_back({x, y, z});
            std::array<int, 3> roots{root[x], root[y], root[z]};
            std::sort(roots.begin(), roots.end());
            auto end = std::unique(roots.begin(), roots.end());
            for (auto it = roots.begin(); it != end; ++it) incident[*it].push_back(id);
            for (auto it = roots.begin(); it != end; ++it)
                for (auto jt = it + 1; jt != end; ++jt)
                    cross[pair_index(*it, *jt)].push_back(id);
        }
    }
    if (edges.size() != 71824) return 3;
    auto mono = [&](int id, int r, const Event *a, int s, const Event *b) {
        auto edge = edges[id];
        auto value = [&](int v) {
            if (a && root[v] == r) return a->image[base[v]];
            if (b && root[v] == s) return b->image[base[v]];
            return base[v];
        };
        return value(edge.x) == value(edge.y) && value(edge.y) == value(edge.z);
    };
    int original = 0;
    for (int id = 0; id < static_cast<int>(edges.size()); ++id)
        original += mono(id, 0, nullptr, 0, nullptr);
    if (original != 4) return 3;

    std::array<std::vector<Event>, WIDTH> events;
    std::uint64_t total_events = 0;
    int single_best = original;
    for (int r = 1; r <= N; r += 2) {
        std::vector<int> observed;
        std::array<bool, 7> used_colour{};
        for (int v = r; v <= N; v *= 2) used_colour[base[v]] = true;
        for (int c = 1; c <= 6; ++c) if (used_colour[c]) observed.push_back(c);
        std::array<unsigned char, 7> image{};
        for (int c = 1; c <= 6; ++c) image[c] = static_cast<unsigned char>(c);
        auto produce = [&](auto &&self, int position, int targets) -> void {
            if (position == static_cast<int>(observed.size())) {
                bool identity = true;
                for (int c : observed) if (image[c] != c) identity = false;
                if (identity) return;
                Event event{image, 0};
                for (int id : incident[r])
                    event.delta += mono(id, r, &event, 0, nullptr)
                                   - mono(id, 0, nullptr, 0, nullptr);
                events[r].push_back(event);
                return;
            }
            int c = observed[position];
            for (int target = 1; target <= 6; ++target) {
                if (targets & (1 << target)) continue;
                image[c] = static_cast<unsigned char>(target);
                self(self, position + 1, targets | (1 << target));
            }
            image[c] = static_cast<unsigned char>(c);
        };
        produce(produce, 0, 0);
        total_events += events[r].size();
        for (const auto &event : events[r])
            single_best = std::min(single_best, original + event.delta);
    }
    if (total_events != 15841 || single_best != 4) return 3;

    std::uint64_t total_pairs = 0, pruned = 0, checked = 0, direct_audits = 0;
    int best = original;
    for (int r = 1; r <= N; r += 2) {
        for (int s = r + 2; s <= N; s += 2) {
            const auto &shared = cross[pair_index(r, s)];
            int interaction_bound = 2 * static_cast<int>(shared.size());
            for (const auto &a : events[r]) {
                for (const auto &b : events[s]) {
                    ++total_pairs;
                    // Each shared triple has correction at least -2.
                    // If this bound already gives score >= 4, omit it safely.
                    if (a.delta + b.delta >= interaction_bound) {
                        ++pruned;
                        continue;
                    }
                    ++checked;
                    int score = original + a.delta + b.delta;
                    for (int id : shared) {
                        score += mono(id, r, &a, s, &b)
                                 - mono(id, r, &a, 0, nullptr)
                                 - mono(id, 0, nullptr, s, &b)
                                 + mono(id, 0, nullptr, 0, nullptr);
                    }
                    if (score < best) best = score;
                    if (score < original || checked % 10000 == 0) {
                        ++direct_audits;
                        int direct = 0;
                        for (int id = 0; id < static_cast<int>(edges.size()); ++id)
                            direct += mono(id, r, &a, s, &b);
                        if (direct != score) return 4;
                    }
                    if (score < original) {
                        std::cout << "COUNTEREXAMPLE roots=" << r << ',' << s
                                  << " score=" << score << '\n';
                        return 5;
                    }
                }
            }
        }
    }
    if (total_pairs != 123114286 || checked + pruned != total_pairs) return 3;
    std::cout << "PASS baseline=" << original << " single_best=" << single_best
              << " chain_events=" << total_events
              << " chain_pairs=" << total_pairs << " pruned=" << pruned
              << " exact_checked=" << checked << " minimum=" << best
              << " direct_audits=" << direct_audits << '\n';
}
