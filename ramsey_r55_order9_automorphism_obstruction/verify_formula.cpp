// Reuse the earlier independent DSU orbit and five-set reconstruction.
// The Python generator uses least images under all powers instead.
#define main partial_order9_verifier_main
#include "../ramsey_r55_order9_partial_automorphism_obstruction/verify_formula.cpp"
#undef main

namespace {

Clause forbid(const std::vector<int> &variables, unsigned int word) {
  Clause result;
  for (std::size_t i = 0; i < variables.size(); ++i) {
    const auto shift = static_cast<unsigned int>(variables.size() - 1 - i);
    result.push_back(((word >> shift) & 1U) ? -variables[i] : variables[i]);
  }
  std::sort(result.begin(), result.end());
  return result;
}

void centralizer_constraints(Formula &formula, const Orbits &orbits,
                             const std::array<int, 3> &counts) {
  const auto &v = orbits.variable;
  // Compare the numeric values of equal-width binary internal profiles.
  for (int kind = 0; kind < 2; ++kind) {
    const int length = kind == 0 ? 9 : 3;
    const int width = (length - 1) / 2;
    const int start = kind == 0 ? 0 : 9 * counts[0];
    for (int c = 0; c + 1 < counts[static_cast<std::size_t>(kind)]; ++c) {
      std::vector<int> variables;
      for (int offset : {c, c + 1}) {
        const int vertex = start + length * offset;
        for (int distance = 1; distance <= width; ++distance) {
          variables.push_back(v.at(static_cast<std::size_t>(vertex))
                               .at(static_cast<std::size_t>(vertex + distance)));
        }
      }
      const unsigned int limit = 1U << static_cast<unsigned int>(width);
      for (unsigned int left = 0; left < limit; ++left) {
        for (unsigned int right = 0; right < left; ++right) {
          formula.insert(forbid(variables, left * limit + right));
        }
      }
    }
  }
  // Enumerate cyclic binary words with integer rotations, independent of
  // Python's tuple slices. The maximum width is nine, so shifts fit uint.
  for (int kind = 0; kind < 2; ++kind) {
    const int length = kind == 0 ? 9 : 3;
    const int start = kind == 0 ? 0 : 9 * counts[0];
    for (int c = (kind == 0 ? 1 : 0); c < counts[static_cast<std::size_t>(kind)]; ++c) {
      std::vector<int> variables;
      for (int offset = 0; offset < length; ++offset) {
        variables.push_back(v[0].at(static_cast<std::size_t>(start + c * length + offset)));
      }
      const unsigned int limit = 1U << static_cast<unsigned int>(length);
      for (unsigned int word = 0; word < limit; ++word) {
        unsigned int rotated = word;
        bool rejected = false;
        for (int step = 1; step < length; ++step) {
          rotated = ((rotated << 1U) & (limit - 1U)) |
                    (rotated >> static_cast<unsigned int>(length - 1));
          rejected = rejected || rotated < word;
        }
        if (rejected) formula.insert(forbid(variables, word));
      }
    }
  }
}

Formula read_normalized(const std::string &path, int expected_variables,
                        int &declared) {
  std::ifstream in(path);
  if (!in) throw std::runtime_error("cannot open formula");
  std::string line;
  bool header = false;
  int parsed = 0;
  Formula result;
  while (std::getline(in, line)) {
    if (line.empty() || line.front() == 'c') continue;
    std::istringstream row(line);
    if (line.front() == 'p') {
      int variables;
      std::string p, cnf, extra;
      if (header || !(row >> p >> cnf >> variables >> declared) ||
          p != "p" || cnf != "cnf" || variables != expected_variables ||
          declared < 0 || (row >> extra)) {
        throw std::runtime_error("bad header");
      }
      header = true;
      continue;
    }
    if (!header) throw std::runtime_error("clause before header");
    Clause clause;
    int literal;
    bool end = false;
    while (row >> literal) {
      if (literal == 0) { end = true; break; }
      if (literal < -expected_variables || literal > expected_variables) {
        throw std::runtime_error("literal out of bounds");
      }
      clause.push_back(literal);
    }
    std::string extra;
    if (!end || clause.empty() || (row >> extra)) {
      throw std::runtime_error("bad clause");
    }
    std::sort(clause.begin(), clause.end());
    if (std::adjacent_find(clause.begin(), clause.end()) != clause.end()) {
      throw std::runtime_error("repeated literal");
    }
    for (int lit : clause) {
      if (std::binary_search(clause.begin(), clause.end(), -lit)) {
        throw std::runtime_error("tautological clause");
      }
    }
    if (!result.insert(clause).second) throw std::runtime_error("duplicate clause");
    ++parsed;
  }
  if (!header || parsed != declared) throw std::runtime_error("count mismatch");
  return result;
}
}  // namespace

int main(int argc, char **argv) {
  try {
    if (argc != 3) throw std::runtime_error("usage: verify_formula CASE FORMULA.cnf");
    const int index = std::stoi(argv[1]);
    if (index < 0 || index > 1) throw std::runtime_error("case must be 0 or 1");
    const std::array<int, 3> counts = index == 0 ? std::array<int, 3>{3, 5, 1}
                                               : std::array<int, 3>{4, 2, 1};
    const Orbits orbits = construct_orbits(counts);
    int variables = orbits.variables;
    Formula expected = expected_formula(orbits, counts, false, variables);
    const auto base_count = expected.size();
    centralizer_constraints(expected, orbits, counts);
    int declared = 0;
    const Formula actual = read_normalized(argv[2], variables, declared);
    if (actual != expected) throw std::runtime_error("formula clause set differs");
    std::cout << "PASS case=" << index << " variables=" << variables
              << " clauses=" << declared << " symmetry_clauses="
              << expected.size() - base_count << " formula_verified=true\n";
  } catch (const std::exception &e) {
    std::cerr << "ERROR: " << e.what() << '\n';
    return 1;
  }
}
