#include <algorithm>
#include <array>
#include <chrono>
#include <cstdio>
#include <cstdint>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <limits>
#include <random>
#include <stdexcept>
#include <string>
#include <vector>

#include "cadical.hpp"

namespace {

struct Five {
  std::array<int, 10> edges{};
  std::array<int, 5> vertices{};
};

struct Options {
  int n = 43;
  uint64_t seed = 1;
  int rounds = 100;
  int initial_fives = 2000;
  int max_new = std::numeric_limits<int>::max();
  int root_degree = -1;
  int degree_lo = -1;
  int degree_hi = -1;
  std::string checkpoint;
};

int edge_id(int n, int a, int b) {
  if (a > b) std::swap(a, b);
  if (a == b || a < 0 || b >= n) throw std::runtime_error("invalid edge");
  return 1 + a * (2 * n - a - 1) / 2 + (b - a - 1);
}

std::vector<Five> make_fives(int n) {
  std::vector<Five> result;
  for (int a = 0; a < n; ++a)
    for (int b = a + 1; b < n; ++b)
      for (int c = b + 1; c < n; ++c)
        for (int d = c + 1; d < n; ++d)
          for (int e = d + 1; e < n; ++e) {
            Five f;
            f.vertices = {a, b, c, d, e};
            int k = 0;
            for (int i = 0; i < 5; ++i)
              for (int j = i + 1; j < 5; ++j)
                f.edges[k++] = edge_id(n, f.vertices[i], f.vertices[j]);
            result.push_back(f);
          }
  return result;
}

uint64_t splitmix64(uint64_t &state) {
  uint64_t z = (state += UINT64_C(0x9e3779b97f4a7c15));
  z = (z ^ (z >> 30)) * UINT64_C(0xbf58476d1ce4e5b9);
  z = (z ^ (z >> 27)) * UINT64_C(0x94d049bb133111eb);
  return z ^ (z >> 31);
}

std::string hex_graph(const std::vector<unsigned char> &model, int edges) {
  static constexpr char hex[] = "0123456789abcdef";
  std::string result;
  result.reserve((edges + 3) / 4);
  for (int start = 1; start <= edges; start += 4) {
    int digit = 0;
    for (int k = 0; k < 4 && start + k <= edges; ++k)
      digit |= static_cast<int>(model[start + k]) << k;
    result.push_back(hex[digit]);
  }
  return result;
}

std::vector<unsigned char> decode_hex_graph(const std::string &text, int edges) {
  if (static_cast<int>(text.size()) != (edges + 3) / 4)
    throw std::runtime_error("checkpoint graph has wrong length");
  std::vector<unsigned char> model(edges + 1, 0);
  for (int start = 1, position = 0; start <= edges; start += 4, ++position) {
    const char c = text[position];
    int digit = -1;
    if ('0' <= c && c <= '9') digit = c - '0';
    if ('a' <= c && c <= 'f') digit = c - 'a' + 10;
    if (digit < 0) throw std::runtime_error("checkpoint graph is not hexadecimal");
    for (int k = 0; k < 4 && start + k <= edges; ++k)
      model[start + k] = (digit >> k) & 1;
    if (start + 3 > edges && (digit >> (edges - start + 1)) != 0)
      throw std::runtime_error("checkpoint graph has nonzero padding");
  }
  return model;
}

void add_clause(CaDiCaL::Solver &solver, const Five &five, bool forbid_red) {
  for (int edge : five.edges) solver.add(forbid_red ? -edge : edge);
  solver.add(0);
}

void add_at_most(CaDiCaL::Solver &solver, const std::vector<int> &literals,
                 int cap, int &next_variable) {
  const int count = static_cast<int>(literals.size());
  if (cap < 0) {
    solver.add(0);
    return;
  }
  if (cap >= count) return;
  if (cap == 0) {
    for (int literal : literals) {
      solver.add(-literal);
      solver.add(0);
    }
    return;
  }

  // Sinz sequential counter: s[i][j] means that the first i inputs contain
  // at least j true literals.  Row zero is deliberately unused.
  std::vector<std::vector<int>> s(count, std::vector<int>(cap + 1));
  for (int i = 1; i < count; ++i)
    for (int j = 1; j <= cap; ++j) s[i][j] = next_variable++;

  for (int i = 1; i < count; ++i) {
    solver.add(-literals[i - 1]);
    solver.add(s[i][1]);
    solver.add(0);
  }
  for (int i = 2; i < count; ++i) {
    solver.add(-s[i - 1][1]);
    solver.add(s[i][1]);
    solver.add(0);
    for (int j = 2; j <= cap; ++j) {
      solver.add(-literals[i - 1]);
      solver.add(-s[i - 1][j - 1]);
      solver.add(s[i][j]);
      solver.add(0);
      solver.add(-s[i - 1][j]);
      solver.add(s[i][j]);
      solver.add(0);
    }
  }
  for (int i = 2; i <= count; ++i) {
    solver.add(-literals[i - 1]);
    solver.add(-s[i - 1][cap]);
    solver.add(0);
  }
}

void add_global_filters(CaDiCaL::Solver &solver, const Options &options,
                        int &next_variable) {
  const int n = options.n;
  if (options.root_degree >= 0) {
    for (int v = 1; v < n; ++v) {
      solver.add(v <= options.root_degree ? edge_id(n, 0, v)
                                          : -edge_id(n, 0, v));
      solver.add(0);
    }
  }
  if (options.degree_lo >= 0) {
    for (int v = 0; v < n; ++v) {
      std::vector<int> incident;
      incident.reserve(n - 1);
      for (int w = 0; w < n; ++w)
        if (w != v) incident.push_back(edge_id(n, v, w));
      add_at_most(solver, incident, options.degree_hi, next_variable);
      for (int &literal : incident) literal = -literal;
      add_at_most(solver, incident, n - 1 - options.degree_lo, next_variable);
    }
  }
}

int cardinality_self_test() {
  uint64_t cases = 0;
  for (int count = 1; count <= 7; ++count) {
    for (int cap = 0; cap <= count; ++cap) {
      for (int sign_pattern = 0; sign_pattern < 2; ++sign_pattern) {
        std::vector<int> literals;
        for (int i = 1; i <= count; ++i)
          literals.push_back(sign_pattern && i % 2 == 0 ? -i : i);
        for (int word = 0; word < (1 << count); ++word) {
          CaDiCaL::Solver solver;
          solver.set("quiet", 1);
          int next_variable = count + 1;
          add_at_most(solver, literals, cap, next_variable);
          int true_literals = 0;
          for (int i = 1; i <= count; ++i) {
            const bool value = word & (1 << (i - 1));
            solver.add(value ? i : -i);
            solver.add(0);
            const bool literal_value = sign_pattern && i % 2 == 0 ? !value : value;
            true_literals += literal_value;
          }
          const int status = solver.solve();
          const bool expected = true_literals <= cap;
          if ((status == 10) != expected)
            throw std::runtime_error("cardinality self-test failed");
          ++cases;
        }
      }
    }
  }
  std::cout << "CARDINALITY_SELF_TEST status=PASS cases=" << cases << "\n";
  return 0;
}

Options parse(int argc, char **argv) {
  if (argc < 6 || argc > 10)
    throw std::runtime_error(
        "usage: cegis N SEED ROUNDS INITIAL_FIVES MAX_NEW "
        "[ROOT_DEGREE [DEG_LO DEG_HI [CHECKPOINT]]]");
  Options o;
  o.n = std::stoi(argv[1]);
  o.seed = std::stoull(argv[2]);
  o.rounds = std::stoi(argv[3]);
  o.initial_fives = std::stoi(argv[4]);
  o.max_new = std::stoi(argv[5]);
  if (argc >= 7) o.root_degree = std::stoi(argv[6]);
  if (argc >= 9) {
    o.degree_lo = std::stoi(argv[7]);
    o.degree_hi = std::stoi(argv[8]);
  }
  if (argc == 10) o.checkpoint = argv[9];
  if (o.n < 5 || o.n > 43 || o.rounds <= 0 || o.initial_fives < 0 ||
      o.max_new <= 0 || o.root_degree >= o.n ||
      (o.degree_lo >= 0 && (o.degree_lo > o.degree_hi ||
                            o.degree_hi >= o.n)))
    throw std::runtime_error("invalid parameter");
  return o;
}

struct SavedState {
  bool resumed = false;
  int rounds_completed = 0;
  int clauses_added = 0;
  int best = std::numeric_limits<int>::max();
  int best_red = -1;
  int best_blue = -1;
  int best_edges = -1;
  std::vector<unsigned char> best_model;
  std::vector<uint32_t> learned_codes;
  std::mt19937_64 rng;
};

void write_checkpoint(const Options &o, int rounds_completed, int clauses_added,
                      int best, int best_red, int best_blue, int best_edges,
                      const std::vector<unsigned char> &best_model,
                      const std::vector<uint32_t> &learned_codes,
                      const std::mt19937_64 &rng) {
  if (o.checkpoint.empty()) return;
  const std::string temporary = o.checkpoint + ".tmp";
  std::ofstream out(temporary, std::ios::trunc);
  if (!out) throw std::runtime_error("cannot open checkpoint");
  out << "R55_CEGIS_CHECKPOINT_V1\n"
      << "n " << o.n << "\nseed " << o.seed << "\nrounds_completed "
      << rounds_completed << "\ninitial_fives " << o.initial_fives
      << "\nmax_new " << o.max_new << "\nroot_degree " << o.root_degree
      << "\ndegree_lo " << o.degree_lo << "\ndegree_hi " << o.degree_hi
      << "\nclauses_added " << clauses_added << "\nbest " << best
      << "\nbest_red " << best_red << "\nbest_blue " << best_blue
      << "\nbest_edges " << best_edges << "\nbest_hex "
      << hex_graph(best_model, o.n * (o.n - 1) / 2) << "\nlearned_codes "
      << learned_codes.size() << "\n";
  for (uint32_t code : learned_codes) out << code << '\n';
  out << "rng " << rng << '\n';
  out.close();
  if (!out) throw std::runtime_error("checkpoint write failure");
  if (std::rename(temporary.c_str(), o.checkpoint.c_str()) != 0)
    throw std::runtime_error("checkpoint rename failure");
}

SavedState read_checkpoint(const Options &o, int edges, size_t five_count) {
  SavedState state;
  state.best_model.assign(edges + 1, 0);
  state.rng.seed(o.seed);
  if (o.checkpoint.empty()) return state;
  std::ifstream in(o.checkpoint);
  if (!in) return state;
  state.resumed = true;
  auto read_named = [&](const char *wanted, auto &value) {
    std::string name;
    if (!(in >> name >> value) || name != wanted)
      throw std::runtime_error(std::string("invalid checkpoint field ") + wanted);
  };
  std::string header;
  if (!(in >> header) || header != "R55_CEGIS_CHECKPOINT_V1")
    throw std::runtime_error("invalid checkpoint header");
  int n, root_degree, degree_lo, degree_hi, initial_fives, max_new;
  uint64_t seed;
  read_named("n", n);
  read_named("seed", seed);
  read_named("rounds_completed", state.rounds_completed);
  read_named("initial_fives", initial_fives);
  read_named("max_new", max_new);
  read_named("root_degree", root_degree);
  read_named("degree_lo", degree_lo);
  read_named("degree_hi", degree_hi);
  read_named("clauses_added", state.clauses_added);
  read_named("best", state.best);
  read_named("best_red", state.best_red);
  read_named("best_blue", state.best_blue);
  read_named("best_edges", state.best_edges);
  std::string graph_hex;
  read_named("best_hex", graph_hex);
  size_t learned_count;
  read_named("learned_codes", learned_count);
  if (n != o.n || seed != o.seed || root_degree != o.root_degree ||
      degree_lo != o.degree_lo || degree_hi != o.degree_hi ||
      initial_fives != o.initial_fives || max_new != o.max_new)
    throw std::runtime_error("checkpoint options mismatch");
  if (state.rounds_completed < 0 || state.rounds_completed > o.rounds ||
      learned_count > 2 * five_count)
    throw std::runtime_error("checkpoint count out of range");
  state.best_model = decode_hex_graph(graph_hex, edges);
  state.learned_codes.resize(learned_count);
  for (uint32_t &code : state.learned_codes)
    if (!(in >> code) || code >= 2 * five_count)
      throw std::runtime_error("invalid checkpoint learned code");
  std::string rng_name;
  if (!(in >> rng_name) || rng_name != "rng" || !(in >> state.rng))
    throw std::runtime_error("invalid checkpoint RNG state");
  std::string extra;
  if (in >> extra) throw std::runtime_error("trailing checkpoint data");
  const size_t expected_clauses =
      2 * std::min<size_t>(o.initial_fives, five_count) +
      state.learned_codes.size();
  if (static_cast<size_t>(state.clauses_added) != expected_clauses)
    throw std::runtime_error("checkpoint clause count mismatch");
  return state;
}

}  // namespace

