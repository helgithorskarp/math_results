#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <numeric>
#include <stdexcept>
#include <string>
#include <vector>

namespace {

// The remaining pure-three-pair case of exact 7-step domination in finite
// abelian Cayley graphs, represented as quotients of the cubic lattice.
constexpr int kRadius = 7;

using Vec = std::array<int, 3>;

struct HNF {
  int a;
  int b;
  int c;
  int x;
  int y;
  int z;

  int order() const { return a * b * c; }

  Vec reduce(Vec v) const {
    auto positive_mod = [](int value, int modulus) {
      value %= modulus;
      if (value < 0) value += modulus;
      return value;
    };
    const int old2 = v[2];
    const int r2 = positive_mod(old2, c);
    const int q2 = (old2 - r2) / c;
    v[0] -= q2 * y;
    v[1] -= q2 * z;
    v[2] = r2;

    const int old1 = v[1];
    const int r1 = positive_mod(old1, b);
    const int q1 = (old1 - r1) / b;
    v[0] -= q1 * x;
    v[1] = r1;
    v[0] = positive_mod(v[0], a);
    return v;
  }

  int encode(const Vec& v) const { return (v[2] * b + v[1]) * a + v[0]; }

  int image(Vec v) const { return encode(reduce(v)); }

  Vec decode(int value) const {
    Vec result{};
    result[0] = value % a;
    value /= a;
    result[1] = value % b;
    result[2] = value / b;
    return result;
  }

