#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <numeric>
#include <optional>
#include <queue>
#include <sstream>
#include <stdexcept>
#include <string>
#include <unordered_set>
#include <utility>
#include <vector>

namespace {

constexpr int kOrder = 8;
using Config = std::array<std::uint16_t, kOrder>;
using Edge = std::pair<int, int>;
using Permutation = std::array<int, kOrder>;

struct ConfigHash {
  std::size_t operator()(const Config& config) const noexcept {
    std::size_t result = 0xcbf29ce484222325ULL;
    for (const std::uint16_t value : config) {
      result ^= static_cast<std::size_t>(value);
      result *= 0x100000001b3ULL;
    }
    return result;
  }
};

using ConfigSet = std::unordered_set<Config, ConfigHash>;

struct CatalogTree {
  int id = -1;
  int recorded_estimate = -1;
  std::vector<Edge> edges;
};

struct EnumerationResult {
  int stacking_number = -1;
  int peak_weight = -1;
  std::size_t peak_nonstackable_orbits = 0;
  Config critical_witness{};
};

std::vector<Edge> parse_edges(const std::string& encoded) {
  std::vector<Edge> result;
  std::stringstream stream(encoded);
  std::string item;
  while (std::getline(stream, item, ',')) {
    const std::size_t dash = item.find('-');
    if (dash == std::string::npos) {
      throw std::runtime_error("malformed edge: " + item);
    }
    const int first = std::stoi(item.substr(0, dash));
    const int second = std::stoi(item.substr(dash + 1));
    if (first < 0 || first >= kOrder || second < 0 || second >= kOrder ||
        first == second) {
      throw std::runtime_error("invalid edge: " + item);
    }
    result.emplace_back(first, second);
  }
  return result;
}

std::vector<CatalogTree> read_catalog(const std::string& path) {
  std::ifstream input(path);
  if (!input) {
    throw std::runtime_error("cannot open catalog: " + path);
  }
  std::vector<CatalogTree> result;
  std::string line;
  while (std::getline(input, line)) {
    if (line.empty()) {
      continue;
    }
    std::stringstream stream(line);
    std::string id;
    std::string estimate;
    std::string edges;
    if (!std::getline(stream, id, '\t') || !std::getline(stream, estimate, '\t') ||
        !std::getline(stream, edges)) {
      throw std::runtime_error("malformed catalog line: " + line);
    }
    result.push_back({std::stoi(id), std::stoi(estimate), parse_edges(edges)});
  }
  if (result.size() != 23) {
    throw std::runtime_error("the order-eight catalog must contain 23 trees");
  }
  for (std::size_t index = 0; index < result.size(); ++index) {
    if (result[index].id != static_cast<int>(index)) {
      throw std::runtime_error("catalog IDs must be consecutive from zero");
    }
  }
  return result;
}

class TreeEnumerator {
 public:
  explicit TreeEnumerator(const CatalogTree& tree) : tree_(tree) {
    if (tree_.edges.size() != kOrder - 1) {
      throw std::runtime_error("tree must have seven edges");
    }
    for (const auto& [first, second] : tree_.edges) {
      if (adjacent_[first][second]) {
        throw std::runtime_error("duplicate edge in catalog");
      }
      adjacent_[first][second] = adjacent_[second][first] = true;
      neighbors_[first].push_back(second);
      neighbors_[second].push_back(first);
    }
    verify_connected();
    compute_automorphisms();
  }

  int estimate() const {
    int result = 0;
    for (int root = 0; root < kOrder; ++root) {
      std::array<int, kOrder> distance{};
      distance.fill(-1);
      distance[root] = 0;
      std::queue<int> queue;
      queue.push(root);
      while (!queue.empty()) {
        const int vertex = queue.front();
        queue.pop();
        for (const int next : neighbors_[vertex]) {
          if (distance[next] == -1) {
            distance[next] = distance[vertex] + 1;
            queue.push(next);
          }
        }
      }
      int sigma = 0;
      int leaves = 0;
      for (int vertex = 0; vertex < kOrder; ++vertex) {
        const int degree = static_cast<int>(neighbors_[vertex].size());
        if (vertex == root || degree > 1) {
          sigma += degree * (1 << distance[vertex]);
        }
        if (vertex != root && degree == 1) {
          ++leaves;
        }
      }
      result = std::max(result, sigma + leaves + 1);
    }
    return result;
  }

  std::size_t automorphism_count() const { return automorphisms_.size(); }

  EnumerationResult enumerate() const {
    ConfigSet previous;
    EnumerationResult result;
    Config last_witness{};

    for (int weight = 1; weight < 1000; ++weight) {
      const auto started = std::chrono::steady_clock::now();
      ConfigSet candidates;
      candidates.reserve(previous.size() * 4 + 256);

      for (const Config& child : previous) {
        for (const auto& [first, second] : tree_.edges) {
          add_parent(child, first, second, candidates);
          add_parent(child, second, first, candidates);
        }
      }
      if (weight <= kOrder) {
        add_binary_orbits(weight, candidates);
      }

      ConfigSet current;
      current.reserve(candidates.size());
      for (const Config& parent : candidates) {
        if (!is_stacked(parent) && every_child_is_in(parent, previous)) {
          current.insert(parent);
        }
      }

      if (!current.empty()) {
        last_witness = *current.begin();
      }
      if (current.size() > result.peak_nonstackable_orbits) {
        result.peak_nonstackable_orbits = current.size();
        result.peak_weight = weight;
      }
      const double seconds = std::chrono::duration<double>(
                                 std::chrono::steady_clock::now() - started)
                                 .count();
      std::cout << "LEVEL tree=" << tree_.id << " weight=" << weight
                << " candidates=" << candidates.size()
                << " nonstackable_orbits=" << current.size()
                << " seconds=" << seconds << "\n" << std::flush;

      if (weight > kOrder && current.empty()) {
        result.stacking_number = weight;
        result.critical_witness = last_witness;
        return result;
      }
      previous = std::move(current);
    }
    throw std::runtime_error("stacking number not found below 1000");
  }

