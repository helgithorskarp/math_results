#include <algorithm>
#include <array>
#include <fstream>
#include <iostream>
#include <map>
#include <numeric>
#include <set>
#include <sstream>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

namespace {

constexpr int order = 43;
constexpr int edge_count = order * (order - 1) / 2;

struct DisjointSet {
  explicit DisjointSet(int size) : parent(static_cast<std::size_t>(size)) {
    std::iota(parent.begin(), parent.end(), 0);
  }
  int find(int item) {
    int &entry = parent.at(static_cast<std::size_t>(item));
    if (entry != item) entry = find(entry);
    return entry;
  }
  void unite(int left, int right) {
    left = find(left);
    right = find(right);
    if (left != right) parent.at(static_cast<std::size_t>(right)) = left;
  }
  std::vector<int> parent;
};

using Pair = std::pair<int, int>;
using Clause = std::vector<int>;

struct ClauseLess {
  bool operator()(const Clause &left, const Clause &right) const {
    if (left.size() != right.size()) return left.size() < right.size();
    return left < right;
  }
};

using Formula = std::set<Clause, ClauseLess>;

struct Orbits {
  std::array<std::array<int, order>, order> variable{};
  std::map<int, int> size_distribution;
  int variables = 0;
};

std::array<int, order> successor(const std::array<int, 3> &counts) {
  constexpr std::array<int, 3> lengths{9, 3, 1};
  std::array<int, order> result{};
  int top = 0;
  for (int kind = 0; kind < 3; ++kind) {
    const int length = lengths.at(static_cast<std::size_t>(kind));
    for (int cycle = 0; cycle < counts.at(static_cast<std::size_t>(kind)); ++cycle) {
      for (int position = 0; position < length; ++position) {
        result.at(static_cast<std::size_t>(top + position)) = top + (position + 1) % length;
      }
      top += length;
    }
  }
  if (top != order) throw std::runtime_error("cycle counts do not cover 43 vertices");
  return result;
}

Orbits construct_orbits(const std::array<int, 3> &counts) {
  const auto permutation = successor(counts);
  std::array<std::array<int, order>, order> edge_id{};
  std::vector<Pair> pairs;
  for (int left = 0; left < order; ++left) {
    for (int right = left + 1; right < order; ++right) {
      const int id = static_cast<int>(pairs.size());
      pairs.emplace_back(left, right);
      edge_id.at(static_cast<std::size_t>(left)).at(static_cast<std::size_t>(right)) = id;
      edge_id.at(static_cast<std::size_t>(right)).at(static_cast<std::size_t>(left)) = id;
    }
  }
  DisjointSet dsu(edge_count);
  for (int id = 0; id < edge_count; ++id) {
    auto [left, right] = pairs.at(static_cast<std::size_t>(id));
    left = permutation.at(static_cast<std::size_t>(left));
    right = permutation.at(static_cast<std::size_t>(right));
    if (left > right) std::swap(left, right);
    dsu.unite(id, edge_id.at(static_cast<std::size_t>(left)).at(static_cast<std::size_t>(right)));
  }

  std::map<int, Pair> representative;
  for (int id = 0; id < edge_count; ++id) {
    const int root = dsu.find(id);
    const Pair pair = pairs.at(static_cast<std::size_t>(id));
    const auto found = representative.find(root);
    if (found == representative.end() || pair < found->second) representative[root] = pair;
  }
  std::vector<std::pair<Pair, int>> ordered;
  for (const auto &[root, pair] : representative) ordered.emplace_back(pair, root);
  std::sort(ordered.begin(), ordered.end());
  std::map<int, int> root_variable;
  for (std::size_t position = 0; position < ordered.size(); ++position) {
    root_variable[ordered.at(position).second] = static_cast<int>(position) + 1;
  }

  Orbits result;
  result.variables = static_cast<int>(ordered.size());
  std::map<int, int> orbit_size;
  for (int id = 0; id < edge_count; ++id) {
    const int variable = root_variable.at(dsu.find(id));
    const auto [left, right] = pairs.at(static_cast<std::size_t>(id));
    result.variable.at(static_cast<std::size_t>(left)).at(static_cast<std::size_t>(right)) = variable;
    result.variable.at(static_cast<std::size_t>(right)).at(static_cast<std::size_t>(left)) = variable;
    ++orbit_size[variable];
  }
  for (const auto &[variable, size] : orbit_size) {
    (void)variable;
    ++result.size_distribution[size];
  }
  return result;
}

void insert_normalized(Formula &formula, Clause clause) {
  std::sort(clause.begin(), clause.end());
  clause.erase(std::unique(clause.begin(), clause.end()), clause.end());
  for (int literal : clause) {
    if (std::binary_search(clause.begin(), clause.end(), -literal)) return;
  }
  formula.insert(std::move(clause));
}

void add_degree_network(Formula &formula, std::vector<int> wires,
                        int &variable_count) {
  if (wires.size() != 42) throw std::runtime_error("degree row does not have 42 inputs");
  for (int end = static_cast<int>(wires.size()) - 1; end > 0; --end) {
    for (int position = 0; position < end; ++position) {
      const int left = wires.at(static_cast<std::size_t>(position));
      const int right = wires.at(static_cast<std::size_t>(position + 1));
      const int high = ++variable_count;
      const int low = ++variable_count;
      insert_normalized(formula, {-left, high});
      insert_normalized(formula, {-right, high});
      insert_normalized(formula, {left, right, -high});
      insert_normalized(formula, {left, -low});
      insert_normalized(formula, {right, -low});
      insert_normalized(formula, {-left, -right, low});
      wires.at(static_cast<std::size_t>(position)) = high;
      wires.at(static_cast<std::size_t>(position + 1)) = low;
    }
  }
  insert_normalized(formula, {wires.at(17)});
  insert_normalized(formula, {-wires.at(24)});
}

Formula expected_formula(const Orbits &orbits, const std::array<int, 3> &counts,
                         bool degree, int &variable_count) {
  Formula result;
  for (int a = 0; a < order - 4; ++a) {
    for (int b = a + 1; b < order - 3; ++b) {
      for (int c = b + 1; c < order - 2; ++c) {
        for (int d = c + 1; d < order - 1; ++d) {
          for (int e = d + 1; e < order; ++e) {
            const std::array<int, 5> vertices{a, b, c, d, e};
            std::set<int> unique;
            for (int left = 0; left < 5; ++left) {
              for (int right = left + 1; right < 5; ++right) {
                unique.insert(orbits.variable.at(static_cast<std::size_t>(vertices.at(static_cast<std::size_t>(left))))
                                  .at(static_cast<std::size_t>(vertices.at(static_cast<std::size_t>(right)))));
              }
            }
            Clause positive(unique.begin(), unique.end());
            Clause negative;
            for (auto item = positive.rbegin(); item != positive.rend(); ++item) negative.push_back(-*item);
            result.insert(std::move(positive));
            result.insert(std::move(negative));
          }
        }
      }
    }
  }
  if (degree) {
    constexpr std::array<int, 3> lengths{9, 3, 1};
    int top = 0;
    for (int kind = 0; kind < 3; ++kind) {
      const int length = lengths.at(static_cast<std::size_t>(kind));
      for (int cycle = 0; cycle < counts.at(static_cast<std::size_t>(kind)); ++cycle) {
        const int vertex = top;
        std::vector<int> inputs;
        for (int other = 0; other < order; ++other) {
          if (other != vertex) {
            inputs.push_back(orbits.variable.at(static_cast<std::size_t>(vertex))
                                 .at(static_cast<std::size_t>(other)));
          }
        }
        add_degree_network(result, std::move(inputs), variable_count);
        top += length;
      }
    }
  }
  return result;
}

Formula read_formula(const std::string &path, int expected_variables,
                     int &declared_clauses) {
  std::ifstream input(path);
  if (!input) throw std::runtime_error("could not open DIMACS");
  std::string line;
  int variables = -1;
  declared_clauses = -1;
  Formula result;
  int parsed = 0;
  while (std::getline(input, line)) {
    if (line.empty() || line.front() == 'c') continue;
    if (line.front() == 'p') {
      std::istringstream header(line);
      std::string p, cnf;
      header >> p >> cnf >> variables >> declared_clauses;
      if (p != "p" || cnf != "cnf" || variables != expected_variables) {
        throw std::runtime_error("bad DIMACS header");
      }
      continue;
    }
    std::istringstream row(line);
    Clause clause;
    int literal = 0;
    bool terminated = false;
    while (row >> literal) {
      if (literal == 0) {
        terminated = true;
        break;
      }
      if (std::abs(literal) > expected_variables) throw std::runtime_error("literal outside range");
      clause.push_back(literal);
    }
    if (!terminated || clause.empty() || !std::is_sorted(clause.begin(), clause.end())) {
      throw std::runtime_error("malformed or unsorted clause");
    }
    if (!result.insert(clause).second) throw std::runtime_error("duplicate clause");
    ++parsed;
  }
  if (variables < 0 || parsed != declared_clauses || parsed != static_cast<int>(result.size())) {
    throw std::runtime_error("DIMACS clause count mismatch");
  }
  return result;
}

}  // namespace

