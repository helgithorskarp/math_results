#include <algorithm>
#include <array>
#include <cstddef>
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

constexpr int n = 43;
using Clause = std::vector<int>;
using Formula = std::set<Clause>;

struct Dsu {
  explicit Dsu(int size) : parent(static_cast<std::size_t>(size)) {
    std::iota(parent.begin(), parent.end(), 0);
  }
  int find(int x) {
    int &p = parent.at(static_cast<std::size_t>(x));
    if (p != x) p = find(p);
    return p;
  }
  void join(int a, int b) {
    a = find(a);
    b = find(b);
    if (a != b) parent.at(static_cast<std::size_t>(b)) = a;
  }
  std::vector<int> parent;
};

int permute(int vertex, int fixed) {
  if (vertex < fixed) return vertex;
  const int cycle = (vertex - fixed) / 7;
  const int position = (vertex - fixed) % 7;
  return fixed + 7 * cycle + (position + 1) % 7;
}

Clause normalize(Clause clause) {
  std::sort(clause.begin(), clause.end());
  if (std::adjacent_find(clause.begin(), clause.end()) != clause.end()) {
    throw std::runtime_error("repeated literal in clause");
  }
  for (int literal : clause) {
    if (std::binary_search(clause.begin(), clause.end(), -literal)) {
      throw std::runtime_error("tautological clause");
    }
  }
  return clause;
}

void insert(Formula &formula, Clause clause) {
  formula.insert(normalize(std::move(clause)));
}

struct Orbits {
  std::array<std::array<int, n>, n> edge{};
  std::map<int, int> sizes;
  int variable_count = 0;
};

Orbits construct_orbits(int fixed) {
  std::array<std::array<int, n>, n> raw{};
  int edge_count = 0;
  for (int u = 0; u < n; ++u) {
    for (int v = u + 1; v < n; ++v) {
      raw.at(static_cast<std::size_t>(u)).at(static_cast<std::size_t>(v)) = edge_count++;
    }
  }
  if (edge_count != 903) throw std::runtime_error("wrong K43 edge count");
  Dsu dsu(edge_count);
  for (int u = 0; u < n; ++u) {
    for (int v = u + 1; v < n; ++v) {
      int pu = permute(u, fixed), pv = permute(v, fixed);
      if (pu > pv) std::swap(pu, pv);
      dsu.join(raw.at(static_cast<std::size_t>(u)).at(static_cast<std::size_t>(v)),
               raw.at(static_cast<std::size_t>(pu)).at(static_cast<std::size_t>(pv)));
    }
  }
  std::map<int, std::pair<int, int>> least;
  std::map<int, int> sizes;
  for (int u = 0; u < n; ++u) {
    for (int v = u + 1; v < n; ++v) {
      const int root = dsu.find(raw.at(static_cast<std::size_t>(u)).at(static_cast<std::size_t>(v)));
      const std::pair<int, int> candidate{u, v};
      if (!least.contains(root) || candidate < least.at(root)) least[root] = candidate;
      ++sizes[root];
    }
  }
  std::vector<std::pair<int, int>> representatives;
  for (const auto &[root, representative] : least) {
    (void)root;
    representatives.push_back(representative);
  }
  std::sort(representatives.begin(), representatives.end());
  std::map<std::pair<int, int>, int> representative_number;
  for (std::size_t i = 0; i < representatives.size(); ++i) {
    representative_number[representatives.at(i)] = static_cast<int>(i) + 1;
  }
  Orbits result;
  result.variable_count = static_cast<int>(representatives.size());
  for (int u = 0; u < n; ++u) {
    for (int v = u + 1; v < n; ++v) {
      const int root = dsu.find(raw.at(static_cast<std::size_t>(u)).at(static_cast<std::size_t>(v)));
      result.edge.at(static_cast<std::size_t>(u)).at(static_cast<std::size_t>(v)) =
          representative_number.at(least.at(root));
    }
  }
  for (const auto &[root, size] : sizes) {
    (void)root;
    ++result.sizes[size];
  }
  return result;
}

int edge(const Orbits &orbits, int u, int v) {
  if (u > v) std::swap(u, v);
  if (u == v) throw std::runtime_error("loop requested");
  return orbits.edge.at(static_cast<std::size_t>(u)).at(static_cast<std::size_t>(v));
}

