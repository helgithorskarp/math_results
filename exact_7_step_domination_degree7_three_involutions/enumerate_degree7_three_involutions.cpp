#include <algorithm>
#include <array>
#include <bit>
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <queue>
#include <stdexcept>
#include <vector>

namespace {

constexpr int kRadius = 7;
constexpr int kShellBound = 176;
constexpr int kMaximumOrder = 6 * kShellBound;

struct Word {
  int first;
  int second;
  int binary;
};

class BinaryQuotient {
 public:
  explicit BinaryQuotient(bool triple_relation)
      : triple_relation_(triple_relation), order_(triple_relation ? 4 : 8) {}

  int order() const { return order_; }
  int kernel_code() const { return triple_relation_ ? 7 : 0; }

  int coset(int value) const {
    value &= 7;
    return triple_relation_ ? std::min(value, value ^ 7) : value;
  }

  int representative(int coset) const { return coset; }
  int add(int left, int right) const {
    return coset(representative(left) ^ representative(right));
  }

 private:
  bool triple_relation_;
  int order_;
};

class Model {
 public:
  Model(BinaryQuotient quotient, int a, int b, int x, int phi_first,
        int phi_second)
      : quotient_(quotient),
        a_(a),
        b_(b),
        x_(x),
        phi_first_(phi_first),
        phi_second_(phi_second) {
    if (a_ <= 0 || b_ <= 0 || x_ < 0 || x_ >= a_) {
      throw std::runtime_error("invalid column HNF");
    }
    if (phi_first_ < 0 || phi_first_ >= quotient_.order() ||
        phi_second_ < 0 || phi_second_ >= quotient_.order()) {
      throw std::runtime_error("invalid gluing homomorphism");
    }
  }

  int order() const { return a_ * b_ * quotient_.order(); }
  int a() const { return a_; }
  int b() const { return b_; }
  int x() const { return x_; }
  int phi_first() const { return phi_first_; }
  int phi_second() const { return phi_second_; }
  const BinaryQuotient& quotient() const { return quotient_; }

  int encode(int first, int second, int binary) const {
    return ((second * a_ + first) * quotient_.order()) + binary;
  }

  std::array<int, 3> decode(int element) const {
    const int binary = element % quotient_.order();
    element /= quotient_.order();
    const int first = element % a_;
    const int second = element / a_;
    return {first, second, binary};
  }

  int image(int first, int second, int binary_vector) const {
    return reduce(first, second, quotient_.coset(binary_vector));
  }

  int add(int left, int right) const {
    const auto u = decode(left);
    const auto v = decode(right);
    return reduce(u[0] + v[0], u[1] + v[1],
                  quotient_.add(u[2], v[2]));
  }

  int inverse(int element) const {
    const auto value = decode(element);
    return reduce(-value[0], -value[1], value[2]);
  }

  int subtract(int left, int right) const { return add(left, inverse(right)); }

  std::vector<int> steps() const {
    const int first = image(1, 0, 0);
    const int second = image(0, 1, 0);
    std::vector<int> result = {
        first,
        inverse(first),
        second,
        inverse(second),
        image(0, 0, 1),
        image(0, 0, 2),
        image(0, 0, 4),
    };
    std::sort(result.begin(), result.end());
    result.erase(std::unique(result.begin(), result.end()), result.end());
    return result;
  }

  bool has_simple_degree_seven_connection_set() const {
    const auto connection = steps();
    return connection.size() == 7 && connection.front() != 0;
  }

 private:
  static int positive_mod(int value, int modulus) {
    value %= modulus;
    if (value < 0) value += modulus;
    return value;
  }

  int reduce(int first, int second, int binary) const {
    // Column-HNF relations are
    //   (a,0,0) = (0,0,phi_first),
    //   (x,b,0) = (0,0,phi_second).
    // Reducing by a relation therefore adds its binary image.
    const int reduced_second = positive_mod(second, b_);
    const int second_quotient = (second - reduced_second) / b_;
    first -= second_quotient * x_;
    if (second_quotient & 1) {
      binary = quotient_.add(binary, phi_second_);
    }

    const int reduced_first = positive_mod(first, a_);
    const int first_quotient = (first - reduced_first) / a_;
    if (first_quotient & 1) {
      binary = quotient_.add(binary, phi_first_);
    }
    return encode(reduced_first, reduced_second, binary);
  }

