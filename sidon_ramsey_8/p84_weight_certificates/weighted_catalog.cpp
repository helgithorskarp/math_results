#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <numeric>
#include <random>
#include <set>
#include <sstream>
#include <stdexcept>
#include <vector>
using U = __uint128_t;
int integer(const char *text) {
  size_t used = 0;
  int x = std::stoi(text, &used);
  if (text[used])
    throw std::runtime_error("invalid integer argument");
  return x;
}
int first(U x) {
  auto lo = uint64_t(x);
  return lo ? __builtin_ctzll(lo) : 64 + __builtin_ctzll(uint64_t(x >> 64));
}
int pop(U x) {
  return __builtin_popcountll(uint64_t(x)) +
         __builtin_popcountll(uint64_t(x >> 64));
}
bool sidon(U s) {
  std::set<int> sums;
  std::vector<int> a;
  while (s) {
    int x = first(s);
    s &= s - 1;
    a.push_back(x);
  }
  for (size_t i = 0; i < a.size(); ++i)
    for (size_t j = i; j < a.size(); ++j)
      if (!sums.insert(a[i] + a[j]).second)
        return false;
  return true;
}
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
    for (int x = 0; x < 84; ++x)
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

int main(int argc, char **argv) {
  try {
    if (argc != 6)
      throw std::runtime_error(
          "usage: catalog method domain.txt output.bin size weights.txt");
    int method = integer(argv[1]), k = integer(argv[4]);
    if ((method != 0 && method != 1) || k < 2 || k > 12)
      throw std::runtime_error("parameters");
    std::ifstream in(argv[2]);
    std::ofstream out(argv[3], std::ios::binary);
    if (!in || !out)
      throw std::runtime_error("input/output");
    U domain = 0;
    int x;
    while (in >> x) {
      if (x < 0 || x >= 84 || (domain & (U(1) << x)))
        throw std::runtime_error("point");
      domain |= U(1) << x;
    }
    if (!in.eof())
      throw std::runtime_error("invalid domain");
    std::array<int64_t, 84> weights{};
    std::ifstream wi(argv[5]);
    for (auto &w : weights)
      if (!(wi >> w) || w < 0 || w > 1000000)
        throw std::runtime_error("weight");
    std::string extra;
    if (wi >> extra)
      throw std::runtime_error("extra weight");
    auto start = std::chrono::steady_clock::now();
    std::vector<U> sets;
    if (method == 0) {
      Enumerate e;
      e.n = 84;
      sets = e.run(domain, k);
    } else {
      Enum e;
      sets = e.run(domain, k);
    }
    std::sort(sets.begin(), sets.end());
    if (std::adjacent_find(sets.begin(), sets.end()) != sets.end())
      throw std::runtime_error("duplicate");
    int64_t maximum = -1;
    U maximizer = 0;
    for (U m : sets) {
      U t = m;
      int64_t weight = 0;
      while (t) {
        int point = first(t);
        t &= t - 1;
        out.put(char(point));
        weight += weights[size_t(point)];
      }
      if (weight > maximum) {
        maximum = weight;
        maximizer = m;
      }
    }
    out.flush();
    if (!out)
      throw std::runtime_error("write");
    std::cout << "{\"method\":" << method << ",\"points\":" << pop(domain)
              << ",\"size\":" << k << ",\"sets\":" << sets.size()
              << ",\"max_weight\":" << maximum << ",\"maximizer\":[";
    bool comma = false;
    while (maximizer) {
      int point = first(maximizer);
      maximizer &= maximizer - 1;
      if (comma)
        std::cout << ',';
      comma = true;
      std::cout << point;
    }
    std::cout << "],\"complete\":true,\"seconds\":"
              << std::chrono::duration<double>(
                     std::chrono::steady_clock::now() - start)
                     .count()
              << "}\n";
  } catch (const std::exception &e) {
    std::cerr << e.what() << '\n';
    return 1;
  }
}
