#include "cadical.hpp"

#include <algorithm>
#include <array>
#include <bit>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <set>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

namespace {

constexpr int N = 43;
constexpr int L = 21;
constexpr int RECORDS = 2178;
constexpr int RECORD_BITS = N * (N - 1) / 2;
constexpr std::uint64_t SELECTOR_CLAUSES_PER_ROOT = 1 + L * (L - 1);

using Tournament = std::array<std::uint64_t, N>;

struct SourceRow {
  std::uint64_t clauses = 0;
  std::uint64_t proof_bytes = 0;
};

struct RootResult {
  std::uint64_t base_clauses = 0;
  std::uint64_t unsat_branches = 0;
};

void need(bool condition, const std::string &message) {
  if (!condition) throw std::runtime_error(message);
}

int pair_variable(int first, int second) {
  if (first > second) std::swap(first, second);
  return 1 + first * (2 * L - first - 1) / 2 + second - first - 1;
}

int before(int first, int second) {
  return first < second ? pair_variable(first, second)
                        : -pair_variable(second, first);
}

template <std::size_t Size>
void add_clause(CaDiCaL::Solver &solver, const std::array<int, Size> &clause,
                std::uint64_t &count) {
  for (int literal : clause) solver.add(literal);
  solver.add(0);
  ++count;
}

Tournament decode(const std::string &record) {
  need(record.size() == RECORD_BITS, "catalog record length");
  Tournament tournament{};
  std::size_t offset = 0;
  for (int first = 0; first < N; ++first) {
    for (int second = first + 1; second < N; ++second) {
      const char bit = record[offset++];
      need(bit == '0' || bit == '1', "non-bit catalog character");
      if (bit == '1') tournament[first] |= std::uint64_t{1} << second;
      else tournament[second] |= std::uint64_t{1} << first;
    }
  }
  return tournament;
}

void check_drt(const Tournament &tournament) {
  for (int first = 0; first < N; ++first) {
    need(((tournament[first] >> first) & 1) == 0, "tournament loop");
    need(std::popcount(tournament[first]) == 21, "nonregular tournament");
    for (int second = first + 1; second < N; ++second) {
      const int forward = (tournament[first] >> second) & 1;
      const int backward = (tournament[second] >> first) & 1;
      need(forward + backward == 1, "pair orientation");
      need(std::popcount(tournament[first] & tournament[second]) == 10,
           "wrong common-outneighbor count");
    }
  }
}

std::vector<SourceRow> read_source_result(const std::string &path) {
  std::ifstream input(path);
  need(static_cast<bool>(input), "cannot read source result");
  std::string line;
  need(static_cast<bool>(std::getline(input, line)) &&
           line == "record\troots\tunsat\tclauses\tproof_bytes",
       "source result header");
  std::vector<SourceRow> rows;
  std::uint64_t total_roots = 0, total_unsat = 0;
  std::uint64_t total_clauses = 0, total_proof_bytes = 0;
  while (std::getline(input, line)) {
    std::istringstream fields(line);
    std::string first;
    fields >> first;
    if (first == "TOTAL") {
      std::uint64_t roots = 0, unsat = 0, clauses = 0, proof_bytes = 0;
      need(static_cast<bool>(fields >> roots >> unsat >> clauses >> proof_bytes),
           "source total fields");
      need(!(fields >> first), "source total trailing field");
      need(roots == total_roots && unsat == total_unsat &&
               clauses == total_clauses && proof_bytes == total_proof_bytes,
           "source total mismatch");
      need(rows.size() == RECORDS, "source result record count");
      return rows;
    }
    int record = -1, roots = -1, unsat = -1;
    std::uint64_t clauses = 0, proof_bytes = 0;
    try {
      record = std::stoi(first);
    } catch (...) {
      throw std::runtime_error("source record field");
    }
    need(static_cast<bool>(fields >> roots >> unsat >> clauses >> proof_bytes),
         "source row fields");
    need(!(fields >> first), "source row trailing field");
    need(record == static_cast<int>(rows.size()) && roots == N && unsat == N,
         "source row coverage or status");
    rows.push_back({clauses, proof_bytes});
    total_roots += roots;
    total_unsat += unsat;
    total_clauses += clauses;
    total_proof_bytes += proof_bytes;
  }
  throw std::runtime_error("source result lacks total");
}

bool arc(const std::array<std::uint32_t, L> &out, int first, int second) {
  return (out[first] >> second) & 1U;
}

template <std::size_t Size>
std::array<int, Size> tournament_order(
    const std::array<std::uint32_t, L> &out,
    const std::array<int, Size> &vertices) {
  std::array<int, Size> degree{};
  for (std::size_t i = 0; i < Size; ++i) {
    for (std::size_t j = 0; j < Size; ++j) {
      if (i != j) degree[i] += arc(out, vertices[i], vertices[j]);
    }
  }
  auto sorted = degree;
  std::sort(sorted.begin(), sorted.end());
  for (std::size_t i = 0; i < Size; ++i) {
    if (sorted[i] != static_cast<int>(i)) return {};
  }
  std::array<int, Size> indices{};
  for (std::size_t i = 0; i < Size; ++i) indices[i] = static_cast<int>(i);
  std::sort(indices.begin(), indices.end(), [&](int first, int second) {
    return degree[first] > degree[second];
  });
  std::array<int, Size> order{};
  for (std::size_t i = 0; i < Size; ++i) order[i] = vertices[indices[i]];
  return order;
}

bool is_zero_order(const std::array<int, 4> &order) {
  return std::all_of(order.begin(), order.end(), [](int value) {
    return value == 0;
  });
}

bool is_zero_order(const std::array<int, 5> &order) {
  return std::all_of(order.begin(), order.end(), [](int value) {
    return value == 0;
  });
}

void validate_counterexample(const std::array<std::uint32_t, L> &out,
                             CaDiCaL::Solver &solver, int assumed_first) {
  std::array<int, L> order{};
  for (int vertex = 0; vertex < L; ++vertex) order[vertex] = vertex;
  std::sort(order.begin(), order.end(), [&](int first, int second) {
    return solver.val(before(first, second)) > 0;
  });
  need(order[0] == assumed_first, "SAT model violates first branch");
  for (int a = 0; a < L; ++a) for (int b = a + 1; b < L; ++b)
    for (int c = b + 1; c < L; ++c) for (int d = c + 1; d < L; ++d) {
      const std::array<int,4> positions{a,b,c,d};
      bool red = true;
      for (int i = 0; i < 4; ++i) for (int j = i + 1; j < 4; ++j)
        red = red && arc(out, order[positions[i]], order[positions[j]]);
      need(!red, "SAT model contains forward transitive four-set");
    }
  for (int a = 0; a < L; ++a) for (int b = a + 1; b < L; ++b)
    for (int c = b + 1; c < L; ++c) for (int d = c + 1; d < L; ++d)
      for (int e = d + 1; e < L; ++e) {
        const std::array<int,5> positions{a,b,c,d,e};
        bool blue = true;
        for (int i = 0; i < 5; ++i) for (int j = i + 1; j < 5; ++j)
          blue = blue && arc(out, order[positions[j]], order[positions[i]]);
        need(!blue, "SAT model contains backward transitive five-set");
      }
}

RootResult solve_root(const Tournament &tournament, int root) {
  std::array<int, L> global{};
  int count = 0;
  for (int vertex = 0; vertex < N; ++vertex) {
    if ((tournament[root] >> vertex) & 1) global[count++] = vertex;
  }
  need(count == L, "root outneighborhood size");
  std::array<std::uint32_t, L> out{};
  for (int first = 0; first < L; ++first) {
    for (int second = 0; second < L; ++second) {
      if ((tournament[global[first]] >> global[second]) & 1)
        out[first] |= std::uint32_t{1} << second;
    }
    need(std::popcount(out[first]) == 10, "local tournament is not regular");
  }

  CaDiCaL::Solver solver;
  need(solver.set("quiet", 1), "cannot set quiet solver option");
  std::uint64_t clauses = 0;
  for (int first = 0; first < L; ++first) {
    for (int second = first + 1; second < L; ++second) {
      for (int third = second + 1; third < L; ++third) {
        add_clause(solver,
                   std::array<int,3>{-before(first, second),
                                     -before(second, third),
                                      before(first, third)}, clauses);
        add_clause(solver,
                   std::array<int,3>{ before(first, second),
                                      before(second, third),
                                     -before(first, third)}, clauses);
      }
    }
  }
  for (int a = 0; a < L; ++a) for (int b = a + 1; b < L; ++b)
    for (int c = b + 1; c < L; ++c) for (int d = c + 1; d < L; ++d) {
      const auto order = tournament_order(out, std::array<int,4>{a,b,c,d});
      if (is_zero_order(order)) continue;
      add_clause(solver,
                 std::array<int,3>{-before(order[0], order[1]),
                                   -before(order[1], order[2]),
                                   -before(order[2], order[3])}, clauses);
    }
  for (int a = 0; a < L; ++a) for (int b = a + 1; b < L; ++b)
    for (int c = b + 1; c < L; ++c) for (int d = c + 1; d < L; ++d)
      for (int e = d + 1; e < L; ++e) {
        const auto order = tournament_order(out, std::array<int,5>{a,b,c,d,e});
        if (is_zero_order(order)) continue;
        add_clause(solver,
                   std::array<int,4>{-before(order[4], order[3]),
                                     -before(order[3], order[2]),
                                     -before(order[2], order[1]),
                                     -before(order[1], order[0])}, clauses);
      }

  std::uint64_t unsat = 0;
  for (int first = 0; first < L; ++first) {
    for (int other = 0; other < L; ++other) {
      if (other != first) solver.assume(before(first, other));
    }
    need(solver.limit("conflicts", 100000), "cannot set solver conflict limit");
    const int status = solver.solve();
    if (status == 10) {
      validate_counterexample(out, solver, first);
      throw std::runtime_error("SAT counterexample found at root " +
                               std::to_string(root));
    }
    need(status == 20, "solver returned UNKNOWN");
    ++unsat;
  }
  return {clauses, unsat};
}

}  // namespace

