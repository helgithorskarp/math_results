#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <map>
#include <numeric>
#include <set>
#include <stdexcept>
#include <tuple>
#include <utility>
#include <vector>

using Graph = std::uint64_t;
using Row = std::array<int, 6>;
using Matrix = std::array<Row, 6>;

struct Choice {
    int source;
    int target;
};

struct FamilyStats {
    std::vector<int> totals;
    int minimum_degree = 1'000'000;
};

struct Audit {
    std::uint64_t zero_root_types = 0;
    std::uint64_t systems = 0;
    std::uint64_t blocked_by_three = 0;
    std::uint64_t blocked_by_four = 0;
    std::uint64_t feasible = 0;
    std::set<Graph> feasible_graphs;
    FamilyStats tournament;
    FamilyStats missing_arc;
};

void need(bool condition, const char* message) {
    if (!condition) {
        throw std::runtime_error(message);
    }
}

bool edge(Graph graph, int from, int to) {
    return ((graph >> (6 * from + to)) & 1U) != 0U;
}

Graph add_edge(Graph graph, int from, int to) {
    return graph | (Graph{1} << (6 * from + to));
}

std::vector<std::vector<int>> permutations(int order) {
    std::vector<int> permutation(static_cast<std::size_t>(order));
    std::iota(permutation.begin(), permutation.end(), 0);
    std::vector<std::vector<int>> result;
    do {
        result.push_back(permutation);
    } while (std::next_permutation(permutation.begin(), permutation.end()));
    return result;
}

Graph canonical(Graph graph, int order, const std::vector<std::vector<int>>& perms) {
    Graph best = ~Graph{0};
    for (const auto& permutation : perms) {
        Graph image = 0;
        for (int i = 0; i < order; ++i) {
            for (int j = 0; j < order; ++j) {
                if (edge(graph, i, j)) {
                    image = add_edge(image, permutation[static_cast<std::size_t>(i)],
                                     permutation[static_cast<std::size_t>(j)]);
                }
            }
        }
        best = std::min(best, image);
    }
    return best;
}

std::pair<std::vector<Graph>, std::vector<int>> augment_graphs() {
    std::vector<Graph> graphs{0};
    std::vector<int> counts{1};
    int power = 1;
    for (int order = 1; order < 6; ++order) {
        power *= 3;
        const auto perms = permutations(order + 1);
        std::set<Graph> next;
        for (Graph old : graphs) {
            for (int word = 0; word < power; ++word) {
                Graph graph = old;
                int value = word;
                for (int i = 0; i < order; ++i) {
                    const int state = value % 3;
                    value /= 3;
                    if (state == 1) {
                        graph = add_edge(graph, i, order);
                    } else if (state == 2) {
                        graph = add_edge(graph, order, i);
                    }
                }
                next.insert(canonical(graph, order + 1, perms));
            }
        }
        graphs.assign(next.begin(), next.end());
        counts.push_back(static_cast<int>(graphs.size()));
    }
    return {graphs, counts};
}

std::array<int, 6> out_masks(Graph graph) {
    std::array<int, 6> result{};
    for (int i = 0; i < 6; ++i) {
        for (int j = 0; j < 6; ++j) {
            if (edge(graph, i, j)) {
                result[static_cast<std::size_t>(i)] |= 1 << j;
            }
        }
    }
    return result;
}

std::vector<Choice> closed_choices(const std::array<int, 6>& out, int root) {
    const int left = out[static_cast<std::size_t>(root)];
    const int outside = 63 & ~(left | (1 << root));
    std::map<int, int> target_to_union;
    for (int source = left; source != 0; source = (source - 1) & left) {
        int target = 0;
        for (int u = 0; u < 6; ++u) {
            if ((source >> u) & 1) {
                target |= out[static_cast<std::size_t>(u)] & outside;
            }
        }
        target_to_union[target] |= source;
    }

    std::vector<Choice> result;
    for (const auto& [target, closure] : target_to_union) {
        int actual = 0;
        for (int u = 0; u < 6; ++u) {
            if ((closure >> u) & 1) {
                actual |= out[static_cast<std::size_t>(u)] & outside;
            }
        }
        need(actual == target, "source grouping did not produce a closure");
        result.push_back({closure, target});
    }
    return result;
}

std::vector<Row> primitive_covers(int maximum, bool require_maximum) {
    int total = 1;
    for (int i = 0; i < 6; ++i) {
        total *= maximum + 1;
    }
    std::vector<Row> result;
    for (int word = 1; word < total; ++word) {
        int value = word;
        Row cover{};
        int gcd = 0;
        bool reaches_maximum = false;
        for (int i = 0; i < 6; ++i) {
            cover[static_cast<std::size_t>(i)] = value % (maximum + 1);
            value /= maximum + 1;
            gcd = std::gcd(gcd, cover[static_cast<std::size_t>(i)]);
            reaches_maximum |= cover[static_cast<std::size_t>(i)] == maximum;
        }
        if (gcd == 1 && (!require_maximum || reaches_maximum)) {
            result.push_back(cover);
        }
    }
    std::sort(result.begin(), result.end(), [](const Row& first, const Row& second) {
        const int first_sum = std::accumulate(first.begin(), first.end(), 0);
        const int second_sum = std::accumulate(second.begin(), second.end(), 0);
        return std::tie(first_sum, first) < std::tie(second_sum, second);
    });
    return result;
}

