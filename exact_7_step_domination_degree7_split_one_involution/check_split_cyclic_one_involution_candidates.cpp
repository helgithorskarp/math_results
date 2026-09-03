#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <numeric>
#include <sstream>
#include <stdexcept>
#include <string>
#include <unordered_set>
#include <vector>

namespace {

constexpr int kRadius = 7;
constexpr int kMaximumBaseOrder = 1032;
constexpr std::uint64_t kBase = 2048;
using Triple = std::array<int, 3>;

int pair_representative(int value, int order) {
  value %= order;
  if (value < 0) value += order;
  return std::min(value, order - value);
}

std::uint64_t pack(Triple triple) {
  std::sort(triple.begin(), triple.end());
  return static_cast<std::uint64_t>(triple[0]) +
         kBase * static_cast<std::uint64_t>(triple[1]) +
         kBase * kBase * static_cast<std::uint64_t>(triple[2]);
}

std::uint64_t canonical_pack(int order, const Triple& generators) {
  std::uint64_t result = UINT64_MAX;
  for (int unit = 1; unit < order; ++unit) {
    if (std::gcd(unit, order) != 1) continue;
    Triple image{};
    for (int index = 0; index < 3; ++index) {
      image[index] = pair_representative(unit * generators[index], order);
    }
    result = std::min(result, pack(image));
  }
  return result;
}

std::vector<int> full_distances(int base_order, const Triple& generators) {
  const int order = 2 * base_order;
  std::array<int, 6> steps = {
      generators[0], base_order - generators[0], generators[1],
      base_order - generators[1], generators[2], base_order - generators[2]};
  std::vector<int> distances(order, -1);
  std::vector<int> queue(order);
  int head = 0;
  int tail = 1;
  queue[0] = 0;
  distances[0] = 0;
  while (head < tail) {
    const int value = queue[head++];
    for (int step : steps) {
      int base = value / 2 + step;
      if (base >= base_order) base -= base_order;
      const int neighbour = 2 * base + (value & 1);
      if (distances[neighbour] == -1) {
        distances[neighbour] = distances[value] + 1;
        queue[tail++] = neighbour;
      }
    }
    const int across = value ^ 1;
    if (distances[across] == -1) {
      distances[across] = distances[value] + 1;
      queue[tail++] = across;
    }
  }
  return distances;
}

int add_split(int left, int right, int base_order, int sign = 1) {
  int base = left / 2 + sign * (right / 2);
  base %= base_order;
  if (base < 0) base += base_order;
  return 2 * base + ((left & 1) ^ (right & 1));
}

bool exact_cover_search(int base_order, const std::vector<int>& sphere,
                        std::vector<bool>& covered, int remaining) {
  const int order = 2 * base_order;
  if (remaining == 0) {
    return std::find(covered.begin(), covered.end(), false) == covered.end();
  }
  const auto first = std::find(covered.begin(), covered.end(), false);
  if (first == covered.end()) return false;
  const int uncovered = static_cast<int>(first - covered.begin());
  std::vector<bool> tried(order, false);
  for (int element : sphere) {
    const int shift = add_split(uncovered, element, base_order, -1);
    if (tried[shift]) continue;
    tried[shift] = true;
    bool disjoint = true;
    for (int value : sphere) {
      const int translated = add_split(value, shift, base_order);
      if (covered[translated]) {
        disjoint = false;
        break;
      }
    }
    if (!disjoint) continue;
    for (int value : sphere) {
      const int translated = add_split(value, shift, base_order);
      covered[translated] = true;
    }
    if (exact_cover_search(base_order, sphere, covered, remaining - 1)) return true;
    for (int value : sphere) {
      const int translated = add_split(value, shift, base_order);
      covered[translated] = false;
    }
  }
  return false;
}

bool has_translate_tiling(int base_order, const std::vector<int>& sphere,
                          int center_count) {
  const int order = 2 * base_order;
  if (static_cast<int>(sphere.size()) * center_count != order) return false;
  std::vector<bool> covered(order, false);
  for (int value : sphere) covered[value] = true;
  return exact_cover_search(base_order, sphere, covered, center_count - 1);
}

// Burnside count for generating three-subsets of the non-involutory inverse
// pairs of Z/order Z under multiplication by units. A fixed three-subset is
// a union of cycles of lengths 1+1+1, 1+2, or 3.
std::uint64_t unit_orbit_count(int order) {
  std::vector<int> representatives;
  for (int value = 1; 2 * value < order; ++value) {
    representatives.push_back(value);
  }
  std::uint64_t burnside_sum = 0;
  std::uint64_t unit_count = 0;
  for (int unit = 1; unit < order; ++unit) {
    if (std::gcd(unit, order) != 1) continue;
    ++unit_count;
    std::vector<bool> visited(order / 2 + 1, false);
    std::vector<std::uint64_t> fixed_by_gcd(order + 1, 0);
    std::vector<std::uint64_t> two_cycles_by_gcd(order + 1, 0);
    std::uint64_t generating_three_cycles = 0;
    for (int start : representatives) {
      if (visited[start]) continue;
      int value = start;
      int length = 0;
      do {
        visited[value] = true;
        value = pair_representative(unit * value, order);
        ++length;
      } while (value != start);
      const int divisor = std::gcd(start, order);
      if (length == 1) {
        ++fixed_by_gcd[divisor];
      } else if (length == 2) {
        ++two_cycles_by_gcd[divisor];
      } else if (length == 3 && divisor == 1) {
        ++generating_three_cycles;
      }
    }

    std::array<std::vector<std::uint64_t>, 4> choose_fixed;
    for (auto& row : choose_fixed) row.assign(order + 1, 0);
    choose_fixed[0][order] = 1;
    for (int divisor = 1; divisor <= order; ++divisor) {
      for (std::uint64_t repeat = 0; repeat < fixed_by_gcd[divisor]; ++repeat) {
        for (int chosen = 2; chosen >= 0; --chosen) {
          for (int current = 1; current <= order; ++current) {
            const auto count = choose_fixed[chosen][current];
            if (count == 0) continue;
            choose_fixed[chosen + 1][std::gcd(current, divisor)] += count;
          }
        }
      }
    }
    std::uint64_t fixed_generating_subsets = choose_fixed[3][1];
    std::vector<int> fixed_divisors;
    std::vector<int> two_cycle_divisors;
    for (int divisor = 1; divisor <= order; ++divisor) {
      if (fixed_by_gcd[divisor] != 0) fixed_divisors.push_back(divisor);
      if (two_cycles_by_gcd[divisor] != 0) {
        two_cycle_divisors.push_back(divisor);
      }
    }
    for (int first_divisor : two_cycle_divisors) {
      for (int second_divisor : fixed_divisors) {
        if (std::gcd(first_divisor, second_divisor) == 1) {
          fixed_generating_subsets += two_cycles_by_gcd[first_divisor] *
                                      fixed_by_gcd[second_divisor];
        }
      }
    }
    fixed_generating_subsets += generating_three_cycles;
    burnside_sum += fixed_generating_subsets;
  }
  if (unit_count == 0 || burnside_sum % unit_count != 0) {
    throw std::runtime_error("nonintegral Burnside count");
  }
  return burnside_sum / unit_count;
}

struct Candidate {
  int center_count;
  int order;
  Triple generators;
  int sphere_size;
};

Candidate parse_candidate(const std::string& line) {
  std::istringstream input(line);
  Candidate result{};
  if (!(input >> result.center_count >> result.order >> result.generators[0] >>
        result.generators[1] >> result.generators[2] >> result.sphere_size)) {
    throw std::runtime_error("malformed candidate");
  }
  int trailing = 0;
  if (input >> trailing) throw std::runtime_error("trailing candidate field");
  return result;
}

}  // namespace

