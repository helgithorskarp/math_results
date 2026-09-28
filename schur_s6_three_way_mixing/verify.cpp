#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <functional>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <string>
#include <vector>

// Literal list-colouring of the integer Schur hypergraph. No SAT library,
// CNF, learned clauses, symmetry assumption, or search cutoff is used.
using Mask = unsigned int;
struct Edge { std::array<int, 3> v{}; int size = 0; };

bool single(Mask x) { return x != 0U && (x & (x - 1U)) == 0U; }

std::vector<Edge> integer_edges(int n) {
    std::vector<Edge> edges;
    for (int x = 1; x <= n; ++x) {
        for (int y = x; x + y <= n; ++y) {
            Edge e;
            if (x == y) { e.v = {x - 1, x + y - 1, 0}; e.size = 2; }
            else { e.v = {x - 1, y - 1, x + y - 1}; e.size = 3; }
            edges.push_back(e);
        }
    }
    return edges;
}

struct Solver {
    int n;
    std::vector<Edge> edges;
    std::vector<std::vector<int>> incident;
    std::vector<int> weight;
    std::uint64_t nodes = 0;
    std::vector<Mask> model;

    Solver(const std::vector<Mask>& domains, const std::vector<Edge>& all)
        : n(static_cast<int>(domains.size())), incident(domains.size()), weight(domains.size(), 0) {
        for (const Edge& e : all) {
            Mask common = 63U;
            int free_vertices = 0;
            for (int j = 0; j < e.size; ++j) {
                common &= domains[static_cast<std::size_t>(e.v[j])];
                free_vertices += !single(domains[static_cast<std::size_t>(e.v[j])]);
            }
            // Empty intersection can never become monochromatic after restriction.
            if (common == 0U) continue;
            const int index = static_cast<int>(edges.size());
            edges.push_back(e);
            for (int j = 0; j < e.size; ++j) {
                const auto v = static_cast<std::size_t>(e.v[j]);
                incident[v].push_back(index);
                weight[v] += (free_vertices <= 2 ? 2 : 1);
            }
        }
    }

    bool search(std::vector<Mask> domains, std::vector<int> pending) {
        if (nodes == std::numeric_limits<std::uint64_t>::max())
            throw std::overflow_error("search node counter overflow");
        ++nodes;
        while (!pending.empty()) {
            const int v = pending.back(); pending.pop_back();
            const Mask colour = domains[static_cast<std::size_t>(v)];
            if (!single(colour)) throw std::logic_error("non-singleton pending domain");
            for (int ei : incident[static_cast<std::size_t>(v)]) {
                const Edge& e = edges[static_cast<std::size_t>(ei)];
                bool safe = false;
                int undecided = 0, last = -1;
                for (int j = 0; j < e.size; ++j) {
                    const int w = e.v[j];
                    const Mask d = domains[static_cast<std::size_t>(w)];
                    if ((d & colour) == 0U) { safe = true; break; }
                    if (d != colour) { ++undecided; last = w; }
                }
                if (safe || undecided > 1) continue;
                if (undecided == 0) return false;
                auto& d = domains[static_cast<std::size_t>(last)];
                d &= ~colour;
                if (d == 0U) return false;
                if (single(d)) pending.push_back(last);
            }
        }
        int choice = -1;
        for (int v = 0; v < n; ++v) {
            if (single(domains[static_cast<std::size_t>(v)])) continue;
            if (choice < 0 || weight[static_cast<std::size_t>(v)] > weight[static_cast<std::size_t>(choice)])
                choice = v;
        }
        if (choice < 0) {
            for (const Edge& e : edges) {
                Mask common = 63U;
                for (int j = 0; j < e.size; ++j) common &= domains[static_cast<std::size_t>(e.v[j])];
                if (common != 0U) throw std::logic_error("invalid terminal assignment");
            }
            model = std::move(domains);
            return true;
        }
        const Mask available = domains[static_cast<std::size_t>(choice)];
        for (Mask bit = 1U; bit <= 32U; bit <<= 1U) {
            if ((available & bit) == 0U) continue;
            auto next = domains;
            next[static_cast<std::size_t>(choice)] = bit;
            if (search(std::move(next), {choice})) return true;
        }
        return false;
    }

    bool solve(const std::vector<Mask>& domains) {
        std::vector<int> pending;
        for (int v = 0; v < n; ++v) {
            const Mask d = domains[static_cast<std::size_t>(v)];
            if (d == 0U || d > 63U) throw std::invalid_argument("invalid initial domain");
            if (single(d)) pending.push_back(v);
        }
        return search(domains, pending);
    }
};

