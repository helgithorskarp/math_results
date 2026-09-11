#pragma once
// Exact catalogs. Derived in-memory rows must come from validated Sidon data.
#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <numeric>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>
using U = __uint128_t;
constexpr U universe = (U(1) << 82) - 1;
constexpr int cap = 4000000, total_weight = 30884468;

int integer(const char *s) {
  size_t n = 0;
  int x = std::stoi(s, &n);
  if (s[n])
    throw std::runtime_error("integer");
  return x;
}
int first(U x) {
  if (!x)
    throw std::runtime_error("first(0)");
  return uint64_t(x) ? __builtin_ctzll(uint64_t(x))
                     : 64 + __builtin_ctzll(uint64_t(x >> 64));
}
int pop(U x) {
  return __builtin_popcountll(uint64_t(x)) +
         __builtin_popcountll(uint64_t(x >> 64));
}
void printset(U m, std::ostream &out) {
  out << '[';
  bool comma = false;
  while (m) {
    int x = first(m);
    m &= m - 1;
    if (comma)
      out << ',';
    comma = true;
    out << x;
  }
  out << ']';
}
bool sidon(U mask, int method) {
  std::vector<int> a;
  while (mask) {
    a.push_back(first(mask));
    mask &= mask - 1;
  }
  std::array<bool, 167> used{};
  for (size_t i = 0; i < a.size(); ++i)
    for (size_t j = i + size_t(method); j < a.size(); ++j) {
      size_t x = size_t(method ? a[j] - a[i] : a[j] + a[i]);
      if (used[x])
        return false;
      used[x] = true;
    }
  return true;
}
U readset(const std::string &line) {
  std::istringstream in(line);
  int x;
  U mask = 0;
  while (in >> x) {
    if (x < 0 || x >= 82 || (mask & (U(1) << x)))
      throw std::runtime_error("point");
    mask |= U(1) << x;
  }
  if (!in.eof())
    throw std::runtime_error("set token");
  return mask;
}
struct Weights {
  std::array<int, 82> w{};
  explicit Weights(const char *path) {
    std::ifstream in(path);
    for (int &x : w)
      if (!(in >> x) || x < 0 || x > 1000000)
        throw std::runtime_error("weight");
    std::string extra;
    if (in >> extra)
      throw std::runtime_error("extra weight");
  }
  int operator()(U m) const {
    int sum = 0;
    while (m) {
      int x = first(m);
      m &= m - 1;
      sum += w[size_t(x)];
    }
    return sum;
  }
};
struct Catalog {
  const Weights &weight;
  int size, minweight, method;
  std::vector<U> masks;
  std::vector<int> weights;
  struct Node {
    U common;
    uint32_t left, right;
    int maximum;
  };
  std::vector<Node> nodes;
  static constexpr uint32_t leaf = uint32_t(1) << 31;
  uint32_t root = leaf;
  std::vector<size_t> order;
  std::vector<int> ordered_weights;
  std::array<std::vector<uint64_t>, 82> incidence;
  std::array<int, 82> point_order{};
  U common(uint32_t id) const {
    return id & leaf ? masks[id & ~leaf] : nodes[id].common;
  }
  int maximum(uint32_t id) const {
    return id & leaf ? weights[id & ~leaf] : nodes[id].maximum;
  }
  uint32_t build(size_t lo, size_t hi) {
    if (hi - lo == 1)
      return leaf | uint32_t(lo);
    U d = masks[lo] ^ masks[hi - 1];
    int bit = uint64_t(d >> 64) ? 127 - __builtin_clzll(uint64_t(d >> 64))
                                : 63 - __builtin_clzll(uint64_t(d));
    U target = (masks[lo] >> bit << bit) | (U(1) << bit);
    size_t mid =
        size_t(std::lower_bound(masks.begin() + std::ptrdiff_t(lo),
                                masks.begin() + std::ptrdiff_t(hi), target) -
               masks.begin());
    if (mid == lo || mid == hi)
      throw std::runtime_error("radix split");
    uint32_t id = uint32_t(nodes.size());
    nodes.push_back({0, 0, 0, 0});
    uint32_t l = build(lo, mid), r = build(mid, hi);
    nodes[id] = {common(l) & common(r), l, r, std::max(maximum(l), maximum(r))};
    return id;
  }
  Catalog(const char *path, const Weights &w, int k, int cut, int alg)
      : weight(w), size(k), minweight(cut), method(alg) {
    if (k < 2 || k > 12 || cut < 0 || (alg != 0 && alg != 1))
      throw std::runtime_error("catalog parameters");
    std::ifstream in(path, std::ios::binary);
    if (!in)
      throw std::runtime_error("catalog input");
    std::array<unsigned char, 12> a{};
    while (in.read(reinterpret_cast<char *>(a.data()), k)) {
      U m = 0;
      for (int i = 0; i < k; ++i) {
        if (a[size_t(i)] >= 82 || (i && a[size_t(i - 1)] >= a[size_t(i)]))
          throw std::runtime_error("catalog point");
        m |= U(1) << a[size_t(i)];
      }
      int v = weight(m);
      if (v < cut || !sidon(m, alg) || (!masks.empty() && m <= masks.back()))
        throw std::runtime_error("catalog set/order/weight");
      masks.push_back(m);
      weights.push_back(v);
    }
    if (!in.eof() || in.gcount() || masks.size() >= leaf)
      throw std::runtime_error("catalog read");
    initialize();
  }
  Catalog(std::vector<U> rows, const Weights &w, int k, int cut, int alg)
      : weight(w), size(k), minweight(cut), method(alg),
        masks(std::move(rows)) {
    if (k < 2 || k > 12 || cut < 0 || (alg != 0 && alg != 1) ||
        masks.size() >= leaf)
      throw std::runtime_error("memory catalog parameters");
    U last = 0;
    for (U a : masks) {
      int z = weight(a);
      // Internal rows come only from a query of the directly validated global
      // catalog.
      if (a <= last || (a & ~universe) || pop(a) != k || z < cut)
        throw std::runtime_error("memory catalog entry");
      last = a;
      weights.push_back(z);
    }
    initialize();
  }
  void initialize() {
    if (masks.empty())
      return;
    if (!method) {
      nodes.reserve(masks.size() - 1);
      root = build(0, masks.size());
      return;
    }
    order.resize(masks.size());
    std::iota(order.begin(), order.end(), 0);
    for (int z : weights)
      if (z < 0 || z > cap)
        throw std::runtime_error("radix weight range");
    // Stable LSD radix sort of cap-weight; original mask order breaks ties.
    std::vector<size_t> temporary(order.size());
    for (int shift : {0, 11}) {
      std::array<size_t, 2048> counts{}, offsets{};
      for (size_t id : order)
        ++counts[(cap - weights[id]) >> shift & 2047];
      size_t total = 0;
      for (size_t i = 0; i < counts.size(); ++i) {
        offsets[i] = total;
        total += counts[i];
      }
      for (size_t id : order)
        temporary[offsets[(cap - weights[id]) >> shift & 2047]++] = id;
      order.swap(temporary);
    }
    for (size_t i = 0; i < order.size(); ++i) {
      if (order[i] >= masks.size())
        throw std::runtime_error("order range");
      if (i && (weights[order[i]] > weights[order[i - 1]] ||
                (weights[order[i]] == weights[order[i - 1]] &&
                 order[i] <= order[i - 1])))
        throw std::runtime_error("strict weight order");
    }
    size_t words = (masks.size() + 63) / 64;
    for (auto &v : incidence)
      v.resize(words);
    std::array<size_t, 82> frequencies{};
    for (size_t i = 0; i < order.size(); ++i) {
      ordered_weights.push_back(weights[order[i]]);
      U m = masks[order[i]];
      while (m) {
        int p = first(m);
        m &= m - 1;
        incidence[size_t(p)][i / 64] |= uint64_t(1) << (i % 64);
        ++frequencies[size_t(p)];
      }
    }
    std::iota(point_order.begin(), point_order.end(), 0);
    std::stable_sort(point_order.begin(), point_order.end(),
                     [&](int a0, int b) {
                       return frequencies[size_t(a0)] > frequencies[size_t(b)];
                     });
  }
  void radix(uint32_t id, U forbidden, int lower, int upper,
             std::vector<U> &out) const {
    if (maximum(id) < lower || (common(id) & forbidden))
      return;
    if (id & leaf) {
      if (weights[id & ~leaf] <= upper)
        out.push_back(masks[id & ~leaf]);
      return;
    }
    radix(nodes[id].left, forbidden, lower, upper, out);
    radix(nodes[id].right, forbidden, lower, upper, out);
  }
  std::vector<U> query(U domain, int lower, int upper) const {
    std::vector<U> answer;
    if (masks.empty() || lower > upper)
      return answer;
    if (!method) {
      radix(root, universe ^ domain, lower, upper, answer);
      return answer;
    }
    auto begin =
        std::lower_bound(ordered_weights.begin(), ordered_weights.end(), upper,
                         std::greater<>());
    auto end = std::upper_bound(ordered_weights.begin(), ordered_weights.end(),
                                lower, std::greater<>());
    size_t lo = size_t(begin - ordered_weights.begin()),
           hi = size_t(end - ordered_weights.begin());
    if (lo >= hi)
      return answer;
    std::array<int, 82> forbidden{};
    size_t count = 0;
    for (int p : point_order)
      if (!(domain & (U(1) << p)))
        forbidden[count++] = p;
    for (size_t word = lo / 64; word < (hi + 63) / 64; ++word) {
      uint64_t bits = ~uint64_t(0);
      if (word == lo / 64)
        bits &= ~uint64_t(0) << (lo % 64);
      if (word == hi / 64)
        bits &= (uint64_t(1) << (hi % 64)) - 1;
      for (size_t i = 0; i < count && bits; ++i)
        bits &= ~incidence[size_t(forbidden[i])][word];
      while (bits) {
        int bit = __builtin_ctzll(bits);
        bits &= bits - 1;
        answer.push_back(masks[order[word * 64 + size_t(bit)]]);
      }
    }
    std::sort(answer.begin(), answer.end());
    return answer;
  }
};
struct Bits {
  U lo = 0, hi = 0;
  void add(int x) {
    if (x < 128)
      lo |= U(1) << x;
    else
      hi |= U(1) << (x - 128);
  }
  bool hit(Bits b) const { return (lo & b.lo) || (hi & b.hi); }
  Bits join(Bits b) const { return {lo | b.lo, hi | b.hi}; }
};
Bits sums_with(U marks, int x) {
  Bits b{marks << x, x ? marks >> (128 - x) : 0};
  b.add(2 * x);
  return b;
}

