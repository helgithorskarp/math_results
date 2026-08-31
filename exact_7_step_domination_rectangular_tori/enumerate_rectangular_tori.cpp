#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <vector>

namespace {

constexpr int kRadius = 7;
constexpr int kMaximumOrder = 6 * 198;

struct Torus {
  int first;
  int second;
  int third;

  int order() const { return first * second * third; }

  int encode(int x, int y, int z) const {
    return (x * second + y) * third + z;
  }

  std::array<int, 3> decode(int value) const {
    const int z = value % third;
    value /= third;
    const int y = value % second;
    return {value / second, y, z};
  }

  int difference(int left, int right) const {
    const auto a = decode(left);
    const auto b = decode(right);
    return encode((a[0] - b[0] + first) % first,
                  (a[1] - b[1] + second) % second,
                  (a[2] - b[2] + third) % third);
  }
};

int cycle_distance(int value, int modulus) {
  return std::min(value, modulus - value);
}

std::vector<int> radius_sphere(const Torus& torus) {
  std::vector<int> result;
  for (int x = 0; x < torus.first; ++x) {
    const int x_distance = cycle_distance(x, torus.first);
    for (int y = 0; y < torus.second; ++y) {
      const int xy_distance = x_distance + cycle_distance(y, torus.second);
      for (int z = 0; z < torus.third; ++z) {
        if (xy_distance + cycle_distance(z, torus.third) == kRadius) {
          result.push_back(torus.encode(x, y, z));
        }
      }
    }
  }
  return result;
}

bool clique_search(const Torus& torus, const std::vector<int>& candidates,
                   const std::vector<bool>& forbidden_difference, int start,
                   int remaining, std::vector<int>& chosen) {
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
  std::vector<bool> forbidden_difference(torus.order(), false);
  for (int left : sphere) {
    for (int right : sphere) {
      forbidden_difference[torus.difference(left, right)] = true;
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

  std::uint64_t dimension_triples = 0;
  std::uint64_t eligible_dimension_triples = 0;
  std::uint64_t four_center_counting_candidates = 0;
  std::uint64_t six_center_counting_candidates = 0;
  std::uint64_t four_center_tilings = 0;
  std::uint64_t six_center_tilings = 0;

  for (int first = 3; first * first * first <= kMaximumOrder; ++first) {
    for (int second = first;
         first * second * second <= kMaximumOrder; ++second) {
      for (int third = second;
           first * second * third <= kMaximumOrder; ++third) {
        ++dimension_triples;
        const Torus torus{first, second, third};
        if (torus.order() % 4 != 0 && torus.order() % 6 != 0) continue;
        ++eligible_dimension_triples;
        const auto sphere = radius_sphere(torus);

        auto evaluate = [&](int center_count, std::uint64_t& candidate_count,
                            std::uint64_t& tiling_count) {
          if (center_count * static_cast<int>(sphere.size()) != torus.order()) {
            return;
          }
          ++candidate_count;
          const bool tiling = has_translate_tiling(torus, sphere, center_count);
          tiling_count += tiling ? 1 : 0;
          candidate_output << center_count << ' ' << first << ' ' << second
                           << ' ' << third << ' ' << sphere.size() << ' '
                           << (tiling ? 1 : 0) << '\n';
        };
        evaluate(4, four_center_counting_candidates, four_center_tilings);
        evaluate(6, six_center_counting_candidates, six_center_tilings);
      }
    }
  }

  std::cout << "radius=" << kRadius << '\n';
  std::cout << "maximum_group_order=" << kMaximumOrder << '\n';
  std::cout << "dimension_triples=" << dimension_triples << '\n';
  std::cout << "eligible_dimension_triples=" << eligible_dimension_triples
            << '\n';
  std::cout << "four_center_counting_candidates="
            << four_center_counting_candidates << '\n';
  std::cout << "six_center_counting_candidates="
            << six_center_counting_candidates << '\n';
  std::cout << "four_center_tilings=" << four_center_tilings << '\n';
  std::cout << "six_center_tilings=" << six_center_tilings << '\n';
  candidate_output.flush();
  if (!candidate_output) throw std::runtime_error("failed to flush output");
  if (dimension_triples != 1369 || eligible_dimension_triples != 1089 ||
      four_center_counting_candidates != 0 ||
      six_center_counting_candidates != 3 || four_center_tilings != 0 ||
      six_center_tilings != 0) {
    throw std::runtime_error("unexpected enumeration result");
  }
}
