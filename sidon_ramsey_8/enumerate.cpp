#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>
using U = __uint128_t;
struct Search {
  int n, k;
  bool endpoints;
  std::array<int, 16> a{};
  uint64_t nodes = 0, normalized = 0, translated = 0;
  std::ofstream out;
  U universe;
  std::vector<int64_t> weights;
  int64_t max_weight = 0;
  static int pop(U x) {
    return __builtin_popcountll(uint64_t(x)) + __builtin_popcountll(uint64_t(x >> 64));
  }
  static int first(U x) {
    auto lo = uint64_t(x);
    return lo ? __builtin_ctzll(lo) : 64 + __builtin_ctzll(uint64_t(x >> 64));
  }
  U above(int x) const { return universe & ~((U(1) << (x + 1)) - 1); }
  void emit() {
    ++normalized;
    int shiftmax = endpoints ? 0 : n - 1 - a[k - 1];
    for (int shift = 0; shift <= shiftmax; ++shift) {
      ++translated;
      if (!weights.empty()) {
        int64_t total = 0;
        for (int i = 0; i < k; ++i)
          total += weights[size_t(a[i] + shift)];
        max_weight = std::max(max_weight, total);
      }
      if (out.is_open()) {
        for (int i = 0; i < k; ++i)
          out << (i ? " " : "") << a[i] + shift;
        out << '\n';
      }
    }
  }
  // available contains exactly the later points compatible with the selected prefix.
  void dfs(int m, U reverse, U differences, U available) {
    ++nodes;
    int remain = k - m;
    if (remain == 0) {
      if (!endpoints || a[m - 1] == n - 1)
        emit();
      return;
    }
    if (pop(available) < remain)
      return;
    // Future consecutive gaps are distinct and cannot reuse an old difference.
    int sum = 0, found = 0;
    U unused = universe & ~differences & ~U(1);
    while (found < remain && unused) {
      int d = first(unused);
      unused &= unused - 1;
      sum += d;
      ++found;
    }
    if (found < remain || a[m - 1] + sum > n - 1)
      return;
    int maxnext = n - 1 - remain * (remain - 1) / 2;
    if (maxnext < 0)
      return;
    U candidates = available & ((U(1) << (maxnext + 1)) - 1);
    if (endpoints && remain == 1)
      candidates &= U(1) << (n - 1);
    while (candidates) {
      int x = first(candidates);
      candidates &= candidates - 1;
      U fresh = reverse >> (n - 1 - x);
      if (fresh & differences)
        throw std::runtime_error("candidate invariant violated");
      a[m] = x;
      if (remain == 1) {
        emit();
        continue;
      }
      U next = available & above(x);
      next &= ~(differences << x);
      for (int i = 0; i <= m; ++i)
        next &= ~(fresh << a[i]);
      dfs(m + 1, reverse | (U(1) << (n - 1 - x)), differences | fresh, next);
    }
  }
  void run() {
    a[0] = 0;
    dfs(1, U(1) << (n - 1), 0, universe & ~U(1));
  }
};
int main(int argc, char **argv) {
  try {
    if (argc < 3 || argc > 6)
      throw std::runtime_error("usage: enumerate N K [all|endpoints] [output.txt|-] [weights.txt]");
    Search s;
    s.n = std::stoi(argv[1]);
    s.k = std::stoi(argv[2]);
    s.endpoints = argc > 3 && std::string(argv[3]) == "endpoints";
    if (s.n < 2 || s.n > 100 || s.k < 2 || s.k > 12 || s.k > s.n)
      throw std::runtime_error("require 2<=K<=12, K<=N<=100");
    if (argc > 3 && std::string(argv[3]) != "all" && std::string(argv[3]) != "endpoints")
      throw std::runtime_error("bad mode");
    if (argc >= 5 && std::string(argv[4]) != "-") {
      s.out.open(argv[4]);
      if (!s.out)
        throw std::runtime_error("cannot open output");
    }
    if (argc == 6) {
      std::ifstream in(argv[5]);
      int64_t value;
      while (in >> value) {
        if (value < 0 || value > 1000000)
          throw std::runtime_error("invalid weight");
        s.weights.push_back(value);
      }
      if (s.weights.size() != size_t(s.n))
        throw std::runtime_error("wrong weight count");
    }
    s.universe = (U(1) << s.n) - 1;
    auto start = std::chrono::steady_clock::now();
    s.run();
    if (s.out.is_open()) {
      s.out.flush();
      if (!s.out)
        throw std::runtime_error("write failure");
    }
    double sec = std::chrono::duration<double>(std::chrono::steady_clock::now() - start).count();
    std::cout << "{\"n\":" << s.n << ",\"k\":" << s.k
              << ",\"endpoints\":" << (s.endpoints ? "true" : "false")
              << ",\"normalized\":" << s.normalized << ",\"sets\":" << s.translated
              << ",\"max_weight\":" << s.max_weight << ",\"nodes\":" << s.nodes
              << ",\"seconds\":" << sec << ",\"complete\":true}\n";
  } catch (const std::exception &e) {
    std::cerr << e.what() << '\n';
    return 1;
  }
}
