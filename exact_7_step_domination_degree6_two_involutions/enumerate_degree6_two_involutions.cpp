#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <queue>
#include <stdexcept>
#include <utility>
#include <vector>

namespace {

// The new exact-degree-six connection sets have two non-involutory inverse
// pairs and two involutions. Degree at most five and the other involutory
// degree-six cases are handled by predecessor results.
constexpr int kRadius = 7;
constexpr int kMaximumOrder = 576;

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

std::uint64_t choose_two(std::uint64_t value) {
  return value * (value - 1) / 2;
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
    addition_.resize(static_cast<std::size_t>(order_) * order_);
    for (int left = 0; left < order_; ++left) {
      for (int right = 0; right < order_; ++right) {
        int encoded = 0;
        for (std::size_t i = 0; i < factors_.size(); ++i) {
          encoded = encoded * factors_[i] +
                    (coordinates_[left][i] + coordinates_[right][i]) %
                        factors_[i];
        }
        addition_[static_cast<std::size_t>(left) * order_ + right] =
            static_cast<std::uint16_t>(encoded);
      }
    }
    inverse_.resize(order_);
    for (int element = 0; element < order_; ++element) {
      int encoded = 0;
      for (std::size_t i = 0; i < factors_.size(); ++i) {
        encoded = encoded * factors_[i] +
                  (factors_[i] - coordinates_[element][i]) % factors_[i];
      }
      inverse_[element] = static_cast<std::uint16_t>(encoded);
    }
  }

  int order() const { return order_; }
  const std::vector<int>& factors() const { return factors_; }
  const std::vector<int>& coordinates(int element) const {
    return coordinates_[element];
  }
  int add(int left, int right) const {
    return addition_[static_cast<std::size_t>(left) * order_ + right];
  }
  int subtract(int left, int right) const { return add(left, inverse(right)); }
  int inverse(int element) const { return inverse_[element]; }

 private:
  std::vector<int> factors_;
  int order_;
  std::vector<std::vector<int>> coordinates_;
  std::vector<std::uint16_t> addition_;
  std::vector<std::uint16_t> inverse_;
};

std::vector<int> prime_divisors(int number) {
  std::vector<int> result;
  for (int prime = 2; prime * prime <= number; ++prime) {
    if (number % prime != 0) continue;
    result.push_back(prime);
    while (number % prime == 0) number /= prime;
  }
  if (number > 1) result.push_back(number);
  return result;
}

// At every odd prime the involutions vanish in A/pA. Thus the two
// non-involutory generators alone must span each odd prime quotient, whose
// rank is necessarily at most two.
bool pair_spans_odd_prime_quotients(const AbelianGroup& group, int first,
                                    int second) {
  for (int prime : prime_divisors(group.order())) {
    if (prime == 2) continue;
    std::vector<int> active;
    for (std::size_t coordinate = 0; coordinate < group.factors().size();
         ++coordinate) {
      if (group.factors()[coordinate] % prime == 0) {
        active.push_back(static_cast<int>(coordinate));
      }
    }
    if (active.size() > 2) return false;
    if (active.size() == 1) {
      const int coordinate = active[0];
      if (group.coordinates(first)[coordinate] % prime == 0 &&
          group.coordinates(second)[coordinate] % prime == 0) {
        return false;
      }
    } else if (active.size() == 2) {
      const std::int64_t determinant =
          static_cast<std::int64_t>(group.coordinates(first)[active[0]]) *
              group.coordinates(second)[active[1]] -
          static_cast<std::int64_t>(group.coordinates(first)[active[1]]) *
              group.coordinates(second)[active[0]];
      if (determinant % prime == 0) return false;
    }
  }
  return true;
}

std::uint32_t vector_mod_two(const AbelianGroup& group, int element) {
  std::uint32_t result = 0;
  std::uint32_t bit = 1;
  for (std::size_t coordinate = 0; coordinate < group.factors().size();
       ++coordinate) {
    if (group.factors()[coordinate] % 2 == 0) {
      if (group.coordinates(element)[coordinate] % 2 != 0) result |= bit;
      bit <<= 1;
    }
  }
  return result;
}

bool four_elements_span_mod_two(const AbelianGroup& group,
                                const std::array<int, 4>& elements) {
  int target_rank = 0;
  for (int factor : group.factors()) target_rank += factor % 2 == 0;
  std::array<std::uint32_t, 4> basis{};
  int rank = 0;
  for (int element : elements) {
    std::uint32_t value = vector_mod_two(group, element);
    while (value != 0) {
      const int pivot = 31 - __builtin_clz(value);
      if (basis[pivot] == 0) {
        basis[pivot] = value;
        ++rank;
        break;
      }
      value ^= basis[pivot];
    }
  }
  return rank == target_rank;
}

std::vector<int> radius_sphere(const AbelianGroup& group,
                               const std::array<int, 4>& generators) {
  const std::array<int, 6> steps = {
      generators[0], group.inverse(generators[0]), generators[1],
      group.inverse(generators[1]), generators[2], generators[3]};
  std::vector<std::int16_t> distance(group.order(), -1);
  std::vector<std::uint16_t> queue(group.order());
  int head = 0;
  int tail = 1;
  queue[0] = 0;
  distance[0] = 0;
  while (head < tail) {
    const int element = queue[head++];
    if (distance[element] == kRadius) continue;
    for (int step : steps) {
      const int neighbour = group.add(element, step);
      if (distance[neighbour] == -1) {
        distance[neighbour] = distance[element] + 1;
        queue[tail++] = static_cast<std::uint16_t>(neighbour);
      }
    }
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
    const int shift = group.subtract(first_uncovered, sphere_element);
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
        factors.size() > 4) {
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
    if (involutions.size() < 2 || pair_representatives.size() < 2) continue;
    raw_descriptions += choose_two(pair_representatives.size()) *
                        choose_two(involutions.size());

    for (std::size_t first = 0; first < pair_representatives.size(); ++first) {
      for (std::size_t second = first + 1;
           second < pair_representatives.size(); ++second) {
        const int generator1 = pair_representatives[first];
        const int generator2 = pair_representatives[second];
        if (!pair_spans_odd_prime_quotients(group, generator1, generator2)) {
          continue;
        }
        for (std::size_t first_involution = 0;
             first_involution < involutions.size(); ++first_involution) {
          for (std::size_t second_involution = first_involution + 1;
               second_involution < involutions.size(); ++second_involution) {
            const std::array<int, 4> generators = {
                generator1, generator2, involutions[first_involution],
                involutions[second_involution]};
            if (!four_elements_span_mod_two(group, generators)) continue;
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
              four_center_tilings += has_translate_tiling(group, sphere, 4);
            }
            if (6 * size == group.order()) {
              ++six_center_counting_candidates;
              write_candidate(6);
              six_center_tilings += has_translate_tiling(group, sphere, 6);
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
  std::cout << "generating_connection_sets=" << generating_connection_sets
            << "\n";
  std::cout << "four_center_counting_candidates="
            << four_center_counting_candidates << "\n";
  std::cout << "six_center_counting_candidates="
            << six_center_counting_candidates << "\n";
  std::cout << "four_center_tilings=" << four_center_tilings << "\n";
  std::cout << "six_center_tilings=" << six_center_tilings << "\n";
  candidate_output.flush();
  if (!candidate_output) throw std::runtime_error("failed to flush output");
  if (types.size() != 1193 || raw_descriptions != 144757815) {
    throw std::runtime_error("unexpected enumeration-universe count");
  }
}