  BinaryQuotient quotient_;
  int a_;
  int b_;
  int x_;
  int phi_first_;
  int phi_second_;
};

std::vector<Word> words(int minimum_norm, int maximum_norm) {
  std::vector<Word> result;
  for (int first = -maximum_norm; first <= maximum_norm; ++first) {
    for (int second = -maximum_norm; second <= maximum_norm; ++second) {
      for (int binary = 0; binary < 8; ++binary) {
        const int norm = std::abs(first) + std::abs(second) +
                         std::popcount(static_cast<unsigned>(binary));
        if (minimum_norm <= norm && norm <= maximum_norm) {
          result.push_back({first, second, binary});
        }
      }
    }
  }
  return result;
}

std::vector<int> coefficient_sphere(const Model& model,
                                    const std::vector<Word>& shorter,
                                    const std::vector<Word>& shell) {
  std::vector<std::uint8_t> state(model.order(), 0);
  for (const Word& word : shorter) {
    state[model.image(word.first, word.second, word.binary)] = 1;
  }
  for (const Word& word : shell) {
    const int element = model.image(word.first, word.second, word.binary);
    if (state[element] == 0) state[element] = 2;
  }
  std::vector<int> result;
  for (int element = 0; element < model.order(); ++element) {
    if (state[element] == 2) result.push_back(element);
  }
  return result;
}

std::vector<int> bfs_sphere(const Model& model) {
  const auto steps = model.steps();
  if (steps.size() != 7 || steps.front() == 0) {
    throw std::runtime_error("BFS called on nonsimple connection set");
  }
  std::vector<int> distance(model.order(), -1);
  std::queue<int> queue;
  distance[0] = 0;
  queue.push(0);
  while (!queue.empty()) {
    const int element = queue.front();
    queue.pop();
    for (int step : steps) {
      const int neighbour = model.add(element, step);
      if (distance[neighbour] != -1) continue;
      distance[neighbour] = distance[element] + 1;
      queue.push(neighbour);
    }
  }
  if (std::find(distance.begin(), distance.end(), -1) != distance.end()) {
    throw std::runtime_error("marked generators failed to generate quotient");
  }
  std::vector<int> result;
  for (int element = 0; element < model.order(); ++element) {
    if (distance[element] == kRadius) result.push_back(element);
  }
  return result;
}

bool clique_search(const Model& model, const std::vector<int>& candidates,
                   const std::vector<std::uint8_t>& forbidden, int start,
                   int remaining, std::vector<int>& chosen) {
  if (remaining == 0) return true;
  if (static_cast<int>(candidates.size()) - start < remaining) return false;
  for (int index = start;
       index + remaining <= static_cast<int>(candidates.size()); ++index) {
    const int candidate = candidates[index];
    bool compatible = true;
    for (int previous : chosen) {
      if (forbidden[model.subtract(candidate, previous)]) {
        compatible = false;
        break;
      }
    }
    if (!compatible) continue;
    chosen.push_back(candidate);
    if (clique_search(model, candidates, forbidden, index + 1,
                      remaining - 1, chosen)) {
      return true;
    }
    chosen.pop_back();
  }
  return false;
}

bool has_translate_tiling(const Model& model, const std::vector<int>& sphere,
                          int center_count) {
  if (center_count * static_cast<int>(sphere.size()) != model.order()) {
    return false;
  }
  std::vector<std::uint8_t> forbidden(model.order(), 0);
  for (int left : sphere) {
    for (int right : sphere) {
      forbidden[model.subtract(left, right)] = 1;
    }
  }
  std::vector<int> candidates;
  for (int shift = 1; shift < model.order(); ++shift) {
    if (!forbidden[shift]) candidates.push_back(shift);
  }
  std::vector<int> chosen;
  return clique_search(model, candidates, forbidden, 0, center_count - 1,
                       chosen);
}

struct Counts {
  std::uint64_t marked_models = 0;
  std::uint64_t degree_seven_models = 0;
  std::uint64_t four_candidates = 0;
  std::uint64_t six_candidates = 0;
  std::uint64_t four_tilings = 0;
  std::uint64_t six_tilings = 0;
};

}  // namespace

