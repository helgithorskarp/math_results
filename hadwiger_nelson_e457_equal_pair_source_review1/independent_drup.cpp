// Independent watched-literal verifier for an all-RUP ASCII DRAT trace.
// The DIMACS CNF path is argv[1]; the decompressed proof is read from stdin.
#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <limits>
#include <map>
#include <sstream>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

namespace {

struct RupResult {
    bool conflict;
    std::uint64_t propagated;
    std::uint64_t clause_inspections;
    std::uint64_t literal_inspections;
};

struct Database {
    int variables;
    std::vector<std::vector<int>> clauses;
    std::vector<int> first_watch;
    std::vector<int> second_watch;
    std::vector<unsigned char> active;
    std::vector<std::vector<int>> watch_lists;
    std::vector<std::pair<int, int>> units;
    std::vector<signed char> assignment;

    explicit Database(int count)
        : variables(count), watch_lists(static_cast<std::size_t>(2*count + 1)),
          assignment(static_cast<std::size_t>(count + 1), 0) {}

    std::size_t literal_index(int literal) const {
        if (literal == 0 || std::abs(literal) > variables) {
            throw std::runtime_error("literal out of range");
        }
        return static_cast<std::size_t>(literal + variables);
    }

    int add(const std::vector<int>& clause) {
        int identifier = static_cast<int>(clauses.size());
        clauses.push_back(clause);
        active.push_back(1);
        if (clause.empty()) {
            first_watch.push_back(-1);
            second_watch.push_back(-1);
        } else if (clause.size() == 1) {
            first_watch.push_back(0);
            second_watch.push_back(0);
            units.emplace_back(identifier, clause[0]);
        } else {
            first_watch.push_back(0);
            second_watch.push_back(1);
            watch_lists[literal_index(clause[0])].push_back(identifier);
            watch_lists[literal_index(clause[1])].push_back(identifier);
        }
        return identifier;
    }

    void deactivate(int identifier) {
        if (identifier < 0 || identifier >= static_cast<int>(active.size()) ||
            active[identifier] == 0) {
            throw std::runtime_error("deactivate inactive clause");
        }
        active[identifier] = 0;
    }

    int value(int literal) const {
        int result = assignment[static_cast<std::size_t>(std::abs(literal))];
        return literal > 0 ? result : -result;
    }

