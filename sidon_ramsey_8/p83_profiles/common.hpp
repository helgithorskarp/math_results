#pragma once
// Exact heaviest-class recursion and two complete P83 packing traversals.
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
constexpr U universe = (U(1) << 83) - 1;
constexpr int cap = 4000000, total_weight = 31134774;
constexpr int threshold = total_weight - 4 * cap;
constexpr int cutoff = (threshold - 2 * cap + 1) / 2;
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
    if (x < 0 || x >= 83 || (mask & (U(1) << x)))
      throw std::runtime_error("point");
    mask |= U(1) << x;
  }
  if (!in.eof())
    throw std::runtime_error("set token");
  return mask;
}
struct Weights {
  std::array<int, 83> w{};
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
