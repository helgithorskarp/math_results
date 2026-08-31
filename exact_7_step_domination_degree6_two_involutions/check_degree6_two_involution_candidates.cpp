#include <algorithm>
#include <array>
#include <bit>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <memory>
#include <queue>
#include <set>
#include <sstream>
#include <stdexcept>
#include <string>
#include <unordered_set>
#include <utility>
#include <vector>

namespace {

constexpr int kRadius = 7;
constexpr int kMaximumOrder = 576;
constexpr int kWords = (kMaximumOrder + 63) / 64;
using Bits = std::array<std::uint64_t, kWords>;

std::vector<std::vector<int>> invariant_factor_types(
    int limit, const std::vector<int>& prefix = {}) {
  int product = 1;
  for (int factor : prefix) product *= factor;
  std::vector<std::vector<int>> result;
  const int lower = prefix.empty() ? 2 : prefix.back();
  for (int factor = lower; factor <= limit / product; ++factor) {
    if (!prefix.empty() && factor % prefix.back() != 0) continue;
    auto extended = prefix;
    extended.push_back(factor);
    result.push_back(extended);
    auto descendants = invariant_factor_types(limit, extended);
    result.insert(result.end(), descendants.begin(), descendants.end());
  }
  return result;
}

std::string factors_key(const std::vector<int>& factors) {
  std::ostringstream output;
  for (int factor : factors) output << factor << ',';
  return output.str();
}

std::uint64_t choose_two(std::uint64_t value) {
  return value < 2 ? 0 : value * (value - 1) / 2;
}

std::uint64_t expected_raw_count(
    const std::vector<std::vector<int>>& types) {
  std::uint64_t total = 0;
  for (const auto& factors : types) {
    int order = 1;
    int even_factors = 0;
    for (int factor : factors) {
      order *= factor;
      even_factors += factor % 2 == 0;
    }
    if ((order % 4 != 0 && order % 6 != 0) || factors.size() > 4) continue;
    const std::uint64_t involutions = (std::uint64_t{1} << even_factors) - 1;
    const std::uint64_t inverse_pairs = (order - 1 - involutions) / 2;
    total += choose_two(inverse_pairs) * choose_two(involutions);
  }
  return total;
}

class DirectProduct {
 public:
  explicit DirectProduct(std::vector<int> factors)
      : factors_(std::move(factors)), order_(1) {
    for (int factor : factors_) order_ *= factor;
    coordinates_.resize(order_);
    for (int element = 0; element < order_; ++element) {
      coordinates_[element].resize(factors_.size());
      int remainder = element;
      for (int coordinate = static_cast<int>(factors_.size()) - 1;
           coordinate >= 0; --coordinate) {
        coordinates_[element][coordinate] = remainder % factors_[coordinate];
        remainder /= factors_[coordinate];
      }
    }
    sums_.resize(static_cast<std::size_t>(order_) * order_);
    inverses_.resize(order_);
    for (int left = 0; left < order_; ++left) {
      for (int right = 0; right < order_; ++right) {
        int encoded = 0;
        for (std::size_t coordinate = 0; coordinate < factors_.size();
             ++coordinate) {
          encoded = encoded * factors_[coordinate] +
                    (coordinates_[left][coordinate] +
                     coordinates_[right][coordinate]) %
                        factors_[coordinate];
        }
        sums_[static_cast<std::size_t>(left) * order_ + right] =
            static_cast<std::uint16_t>(encoded);
      }
      int inverse = 0;
      for (std::size_t coordinate = 0; coordinate < factors_.size();
           ++coordinate) {
        inverse = inverse * factors_[coordinate] +
                  (factors_[coordinate] - coordinates_[left][coordinate]) %
                      factors_[coordinate];
      }
      inverses_[left] = static_cast<std::uint16_t>(inverse);
    }
  }

  int order() const { return order_; }
  int add(int left, int right) const {
    return sums_[static_cast<std::size_t>(left) * order_ + right];
  }
  int inverse(int element) const { return inverses_[element]; }
  int subtract(int left, int right) const { return add(left, inverse(right)); }