    RupResult rup(const std::vector<int>& candidate) {
        std::vector<int> trail;
        std::vector<int> queue;
        std::uint64_t inspected_clauses = 0;
        std::uint64_t inspected_literals = 0;

        auto enqueue = [&](int literal) {
            int variable = std::abs(literal);
            signed char wanted = static_cast<signed char>(literal > 0 ? 1 : -1);
            signed char& old = assignment[static_cast<std::size_t>(variable)];
            if (old == 0) {
                old = wanted;
                trail.push_back(variable);
                queue.push_back(literal);
                return true;
            }
            return old == wanted;
        };

        bool conflict = false;
        for (auto [identifier, literal] : units) {
            if (active[identifier] != 0 && !enqueue(literal)) {
                conflict = true;
                break;
            }
        }
        if (!conflict) {
            for (int literal : candidate) {
                if (!enqueue(-literal)) {
                    conflict = true;
                    break;
                }
            }
        }

        std::size_t queue_position = 0;
        while (!conflict && queue_position < queue.size()) {
            int made_false = -queue[queue_position++];
            auto& watched = watch_lists[literal_index(made_false)];
            std::size_t position = 0;
            while (position < watched.size()) {
                int identifier = watched[position];
                if (active[identifier] == 0) {
                    watched[position] = watched.back();
                    watched.pop_back();
                    continue;
                }
                ++inspected_clauses;
                const auto& clause = clauses[identifier];
                int first = first_watch[identifier];
                int second = second_watch[identifier];
                int false_slot = -1;
                int other_slot = -1;
                if (clause[static_cast<std::size_t>(first)] == made_false) {
                    false_slot = 0;
                    other_slot = second;
                } else if (clause[static_cast<std::size_t>(second)] == made_false) {
                    false_slot = 1;
                    other_slot = first;
                } else {
                    throw std::runtime_error("stale watch");
                }
                int other_literal = clause[static_cast<std::size_t>(other_slot)];
                if (value(other_literal) > 0) {
                    ++position;
                    continue;
                }

                int replacement = -1;
                for (int slot = 0; slot < static_cast<int>(clause.size()); ++slot) {
                    if (slot == first || slot == second) {
                        continue;
                    }
                    ++inspected_literals;
                    if (value(clause[static_cast<std::size_t>(slot)]) >= 0) {
                        replacement = slot;
                        break;
                    }
                }
                if (replacement >= 0) {
                    if (false_slot == 0) {
                        first_watch[identifier] = replacement;
                    } else {
                        second_watch[identifier] = replacement;
                    }
                    watched[position] = watched.back();
                    watched.pop_back();
                    watch_lists[literal_index(clause[static_cast<std::size_t>(replacement)])]
                        .push_back(identifier);
                    continue;
                }

                int other_value = value(other_literal);
                if (other_value < 0 || !enqueue(other_literal)) {
                    conflict = true;
                    break;
                }
                ++position;
            }
        }

        std::uint64_t propagated = static_cast<std::uint64_t>(queue.size());
        for (int variable : trail) {
            assignment[static_cast<std::size_t>(variable)] = 0;
        }
        return {conflict, propagated, inspected_clauses, inspected_literals};
    }
};

void validate_clause(std::vector<int> clause, int variables) {
    for (int literal : clause) {
        if (literal == 0 || std::abs(literal) > variables) {
            throw std::runtime_error("literal outside declared range");
        }
    }
    std::sort(clause.begin(), clause.end());
    if (std::adjacent_find(clause.begin(), clause.end()) != clause.end()) {
        throw std::runtime_error("repeated literal");
    }
    for (int literal : clause) {
        if (std::binary_search(clause.begin(), clause.end(), -literal)) {
            throw std::runtime_error("tautological clause");
        }
    }
}

std::vector<int> key(std::vector<int> clause) {
    std::sort(clause.begin(), clause.end());
    return clause;
}

struct Formula {
    int variables;
    std::vector<std::vector<int>> clauses;
};

Formula read_cnf(const std::string& path) {
    std::ifstream input(path);
    if (!input) {
        throw std::runtime_error("cannot open CNF");
    }
    int variables = -1;
    int declared = -1;
    std::vector<std::vector<int>> clauses;
    std::string line;
    while (std::getline(input, line)) {
        if (line.empty() || line[0] == 'c') {
            continue;
        }
        std::istringstream stream(line);
        if (line[0] == 'p') {
            std::string p;
            std::string cnf;
            std::string trailing;
            if (!(stream >> p >> cnf >> variables >> declared) || p != "p" || cnf != "cnf" ||
                variables <= 0 || declared < 0 || (stream >> trailing)) {
                throw std::runtime_error("bad CNF header");
            }
            continue;
        }
        if (variables < 0) {
            throw std::runtime_error("clause before CNF header");
        }
        std::vector<int> clause;
        int literal = 0;
        bool terminated = false;
        while (stream >> literal) {
            if (literal == 0) {
                terminated = true;
                std::string trailing;
                if (stream >> trailing) {
                    throw std::runtime_error("CNF content after terminator");
                }
                break;
            }
            clause.push_back(literal);
        }
        if (!terminated) {
            throw std::runtime_error("unterminated CNF clause");
        }
        validate_clause(clause, variables);
        clauses.push_back(std::move(clause));
    }
    if (variables < 0 || static_cast<int>(clauses.size()) != declared) {
        throw std::runtime_error("CNF clause count mismatch");
    }
    return {variables, std::move(clauses)};
}

int self_test() {
    Database forced(1);
    forced.add({1});
    forced.add({-1});
    bool empty_is_rup = forced.rup({}).conflict;

    Database open(2);
    open.add({1, 2});
    bool unsupported_rejected = !open.rup({1}).conflict;

    Database square(2);
    square.add({1, 2});
    square.add({-1, 2});
    square.add({1, -2});
    square.add({-1, -2});
    bool derived_unit = square.rup({2}).conflict;
    if (!(empty_is_rup && unsupported_rejected && derived_unit)) {
        throw std::runtime_error("self-test failed");
    }
    std::cout << "{\"unit_conflict_empty_clause_rup\":true,"
                 "\"unsupported_unit_rejected\":true,"
                 "\"four_clause_derived_unit_rup\":true}\n";
    return 0;
}

}  // namespace

