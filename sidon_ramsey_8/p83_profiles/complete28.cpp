// Complete three-class profile decisions on 28-point subsets of [83].
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
    for (int x = 0; x < 83; ++x)
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

struct Solve {
  int method;
  uint64_t counts9 = 0, counts10 = 0, counts11 = 0;
  std::ostream &trace;
  int profile = -1;
  bool allows(int p) const { return profile < 0 || profile == p; }
  void word(uint64_t v) {
    for (int i = 0; i < 8; ++i)
      trace.put(char((v >> (8 * i)) & 255));
  }
  void mask(U m) {
    word(uint64_t(m));
    word(uint64_t(m >> 64));
  }
  std::vector<U> generate(U r, int k) {
    std::vector<U> a;
    if (method) {
      Enum e;
      a = e.run(r, k);
    } else {
      Enumerate e;
      e.n = 83;
      a = e.run(r, k);
    }
    std::sort(a.begin(), a.end());
    mask(r);
    word(uint64_t(k));
    word(a.size());
    for (U m : a)
      mask(m);
    if (k == 9)
      counts9 += a.size();
    if (k == 10)
      counts10 += a.size();
    if (k == 11)
      counts11 += a.size();
    return a;
  }
  std::vector<U> run(U r) {
    auto ten = generate(r, 10);
    if (ten.empty())
      return {};
    std::vector<U> eleven;
    if (ten.size() >= 11)
      eleven = generate(r, 11);
    for (size_t i = 0; i < ten.size(); ++i) {
      U a = ten[i];
      for (size_t j = i + 1; j < ten.size(); ++j)
        if (allows(0) && !(a & ten[j]) && sidon(r ^ a ^ ten[j]))
          return {a, ten[j], r ^ a ^ ten[j]};
      auto nine = generate(r ^ a, 9);
      for (U b : nine)
        if (allows(1) && sidon(r ^ a ^ b))
          return {a, b, r ^ a ^ b};
    }
    for (size_t i = 0; i < eleven.size(); ++i) {
      U a = eleven[i];
      for (U b : ten)
        if (allows(2) && !(a & b) && sidon(r ^ a ^ b))
          return {a, b, r ^ a ^ b};
      for (size_t j = i + 1; j < eleven.size(); ++j)
        if (allows(3) && !(a & eleven[j]) && sidon(r ^ a ^ eleven[j]))
          return {a, eleven[j], r ^ a ^ eleven[j]};
      auto nine = generate(r ^ a, 9);
      for (U b : nine)
        if (allows(4) && sidon(r ^ a ^ b))
          return {a, b, r ^ a ^ b};
    }
    return {};
  }
};
int main(int argc, char **argv) {
  try {
    if (argc != 5 && argc != 6)
      throw std::runtime_error(
          "method domains trace decisions [profile: 0=10,10,8; 1=10,9,9; "
          "2=11,10,7; 3=11,11,6; 4=11,9,8]");
    int method = integer(argv[1]);
    if (method != 0 && method != 1)
      throw std::runtime_error("method");
    std::ifstream in(argv[2]);
    std::ofstream trace(argv[3], std::ios::binary), dec(argv[4]);
    if (!in || !trace || !dec)
      throw std::runtime_error("IO");
    Solve solve{method, 0, 0, 0, trace};
    if (argc == 6) {
      solve.profile = integer(argv[5]);
      if (solve.profile < 0 || solve.profile > 4)
        throw std::runtime_error("profile");
    }
    std::string line;
    uint64_t n = 0, found = 0;
    auto start = std::chrono::steady_clock::now();
    while (std::getline(in, line)) {
      std::istringstream s(line);
      int x;
      U r = 0;
      while (s >> x) {
        if (x < 0 || x >= 83 || (r & (U(1) << x)))
          throw std::runtime_error("point");
        r |= U(1) << x;
      }
      if (!s.eof() || pop(r) != 28)
        throw std::runtime_error("domain");
      auto a = solve.run(r);
      if (!a.empty())
        ++found;
      dec << "{\"found\":" << (!a.empty() ? "true" : "false")
          << ",\"partition\":[";
      for (size_t i = 0; i < a.size(); ++i) {
        if (i)
          dec << ',';
        dec << '[';
        bool comma = false;
        for (int j = 0; j < 83; ++j)
          if (a[i] & (U(1) << j)) {
            if (comma)
              dec << ',';
            dec << j;
            comma = true;
          }
        dec << ']';
      }
      dec << "]}\n";
      ++n;
    }
    trace.flush();
    dec.flush();
    if (!in.eof() || !trace || !dec)
      throw std::runtime_error("completion");
    std::cout << "{\"method\":" << method << ",\"domains\":" << n
              << ",\"found\":" << found
              << ",\"nine_occurrences\":" << solve.counts9
              << ",\"ten_occurrences\":" << solve.counts10
              << ",\"eleven_occurrences\":" << solve.counts11
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
