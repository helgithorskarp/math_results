// Independent complete physical graph reconstruction. C++17, integers only.
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

using Graph = std::vector<uint32_t>;
int pc(uint32_t x) { return __builtin_popcount(x); }
void need(bool good, const std::string &why) { if (!good) throw std::runtime_error(why); }
void edge(Graph &g, int u, int v) { g[u] |= 1u << v; g[v] |= 1u << u; }

Graph orbit_graph(uint32_t word, int cycles) {
    Graph g(3 * cycles);
    for (int u = 0; u < 3 * cycles; ++u) for (int v = u + 1; v < 3 * cycles; ++v) {
        int i = u / 3, j = v / 3, bit = i;
        if (i != j) {
            int pair = 0;
            for (int a = 0; a < i; ++a) pair += cycles - 1 - a;
            pair += j - i - 1;
            bit = cycles + 3 * pair + (v % 3 - u % 3 + 3) % 3;
        }
        if ((word >> bit) & 1u) edge(g, u, v);
    }
    return g;
}

// General literal colored page count, with no degree assumption.
int literal(const Graph &g, int u, int v) {
    bool red = (g[u] >> v) & 1u;
    int pages = 0;
    for (int w = 0; w < int(g.size()); ++w) if (w != u && w != v) {
        bool uw = (g[u] >> w) & 1u, vw = (g[v] >> w) & 1u;
        if (uw == red && vw == red) ++pages;
    }
    return pages;
}

bool general_valid(const Graph &g) {
    for (int u = 0; u < int(g.size()); ++u) for (int v = u + 1; v < int(g.size()); ++v)
        if (literal(g, u, v) > (((g[u] >> v) & 1u) ? 3 : 6)) return false;
    return true;
}

// Domain guard BEFORE the collapsed common-red predicate can be used.
void regular(const Graph &g, int degree) {
    for (int u = 0; u < int(g.size()); ++u) {
        need(!(g[u] & (1u << u)), "diagonal bit");
        need(pc(g[u]) == degree, "regularity bridge failed");
        for (int v = 0; v < int(g.size()); ++v)
            need(((g[u] >> v) & 1u) == ((g[v] >> u) & 1u), "symmetry bridge failed");
    }
}

struct Frame { uint32_t word; std::array<uint32_t, 12> columns; };

