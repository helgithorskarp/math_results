#include <algorithm>
#include <chrono>
#include <cstdint>
#include <iomanip>
#include <iostream>
#include <optional>
#include <set>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

namespace {

using Layout = std::vector<int>;

struct StructuralCheck {
  bool height_balance = true;
  int siblings = 0;
  int internal_height = 0;
  int height_bound = 0;
};

StructuralCheck last_structural_check;

struct BigInteger {
  static constexpr std::uint64_t kBase = 1000000000ULL;
  std::vector<std::uint32_t> digits = {0};

  explicit BigInteger(std::uint64_t value = 0) {
    digits.clear();
    do {
      digits.push_back(value % kBase);
      value /= kBase;
    } while (value != 0);
  }

  void trim() {
    while (digits.size() > 1 && digits.back() == 0) {
      digits.pop_back();
    }
  }

  BigInteger& operator*=(std::uint64_t factor) {
    std::uint64_t carry = 0;
    for (std::uint32_t& digit : digits) {
      const std::uint64_t value = static_cast<std::uint64_t>(digit) * factor + carry;
      digit = value % kBase;
      carry = value / kBase;
    }
    while (carry != 0) {
      digits.push_back(carry % kBase);
      carry /= kBase;
    }
    return *this;
  }

  BigInteger& operator/=(std::uint32_t divisor) {
    std::uint64_t remainder = 0;
    for (auto it = digits.rbegin(); it != digits.rend(); ++it) {
      const std::uint64_t value = remainder * kBase + *it;
      *it = value / divisor;
      remainder = value % divisor;
    }
    if (remainder != 0) {
      throw std::runtime_error("inexact big-integer division");
    }
    trim();
    return *this;
  }

  BigInteger& operator+=(const BigInteger& other) {
    digits.resize(std::max(digits.size(), other.digits.size()), 0);
    std::uint64_t carry = 0;
    for (std::size_t i = 0; i < digits.size(); ++i) {
      const std::uint64_t value = static_cast<std::uint64_t>(digits[i]) +
                                  (i < other.digits.size() ? other.digits[i] : 0) + carry;
      digits[i] = value % kBase;
      carry = value / kBase;
    }
    if (carry != 0) {
      digits.push_back(carry);
    }
    return *this;
  }

  std::string str() const {
    std::ostringstream output;
    output << digits.back();
    for (auto it = digits.rbegin() + 1; it != digits.rend(); ++it) {
      output << std::setw(9) << std::setfill('0') << *it;
    }
    return output.str();
  }

  friend bool operator==(const BigInteger& left, const BigInteger& right) {
    return left.digits == right.digits;
  }