bool has_cover(const Matrix& matrix, const std::vector<Row>& covers) {
    for (const Row& cover : covers) {
        bool works = true;
        for (int column = 0; column < 6 && works; ++column) {
            int value = 0;
            for (int row = 0; row < 6; ++row) {
                value += cover[static_cast<std::size_t>(row)]
                       * matrix[static_cast<std::size_t>(row)][static_cast<std::size_t>(column)];
            }
            works = value <= 0;
        }
        if (works) {
            return true;
        }
    }
    return false;
}

long long determinant(const Matrix& input) {
    std::array<std::array<long long, 6>, 6> matrix{};
    for (int i = 0; i < 6; ++i) {
        for (int j = 0; j < 6; ++j) {
            matrix[static_cast<std::size_t>(i)][static_cast<std::size_t>(j)] =
                input[static_cast<std::size_t>(i)][static_cast<std::size_t>(j)];
        }
    }
    long long sign = 1;
    long long previous = 1;
    for (int column = 0; column < 5; ++column) {
        int pivot_row = column;
        while (pivot_row < 6 && matrix[static_cast<std::size_t>(pivot_row)][static_cast<std::size_t>(column)] == 0) {
            ++pivot_row;
        }
        if (pivot_row == 6) {
            return 0;
        }
        if (pivot_row != column) {
            std::swap(matrix[static_cast<std::size_t>(pivot_row)], matrix[static_cast<std::size_t>(column)]);
            sign = -sign;
        }
        const long long pivot = matrix[static_cast<std::size_t>(column)][static_cast<std::size_t>(column)];
        for (int i = column + 1; i < 6; ++i) {
            for (int j = column + 1; j < 6; ++j) {
                const long long numerator =
                    matrix[static_cast<std::size_t>(i)][static_cast<std::size_t>(j)] * pivot
                    - matrix[static_cast<std::size_t>(i)][static_cast<std::size_t>(column)]
                      * matrix[static_cast<std::size_t>(column)][static_cast<std::size_t>(j)];
                need(numerator % previous == 0, "nonexact Bareiss division");
                matrix[static_cast<std::size_t>(i)][static_cast<std::size_t>(j)] = numerator / previous;
            }
        }
        for (int i = column + 1; i < 6; ++i) {
            matrix[static_cast<std::size_t>(i)][static_cast<std::size_t>(column)] = 0;
        }
        previous = pivot;
    }
    return sign * matrix[5][5];
}

Row solve_unit(const Matrix& matrix) {
    const long long denominator = determinant(matrix);
    need(denominator == -1, "unobstructed system is not determinant minus one");
    Row weights{};
    for (int column = 0; column < 6; ++column) {
        Matrix replaced = matrix;
        for (int row = 0; row < 6; ++row) {
            replaced[static_cast<std::size_t>(row)][static_cast<std::size_t>(column)] = 1;
        }
        const long long numerator = determinant(replaced);
        need(numerator % denominator == 0, "nonintegral unit solution");
        weights[static_cast<std::size_t>(column)] = static_cast<int>(numerator / denominator);
        need(weights[static_cast<std::size_t>(column)] > 0, "unobstructed system lacks a positive unit solution");
    }
    for (int row = 0; row < 6; ++row) {
        int value = 0;
        for (int column = 0; column < 6; ++column) {
            value += matrix[static_cast<std::size_t>(row)][static_cast<std::size_t>(column)]
                   * weights[static_cast<std::size_t>(column)];
        }
        need(value == 1, "Cramer solution check failed");
    }
    return weights;
}

int missing_pairs(Graph graph) {
    int missing = 0;
    for (int i = 0; i < 6; ++i) {
        for (int j = i + 1; j < 6; ++j) {
            missing += !edge(graph, i, j) && !edge(graph, j, i);
        }
    }
    return missing;
}

void record_feasible(Graph graph, const std::array<int, 6>& out, const Matrix& matrix, Audit& audit) {
    const Row weights = solve_unit(matrix);
    ++audit.feasible;
    audit.feasible_graphs.insert(graph);
    FamilyStats* family = nullptr;
    const int missing = missing_pairs(graph);
    if (missing == 0) {
        family = &audit.tournament;
    } else if (missing == 1) {
        family = &audit.missing_arc;
    } else {
        throw std::runtime_error("unexpected feasible missing-pair count");
    }
    family->totals.push_back(std::accumulate(weights.begin(), weights.end(), 0));
    for (int root = 0; root < 6; ++root) {
        int degree = 0;
        for (int vertex = 0; vertex < 6; ++vertex) {
            if ((out[static_cast<std::size_t>(root)] >> vertex) & 1) {
                degree += weights[static_cast<std::size_t>(vertex)];
            }
        }
        family->minimum_degree = std::min(family->minimum_degree, degree);
    }
}

