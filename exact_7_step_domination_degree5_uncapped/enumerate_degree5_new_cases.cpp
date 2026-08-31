#include <algorithm>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <queue>
#include <stdexcept>
#include <utility>
#include <vector>

namespace {

// Enumerate only the connection sets of cardinality exactly five.  The
// degree-at-most-four cases are supplied by the separately corrected and
// independently checked predecessor contribution.

constexpr int kRadius = 7;
constexpr int kMaximumOrder = 312;

std::vector<std::vector<int>> invariant_factor_types(
    int limit, const std::vector<int>& prefix = {}) {
  int product = 1;
  for (int factor : prefix) {
    product *= factor;
  }
  const int start = prefix.empty() ? 2 : prefix.back();
  std::vector<std::vector<int>> result;
  for (int factor = start; product * factor <= limit; ++factor) {
    if (!prefix.empty() && factor % prefix.back() != 0) {
      continue;
    }
    std::vector<int> next = prefix;
    next.push_back(factor);
    result.push_back(next);
    auto descendants = invariant_factor_types(limit, next);
    result.insert(result.end(), descendants.begin(), descendants.end());
  }
  return result;
}

class AbelianGroup {
 public:
  explicit AbelianGroup(std::vector<int> factors)
      : factors_(std::move(factors)), order_(1) {
    for (int factor : factors_) {
      order_ *= factor;
    }
    coordinates_.resize(order_);
    for (int element = 0; element < order_; ++element) {
      int remainder = element;
      coordinates_[element].resize(factors_.size());
      for (int i = static_cast<int>(factors_.size()) - 1; i >= 0; --i) {
        coordinates_[element][i] = remainder % factors_[i];
        remainder /= factors_[i];
      }
    }
  }

  int order() const { return order_; }
  const std::vector<int>& factors() const { return factors_; }

  int add(int left, int right, int sign = 1) const {
    int encoded = 0;
    for (std::size_t i = 0; i < factors_.size(); ++i) {
      int coordinate =
          (coordinates_[left][i] + sign * coordinates_[right][i]) % factors_[i];
      if (coordinate < 0) {
        coordinate += factors_[i];
      }
      encoded = encoded * factors_[i] + coordinate;
    }
    return encoded;
  }

  int inverse(int element) const { return add(0, element, -1); }

 private:
  std::vector<int> factors_;
  int order_;
  std::vector<std::vector<int>> coordinates_;
};

std::pair<bool, int> connected_and_sphere_size(
    const AbelianGroup& group, const std::vector<int>& generators) {
  std::vector<int> distance(group.order(), -1);
  std::queue<int> queue;
  distance[0] = 0;
  queue.push(0);
  while (!queue.empty()) {
    const int element = queue.front();
    queue.pop();
    for (int generator : generators) {
      for (int sign : {-1, 1}) {
        const int neighbour = group.add(element, generator, sign);
        if (distance[neighbour] == -1) {
          distance[neighbour] = distance[element] + 1;
          queue.push(neighbour);
        }
      }
    }
  }
  const bool connected =
      std::find(distance.begin(), distance.end(), -1) == distance.end();
  const int sphere_size = static_cast<int>(
      std::count(distance.begin(), distance.end(), kRadius));
  return {connected, sphere_size};
}

std::vector<int> radius_sphere(const AbelianGroup& group,
                               const std::vector<int>& generators) {
  std::vector<int> distance(group.order(), -1);
  std::queue<int> queue;
  distance[0] = 0;
  queue.push(0);
  while (!queue.empty()) {
    const int element = queue.front();
    queue.pop();
    if (distance[element] == kRadius) {
      // Connectivity was already checked by the uncapped BFS above.  This
      // second BFS is truncated only because it extracts the radius-7 sphere.
      continue;
    }
    for (int generator : generators) {
      for (int sign : {-1, 1}) {
        const int neighbour = group.add(element, generator, sign);
        if (distance[neighbour] == -1) {
          distance[neighbour] = distance[element] + 1;
          queue.push(neighbour);
        }
      }
    }
  }
  std::vector<int> result;
  for (int element = 0; element < group.order(); ++element) {
    if (distance[element] == kRadius) {
      result.push_back(element);
    }
  }
  return result;
}

bool tile_recursively(const AbelianGroup& group, const std::vector<int>& sphere,
                      std::vector<bool>& covered, int remaining_translates) {
  if (remaining_translates == 0) {
    return std::find(covered.begin(), covered.end(), false) == covered.end();
  }
  const auto first = std::find(covered.begin(), covered.end(), false);
  if (first == covered.end()) {
    return false;
  }
  const int first_uncovered = static_cast<int>(first - covered.begin());
  std::vector<bool> tried_shift(group.order(), false);
  for (int sphere_element : sphere) {
    const int shift = group.add(first_uncovered, sphere_element, -1);
    if (tried_shift[shift]) {
      continue;
    }
    tried_shift[shift] = true;
    std::vector<int> translate;
    bool disjoint = true;
    for (int element : sphere) {
      const int translated = group.add(element, shift);
      if (covered[translated]) {
        disjoint = false;
        break;
      }
      translate.push_back(translated);
    }
    if (!disjoint) {
      continue;
    }
    for (int element : translate) {
      covered[element] = true;
    }
    if (tile_recursively(group, sphere, covered, remaining_translates - 1)) {
      return true;
    }
    for (int element : translate) {
      covered[element] = false;
    }
  }
  return false;
}

bool has_translate_tiling(const AbelianGroup& group,
                          const std::vector<int>& generators,
                          int translate_count) {
  const std::vector<int> sphere = radius_sphere(group, generators);
  if (static_cast<int>(sphere.size()) * translate_count != group.order()) {
    return false;
  }
  std::vector<bool> covered(group.order(), false);
  for (int element : sphere) {
    covered[element] = true;
  }
  return tile_recursively(group, sphere, covered, translate_count - 1);
}

}  // namespace

