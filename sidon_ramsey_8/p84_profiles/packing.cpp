#include <algorithm>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <numeric>
#include <sstream>
#include <stdexcept>
#include <vector>
using U = __uint128_t;
struct Ref {
  std::vector<U> sets;
  std::vector<int64_t> w;
  std::vector<int> a;
  std::ofstream out;
  int64_t threshold = 4899969;
  uint64_t found = 0, nodes = 0;
  void dfs(const std::vector<int> &cand, int need, int64_t weight) {
    ++nodes;
    if (need == 0) {
      if (weight >= threshold) {
        ++found;
        for (size_t i = 0; i < a.size(); ++i)
          out << (i ? " " : "") << a[i];
        out << '\n';
      }
      return;
    }
    if (cand.size() < size_t(need))
      return;
    int64_t upper = weight;
    for (int i = 0; i < need; ++i)
      upper += w[size_t(cand[size_t(i)])];
    if (upper < threshold)
      return;
    for (size_t i = 0; i + size_t(need) <= cand.size(); ++i) {
      int v = cand[i];
      if (weight + need * w[size_t(v)] < threshold)
        break;
      a.push_back(v);
      if (need == 1)
        dfs({}, 0, weight + w[size_t(v)]);
      else {
        std::vector<int> next;
        int64_t bound =
            weight + w[size_t(v)] + (need - 2) * w[size_t(cand[i + 1])];
        for (size_t j = i + 1; j < cand.size(); ++j) {
          int u = cand[j];
          if (bound + w[size_t(u)] < threshold)
            break;
          if (!(sets[size_t(u)] & sets[size_t(v)]))
            next.push_back(u);
        }
        dfs(next, need - 1, weight + w[size_t(v)]);
      }
      a.pop_back();
    }
  }
};
int main(int argc, char **argv) {
  try {
    if (argc != 4)
      throw std::runtime_error(
          "usage: packing_reference sorted_sets weights output");
    Ref r;
    std::ifstream si(argv[1]), wi(argv[2]);
    if (!si || !wi)
      throw std::runtime_error("cannot open input");
    std::vector<int64_t> pw;
    int64_t value;
    while (wi >> value) {
      if (value < 0 || value > 1000000)
        throw std::runtime_error("invalid weight");
      pw.push_back(value);
    }
    if (pw.size() != 84)
      throw std::runtime_error("bad weights");
    r.threshold = std::accumulate(pw.begin(), pw.end(), int64_t(0)) - 6000000;
    std::string line;
    while (std::getline(si, line)) {
      std::istringstream in(line);
      int x;
      U m = 0;
      int64_t weight = 0;
      while (in >> x) {
        if (x < 0 || x >= 84)
          throw std::runtime_error("bad point");
        m |= U(1) << x;
        weight += pw[size_t(x)];
      }
      r.sets.push_back(m);
      r.w.push_back(weight);
    }
    if (!std::is_sorted(r.w.begin(), r.w.end(), std::greater<>()))
      throw std::runtime_error("weights not sorted");
    r.out.open(argv[3]);
    if (!r.out)
      throw std::runtime_error("open failed");
    std::vector<int> all(r.sets.size());
    std::iota(all.begin(), all.end(), 0);
    auto start = std::chrono::steady_clock::now();
    r.dfs(all, 5, 0);
    r.out.flush();
    if (!r.out)
      throw std::runtime_error("write failed");
    std::cout << "{\"packings\":" << r.found << ",\"nodes\":" << r.nodes
              << ",\"seconds\":"
              << std::chrono::duration<double>(
                     std::chrono::steady_clock::now() - start)
                     .count()
              << ",\"complete\":true}\n";
  } catch (const std::exception &e) {
    std::cerr << e.what() << '\n';
    return 1;
  }
}
