#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <numeric>
#include <queue>
#include <sstream>
#include <stdexcept>
#include <string>
#include <unordered_set>
#include <vector>

namespace {

// Independent decisive algorithms: analytic HNF counts, full graph BFS, and
// direct translate exact cover for every emitted counting candidate.
constexpr int kRadius = 7;
constexpr int kMaximumBaseOrder = 1032;
using Vec = std::array<int, 3>;

struct HNF {
  int a;
  int b;
  int c;
  int x;
  int y;
  int z;

  int order() const { return a * b * c; }

  Vec reduce(Vec value) const {
    auto residue = [](int n, int modulus) {
      int result = n % modulus;
      return result < 0 ? result + modulus : result;
    };
    int next = residue(value[2], c);
    int quotient = (value[2] - next) / c;
    value[0] -= quotient * y;
    value[1] -= quotient * z;
    value[2] = next;
    next = residue(value[1], b);
    quotient = (value[1] - next) / b;
    value[0] -= quotient * x;
    value[1] = next;
    value[0] = residue(value[0], a);
    return value;
  }

  int encode(const Vec& value) const {
    return value[0] + a * (value[1] + b * value[2]);
  }

  int image(const Vec& value) const { return encode(reduce(value)); }

  Vec decode(int encoded) const {
    const int first = encoded % a;
    encoded /= a;
    const int second = encoded % b;
    return {first, second, encoded / b};
  }

  int add(int left, int right, int sign = 1) const {
    Vec first = decode(left);
    const Vec second = decode(right);
    for (int i = 0; i < 3; ++i) first[i] += sign * second[i];
    return image(first);
  }
};

bool cyclic_quotient(const HNF& h) {
  const std::array<int, 6> minors = {
      h.a * h.b, h.a * h.z, h.x * h.z - h.b * h.y,
      h.a * h.c, h.x * h.c, h.b * h.c};
  int divisor = 0;
  for (int minor : minors) divisor = std::gcd(divisor, std::abs(minor));
  return divisor == 1;
}

std::vector<int> full_distances(const HNF& h) {
  const std::array<int, 6> steps = {
      h.image({1, 0, 0}), h.image({-1, 0, 0}),
      h.image({0, 1, 0}), h.image({0, -1, 0}),
      h.image({0, 0, 1}), h.image({0, 0, -1})};
  const int order = 2 * h.order();
  std::vector<int> distance(order, -1);
  std::queue<int> queue;
  distance[0] = 0;
  queue.push(0);
  while (!queue.empty()) {
    const int current = queue.front();
    queue.pop();
    for (int step : steps) {
      const int neighbour = 2 * h.add(current / 2, step) + (current & 1);
      if (distance[neighbour] != -1) continue;
      distance[neighbour] = distance[current] + 1;
      queue.push(neighbour);
    }
    const int across = current ^ 1;
    if (distance[across] == -1) {
      distance[across] = distance[current] + 1;
      queue.push(across);
    }
  }
  return distance;
}

int split_add(const HNF& h, int left, int right, int sign = 1) {
  return 2 * h.add(left / 2, right / 2, sign) + ((left & 1) ^ (right & 1));
}

bool exact_cover(const HNF& h, const std::vector<int>& sphere,
                 std::vector<std::uint8_t>& covered, int remaining) {
  if (remaining == 0) {
    return std::find(covered.begin(), covered.end(), 0) == covered.end();
  }
  const auto first = std::find(covered.begin(), covered.end(), 0);
  if (first == covered.end()) return false;
  const int uncovered = static_cast<int>(first - covered.begin());
  std::vector<std::uint8_t> tried(2 * h.order(), 0);
  for (int element : sphere) {
    const int shift = split_add(h, uncovered, element, -1);
    if (tried[shift]) continue;
    tried[shift] = 1;
    bool disjoint = true;
    for (int value : sphere) {
      if (covered[split_add(h, value, shift)]) {
        disjoint = false;
        break;
      }
    }
    if (!disjoint) continue;
    for (int value : sphere) covered[split_add(h, value, shift)] = 1;
    if (exact_cover(h, sphere, covered, remaining - 1)) return true;
    for (int value : sphere) covered[split_add(h, value, shift)] = 0;
  }
  return false;
}

bool has_tiling(const HNF& h, const std::vector<int>& sphere,
                int center_count) {
  std::vector<std::uint8_t> covered(2 * h.order(), 0);
  for (int element : sphere) covered[element] = 1;
  return exact_cover(h, sphere, covered, center_count - 1);
}

std::uint64_t euler_phi(int n) {
  std::uint64_t result = n;
  for (int prime = 2; prime * prime <= n; ++prime) {
    if (n % prime != 0) continue;
    result = result / prime * (prime - 1);
    while (n % prime == 0) n /= prime;
  }
  if (n > 1) result = result / n * (n - 1);
  return result;
}

std::uint64_t jordan_totient_three(int n) {
  std::uint64_t result = static_cast<std::uint64_t>(n) * n * n;
  int remainder = n;
  for (int prime = 2; prime * prime <= remainder; ++prime) {
    if (remainder % prime != 0) continue;
    const std::uint64_t cube = static_cast<std::uint64_t>(prime) * prime * prime;
    result = result / cube * (cube - 1);
    while (remainder % prime == 0) remainder /= prime;
  }
  if (remainder > 1) {
    const std::uint64_t cube =
        static_cast<std::uint64_t>(remainder) * remainder * remainder;
    result = result / cube * (cube - 1);
  }
  return result;
}

std::uint64_t hnf_count(int n) {
  std::uint64_t result = 0;
  for (int a = 1; a <= n; ++a) {
    if (n % a != 0) continue;
    const int quotient = n / a;
    for (int b = 1; b <= quotient; ++b) {
      if (quotient % b == 0) {
        result += static_cast<std::uint64_t>(a) * a * b;
      }
    }
  }
  return result;
}

struct Candidate {
  int centers;
  int order;
  HNF h;
  int sphere_size;
};

Candidate parse(const std::string& line) {
  std::istringstream input(line);
  Candidate candidate{};
  if (!(input >> candidate.centers >> candidate.order >> candidate.h.a >>
        candidate.h.b >> candidate.h.c >> candidate.h.x >> candidate.h.y >>
        candidate.h.z >> candidate.sphere_size)) {
    throw std::runtime_error("malformed candidate line");
  }
  std::string trailing;
  if (input >> trailing) throw std::runtime_error("trailing candidate field");
  return candidate;
}

std::string key(const Candidate& candidate) {
  std::ostringstream output;
  output << candidate.centers << ':' << candidate.order << ':' << candidate.h.a
         << ':' << candidate.h.b << ':' << candidate.h.c << ':' << candidate.h.x
         << ':' << candidate.h.y << ':' << candidate.h.z;
  return output.str();
}

}  // namespace

