#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

namespace {

constexpr int kRadius = 7;
constexpr int kMaximumOrder = 6 * 198;

struct Torus {
  int first;
  int second;

  int order() const { return first * second; }
  int encode(int x, int y) const { return x * second + y; }
  std::array<int, 2> decode(int value) const {
    return {value / second, value % second};
  }
  int add(int left, int right) const {
    const auto a = decode(left);
    const auto b = decode(right);
    return encode((a[0] + b[0]) % first, (a[1] + b[1]) % second);
  }
  int subtract(int left, int right) const {
    const auto a = decode(left);
    const auto b = decode(right);
    return encode((a[0] - b[0] + first) % first,
                  (a[1] - b[1] + second) % second);
  }
  int negate(int value) const { return subtract(0, value); }
};

struct Candidate {
  int center_count;
  int first;
  int second;
  int diagonal_first;
  int diagonal_second;
  int sphere_size;

  auto fields() const {
    return std::array<int, 6>{center_count, first, second, diagonal_first,
                              diagonal_second, sphere_size};
  }
  bool operator<(const Candidate& other) const {
    return fields() < other.fields();
  }
  bool operator==(const Candidate& other) const {
    return fields() == other.fields();
  }
};

Candidate parse_candidate(const std::string& line) {
  std::istringstream input(line);
  Candidate result{};
  int claimed_tiling = -1;
  if (!(input >> result.center_count >> result.first >> result.second >>
        result.diagonal_first >> result.diagonal_second >> result.sphere_size >>
        claimed_tiling)) {
    throw std::runtime_error("malformed candidate line");
  }
  int trailing = 0;
  if (input >> trailing) throw std::runtime_error("trailing candidate field");
  if (claimed_tiling != 0) {
    throw std::runtime_error("enumerator claimed an unexpected tiling");
  }
  return result;
}

std::vector<int> bfs_sphere(const Torus& torus, int diagonal) {
  const int first_step = torus.encode(1, 0);
  const int second_step = torus.encode(0, 1);
  const std::array<int, 6> steps = {
      first_step, torus.negate(first_step), second_step,
      torus.negate(second_step), diagonal, torus.negate(diagonal)};
  std::vector<std::int8_t> distance(torus.order(), -1);
  std::vector<int> queue(torus.order());
  int head = 0;
  int tail = 1;
  queue[0] = 0;
  distance[0] = 0;
  while (head < tail) {
    const int value = queue[head++];
    if (distance[value] == kRadius) continue;
    for (int step : steps) {
      const int neighbour = torus.add(value, step);
      if (distance[neighbour] != -1) continue;
      distance[neighbour] = distance[value] + 1;
      queue[tail++] = neighbour;
    }
  }
  std::vector<int> sphere;
  for (int value = 0; value < torus.order(); ++value) {
    if (distance[value] == kRadius) sphere.push_back(value);
  }
  return sphere;
}

bool exact_cover_search(const Torus& torus, const std::vector<int>& sphere,
                        std::vector<std::uint8_t>& covered, int remaining) {
  if (remaining == 0) {
    return std::find(covered.begin(), covered.end(), 0) == covered.end();
  }
  const auto first = std::find(covered.begin(), covered.end(), 0);
  if (first == covered.end()) return false;
  const int uncovered = static_cast<int>(first - covered.begin());
  std::vector<std::uint8_t> tried(torus.order(), 0);
  for (int element : sphere) {
    const int shift = torus.subtract(uncovered, element);
    if (tried[shift]) continue;
    tried[shift] = 1;
    bool disjoint = true;
    for (int value : sphere) {
      if (covered[torus.add(value, shift)]) {
        disjoint = false;
        break;
      }
    }
    if (!disjoint) continue;
    for (int value : sphere) covered[torus.add(value, shift)] = 1;
    if (exact_cover_search(torus, sphere, covered, remaining - 1)) return true;
    for (int value : sphere) covered[torus.add(value, shift)] = 0;
  }
  return false;
}

bool has_translate_tiling(const Torus& torus, const std::vector<int>& sphere,
                          int center_count) {
  if (center_count * static_cast<int>(sphere.size()) != torus.order()) {
    return false;
  }
  std::vector<std::uint8_t> covered(torus.order(), 0);
  for (int value : sphere) covered[value] = 1;
  return exact_cover_search(torus, sphere, covered, center_count - 1);
}

}  // namespace