Clause block(const std::vector<int> &vars, const std::vector<int> &values) {
  if (vars.size() != values.size()) throw std::runtime_error("bad blocking assignment");
  Clause clause;
  for (std::size_t i = 0; i < vars.size(); ++i) {
    clause.push_back(values.at(i) ? -vars.at(i) : vars.at(i));
  }
  return clause;
}

std::vector<int> binary(int value, int width) {
  std::vector<int> answer;
  for (int bit = width - 1; bit >= 0; --bit) answer.push_back((value >> bit) & 1);
  return answer;
}

bool least_rotation(const std::vector<int> &word) {
  for (std::size_t shift = 1; shift < word.size(); ++shift) {
    std::vector<int> rotated;
    for (std::size_t i = 0; i < word.size(); ++i) {
      rotated.push_back(word.at((i + shift) % word.size()));
    }
    if (rotated < word) return false;
  }
  return true;
}

Formula expected_formula(const Orbits &orbits, int fixed) {
  const int cycles = (n - fixed) / 7;
  Formula expected;
  for (int a = 0; a < n; ++a) {
    for (int b = a + 1; b < n; ++b) {
      for (int c = b + 1; c < n; ++c) {
        for (int d = c + 1; d < n; ++d) {
          for (int e = d + 1; e < n; ++e) {
            const std::array<int, 5> vertex{a, b, c, d, e};
            Clause positive;
            for (int i = 0; i < 5; ++i) {
              for (int j = i + 1; j < 5; ++j) positive.push_back(edge(orbits, vertex.at(i), vertex.at(j)));
            }
            std::sort(positive.begin(), positive.end());
            positive.erase(std::unique(positive.begin(), positive.end()), positive.end());
            insert(expected, positive);
            Clause negative;
            for (int variable : positive) negative.push_back(-variable);
            insert(expected, std::move(negative));
          }
        }
      }
    }
  }

  std::vector<std::vector<int>> cycle_profile(static_cast<std::size_t>(cycles));
  for (int cycle = 0; cycle < cycles; ++cycle) {
    const int base = fixed + 7 * cycle;
    cycle_profile.at(cycle) = {edge(orbits, base, base + 1),
                               edge(orbits, base, base + 2),
                               edge(orbits, base, base + 3)};
  }
  for (int cycle = 0; cycle + 1 < cycles; ++cycle) {
    std::vector<int> vars = cycle_profile.at(cycle);
    vars.insert(vars.end(), cycle_profile.at(cycle + 1).begin(),
                cycle_profile.at(cycle + 1).end());
    for (int left = 0; left < 8; ++left) {
      for (int right = 0; right < 8; ++right) {
        if (left <= right) continue;
        std::vector<int> values = binary(left, 3);
        const auto other = binary(right, 3);
        values.insert(values.end(), other.begin(), other.end());
        insert(expected, block(vars, values));
      }
    }
  }

  std::vector<std::vector<int>> fixed_profile(static_cast<std::size_t>(fixed));
  for (int vertex = 0; vertex < fixed; ++vertex) {
    for (int cycle = 0; cycle < cycles; ++cycle) {
      fixed_profile.at(vertex).push_back(
          edge(orbits, vertex, fixed + 7 * cycle));
    }
  }
  const int fixed_pattern_count = 1 << cycles;
  for (int vertex = 0; vertex + 1 < fixed; ++vertex) {
    std::vector<int> vars = fixed_profile.at(vertex);
    vars.insert(vars.end(), fixed_profile.at(vertex + 1).begin(),
                fixed_profile.at(vertex + 1).end());
    for (int left = 0; left < fixed_pattern_count; ++left) {
      for (int right = 0; right < fixed_pattern_count; ++right) {
        if (left <= right) continue;
        std::vector<int> values = binary(left, cycles);
        const auto other = binary(right, cycles);
        values.insert(values.end(), other.begin(), other.end());
        insert(expected, block(vars, values));
      }
    }
  }

  for (int cycle = 1; cycle < cycles; ++cycle) {
    std::vector<int> vars;
    const int base = fixed + 7 * cycle;
    for (int offset = 0; offset < 7; ++offset) {
      vars.push_back(edge(orbits, fixed, base + offset));
    }
    for (int value = 0; value < 128; ++value) {
      const auto word = binary(value, 7);
      if (!least_rotation(word)) insert(expected, block(vars, word));
    }
  }

  if (fixed == 36) {
    std::vector<int> incidence;
    for (int vertex = 0; vertex < fixed; ++vertex) {
      incidence.push_back(edge(orbits, vertex, fixed));
    }
    std::vector<int> internal;
    for (int distance = 1; distance <= 3; ++distance) {
      internal.push_back(edge(orbits, fixed, fixed + distance));
    }
    for (int value = 0; value < 8; ++value) {
      const std::vector<int> values = binary(value, 3);
      const int selected = std::accumulate(values.begin(), values.end(), 0);
      const int lower = 18 - 2 * selected;
      const int upper = 24 - 2 * selected;
      Clause lower_clause = block(internal, values);
      lower_clause.push_back(incidence.at(static_cast<std::size_t>(fixed - lower)));
      insert(expected, lower_clause);
      Clause upper_clause = block(internal, values);
      upper_clause.push_back(-incidence.at(static_cast<std::size_t>(fixed - upper - 1)));
      insert(expected, upper_clause);
    }
  }
  return expected;
}

