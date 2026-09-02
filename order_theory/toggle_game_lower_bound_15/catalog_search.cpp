#include <algorithm>
#include <cctype>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <queue>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

using std::uint16_t;

static std::vector<std::pair<int, int>> parse_edges(const std::string& line) {
    std::vector<std::pair<int, int>> edges;
    std::size_t pos = 0;
    while ((pos = line.find('[', pos)) != std::string::npos) {
        ++pos;
        if (pos >= line.size() || !std::isdigit(static_cast<unsigned char>(line[pos]))) {
            continue;
        }
        int a = 0;
        while (pos < line.size() && std::isdigit(static_cast<unsigned char>(line[pos]))) {
            a = 10 * a + (line[pos++] - '0');
        }
        if (pos >= line.size() || line[pos++] != ',') throw std::runtime_error("missing comma");
        int b = 0;
        if (pos >= line.size() || !std::isdigit(static_cast<unsigned char>(line[pos]))) {
            throw std::runtime_error("malformed second endpoint");
        }
        while (pos < line.size() && std::isdigit(static_cast<unsigned char>(line[pos]))) {
            b = 10 * b + (line[pos++] - '0');
        }
        if (pos >= line.size() || line[pos++] != ']') throw std::runtime_error("missing bracket");
        edges.emplace_back(a, b);
    }
    if (edges.empty()) throw std::runtime_error("empty edge list");
    return edges;
}

static bool is_winnable(int n, int top, const std::vector<std::pair<int, int>>& edges,
                        std::uint64_t& reached) {
    if (n < 2 || n > 15) throw std::runtime_error("supported order is 2..15");
    bool leq[15][15] = {};
    for (int i = 0; i < n; ++i) leq[i][i] = true;
    for (auto [a, b] : edges) {
        if (a < 0 || a >= n || b < 0 || b >= n || a == b) {
            throw std::runtime_error("endpoint outside lattice");
        }
        leq[a][b] = true;
    }
    for (int k = 0; k < n; ++k)
        for (int i = 0; i < n; ++i)
            for (int j = 0; j < n; ++j)
                leq[i][j] = leq[i][j] || (leq[i][k] && leq[k][j]);
    for (int i = 0; i < n; ++i) {
        if (!leq[i][top]) throw std::runtime_error("catalogue top label is not top");
    }
    int mu[15] = {};
    bool done[15] = {};
    mu[top] = 1;
    done[top] = true;
    auto compute_mu = [&](auto&& self, int i) -> int {
        if (done[i]) return mu[i];
        int sum = 0;
        for (int j = 0; j < n; ++j) {
            if (i != j && leq[i][j]) sum += self(self, j);
        }
        mu[i] = -sum;
        done[i] = true;
        return mu[i];
    };
    std::vector<uint16_t> moves;
    for (int i = 0; i < n; ++i) {
        compute_mu(compute_mu, i);
        if (i == top || mu[i] == 0) continue;
        uint16_t ideal = 0;
        for (int j = 0; j < n; ++j) if (leq[j][i]) ideal |= uint16_t(1U << j);
        moves.push_back(ideal);
    }
    const uint16_t goal = uint16_t(((1U << n) - 1U) ^ (1U << top));
    std::vector<unsigned char> seen(std::size_t(1U << n), 0);
    std::queue<uint16_t> queue;
    seen[0] = 1;
    queue.push(0);
    reached = 1;
    while (!queue.empty()) {
        uint16_t state = queue.front();
        queue.pop();
        if (state == goal) return true;
        for (uint16_t ideal : moves) {
            const uint16_t on = state & ideal;
            if (on != 0 && on != ideal) continue;
            const uint16_t next = state ^ ideal;
            if (!seen[next]) {
                seen[next] = 1;
                queue.push(next);
                ++reached;
            }
        }
    }
    return false;
}

int main(int argc, char** argv) {
    if (argc != 3 && argc != 4) {
        std::cerr << "usage: catalog_search ORDER CATALOG [cats]\n";
        return 2;
    }
    const int n = std::stoi(argv[1]);
    const bool cats = argc == 4 && std::string(argv[3]) == "cats";
    std::ifstream input(argv[2]);
    if (!input) {
        std::cerr << "cannot open " << argv[2] << "\n";
        return 2;
    }
    std::uint64_t total = 0, wins = 0, max_reached = 0;
    std::string line;
    while (std::getline(input, line)) {
        if (line.empty()) continue;
        ++total;
        std::vector<std::pair<int, int>> edges;
        int top = 1;
        if (cats) {
            top = 0;
            const std::size_t expected = std::size_t(n * (n - 1) / 2);
            if (line.size() != expected) throw std::runtime_error("wrong cats line length");
            for (int b = 2; b <= n; ++b) {
                for (int a = 1; a < b; ++a) {
                    const std::size_t pos = std::size_t((b - 1) * (b - 2) / 2 + a - 1);
                    if (line[pos] == '1') edges.emplace_back(b - 1, a - 1);
                    else if (line[pos] != '.') throw std::runtime_error("bad cats character");
                }
            }
        } else {
            edges = parse_edges(line);
        }
        std::uint64_t reached = 0;
        if (is_winnable(n, top, edges, reached)) {
            ++wins;
        } else {
            std::cout << "UNWINNABLE order=" << n << " index=" << total
                      << " reached=" << reached << "\n" << line << "\n";
            return 1;
        }
        max_reached = std::max(max_reached, reached);
    }
    std::cout << "PASS order=" << n << " total=" << total << " winnable=" << wins
              << " max_states_before_goal=" << max_reached << "\n";
    return 0;
}