struct Enum {
  std::vector<int> a;
  std::vector<U> answers;
  int hi;
  void visit(int start, int remain, U selected, Bits sums) {
    if (remain == 0) {
      answers.push_back(selected);
      return;
    }
    int upper = a[size_t(hi)] - remain * (remain + 1) / 2;
    for (int i = start; i + remain <= hi; ++i) {
      int x = a[size_t(i)];
      if (x > upper)
        break;
      auto fresh = sums_with(selected, x);
      if (!fresh.hit(sums))
        visit(i + 1, remain - 1, selected | (U(1) << x), sums.join(fresh));
    }
  }
  std::vector<U> run(U domain, int k) {
    a.clear();
    answers.clear();
    for (int x = 0; x < 82; ++x)
      if (domain & (U(1) << x))
        a.push_back(x);
    for (int lo = 0; lo + k <= int(a.size()); ++lo)
      for (hi = lo + k - 1; hi < int(a.size()); ++hi) {
        int x = a[size_t(lo)], y = a[size_t(hi)];
        if (y - x < k * (k - 1) / 2)
          continue;
        Bits sums;
        sums.add(2 * x);
        sums.add(x + y);
        sums.add(2 * y);
        visit(lo + 1, k - 2, (U(1) << x) | (U(1) << y), sums);
      }
    return answers;
  }
};