int main(int argc, char** argv) {
  if (argc < 2) {
    throw std::runtime_error("usage: checker candidate-file [candidate-file ...]");
  }

  std::uint64_t all_hnfs = 0;
  std::uint64_t cyclic_hnfs = 0;
  for (int order = 1; order <= kMaximumBaseOrder; ++order) {
    if (order % 2 != 0 && order % 3 != 0) continue;
    all_hnfs += hnf_count(order);
    const std::uint64_t phi = euler_phi(order);
    const std::uint64_t jordan = jordan_totient_three(order);
    if (phi == 0 || jordan % phi != 0) {
      throw std::runtime_error("invalid cyclic-kernel formula");
    }
    cyclic_hnfs += jordan / phi;
  }

  std::unordered_set<std::string> descriptors;
  std::uint64_t four_candidates = 0;
  std::uint64_t six_candidates = 0;
  std::uint64_t four_tilings = 0;
  std::uint64_t six_tilings = 0;
  for (int argument = 1; argument < argc; ++argument) {
    std::ifstream input(argv[argument]);
    if (!input) throw std::runtime_error("could not open candidate file");
    std::string line;
    int line_number = 0;
    while (std::getline(input, line)) {
      ++line_number;
      const Candidate candidate = parse(line);
      const HNF& h = candidate.h;
      if (candidate.order != 2 * h.order() || candidate.order <= 0 ||
          candidate.order > 2 * kMaximumBaseOrder ||
          (h.order() % 2 != 0 && h.order() % 3 != 0) ||
          h.a <= 0 || h.b <= 0 || h.c <= 0 || h.x < 0 || h.x >= h.a ||
          h.y < 0 || h.y >= h.a || h.z < 0 || h.z >= h.b ||
          cyclic_quotient(h)) {
        throw std::runtime_error("invalid HNF at line " +
                                 std::to_string(line_number));
      }
      const std::array<int, 6> steps = {
          h.image({1, 0, 0}), h.image({-1, 0, 0}),
          h.image({0, 1, 0}), h.image({0, -1, 0}),
          h.image({0, 0, 1}), h.image({0, 0, -1})};
      std::array<int, 6> sorted_steps = steps;
      std::sort(sorted_steps.begin(), sorted_steps.end());
      if (sorted_steps[0] == 0 ||
          std::adjacent_find(sorted_steps.begin(), sorted_steps.end()) !=
              sorted_steps.end()) {
        throw std::runtime_error("connection set is not simple degree six");
      }
      if (!descriptors.insert(key(candidate)).second) {
        throw std::runtime_error("duplicate candidate HNF");
      }

      const auto distance = full_distances(h);
      if (std::find(distance.begin(), distance.end(), -1) != distance.end()) {
        throw std::runtime_error("candidate quotient is disconnected");
      }
      std::vector<int> sphere;
      for (int element = 0; element < 2 * h.order(); ++element) {
        if (distance[element] == kRadius) sphere.push_back(element);
      }
      if (static_cast<int>(sphere.size()) != candidate.sphere_size ||
          candidate.centers * candidate.sphere_size != candidate.order) {
        throw std::runtime_error("sphere/count mismatch at line " +
                                 std::to_string(line_number));
      }
      const bool tiling = has_tiling(h, sphere, candidate.centers);
      if (candidate.centers == 4) {
        ++four_candidates;
        four_tilings += tiling ? 1 : 0;
      } else if (candidate.centers == 6) {
        ++six_candidates;
        six_tilings += tiling ? 1 : 0;
      } else {
        throw std::runtime_error("invalid center count");
      }
    }
  }

  std::cout << "eligible_hnfs=" << all_hnfs << '\n';
  std::cout << "cyclic_quotient_hnfs=" << cyclic_hnfs << '\n';
  std::cout << "noncyclic_quotient_hnfs=" << all_hnfs - cyclic_hnfs << '\n';
  std::cout << "candidate_hnfs=" << descriptors.size() << '\n';
  std::cout << "four_center_candidates_checked=" << four_candidates << '\n';
  std::cout << "six_center_candidates_checked=" << six_candidates << '\n';
  std::cout << "four_center_tilings=" << four_tilings << '\n';
  std::cout << "six_center_tilings=" << six_tilings << '\n';
}