 private:
  CatalogTree tree_;
  std::array<std::array<bool, kOrder>, kOrder> adjacent_{};
  std::array<std::vector<int>, kOrder> neighbors_{};
  std::vector<Permutation> automorphisms_;

  void verify_connected() const {
    std::array<bool, kOrder> seen{};
    std::queue<int> queue;
    seen[0] = true;
    queue.push(0);
    while (!queue.empty()) {
      const int vertex = queue.front();
      queue.pop();
      for (const int next : neighbors_[vertex]) {
        if (!seen[next]) {
          seen[next] = true;
          queue.push(next);
        }
      }
    }
    if (!std::all_of(seen.begin(), seen.end(), [](bool value) { return value; })) {
      throw std::runtime_error("catalog entry is disconnected");
    }
  }

  void compute_automorphisms() {
    Permutation permutation{};
    std::iota(permutation.begin(), permutation.end(), 0);
    do {
      bool preserves_edges = true;
      for (int first = 0; first < kOrder && preserves_edges; ++first) {
        for (int second = 0; second < kOrder; ++second) {
          if (adjacent_[first][second] !=
              adjacent_[permutation[first]][permutation[second]]) {
            preserves_edges = false;
            break;
          }
        }
      }
      if (preserves_edges) {
        automorphisms_.push_back(permutation);
      }
    } while (std::next_permutation(permutation.begin(), permutation.end()));
    if (automorphisms_.empty()) {
      throw std::runtime_error("identity automorphism was not found");
    }
  }

  Config canonical(const Config& config) const {
    Config result = config;
    Config transformed{};
    for (const Permutation& permutation : automorphisms_) {
      for (int vertex = 0; vertex < kOrder; ++vertex) {
        transformed[vertex] = config[permutation[vertex]];
      }
      result = std::min(result, transformed);
    }
    return result;
  }

  static bool is_stacked(const Config& config) {
    int support = 0;
    for (const std::uint16_t value : config) {
      support += value != 0;
    }
    return support == 1;
  }

  void add_parent(const Config& child, int source, int target,
                  ConfigSet& candidates) const {
    if (child[target] == 0) {
      return;
    }
    Config parent = child;
    parent[source] += 2;
    parent[target] -= 1;
    candidates.insert(canonical(parent));
  }

  void add_binary_orbits(int weight, ConfigSet& candidates) const {
    for (unsigned mask = 0; mask < (1U << kOrder); ++mask) {
      if (__builtin_popcount(mask) != weight) {
        continue;
      }
      Config config{};
      for (int vertex = 0; vertex < kOrder; ++vertex) {
        config[vertex] = static_cast<std::uint16_t>((mask >> vertex) & 1U);
      }
      if (!is_stacked(config)) {
        candidates.insert(canonical(config));
      }
    }
  }

  bool every_child_is_in(const Config& parent, const ConfigSet& previous) const {
    for (int source = 0; source < kOrder; ++source) {
      if (parent[source] < 2) {
        continue;
      }
      for (const int target : neighbors_[source]) {
        Config child = parent;
        child[source] -= 2;
        child[target] += 1;
        if (!previous.contains(canonical(child))) {
          return false;
        }
      }
    }
    return true;
  }
};

std::string format_config(const Config& config) {
  std::string result = "[";
  for (int vertex = 0; vertex < kOrder; ++vertex) {
    if (vertex != 0) {
      result += ',';
    }
    result += std::to_string(config[vertex]);
  }
  return result + ']';
}

}  // namespace

int main(int argc, char** argv) {
  if (argc < 2 || argc > 3) {
    std::cerr << "usage: enumerate_tree8_stacking CATALOG.tsv [TREE_ID]\n";
    return 2;
  }
  const std::optional<int> selected = argc == 3 ? std::optional(std::stoi(argv[2]))
                                                 : std::nullopt;
  const std::vector<CatalogTree> catalog = read_catalog(argv[1]);
  int completed = 0;
  for (const CatalogTree& tree : catalog) {
    if (selected && tree.id != *selected) {
      continue;
    }
    TreeEnumerator enumerator(tree);
    const int estimate = enumerator.estimate();
    if (estimate != tree.recorded_estimate) {
      throw std::runtime_error("recorded estimate mismatch for tree " +
                               std::to_string(tree.id));
    }
    const EnumerationResult result = enumerator.enumerate();
    std::cout << "RESULT tree=" << tree.id
              << " stacking_number=" << result.stacking_number
              << " estimate=" << estimate
              << " automorphisms=" << enumerator.automorphism_count()
              << " peak_weight=" << result.peak_weight
              << " peak_nonstackable_orbits=" << result.peak_nonstackable_orbits
              << " critical_witness=" << format_config(result.critical_witness)
              << "\n";
    if (result.stacking_number != estimate) {
      throw std::runtime_error("tree formula fails at catalog ID " +
                               std::to_string(tree.id));
    }
    ++completed;
  }
  if (selected && completed != 1) {
    throw std::runtime_error("selected tree ID is absent from the catalog");
  }
  std::cout << "COMPLETE trees=" << completed << " all_equal=true\n";
}