int main(int argc, char** argv) {
  if (argc != 2) {
    throw std::runtime_error("usage: checker /scratch/candidates.txt");
  }

  std::uint64_t burnside_orbits = 0;
  for (int order = 1; order <= kMaximumBaseOrder; ++order) {
    if (order % 2 == 0 || order % 3 == 0) {
      burnside_orbits += unit_orbit_count(order);
    }
  }

  std::ifstream input(argv[1]);
  if (!input) throw std::runtime_error("could not open candidate file");
  std::unordered_set<std::uint64_t> descriptors;
  std::uint64_t four_candidates = 0;
  std::uint64_t six_candidates = 0;
  std::uint64_t four_tilings = 0;
  std::uint64_t six_tilings = 0;
  std::string line;
  int line_number = 0;
  while (std::getline(input, line)) {
    ++line_number;
    const Candidate candidate = parse_candidate(line);
    if (candidate.order <= 0 || candidate.order > 2 * kMaximumBaseOrder ||
        candidate.order % 2 != 0) {
      throw std::runtime_error("invalid order at line " +
                               std::to_string(line_number));
    }
    const int base_order = candidate.order / 2;
    if (base_order % 2 != 0 && base_order % 3 != 0) {
      throw std::runtime_error("invalid divisibility at line " +
                               std::to_string(line_number));
    }
    auto sorted = candidate.generators;
    std::sort(sorted.begin(), sorted.end());
    if (sorted != candidate.generators || sorted[0] <= 0 ||
        2 * sorted[2] >= base_order || sorted[0] == sorted[1] ||
        sorted[1] == sorted[2] ||
        std::gcd(base_order,
                 std::gcd(sorted[0], std::gcd(sorted[1], sorted[2]))) != 1) {
      throw std::runtime_error("invalid generators at line " +
                               std::to_string(line_number));
    }
    const std::uint64_t orbit_key =
        static_cast<std::uint64_t>(candidate.order) * kBase * kBase * kBase +
        canonical_pack(base_order, candidate.generators);
    if (!descriptors.insert(orbit_key).second) {
      throw std::runtime_error("duplicate unit orbit at line " +
                               std::to_string(line_number));
    }

    const auto distances = full_distances(base_order, candidate.generators);
    if (std::find(distances.begin(), distances.end(), -1) != distances.end()) {
      throw std::runtime_error("disconnected candidate");
    }
    std::vector<int> sphere;
    for (int value = 0; value < candidate.order; ++value) {
      if (distances[value] == kRadius) sphere.push_back(value);
    }
    if (static_cast<int>(sphere.size()) != candidate.sphere_size ||
        candidate.center_count * candidate.sphere_size != candidate.order) {
      throw std::runtime_error("sphere/count mismatch at line " +
                               std::to_string(line_number));
    }
    const bool tiling = has_translate_tiling(
        base_order, sphere, candidate.center_count);
    if (candidate.center_count == 4) {
      ++four_candidates;
      four_tilings += tiling ? 1 : 0;
    } else if (candidate.center_count == 6) {
      ++six_candidates;
      six_tilings += tiling ? 1 : 0;
    } else {
      throw std::runtime_error("invalid center count");
    }
  }

  std::cout << "burnside_unit_orbits=" << burnside_orbits << '\n';
  std::cout << "candidate_unit_orbits=" << descriptors.size() << '\n';
  std::cout << "four_center_candidates_checked=" << four_candidates << '\n';
  std::cout << "six_center_candidates_checked=" << six_candidates << '\n';
  std::cout << "four_center_tilings=" << four_tilings << '\n';
  std::cout << "six_center_tilings=" << six_tilings << '\n';

}
