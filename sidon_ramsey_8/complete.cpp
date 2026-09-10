#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>
#include <unordered_set>
#include <vector>
using U = __uint128_t;
struct Hash {
  size_t operator()(U x) const {
    return size_t(uint64_t(x) ^ (uint64_t(x >> 64) * UINT64_C(0x9e3779b97f4a7c15)));
  }
};
int first(U x) {
  auto lo = uint64_t(x);
  return lo ? __builtin_ctzll(lo) : 64 + __builtin_ctzll(uint64_t(x >> 64));
}
int pop(U x) { return __builtin_popcountll(uint64_t(x)) + __builtin_popcountll(uint64_t(x >> 64)); }
bool sidon(U s) {
  U d = 0;
  while (s) {
    int x = first(s);
    s &= s - 1;
    U t = s;
    while (t) {
      int y = first(t);
      t &= t - 1;
      U b = U(1) << (y - x);
      if (d & b)
        return false;
      d |= b;
    }
  }
  return true;
}
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
std::vector<U> solve(U r, int n, uint64_t &ten_total, uint64_t &eleven_total) {
  Enumerate gen;
  gen.n = n;
  gen.universe = (U(1) << n) - 1;
  auto ten = gen.run(r, 10);
  ten_total += ten.size();
  if (ten.size() < 3)
    return {};
  std::vector<U> eleven;
  if (ten.size() >= 11)
    eleven = gen.run(r, 11);
  eleven_total += eleven.size();
  std::unordered_set<U, Hash> h(ten.begin(), ten.end());
  int p = first(r);
  for (auto a : ten)
    if (a & (U(1) << p)) {
      U rest = r ^ a;
      int q = first(rest);
      for (auto b : ten)
        if ((b & (U(1) << q)) && !(a & b)) {
          U c = rest ^ b;
          if (h.contains(c))
            return {a, b, c};
        }
    }
  for (auto a : eleven)
    for (auto b : ten)
      if (!(a & b)) {
        U c = r ^ a ^ b;
        if (sidon(c))
          return {a, b, c};
      }
  for (size_t i = 0; i < eleven.size(); ++i)
    for (size_t j = i + 1; j < eleven.size(); ++j)
      if (!(eleven[i] & eleven[j])) {
        U c = r ^ eleven[i] ^ eleven[j];
        if (sidon(c))
          return {eleven[i], eleven[j], c};
      }
  return {};
}
void printset(U x) {
  std::cout << '[';
  bool comma = false;
  while (x) {
    int a = first(x);
    x &= x - 1;
    if (comma)
      std::cout << ',';
    comma = true;
    std::cout << a + 1;
  }
  std::cout << ']';
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
        if (x < 0 || x >= 85 || (r & (U(1) << x)))
          throw std::runtime_error("bad residual point");
        r |= U(1) << x;
      }
      if (pop(r) != 30)
        throw std::runtime_error("need 30 residual points");
      uint64_t tens = 0, elevens = 0;
      auto result = solve(r, 85, tens, elevens);
      std::cout << "{\"found\":" << (result.empty() ? "false" : "true") << ",\"ten_sets\":" << tens
                << ",\"eleven_sets\":" << elevens << ",\"partition\":[";
      for (size_t i = 0; i < result.size(); ++i) {
        if (i)
          std::cout << ',';
        printset(result[i]);
      }
      std::cout << "]}\n";
      return 0;
    }
    if (argc != 4)
      throw std::runtime_error(
          "usage: complete N sets.txt tuples.txt OR complete --residual points.txt");
    int n = std::stoi(argv[1]);
    if (n != 85)
      throw std::runtime_error("only P85 supported");
    std::ifstream in(argv[2]);
    if (!in)
      throw std::runtime_error("cannot open sets");
    std::vector<U> sets;
    std::string line;
    while (std::getline(in, line)) {
      std::istringstream s(line);
      int x;
      U mask = 0;
      while (s >> x) {
        if (x < 0 || x >= n || (mask & (U(1) << x)))
          throw std::runtime_error("bad set");
        mask |= U(1) << x;
      }
      if (pop(mask) != 11 || !sidon(mask))
        throw std::runtime_error("invalid Sidon set");
      sets.push_back(mask);
    }
    std::ifstream tuples(argv[3]);
    if (!tuples)
      throw std::runtime_error("cannot open tuples");
    uint64_t count = 0, unique = 0, tens = 0, elevens = 0;
    std::unordered_set<U, Hash> seen;
    auto start = std::chrono::steady_clock::now();
    while (std::getline(tuples, line)) {
      std::istringstream s(line);
      std::vector<int> ids;
      int x;
      U used = 0;
      while (s >> x) {
        if (x < 0 || size_t(x) >= sets.size() || (!ids.empty() && x <= ids.back()) ||
            (used & sets[size_t(x)]))
          throw std::runtime_error("bad tuple");
        ids.push_back(x);
        used |= sets[size_t(x)];
      }
      if (ids.size() != 5)
        throw std::runtime_error("tuple not of size 5");
      ++count;
      U residual = ((U(1) << n) - 1) ^ used;
      if (!seen.insert(residual).second)
        continue;
      ++unique;
      auto result = solve(residual, n, tens, elevens);
      if (!result.empty()) {
        std::cout << "{\"found\":true,\"tuple_index\":" << count << ",\"partition\":[";
        bool comma = false;
        for (auto id : ids) {
          if (comma)
            std::cout << ',';
          comma = true;
          printset(sets[size_t(id)]);
        }
        for (auto a : result) {
          std::cout << ',';
          printset(a);
        }
        std::cout << "]}\n";
        return 0;
      }
      if (count % 10000 == 0)
        std::cerr << "tuples=" << count << " unique=" << unique << " ten_sets=" << tens
                  << " eleven_sets=" << elevens << '\n';
    }
    std::cout << "{\"found\":false,\"tuples\":" << count << ",\"unique_residuals\":" << unique
              << ",\"ten_sets\":" << tens << ",\"eleven_sets\":" << elevens << ",\"seconds\":"
              << std::chrono::duration<double>(std::chrono::steady_clock::now() - start).count()
              << ",\"input_read_complete\":true}\n";
  } catch (const std::exception &e) {
    std::cerr << e.what() << '\n';
    return 1;
  }
}