void print_model(const std::vector<Mask>& model) {
    for (Mask m : model) {
        int d = 1;
        while (m > 1U) { ++d; m >>= 1U; }
        std::cout << d;
    }
}

int main(int argc, char** argv) {
    try {
        if (argc == 2 && std::string(argv[1]) == "--lists") {
            int count; if (!(std::cin >> count) || count < 0) return 2;
            for (int i = 0; i < count; ++i) {
                int n; if (!(std::cin >> n) || n < 1 || n > 537) return 2;
                std::vector<Mask> domains(static_cast<std::size_t>(n));
                for (auto& d : domains) if (!(std::cin >> d) || d == 0U || d > 63U) return 2;
                Solver solver(domains, integer_edges(n));
                const bool sat = solver.solve(domains);
                std::cout << i << ' ' << (sat ? "SAT" : "UNSAT") << ' ' << solver.nodes;
                if (sat) { std::cout << ' '; print_model(solver.model); }
                std::cout << '\n';
            }
            return 0;
        }
        if (argc != 2 && argc != 4) throw std::invalid_argument("usage: verifier word.txt [start count]");
        std::ifstream input(argv[1]); std::string word, extra;
        if (!(input >> word) || (input >> extra) || word.size() != 536U)
            throw std::invalid_argument("expected one 536-entry word");
        std::vector<Mask> fixed;
        for (char c : word) {
            if (c < '1' || c > '6') throw std::invalid_argument("invalid input colour");
            fixed.push_back(1U << static_cast<unsigned int>(c - '1'));
        }
        for (const Edge& e : integer_edges(536)) {
            Mask common = 63U;
            for (int j = 0; j < e.size; ++j) common &= fixed[static_cast<std::size_t>(e.v[j])];
            if (common != 0U) throw std::invalid_argument("input word is not sum-free");
        }
        int start = 0, count = 7830;
        if (argc == 4) { start = std::stoi(argv[2]); count = std::stoi(argv[3]); }
        if (start < 0 || count < 0 || start > 7830 || count > 7830 - start)
            throw std::invalid_argument("invalid case interval");
        const auto all = integer_edges(537);
        int index = 0;
        for (int r = 2; r <= 6; ++r) {
            std::vector<int> order;
            std::array<bool, 7> used{};
            std::function<void()> enumerate = [&]() {
                if (static_cast<int>(order.size()) < r) {
                    for (int d = 1; d <= 6; ++d) if (!used[static_cast<std::size_t>(d)]) {
                        used[static_cast<std::size_t>(d)] = true; order.push_back(d);
                        enumerate();
                        order.pop_back(); used[static_cast<std::size_t>(d)] = false;
                    }
                    return;
                }
                for (int entry = 0; entry < r - 1; ++entry, ++index) {
                    if (index < start || index >= start + count) continue;
                    std::array<int, 7> destination{};
                    for (int j = 0; j < r - 1; ++j)
                        destination[static_cast<std::size_t>(order[static_cast<std::size_t>(j)])] = order[static_cast<std::size_t>(j + 1)];
                    destination[static_cast<std::size_t>(order.back())] = order[static_cast<std::size_t>(entry)];
                    auto domains = fixed;
                    for (std::size_t v = 0; v < word.size(); ++v) {
                        const int to = destination[static_cast<std::size_t>(word[v] - '0')];
                        if (to != 0) domains[v] |= 1U << static_cast<unsigned int>(to - 1);
                    }
                    domains.push_back(1U << static_cast<unsigned int>(order.front() - 1));
                    Solver solver(domains, all);
                    const bool sat = solver.solve(domains);
                    std::cout << index << ' ';
                    for (int d : order) std::cout << d;
                    std::cout << ' ' << entry << ' ' << (sat ? "SAT" : "UNSAT")
                              << ' ' << solver.nodes << ' ' << solver.edges.size() << '\n';
                    if (sat) {
                        print_model(solver.model); std::cout << '\n';
                        throw std::runtime_error("satisfiable path-cycle case");
                    }
                }
            };
            enumerate();
        }
        if (index != 7830) throw std::logic_error("enumeration count mismatch");
    } catch (const std::exception& e) {
        std::cerr << "ERROR: " << e.what() << '\n'; return 2;
    }
}
