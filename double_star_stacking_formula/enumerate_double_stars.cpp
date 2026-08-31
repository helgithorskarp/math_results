#include <algorithm>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <string>
#include <unordered_set>
#include <utility>
#include <vector>

namespace {

using Config = std::vector<std::uint16_t>;
using Edge = std::pair<int, int>;

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

class DoubleStarEnumerator {
 public:
  DoubleStarEnumerator(int a, int b) : a_(a), b_(b), order_(a + b + 2) {
    if (a_ < b_ || b_ < 1) {
      throw std::runtime_error("parameters must satisfy a >= b >= 1");
    }
    edges_.emplace_back(0, 1);
    for (int i = 0; i < a_; ++i) {
      edges_.emplace_back(0, 2 + i);
    }
    for (int i = 0; i < b_; ++i) {
      edges_.emplace_back(1, 2 + a_ + i);
    }
  }

  int conjectured_value() const { return 5 * a_ + 3 * b_ + 7; }

  int enumerate() const {
    ConfigSet previous;
    std::size_t peak = 0;
    int peak_weight = 0;

    for (int weight = 1; weight <= conjectured_value(); ++weight) {
      ConfigSet candidates;
      candidates.reserve(previous.size() * 4 + 256);
      for (const Config& child : previous) {
        for (const auto& [first, second] : edges_) {
          add_parent(child, first, second, candidates);
          add_parent(child, second, first, candidates);
        }
      }
      if (weight <= order_) {
        add_binary_orbits(weight, candidates);
      }

      ConfigSet current;
      current.reserve(candidates.size());
      for (const Config& candidate : candidates) {
        if (!is_stacked(candidate) && every_child_is_in(candidate, previous)) {
          current.insert(candidate);
        }
      }
      if (weight == conjectured_value() - 1) {
        const Config witness = canonical(proposed_critical_witness());
        if (!current.contains(witness)) {
          throw std::runtime_error("proposed critical witness is stackable");
        }
      }
      if (current.size() > peak) {
        peak = current.size();
        peak_weight = weight;
      }
      if (weight > order_ && current.empty()) {
        std::cout << "RESULT a=" << a_ << " b=" << b_
                  << " stacking_number=" << weight
                  << " formula=" << conjectured_value()
                  << " peak_weight=" << peak_weight
                  << " peak_orbits=" << peak
                  << " critical_witness="
                  << format(canonical(proposed_critical_witness())) << "\n";
        return weight;
      }
      previous = std::move(current);
    }
    throw std::runtime_error("frontier did not empty at the claimed value");
  }

 private:
  int a_;
  int b_;
  int order_;
  std::vector<Edge> edges_;

  Config proposed_critical_witness() const {
    Config result(order_, 0);
    for (int i = 0; i < a_; ++i) {
      result[2 + i] = 1;
    }
    for (int i = 0; i < b_; ++i) {
      result[2 + a_ + i] = 1;
    }
    result[2 + a_ + b_ - 1] =
        static_cast<std::uint16_t>(4 * a_ + 2 * b_ + 7);
    return result;
  }

  Config canonical(Config config) const {
    std::sort(config.begin() + 2, config.begin() + 2 + a_);
    std::sort(config.begin() + 2 + a_, config.end());
    if (a_ == b_) {
      Config swapped(order_, 0);
      swapped[0] = config[1];
      swapped[1] = config[0];
      std::copy(config.begin() + 2 + a_, config.end(), swapped.begin() + 2);
      std::copy(config.begin() + 2, config.begin() + 2 + a_,
                swapped.begin() + 2 + a_);
      config = std::min(config, swapped);
    }
    return config;
  }

  static bool is_stacked(const Config& config) {
    return std::count_if(config.begin(), config.end(),
                         [](std::uint16_t value) { return value != 0; }) == 1;
  }

  void add_parent(const Config& child, int source, int target,
                  ConfigSet& candidates) const {
    if (child[target] == 0 || child[source] > 65533) {
      return;
    }
    Config parent = child;
    parent[source] += 2;
    parent[target] -= 1;
    candidates.insert(canonical(std::move(parent)));
  }

  void add_binary_orbits(int weight, ConfigSet& candidates) const {
    if (order_ >= 31) {
      throw std::runtime_error("binary mask implementation requires order < 31");
    }
    for (std::uint32_t mask = 0; mask < (1U << order_); ++mask) {
      if (__builtin_popcount(mask) != weight) {
        continue;
      }
      Config config(order_, 0);
      for (int vertex = 0; vertex < order_; ++vertex) {
        config[vertex] = static_cast<std::uint16_t>((mask >> vertex) & 1U);
      }
      if (!is_stacked(config)) {
        candidates.insert(canonical(std::move(config)));
      }
    }
  }

  bool every_child_is_in(const Config& parent,
                         const ConfigSet& previous) const {
    for (const auto& [first, second] : edges_) {
      for (const auto& [source, target] : {Edge{first, second},
                                          Edge{second, first}}) {
        if (parent[source] < 2) {
          continue;
        }
        Config child = parent;
        child[source] -= 2;
        child[target] += 1;
        if (!previous.contains(canonical(std::move(child)))) {
          return false;
        }
      }
    }
    return true;
  }

  static std::string format(const Config& config) {
    std::string result = "[";
    for (std::size_t i = 0; i < config.size(); ++i) {
      if (i != 0) {
        result += ',';
      }
      result += std::to_string(config[i]);
    }
    return result + ']';
  }
};

}  // namespace

int main(int argc, char** argv) {
  int max_leaf_sum = 8;
  if (argc == 2) {
    max_leaf_sum = std::stoi(argv[1]);
  } else if (argc != 1) {
    std::cerr << "usage: enumerate_double_stars [MAX_A_PLUS_B]\n";
    return 2;
  }
  if (max_leaf_sum < 2 || max_leaf_sum > 20) {
    throw std::runtime_error("MAX_A_PLUS_B must lie between 2 and 20");
  }

  int checked = 0;
  for (int sum = 2; sum <= max_leaf_sum; ++sum) {
    for (int b = 1; b * 2 <= sum; ++b) {
      const int a = sum - b;
      DoubleStarEnumerator enumerator(a, b);
      if (enumerator.enumerate() != enumerator.conjectured_value()) {
        throw std::runtime_error("formula mismatch");
      }
      ++checked;
    }
  }
  std::cout << "COMPLETE parameter_pairs=" << checked
            << " max_leaf_sum=" << max_leaf_sum << " all_equal=true\n";
}
