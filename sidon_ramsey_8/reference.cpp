#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>
using U = __uint128_t;
struct Bits {
  U low = 0, high = 0;
  void add(int x) {
    if (x < 128)
      low |= U(1) << x;
    else
      high |= U(1) << (x - 128);
  }
  bool intersects(Bits b) const { return (low & b.low) || (high & b.high); }
  Bits plus(Bits b) const { return {low | b.low, high | b.high}; }
};
struct Reference {
  int n, k, diameter;
  uint64_t nodes = 0, count = 0;
  std::vector<int> a;
  std::ofstream out;
  void visit(int start, int remain, U marks, Bits sums) {
    ++nodes;
    if (remain == 0) {
      for (int shift = 0; shift < n - diameter; ++shift) {
        ++count;
        if (out.is_open()) {
          out << shift;
          for (auto x : a)
            out << ' ' << x + shift;
          out << ' ' << diameter + shift << '\n';
        }
      }
      return;
    }
    int upper = diameter - remain * (remain + 1) / 2;
    for (int x = start; x <= upper; ++x) {
      Bits fresh{marks << x, marks >> (128 - x)};
      fresh.add(2 * x);
      if (fresh.intersects(sums))
        continue;
      a.push_back(x);
      visit(x + 1, remain - 1, marks | (U(1) << x), sums.plus(fresh));
      a.pop_back();
    }
  }
  void run() {
    for (diameter = k * (k - 1) / 2; diameter < n; ++diameter) {
      Bits sums;
      sums.add(0);
      sums.add(diameter);
      sums.add(2 * diameter);
      visit(1, k - 2, U(1) | (U(1) << diameter), sums);
    }
  }
};
int main(int argc, char **argv) {
  try {
    if (argc < 3 || argc > 4)
      throw std::runtime_error("usage: reference N K [sets.txt]");
    Reference r;
    r.n = std::stoi(argv[1]);
    r.k = std::stoi(argv[2]);
    if (r.n < 2 || r.n > 100 || r.k < 2 || r.k > 12)
      throw std::runtime_error("invalid parameters");
    if (argc == 4) {
      r.out.open(argv[3]);
      if (!r.out)
        throw std::runtime_error("open failed");
    }
    auto t = std::chrono::steady_clock::now();
    r.run();
    if (r.out.is_open()) {
      r.out.flush();
      if (!r.out)
        throw std::runtime_error("write failed");
    }
    std::cout << "{\"n\":" << r.n << ",\"k\":" << r.k << ",\"sets\":" << r.count
              << ",\"nodes\":" << r.nodes << ",\"seconds\":"
              << std::chrono::duration<double>(std::chrono::steady_clock::now() - t).count()
              << ",\"complete\":true}\n";
  } catch (const std::exception &e) {
    std::cerr << e.what() << '\n';
    return 1;
  }
}