int main(int argc, char** argv) {
  if (argc != 2) {
    throw std::runtime_error("usage: enumerator /scratch/candidates.txt");
  }
  std::ofstream candidate_output(argv[1]);
  if (!candidate_output) {
    throw std::runtime_error("could not open candidate output");
  }
  {
    AbelianGroup diagnostic({18});
    const auto [is_connected, sphere_size] =
        connected_and_sphere_size(diagnostic, {1});
    if (!is_connected || sphere_size != 2) {
      throw std::runtime_error("uncapped-connectivity regression");
    }
  }
  std::uint64_t examined = 0;
  std::uint64_t connected = 0;
  std::uint64_t four_center_counting_candidates = 0;
  std::uint64_t six_center_counting_candidates = 0;
  std::uint64_t four_center_tilings = 0;
  std::uint64_t six_center_tilings = 0;
  const auto types = invariant_factor_types(kMaximumOrder);

  for (const auto& factors : types) {
    AbelianGroup group(factors);
    if (group.order() % 4 != 0 && group.order() % 6 != 0) {
      continue;
    }
    std::vector<int> involutions;
    std::vector<int> pair_representatives;
    for (int element = 1; element < group.order(); ++element) {
      const int inverse = group.inverse(element);
      if (inverse == element) {
        involutions.push_back(element);
      } else if (element < inverse) {
        pair_representatives.push_back(element);
      }
    }

    auto check = [&](const std::vector<int>& generators) {
      ++examined;
      const auto [is_connected, size] =
          connected_and_sphere_size(group, generators);
      if (!is_connected) {
        return;
      }
      ++connected;
      auto write_candidate = [&](int center_count) {
        candidate_output << center_count << " " << group.factors().size();
        for (int factor : group.factors()) {
          candidate_output << " " << factor;
        }
        candidate_output << " " << generators.size();
        for (int generator : generators) {
          candidate_output << " " << generator;
        }
        candidate_output << " " << size << "\n";
      };
      if (4 * size == group.order()) {
        ++four_center_counting_candidates;
        write_candidate(4);
        const bool tiles = has_translate_tiling(group, generators, 4);
        four_center_tilings += tiles;
      }
      if (6 * size == group.order()) {
        ++six_center_counting_candidates;
        write_candidate(6);
        const bool tiles = has_translate_tiling(group, generators, 6);
        six_center_tilings += tiles;
      }
    };

    for (int generator : pair_representatives) {
      if (group.order() <= 96 && factors.size() <= 4) {
        for (std::size_t i = 0; i < involutions.size(); ++i) {
          for (std::size_t j = i + 1; j < involutions.size(); ++j) {
            for (std::size_t k = j + 1; k < involutions.size(); ++k) {
              check(
                  {generator, involutions[i], involutions[j], involutions[k]});
            }
          }
        }
      }
    }
    for (std::size_t i = 0; i < pair_representatives.size(); ++i) {
      for (std::size_t j = i + 1; j < pair_representatives.size(); ++j) {
        if (factors.size() <= 3) {
          for (int involution : involutions) {
            check(
                {pair_representatives[i], pair_representatives[j], involution});
          }
        }
      }
    }
  }

  std::cout << "radius=" << kRadius << "\n";
  std::cout << "maximum_group_order=" << kMaximumOrder << "\n";
  std::cout << "invariant_factor_types=" << types.size() << "\n";
  std::cout << "connection_sets_examined=" << examined << "\n";
  std::cout << "connected_connection_sets=" << connected << "\n";
  std::cout << "four_center_counting_candidates="
            << four_center_counting_candidates << "\n";
  std::cout << "six_center_counting_candidates="
            << six_center_counting_candidates << "\n";
  std::cout << "four_center_tilings=" << four_center_tilings << "\n";
  std::cout << "six_center_tilings=" << six_center_tilings << "\n";
  candidate_output.flush();
  if (!candidate_output || examined != 3822979 || connected != 1681610 ||
      four_center_counting_candidates != 702 ||
      six_center_counting_candidates != 25304 || four_center_tilings != 0 ||
      six_center_tilings != 0) {
    throw std::runtime_error("unexpected degree-five enumeration result");
  }
}
