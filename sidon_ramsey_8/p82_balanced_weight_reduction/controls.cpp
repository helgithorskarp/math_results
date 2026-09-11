#include "search.hpp"
#include <random>
// Query oracle scans masks without either index or weight-order arrays.
std::vector<U> direct(const Catalog &c, U d, int lo, int hi) {
  std::vector<U> a;
  for (U m : c.masks)
    if (!(m & ~d) && c.weight(m) >= lo && c.weight(m) <= hi)
      a.push_back(m);
  return a;
}
// Independent combination enumeration: choose r-1 unordered catalog rows and
// validate the final complement, which must be a lightest class.
bool brute(const Catalog &c, U d, int r, size_t start, int upper) {
  if (r == 1)
    return c.weight(d) <= upper && sidon(d, 0);
  for (size_t i = start; i < c.masks.size(); ++i) {
    U a = c.masks[i];
    if (!(a & ~d) &&
        brute(c, d ^ a, r - 1, i + 1, std::min(upper, c.weights[i])))
      return true;
  }
  return false;
}
int main(int argc, char **argv) {
  try {
    if (argc != 4)
      throw std::runtime_error("weights fixture partition80");
    Weights w(argv[1]);
    std::vector<U> rows, p80;
    std::string line;
    for (auto spec : {std::pair<const char *, std::vector<U> *>(argv[2], &rows),
                      {argv[3], &p80}}) {
      std::ifstream in(spec.first);
      while (std::getline(in, line)) {
        U a = readset(line);
        if (pop(a) != 10 || !sidon(a, 0) || !sidon(a, 1))
          throw std::runtime_error("fixture");
        spec.second->push_back(a);
      }
      if (!in.eof())
        throw std::runtime_error("fixture input");
    }
    std::sort(rows.begin(), rows.end());
    if (std::adjacent_find(rows.begin(), rows.end()) != rows.end() ||
        rows.size() < 129 || p80.size() != 8)
      throw std::runtime_error("fixture size");
    Catalog c(rows, w, 10, 0, 1), radix(rows, w, 10, 0, 0);
    std::mt19937_64 rng(20260911);
    uint64_t checks = 0;
    for (int t = 0; t < 3000; ++t) {
      U d = universe;
      int lo = 0, hi = cap;
      if (t % 4 == 0)
        d = rows[size_t(rng() % rows.size())] |
            rows[size_t(rng() % rows.size())];
      if (t % 4 == 1)
        d &= ~(U(1) << (rng() % 82));
      if (t % 4 == 2)
        d = (U(rng()) | (U(rng() & ((1 << 18) - 1)) << 64));
      if (t % 3 == 0) {
        lo = int(rng() % 4000001);
        hi = int(rng() % 4000001);
        if (lo > hi)
          std::swap(lo, hi);
      }
      if (t % 7 == 0)
        lo = hi = w(rows[size_t(rng() % rows.size())]);
      auto a = direct(c, d, lo, hi);
      Search s{w, c, 0, 100000};
      if (s.query(d, lo, hi) != a || c.query(d, lo, hi) != a ||
          radix.query(d, lo, hi) != a)
        throw std::runtime_error("query oracle");
      ++checks;
    }
    uint64_t positives = 0, negatives = 0;
    // All six-class unions of the published P80 partition are positive
    // controls.
    auto small = p80;
    std::sort(small.begin(), small.end());
    Catalog tiny(small, w, 10, 0, 1);
    for (int mask = 0; mask < 256; ++mask) {
      if (__builtin_popcount(unsigned(mask)) < 2 ||
          __builtin_popcount(unsigned(mask)) > 6)
        continue;
      U d = 0;
      int r = 0;
      for (int i = 0; i < 8; ++i)
        if (mask & (1 << i)) {
          if (d & p80[size_t(i)])
            throw std::runtime_error("p80 overlap");
          d |= p80[size_t(i)];
          ++r;
        }
      if (!brute(tiny, d, r, 0, cap))
        throw std::runtime_error("positive oracle");
      for (int m : {0, 1}) {
        Search s{w, tiny, m, 100000};
        if (!s.visit(d, r, cap))
          throw std::runtime_error("positive search");
        U used = 0;
        for (U a : s.chosen) {
          if (pop(a) != 10 || !sidon(a, 0) || (a & used))
            throw std::runtime_error("positive witness");
          used |= a;
        }
        if (used != d)
          throw std::runtime_error("positive coverage");
      }
      ++positives;
    }
    // Swap one occupied point for an absent point; compare the complete
    // decision.
    for (int t = 0; t < 300; ++t) {
      U d = p80[0] | p80[1] | p80[2];
      int x = first(d);
      d ^= U(1) << x;
      int y = int(rng() % 82);
      while (d & (U(1) << y))
        y = (y + 1) % 82;
      d |= U(1) << y;
      bool expected = brute(tiny, d, 3, 0, cap);
      for (int m : {0, 1}) {
        Search s{w, tiny, m, 100000};
        if (s.visit(d, 3, cap) != expected)
          throw std::runtime_error("decision oracle");
      }
      if (!expected)
        ++negatives;
    }
    // The limit is an explicit unknown, never a false exclusion.
    bool limited = false;
    try {
      Search s{w, tiny, 1, 1};
      s.visit(p80[0] | p80[1] | p80[2], 3, cap);
    } catch (Limit &) {
      limited = true;
    }
    if (!limited)
      throw std::runtime_error("budget control");
    std::cout << "{\"verified\":true,\"query_oracle_checks\":" << checks
              << ",\"positive_domains\":" << positives
              << ",\"negative_domains\":" << negatives
              << ",\"budget_unknown\":true}\n";
  } catch (std::exception &e) {
    std::cerr << e.what() << '\n';
    return 1;
  }
}
