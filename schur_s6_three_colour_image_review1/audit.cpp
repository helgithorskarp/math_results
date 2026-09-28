// Independent exact list-colouring audit of the 7,830 orbit cases.
#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <functional>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

using Domain = unsigned char;
struct Edge { std::array<int, 3> v; int size; };

std::vector<Edge> schur_edges(int n) {
    std::vector<Edge> result;
    for (int z = 2; z <= n; ++z)
        for (int x = 1; x <= z / 2; ++x) {
            int y = z - x;
            if (x == y) result.push_back({{x - 1, z - 1, -1}, 2});
            else result.push_back({{x - 1, y - 1, z - 1}, 3});
        }
    return result;
}

bool singleton(Domain mask) { return mask && !(mask & (mask - 1)); }

struct Solver {
    int n;
    std::vector<Edge> edges;
    std::vector<std::vector<int>> incident;
    std::uint64_t nodes = 0;

    Solver(const std::vector<Domain>& initial, const std::vector<Edge>& all)
        : n(static_cast<int>(initial.size())), incident(initial.size()) {
        for (const Edge &e : all) {
            Domain common = 63;
            for (int j = 0; j < e.size; ++j) common &= initial[e.v[j]];
            if (!common) continue;
            int id = static_cast<int>(edges.size());
            edges.push_back(e);
            for (int j = 0; j < e.size; ++j) incident[e.v[j]].push_back(id);
        }
    }

    bool dfs(std::vector<Domain> domain, std::vector<int> pending) {
        ++nodes;
        while (!pending.empty()) {
            int v = pending.back();
            pending.pop_back();
            Domain bit = domain[v];
            if (!singleton(bit)) throw std::runtime_error("bad propagation queue");
            for (int id : incident[v]) {
                const Edge &e = edges[id];
                bool already_safe = false;
                int free_count = 0, last = -1;
                for (int j = 0; j < e.size; ++j) {
                    int w = e.v[j];
                    if (!(domain[w] & bit)) { already_safe = true; break; }
                    if (domain[w] != bit) { ++free_count; last = w; }
                }
                if (already_safe || free_count > 1) continue;
                if (free_count == 0) return false;
                domain[last] = static_cast<Domain>(domain[last] & ~bit);
                if (!domain[last]) return false;
                if (singleton(domain[last])) pending.push_back(last);
            }
        }

        int choice = -1;
        for (int v = 0; v < n; ++v) {
            if (singleton(domain[v])) continue;
            if (choice < 0 ||
                __builtin_popcount(domain[v]) < __builtin_popcount(domain[choice]) ||
                (__builtin_popcount(domain[v]) == __builtin_popcount(domain[choice]) &&
                 (incident[v].size() > incident[choice].size() ||
                  (incident[v].size() == incident[choice].size() && v > choice))))
                choice = v;
        }
        if (choice < 0) {
            for (const Edge &e : edges) {
                Domain common = 63;
                for (int j = 0; j < e.size; ++j) common &= domain[e.v[j]];
                if (common) throw std::runtime_error("invalid terminal model");
            }
            return true;
        }
        Domain available = domain[choice];
        for (Domain bit = 1; bit <= 32; bit <<= 1) {
            if (!(available & bit)) continue;
            auto branch = domain;
            branch[choice] = bit;
            if (dfs(std::move(branch), {choice})) return true;
        }
        return false;
    }

    bool solve(const std::vector<Domain>& initial) {
        std::vector<int> pending;
        for (int v = 0; v < n; ++v) {
            if (!initial[v] || initial[v] > 63) throw std::runtime_error("invalid domain");
            if (singleton(initial[v])) pending.push_back(v);
        }
        return dfs(initial, pending);
    }
};

bool brute(const std::vector<Domain>& domains, const std::vector<Edge>& edges) {
    std::vector<Domain> fixed(domains.size());
    auto rec = [&](auto &&self, int v) -> bool {
        if (v == static_cast<int>(domains.size())) {
            for (const Edge &e : edges) {
                Domain common = 7;
                for (int j = 0; j < e.size; ++j) common &= fixed[e.v[j]];
                if (common) return false;
            }
            return true;
        }
        for (Domain bit = 1; bit <= 4; bit <<= 1) if (domains[v] & bit) {
            fixed[v] = bit;
            if (self(self, v + 1)) return true;
        }
        return false;
    };
    return rec(rec, 0);
}

