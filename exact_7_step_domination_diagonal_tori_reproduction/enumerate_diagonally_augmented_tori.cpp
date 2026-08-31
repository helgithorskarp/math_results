#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <vector>

namespace {

constexpr int kRadius = 7;
constexpr int kMaximumOrder = 6 * 198;
using Coefficient = std::array<int, 3>;

struct Torus {
  int first;
  int second;

  int order() const { return first * second; }
  int encode(int x, int y) const { return x * second + y; }
  std::array<int, 2> decode(int value) const {
    return {value / second, value % second};
  }
  int negate(int value) const {
    const auto point = decode(value);
    return encode((first - point[0]) % first,
                  (second - point[1]) % second);
  }
  int difference(int left, int right) const {
    const auto a = decode(left);
    const auto b = decode(right);
    return encode((a[0] - b[0] + first) % first,
                  (a[1] - b[1] + second) % second);
  }
};

std::vector<Coefficient> coefficient_vectors(int minimum_norm,
                                             int maximum_norm) {
  std::vector<Coefficient> result;
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

std::vector<int> radius_sphere(
    const Torus& torus, int diagonal,
    const std::vector<Coefficient>& shorter_coefficients,
    const std::vector<Coefficient>& shell_coefficients) {
  const auto step = torus.decode(diagonal);
  std::vector<std::uint8_t> shorter(torus.order(), 0);
  std::vector<std::uint8_t> shell(torus.order(), 0);
  auto image = [&](const Coefficient& coefficient) {
    std::int64_t x = coefficient[0] +
                     static_cast<std::int64_t>(coefficient[2]) * step[0];
    std::int64_t y = coefficient[1] +
                     static_cast<std::int64_t>(coefficient[2]) * step[1];
    x %= torus.first;
    y %= torus.second;
    if (x < 0) x += torus.first;
    if (y < 0) y += torus.second;
    return torus.encode(static_cast<int>(x), static_cast<int>(y));
  };
  for (const auto& coefficient : shorter_coefficients) {
    shorter[image(coefficient)] = 1;
  }
  for (const auto& coefficient : shell_coefficients) {
    shell[image(coefficient)] = 1;
  }
  std::vector<int> result;
  for (int value = 0; value < torus.order(); ++value) {
    if (shell[value] && !shorter[value]) result.push_back(value);
  }
  return result;
}

bool clique_search(const Torus& torus, const std::vector<int>& candidates,
                   const std::vector<std::uint8_t>& forbidden_difference,
                   int start, int remaining, std::vector<int>& chosen) {
  if (remaining == 0) return true;
  if (static_cast<int>(candidates.size()) - start < remaining) return false;
  for (int index = start;
       index + remaining <= static_cast<int>(candidates.size()); ++index) {
    const int candidate = candidates[index];
    bool compatible = true;
    for (int previous : chosen) {
      if (forbidden_difference[torus.difference(candidate, previous)]) {
        compatible = false;
        break;
      }
    }
    if (!compatible) continue;
    chosen.push_back(candidate);
    if (clique_search(torus, candidates, forbidden_difference, index + 1,
                      remaining - 1, chosen)) {
      return true;
    }
    chosen.pop_back();
  }
  return false;
}

bool has_translate_tiling(const Torus& torus, const std::vector<int>& sphere,
                          int center_count) {
  if (center_count * static_cast<int>(sphere.size()) != torus.order()) {
    return false;
  }
  std::vector<std::uint8_t> forbidden_difference(torus.order(), 0);
  for (int left : sphere) {
    for (int right : sphere) {
      forbidden_difference[torus.difference(left, right)] = 1;
    }
  }
  std::vector<int> allowed;
  for (int shift = 1; shift < torus.order(); ++shift) {
    if (!forbidden_difference[shift]) allowed.push_back(shift);
  }
  std::vector<int> chosen;
  return clique_search(torus, allowed, forbidden_difference, 0,
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

  std::uint64_t dimension_pairs = 0;
  std::uint64_t eligible_dimension_pairs = 0;
  std::uint64_t raw_diagonal_elements = 0;
  std::uint64_t admissible_inverse_pairs = 0;
  std::uint64_t four_center_counting_candidates = 0;
  std::uint64_t six_center_counting_candidates = 0;
  std::uint64_t four_center_tilings = 0;
  std::uint64_t six_center_tilings = 0;

  for (int first = 3; first * first <= kMaximumOrder; ++first) {
    for (int second = first; first * second <= kMaximumOrder; ++second) {
      ++dimension_pairs;
      const Torus torus{first, second};
      if (torus.order() % 4 != 0 && torus.order() % 6 != 0) continue;
      ++eligible_dimension_pairs;
      const int first_step = torus.encode(1, 0);
      const int second_step = torus.encode(0, 1);
      for (int diagonal = 1; diagonal < torus.order(); ++diagonal) {
        const int negative = torus.negate(diagonal);
        if (diagonal > negative) continue;
        ++raw_diagonal_elements;
        if (diagonal == negative) continue;
        if (diagonal == first_step || diagonal == torus.negate(first_step) ||
            diagonal == second_step || diagonal == torus.negate(second_step)) {
          continue;
        }
        ++admissible_inverse_pairs;
        const auto sphere = radius_sphere(torus, diagonal,
                                          shorter_coefficients,
                                          shell_coefficients);
        auto evaluate = [&](int center_count, std::uint64_t& candidate_count,
                            std::uint64_t& tiling_count) {
          if (center_count * static_cast<int>(sphere.size()) != torus.order()) {
            return;
          }
          ++candidate_count;
          const bool tiling = has_translate_tiling(torus, sphere, center_count);
          tiling_count += tiling ? 1 : 0;
          const auto point = torus.decode(diagonal);
          candidate_output << center_count << ' ' << first << ' ' << second
                           << ' ' << point[0] << ' ' << point[1] << ' '
                           << sphere.size() << ' ' << (tiling ? 1 : 0) << '\n';
        };
        evaluate(4, four_center_counting_candidates, four_center_tilings);
        evaluate(6, six_center_counting_candidates, six_center_tilings);
      }
    }
  }

  std::cout << "radius=" << kRadius << '\n';
  std::cout << "maximum_group_order=" << kMaximumOrder << '\n';
  std::cout << "dimension_pairs=" << dimension_pairs << '\n';
  std::cout << "eligible_dimension_pairs=" << eligible_dimension_pairs << '\n';
  std::cout << "raw_diagonal_elements=" << raw_diagonal_elements << '\n';
  std::cout << "admissible_inverse_pairs=" << admissible_inverse_pairs << '\n';
  std::cout << "four_center_counting_candidates="
            << four_center_counting_candidates << '\n';
  std::cout << "six_center_counting_candidates="
            << six_center_counting_candidates << '\n';
  std::cout << "four_center_tilings=" << four_center_tilings << '\n';
  std::cout << "six_center_tilings=" << six_center_tilings << '\n';
  candidate_output.flush();
  if (!candidate_output) throw std::runtime_error("failed to flush output");
  if (dimension_pairs != 2538 || eligible_dimension_pairs != 1644 ||
      raw_diagonal_elements != 545614 ||
      admissible_inverse_pairs != 539518 ||
      four_center_counting_candidates != 80 ||
      six_center_counting_candidates != 4351 || four_center_tilings != 0 ||
      six_center_tilings != 0) {
    throw std::runtime_error("unexpected enumeration result");
  }
}
