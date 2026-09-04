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
constexpr int variables = 129;
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

int permute(int vertex) {
  if (vertex == 0) return 0;
  const int cycle = (vertex - 1) / 7;
  const int position = (vertex - 1) % 7;
  return 1 + 7 * cycle + (position + 1) % 7;
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
};

Orbits construct_orbits() {
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
      int pu = permute(u), pv = permute(v);
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
  if (representatives.size() != variables) throw std::runtime_error("wrong edge-orbit count");
  std::map<std::pair<int, int>, int> representative_number;
  for (std::size_t i = 0; i < representatives.size(); ++i) {
    representative_number[representatives.at(i)] = static_cast<int>(i) + 1;
  }
  Orbits result;
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

Formula expected_formula(const Orbits &orbits) {
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

  std::array<int, 6> fixed{};
  for (int cycle = 0; cycle < 6; ++cycle) fixed.at(cycle) = edge(orbits, 0, 1 + 7 * cycle);
  for (int a = 0; a < 6; ++a) {
    for (int b = a + 1; b < 6; ++b) {
      for (int c = b + 1; c < 6; ++c) {
        for (int d = c + 1; d < 6; ++d) {
          Clause positive{fixed.at(a), fixed.at(b), fixed.at(c), fixed.at(d)};
          insert(expected, positive);
          for (int &literal : positive) literal = -literal;
          insert(expected, positive);
        }
      }
    }
  }

  std::array<std::vector<int>, 6> profile;
  for (int cycle = 0; cycle < 6; ++cycle) {
    const int base = 1 + 7 * cycle;
    profile.at(cycle) = {edge(orbits, 0, base), edge(orbits, base, base + 1),
                         edge(orbits, base, base + 2), edge(orbits, base, base + 3)};
  }
  for (int cycle = 0; cycle < 5; ++cycle) {
    std::vector<int> vars = profile.at(cycle);
    vars.insert(vars.end(), profile.at(cycle + 1).begin(), profile.at(cycle + 1).end());
    for (int left = 0; left < 16; ++left) {
      for (int right = 0; right < 16; ++right) {
        if (left <= right) continue;
        std::vector<int> values = binary(left, 4);
        const auto other = binary(right, 4);
        values.insert(values.end(), other.begin(), other.end());
        insert(expected, block(vars, values));
      }
    }
  }

  for (int cycle = 1; cycle < 6; ++cycle) {
    std::vector<int> vars;
    const int base = 1 + 7 * cycle;
    for (int offset = 0; offset < 7; ++offset) vars.push_back(edge(orbits, 1, base + offset));
    for (int value = 0; value < 128; ++value) {
      const auto word = binary(value, 7);
      if (!least_rotation(word)) insert(expected, block(vars, word));
    }
  }
  return expected;
}

Formula read_formula(const std::string &path, int &declared_clauses) {
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
      if (!words || p != "p" || cnf != "cnf" || declared_variables != variables || header_seen) {
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
      if (literal < -variables || literal > variables) throw std::runtime_error("literal out of range");
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
    if (argc != 2) {
      std::cerr << "usage: verify_formula FORMULA.cnf\n";
      return 2;
    }
    const Orbits orbits = construct_orbits();
    if (orbits.sizes != std::map<int, int>{{7, 129}}) throw std::runtime_error("wrong orbit sizes");
    const Formula expected = expected_formula(orbits);
    int declared_clauses = 0;
    const Formula actual = read_formula(argv[1], declared_clauses);
    if (expected != actual) {
      std::cerr << "formula mismatch: expected=" << expected.size() << " actual=" << actual.size() << "\n";
      return 1;
    }
    std::map<std::size_t, std::size_t> histogram;
    for (const Clause &clause : actual) ++histogram[clause.size()];
    std::cout << "vertices=43 edges=903 edge_orbits=129 orbit_size=7\n";
    std::cout << "variables=129 clauses=" << declared_clauses << "\n";
    std::cout << "clause_lengths";
    for (const auto &[length, count] : histogram) std::cout << " " << length << ":" << count;
    std::cout << "\nformula_verified=true\n";
    return 0;
  } catch (const std::exception &error) {
    std::cerr << "error: " << error.what() << "\n";
    return 1;
  }
}