  int add(int left, int right, int sign = 1) const {
    Vec u = decode(left);
    const Vec v = decode(right);
    for (int i = 0; i < 3; ++i) u[i] += sign * v[i];
    return image(u);
  }
};

std::vector<int> divisors(int n) {
  std::vector<int> result;
  for (int d = 1; d * d <= n; ++d) {
    if (n % d != 0) continue;
    result.push_back(d);
    if (d * d != n) result.push_back(n / d);
  }
  std::sort(result.begin(), result.end());
  return result;
}

int element_order(const HNF& h, const Vec& value,
                  const std::vector<int>& order_divisors) {
  for (int d : order_divisors) {
    if (h.image({d * value[0], d * value[1], d * value[2]}) == 0) return d;
  }
  throw std::runtime_error("element order did not divide group order");
}

Vec canonical_sign(Vec value) {
  for (int coordinate : value) {
    if (coordinate == 0) continue;
    if (coordinate < 0) {
      for (int& entry : value) entry = -entry;
    }
    break;
  }
  return value;
}

int ternary_key(const Vec& value) {
  return (value[0] + 1) * 9 + (value[1] + 1) * 3 + value[2] + 1;
}

const std::array<Vec, 13> kSignatureForms = {{
    {1, 0, 0}, {0, 1, 0}, {0, 0, 1},
    {1, 1, 0}, {1, -1, 0}, {1, 0, 1}, {1, 0, -1},
    {0, 1, 1}, {0, 1, -1},
    {1, 1, 1}, {1, 1, -1}, {1, -1, 1}, {-1, 1, 1}
}};

bool signature_canonical(const HNF& h,
                         const std::vector<int>& order_divisors) {
  std::array<int, 27> orders{};
  for (int u = -1; u <= 1; ++u) {
    for (int v = -1; v <= 1; ++v) {
      for (int w = -1; w <= 1; ++w) {
        if (u == 0 && v == 0 && w == 0) continue;
        Vec coefficient = canonical_sign({u, v, w});
        const int key = ternary_key(coefficient);
        if (orders[key] == 0) {
          orders[key] = element_order(h, coefficient, order_divisors);
        }
      }
    }
  }

  auto signature = [&](const std::array<int, 3>& permutation,
                       const std::array<int, 3>& signs) {
    std::array<int, kSignatureForms.size()> result{};
    for (std::size_t i = 0; i < kSignatureForms.size(); ++i) {
      Vec transformed{};
      for (int j = 0; j < 3; ++j) {
        transformed[permutation[j]] = signs[j] * kSignatureForms[i][j];
      }
      transformed = canonical_sign(transformed);
      result[i] = orders[ternary_key(transformed)];
    }
    return result;
  };

  const std::array<int, 3> identity = {0, 1, 2};
  const std::array<int, 3> positive = {1, 1, 1};
  const auto own = signature(identity, positive);
  auto best = own;
  std::array<int, 3> permutation = {0, 1, 2};
  do {
    for (int mask = 0; mask < 8; ++mask) {
      std::array<int, 3> signs{};
      for (int i = 0; i < 3; ++i) signs[i] = (mask & (1 << i)) ? -1 : 1;
      best = std::min(best, signature(permutation, signs));
    }
  } while (std::next_permutation(permutation.begin(), permutation.end()));
  return own == best;
}

bool cyclic_quotient(const HNF& h) {
  int minors = 0;
  const std::array<int, 6> values = {
      h.a * h.b, h.a * h.z, h.x * h.z - h.b * h.y,
      h.a * h.c, h.x * h.c, h.b * h.c};
  for (int value : values) minors = std::gcd(minors, std::abs(value));
  return minors == 1;
}

bool degree_six(const HNF& h) {
  const std::array<Vec, 3> basis = {{{1, 0, 0}, {0, 1, 0}, {0, 0, 1}}};
  std::array<int, 3> images{};
  std::array<int, 3> inverses{};
  for (int i = 0; i < 3; ++i) {
    images[i] = h.image(basis[i]);
    inverses[i] = h.image({-basis[i][0], -basis[i][1], -basis[i][2]});
    if (images[i] == 0 || images[i] == inverses[i]) return false;
  }
  for (int i = 0; i < 3; ++i) {
    for (int j = i + 1; j < 3; ++j) {
      if (images[i] == images[j] || images[i] == inverses[j]) return false;
    }
  }
  return true;
}

std::vector<Vec> coefficient_vectors(int minimum_norm, int maximum_norm) {
  std::vector<Vec> result;
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

std::vector<int> radius_sphere(const HNF& h,
                               const std::vector<Vec>& shorter,
                               const std::vector<Vec>& shell) {
  std::vector<std::uint8_t> state(h.order(), 0);
  for (const Vec& coefficient : shorter) state[h.image(coefficient)] = 1;
  for (const Vec& coefficient : shell) {
    int element = h.image(coefficient);
    if (state[element] == 0) state[element] = 2;
  }
  std::vector<int> result;
  for (int element = 0; element < h.order(); ++element) {
    if (state[element] == 2) result.push_back(element);
  }
  return result;
}

bool clique_search(const HNF& h, const std::vector<int>& candidates,
                   const std::vector<std::uint8_t>& forbidden, int start,
                   int remaining, std::vector<int>& chosen) {
  if (remaining == 0) return true;
  if (static_cast<int>(candidates.size()) - start < remaining) return false;
  for (int index = start;
       index + remaining <= static_cast<int>(candidates.size()); ++index) {
    const int candidate = candidates[index];
    bool compatible = true;
    for (int previous : chosen) {
      if (forbidden[h.add(candidate, previous, -1)]) {
        compatible = false;
        break;
      }
    }
    if (!compatible) continue;
    chosen.push_back(candidate);
    if (clique_search(h, candidates, forbidden, index + 1, remaining - 1,
                      chosen)) return true;
    chosen.pop_back();
  }
  return false;
}

bool has_translate_tiling(const HNF& h, const std::vector<int>& sphere,
                          int center_count) {
  if (static_cast<int>(sphere.size()) * center_count != h.order()) return false;
  std::vector<std::uint8_t> forbidden(h.order(), 0);
  for (int left : sphere) {
    for (int right : sphere) forbidden[h.add(left, right, -1)] = 1;
  }
  std::vector<int> candidates;
  for (int shift = 1; shift < h.order(); ++shift) {
    if (!forbidden[shift]) candidates.push_back(shift);
  }
  std::vector<int> chosen;
  return clique_search(h, candidates, forbidden, 0, center_count - 1, chosen);
}

struct Counts {
  std::uint64_t hnfs = 0;
  std::uint64_t noncyclic = 0;
  std::uint64_t degree6 = 0;
  std::uint64_t signature_representatives = 0;
  std::uint64_t four_candidates = 0;
  std::uint64_t six_candidates = 0;
  std::uint64_t four_tilings = 0;
  std::uint64_t six_tilings = 0;
};

}  // namespace

int main(int argc, char** argv) {
  if (argc != 4) {
    throw std::runtime_error(
        "usage: enumerator minimum_order maximum_order candidates");
  }
  const int minimum_order = std::stoi(argv[1]);
  const int maximum_order = std::stoi(argv[2]);
  std::ofstream output(argv[3]);
  if (!output) throw std::runtime_error("could not open candidate output");

  const auto shorter = coefficient_vectors(0, kRadius - 1);
  const auto shell = coefficient_vectors(kRadius, kRadius);
  if (shorter.size() != 377 || shell.size() != 198) {
    throw std::runtime_error("unexpected Lee ball or shell size");
  }

  Counts counts;
  const auto start = std::chrono::steady_clock::now();
  for (int order = minimum_order; order <= maximum_order; ++order) {
    if (order % 4 != 0 && order % 6 != 0) continue;
    const auto order_divisors = divisors(order);
    for (int a = 1; a <= order; ++a) {
      if (order % a != 0) continue;
      const int after_a = order / a;
      for (int b = 1; b <= after_a; ++b) {
        if (after_a % b != 0) continue;
        const int c = after_a / b;
        for (int x = 0; x < a; ++x) {
          for (int y = 0; y < a; ++y) {
            for (int z = 0; z < b; ++z) {
              const HNF h{a, b, c, x, y, z};
              ++counts.hnfs;
              if (cyclic_quotient(h)) continue;
              ++counts.noncyclic;
              if (!degree_six(h)) continue;
              ++counts.degree6;
              if (!signature_canonical(h, order_divisors)) continue;
              ++counts.signature_representatives;
              const auto sphere = radius_sphere(h, shorter, shell);
              auto candidate = [&](int center_count) {
                output << center_count << ' ' << order << ' ' << a << ' ' << b
                       << ' ' << c << ' ' << x << ' ' << y << ' ' << z << ' '
                       << sphere.size() << '\n';
                return has_translate_tiling(h, sphere, center_count);
              };
              if (4 * static_cast<int>(sphere.size()) == order) {
                ++counts.four_candidates;
                counts.four_tilings += candidate(4) ? 1 : 0;
              }
              if (6 * static_cast<int>(sphere.size()) == order) {
                ++counts.six_candidates;
                counts.six_tilings += candidate(6) ? 1 : 0;
              }
            }
          }
        }
      }
    }
    if (order % 100 == 0) {
      const auto seconds = std::chrono::duration<double>(
          std::chrono::steady_clock::now() - start).count();
      std::cerr << "order=" << order << " hnfs=" << counts.hnfs
                << " reps=" << counts.signature_representatives
                << " seconds=" << seconds << '\n';
    }
  }
  output.flush();
  if (!output) throw std::runtime_error("candidate output failure");
  const auto seconds = std::chrono::duration<double>(
      std::chrono::steady_clock::now() - start).count();
  std::cout << "minimum_order=" << minimum_order << '\n';
  std::cout << "maximum_order=" << maximum_order << '\n';
  std::cout << "hnfs=" << counts.hnfs << '\n';
  std::cout << "noncyclic_hnfs=" << counts.noncyclic << '\n';
  std::cout << "degree_six_hnfs=" << counts.degree6 << '\n';
  std::cout << "signature_representatives=" << counts.signature_representatives << '\n';
  std::cout << "four_candidates=" << counts.four_candidates << '\n';
  std::cout << "six_candidates=" << counts.six_candidates << '\n';
  std::cout << "four_tilings=" << counts.four_tilings << '\n';
  std::cout << "six_tilings=" << counts.six_tilings << '\n';
  std::cout << "seconds=" << seconds << '\n';
  if (minimum_order == 1 && maximum_order == 1188 &&
      (counts.hnfs != 563799191 || counts.noncyclic != 120624452 ||
       counts.degree6 != 118667394 ||
       counts.signature_representatives != 15797397 ||
       counts.four_candidates != 3062 || counts.six_candidates != 73645 ||
       counts.four_tilings != 0 || counts.six_tilings != 0)) {
    throw std::runtime_error("unexpected complete enumeration result");
  }
}
