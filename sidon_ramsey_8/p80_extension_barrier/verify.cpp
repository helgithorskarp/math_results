// Exact exclusion of extensions of the specified P80 seed retaining three
// classes. Method 0 uses positive differences; method 1 fixes endpoints and
// uses pair sums.
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
struct Audit {
  int method;
  std::ofstream trace;
  uint64_t domains = 0, eleven_occ = 0, pairs = 0, balanced_tens = 0,
           other_tens = 0, other_elevens = 0, twelves = 0, calls = 0;
  std::vector<U> answer;
  void word(uint64_t x) {
    for (int i = 0; i < 8; ++i)
      trace.put(char((x >> (8 * i)) & 255));
  }
  void mask(U x) {
    word(uint64_t(x));
    word(uint64_t(x >> 64));
  }
  std::vector<U> gen(U r, int k) {
    std::vector<U> ans;
    if (method == 0) {
      Enumerate e;
      e.n = 81;
      ans = e.run(r, k);
    } else {
      Enum e;
      ans = e.run(r, k);
    }
    std::sort(ans.begin(), ans.end());
    if (std::adjacent_find(ans.begin(), ans.end()) != ans.end())
      throw std::runtime_error("duplicate set");
    ++calls;
    mask(r);
    word(uint64_t(k));
    word(ans.size());
    for (U x : ans)
      mask(x);
    if (!trace)
      throw std::runtime_error("trace write");
    return ans;
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
  bool small29(U r) {
    auto ten = gen(r, 10), eleven = gen(r, 11);
    other_tens += ten.size();
    other_elevens += eleven.size();
    for (size_t i = 0; i < ten.size(); ++i)
      for (size_t j = i + 1; j < ten.size(); ++j)
        if (!(ten[i] & ten[j]) && sidon(r ^ ten[i] ^ ten[j])) {
          answer = {ten[i], ten[j], r ^ ten[i] ^ ten[j]};
          return true;
        }
    for (U a : eleven) {
      for (U b : ten)
        if (!(a & b) && sidon(r ^ a ^ b)) {
          answer = {a, b, r ^ a ^ b};
          return true;
        }
      for (U b : eleven)
        if (!(a & b) && sidon(r ^ a ^ b)) {
          answer = {a, b, r ^ a ^ b};
          return true;
        }
      auto nine = gen(r ^ a, 9);
      for (U b : nine)
        if (sidon(r ^ a ^ b)) {
          answer = {a, b, r ^ a ^ b};
          return true;
        }
    }
    return false;
  }
  bool solve(U r) {
    ++domains;
    auto too_large = gen(r, 12);
    twelves += too_large.size();
    if (!too_large.empty())
      throw std::runtime_error("twelve-set invalidates reduction");
    auto eleven = gen(r, 11);
    eleven_occ += eleven.size();
    for (U a : eleven) {
      auto ten = gen(r ^ a, 10);
      balanced_tens += ten.size();
      auto result =
          method == 0 ? cover(r ^ a, 4, ten) : fixed_cover(r ^ a, 4, ten);
      if (!result.empty()) {
        answer = result;
        answer.push_back(a);
        return true;
      }
    }
    for (size_t i = 0; i < eleven.size(); ++i)
      for (size_t j = i + 1; j < eleven.size(); ++j)
        if (!(eleven[i] & eleven[j])) {
          ++pairs;
          if (small29(r ^ eleven[i] ^ eleven[j])) {
            answer.push_back(eleven[i]);
            answer.push_back(eleven[j]);
            return true;
          }
        }
    return false;
  }
};
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
    if (argc == 5 && std::string(argv[1]) == "--residual") {
      Audit a;
      a.method = integer(argv[2]);
      if (a.method != 0 && a.method != 1)
        throw std::runtime_error("method");
      a.trace.open(argv[4], std::ios::binary);
      std::ifstream in(argv[3]);
      if (!in || !a.trace)
        throw std::runtime_error("input");
      U r = 0;
      int x;
      while (in >> x) {
        if (x < 1 || x > 81 || ((r >> (x - 1)) & 1))
          throw std::runtime_error("residual point");
        r |= U(1) << (x - 1);
      }
      if (!in.eof())
        throw std::runtime_error("invalid residual token");
      bool yes;
      if (pop(r) == 51)
        yes = a.solve(r);
      else if (pop(r) == 29)
        yes = a.small29(r);
      else if (pop(r) == 40) {
        auto ten = a.gen(r, 10);
        a.answer = a.method == 0 ? cover(r, 4, ten) : a.fixed_cover(r, 4, ten);
        yes = !a.answer.empty();
      } else
        throw std::runtime_error("residual size");
      std::cout << "{\"found\":" << (yes ? "true" : "false")
                << ",\"partition\":[";
      for (size_t i = 0; i < a.answer.size(); ++i) {
        if (i)
          std::cout << ',';
        printset(a.answer[i], std::cout);
      }
      std::cout << "]}\n";
      return 0;
    }
    if (argc != 5)
      throw std::runtime_error(
          "usage: extension_audit seed shift method trace");
    int shift = integer(argv[2]);
    Audit a;
    a.method = integer(argv[3]);
    if ((shift != 0 && shift != 1) || (a.method != 0 && a.method != 1))
      throw std::runtime_error("mode");
    a.trace.open(argv[4], std::ios::binary);
    if (!a.trace)
      throw std::runtime_error("trace");
    std::ifstream file(argv[1]);
    if (!file)
      throw std::runtime_error("seed");
    std::vector<U> base;
    U used = 0;
    std::string line;
    while (std::getline(file, line)) {
      std::istringstream in(line);
      int x;
      U m = 0;
      while (in >> x) {
        if (x < 1 || x > 80 || ((m >> (x - 1 + shift)) & 1))
          throw std::runtime_error("bad seed point");
        m |= U(1) << (x - 1 + shift);
      }
      if (!in.eof())
        throw std::runtime_error("invalid seed token");
      if (pop(m) != 10 || !sidon(m) || (used & m))
        throw std::runtime_error("seed not a Sidon partition");
      used |= m;
      base.push_back(m);
    }
    if (base.size() != 8 || used != (((U(1) << 80) - 1) << shift))
      throw std::runtime_error("seed coverage");
    auto start = std::chrono::steady_clock::now();
    bool found = false;
    for (int i = 0; i < 8 && !found; ++i)
      for (int j = i + 1; j < 8 && !found; ++j)
        for (int k = j + 1; k < 8 && !found; ++k) {
          U r = ((U(1) << 81) - 1) ^ base[size_t(i)] ^ base[size_t(j)] ^
                base[size_t(k)];
          if (a.solve(r)) {
            found = true;
            a.answer.push_back(base[size_t(i)]);
            a.answer.push_back(base[size_t(j)]);
            a.answer.push_back(base[size_t(k)]);
          }
          std::cerr << "domain=" << a.domains << " elevens=" << a.eleven_occ
                    << " pairs=" << a.pairs << " seconds="
                    << std::chrono::duration<double>(
                           std::chrono::steady_clock::now() - start)
                           .count()
                    << '\n';
        }
    a.trace.flush();
    if (!a.trace)
      throw std::runtime_error("trace flush");
    std::cout << "{\"shift\":" << shift << ",\"method\":" << a.method
              << ",\"found\":" << (found ? "true" : "false")
              << ",\"domains\":" << a.domains
              << ",\"eleven_occurrences\":" << a.eleven_occ
              << ",\"large_pairs\":" << a.pairs
              << ",\"balanced_ten_occurrences\":" << a.balanced_tens
              << ",\"other_ten_occurrences\":" << a.other_tens
              << ",\"other_eleven_occurrences\":" << a.other_elevens
              << ",\"twelve_occurrences\":" << a.twelves
              << ",\"catalog_calls\":" << a.calls << ",\"complete\":"
              << (!found && a.domains == 56 ? "true" : "false")
              << ",\"seconds\":"
              << std::chrono::duration<double>(
                     std::chrono::steady_clock::now() - start)
                     .count()
              << ",\"partition\":[";
    for (size_t i = 0; i < a.answer.size(); ++i) {
      if (i)
        std::cout << ',';
      printset(a.answer[i], std::cout);
    }
    std::cout << "]}\n";
  } catch (const std::exception &e) {
    std::cerr << e.what() << '\n';
    return 1;
  }
}