int main(int argc, char **argv) {
  try {
    if (argc == 2 && std::string(argv[1]) == "--cardinality-self-test")
      return cardinality_self_test();
    const Options options = parse(argc, argv);
    const int edges = options.n * (options.n - 1) / 2;
    const std::vector<Five> fives = make_fives(options.n);
    std::vector<size_t> order(fives.size());
    for (size_t i = 0; i < order.size(); ++i) order[i] = i;
    std::mt19937_64 initial_rng(options.seed);
    std::shuffle(order.begin(), order.end(), initial_rng);

    CaDiCaL::Solver solver;
    solver.set("quiet", 1);
    solver.set("seed", static_cast<int>(options.seed % 2000000000ULL));
    solver.reserve(edges);
    int next_variable = edges + 1;
    uint64_t phase_state = options.seed;
    for (int edge = 1; edge <= edges; ++edge)
      solver.phase((splitmix64(phase_state) & 1) ? edge : -edge);
    add_global_filters(solver, options, next_variable);

    std::vector<unsigned char> seen(2 * fives.size(), 0);
    int clauses_added = 0;
    const int initial = std::min<int>(options.initial_fives, fives.size());
    for (int i = 0; i < initial; ++i) {
      const size_t index = order[i];
      add_clause(solver, fives[index], false);
      add_clause(solver, fives[index], true);
      seen[2 * index] = seen[2 * index + 1] = 1;
      clauses_added += 2;
    }

    SavedState saved = read_checkpoint(options, edges, fives.size());
    if (saved.resumed) {
      clauses_added = saved.clauses_added;
      for (uint32_t code : saved.learned_codes) {
        if (seen[code]) throw std::runtime_error("duplicate checkpoint clause");
        add_clause(solver, fives[code / 2], code & 1U);
        seen[code] = 1;
      }
      if (saved.best != std::numeric_limits<int>::max())
        for (int edge = 1; edge <= edges; ++edge)
          solver.phase(saved.best_model[edge] ? edge : -edge);
    }
    std::mt19937_64 rng = saved.rng;
    std::vector<unsigned char> model(edges + 1, 0);
    std::vector<unsigned char> best_model = saved.best_model;
    std::vector<uint32_t> learned_codes = saved.learned_codes;
    int best = saved.best;
    int best_red = saved.best_red, best_blue = saved.best_blue;
    int best_edges = saved.best_edges;
    const auto started = std::chrono::steady_clock::now();

    for (int round = saved.rounds_completed; round < options.rounds; ++round) {
      const int solver_status = solver.solve();
      if (solver_status == 20) {
        write_checkpoint(options, round, clauses_added, best, best_red,
                         best_blue, best_edges, best_model, learned_codes, rng);
        std::cout << "RESULT status=UNSAT_SUBFORMULA n=" << options.n
                  << " root_degree=" << options.root_degree
                  << " rounds=" << round << " clauses_added=" << clauses_added
                  << "\n";
        return 0;
      }
      if (solver_status != 10)
        throw std::runtime_error("SAT solver returned UNKNOWN");

      int red_edges = 0;
      for (int edge = 1; edge <= edges; ++edge) {
        model[edge] = solver.val(edge) > 0;
        red_edges += model[edge];
      }

      std::vector<uint32_t> violations;
      violations.reserve(4096);
      int red_bad = 0, blue_bad = 0;
      for (size_t index = 0; index < fives.size(); ++index) {
        int reds = 0;
        for (int edge : fives[index].edges) reds += model[edge];
        if (reds == 0) {
          violations.push_back(static_cast<uint32_t>(2 * index));
          ++blue_bad;
        } else if (reds == 10) {
          violations.push_back(static_cast<uint32_t>(2 * index + 1));
          ++red_bad;
        }
      }

      const bool improved = static_cast<int>(violations.size()) < best;
      if (improved) {
        best = static_cast<int>(violations.size());
        best_red = red_bad;
        best_blue = blue_bad;
        best_edges = red_edges;
        best_model = model;
      }
      if (improved || round % 100 == 0) {
        const double seconds = std::chrono::duration<double>(
            std::chrono::steady_clock::now() - started).count();
        std::cout << "ROUND round=" << round << " violations="
                  << violations.size() << " red=" << red_bad
                  << " blue=" << blue_bad << " red_edges=" << red_edges
                  << " clauses_added=" << clauses_added << " best=" << best
                  << " elapsed=" << std::fixed << std::setprecision(6)
                  << seconds << "\n";
        std::cout.flush();
      }

      if (violations.empty()) {
        write_checkpoint(options, round + 1, clauses_added, 0, 0, 0,
                         red_edges, model, learned_codes, rng);
        std::cout << "RESULT status=GOOD_GRAPH n=" << options.n
                  << " root_degree=" << options.root_degree
                  << " rounds=" << round + 1 << " clauses_added="
                  << clauses_added << " red_edges=" << red_edges
                  << " red_bits_hex=" << hex_graph(model, edges) << "\n";
        return 0;
      }

      for (int edge = 1; edge <= edges; ++edge)
        solver.phase(model[edge] ? edge : -edge);
      std::shuffle(violations.begin(), violations.end(), rng);
      const int take = std::min<int>(options.max_new, violations.size());
      for (int i = 0; i < take; ++i) {
        const uint32_t code = violations[i];
        if (seen[code])
          throw std::runtime_error("solver model violates an existing clause");
        const size_t index = code / 2;
        const bool forbid_red = code & 1U;
        add_clause(solver, fives[index], forbid_red);
        seen[code] = 1;
        learned_codes.push_back(code);
        ++clauses_added;
      }
      write_checkpoint(options, round + 1, clauses_added, best, best_red,
                       best_blue, best_edges, best_model, learned_codes, rng);
    }

    std::cout << "RESULT status=INCOMPLETE n=" << options.n
              << " root_degree=" << options.root_degree
              << " rounds=" << options.rounds << " clauses_added="
              << clauses_added << " best=" << best << " best_red="
              << best_red << " best_blue=" << best_blue << " best_edges="
              << best_edges << " best_hex=" << hex_graph(best_model, edges)
              << "\n";
    return 0;
  } catch (const std::exception &error) {
    std::cerr << "ERROR " << error.what() << "\n";
    return 2;
  }
}