int main(int argc, char** argv) {
  if (argc != 2) {
    throw std::runtime_error("usage: checker /scratch/candidates.txt");
  }
  std::ifstream input(argv[1]);
  if (!input) throw std::runtime_error("could not open candidate file");
  std::vector<Candidate> emitted;
  std::string line;
  while (std::getline(input, line)) {
    if (!line.empty()) emitted.push_back(parse_candidate(line));
  }
  if (!input.eof()) throw std::runtime_error("failed while reading candidates");
  std::sort(emitted.begin(), emitted.end());
  if (std::adjacent_find(emitted.begin(), emitted.end()) != emitted.end()) {
    throw std::runtime_error("duplicate candidate descriptor");
  }

  std::uint64_t dimension_pairs = 0;
  std::uint64_t eligible_dimension_pairs = 0;
  std::uint64_t raw_diagonal_elements = 0;
  std::uint64_t admissible_inverse_pairs = 0;
  std::vector<Candidate> rescanned;
  for (int first = 3; first * first <= kMaximumOrder; ++first) {
    for (int second = first; first * second <= kMaximumOrder; ++second) {
      ++dimension_pairs;
      const Torus torus{first, second};
      if (torus.order() % 4 != 0 && torus.order() % 6 != 0) continue;
      ++eligible_dimension_pairs;
      const int first_step = torus.encode(1, 0);
      const int second_step = torus.encode(0, 1);
      for (int x = 0; x < first; ++x) {
        for (int y = 0; y < second; ++y) {
          const int diagonal = torus.encode(x, y);
          if (diagonal == 0) continue;
          const int negative = torus.negate(diagonal);
          if (diagonal > negative) continue;
          ++raw_diagonal_elements;
          if (diagonal == negative) continue;
          if (diagonal == first_step || diagonal == torus.negate(first_step) ||
              diagonal == second_step ||
              diagonal == torus.negate(second_step)) {
            continue;
          }
          ++admissible_inverse_pairs;
          const auto sphere = bfs_sphere(torus, diagonal);
          for (int center_count : {4, 6}) {
            if (center_count * static_cast<int>(sphere.size()) ==
                torus.order()) {
              rescanned.push_back(
                  {center_count, first, second, x, y,
                   static_cast<int>(sphere.size())});
            }
          }
        }
      }
    }
  }
  std::sort(rescanned.begin(), rescanned.end());
  if (rescanned != emitted) {
    throw std::runtime_error("BFS rescan differs from emitted candidates");
  }

  std::uint64_t four_center_tilings = 0;
  std::uint64_t six_center_tilings = 0;
  for (const Candidate& candidate : emitted) {
    const Torus torus{candidate.first, candidate.second};
    const int diagonal =
        torus.encode(candidate.diagonal_first, candidate.diagonal_second);
    const auto sphere = bfs_sphere(torus, diagonal);
    if (static_cast<int>(sphere.size()) != candidate.sphere_size) {
      throw std::runtime_error("candidate sphere-size mismatch");
    }
    const bool tiling =
        has_translate_tiling(torus, sphere, candidate.center_count);
    if (candidate.center_count == 4) {
      four_center_tilings += tiling ? 1 : 0;
    } else if (candidate.center_count == 6) {
      six_center_tilings += tiling ? 1 : 0;
    } else {
      throw std::runtime_error("unexpected center count");
    }
  }

  const auto four_center_candidates =
      std::count_if(emitted.begin(), emitted.end(),
                    [](const Candidate& candidate) {
                      return candidate.center_count == 4;
                    });
  const auto six_center_candidates =
      std::count_if(emitted.begin(), emitted.end(),
                    [](const Candidate& candidate) {
                      return candidate.center_count == 6;
                    });
  std::cout << "radius=" << kRadius << '\n';
  std::cout << "maximum_group_order=" << kMaximumOrder << '\n';
  std::cout << "dimension_pairs=" << dimension_pairs << '\n';
  std::cout << "eligible_dimension_pairs=" << eligible_dimension_pairs << '\n';
  std::cout << "raw_diagonal_elements=" << raw_diagonal_elements << '\n';
  std::cout << "admissible_inverse_pairs=" << admissible_inverse_pairs << '\n';
  std::cout << "four_center_candidates_checked=" << four_center_candidates
            << '\n';
  std::cout << "six_center_candidates_checked=" << six_center_candidates
            << '\n';
  std::cout << "four_center_tilings=" << four_center_tilings << '\n';
  std::cout << "six_center_tilings=" << six_center_tilings << '\n';

  if (dimension_pairs != 2538 || eligible_dimension_pairs != 1644 ||
      raw_diagonal_elements != 545614 ||
      admissible_inverse_pairs != 539518 || four_center_candidates != 80 ||
      six_center_candidates != 4351 || four_center_tilings != 0 ||
      six_center_tilings != 0) {
    throw std::runtime_error("unexpected independent-check result");
  }
}
