// Independent DSATUR decision check for the E457 terminal-colour relation.
//
// This deliberately does not use the reviewed checker's minimum-domain copy
// recursion or singleton queue.  It assigns one maximum-saturation vertex at
// a time and maintains neighbour colour masks with an explicit undo trail.
#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

namespace {

using Mask = std::uint8_t;

unsigned popcount(Mask value) {
    unsigned answer = 0;
    while (value != 0) {
        value = static_cast<Mask>(value & static_cast<Mask>(value - 1));
        ++answer;
    }
    return answer;
}

Mask low_bit(Mask value) {
    return static_cast<Mask>(value & static_cast<Mask>(~value + 1));
}

struct Solver {
    int n;
    std::vector<std::vector<int>> adjacency;
    std::vector<int> colour;
    std::vector<Mask> forbidden;
    std::vector<int> solution;
    std::uint64_t nodes = 0;
    std::uint64_t conflicts = 0;
    int maximum_depth = 0;

    void increment(std::uint64_t& value) {
        if (value == std::numeric_limits<std::uint64_t>::max()) {
            throw std::runtime_error("counter overflow");
        }
        ++value;
    }

    bool search(int assigned, Mask used_colours) {
        increment(nodes);
        maximum_depth = std::max(maximum_depth, assigned);
        if (assigned == n) {
            solution = colour;
            return true;
        }

        int chosen = -1;
        std::array<int, 4> best = {-1, -1, -1, 0};
        for (int vertex = 0; vertex < n; ++vertex) {
            if (colour[vertex] >= 0) {
                continue;
            }
            if (forbidden[vertex] == Mask{15}) {
                increment(conflicts);
                return false;
            }
            int uncoloured_degree = 0;
            for (int neighbour : adjacency[vertex]) {
                uncoloured_degree += colour[neighbour] < 0;
            }
            std::array<int, 4> score = {
                static_cast<int>(popcount(forbidden[vertex])),
                uncoloured_degree,
                static_cast<int>(adjacency[vertex].size()),
                -vertex
            };
            if (chosen < 0 || score > best) {
                chosen = vertex;
                best = score;
            }
        }
        if (chosen < 0) {
            throw std::runtime_error("assignment census mismatch");
        }

        Mask available = static_cast<Mask>(Mask{15} & ~forbidden[chosen]);
        Mask candidates = static_cast<Mask>(available & used_colours);
        Mask unused = static_cast<Mask>(available & ~used_colours & Mask{15});
        if (unused != 0) {
            // Globally unused colour names are interchangeable.
            candidates = static_cast<Mask>(candidates | low_bit(unused));
        }

        while (candidates != 0) {
            Mask bit = low_bit(candidates);
            candidates = static_cast<Mask>(candidates & ~bit);
            int selected_colour = 0;
            while ((Mask{1} << selected_colour) != bit) {
                ++selected_colour;
            }
            std::vector<std::pair<int, Mask>> changed;
            std::vector<int> newly_assigned;
            std::vector<std::pair<int, int>> pending{{chosen, selected_colour}};
            Mask branch_used = used_colours;
            bool immediate_conflict = false;
            while (!pending.empty() && !immediate_conflict) {
                auto [vertex, forced_colour] = pending.back();
                pending.pop_back();
                if (colour[vertex] >= 0) {
                    immediate_conflict = colour[vertex] != forced_colour;
                    continue;
                }
                Mask forced_bit = static_cast<Mask>(Mask{1} << forced_colour);
                if ((forbidden[vertex] & forced_bit) != 0) {
                    immediate_conflict = true;
                    continue;
                }
                colour[vertex] = forced_colour;
                newly_assigned.push_back(vertex);
                branch_used = static_cast<Mask>(branch_used | forced_bit);
                for (int neighbour : adjacency[vertex]) {
                    if (colour[neighbour] == forced_colour) {
                        immediate_conflict = true;
                        break;
                    }
                    if (colour[neighbour] < 0 &&
                        (forbidden[neighbour] & forced_bit) == 0) {
                        changed.emplace_back(neighbour, forbidden[neighbour]);
                        forbidden[neighbour] =
                            static_cast<Mask>(forbidden[neighbour] | forced_bit);
                        Mask remaining =
                            static_cast<Mask>(Mask{15} & ~forbidden[neighbour]);
                        if (remaining == 0) {
                            immediate_conflict = true;
                            break;
                        }
                        if ((remaining & static_cast<Mask>(remaining - 1)) == 0) {
                            int only_colour = 0;
                            while ((Mask{1} << only_colour) != remaining) {
                                ++only_colour;
                            }
                            pending.emplace_back(neighbour, only_colour);
                        }
                    }
                }
            }
            if (immediate_conflict) {
                increment(conflicts);
            } else if (search(assigned + static_cast<int>(newly_assigned.size()), branch_used)) {
                return true;
            }
            for (auto it = changed.rbegin(); it != changed.rend(); ++it) {
                forbidden[it->first] = it->second;
            }
            for (int vertex : newly_assigned) {
                colour[vertex] = -1;
            }
        }
        return false;
    }