  friend bool operator>(const BigInteger& left, const BigInteger& right) {
    if (left.digits.size() != right.digits.size()) {
      return left.digits.size() > right.digits.size();
    }
    return std::lexicographical_compare(
        right.digits.rbegin(), right.digits.rend(), left.digits.rbegin(), left.digits.rend());
  }
};

const std::vector<std::uint64_t> kTreeCounts = {
    0,       0,       1,       1,       2,       3,       6,       11,
    23,      47,      106,     235,     551,     1301,    3159,    7741,
    19320,   48629,   123867,  317955,  823065,  2144505, 5623756,
};

std::optional<Layout> next_rooted_tree(const Layout& predecessor, int p = -1) {
  const int n = static_cast<int>(predecessor.size());
  if (p < 0) {
    p = n - 1;
    while (predecessor[p] == 1) {
      --p;
    }
  }
  if (p == 0) {
    return std::nullopt;
  }
  int q = p - 1;
  while (predecessor[q] != predecessor[p] - 1) {
    --q;
  }
  Layout result = predecessor;
  for (int i = p; i < n; ++i) {
    result[i] = result[i - p + q];
  }
  return result;
}

std::pair<Layout, Layout> split_tree(const Layout& layout) {
  bool one_found = false;
  int split = static_cast<int>(layout.size());
  for (int i = 0; i < static_cast<int>(layout.size()); ++i) {
    if (layout[i] == 1) {
      if (one_found) {
        split = i;
        break;
      }
      one_found = true;
    }
  }
  Layout left;
  for (int i = 1; i < split; ++i) {
    left.push_back(layout[i] - 1);
  }
  Layout rest = {0};
  rest.insert(rest.end(), layout.begin() + split, layout.end());
  return {left, rest};
}

std::optional<Layout> next_tree(const Layout& candidate) {
  const auto [left, rest] = split_tree(candidate);
  const int left_height = *std::max_element(left.begin(), left.end());
  const int rest_height = *std::max_element(rest.begin(), rest.end());
  bool valid = rest_height >= left_height;
  if (valid && rest_height == left_height) {
    if (left.size() > rest.size() ||
        (left.size() == rest.size() &&
         std::lexicographical_compare(rest.begin(), rest.end(), left.begin(), left.end()))) {
      valid = false;
    }
  }
  if (valid) {
    return candidate;
  }

  const int p = static_cast<int>(left.size());
  auto result = next_rooted_tree(candidate, p);
  if (!result) {
    return std::nullopt;
  }
  if (candidate[p] > 2) {
    const auto [new_left, ignored] = split_tree(*result);
    const int new_height = *std::max_element(new_left.begin(), new_left.end());
    const int suffix_length = new_height + 1;
    for (int i = 0; i < suffix_length; ++i) {
      (*result)[static_cast<int>(result->size()) - suffix_length + i] = i + 1;
    }
  }
  return result;
}

std::vector<std::vector<int>> adjacency(const Layout& layout) {
  std::vector<std::vector<int>> result(layout.size());
  std::vector<int> stack;
  for (int i = 0; i < static_cast<int>(layout.size()); ++i) {
    if (!stack.empty()) {
      while (layout[stack.back()] >= layout[i]) {
        stack.pop_back();
      }
      const int parent = stack.back();
      result[i].push_back(parent);
      result[parent].push_back(i);
    }
    stack.push_back(i);
  }
  return result;
}

BigInteger binomial(std::uint64_t n, int k) {
  if (k < 0 || static_cast<std::uint64_t>(k) > n) {
    return BigInteger(0);
  }
  k = std::min<std::uint64_t>(k, n - k);
  BigInteger result(1);
  for (int i = 1; i <= k; ++i) {
    result *= n - static_cast<std::uint64_t>(k) + i;
    result /= i;
  }
  return result;
}

BigInteger critical_count(const std::vector<std::vector<int>>& tree) {
  const int n = static_cast<int>(tree.size());
  last_structural_check = StructuralCheck{};
  if (n == 2) {
    return BigInteger(1);
  }
  std::vector<int> parent(n, -2);
  std::vector<int> traversal = {0};
  parent[0] = -1;
  for (int cursor = 0; cursor < n; ++cursor) {
    const int vertex = traversal[cursor];
    for (int neighbor : tree[vertex]) {
      if (neighbor != parent[vertex]) {
        parent[neighbor] = vertex;
        traversal.push_back(neighbor);
      }
    }
  }

  std::vector<std::uint64_t> down(n, 0);
  for (int vertex = 0; vertex < n; ++vertex) {
    if (tree[vertex].size() > 1) {
      down[vertex] = tree[vertex].size();
    }
  }
  for (auto it = traversal.rbegin(); it != traversal.rend(); ++it) {
    const int vertex = *it;
    for (int neighbor : tree[vertex]) {
      if (parent[neighbor] == vertex) {
        down[vertex] += 2 * down[neighbor];
      }
    }
  }
  std::vector<std::uint64_t> potential(n, 0);
  potential[0] = down[0];
  for (int cursor = 1; cursor < n; ++cursor) {
    const int vertex = traversal[cursor];
    potential[vertex] = 2 * potential[parent[vertex]] - 3 * down[vertex];
  }

  std::uint64_t maximum = 0;
  for (int vertex = 0; vertex < n; ++vertex) {
    if (tree[vertex].size() == 1) {
      if (potential[vertex] % 2 != 0) {
        throw std::runtime_error("odd leaf potential");
      }
      maximum = std::max(maximum, potential[vertex] / 2);
    }
  }
  std::set<int> maximizing_parents;
  for (int vertex = 0; vertex < n; ++vertex) {
    if (tree[vertex].size() == 1 && potential[vertex] / 2 == maximum) {
      maximizing_parents.insert(tree[vertex][0]);
    }
  }
  BigInteger result(0);
  for (int class_parent : maximizing_parents) {
    int siblings = 0;
    int internal_neighbors = 0;
    for (int neighbor : tree[class_parent]) {
      siblings += tree[neighbor].size() == 1;
      internal_neighbors += tree[neighbor].size() > 1;
    }
    if (internal_neighbors > 1) {
      throw std::runtime_error("maximizing leaf class is not a core endpoint");
    }
    if (internal_neighbors == 1) {
      std::vector<int> distance(n, -1);
      std::vector<int> queue = {class_parent};
      distance[class_parent] = 0;
      int internal_height = 0;
      for (int cursor = 0; cursor < n; ++cursor) {
        const int vertex = queue[cursor];
        if (tree[vertex].size() > 1) {
          internal_height = std::max(internal_height, distance[vertex]);
        }
        for (int neighbor : tree[vertex]) {
          if (distance[neighbor] < 0) {
            distance[neighbor] = distance[vertex] + 1;
            queue.push_back(neighbor);
          }
        }
      }
      if (internal_height > n - 2 * siblings - 1) {
        last_structural_check.height_balance = false;
        last_structural_check.siblings = siblings;
        last_structural_check.internal_height = internal_height;
        last_structural_check.height_bound = n - 2 * siblings - 1;
      }
    }
    result += binomial(maximum + siblings - 1, siblings - 1);
  }
  return result;
}

std::string json_array(const std::vector<int>& values) {
  std::string result = "[";
  for (int i = 0; i < static_cast<int>(values.size()); ++i) {
    if (i != 0) {
      result += ",";
    }
    result += std::to_string(values[i]);
  }
  return result + "]";
}

std::string family_record(const std::vector<std::vector<int>>& tree) {
  const int n = static_cast<int>(tree.size());
  std::vector<int> degree_sequence;
  std::vector<int> hubs;
  for (int vertex = 0; vertex < n; ++vertex) {
    const int degree = tree[vertex].size();
    degree_sequence.push_back(degree);
    if (degree > 2) {
      hubs.push_back(vertex);
    }
  }
  std::sort(degree_sequence.begin(), degree_sequence.end());
  if (hubs.size() != 2 || tree[hubs[0]].size() != tree[hubs[1]].size()) {
    return "{\"family\":\"other\",\"degree_sequence\":" +
           json_array(degree_sequence) + "}";
  }
  const int d = static_cast<int>(tree[hubs[0]].size()) - 1;
  for (int hub : hubs) {
    int leaves = 0;
    for (int neighbor : tree[hub]) {
      leaves += tree[neighbor].size() == 1;
    }
    if (leaves != d) {
      return "{\"family\":\"other\",\"degree_sequence\":" +
             json_array(degree_sequence) + "}";
    }
  }
  std::vector<int> distance(n, -1);
  std::vector<int> queue = {hubs[0]};
  distance[hubs[0]] = 0;
  for (int cursor = 0; cursor < n; ++cursor) {
    for (int neighbor : tree[queue[cursor]]) {
      if (distance[neighbor] < 0) {
        distance[neighbor] = distance[queue[cursor]] + 1;
        queue.push_back(neighbor);
      }
    }
  }
  return "{\"family\":\"symmetric_double_broom\",\"leaves_per_hub\":" +
         std::to_string(d) + ",\"hub_distance\":" +
         std::to_string(distance[hubs[1]]) + ",\"degree_sequence\":" +
         json_array(degree_sequence) + "}";
}

}  // namespace

