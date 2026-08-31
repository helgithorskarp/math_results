#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <numeric>
#include <stdexcept>
#include <unordered_set>
#include <vector>

namespace {

constexpr int kRadius = 7;
constexpr int kMaximumOrder = 6 * 198;
constexpr std::uint64_t kBase = 2048;

using Triple = std::array<int, 3>;

std::vector<std::array<int, 3>> coefficient_vectors(int minimum_norm,
                                                    int maximum_norm) {
  std::vector<std::array<int, 3>> result;
  for (int x = -maximum_norm; x <= maximum_norm; ++x) {
    for (int y = -maximum_norm; y <= maximum_norm; ++y) {
      for (int z = -maximum_norm; z <= maximum_norm; ++z) {
        const int norm = std::abs(x) + std::abs(y) + std::abs(z);
        if (minimum_norm <= norm && norm <= maximum_norm) {
          result.push_back({x, y, z});
        }
      }
    }
  }
  return result;
}

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

std::vector<int> radius_sphere(
    int order, const Triple& generators,
    const std::vector<std::array<int, 3>>& shorter_coefficients,
    const std::vector<std::array<int, 3>>& shell_coefficients) {
  std::vector<bool> shorter(order, false);
  std::vector<bool> shell(order, false);
  auto image = [&](const std::array<int, 3>& coefficient) {
    std::int64_t value = 0;
    for (int i = 0; i < 3; ++i) {
      value += static_cast<std::int64_t>(coefficient[i]) * generators[i];
    }
    value %= order;
    if (value < 0) value += order;
    return static_cast<int>(value);
  };
  for (const auto& coefficient : shorter_coefficients) {
    shorter[image(coefficient)] = true;
  }
  for (const auto& coefficient : shell_coefficients) {
    shell[image(coefficient)] = true;
  }
  std::vector<int> result;
  for (int value = 0; value < order; ++value) {
    if (shell[value] && !shorter[value]) result.push_back(value);
  }
  return result;
}

bool clique_search(const std::vector<int>& candidates,
                   const std::vector<bool>& forbidden_difference,
                   int order, int start, int remaining,
                   std::vector<int>& chosen) {
  if (remaining == 0) return true;
  if (static_cast<int>(candidates.size()) - start < remaining) return false;
  for (int index = start;
       index + remaining <= static_cast<int>(candidates.size()); ++index) {
    const int candidate = candidates[index];
    bool compatible = true;
    for (int previous : chosen) {
      int difference = candidate - previous;
      if (difference < 0) difference += order;
      if (forbidden_difference[difference]) {
        compatible = false;
        break;
      }
    }
    if (!compatible) continue;
    chosen.push_back(candidate);
    if (clique_search(candidates, forbidden_difference, order, index + 1,
                      remaining - 1, chosen)) {
      return true;
    }
    chosen.pop_back();
  }
  return false;
}

bool has_translate_tiling(int order, const std::vector<int>& sphere,
                          int center_count) {
  if (static_cast<int>(sphere.size()) * center_count != order) return false;
  std::vector<bool> forbidden_difference(order, false);
  for (int left : sphere) {
    for (int right : sphere) {
      int difference = left - right;
      if (difference < 0) difference += order;
      forbidden_difference[difference] = true;
    }
  }
  std::vector<int> allowed;
  for (int shift = 1; shift < order; ++shift) {
    if (!forbidden_difference[shift]) allowed.push_back(shift);
  }
  std::vector<int> chosen;
  return clique_search(allowed, forbidden_difference, order, 0,
                       center_count - 1, chosen);
}

}  // namespace