void enumerate_systems(Graph graph, const std::array<int, 6>& out,
                       const std::array<std::vector<Choice>, 6>& choices,
                       const std::vector<Row>& covers_three,
                       const std::vector<Row>& covers_four,
                       int root, Matrix& matrix, Audit& audit) {
    if (root < 6) {
        for (const Choice& choice : choices[static_cast<std::size_t>(root)]) {
            for (int vertex = 0; vertex < 6; ++vertex) {
                matrix[static_cast<std::size_t>(root)][static_cast<std::size_t>(vertex)] =
                    ((choice.source >> vertex) & 1) - ((choice.target >> vertex) & 1);
            }
            enumerate_systems(graph, out, choices, covers_three, covers_four,
                              root + 1, matrix, audit);
        }
        return;
    }

    ++audit.systems;
    if (has_cover(matrix, covers_three)) {
        ++audit.blocked_by_three;
    } else if (has_cover(matrix, covers_four)) {
        ++audit.blocked_by_four;
    } else {
        record_feasible(graph, out, matrix, audit);
    }
}

Graph from_out_lists(const std::array<std::vector<int>, 6>& lists) {
    Graph graph = 0;
    for (int i = 0; i < 6; ++i) {
        for (int j : lists[static_cast<std::size_t>(i)]) {
            graph = add_edge(graph, i, j);
        }
    }
    return graph;
}

void print_vector(const std::vector<int>& values) {
    std::cout << '[';
    for (std::size_t i = 0; i < values.size(); ++i) {
        if (i != 0) {
            std::cout << ',';
        }
        std::cout << values[i];
    }
    std::cout << ']';
}

void print_family(const FamilyStats& family) {
    std::vector<int> totals = family.totals;
    std::sort(totals.begin(), totals.end());
    std::cout << "{\"cones\":" << totals.size() << ",\"cone_minima\":";
    print_vector(totals);
    std::cout << ",\"minimum_total\":" << totals.front()
              << ",\"minimum_external_out_degree\":" << family.minimum_degree << '}';
}

int main() {
    try {
        const auto [graphs, counts] = augment_graphs();
        need(counts == std::vector<int>({1, 2, 7, 42, 582, 21480}),
             "canonical augmentation count mismatch");

        const auto covers_three = primitive_covers(3, false);
        const auto covers_four = primitive_covers(4, true);
        Audit audit;
        for (Graph graph : graphs) {
            const auto out = out_masks(graph);
            std::array<std::vector<Choice>, 6> choices;
            bool zero_root = false;
            for (int root = 0; root < 6; ++root) {
                choices[static_cast<std::size_t>(root)] = closed_choices(out, root);
                zero_root |= choices[static_cast<std::size_t>(root)].empty();
            }
            if (zero_root) {
                ++audit.zero_root_types;
            } else {
                Matrix matrix{};
                enumerate_systems(graph, out, choices, covers_three, covers_four, 0, matrix, audit);
            }
        }

        const std::array<std::vector<int>, 6> tournament{{
            {1, 2, 3}, {2, 3, 4}, {3, 5}, {4, 5}, {0, 2}, {0, 1, 4}}};
        const std::array<std::vector<int>, 6> missing_arc{{
            {2, 3}, {4, 5}, {1, 3, 4}, {1, 5}, {0, 3, 5}, {0, 2}}};
        const auto perms = permutations(6);
        const std::set<Graph> expected_graphs{
            canonical(from_out_lists(tournament), 6, perms),
            canonical(from_out_lists(missing_arc), 6, perms)};

        need(audit.zero_root_types == 13348, "zero-root count mismatch");
        need(audit.systems == 235526, "Hall-system count mismatch");
        need(audit.blocked_by_three == 235505, "coefficient-three count mismatch");
        need(audit.blocked_by_four == 1, "coefficient-four count mismatch");
        need(audit.feasible == 20, "feasible-system count mismatch");
        need(audit.feasible_graphs == expected_graphs, "feasible quotient classification mismatch");

        std::cout << "{\"status\":\"REVIEWER EXHAUSTIVE CLASSIFICATION VERIFIED\","
                  << "\"augmentation_counts\":";
        print_vector(counts);
        std::cout << ",\"oriented_types\":" << graphs.size()
                  << ",\"zero_root_types\":" << audit.zero_root_types
                  << ",\"closed_hall_systems\":" << audit.systems
                  << ",\"blocked_by_coefficients_at_most_three\":" << audit.blocked_by_three
                  << ",\"blocked_only_after_allowing_coefficient_four\":" << audit.blocked_by_four
                  << ",\"feasible_systems\":" << audit.feasible
                  << ",\"families\":{\"tournament\":";
        print_family(audit.tournament);
        std::cout << ",\"missing_arc\":";
        print_family(audit.missing_arc);
        std::cout << "}}\n";
        return 0;
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
