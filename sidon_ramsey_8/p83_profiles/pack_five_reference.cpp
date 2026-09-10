#include <algorithm>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>
using U = __uint128_t;
struct Packing {
  int n, k, target;
  size_t words;
  uint64_t nodes = 0, found = 0;
  std::vector<U> sets;
  std::vector<uint64_t> adj;
  std::vector<int> chosen;
  std::vector<int64_t> weight;
  int64_t threshold = 0, current = 0;
  std::ofstream out;
  static int pop(const std::vector<uint64_t> &a) {
    int n = 0;
    for (auto x : a)
      n += __builtin_popcountll(x);
    return n;
  }
  void sparse(const std::vector<int> &cand, int remain) {
    ++nodes;
    int64_t upper = current;
    for (size_t i = 0; i < cand.size() && i < size_t(remain); ++i)
      upper += weight[size_t(cand[i])];
    if (upper < threshold)
      return;
    if (remain == 0) {
      ++found;
      if (out.is_open()) {
        for (size_t i = 0; i < chosen.size(); ++i)
          out << (i ? " " : "") << chosen[i];
        out << '\n';
      }
      return;
    }
    if (cand.size() < size_t(remain))
      return;
    for (size_t i = 0; i + size_t(remain) <= cand.size(); ++i) {
      int v = cand[i];
      chosen.push_back(v);
      current += weight[size_t(v)];
      if (remain == 1)
        sparse({}, 0);
      else {
        std::vector<int> next;
        for (size_t j = i + 1; j < cand.size(); ++j)
          if (!(sets[size_t(v)] & sets[size_t(cand[j])]))
            next.push_back(cand[j]);
        sparse(next, remain - 1);
      }
      current -= weight[size_t(v)];
      chosen.pop_back();
    }
  }
  void dfs(std::vector<uint64_t> cand, int remain) {
    ++nodes;
    if (remain <= 3) {
      std::vector<int> list;
      for (size_t w = 0; w < words; ++w) {
        auto bits = cand[w];
        while (bits) {
          int b = __builtin_ctzll(bits);
          bits &= bits - 1;
          list.push_back(int(w * 64) + b);
        }
      }
      sparse(list, remain);
      return;
    }
    int count = pop(cand);
    if (count < remain)
      return;
    int need = remain;
    int64_t upper = current;
    for (size_t w = 0; w < words && need; ++w) {
      auto bits = cand[w];
      while (bits && need) {
        int b = __builtin_ctzll(bits);
        bits &= bits - 1;
        upper += weight[w * 64 + size_t(b)];
        --need;
      }
    }
    if (upper < threshold)
      return;
    for (size_t w = 0; w < words; ++w)
      while (cand[w]) {
        int b = __builtin_ctzll(cand[w]);
        cand[w] &= cand[w] - 1;
        --count;
        int v = int(w * 64) + b;
        if (chosen.empty() && v % 5000 == 0)
          std::cerr << "root=" << v << " packings=" << found << '\n';
        chosen.push_back(v);
        current += weight[size_t(v)];
        if (remain == 1)
          dfs({}, 0);
        else if (count >= remain - 1) {
          std::vector<uint64_t> next(words);
          for (size_t j = w; j < words; ++j)
            next[j] = cand[j] & adj[size_t(v) * words + j];
          dfs(std::move(next), remain - 1);
        }
        current -= weight[size_t(v)];
        chosen.pop_back();
        if (count < remain)
          return;
      }
  }
  void run() {
    words = (sets.size() + 63) / 64;
    adj.assign(sets.size() * words, 0);
    uint64_t edges = 0;
    for (size_t i = 0; i < sets.size(); ++i)
      for (size_t j = i + 1; j < sets.size(); ++j)
        if (!(sets[i] & sets[j])) {
          adj[i * words + j / 64] |= uint64_t(1) << (j % 64);
          ++edges;
        }
    std::cerr << "vertices=" << sets.size() << " edges=" << edges
              << " adjacency_bytes=" << adj.size() * 8 << '\n';
    std::vector<uint64_t> all(words, ~uint64_t(0));
    if (sets.size() % 64)
      all.back() = (uint64_t(1) << (sets.size() % 64)) - 1;
    dfs(std::move(all), target);
  }
};
int main(int argc, char **argv) {
  try {
    if (argc != 7)
      throw std::runtime_error(
          "usage: packing_weighted N K TARGET sets.txt weights.txt tuples.txt");
    Packing p;
    p.n = std::stoi(argv[1]);
    p.k = std::stoi(argv[2]);
    p.target = std::stoi(argv[3]);
    if (p.n != 83 || p.k != 11 || p.target != 5)
      throw std::runtime_error("invalid parameters");
    std::ifstream in(argv[4]);
    if (!in)
      throw std::runtime_error("open input failed");
    std::string line;
    while (std::getline(in, line)) {
      std::istringstream s(line);
      int a, count = 0;
      U mask = 0;
      while (s >> a) {
        if (a < 0 || a >= p.n || (mask & (U(1) << a)))
          throw std::runtime_error("invalid row");
        mask |= U(1) << a;
        ++count;
      }
      if (count != p.k)
        throw std::runtime_error("wrong row size");
      p.sets.push_back(mask);
    }
    std::ifstream weights(argv[5]);
    int64_t z;
    std::vector<int64_t> point_weights;
    while (weights >> z)
      point_weights.push_back(z);
    if (point_weights.size() != size_t(p.n))
      throw std::runtime_error("wrong weights length");
    for (auto value : point_weights) {
      if (value < 0)
        throw std::runtime_error("negative weight");
      p.threshold += value;
    }
    p.threshold -= 12000000;
    std::vector<std::pair<int64_t, U>> order;
    for (auto mask : p.sets) {
      int64_t val = 0;
      for (int x = 0; x < p.n; ++x)
        if (mask & (U(1) << x))
          val += point_weights[size_t(x)];
      order.push_back({val, mask});
    }
    std::sort(order.begin(), order.end(), [](const auto &a, const auto &b) {
      return a.first != b.first ? a.first > b.first : a.second < b.second;
    });
    p.sets.clear();
    for (auto row : order) {
      p.weight.push_back(row.first);
      p.sets.push_back(row.second);
    }
    p.out.open(argv[6]);
    if (!p.out)
      throw std::runtime_error("open output failed");
    std::ofstream ordered(std::string(argv[6]) + ".sets");
    if (!ordered)
      throw std::runtime_error("open reordered sets failed");
    for (auto mask : p.sets) {
      bool space = false;
      for (int x = 0; x < p.n; ++x)
        if (mask & (U(1) << x)) {
          if (space)
            ordered << ' ';
          space = true;
          ordered << x;
        }
      ordered << '\n';
    }
    ordered.close();
    auto start = std::chrono::steady_clock::now();
    p.run();
    if (p.out.is_open()) {
      p.out.flush();
      if (!p.out)
        throw std::runtime_error("write failed");
    }
    std::cout << "{\"n\":" << p.n << ",\"k\":" << p.k
              << ",\"target\":" << p.target << ",\"packings\":" << p.found
              << ",\"nodes\":" << p.nodes << ",\"seconds\":"
              << std::chrono::duration<double>(
                     std::chrono::steady_clock::now() - start)
                     .count()
              << ",\"complete\":true}\n";
  } catch (const std::exception &e) {
    std::cerr << e.what() << '\n';
    return 1;
  }
}