int main(int argc, char** argv) {
    try {
        if (argc == 2 && std::string(argv[1]) == "--self-test") {
            return self_test();
        }
        if (argc != 2) {
            throw std::runtime_error("usage: independent_drup CNF < decompressed.drat");
        }
        Formula formula = read_cnf(argv[1]);
        Database database(formula.variables);
        std::map<std::vector<int>, std::vector<int>> active;
        for (const auto& clause : formula.clauses) {
            int identifier = database.add(clause);
            active[key(clause)].push_back(identifier);
        }

        std::uint64_t lines = 0;
        std::uint64_t additions = 0;
        std::uint64_t deletions = 0;
        std::uint64_t propagated = 0;
        std::uint64_t clause_inspections = 0;
        std::uint64_t literal_inspections = 0;
        std::size_t maximum_clause_length = 0;
        std::uint64_t empty_line = 0;
        std::string line;
        while (std::getline(std::cin, line)) {
            ++lines;
            if (empty_line != 0 || line.empty()) {
                throw std::runtime_error("empty line or content after empty clause");
            }
            std::istringstream stream(line);
            std::string first_token;
            if (!(stream >> first_token)) {
                throw std::runtime_error("bad proof line");
            }
            bool deleting = first_token == "d";
            std::vector<int> values;
            if (!deleting) {
                std::size_t consumed = 0;
                int first_literal = std::stoi(first_token, &consumed);
                if (consumed != first_token.size()) {
                    throw std::runtime_error("bad proof literal");
                }
                values.push_back(first_literal);
            }
            int value = 0;
            while (stream >> value) {
                values.push_back(value);
            }
            if (values.empty() || values.back() != 0 ||
                std::find(values.begin(), values.end() - 1, 0) != values.end() - 1) {
                throw std::runtime_error("bad proof terminator");
            }
            values.pop_back();
            validate_clause(values, formula.variables);
            maximum_clause_length = std::max(maximum_clause_length, values.size());
            auto normalized = key(values);
            if (deleting) {
                auto found = active.find(normalized);
                if (values.empty() || found == active.end() || found->second.empty()) {
                    throw std::runtime_error("delete inactive clause");
                }
                database.deactivate(found->second.back());
                found->second.pop_back();
                ++deletions;
                continue;
            }

            RupResult result = database.rup(values);
            if (!result.conflict) {
                throw std::runtime_error("non-RUP addition at proof line " + std::to_string(lines));
            }
            ++additions;
            propagated += result.propagated;
            clause_inspections += result.clause_inspections;
            literal_inspections += result.literal_inspections;
            int identifier = database.add(values);
            active[normalized].push_back(identifier);
            if (values.empty()) {
                empty_line = lines;
            }
        }

        if (empty_line != lines || additions != 131322 || deletions != 141579) {
            throw std::runtime_error("proof dimension or final-clause mismatch");
        }
        std::cout << "{\"drup_lines\":" << lines
                  << ",\"drup_additions_verified_by_watched_rup\":" << additions
                  << ",\"drup_deletion_lines_live\":" << deletions
                  << ",\"drup_final_empty_clause_line\":" << empty_line
                  << ",\"drup_maximum_clause_length\":" << maximum_clause_length
                  << ",\"drup_propagated_assignments\":" << propagated
                  << ",\"drup_watched_clause_inspections\":" << clause_inspections
                  << ",\"drup_replacement_literal_inspections\":" << literal_inspections
                  << ",\"drup_deletions_applied_after_liveness_check\":true}\n";
        return 0;
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 2;
    }
}