int main(int argc, char **argv) {
    try {
        if (argc != 2) return 2;
        std::uint64_t toy_sat = 0, toy_unsat = 0;
        for (int n = 1; n <= 5; ++n) {
            const auto edges = schur_edges(n);
            std::vector<Domain> domains(n);
            auto test = [&](auto &&self, int v) -> void {
                if (v < n) {
                    for (Domain mask = 1; mask <= 7; ++mask) {
                        domains[v] = mask;
                        self(self, v + 1);
                    }
                    return;
                }
                Solver solver(domains, edges);
                bool answer = solver.solve(domains);
                if (answer != brute(domains, edges))
                    throw std::runtime_error("small exhaustive oracle disagreement");
                if (answer) ++toy_sat;
                else ++toy_unsat;
            };
            test(test, 0);
        }
        if (toy_sat != 16058 || toy_unsat != 3549) return 3;

        std::ifstream file(argv[1]);
        std::string word;
        file >> word;
        if (word.size() != 536 || word.find_first_not_of("123456") != std::string::npos)
            return 2;
        std::vector<int> old(536);
        for (int i = 0; i < 536; ++i) old[i] = word[i] - '0';
        const auto old_edges = schur_edges(536);
        const auto all = schur_edges(537);
        if (all.size() != 72092) return 3;
        for (const Edge &e : old_edges) {
            int c = old[e.v[0]];
            bool bad = true;
            for (int j = 1; j < e.size; ++j) bad &= old[e.v[j]] == c;
            if (bad) return 3;
        }

        std::array<std::uint64_t, 7> cases{}, nodes{}, maxima{};
        for (int length = 2; length <= 6; ++length) {
            std::vector<int> order;
            std::array<bool, 7> used{};
            auto generate = [&](auto &&self) -> void {
                if (static_cast<int>(order.size()) < length) {
                    for (int c = 1; c <= 6; ++c) if (!used[c]) {
                        used[c] = true;
                        order.push_back(c);
                        self(self);
                        order.pop_back();
                        used[c] = false;
                    }
                    return;
                }
                for (int entry = 0; entry < length - 1; ++entry) {
                    std::array<int, 7> destination{};
                    for (int j = 0; j < length - 1; ++j)
                        destination[order[j]] = order[j + 1];
                    destination[order.back()] = order[entry];
                    std::vector<Domain> domains(537);
                    for (int v = 0; v < 536; ++v) {
                        domains[v] = static_cast<Domain>(1 << (old[v] - 1));
                        int to = destination[old[v]];
                        if (to) domains[v] |= static_cast<Domain>(1 << (to - 1));
                    }
                    domains[536] = static_cast<Domain>(1 << (order.front() - 1));
                    Solver solver(domains, all);
                    if (solver.solve(domains)) {
                        std::cerr << "SAT orbit:";
                        for (int c : order) std::cerr << ' ' << c;
                        std::cerr << " entry=" << entry << '\n';
                        throw std::runtime_error("counterexample to target");
                    }
                    ++cases[length];
                    nodes[length] += solver.nodes;
                    maxima[length] = std::max(maxima[length], solver.nodes);
                }
            };
            generate(generate);
        }
        const std::array<std::uint64_t, 7> expected{0, 0, 30, 240, 1080, 2880, 3600};
        if (cases != expected) return 3;
        std::uint64_t total_nodes = 0, largest = 0;
        for (int r = 2; r <= 6; ++r) {
            total_nodes += nodes[r];
            largest = std::max(largest, maxima[r]);
        }
        std::cout << "PASS cases=7830 toy_sat=" << toy_sat
                  << " toy_unsat=" << toy_unsat
                  << " independent_nodes=" << total_nodes
                  << " largest=" << largest << '\n';
        for (int r = 2; r <= 6; ++r)
            std::cout << "length=" << r << " cases=" << cases[r]
                      << " nodes=" << nodes[r] << " largest=" << maxima[r] << '\n';
    } catch (const std::exception &e) {
        std::cerr << e.what() << '\n';
        return 4;
    }
}