  std::vector<int> full_distances(const std::array<int, 6>& steps) const {
    std::vector<int> distances(order_, -1);
    std::vector<std::uint16_t> queue(order_);
    int head = 0;
    int tail = 1;
    queue[0] = 0;
    distances[0] = 0;
    while (head < tail) {
      const int element = queue[head++];
      for (int step : steps) {
        const int neighbour = add(element, step);
        if (distances[neighbour] == -1) {
          distances[neighbour] = distances[element] + 1;
          queue[tail++] = static_cast<std::uint16_t>(neighbour);
        }
      }
    }
    return distances;
  }

 private:
  std::vector<int> factors_;
  int order_;
  std::vector<std::vector<int>> coordinates_;
  std::vector<std::uint16_t> sums_;
  std::vector<std::uint16_t> inverses_;
};

void set_bit(Bits& bits, int value) {
  bits[value / 64] |= std::uint64_t{1} << (value % 64);
}

bool test_bit(const Bits& bits, int value) {
  return (bits[value / 64] >> (value % 64)) & 1U;
}

int bit_count(const Bits& bits) {
  int result = 0;
  for (std::uint64_t word : bits) result += std::popcount(word);
  return result;
}

bool pop_first(Bits& bits, int& value) {
  for (int word = 0; word < kWords; ++word) {
    if (bits[word] == 0) continue;
    const int offset = std::countr_zero(bits[word]);
    bits[word] &= bits[word] - 1;
    value = 64 * word + offset;
    return true;
  }
  return false;
}

Bits intersect(const Bits& left, const Bits& right) {
  Bits result{};
  for (int word = 0; word < kWords; ++word) {
    result[word] = left[word] & right[word];
  }
  return result;
}

bool has_clique(Bits candidates, const std::vector<Bits>& adjacency,
                int remaining) {
  if (remaining == 0) return true;
  if (bit_count(candidates) < remaining) return false;
  int vertex = 0;
  while (pop_first(candidates, vertex)) {
    if (has_clique(intersect(candidates, adjacency[vertex]), adjacency,
                   remaining - 1)) {
      return true;
    }
    if (bit_count(candidates) < remaining) return false;
  }
  return false;
}

// With |A| = k|sphere|, k translates tile A iff they are pairwise disjoint.
// After fixing one shift at zero, allowable shifts are outside sphere-sphere;
// the other k-1 shifts must form a clique in the corresponding difference
// graph. This is independent of the enumerator's exact-cover recursion.
bool has_translate_tiling(const DirectProduct& group,
                          const std::vector<int>& sphere, int center_count) {
  Bits forbidden{};
  for (int left : sphere) {
    for (int right : sphere) set_bit(forbidden, group.subtract(left, right));
  }
  Bits allowed{};
  for (int shift = 0; shift < group.order(); ++shift) {
    if (!test_bit(forbidden, shift)) set_bit(allowed, shift);
  }
  std::vector<Bits> adjacency(group.order());
  for (int shift = 0; shift < group.order(); ++shift) {
    if (!test_bit(allowed, shift)) continue;
    for (int other = 0; other < group.order(); ++other) {
      if (test_bit(allowed, other) &&
          !test_bit(forbidden, group.subtract(other, shift))) {
        set_bit(adjacency[shift], other);
      }
    }
  }
  return has_clique(allowed, adjacency, center_count - 1);
}

struct Candidate {
  int center_count;
  std::vector<int> factors;
  std::vector<int> generators;
  int sphere_size;
};

Candidate parse_candidate(const std::string& line) {
  std::istringstream input(line);
  Candidate result{};
  int rank = 0;
  int generator_count = 0;
  if (!(input >> result.center_count >> rank) || rank <= 0) {
    throw std::runtime_error("invalid candidate prefix");
  }
  result.factors.resize(rank);
  for (int& factor : result.factors) input >> factor;
  input >> generator_count;
  result.generators.resize(generator_count);
  for (int& generator : result.generators) input >> generator;
  if (!(input >> result.sphere_size)) {
    throw std::runtime_error("missing sphere size");
  }
  int trailing = 0;
  if (input >> trailing) throw std::runtime_error("trailing candidate field");
  if (!input.eof()) throw std::runtime_error("malformed candidate line");
  return result;
}

}  // namespace