    bool pin(int vertex, int selected_colour) {
        if (colour[vertex] >= 0) {
            return colour[vertex] == selected_colour;
        }
        Mask bit = static_cast<Mask>(Mask{1} << selected_colour);
        if ((forbidden[vertex] & bit) != 0) {
            return false;
        }
        colour[vertex] = selected_colour;
        for (int neighbour : adjacency[vertex]) {
            if (colour[neighbour] == selected_colour) {
                return false;
            }
            if (colour[neighbour] < 0) {
                forbidden[neighbour] = static_cast<Mask>(forbidden[neighbour] | bit);
            }
        }
        return true;
    }
};

}  // namespace

int main() {
    try {
        int n = 0;
        int m = 0;
        if (!(std::cin >> n >> m) || n < 0 || n > 4096 || m < 0 ||
            static_cast<long long>(m) > static_cast<long long>(n) * (n - 1) / 2) {
            throw std::runtime_error("bad dimensions");
        }
        Solver solver{n, std::vector<std::vector<int>>(n),
                      std::vector<int>(n, -1), std::vector<Mask>(n, 0), {}};
        for (int edge = 0; edge < m; ++edge) {
            int first = 0;
            int second = 0;
            if (!(std::cin >> first >> second) || first < 0 || second < 0 ||
                first >= n || second >= n || first == second) {
                throw std::runtime_error("bad edge");
            }
            solver.adjacency[first].push_back(second);
            solver.adjacency[second].push_back(first);
        }
        for (auto& neighbours : solver.adjacency) {
            std::sort(neighbours.begin(), neighbours.end());
            if (std::adjacent_find(neighbours.begin(), neighbours.end()) != neighbours.end()) {
                throw std::runtime_error("duplicate edge");
            }
        }

        int pin_count = 0;
        if (!(std::cin >> pin_count) || pin_count < 0 || pin_count > n) {
            throw std::runtime_error("bad pin count");
        }
        int assigned = 0;
        Mask used = 0;
        bool consistent = true;
        for (int index = 0; index < pin_count; ++index) {
            int vertex = 0;
            int selected_colour = 0;
            if (!(std::cin >> vertex >> selected_colour) || vertex < 0 || vertex >= n ||
                selected_colour < 0 || selected_colour >= 4 || solver.colour[vertex] >= 0) {
                throw std::runtime_error("bad pin");
            }
            consistent &= solver.pin(vertex, selected_colour);
            ++assigned;
            used = static_cast<Mask>(used | static_cast<Mask>(Mask{1} << selected_colour));
        }
        std::string trailing;
        if (std::cin >> trailing) {
            throw std::runtime_error("trailing input");
        }

        bool satisfiable = consistent && solver.search(assigned, used);
        std::cout << "{\"satisfiable\":" << (satisfiable ? "true" : "false")
                  << ",\"nodes\":" << solver.nodes
                  << ",\"conflicts\":" << solver.conflicts
                  << ",\"maximum_depth\":" << solver.maximum_depth
                  << ",\"colouring\":[";
        if (satisfiable) {
            for (int vertex = 0; vertex < n; ++vertex) {
                if (vertex != 0) {
                    std::cout << ',';
                }
                std::cout << solver.solution[vertex];
            }
        }
        std::cout << "]}\n";
        return 0;
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 2;
    }
}
