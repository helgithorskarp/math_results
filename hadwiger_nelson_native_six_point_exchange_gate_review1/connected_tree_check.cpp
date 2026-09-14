#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <vector>

// Clean-room connected-six checker.  It deliberately performs no tree
// automorphism quotienting: every injective embedding of each of the six
// unlabelled six-vertex tree shapes is visited.  Thus its search partition is
// different from both enumerators in the result under review.

using Mask = std::array<std::uint64_t, 2>;

int vertex_count;
Mask complete_mask;
std::vector<int> free_vertices;
std::vector<int> base_degree;
std::vector<std::vector<int>> adjacency;
std::vector<std::uint8_t> edge;
std::vector<Mask> omission_mask;
std::array<int, 6> selected{};
std::array<int, 6> parent{};
std::uint64_t leaf_visits;
std::uint64_t qualified;
std::uint64_t uncovered;

bool linked(int first, int second) {
    return edge[static_cast<std::size_t>(first) * vertex_count + second] != 0;
}

void search(int depth, Mask accumulated) {
    if (depth == 6) {
        ++leaf_visits;
        for (int v : selected) {
            int degree = base_degree[v];
            for (int u : selected) {
                degree += linked(v, u) ? 1 : 0;
            }
            if (degree < 4) {
                return;
            }
        }
        ++qualified;
        if (accumulated == complete_mask) {
            ++uncovered;
            if (uncovered == 1) {
                std::cerr << "first uncovered mapping";
                for (int v : selected) {
                    std::cerr << ' ' << v;
                }
                std::cerr << '\n';
            }
        }
        return;
    }

    for (int candidate : adjacency[selected[parent[depth]]]) {
        bool used = false;
        for (int index = 0; index < depth; ++index) {
            used = used || selected[index] == candidate;
        }
        if (used) {
            continue;
        }
        selected[depth] = candidate;

        // Any future vertex can add at most one neighbour to each vertex
        // already selected.  This upper bound only prunes prefixes that cannot
        // reach minimum degree four in the final B-plus-six graph.
        bool viable = true;
        for (int index = 0; index <= depth; ++index) {
            int degree = base_degree[selected[index]];
            for (int other = 0; other <= depth; ++other) {
                degree += linked(selected[index], selected[other]) ? 1 : 0;
            }
            if (degree + (5 - depth) < 4) {
                viable = false;
                break;
            }
        }
        if (viable) {
            search(depth + 1,
                   {accumulated[0] | omission_mask[candidate][0],
                    accumulated[1] | omission_mask[candidate][1]});
        }
    }
}

int main(int argc, char** argv) {
    if (argc != 2) {
        return 2;
    }
    std::ifstream input(argv[1]);
    int free_count;
    int width;
    input >> vertex_count >> free_count >> width;
    if (!input || vertex_count < 1 || vertex_count > 10000 ||
        free_count < 1 || width < 1 || width > 128) {
        return 3;
    }
    complete_mask = {
        width >= 64 ? ~std::uint64_t(0) : (std::uint64_t(1) << width) - 1,
        width <= 64 ? 0
                    : (width == 128 ? ~std::uint64_t(0)
                                    : (std::uint64_t(1) << (width - 64)) - 1),
    };
    base_degree.assign(vertex_count, 0);
    adjacency.resize(vertex_count);
    omission_mask.resize(vertex_count);
    edge.assign(static_cast<std::size_t>(vertex_count) * vertex_count, 0);
    for (int row = 0; row < free_count; ++row) {
        int vertex;
        int degree;
        std::uint64_t low;
        std::uint64_t high;
        int neighbours;
        input >> vertex >> degree >> low >> high >> neighbours;
        if (!input || vertex < 0 || vertex >= vertex_count ||
            neighbours < 0 || neighbours >= vertex_count) {
            return 4;
        }
        free_vertices.push_back(vertex);
        base_degree[vertex] = degree;
        omission_mask[vertex] = {low, high};
        for (int index = 0; index < neighbours; ++index) {
            int other;
            input >> other;
            if (!input || other < 0 || other >= vertex_count) {
                return 5;
            }
            adjacency[vertex].push_back(other);
            edge[static_cast<std::size_t>(vertex) * vertex_count + other] = 1;
        }
    }

    const std::array<std::array<int, 6>, 6> tree_parents{{
        {{-1, 0, 0, 0, 0, 0}}, // star
        {{-1, 0, 1, 2, 3, 4}}, // path
        {{-1, 0, 1, 0, 0, 0}}, // degree-four broom
        {{-1, 0, 0, 0, 1, 1}}, // double star
        {{-1, 0, 1, 2, 0, 0}}, // arm lengths 3,1,1
        {{-1, 0, 1, 0, 3, 0}}, // arm lengths 2,2,1
    }};

    bool failed = false;
    for (std::size_t shape = 0; shape < tree_parents.size(); ++shape) {
        parent = tree_parents[shape];
        leaf_visits = qualified = uncovered = 0;
        for (int root : free_vertices) {
            selected[0] = root;
            search(1, omission_mask[root]);
        }
        std::cout << shape << ' ' << leaf_visits << ' ' << qualified << ' '
                  << uncovered << '\n';
        failed = failed || uncovered != 0;
    }
    return failed ? 10 : 0;
}
