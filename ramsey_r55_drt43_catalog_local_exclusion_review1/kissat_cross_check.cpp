extern "C" {
#include "kissat.h"
}
#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <numeric>
#include <string>
#include <vector>

constexpr int N = 43;
constexpr int L = 21;

int pair_var(int a, int b) {
  if (a > b) std::swap(a, b);
  return 1 + a * (2 * L - a - 1) / 2 + b - a - 1;
}

int before(int a, int b) {
  return a < b ? pair_var(a, b) : -pair_var(b, a);
}

void clause(kissat *solver, std::initializer_list<int> literals,
            std::uint64_t &count) {
  for (int literal : literals) kissat_add(solver, literal);
  kissat_add(solver, 0);
  ++count;
}

int solve(const std::array<std::uint64_t, N> &out, int root,
          std::uint64_t &clause_count) {
  std::array<int, L> q{};
  int qn = 0;
  for (int vertex = 0; vertex < N; ++vertex)
    if ((out[root] >> vertex) & 1) q[qn++] = vertex;
  if (qn != L) return -1;
  kissat *solver = kissat_init();
  kissat_set_option(solver, "quiet", 1);
  clause_count = 0;
  for (int a = 0; a < L; ++a) for (int b = a + 1; b < L; ++b)
    for (int c = b + 1; c < L; ++c) {
      clause(solver, {-before(a,b), -before(b,c), before(a,c)}, clause_count);
      clause(solver, {before(a,b), before(b,c), -before(a,c)}, clause_count);
    }
  for (int a = 0; a < L; ++a) for (int b = a + 1; b < L; ++b)
    for (int c = b + 1; c < L; ++c) for (int d = c + 1; d < L; ++d) {
      std::array<int, 4> vertices{a,b,c,d};
      std::array<int, 4> degree{};
      for (int i = 0; i < 4; ++i) for (int j = 0; j < 4; ++j)
        if (i != j) degree[i] += (out[q[vertices[i]]] >> q[vertices[j]]) & 1;
      auto sorted = degree;
      std::sort(sorted.begin(), sorted.end());
      if (sorted != std::array<int,4>{0,1,2,3}) continue;
      std::array<int,4> order{0,1,2,3};
      std::sort(order.begin(), order.end(), [&](int i, int j) { return degree[i] > degree[j]; });
      clause(solver, {-before(vertices[order[0]], vertices[order[1]]),
                      -before(vertices[order[1]], vertices[order[2]]),
                      -before(vertices[order[2]], vertices[order[3]])}, clause_count);
    }
  for (int a = 0; a < L; ++a) for (int b = a + 1; b < L; ++b)
    for (int c = b + 1; c < L; ++c) for (int d = c + 1; d < L; ++d)
      for (int e = d + 1; e < L; ++e) {
        std::array<int,5> vertices{a,b,c,d,e};
        std::array<int,5> degree{};
        for (int i = 0; i < 5; ++i) for (int j = 0; j < 5; ++j)
          if (i != j) degree[i] += (out[q[vertices[i]]] >> q[vertices[j]]) & 1;
        auto sorted = degree;
        std::sort(sorted.begin(), sorted.end());
        if (sorted != std::array<int,5>{0,1,2,3,4}) continue;
        std::array<int,5> order{0,1,2,3,4};
        std::sort(order.begin(), order.end(), [&](int i, int j) { return degree[i] > degree[j]; });
        clause(solver, {-before(vertices[order[1]], vertices[order[0]]),
                        -before(vertices[order[2]], vertices[order[1]]),
                        -before(vertices[order[3]], vertices[order[2]]),
                        -before(vertices[order[4]], vertices[order[3]])}, clause_count);
      }
  int status = kissat_solve(solver);
  kissat_release(solver);
  return status;
}

int main(int argc, char **argv) {
  if (argc != 5 && argc != 6) return 2;
  std::ifstream input(argv[1]);
  std::vector<std::string> lines;
  std::string line;
  while (input >> line) lines.push_back(line);
  int first_record = std::stoi(argv[2]);
  int record_count = std::stoi(argv[3]);
  int roots = std::stoi(argv[4]);
  int first_root = argc == 6 ? std::stoi(argv[5]) : 0;
  std::uint64_t tested = 0, unsat = 0, sat = 0, total_clauses = 0;
  for (int record = first_record; record < first_record + record_count; ++record) {
    std::array<std::uint64_t, N> out{};
    std::size_t offset = 0;
    for (int u = 0; u < N; ++u) for (int v = u + 1; v < N; ++v) {
      if (lines[record][offset++] == '1') out[u] |= std::uint64_t{1} << v;
      else out[v] |= std::uint64_t{1} << u;
    }
    for (int root = first_root; root < first_root + roots; ++root) {
      std::uint64_t clauses = 0;
      int status = solve(out, root, clauses);
      ++tested; total_clauses += clauses;
      if (status == 20) ++unsat;
      else if (status == 10) ++sat;
      else { std::cerr << "UNKNOWN " << record << ' ' << root << ' ' << status << '\n'; return 3; }
    }
    std::cerr << "record " << record << " tested " << tested << " unsat " << unsat << " sat " << sat << '\n';
  }
  std::cout << "FINAL " << tested << ' ' << unsat << ' ' << sat << ' ' << total_clauses << '\n';
}
