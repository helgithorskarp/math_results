// Independent pair-sum enumeration of all Sidon 10-sets in {0,...,83}.
#include <algorithm>
#include <array>
#include <bitset>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <string>
#include <vector>

class Search {
 public:
  static constexpr int n = 84;
  static constexpr int k = 10;
  std::array<int, k> chosen{};
  std::array<std::int64_t, n> weight{};
  std::uint64_t normalized = 0;
  std::uint64_t translated = 0;
  std::uint64_t nodes = 0;
  std::int64_t maximum = std::numeric_limits<std::int64_t>::min();
  std::array<int, k> maximizing{};

  void visit(int used, int start, int remaining, int high,
             const std::bitset<2 * n - 1>& sums) {
    ++nodes;
    if (remaining == 0) {
      ++normalized;
      for (int shift = 0; shift + high < n; ++shift) {
        std::int64_t total = 0;
        for (int i = 0; i < k; ++i) total += weight[chosen[i] + shift];
        ++translated;
        if (total > maximum) {
          maximum = total;
          for (int i = 0; i < k; ++i) maximizing[i] = chosen[i] + shift;
        }
      }
      return;
    }

    // After choosing x, the remaining interior points and the fixed high
    // endpoint create 'remaining' distinct positive consecutive gaps.
    // Their sum is at least 1+...+remaining.
    const int upper = high - remaining * (remaining + 1) / 2;
    for (int x = start; x <= upper; ++x) {
      std::array<int, k + 1> fresh{};
      int fresh_count = 0;
      bool valid = true;
      for (int i = 0; i < used; ++i) {
        const int s = chosen[i] + x;
        if (sums.test(s)) valid = false;
        fresh[fresh_count++] = s;
      }
      const int with_high = high + x;
      if (sums.test(with_high)) valid = false;
      fresh[fresh_count++] = with_high;
      const int diagonal = 2 * x;
      if (sums.test(diagonal)) valid = false;
      for (int i = 0; i < fresh_count; ++i)
        if (fresh[i] == diagonal) valid = false;
      if (!valid) continue;

      auto next = sums;
      for (int i = 0; i < fresh_count; ++i) next.set(fresh[i]);
      next.set(diagonal);
      chosen[used] = x;
      visit(used + 1, x + 1, remaining - 1, high, next);
    }
  }

  void run() {
    for (int high = k * (k - 1) / 2; high < n; ++high) {
      chosen[0] = 0;
      chosen[k - 1] = high;
      std::bitset<2 * n - 1> sums;
      sums.set(0);
      sums.set(high);
      sums.set(2 * high);
      visit(1, 1, k - 2, high, sums);
    }
  }
};

int main(int argc, char** argv) {
  try {
    if (argc != 2) throw std::runtime_error("usage: independent_ten_cap weights.txt");
    Search search;
    std::ifstream input(argv[1]);
    for (auto& value : search.weight)
      if (!(input >> value) || value < 0) throw std::runtime_error("invalid weight");
    std::string extra;
    if (input >> extra) throw std::runtime_error("extra weight");
    if (!std::equal(search.weight.begin(), search.weight.end(),
                    search.weight.rbegin()))
      throw std::runtime_error("weights are not reflection symmetric");
    const auto start = std::chrono::steady_clock::now();
    search.run();
    std::cout << "{\"normalized\":" << search.normalized
              << ",\"sets\":" << search.translated
              << ",\"max_weight\":" << search.maximum
              << ",\"maximizer\":[";
    for (int i = 0; i < Search::k; ++i) {
      if (i) std::cout << ',';
      std::cout << search.maximizing[i];
    }
    std::cout << "],\"nodes\":" << search.nodes
              << ",\"complete\":true}\n";
    std::cerr << "elapsed_seconds="
              << std::chrono::duration<double>(
                     std::chrono::steady_clock::now() - start).count()
              << '\n';
  } catch (const std::exception& error) {
    std::cerr << error.what() << '\n';
    return 1;
  }
}
