#include <algorithm>
#include <array>
#include <atomic>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <thread>
#include <vector>

constexpr int N = 43;
constexpr int M = 903;

struct Input {
  std::array<std::array<int, N>, N> edge_id{};
  std::array<std::pair<int, int>, M> endpoints{};
  std::array<std::uint8_t, M> base{};
  std::vector<std::vector<int>> rows;

  explicit Input(const std::string &path) {
    int next = 0;
    for (int u = 0; u < N; ++u) {
      for (int v = u + 1; v < N; ++v) {
        edge_id[u][v] = edge_id[v][u] = next;
        endpoints[next++] = {u, v};
      }
    }
    std::array<int, 11> lengths{1, 2, 7, 10, 12, 13, 14, 16, 18, 20, 21};
    for (int edge = 0; edge < M; ++edge) {
      auto [u, v] = endpoints[edge];
      int distance = std::min(v - u, N - v + u);
      base[edge] = std::find(lengths.begin(), lengths.end(), distance) != lengths.end();
    }
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
    if (rows.size() != 238) throw std::runtime_error("expected 238 representatives");
  }
};

struct Result {
  int defects = 0;
  int red_defects = 0;
  int blue_defects = 0;
  int support_edges = 0;
};

Result inspect(const Input &input, int index) {
  auto color = input.base;
  for (int edge : input.rows[index]) {
    if (edge < 0 || edge >= M) throw std::runtime_error("edge index out of range");
    color[edge] ^= 1;
  }
  std::array<std::uint8_t, M> used{};
  Result result;
  for (int a = 0; a < N; ++a)
    for (int b = a + 1; b < N; ++b)
      for (int c = b + 1; c < N; ++c)
        for (int d = c + 1; d < N; ++d)
          for (int e = d + 1; e < N; ++e) {
            int vertices[5]{a, b, c, d, e};
            int red = 0;
            std::array<int, 10> edges{};
            int next = 0;
            for (int i = 0; i < 5; ++i)
              for (int j = i + 1; j < 5; ++j) {
                int edge = input.edge_id[vertices[i]][vertices[j]];
                edges[next++] = edge;
                red += color[edge];
              }
            if (red == 0 || red == 10) {
              ++result.defects;
              result.red_defects += red == 10;
              result.blue_defects += red == 0;
              for (int edge : edges) used[edge] = 1;
            }
          }
  result.support_edges = static_cast<int>(
      std::count(used.begin(), used.end(), std::uint8_t{1}));
  if (result.defects != 12) throw std::runtime_error("source objective is not 12");
  return result;
}

int main(int argc, char **argv) try {
  if (argc != 3) {
    std::cerr << "usage: select_support INPUT.json OUTPUT.tsv\n";
    return 2;
  }
  Input input(argv[1]);
  std::vector<Result> results(input.rows.size());
  std::atomic<int> next{0};
  std::vector<std::thread> workers;
  int count = std::max(1u, std::thread::hardware_concurrency());
  for (int worker = 0; worker < count; ++worker) {
    workers.emplace_back([&] {
      for (;;) {
        int index = next.fetch_add(1);
        if (index >= static_cast<int>(results.size())) break;
        results[index] = inspect(input, index);
      }
    });
  }
  for (auto &worker : workers) worker.join();
  std::ofstream output(argv[2]);
  if (!output) throw std::runtime_error("cannot open output");
  output << "index\ttoggles\tdefects\tred_defects\tblue_defects\tsupport_edges\n";
  int selected = -1;
  for (int index = 0; index < static_cast<int>(results.size()); ++index) {
    auto const &row = results[index];
    output << index << '\t' << input.rows[index].size() << '\t' << row.defects << '\t'
           << row.red_defects << '\t' << row.blue_defects << '\t'
           << row.support_edges << '\n';
    if (selected < 0 || row.support_edges < results[selected].support_edges) selected = index;
  }
  std::cout << "representatives=" << results.size() << " selected=" << selected
            << " support_edges=" << results[selected].support_edges
            << " red_defects=" << results[selected].red_defects
            << " blue_defects=" << results[selected].blue_defects << '\n';
  return 0;
} catch (std::exception const &error) {
  std::cerr << error.what() << '\n';
  return 2;
}