int main(int argc, char** argv) {
  if (argc != 2) {
    std::cerr << "usage: census_global ORDER\n";
    return 2;
  }
  const int n = std::stoi(argv[1]);
  if (n < 2 || n >= static_cast<int>(kTreeCounts.size())) {
    throw std::invalid_argument("order must be between 2 and 22");
  }

  Layout initial;
  for (int i = 0; i <= n / 2; ++i) {
    initial.push_back(i);
  }
  for (int i = 1; i < (n + 1) / 2; ++i) {
    initial.push_back(i);
  }

  std::optional<Layout> layout = initial;
  std::uint64_t checked = 0;
  BigInteger best(0);
  bool have_best = false;
  std::vector<Layout> maximizers;
  std::uint64_t height_balance_violations = 0;
  std::optional<Layout> first_height_balance_violation;
  StructuralCheck first_violation_data;
  const auto started = std::chrono::steady_clock::now();
  while (layout) {
    layout = next_tree(*layout);
    if (layout) {
      const BigInteger value = critical_count(adjacency(*layout));
      ++checked;
      if (!last_structural_check.height_balance) {
        ++height_balance_violations;
        if (!first_height_balance_violation) {
          first_height_balance_violation = *layout;
          first_violation_data = last_structural_check;
        }
      }
      if (!have_best || value > best) {
        have_best = true;
        best = value;
        maximizers = {*layout};
      } else if (value == best) {
        maximizers.push_back(*layout);
      }
      layout = next_rooted_tree(*layout);
    }
  }
  if (checked != kTreeCounts[n]) {
    throw std::runtime_error("unlabeled-tree count mismatch");
  }
  const double seconds = std::chrono::duration<double>(
                             std::chrono::steady_clock::now() - started)
                             .count();
  std::cout << "{\"order\":" << n << ",\"trees_checked\":" << checked
            << ",\"maximum\":\"" << best.str() << "\",\"maximizer_count\":"
            << maximizers.size() << ",\"maximizers\":[";
  for (int i = 0; i < static_cast<int>(maximizers.size()); ++i) {
    if (i != 0) {
      std::cout << ',';
    }
    const auto tree = adjacency(maximizers[i]);
    std::cout << "{\"layout\":" << json_array(maximizers[i]) << ','
              << family_record(tree).substr(1);
  }
  std::cout << "],\"core_endpoint_checks\":true,\"height_balance_violations\":"
            << height_balance_violations;
  if (first_height_balance_violation) {
    std::cout << ",\"first_height_balance_violation\":{\"layout\":"
              << json_array(*first_height_balance_violation)
              << ",\"leaf_class\":" << first_violation_data.siblings
              << ",\"internal_height\":" << first_violation_data.internal_height
              << ",\"claimed_bound\":" << first_violation_data.height_bound << '}';
  }
  std::cout << ",\"elapsed_seconds\":" << seconds << ",\"all_checks\":true}\n";
}
