#include <cadical.hpp>

#include <algorithm>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

using Matrix = std::vector<std::vector<unsigned char>>;

static Matrix decode(const std::string &record) {
    if (record.empty()) throw std::runtime_error("empty graph6");
    int order = static_cast<unsigned char>(record[0]) - 63;
    if (order != 42) throw std::runtime_error("order is not 42");
    std::vector<int> bits;
    for (size_t position = 1; position < record.size(); ++position) {
        int value = static_cast<unsigned char>(record[position]) - 63;
        if (value < 0 || value > 63)
            throw std::runtime_error("bad graph6 byte");
        for (int shift = 5; shift >= 0; --shift)
            bits.push_back((value >> shift) & 1);
    }
    if (bits.size() < 861) throw std::runtime_error("truncated graph6");
    Matrix adjacency(order, std::vector<unsigned char>(order));
    int at = 0;
    for (int high = 1; high < order; ++high)
        for (int low = 0; low < high; ++low)
            adjacency[low][high] = adjacency[high][low] = bits[at++];
    return adjacency;
}

static std::string graph6(const Matrix &adjacency) {
    std::string record(1, static_cast<char>(adjacency.size() + 63));
    int value = 0, used = 0;
    for (int high = 1; high < static_cast<int>(adjacency.size()); ++high) {
        for (int low = 0; low < high; ++low) {
            value = (value << 1) | adjacency[low][high];
            if (++used == 6) {
                record.push_back(static_cast<char>(value + 63));
                value = used = 0;
            }
        }
    }
    if (used) {
        value <<= 6 - used;
        record.push_back(static_cast<char>(value + 63));
    }
    return record;
}

static int edge_index(int low, int high) {
    if (low > high) std::swap(low, high);
    return high * (high - 1) / 2 + low;
}

// Seven one-way threshold levels are enough to forbid a seventh selected edge.
static int counter_var(int edge, int level) {
    return 862 + 7 * edge + (level - 1);
}

static void add_clause(CaDiCaL::Solver &solver,
                       const std::vector<int> &clause) {
    for (int literal : clause) solver.add(literal);
    solver.add(0);
}

int main(int argc, char **argv) try {
    if (argc != 4) {
        std::cerr << "usage: enumerate_six_flip_sat CATALOG.g6 START COUNT\n";
        return 2;
    }
    size_t start = std::stoull(argv[2]);
    size_t count = std::stoull(argv[3]);
    std::ifstream input(argv[1]);
    std::vector<std::string> records;
    std::string line;
    while (std::getline(input, line))
        if (!line.empty()) records.push_back(line);
    if (start > records.size() || count > records.size() - start)
        throw std::runtime_error("bad range");

    std::vector<std::pair<int, int>> edges;
    for (int high = 1; high < 42; ++high)
        for (int low = 0; low < high; ++low)
            edges.emplace_back(low, high);

    uint64_t total_exact6 = 0, total_lower = 0;
    for (size_t index = start; index < start + count; ++index) {
        Matrix adjacency = decode(records[index]);
        CaDiCaL::Solver solver;
        long clauses = 0, ramsey_clauses = 0;

        // Forward sequential counter: selecting seven flip variables implies
        // the forbidden final level. Auxiliary variables need not be exact.
        for (int edge = 0; edge < 861; ++edge) {
            int flip = edge + 1;
            add_clause(solver, {-flip, counter_var(edge, 1)});
            ++clauses;
            if (edge) {
                for (int level = 1; level <= 7; ++level) {
                    add_clause(solver,
                               {-counter_var(edge - 1, level),
                                counter_var(edge, level)});
                    ++clauses;
                }
                for (int level = 2; level <= 7; ++level) {
                    add_clause(solver,
                               {-flip, -counter_var(edge - 1, level - 1),
                                counter_var(edge, level)});
                    ++clauses;
                }
            }
        }
        add_clause(solver, {-counter_var(860, 7)});
        ++clauses;

        // Under the at-most-six condition, add each homogeneous state whose
        // Hamming distance from the original 5-set is at most six.
        for (int v0 = 0; v0 < 42; ++v0)
            for (int v1 = v0 + 1; v1 < 42; ++v1)
                for (int v2 = v1 + 1; v2 < 42; ++v2)
                    for (int v3 = v2 + 1; v3 < 42; ++v3)
                        for (int v4 = v3 + 1; v4 < 42; ++v4) {
                            int vertices[5] = {v0, v1, v2, v3, v4};
                            std::vector<int> present, absent;
                            for (int i = 0; i < 5; ++i) {
                                for (int j = i + 1; j < 5; ++j) {
                                    int flip =
                                        edge_index(vertices[i], vertices[j]) + 1;
                                    (adjacency[vertices[i]][vertices[j]] ? present
                                                                         : absent)
                                        .push_back(flip);
                                }
                            }
                            if (absent.size() <= 6) {
                                std::vector<int> clause;
                                for (int flip : present) clause.push_back(flip);
                                for (int flip : absent) clause.push_back(-flip);
                                add_clause(solver, clause);
                                ++clauses;
                                ++ramsey_clauses;
                            }
                            if (present.size() <= 6) {
                                std::vector<int> clause;
                                for (int flip : present) clause.push_back(-flip);
                                for (int flip : absent) clause.push_back(flip);
                                add_clause(solver, clause);
                                ++clauses;
                                ++ramsey_clauses;
                            }
                        }

        uint64_t exact6 = 0, lower = 0;
        while (true) {
            int status = solver.solve();
            if (status == CaDiCaL::UNSATISFIABLE) break;
            if (status != CaDiCaL::SATISFIABLE)
                throw std::runtime_error("solver returned UNKNOWN");
            std::vector<int> selected;
            for (int edge = 0; edge < 861; ++edge)
                if (solver.val(edge + 1) > 0) selected.push_back(edge);
            if (selected.size() > 6)
                throw std::runtime_error("cardinality encoding failure");

            if (selected.size() == 6) {
                Matrix variant = adjacency;
                for (int edge : selected) {
                    auto [low, high] = edges[edge];
                    variant[low][high] = variant[high][low] =
                        !variant[low][high];
                }
                std::cout << index;
                for (int edge : selected) {
                    auto [low, high] = edges[edge];
                    std::cout << '\t' << low << ',' << high;
                }
                std::cout << '\t' << graph6(variant) << '\n';
                ++exact6;
                ++total_exact6;
            } else {
                ++lower;
                ++total_lower;
            }

            // Block the complete flip-variable assignment, independent of
            // the deliberately nonunique sequential-counter auxiliaries.
            for (int edge = 0; edge < 861; ++edge) {
                bool chosen =
                    std::binary_search(selected.begin(), selected.end(), edge);
                solver.add(chosen ? -(edge + 1) : edge + 1);
            }
            solver.add(0);
        }
        std::cerr << "parent=" << index << " exact6=" << exact6
                  << " lower_models=" << lower << " variables=6888"
                  << " clauses=" << clauses
                  << " ramsey_clauses=" << ramsey_clauses << '\n';
    }
    std::cerr << "SUMMARY start=" << start << " count=" << count
              << " exact6=" << total_exact6
              << " lower_models=" << total_lower << '\n';
    return 0;
} catch (const std::exception &error) {
    std::cerr << "error: " << error.what() << '\n';
    return 1;
}
