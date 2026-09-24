#include <algorithm>
#include <bit>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <limits>
#include <numeric>
#include <set>
#include <string>
#include <utility>
#include <vector>

struct Term {
  int i;
  int j;
  std::int64_t coefficient;
};

struct Case {
  std::vector<int> partition;
  std::int64_t constant;
  std::vector<Term> terms;
  int expected_types;
  std::int64_t expected_minimum;
  std::int64_t expected_maximum;
  std::int64_t expected_target;
};

static std::int64_t evaluate(const std::vector<int>& values,
                             const Case& instance) {
  std::int64_t result = instance.constant;
  for (const Term& term : instance.terms) {
    result += term.coefficient * values[term.i] * values[term.j];
  }
  return result;
}

static std::int64_t target_value(const Case& instance) {
  std::int64_t result = 23 * instance.constant;
  for (const Term& term : instance.terms) {
    const std::int64_t left = instance.partition[term.i];
    const std::int64_t right = instance.partition[term.j];
    const std::int64_t moment =
        (term.i == term.j ? left * (20 + 4 * left) : 0) - left * right;
    result += term.coefficient * moment;
  }
  return result;
}

static void check_case(const Case& instance) {
  assert(std::accumulate(instance.partition.begin(), instance.partition.end(), 0) ==
         23);

  std::vector<int> denominators;
  std::int64_t common_denominator = 1;
  for (int size : instance.partition) {
    const int denominator = 20 + 4 * size;
    denominators.push_back(denominator);
    common_denominator = std::lcm(common_denominator,
                                  static_cast<std::int64_t>(denominator));
  }
  std::int64_t schur_numerator = common_denominator;
  for (std::size_t i = 0; i < instance.partition.size(); ++i) {
    schur_numerator -= instance.partition[i] *
                       (common_denominator / denominators[i]);
  }
  assert(schur_numerator > 0);

  std::set<std::vector<int>> admissible;
  // A normalized column has total sign sum 3 modulo 4.  Since its length is
  // 23, this is equivalent to an odd number of +1 entries.
  for (std::uint32_t mask = 0; mask < (std::uint32_t{1} << 23); ++mask) {
    if ((std::popcount(mask) & 1) == 0) {
      continue;
    }
    std::vector<int> block_sums;
    int offset = 0;
    std::int64_t weighted_sum = 0;
    std::int64_t square_sum = 0;
    for (std::size_t i = 0; i < instance.partition.size(); ++i) {
      const int size = instance.partition[i];
      const std::uint32_t block_mask =
          (mask >> offset) & ((std::uint32_t{1} << size) - 1);
      const int value = 2 * std::popcount(block_mask) - size;
      block_sums.push_back(value);
      const std::int64_t scale = common_denominator / denominators[i];
      weighted_sum += value * scale;
      square_sum += 4 * value * value * scale;
      offset += size;
    }
    assert(offset == 23);

    // This is the denominator-cleared identity u^T Z u = 3.
    if (square_sum * schur_numerator - 20 * weighted_sum * weighted_sum ==
        3 * common_denominator * schur_numerator) {
      admissible.insert(block_sums);
    }
  }

  std::int64_t minimum = std::numeric_limits<std::int64_t>::max();
  std::int64_t maximum = std::numeric_limits<std::int64_t>::min();
  for (const auto& values : admissible) {
    const std::int64_t result = evaluate(values, instance);
    minimum = std::min(minimum, result);
    maximum = std::max(maximum, result);
  }
  const std::int64_t target = target_value(instance);
  assert(static_cast<int>(admissible.size()) == instance.expected_types);
  if (admissible.empty()) {
    assert(instance.expected_minimum == 0 && instance.expected_maximum == 0);
    assert(instance.expected_target == 0);
    std::cout << '(';
    for (std::size_t i = 0; i < instance.partition.size(); ++i) {
      if (i != 0) std::cout << ',';
      std::cout << instance.partition[i];
    }
    std::cout << "): no admissible normalized column type\n";
    return;
  }
  assert(minimum == instance.expected_minimum && minimum >= 0);
  assert(maximum == instance.expected_maximum);
  assert(target == instance.expected_target && target < 0);

  std::cout << '(';
  for (std::size_t i = 0; i < instance.partition.size(); ++i) {
    if (i != 0) std::cout << ',';
    std::cout << instance.partition[i];
  }
  std::cout << "): " << admissible.size() << " types, certificate range ["
            << minimum << ", " << maximum << "], target " << target << '\n';
}

int main() {
  const std::vector<Case> cases = {
      {{11, 3, 3, 3, 1, 1, 1}, -3, {{0, 1, -1}}, 2, 0, 4, -36},
      {{11, 3, 3, 1, 1, 1, 1, 1, 1}, -3, {{2, 6, -1}}, 1, 0, 0, -66},
      {{9, 8, 2, 2, 2}, 0, {{0, 2, 6}, {1, 2, 14}, {2, 3, -13}},
       3, 0, 0, -280},
      {{9, 5, 5, 2, 2}, 0,
       {{0, 1, 5}, {0, 2, 5}, {1, 2, -1}, {1, 3, 10},
        {1, 4, 10}, {2, 2, -1}, {2, 3, 10}, {2, 4, 10}},
       22, 0, 0, -1000},
      {{9, 5, 2, 2, 2, 1, 1, 1}, -81, {{0, 0, 1}}, 2, 0, 0, -1440},
      {{9, 4, 2, 2, 2, 1, 1, 1, 1}, 0,
       {{0, 0, 1}, {8, 8, -81}}, 4, 0, 0, -1440},
      {{9, 3, 2, 2, 2, 2, 1, 1, 1}, 0,
       {{0, 0, 1}, {8, 8, -81}}, 4, 0, 0, -1440},
      {{8, 5, 5, 5}, -1, {{1, 2, 1}}, 4, 0, 24, -48},
      {{8, 4, 4, 4, 1, 1, 1}, 0, {{2, 5, 1}, {4, 5, 4}},
       3, 0, 6, -8},
      {{6, 6, 6, 2, 1, 1, 1}, -2, {{3, 6, -1}}, 1, 0, 0, -44},
      {{6, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1}, 0,
       {{9, 10, 1}, {10, 10, -1}}, 43, 0, 0, -24},
      {{5, 5, 5, 5, 1, 1, 1}, -1, {{4, 5, 1}}, 37, 0, 0, -24},
      {{5, 5, 5, 4, 1, 1, 1, 1}, 0,
       {{0, 1, 5}, {0, 2, 5}, {0, 4, 6}, {1, 2, 4}},
       46, 0, 380, -380},
      {{5, 5, 5, 3, 2, 1, 1, 1}, 0,
       {{0, 4, 1}, {5, 6, 10}}, 13, 0, 16, -20},
      {{5, 5, 2, 2, 2, 2, 2, 1, 1, 1}, 0, {}, 0, 0, 0, 0},
      {{5, 3, 3, 3, 3, 2, 2, 2}, 0,
       {{0, 5, -2}, {5, 5, -5}}, 2, 0, 0, -240},
  };

  for (const Case& instance : cases) {
    check_case(instance);
  }
  std::cout << "independent direct-column check verified all 16 obstructions\n";
  return 0;
}
