#include <algorithm>
#include <array>
#include <atomic>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <mutex>
#include <stdexcept>
#include <string>
#include <thread>
#include <vector>

// Red is one and blue is zero throughout.
constexpr int N = 43;
constexpr int M = 903;

struct Five {
  std::array<std::uint8_t, 5> vertices{};
  std::array<std::uint16_t, 10> edges{};
};

struct Input {
  std::array<std::array<int, N>, N> edge_id{};
  std::array<std::uint8_t, M> base{};
  std::vector<std::vector<int>> rows;
  std::vector<Five> fives;

  explicit Input(const std::string &path) {
    int next_edge = 0;
    std::array<int, 11> lengths{1, 2, 7, 10, 12, 13, 14, 16, 18, 20, 21};
    for (int u = 0; u < N; ++u) {
      for (int v = u + 1; v < N; ++v) {
        edge_id[u][v] = edge_id[v][u] = next_edge;
        int distance = std::min(v - u, N - v + u);
        base[next_edge] = static_cast<std::uint8_t>(
            std::find(lengths.begin(), lengths.end(), distance) != lengths.end());
        ++next_edge;
      }
    }
    if (next_edge != M) throw std::runtime_error("edge count");

    for (int a = 0; a < N; ++a)
      for (int b = a + 1; b < N; ++b)
        for (int c = b + 1; c < N; ++c)
          for (int d = c + 1; d < N; ++d)
            for (int e = d + 1; e < N; ++e) {
              Five five;
              five.vertices = {static_cast<std::uint8_t>(a),
                               static_cast<std::uint8_t>(b),
                               static_cast<std::uint8_t>(c),
                               static_cast<std::uint8_t>(d),
                               static_cast<std::uint8_t>(e)};
              int vertices[5]{a, b, c, d, e};
              int at = 0;
              for (int i = 0; i < 5; ++i)
                for (int j = i + 1; j < 5; ++j)
                  five.edges[at++] = static_cast<std::uint16_t>(
                      edge_id[vertices[i]][vertices[j]]);
              fives.push_back(five);
            }
    if (fives.size() != 962598U) throw std::runtime_error("five-set count");

    std::ifstream stream(path);
    if (!stream) throw std::runtime_error("cannot open input");
    std::string text((std::istreambuf_iterator<char>(stream)), {});
    auto key = text.find("\"complete_additional_objective_12_rotation_representatives\"");
    if (key == std::string::npos) throw std::runtime_error("input key absent");
    std::size_t at = text.find('[', key);
    int depth = 0;
    std::vector<int> row;
    for (; at < text.size(); ++at) {
      char ch = text[at];
      if (ch == '[') {
        ++depth;
        if (depth == 2) row.clear();
      } else if (ch == ']') {
        if (depth == 2) rows.push_back(row);
        if (--depth == 0) break;
      } else if (depth == 2 && ch >= '0' && ch <= '9') {
        int value = 0;
        do {
          value = 10 * value + text[at] - '0';
          ++at;
        } while (at < text.size() && text[at] >= '0' && text[at] <= '9');
        --at;
        row.push_back(value);
      }
    }
    if (rows.size() != 238U) throw std::runtime_error("expected 238 representatives");
  }
};

struct Clause {
  std::array<std::int16_t, 10> literals{};
  std::uint8_t width = 0;
  std::uint32_t witness = 0;
};

struct Result {
  int index = -1;
  int red_defects = 0;
  int blue_defects = 0;
  int support = 0;
  int assigned = 0;
  bool unsat = false;
  struct Trace {
    bool conflict = false;
    int edge = -1;
    int value = -1;
    std::uint32_t witness = 0;
  };
  std::vector<Trace> trace;
};

