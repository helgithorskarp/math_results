// Complete four-ten cover decisions on 40-point subsets of [84].
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
std::vector<U> cover(U r, int need, const std::vector<U> &ten) {
  if (need == 1)
    return sidon(r) ? std::vector<U>{r} : std::vector<U>{};
  std::array<int, 84> counts{};
  std::vector<U> candidates;
  for (U a : ten)
    if ((a & r) == a) {
      candidates.push_back(a);
      U t = a;
      while (t) {
        int p = first(t);
        t &= t - 1;
        ++counts[size_t(p)];
      }
    }
  U t = r;
  int chosen = -1, mincount = 1000000000;
  while (t) {
    int p = first(t);
    t &= t - 1;
    if (counts[size_t(p)] < mincount) {
      chosen = p;
      mincount = counts[size_t(p)];
    }
  }
  if (mincount == 0)
    return {};
  for (U a : candidates)
    if (a & (U(1) << chosen)) {
      auto answer = cover(r ^ a, need - 1, candidates);
      if (!answer.empty()) {
        answer.push_back(a);
        return answer;
      }
    }
  return {};
}
std::vector<U> fixed_cover(U r, int need, const std::vector<U> &ten) {
  if (need == 1)
    return sidon(r) ? std::vector<U>{r} : std::vector<U>{};
  int point = first(r);
  std::vector<U> cand;
  for (U a : ten)
    if ((a & r) == a)
      cand.push_back(a);
  for (U a : cand)
    if ((a >> point) & 1) {
      auto result = fixed_cover(r ^ a, need - 1, cand);
      if (!result.empty()) {
        result.push_back(a);
        return result;
      }
    }
  return {};
}
void printset(U m, std::ostream &o) {
  o << '[';
  bool c = false;
  while (m) {
    int x = first(m);
    m &= m - 1;
    if (c)
      o << ',';
    c = true;
    o << x + 1;
  }
  o << ']';
}

int main(int argc, char **argv) {
  try {
    if (argc != 5)
      throw std::runtime_error(
          "usage: complete40 method domains.txt trace.bin decisions.txt");
    int method = integer(argv[1]);
    if (method != 0 && method != 1)
      throw std::runtime_error("method");
    std::ifstream in(argv[2]);
    std::ofstream trace(argv[3], std::ios::binary), decisions(argv[4]);
    if (!in || !trace || !decisions)
      throw std::runtime_error("input/output");
    auto word = [&](uint64_t x) {
      for (int i = 0; i < 8; ++i)
        trace.put(char((x >> (8 * i)) & 255));
    };
    auto mask = [&](U x) {
      word(uint64_t(x));
      word(uint64_t(x >> 64));
    };
    uint64_t domains = 0, tens = 0, found = 0;
    std::string line;
    auto start = std::chrono::steady_clock::now();
    while (std::getline(in, line)) {
      std::istringstream input(line);
      int x;
      U r = 0;
      while (input >> x) {
        if (x < 0 || x >= 84 || (r & (U(1) << x)))
          throw std::runtime_error("point");
        r |= U(1) << x;
      }
      if (!input.eof() || pop(r) != 40)
        throw std::runtime_error("domain");
      std::vector<U> catalog;
      if (method == 0) {
        Enumerate e;
        e.n = 84;
        catalog = e.run(r, 10);
      } else {
        Enum e;
        catalog = e.run(r, 10);
      }
      std::sort(catalog.begin(), catalog.end());
      if (std::adjacent_find(catalog.begin(), catalog.end()) != catalog.end())
        throw std::runtime_error("duplicate ten");
      mask(r);
      word(catalog.size());
      for (U a : catalog)
        mask(a);
      if (!trace)
        throw std::runtime_error("trace write");
      auto answer =
          method == 0 ? cover(r, 4, catalog) : fixed_cover(r, 4, catalog);
      ++domains;
      tens += catalog.size();
      if (!answer.empty())
        ++found;
      decisions << "{\"domain_index\":" << (domains - 1)
                << ",\"ten_sets\":" << catalog.size()
                << ",\"found\":" << (!answer.empty() ? "true" : "false")
                << ",\"partition\":[";
      for (size_t i = 0; i < answer.size(); ++i) {
        if (i)
          decisions << ',';
        printset(answer[i], decisions);
      }
      decisions << "]}\n";
    }
    if (!in.eof())
      throw std::runtime_error("input read");
    trace.flush();
    decisions.flush();
    if (!trace || !decisions)
      throw std::runtime_error("output write");
    std::cout << "{\"method\":" << method << ",\"domains\":" << domains
              << ",\"ten_sets\":" << tens << ",\"found\":" << found
              << ",\"complete\":true,\"seconds\":"
              << std::chrono::duration<double>(
                     std::chrono::steady_clock::now() - start)
                     .count()
              << "}\n";
  } catch (const std::exception &e) {
    std::cerr << e.what() << '\n';
    return 1;
  }
}
