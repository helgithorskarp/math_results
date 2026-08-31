#include <algorithm>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <queue>
#include <stdexcept>
#include <utility>
#include <vector>

namespace {

// Exact degree-six connection sets with one non-involutory inverse pair and
// four involutions.  Degree at most five is handled by the predecessor result.
constexpr int kRadius = 7;
constexpr int kMaximumOrder = 192;

std::vector<std::vector<int>> invariant_factor_types(
    int limit, const std::vector<int>& prefix = {}) {
  int product = 1;
  for (int factor : prefix) product *= factor;
  const int start = prefix.empty() ? 2 : prefix.back();
  std::vector<std::vector<int>> result;
  for (int factor = start; product * factor <= limit; ++factor) {
    if (!prefix.empty() && factor % prefix.back() != 0) continue;
    auto next = prefix;
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
    for (int factor : factors_) order_ *= factor;
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
  const std::vector<int>& coordinates(int element) const {
    return coordinates_[element];
  }

  int add(int left, int right, int sign = 1) const {
    int encoded = 0;
    for (std::size_t i = 0; i < factors_.size(); ++i) {
      int coordinate =
          (coordinates_[left][i] + sign * coordinates_[right][i]) % factors_[i];
      if (coordinate < 0) coordinate += factors_[i];
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

std::vector<int> prime_divisors(int number) {
  std::vector<int> result;
  for (int p = 2; p * p <= number; ++p) {
    if (number % p != 0) continue;
    result.push_back(p);
    while (number % p == 0) number /= p;
  }
  if (number > 1) result.push_back(number);
  return result;
}

int rank_mod_p(std::vector<std::vector<int>> matrix, int p) {
  if (matrix.empty()) return 0;
  const int rows = static_cast<int>(matrix.size());
  const int cols = static_cast<int>(matrix[0].size());
  int rank = 0;
  for (int col = 0; col < cols && rank < rows; ++col) {
    int pivot = rank;
    while (pivot < rows && matrix[pivot][col] % p == 0) ++pivot;
    if (pivot == rows) continue;
    std::swap(matrix[rank], matrix[pivot]);
    int inverse = 1;
    const int value = matrix[rank][col] % p;
    while ((inverse * value) % p != 1) ++inverse;
    for (int j = col; j < cols; ++j) {
      matrix[rank][j] = (matrix[rank][j] * inverse) % p;
    }
    for (int i = 0; i < rows; ++i) {
      if (i == rank) continue;
      const int multiple = matrix[i][col] % p;
      for (int j = col; j < cols; ++j) {
        matrix[i][j] =
            (matrix[i][j] - multiple * matrix[rank][j]) % p;
        if (matrix[i][j] < 0) matrix[i][j] += p;
      }
    }
    ++rank;
  }
  return rank;
}

// For a finite abelian group A, a set generates A iff its images span A/pA
// for every prime p dividing |A| (the finite abelian Frattini criterion).
bool generates_via_prime_quotients(const AbelianGroup& group,
                                   const std::vector<int>& generators) {
  for (int p : prime_divisors(group.order())) {
    std::vector<int> active_coordinates;
    for (std::size_t i = 0; i < group.factors().size(); ++i) {
      if (group.factors()[i] % p == 0) {
        active_coordinates.push_back(static_cast<int>(i));
      }
    }
    std::vector<std::vector<int>> matrix(
        active_coordinates.size(), std::vector<int>(generators.size()));
    for (std::size_t i = 0; i < active_coordinates.size(); ++i) {
      for (std::size_t j = 0; j < generators.size(); ++j) {
        matrix[i][j] =
            group.coordinates(generators[j])[active_coordinates[i]] % p;
      }
    }
    if (rank_mod_p(matrix, p) != static_cast<int>(active_coordinates.size())) {
      return false;
    }
  }
  return true;
}

std::vector<int> connection_set(const AbelianGroup& group,
                                const std::vector<int>& generators) {
  std::vector<int> result;
  result.push_back(generators[0]);
  result.push_back(group.inverse(generators[0]));
  result.insert(result.end(), generators.begin() + 1, generators.end());
  std::sort(result.begin(), result.end());
  result.erase(std::unique(result.begin(), result.end()), result.end());
  return result;
}

std::vector<int> all_distances(const AbelianGroup& group,
                               const std::vector<int>& generators) {
  const auto neighbours = connection_set(group, generators);
  if (neighbours.size() != 6) {
    throw std::runtime_error("connection set does not have cardinality six");
  }
  std::vector<int> distance(group.order(), -1);
  std::queue<int> queue;
  distance[0] = 0;
  queue.push(0);
  while (!queue.empty()) {
    const int element = queue.front();
    queue.pop();
    for (int neighbour_step : neighbours) {
      const int neighbour = group.add(element, neighbour_step);
      if (distance[neighbour] == -1) {
        distance[neighbour] = distance[element] + 1;
        queue.push(neighbour);
      }
    }
  }
  return distance;
}

std::vector<int> radius_sphere(const AbelianGroup& group,
                               const std::vector<int>& generators) {
  const auto distance = all_distances(group, generators);
  if (std::find(distance.begin(), distance.end(), -1) != distance.end()) {
    throw std::runtime_error("prime-quotient generation test disagrees with BFS");
  }
  std::vector<int> sphere;
  for (int element = 0; element < group.order(); ++element) {
    if (distance[element] == kRadius) sphere.push_back(element);
  }
  return sphere;
}

bool tile_recursively(const AbelianGroup& group, const std::vector<int>& sphere,
                      std::vector<bool>& covered, int remaining_translates) {
  if (remaining_translates == 0) {
    return std::find(covered.begin(), covered.end(), false) == covered.end();
  }
  const auto first = std::find(covered.begin(), covered.end(), false);
  if (first == covered.end()) return false;
  const int first_uncovered = static_cast<int>(first - covered.begin());
  std::vector<bool> tried_shift(group.order(), false);
  for (int sphere_element : sphere) {
    const int shift = group.add(first_uncovered, sphere_element, -1);
    if (tried_shift[shift]) continue;
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
    if (!disjoint) continue;
    for (int element : translate) covered[element] = true;
    if (tile_recursively(group, sphere, covered, remaining_translates - 1)) {
      return true;
    }
    for (int element : translate) covered[element] = false;
  }
  return false;
}

bool has_translate_tiling(const AbelianGroup& group,
                          const std::vector<int>& sphere,
                          int translate_count) {
  if (static_cast<int>(sphere.size()) * translate_count != group.order()) {
    return false;
  }
  std::vector<bool> covered(group.order(), false);
  for (int element : sphere) covered[element] = true;
  return tile_recursively(group, sphere, covered, translate_count - 1);
}

}  // namespace

int main(int argc, char** argv) {
  if (argc != 2) {
    throw std::runtime_error("usage: enumerator /scratch/candidates.txt");
  }
  std::ofstream candidate_output(argv[1]);
  if (!candidate_output) throw std::runtime_error("could not open output");

  std::uint64_t raw_descriptions = 0;
  std::uint64_t generating_connection_sets = 0;
  std::uint64_t four_center_counting_candidates = 0;
  std::uint64_t six_center_counting_candidates = 0;
  std::uint64_t four_center_tilings = 0;
  std::uint64_t six_center_tilings = 0;
  const auto types = invariant_factor_types(kMaximumOrder);

  for (const auto& factors : types) {
    AbelianGroup group(factors);
    if ((group.order() % 4 != 0 && group.order() % 6 != 0) ||
        factors.size() > 5) {
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
    if (involutions.size() < 4) continue;

    for (int generator : pair_representatives) {
      for (std::size_t i = 0; i < involutions.size(); ++i) {
        for (std::size_t j = i + 1; j < involutions.size(); ++j) {
          for (std::size_t k = j + 1; k < involutions.size(); ++k) {
            for (std::size_t l = k + 1; l < involutions.size(); ++l) {
              ++raw_descriptions;
              const std::vector<int> generators = {
                  generator, involutions[i], involutions[j], involutions[k],
                  involutions[l]};
              if (!generates_via_prime_quotients(group, generators)) continue;
              ++generating_connection_sets;
              const auto sphere = radius_sphere(group, generators);
              const int size = static_cast<int>(sphere.size());
              auto write_candidate = [&](int center_count) {
                candidate_output << center_count << " " << factors.size();
                for (int factor : factors) candidate_output << " " << factor;
                candidate_output << " " << generators.size();
                for (int value : generators) candidate_output << " " << value;
                candidate_output << " " << size << "\n";
              };
              if (4 * size == group.order()) {
                ++four_center_counting_candidates;
                write_candidate(4);
                four_center_tilings +=
                    has_translate_tiling(group, sphere, 4);
              }
              if (6 * size == group.order()) {
                ++six_center_counting_candidates;
                write_candidate(6);
                six_center_tilings +=
                    has_translate_tiling(group, sphere, 6);
              }
            }
          }
        }
      }
    }
  }

  std::cout << "radius=" << kRadius << "\n";
  std::cout << "maximum_group_order=" << kMaximumOrder << "\n";
  std::cout << "invariant_factor_types=" << types.size() << "\n";
  std::cout << "raw_connection_set_descriptions=" << raw_descriptions << "\n";
  std::cout << "generating_connection_sets=" << generating_connection_sets << "\n";
  std::cout << "four_center_counting_candidates="
            << four_center_counting_candidates << "\n";
  std::cout << "six_center_counting_candidates="
            << six_center_counting_candidates << "\n";
  std::cout << "four_center_tilings=" << four_center_tilings << "\n";
  std::cout << "six_center_tilings=" << six_center_tilings << "\n";
  candidate_output.flush();
  if (!candidate_output) throw std::runtime_error("failed to flush output");
  if (raw_descriptions != 10237220 ||
      generating_connection_sets != 2749460 ||
      four_center_counting_candidates != 0 ||
      six_center_counting_candidates != 8960 ||
      four_center_tilings != 0 || six_center_tilings != 0) {
    throw std::runtime_error("unexpected four-involution enumeration result");
  }
}
