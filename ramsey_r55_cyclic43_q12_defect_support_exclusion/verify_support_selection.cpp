#include <algorithm>
#include <array>
#include <atomic>
#include <bit>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <thread>
#include <vector>

constexpr int N = 43;
constexpr int M = 903;
constexpr std::uint64_t ALL = (UINT64_C(1) << N) - 1;

struct Input {
  std::array<std::array<int, N>, N> edge_id{};
  std::array<std::pair<int, int>, M> endpoints{};
  std::array<std::uint8_t, M> base{};
  std::vector<std::vector<int>> rows;

  explicit Input(const std::string &path) {
    int next = 0;
    for (int u = 0; u < N; ++u)
      for (int v = u + 1; v < N; ++v) {
        edge_id[u][v] = edge_id[v][u] = next;
        endpoints[next++] = {u, v};
      }
    const std::array<int, 11> lengths{1, 2, 7, 10, 12, 13, 14, 16, 18, 20, 21};
    for (int edge = 0; edge < M; ++edge) {
      auto [u, v] = endpoints[edge];
      int distance = std::min(v - u, N - v + u);
      base[edge] = std::find(lengths.begin(), lengths.end(), distance) != lengths.end();
    }
    std::ifstream stream(path);
    if (!stream) throw std::runtime_error("input open");
    std::string text((std::istreambuf_iterator<char>(stream)), {});
    auto key = text.find("\"complete_additional_objective_12_rotation_representatives\"");
    if (key == std::string::npos) throw std::runtime_error("input key");
    std::size_t at = text.find('[', key);
    int level = 0;
    std::vector<int> row;
    while (at < text.size()) {
      char ch = text[at++];
      if (ch == '[') {
        ++level;
        if (level == 2) row.clear();
      } else if (ch == ']') {
        if (level == 2) rows.push_back(row);
        if (--level == 0) break;
      } else if (level == 2 && ch >= '0' && ch <= '9') {
        int value = ch - '0';
        while (at < text.size() && text[at] >= '0' && text[at] <= '9')
          value = 10 * value + text[at++] - '0';
        row.push_back(value);
      }
    }
    if (rows.size() != 238) throw std::runtime_error("row count");
  }
};

struct Result {
  int red = 0;
  int blue = 0;
  int support = 0;
};

void cliques(std::array<std::uint64_t, N> const &adjacency,
             std::array<std::array<int, N>, N> const &edge_id,
             std::uint64_t candidates, int depth, std::array<int, 5> &chosen,
             std::array<std::uint8_t, M> &support, int &count) {
  if (depth == 5) {
    ++count;
    for (int i = 0; i < 5; ++i)
      for (int j = i + 1; j < 5; ++j)
        support[edge_id[chosen[i]][chosen[j]]] = 1;
    return;
  }
  if (std::popcount(candidates) < 5 - depth) return;
  while (candidates) {
    int vertex = std::countr_zero(candidates);
    candidates &= candidates - 1;
    chosen[depth] = vertex;
    cliques(adjacency, edge_id, candidates & adjacency[vertex], depth + 1,
            chosen, support, count);
  }
}

Result inspect(Input const &input, int index) {
  auto colors = input.base;
  for (int edge : input.rows[index]) {
    if (edge < 0 || edge >= M) throw std::runtime_error("edge range");
    colors[edge] ^= 1;
  }
  std::array<std::uint64_t, N> red{};
  for (int edge = 0; edge < M; ++edge) {
    if (!colors[edge]) continue;
    auto [u, v] = input.endpoints[edge];
    red[u] |= UINT64_C(1) << v;
    red[v] |= UINT64_C(1) << u;
  }
  std::array<std::uint64_t, N> blue{};
  for (int vertex = 0; vertex < N; ++vertex)
    blue[vertex] = ALL & ~(red[vertex] | (UINT64_C(1) << vertex));
  std::array<std::uint8_t, M> support{};
  std::array<int, 5> chosen{};
  Result result;
  cliques(red, input.edge_id, ALL, 0, chosen, support, result.red);
  cliques(blue, input.edge_id, ALL, 0, chosen, support, result.blue);
  result.support = static_cast<int>(
      std::count(support.begin(), support.end(), std::uint8_t{1}));
  if (result.red + result.blue != 12) throw std::runtime_error("objective mismatch");
  return result;
}

int main(int argc, char **argv) try {
  if (argc != 3) {
    std::cerr << "usage: verify_support_selection INPUT.json EXPECTED.tsv\n";
    return 2;
  }
  Input input(argv[1]);
  std::ifstream expected(argv[2]);
  if (!expected) throw std::runtime_error("expected census open");
  std::string header;
  std::getline(expected, header);
  if (header != "index\ttoggles\tdefects\tred_defects\tblue_defects\tsupport_edges")
    throw std::runtime_error("expected census header");
  struct Claim { int toggles, defects, red, blue, support; };
  std::vector<Claim> claims;
  for (int wanted = 0; wanted < 238; ++wanted) {
    int index;
    Claim row{};
    if (!(expected >> index >> row.toggles >> row.defects >> row.red >> row.blue >> row.support)
        || index != wanted) throw std::runtime_error("expected census row");
    claims.push_back(row);
  }
  std::string trailing;
  if (expected >> trailing) throw std::runtime_error("trailing census data");

  std::vector<Result> results(238);
  std::atomic<int> next{0};
  std::vector<std::thread> workers;
  int worker_count = std::max(1u, std::thread::hardware_concurrency());
  for (int worker = 0; worker < worker_count; ++worker)
    workers.emplace_back([&] {
      for (;;) {
        int index = next.fetch_add(1);
        if (index >= 238) break;
        results[index] = inspect(input, index);
      }
    });
  for (auto &worker : workers) worker.join();

  int selected = -1;
  for (int index = 0; index < 238; ++index) {
    auto const &claim = claims[index];
    auto const &result = results[index];
    if (claim.toggles != static_cast<int>(input.rows[index].size()) ||
        claim.defects != result.red + result.blue || claim.red != result.red ||
        claim.blue != result.blue || claim.support != result.support)
      throw std::runtime_error("census mismatch at " + std::to_string(index));
    if (selected < 0 || result.support < results[selected].support) selected = index;
  }
  if (selected != 51 || results[selected].support != 60)
    throw std::runtime_error("selection mismatch");
  std::cout << "PASS independent clique-recursion census representatives=238 selected="
            << selected << " support_edges=" << results[selected].support << '\n';
  return 0;
} catch (std::exception const &error) {
  std::cerr << error.what() << '\n';
  return 2;
}