Formula read_formula(const std::string &path, int expected_variables, int &declared_clauses) {
  std::ifstream input(path);
  if (!input) throw std::runtime_error("cannot open CNF");
  Formula formula;
  std::string line;
  bool header_seen = false;
  int clause_lines = 0;
  while (std::getline(input, line)) {
    if (line.empty() || line.front() == 'c') continue;
    std::istringstream words(line);
    if (line.front() == 'p') {
      std::string p, cnf;
      int declared_variables = 0;
      words >> p >> cnf >> declared_variables >> declared_clauses;
      if (!words || p != "p" || cnf != "cnf" || declared_variables != expected_variables || header_seen) {
        throw std::runtime_error("invalid DIMACS header");
      }
      header_seen = true;
      continue;
    }
    if (!header_seen) throw std::runtime_error("clause before header");
    Clause clause;
    int literal = 0;
    bool terminated = false;
    while (words >> literal) {
      if (literal == 0) {
        terminated = true;
        break;
      }
      if (literal < -expected_variables || literal > expected_variables) {
        throw std::runtime_error("literal out of range");
      }
      clause.push_back(literal);
    }
    std::string trailing;
    if (!terminated || (words >> trailing)) throw std::runtime_error("invalid clause line");
    if (!formula.insert(normalize(std::move(clause))).second) throw std::runtime_error("duplicate clause");
    ++clause_lines;
  }
  if (!header_seen || clause_lines != declared_clauses) throw std::runtime_error("clause count mismatch");
  return formula;
}

}  // namespace

int main(int argc, char **argv) {
  try {
    if (argc != 3) {
      std::cerr << "usage: verify_formula FIXED FORMULA.cnf\n";
      return 2;
    }
    const int fixed = std::stoi(argv[1]);
    if (fixed != 15 && fixed != 22 && fixed != 29 && fixed != 36) {
      throw std::runtime_error("FIXED must be 15, 22, 29, or 36");
    }
    const int cycles = (n - fixed) / 7;
    const Orbits orbits = construct_orbits(fixed);
    const int singleton_orbits = fixed * (fixed - 1) / 2;
    const int seven_orbits = (903 - singleton_orbits) / 7;
    if (orbits.sizes != std::map<int, int>{{1, singleton_orbits}, {7, seven_orbits}}) {
      throw std::runtime_error("wrong orbit sizes");
    }
    const Formula expected = expected_formula(orbits, fixed);
    int declared_clauses = 0;
    const Formula actual = read_formula(argv[2], orbits.variable_count, declared_clauses);
    if (expected != actual) {
      std::cerr << "formula mismatch: expected=" << expected.size() << " actual=" << actual.size() << "\n";
      return 1;
    }
    std::map<std::size_t, std::size_t> histogram;
    for (const Clause &clause : actual) ++histogram[clause.size()];
    std::cout << "fixed=" << fixed << " cycles=" << cycles
              << " edge_orbits=" << orbits.variable_count << " orbit_sizes=1:"
              << singleton_orbits << ",7:" << seven_orbits << "\n";
    std::cout << "variables=" << orbits.variable_count << " clauses="
              << declared_clauses << "\n";
    std::cout << "clause_lengths";
    for (const auto &[length, count] : histogram) std::cout << " " << length << ":" << count;
    std::cout << "\nformula_verified=true\n";
    return 0;
  } catch (const std::exception &error) {
    std::cerr << "error: " << error.what() << "\n";
    return 1;
  }
}