struct Enumerate {
  int n, k;
  std::array<int, 16> a{};
  std::vector<U> answer;
  U universe;
  void dfs(int m, U rev, U diff, U available, U selected) {
    int remain = k - m;
    if (pop(available) < remain)
      return;
    int maxnext = n - 1 - remain * (remain - 1) / 2;
    if (maxnext < 0)
      return;
    U candidates = available & ((U(1) << (maxnext + 1)) - 1);
    while (candidates) {
      int x = first(candidates);
      candidates &= candidates - 1;
      a[size_t(m)] = x;
      U fresh = rev >> (n - 1 - x);
      if (fresh & diff)
        throw std::runtime_error("invalid candidate");
      U mask = selected | (U(1) << x);
      if (remain == 1) {
        answer.push_back(mask);
        continue;
      }
      U next = available & ~((U(1) << (x + 1)) - 1);
      next &= ~(diff << x);
      for (int i = 0; i <= m; ++i)
        next &= ~(fresh << a[size_t(i)]);
      dfs(m + 1, rev | (U(1) << (n - 1 - x)), diff | fresh, next, mask);
    }
  }
  std::vector<U> run(U domain, int target) {
    k = target;
    answer.clear();
    dfs(0, 0, 0, domain, 0);
    return answer;
  }
};