int main(int argc, char **argv) {
    try {
        need(argc == 4, "usage: complete FRAMES PRIMARY21 OUTPUT_PREFIX");
        std::ifstream frame_input(argv[1]); need(bool(frame_input), "frames unavailable");
        std::vector<Frame> frames;
        std::string line;
        while (std::getline(frame_input, line)) {
            std::istringstream in(line); Frame f{}; need(bool(in >> f.word), "bad frame word");
            for (auto &m : f.columns) need(bool(in >> m) && m < 512 && pc(m) == 4, "bad column");
            std::string extra; need(!(in >> extra), "extra frame field");
            frames.push_back(f);
        }
        need(!frames.empty(), "empty frames");
        std::ifstream primary_input(argv[2]); need(bool(primary_input), "primary unavailable");
        Graph primary;
        while (std::getline(primary_input, line)) {
            need(line.size() == 21, "primary row width");
            uint32_t mask = 0;
            for (int i = 0; i < 21; ++i) {
                need(line[i] == '0' || line[i] == '1', "bad primary bit");
                if (line[i] == '1') mask |= 1u << i;
            }
            primary.push_back(mask);
        }
        need(primary.size() == 21 && general_valid(primary), "primary positive control failed");
        std::array<int, 21> primary_red{}, primary_blue{};
        for (int u = 0; u < 21; ++u) {
            need(!(primary[u] & (1u << u)), "primary diagonal");
            for (int v = u + 1; v < 21; ++v) {
                need(((primary[u] >> v) & 1u) == ((primary[v] >> u) & 1u), "primary symmetry");
                int p = literal(primary, u, v);
                (((primary[u] >> v) & 1u) ? primary_red : primary_blue)[p]++;
            }
        }
        uint64_t controls = 0, nonregular_rejections = 0;
        for (int n : {5, 6, 8, 9, 21, 22}) for (int mode = 0; mode < 8; ++mode) {
            Graph g(n);
            for (int u = 0; u < n; ++u) for (int v = u + 1; v < n; ++v)
                if (mode == 0 || (mode > 1 && (u * 17 + v * 23 + mode * 11) % 7 < mode - 1)) edge(g, u, v);
            for (int u = 0; u < n; ++u) for (int v = u + 1; v < n; ++v) {
                bool red = (g[u] >> v) & 1u;
                int c = pc(g[u] & g[v]);
                int derived = red ? c : n - 2 - pc(g[u]) - pc(g[v]) + c;
                need(derived == literal(g, u, v), "general red/blue identity control");
                ++controls;
            }
            if (n == 22) {
                bool is_regular = true;
                for (auto row : g) if (pc(row) != 9) is_regular = false;
                if (!is_regular) {
                    try { regular(g, 9); } catch (const std::runtime_error &) { ++nonregular_rejections; continue; }
                    throw std::runtime_error("missing nonregular domain rejection");
                }
            }
            if (mode == 0 && (n == 5 || n == 6)) need(general_valid(g) == (n == 5), "red threshold control");
            if (mode == 1 && (n == 8 || n == 9)) need(general_valid(g) == (n == 8), "blue threshold control");
        }
        std::string prefix(argv[3]);
        std::ofstream words(prefix + ".kwords.txt"); need(bool(words), "output unavailable");
        std::vector<std::pair<uint32_t, Graph>> candidates;
        uint64_t degree_matches = 0, screen_spines = 0;
        for (uint32_t word = 0; word < (1u << 22); ++word) {
            std::array<int, 4> degrees{};
            for (int i = 0; i < 4; ++i) degrees[i] = ((word >> i) & 1u) * 2;
            int bit = 4;
            for (int i = 0; i < 4; ++i) for (int j = i + 1; j < 4; ++j, bit += 3) {
                int weight = pc((word >> bit) & 7u); degrees[i] += weight; degrees[j] += weight;
            }
            bool good = true; for (int d : degrees) if (d != 5) good = false;
            if (!good) continue;
            ++degree_matches;
            Graph k = orbit_graph(word, 4); regular(k, 5);
            for (int u = 0; u < 12; ++u) for (int v = u + 1; v < 12; ++v) {
                bool red = (k[u] >> v) & 1u;
                int common = pc(k[u] & k[v]);
                need(common == literal(k, u, v), "five-regular outside color identity");
                if (common > (red ? 3 : 4)) good = false;
                ++screen_spines;
            }
            if (good) { words << word << '\n'; candidates.emplace_back(word, std::move(k)); }
        }
        words.close();
        std::ofstream stream(prefix + ".valid.bin", std::ios::binary);
        uint64_t completions = 0, valid_total = 0, red_first = 0, blue_first = 0;
        std::vector<uint64_t> per_frame;
        uint64_t compared_spines = 0;
        for (const auto &f : frames) {
            uint64_t count = 0;
            Graph h = orbit_graph(f.word, 3);
            for (const auto &candidate : candidates) {
                Graph g(22);
                for (int u = 0; u < 9; ++u) {
                    g[u] = h[u]; edge(g, u, 21);
                }
                for (int b = 0; b < 12; ++b) {
                    g[9 + b] |= candidate.second[b] << 9;
                    for (int u = 0; u < 9; ++u) if ((f.columns[b] >> u) & 1u) edge(g, u, 9 + b);
                }
                regular(g, 9);
                bool good = true;
                for (int u = 0; u < 22 && good; ++u) for (int v = u + 1; v < 22; ++v) {
                    bool red = (g[u] >> v) & 1u;
                    int common = pc(g[u] & g[v]);
                    int colored_pages = literal(g, u, v);
                    need(colored_pages == (red ? common : 2 + common), "regular collapse failed");
                    need((common <= (red ? 3 : 4)) == (colored_pages <= (red ? 3 : 6)), "predicate mismatch");
                    ++compared_spines;
                    if (common > (red ? 3 : 4)) {
                        if (red) ++red_first; else ++blue_first;
                        good = false; break;
                    }
                }
                stream.put(good ? 1 : 0);
                if (good) ++count;
                ++completions;
            }
            per_frame.push_back(count); valid_total += count;
        }
        stream.close();
        std::cout << "{\"k_words_tested\":4194304,\"k_degree_matches\":" << degree_matches
                  << ",\"k_candidates\":" << candidates.size() << ",\"k_all_screen_spines\":" << screen_spines
                  << ",\"frames\":" << frames.size() << ",\"completions\":" << completions
                  << ",\"valid\":" << valid_total << ",\"pair_order_red_first\":" << red_first
                  << ",\"pair_order_blue_first\":" << blue_first
                  << ",\"literal_collapse_compared_spines\":" << compared_spines
                  << ",\"general_control_spines\":" << controls
                  << ",\"nonregular_domain_rejections\":" << nonregular_rejections << ",\"per_frame_valid\":[";
        for (size_t i = 0; i < per_frame.size(); ++i) { if (i) std::cout << ','; std::cout << per_frame[i]; }
        std::cout << "],\"primary_red_page_histogram\":{";
        bool first = true;
        for (int i = 0; i < 21; ++i) if (primary_red[i]) { if (!first) std::cout << ','; first = false; std::cout << '\"' << i << "\":" << primary_red[i]; }
        std::cout << "},\"primary_blue_page_histogram\":{"; first = true;
        for (int i = 0; i < 21; ++i) if (primary_blue[i]) { if (!first) std::cout << ','; first = false; std::cout << '\"' << i << "\":" << primary_blue[i]; }
        std::cout << "}}\n";
        return 0;
    } catch (const std::exception &e) { std::cerr << e.what() << '\n'; return 1; }
}