int main(int argc, char** argv) {
  if (argc != 2) {
    throw std::runtime_error("usage: enumerator /scratch/candidates.txt");
  }
  std::ofstream candidate_output(argv[1]);
  if (!candidate_output) throw std::runtime_error("could not open output");

  const auto shorter_coefficients = coefficient_vectors(0, kRadius - 1);
  const auto shell_coefficients = coefficient_vectors(kRadius, kRadius);
  if (shorter_coefficients.size() != 377 || shell_coefficients.size() != 198) {
    throw std::runtime_error("unexpected Lee ball or shell size");
  }

  std::uint64_t eligible_orders = 0;
  std::uint64_t normalized_descriptions = 0;
  std::uint64_t generating_normalized_descriptions = 0;
  std::uint64_t unit_orbits = 0;
  std::uint64_t four_center_counting_candidates = 0;
  std::uint64_t six_center_counting_candidates = 0;
  std::uint64_t four_center_tilings = 0;
  std::uint64_t six_center_tilings = 0;

  for (int order = 1; order <= kMaximumOrder; ++order) {
    if (order % 4 != 0 && order % 6 != 0) continue;
    ++eligible_orders;
    std::vector<int> representatives;
    for (int value = 1; value * 2 < order; ++value) {
      representatives.push_back(value);
    }
    if (representatives.size() < 3) continue;
    std::vector<int> units;
    for (int value = 1; value < order; ++value) {
      if (std::gcd(value, order) == 1) units.push_back(value);
    }
    std::vector<int> gcd_with_order(order / 2 + 1);
    for (int value : representatives) {
      gcd_with_order[value] = std::gcd(value, order);
    }

    std::unordered_set<std::uint64_t> seen_normalized;
    for (int distinguished : representatives) {
      if (order % distinguished != 0) continue;
      std::vector<int> remaining;
      for (int value : representatives) {
        if (value != distinguished &&
            gcd_with_order[value] >= distinguished) {
          remaining.push_back(value);
        }
      }
      for (std::size_t first = 0; first < remaining.size(); ++first) {
        for (std::size_t second = first + 1; second < remaining.size();
             ++second) {
          ++normalized_descriptions;
          Triple generators = {distinguished, remaining[first],
                               remaining[second]};
          if (std::gcd(order,
                       std::gcd(generators[0],
                                std::gcd(generators[1], generators[2]))) != 1) {
            continue;
          }
          ++generating_normalized_descriptions;
          const auto descriptor = pack(generators);
          if (seen_normalized.contains(descriptor)) continue;
          ++unit_orbits;

          // Mark exactly the normalized descriptions from this unit orbit.
          // All generator gcds are invariant under units, so the minimum gcd
          // remains `distinguished`.
          for (int unit : units) {
            Triple image{};
            bool contains_distinguished = false;
            for (int i = 0; i < 3; ++i) {
              image[i] = pair_representative(unit * generators[i], order);
              contains_distinguished |= image[i] == distinguished;
            }
            if (contains_distinguished) seen_normalized.insert(pack(image));
          }

          const auto sphere = radius_sphere(order, generators,
                                            shorter_coefficients,
                                            shell_coefficients);
          auto record_candidate = [&](int center_count) {
            candidate_output << center_count << ' ' << order;
            for (int generator : generators) {
              candidate_output << ' ' << generator;
            }
            candidate_output << ' ' << sphere.size() << '\n';
          };
          if (4 * static_cast<int>(sphere.size()) == order) {
            ++four_center_counting_candidates;
            record_candidate(4);
            four_center_tilings +=
                has_translate_tiling(order, sphere, 4) ? 1 : 0;
          }
          if (6 * static_cast<int>(sphere.size()) == order) {
            ++six_center_counting_candidates;
            record_candidate(6);
            six_center_tilings +=
                has_translate_tiling(order, sphere, 6) ? 1 : 0;
          }
        }
      }
    }
  }

  std::cout << "radius=" << kRadius << '\n';
  std::cout << "maximum_group_order=" << kMaximumOrder << '\n';
  std::cout << "eligible_orders=" << eligible_orders << '\n';
  std::cout << "normalized_descriptions=" << normalized_descriptions << '\n';
  std::cout << "generating_normalized_descriptions="
            << generating_normalized_descriptions << '\n';
  std::cout << "unit_orbits=" << unit_orbits << '\n';
  std::cout << "four_center_counting_candidates="
            << four_center_counting_candidates << '\n';
  std::cout << "six_center_counting_candidates="
            << six_center_counting_candidates << '\n';
  std::cout << "four_center_tilings=" << four_center_tilings << '\n';
  std::cout << "six_center_tilings=" << six_center_tilings << '\n';
  candidate_output.flush();
  if (!candidate_output) throw std::runtime_error("failed to flush output");
  if (eligible_orders != 396 || normalized_descriptions != 39806626 ||
      generating_normalized_descriptions != 29453918 ||
      unit_orbits != 18339216 || four_center_counting_candidates != 3535 ||
      six_center_counting_candidates != 122095 ||
      four_center_tilings != 0 || six_center_tilings != 0) {
    throw std::runtime_error("unexpected enumeration result");
  }
}
