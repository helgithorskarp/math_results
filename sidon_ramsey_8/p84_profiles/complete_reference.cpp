#include <algorithm>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <unordered_set>
#include <vector>
using U = __uint128_t;
struct H {
  size_t operator()(U x) const {
    return size_t(uint64_t(x) ^
                  (uint64_t(x >> 64) * UINT64_C(0x9e3779b97f4a7c15)));
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
bool sidon(U m) {
  Bits sums;
  U selected = 0;
  for (int x = 0; x < 84; ++x)
    if (m & (U(1) << x)) {
      auto fresh = sums_with(selected, x);
      if (fresh.hit(sums))
        return false;
      sums = sums.join(fresh);
      selected |= U(1) << x;
    }
  return true;
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
bool possible(U r, uint64_t &tens, uint64_t &elevens) {
  Enum gen;
  auto ten = gen.run(r, 10), eleven = gen.run(r, 11);
  tens += ten.size();
  elevens += eleven.size();
  for (size_t i = 0; i < ten.size(); ++i)
    for (size_t j = i + 1; j < ten.size(); ++j)
      if (!(ten[i] & ten[j]) && sidon(r ^ ten[i] ^ ten[j]))
        return true;
  for (auto a : eleven) {
    for (auto b : ten)
      if (!(a & b) && sidon(r ^ a ^ b))
        return true;
    for (auto b : eleven)
      if (!(a & b) && sidon(r ^ a ^ b))
        return true;
    auto nine = gen.run(r ^ a, 9);
    for (auto b : nine)
      if (sidon(r ^ a ^ b))
        return true;
  }
  return false;
}
int main(int argc, char **argv) {
  try {
    if (argc == 3 && std::string(argv[1]) == "--residual") {
      std::ifstream input(argv[2]);
      if (!input)
        throw std::runtime_error("cannot open residual");
      int x;
      U r = 0;
      while (input >> x) {
        if (x < 0 || x >= 84 || (r & (U(1) << x)))
          throw std::runtime_error("bad residual");
        r |= U(1) << x;
      }
      if (__builtin_popcountll(uint64_t(r)) +
              __builtin_popcountll(uint64_t(r >> 64)) !=
          29)
        throw std::runtime_error("need 29 points");
      uint64_t tens = 0, elevens = 0;
      bool yes = possible(r, tens, elevens);
      std::cout << "{\"found\":" << (yes ? "true" : "false")
                << ",\"ten_sets\":" << tens << ",\"eleven_sets\":" << elevens
                << "}\n";
      return 0;
    }
    if (argc != 3)
      throw std::runtime_error("usage: residual_reference sets tuples");
    std::ifstream sf(argv[1]), tf(argv[2]);
    if (!sf || !tf)
      throw std::runtime_error("input open failed");
    std::vector<U> sets;
    std::string line;
    while (std::getline(sf, line)) {
      std::istringstream in(line);
      int x;
      U mask = 0;
      while (in >> x) {
        if (x < 0 || x >= 84)
          throw std::runtime_error("bad point");
        mask |= U(1) << x;
      }
      sets.push_back(mask);
    }
    uint64_t count = 0, tens = 0, elevens = 0;
    auto t = std::chrono::steady_clock::now();
    while (std::getline(tf, line)) {
      std::istringstream in(line);
      U used = 0;
      int i, n = 0;
      while (in >> i) {
        if (i < 0 || size_t(i) >= sets.size() || (used & sets[size_t(i)]))
          throw std::runtime_error("bad tuple");
        used |= sets[size_t(i)];
        ++n;
      }
      if (n != 5)
        throw std::runtime_error("not five");
      ++count;
      U r = ((U(1) << 84) - 1) ^ used;
      if (possible(r, tens, elevens)) {
        std::cout << "FOUND " << count << '\n';
        return 2;
      }
      if (count % 10000 == 0)
        std::cerr << "tested=" << count << '\n';
    }
    std::cout << "{\"tested\":" << count << ",\"ten_sets\":" << tens
              << ",\"eleven_sets\":" << elevens << ",\"seconds\":"
              << std::chrono::duration<double>(
                     std::chrono::steady_clock::now() - t)
                     .count()
              << ",\"all_unsatisfiable\":true}\n";
  } catch (const std::exception &e) {
    std::cerr << e.what() << '\n';
    return 1;
  }
}