int main(int argc, char** argv) {
  if (argc != 2) {
    throw std::runtime_error("usage: checker /scratch/candidates.txt");
  }
  const auto types = invariant_factor_types(kMaximumOrder);
  std::unordered_set<std::string> valid_types;
  for (const auto& factors : types) valid_types.insert(factors_key(factors));
  if (types.size() != 1193 || expected_raw_count(types) != 144757815) {
    throw std::runtime_error("independent universe count failed");
  }

  std::ifstream input(argv[1]);
  if (!input) throw std::runtime_error("could not open candidate file");
  std::unordered_set<std::string> descriptors;
  std::unordered_set<std::string> completed_factor_blocks;
  std::string current_factors;
  std::unique_ptr<DirectProduct> group;
  std::uint64_t candidate_count = 0;
  std::uint64_t four_candidates = 0;
  std::uint64_t six_candidates = 0;
  std::uint64_t four_tilings = 0;
  std::uint64_t six_tilings = 0;

  std::string line;
  int line_number = 0;
  while (std::getline(input, line)) {
    ++line_number;
    if (!descriptors.insert(line).second) {
      throw std::runtime_error("duplicate descriptor at line " +
                               std::to_string(line_number));
    }
    const Candidate candidate = parse_candidate(line);
    const std::string key = factors_key(candidate.factors);
    if (!valid_types.contains(key)) {
      throw std::runtime_error("invalid group type at line " +
                               std::to_string(line_number));
    }
    if (key != current_factors) {
      if (!current_factors.empty()) completed_factor_blocks.insert(current_factors);
      if (completed_factor_blocks.contains(key)) {
        throw std::runtime_error("noncontiguous group block at line " +
                                 std::to_string(line_number));
      }
      group = std::make_unique<DirectProduct>(candidate.factors);
      current_factors = key;
    }
    if (candidate.generators.size() != 4) {
      throw std::runtime_error("wrong generator count at line " +
                               std::to_string(line_number));
    }
    const int first = candidate.generators[0];
    const int second = candidate.generators[1];
    const int involution1 = candidate.generators[2];
    const int involution2 = candidate.generators[3];
    if (!(first < group->inverse(first) && second < group->inverse(second) &&
          first < second && 0 < involution1 && involution1 < involution2 &&
          group->inverse(involution1) == involution1 &&
          group->inverse(involution2) == involution2)) {
      throw std::runtime_error("noncanonical generators at line " +
                               std::to_string(line_number));
    }
    std::array<int, 6> steps = {first, group->inverse(first), second,
                                group->inverse(second), involution1,
                                involution2};
    auto sorted_steps = steps;
    std::sort(sorted_steps.begin(), sorted_steps.end());
    if (std::adjacent_find(sorted_steps.begin(), sorted_steps.end()) !=
        sorted_steps.end()) {
      throw std::runtime_error("connection set has fewer than six elements");
    }
    const auto distances = group->full_distances(steps);
    if (std::find(distances.begin(), distances.end(), -1) != distances.end()) {
      throw std::runtime_error("disconnected candidate at line " +
                               std::to_string(line_number));
    }
    std::vector<int> sphere;
    for (int element = 0; element < group->order(); ++element) {
      if (distances[element] == kRadius) sphere.push_back(element);
    }
    if (static_cast<int>(sphere.size()) != candidate.sphere_size ||
        candidate.center_count * candidate.sphere_size != group->order()) {
      throw std::runtime_error("sphere or counting mismatch at line " +
                               std::to_string(line_number));
    }
    const bool tiling =
        has_translate_tiling(*group, sphere, candidate.center_count);
    if (candidate.center_count == 4) {
      ++four_candidates;
      four_tilings += tiling;
    } else if (candidate.center_count == 6) {
      ++six_candidates;
      six_tilings += tiling;
    } else {
      throw std::runtime_error("invalid center count at line " +
                               std::to_string(line_number));
    }
    ++candidate_count;
  }

  std::cout << "invariant_factor_types=" << types.size() << '\n';
  std::cout << "raw_connection_set_descriptions=" << expected_raw_count(types)
            << '\n';
  std::cout << "candidate_descriptors=" << candidate_count << '\n';
  std::cout << "four_center_candidates_checked=" << four_candidates << '\n';
  std::cout << "six_center_candidates_checked=" << six_candidates << '\n';
  std::cout << "four_center_tilings=" << four_tilings << '\n';
  std::cout << "six_center_tilings=" << six_tilings << '\n';
  if (candidate_count != 693726 || four_candidates != 2304 ||
      six_candidates != 691422 || four_tilings != 0 || six_tilings != 0) {
    throw std::runtime_error("unexpected independent checker result");
  }
}
