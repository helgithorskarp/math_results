#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <iomanip>
#include <iostream>
#include <stdexcept>
#include <string>
#include <unordered_set>
#include <vector>

namespace {

constexpr int kMaxN = 19;
using Config = std::array<std::uint16_t, kMaxN>;

int graph_order = 0;

struct ConfigHash {
  std::size_t operator()(const Config& config) const noexcept {
    std::size_t result = 0xcbf29ce484222325ULL;
    for (int i = 0; i < graph_order; ++i) {
      result ^= static_cast<std::size_t>(config[i]);
      result *= 0x100000001b3ULL;
    }
    return result;
  }
};

using ConfigSet = std::unordered_set<Config, ConfigHash>;

int least_rotation(const Config& sequence) {
  int first = 0;
  int second = 1;
  int offset = 0;
  while (first < graph_order && second < graph_order && offset < graph_order) {
    const std::uint16_t a = sequence[(first + offset) % graph_order];
    const std::uint16_t b = sequence[(second + offset) % graph_order];
    if (a == b) {
      ++offset;
      continue;
    }
    if (a > b) {
      first += offset + 1;
      if (first == second) {
        ++first;
      }
    } else {
      second += offset + 1;
      if (first == second) {
        ++second;
      }
    }
    offset = 0;
  }
  return std::min(first, second);
}

Config rotated(const Config& sequence, int shift) {
  Config result{};
  for (int j = 0; j < graph_order; ++j) {
    result[j] = sequence[(j + shift) % graph_order];
  }
  return result;
}

Config canonical(const Config& config) {
  const Config forward = rotated(config, least_rotation(config));
  Config reverse{};
  reverse[0] = config[0];
  for (int j = 1; j < graph_order; ++j) {
    reverse[j] = config[graph_order - j];
  }
  reverse = rotated(reverse, least_rotation(reverse));
  return std::min(forward, reverse);
}

bool is_stacked(const Config& config) {
  int support = 0;
  for (int i = 0; i < graph_order; ++i) {
    support += config[i] != 0;
  }
  return support == 1;
}

void add_binary_orbits(ConfigSet& configurations, int weight) {
  if (weight < 0 || weight > graph_order) {
    return;
  }
  const std::uint64_t limit = std::uint64_t{1} << graph_order;
  for (std::uint64_t mask = 0; mask < limit; ++mask) {
    if (__builtin_popcountll(mask) != weight) {
      continue;
    }
    Config config{};
    for (int i = 0; i < graph_order; ++i) {
      config[i] = static_cast<std::uint16_t>((mask >> i) & 1U);
    }
    if (!is_stacked(config)) {
      configurations.insert(canonical(config));
    }
  }
}

ConfigSet parents_of(const ConfigSet& children) {
  ConfigSet parents;
  parents.reserve(children.size() * static_cast<std::size_t>(graph_order));
  for (const Config& child : children) {
    for (int source = 0; source < graph_order; ++source) {
      for (int delta : {-1, 1}) {
        const int target = (source + delta + graph_order) % graph_order;
        if (child[target] == 0) {
          continue;
        }
        Config parent = child;
        parent[source] += 2;
        parent[target] -= 1;
        parents.insert(canonical(parent));
      }
    }
  }
  return parents;
}

bool every_child_is_in(const Config& parent, const ConfigSet& previous) {
  for (int source = 0; source < graph_order; ++source) {
    if (parent[source] < 2) {
      continue;
    }
    for (int delta : {-1, 1}) {
      const int target = (source + delta + graph_order) % graph_order;
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

std::string format_config(const Config& config) {
  std::string result = "[";
  for (int i = 0; i < graph_order; ++i) {
    if (i != 0) {
      result += ",";
    }
    result += std::to_string(config[i]);
  }
  result += "]";
  return result;
}

}  // namespace

int main(int argc, char** argv) {
  if (argc != 2) {
    std::cerr << "usage: enumerate_stacking ODD_CYCLE_ORDER\n";
    return 2;
  }
  graph_order = std::stoi(argv[1]);
  if (graph_order < 3 || graph_order > kMaxN || graph_order % 2 == 0) {
    throw std::invalid_argument("order must be odd and between 3 and 19");
  }

  ConfigSet previous;
  Config last_witness{};
  std::cout << "order=" << graph_order << "\n";

  for (int weight = 1; weight < 65535; ++weight) {
    const auto started = std::chrono::steady_clock::now();
    ConfigSet current = parents_of(previous);
    const std::size_t parent_candidates = current.size();
    add_binary_orbits(current, weight);

    for (auto it = current.begin(); it != current.end();) {
      if (is_stacked(*it) || !every_child_is_in(*it, previous)) {
        it = current.erase(it);
      } else {
        ++it;
      }
    }

    const auto ended = std::chrono::steady_clock::now();
    const double seconds =
        std::chrono::duration_cast<std::chrono::duration<double>>(ended - started)
            .count();
    std::cout << "weight=" << weight << " parent_candidates="
              << parent_candidates << " nonstackable_orbits=" << current.size()
              << " seconds=" << std::fixed << std::setprecision(6) << seconds;
    if (!current.empty()) {
      last_witness = *current.begin();
      std::cout << " witness=" << format_config(last_witness);
    }
    std::cout << "\n" << std::flush;

    if (weight > graph_order && current.empty()) {
      std::cout << "stacking_number=" << weight
                << " critical_weight=" << (weight - 1)
                << " critical_witness=" << format_config(last_witness) << "\n";
      return 0;
    }
    previous = std::move(current);
  }
  throw std::runtime_error("no stacking number below 65535");
}