int main(int argc, char** argv) {
  if (argc != 2) {
    throw std::runtime_error("usage: enumerator /scratch/candidates.txt");
  }
  std::ofstream output(argv[1]);
  if (!output) throw std::runtime_error("could not open candidate output");

  const auto shorter = words(0, kRadius - 1);
  const auto shell = words(kRadius, kRadius);
  if (shorter.size() != 416 || shell.size() != kShellBound) {
    throw std::runtime_error("unexpected mixed Lee/binary ball or shell size");
  }

  std::array<Counts, 2> by_kernel{};
  const auto start = std::chrono::steady_clock::now();

  for (int relation_index = 0; relation_index < 2; ++relation_index) {
    const BinaryQuotient quotient(relation_index == 1);
    Counts& counts = by_kernel[relation_index];
    const int maximum_lattice_index = kMaximumOrder / quotient.order();
    for (int lattice_index = 1; lattice_index <= maximum_lattice_index;
         ++lattice_index) {
      for (int a = 1; a <= lattice_index; ++a) {
        if (lattice_index % a != 0) continue;
        const int b = lattice_index / a;
        for (int x = 0; x < a; ++x) {
          for (int phi_first = 0; phi_first < quotient.order(); ++phi_first) {
            for (int phi_second = 0; phi_second < quotient.order();
                 ++phi_second) {
              const Model model(quotient, a, b, x, phi_first, phi_second);
              ++counts.marked_models;
              if (!model.has_simple_degree_seven_connection_set()) continue;
              ++counts.degree_seven_models;

              const auto sphere = coefficient_sphere(model, shorter, shell);
              if (sphere.size() > kShellBound) {
                throw std::runtime_error("sphere exceeds proved shell bound");
              }
              for (int center_count : {4, 6}) {
                if (center_count * static_cast<int>(sphere.size()) !=
                    model.order()) {
                  continue;
                }
                const auto bfs = bfs_sphere(model);
                if (bfs != sphere) {
                  throw std::runtime_error(
                      "coefficient and BFS spheres disagree on candidate");
                }
                output << center_count << ' ' << quotient.kernel_code() << ' '
                       << a << ' ' << b << ' ' << x << ' ' << phi_first << ' '
                       << phi_second << ' ' << sphere.size() << '\n';
                const bool tiling =
                    has_translate_tiling(model, sphere, center_count);
                if (center_count == 4) {
                  ++counts.four_candidates;
                  counts.four_tilings += tiling ? 1 : 0;
                } else {
                  ++counts.six_candidates;
                  counts.six_tilings += tiling ? 1 : 0;
                }
              }
            }
          }
        }
      }
    }
  }

  output.flush();
  if (!output) throw std::runtime_error("candidate output failure");

  Counts total;
  for (int relation_index = 0; relation_index < 2; ++relation_index) {
    const auto& counts = by_kernel[relation_index];
    const int kernel = relation_index == 0 ? 0 : 7;
    std::cout << "kernel=" << kernel
              << " marked_models=" << counts.marked_models
              << " degree_seven_models=" << counts.degree_seven_models
              << " four_candidates=" << counts.four_candidates
              << " six_candidates=" << counts.six_candidates
              << " four_tilings=" << counts.four_tilings
              << " six_tilings=" << counts.six_tilings << '\n';
    total.marked_models += counts.marked_models;
    total.degree_seven_models += counts.degree_seven_models;
    total.four_candidates += counts.four_candidates;
    total.six_candidates += counts.six_candidates;
    total.four_tilings += counts.four_tilings;
    total.six_tilings += counts.six_tilings;
  }
  const auto elapsed = std::chrono::duration<double>(
      std::chrono::steady_clock::now() - start);
  std::cout << "radius=" << kRadius << '\n';
  std::cout << "maximum_group_order=" << kMaximumOrder << '\n';
  std::cout << "marked_models=" << total.marked_models << '\n';
  std::cout << "degree_seven_models=" << total.degree_seven_models << '\n';
  std::cout << "four_center_counting_candidates=" << total.four_candidates
            << '\n';
  std::cout << "six_center_counting_candidates=" << total.six_candidates
            << '\n';
  std::cout << "four_center_tilings=" << total.four_tilings << '\n';
  std::cout << "six_center_tilings=" << total.six_tilings << '\n';
  std::cout << "elapsed_seconds=" << elapsed.count() << '\n';
  const std::array<Counts, 2> expected = {{
      {923584, 902571, 354, 16312, 0, 0},
      {920400, 907767, 33, 4226, 0, 0},
  }};
  for (int relation_index = 0; relation_index < 2; ++relation_index) {
    const Counts& actual = by_kernel[relation_index];
    const Counts& wanted = expected[relation_index];
    if (actual.marked_models != wanted.marked_models ||
        actual.degree_seven_models != wanted.degree_seven_models ||
        actual.four_candidates != wanted.four_candidates ||
        actual.six_candidates != wanted.six_candidates ||
        actual.four_tilings != wanted.four_tilings ||
        actual.six_tilings != wanted.six_tilings) {
      throw std::runtime_error("unexpected complete-enumeration result");
    }
  }
  return 0;
}