int main(int argc, char **argv) try {
  need(argc == 4 || argc == 5,
       "usage: independent_check CATALOG SOURCE_RESULT OUTPUT [RECORD_LIMIT]");
  const int record_limit = argc == 5 ? std::stoi(argv[4]) : RECORDS;
  need(record_limit >= 1 && record_limit <= RECORDS, "record limit range");
  const auto source = read_source_result(argv[2]);
  std::ifstream input(argv[1]);
  need(static_cast<bool>(input), "cannot read catalog");
  std::vector<std::string> records;
  std::string record;
  while (input >> record) records.push_back(record);
  need(records.size() == RECORDS, "catalog record count");
  need(std::set<std::string>(records.begin(), records.end()).size() == RECORDS,
       "duplicate catalog record");
  std::ofstream output(argv[3]);
  need(static_cast<bool>(output), "cannot create output");
  output << "record\troots\tbranches_unsat\tbase_clauses\tsource_clauses"
            "\tsource_reported_proof_bytes\n";
  std::uint64_t total_roots = 0, total_branches = 0;
  std::uint64_t total_base = 0, total_source = 0, total_proof = 0;
  for (int index = 0; index < record_limit; ++index) {
    const Tournament tournament = decode(records[index]);
    check_drt(tournament);
    std::uint64_t record_base = 0, record_branches = 0;
    for (int root = 0; root < N; ++root) {
      const RootResult result = solve_root(tournament, root);
      record_base += result.base_clauses;
      record_branches += result.unsat_branches;
    }
    const std::uint64_t reconstructed_source =
        record_base + N * SELECTOR_CLAUSES_PER_ROOT;
    need(record_branches == static_cast<std::uint64_t>(N * L),
         "incomplete first-position coverage");
    need(reconstructed_source == source[index].clauses,
         "per-record source clause-count mismatch");
    output << index << '\t' << N << '\t' << record_branches << '\t'
           << record_base << '\t' << reconstructed_source << '\t'
           << source[index].proof_bytes << '\n';
    output.flush();
    total_roots += N;
    total_branches += record_branches;
    total_base += record_base;
    total_source += reconstructed_source;
    total_proof += source[index].proof_bytes;
    std::cerr << "record " << index << " roots " << total_roots
              << " branches " << total_branches << '\n';
  }
  output << "TOTAL\t" << total_roots << '\t' << total_branches << '\t'
         << total_base << '\t' << total_source << '\t' << total_proof << '\n';
  output.close();
  need(static_cast<bool>(output), "failed writing output");
  if (record_limit == RECORDS) {
    need(total_roots == 93654 && total_branches == 1966734,
         "global coverage mismatch");
    need(total_source == 548087198 && total_proof == 2482356972,
         "source totals mismatch");
  }
  std::cout << (record_limit == RECORDS
                    ? "INDEPENDENTLY_EXCLUDED_DRT43_CATALOG_ORDERS "
                    : "PARTIAL_DRT43_CATALOG_CHECK ")
            << "records=" << record_limit << " roots=" << total_roots
            << " first_branches=" << total_branches
            << " base_clauses=" << total_base
            << " source_clauses=" << total_source << '\n';
  return 0;
} catch (const std::exception &error) {
  std::cerr << "error: " << error.what() << '\n';
  return 1;
}