Result classify(const Input &input, int index) {
  Result result;
  result.index = index;
  auto color = input.base;
  for (int edge : input.rows[static_cast<std::size_t>(index)]) {
    if (edge < 0 || edge >= M) throw std::runtime_error("toggle range");
    color[static_cast<std::size_t>(edge)] ^= 1U;
  }

  std::array<std::uint8_t, M> support{};
  for (auto const &five : input.fives) {
    int red = 0;
    for (auto edge : five.edges) red += color[edge];
    if (red == 0 || red == 10) {
      result.red_defects += red == 10;
      result.blue_defects += red == 0;
      for (auto edge : five.edges) support[edge] = 1;
    }
  }
  if (result.red_defects + result.blue_defects != 12)
    throw std::runtime_error("objective is not twelve");
  result.support = static_cast<int>(
      std::count(support.begin(), support.end(), std::uint8_t{1}));

  std::vector<Clause> clauses;
  clauses.reserve(4000);
  for (std::size_t five_index = 0; five_index < input.fives.size(); ++five_index) {
    auto const &five = input.fives[five_index];
    bool fixed_all_red = true;
    bool fixed_all_blue = true;
    std::array<std::uint16_t, 10> free{};
    int free_count = 0;
    for (auto edge : five.edges) {
      if (support[edge]) {
        free[static_cast<std::size_t>(free_count++)] = edge;
      } else {
        fixed_all_red = fixed_all_red && color[edge] != 0U;
        fixed_all_blue = fixed_all_blue && color[edge] == 0U;
      }
    }
    auto add = [&](bool positive) {
      if (free_count == 0) throw std::runtime_error("fixed monochromatic K5");
      Clause clause;
      clause.width = static_cast<std::uint8_t>(free_count);
      clause.witness = static_cast<std::uint32_t>(five_index);
      for (int i = 0; i < free_count; ++i) {
        int variable = static_cast<int>(free[static_cast<std::size_t>(i)]) + 1;
        clause.literals[static_cast<std::size_t>(i)] = static_cast<std::int16_t>(
            positive ? variable : -variable);
      }
      clauses.push_back(clause);
    };
    if (fixed_all_red) add(false);
    if (fixed_all_blue) add(true);
  }

  std::array<std::int8_t, M> assignment{};
  assignment.fill(-1);
  bool changed = true;
  while (changed && !result.unsat) {
    changed = false;
    for (auto const &clause : clauses) {
      bool satisfied = false;
      int unset_count = 0;
      int unit_literal = 0;
      for (int i = 0; i < clause.width; ++i) {
        int literal = clause.literals[static_cast<std::size_t>(i)];
        int edge = std::abs(literal) - 1;
        int value = assignment[static_cast<std::size_t>(edge)];
        if (value < 0) {
          ++unset_count;
          unit_literal = literal;
        } else if ((literal > 0) == (value == 1)) {
          satisfied = true;
          break;
        }
      }
      if (satisfied) continue;
      if (unset_count == 0) {
        result.unsat = true;
        result.trace.push_back({true, -1, -1, clause.witness});
        break;
      }
      if (unset_count == 1) {
        int edge = std::abs(unit_literal) - 1;
        int value = unit_literal > 0 ? 1 : 0;
        auto &slot = assignment[static_cast<std::size_t>(edge)];
        if (slot < 0) {
          slot = static_cast<std::int8_t>(value);
          ++result.assigned;
          result.trace.push_back({false, edge, value, clause.witness});
          changed = true;
        } else if (slot != value) {
          throw std::runtime_error("missed contradiction");
        }
      }
    }
  }
  return result;
}

int main(int argc, char **argv) try {
  if (argc != 4) {
    std::cerr << "usage: classify_up INPUT.json CENSUS.tsv PROOF.tsv\n";
    return 2;
  }
  Input input(argv[1]);
  std::vector<Result> results(input.rows.size());
  std::atomic<int> next{0};
  std::atomic<bool> failed{false};
  std::mutex error_mutex;
  std::string error;
  unsigned hardware = std::thread::hardware_concurrency();
  unsigned workers_count = std::min<unsigned>(32U, std::max(1U, hardware));
  std::vector<std::thread> workers;
  for (unsigned worker = 0; worker < workers_count; ++worker) {
    workers.emplace_back([&] {
      try {
        while (!failed.load()) {
          int index = next.fetch_add(1);
          if (index >= static_cast<int>(results.size())) break;
          results[static_cast<std::size_t>(index)] = classify(input, index);
        }
      } catch (std::exception const &exception) {
        failed.store(true);
        std::lock_guard<std::mutex> lock(error_mutex);
        if (error.empty()) error = exception.what();
      }
    });
  }
  for (auto &worker : workers) worker.join();
  if (failed.load()) throw std::runtime_error(error);

  std::ofstream output(argv[2]);
  if (!output) throw std::runtime_error("cannot open output");
  std::ofstream proof(argv[3]);
  if (!proof) throw std::runtime_error("cannot open proof");
  output << "index\ttoggles\tred_defects\tblue_defects\tsupport_edges"
            "\tproof_assignments\tcore_clauses\tstatus\n";
  proof << "source\tstep\tkind\tedge_index\tvalue\tv0\tv1\tv2\tv3\tv4\n";
  int closed = 0;
  for (auto const &result : results) {
    closed += result.unsat;
    output << result.index << '\t'
           << input.rows[static_cast<std::size_t>(result.index)].size() << '\t'
           << result.red_defects << '\t'
           << result.blue_defects << '\t' << result.support << '\t'
           << result.assigned << '\t' << result.trace.size() << '\t'
           << (result.unsat ? "UP_UNSAT" : "UP_OPEN") << '\n';
    for (std::size_t step = 0; step < result.trace.size(); ++step) {
      auto const &trace = result.trace[step];
      auto const &vertices = input.fives[trace.witness].vertices;
      proof << result.index << '\t' << step << '\t'
            << (trace.conflict ? "CONFLICT" : "ASSIGN") << '\t'
            << trace.edge << '\t' << trace.value;
      for (auto vertex : vertices) proof << '\t' << static_cast<int>(vertex);
      proof << '\n';
    }
  }
  std::cout << "representatives=" << results.size() << " up_unsat=" << closed
            << " up_open=" << (static_cast<int>(results.size()) - closed)
            << " workers=" << workers_count << '\n';
  return 0;
} catch (std::exception const &exception) {
  std::cerr << exception.what() << '\n';
  return 2;
}