int main(int argc, char **argv) {
  try {
    if (argc != 6) {
      std::cerr << "usage: verify_formula C9 C3 FIXED DEGREE FORMULA.cnf\n";
      return 2;
    }
    std::array<int, 3> counts{};
    for (int index = 0; index < 3; ++index) {
      counts.at(static_cast<std::size_t>(index)) = std::stoi(argv[index + 1]);
    }
    const bool degree = std::stoi(argv[4]) != 0;
    const Orbits orbits = construct_orbits(counts);
    int variable_count = orbits.variables;
    const Formula expected = expected_formula(orbits, counts, degree, variable_count);
    int declared_clauses = 0;
    const Formula actual = read_formula(argv[5], variable_count, declared_clauses);
    if (actual != expected) throw std::runtime_error("formula clause set differs");

    std::map<std::size_t, int> lengths;
    for (const Clause &clause : actual) ++lengths[clause.size()];
    std::cout << "case=" << counts[0] << ',' << counts[1] << ',' << counts[2]
              << " degree=" << degree << " edge_orbits=" << orbits.variables
              << " variables=" << variable_count << " orbit_sizes=";
    bool first = true;
    for (const auto &[size, count] : orbits.size_distribution) {
      if (!first) std::cout << ',';
      std::cout << size << ':' << count;
      first = false;
    }
    std::cout << "\nclauses=" << declared_clauses << " clause_lengths=";
    first = true;
    for (const auto &[length, count] : lengths) {
      if (!first) std::cout << ',';
      std::cout << length << ':' << count;
      first = false;
    }
    std::cout << "\nformula_verified=true\n";
    return 0;
  } catch (const std::exception &error) {
    std::cerr << "ERROR: " << error.what() << '\n';
    return 1;
  }
}
