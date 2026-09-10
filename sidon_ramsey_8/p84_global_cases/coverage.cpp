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
struct Counter {
  std::vector<U> sets;
  std::vector<int64_t> weights;
  std::vector<uint64_t> counts, both, fixed;
  std::vector<int> selected;
  int64_t threshold;
  uint64_t nodes = 0;
  std::vector<bool> selected_cases;
  std::ofstream tuples;
  void global(const std::vector<int> &cand, int need, int64_t weight) {
    ++nodes;
    if (!need) {
      if (weight < threshold)
        throw std::runtime_error("bad leaf");
      size_t j = size_t(selected.front() / 2);
      ++counts[j];
      bool invariant = true;
      for (int a : selected)
        if (std::find(selected.begin(), selected.end(), a ^ 1) ==
            selected.end())
          invariant = false;
      if (invariant)
        ++fixed[j];
      return;
    }
    if (cand.size() < size_t(need))
      return;
    int64_t upper = weight;
    for (int i = 0; i < need; ++i)
      upper += weights[size_t(cand[size_t(i)])];
    if (upper < threshold)
      return;
    for (size_t i = 0; i + size_t(need) <= cand.size(); ++i) {
      int v = cand[i];
      if (weight + need * weights[size_t(v)] < threshold)
        break;
      selected.push_back(v);
      if (need == 1)
        global({}, 0, weight + weights[size_t(v)]);
      else {
        std::vector<int> next;
        int64_t bound = weight + weights[size_t(v)] +
                        (need - 2) * weights[size_t(cand[i + 1])];
        for (size_t k = i + 1; k < cand.size(); ++k) {
          int u = cand[k];
          if (bound + weights[size_t(u)] < threshold)
            break;
          if (!(sets[size_t(u)] & sets[size_t(v)]))
            next.push_back(u);
        }
        global(next, need - 1, weight + weights[size_t(v)]);
      }
      selected.pop_back();
    }
  }
  void anchored() {
    // A different fixed-depth traversal, with direct union masks and no
    // recursive candidate filtering, checks the global histogram.
    for (size_t a = 0; a < sets.size(); a += 2) {
      if (4 * weights[a] < threshold)
        break;
      if (!selected_cases.empty() && !selected_cases[a / 2])
        continue;
      std::vector<size_t> cand;
      for (size_t b = a + 1; b < sets.size(); ++b)
        if (!(sets[a] & sets[b]))
          cand.push_back(b);
      for (size_t i = 0; i + 2 < cand.size(); ++i) {
        size_t b = cand[i];
        ++nodes;
        if (weights[a] + 3 * weights[b] < threshold)
          break;
        for (size_t j = i + 1; j + 1 < cand.size(); ++j) {
          size_t c = cand[j];
          if (weights[a] + weights[b] + 2 * weights[c] < threshold)
            break;
          if (sets[b] & sets[c])
            continue;
          U used = sets[b] | sets[c];
          int64_t need = threshold - weights[a] - weights[b] - weights[c];
          for (size_t k = j + 1; k < cand.size(); ++k) {
            size_t d = cand[k];
            if (weights[d] < need)
              break;
            if (sets[d] & used)
              continue;
            ++counts[a / 2];
            if (tuples.is_open())
              tuples << a << ' ' << b << ' ' << c << ' ' << d << '\n';
            if (b == a + 1)
              ++both[a / 2];
            if (b == (a ^ 1) && d == (c ^ 1))
              ++fixed[a / 2];
          }
        }
      }
    }
  }
};
int main(int argc, char **argv) {
  try {
    if (argc != 5 && argc != 7)
      throw std::runtime_error(
          "usage: coverage global|anchored orbit_catalog weights output.csv "
          "[selected_cases.txt tuples.txt]");
    std::string mode = argv[1];
    if (mode != "global" && mode != "anchored")
      throw std::runtime_error("mode");
    std::ifstream si(argv[2]), wi(argv[3]);
    if (!si || !wi)
      throw std::runtime_error("input");
    std::vector<int64_t> pw;
    int64_t xw;
    while (wi >> xw) {
      if (xw < 0 || xw > 2000000)
        throw std::runtime_error("weight");
      pw.push_back(xw);
    }
    if (pw.size() != 84)
      throw std::runtime_error("weight count");
    if (!std::equal(pw.begin(), pw.end(), pw.rbegin()))
      throw std::runtime_error("asymmetric weights");
    Counter r;
    r.threshold = std::accumulate(pw.begin(), pw.end(), int64_t(0)) - 8000000;
    std::string line;
    while (std::getline(si, line)) {
      std::istringstream in(line);
      int x;
      U mask = 0;
      int64_t w = 0;
      std::vector<int> points;
      while (in >> x) {
        if (x < 0 || x >= 84 || (mask & (U(1) << x)))
          throw std::runtime_error("point");
        mask |= U(1) << x;
        w += pw[size_t(x)];
        points.push_back(x);
      }
      if (points.size() != 11)
        throw std::runtime_error("set size");
      std::array<bool, 167> sums{};
      for (size_t i = 0; i < points.size(); ++i)
        for (size_t j = i; j < points.size(); ++j) {
          size_t s = size_t(points[i] + points[j]);
          if (sums[s])
            throw std::runtime_error("not Sidon");
          sums[s] = true;
        }
      r.sets.push_back(mask);
      r.weights.push_back(w);
    }
    if (r.sets.size() != 30510)
      throw std::runtime_error("catalog count");
    for (size_t a = 0; a < r.sets.size(); a += 2) {
      U reflected = 0;
      for (int i = 0; i < 84; ++i)
        if (r.sets[a] & (U(1) << i))
          reflected |= U(1) << (83 - i);
      if (reflected != r.sets[a + 1] || r.sets[a] >= r.sets[a + 1])
        throw std::runtime_error("orbit order");
      if (a && r.weights[a] == r.weights[a - 2] && r.sets[a] <= r.sets[a - 2])
        throw std::runtime_error("tie order");
    }
    if (!std::is_sorted(r.weights.begin(), r.weights.end(), std::greater<>()))
      throw std::runtime_error("weight order");
    size_t norbits = r.sets.size() / 2;
    r.counts.resize(norbits);
    r.both.resize(norbits);
    r.fixed.resize(norbits);
    if (argc == 7) {
      if (mode != "anchored")
        throw std::runtime_error("selected mode requires anchored");
      r.selected_cases.resize(norbits, false);
      std::ifstream in(argv[5]);
      size_t j;
      if (!in)
        throw std::runtime_error("selected input");
      while (in >> j) {
        if (j >= norbits || r.selected_cases[j])
          throw std::runtime_error("selected case");
        r.selected_cases[j] = true;
      }
      if (!in.eof())
        throw std::runtime_error("selected token");
      r.tuples.open(argv[6]);
      if (!r.tuples)
        throw std::runtime_error("tuple output");
    }
    auto start = std::chrono::steady_clock::now();
    if (mode == "global") {
      std::vector<int> all(r.sets.size());
      std::iota(all.begin(), all.end(), 0);
      r.global(all, 4, 0);
    } else
      r.anchored();
    std::ofstream out(argv[4]);
    if (!out)
      throw std::runtime_error("output");
    out << "orbit,weight,count,both_orientations,reflection_fixed\n";
    size_t eligible = 0, nonempty = 0;
    for (size_t j = 0; j < norbits; ++j) {
      if (4 * r.weights[2 * j] < r.threshold) {
        if (r.counts[j])
          throw std::runtime_error("ineligible leaf");
        continue;
      }
      ++eligible;
      if (r.counts[j])
        ++nonempty;
      out << j << ',' << r.weights[2 * j] << ',' << r.counts[j] << ','
          << r.both[j] << ',' << r.fixed[j] << '\n';
    }
    out.flush();
    if (!out)
      throw std::runtime_error("write");
    if (r.tuples.is_open()) {
      r.tuples.flush();
      if (!r.tuples)
        throw std::runtime_error("tuple write");
    }
    std::cout << "{\"mode\":\"" << mode << "\",\"complete\":true,\"packings\":"
              << std::accumulate(r.counts.begin(), r.counts.end(), uint64_t(0))
              << ",\"both_orientations\":"
              << std::accumulate(r.both.begin(), r.both.end(), uint64_t(0))
              << ",\"reflection_fixed\":"
              << std::accumulate(r.fixed.begin(), r.fixed.end(), uint64_t(0))
              << ",\"eligible_orbits\":" << eligible
              << ",\"nonempty_orbits\":" << nonempty << ",\"nodes\":" << r.nodes
              << ",\"seconds\":"
              << std::chrono::duration<double>(
                     std::chrono::steady_clock::now() - start)
                     .count()
              << "}\n";
  } catch (const std::exception &e) {
    std::cerr << e.what() << '\n';
    return 1;
  }
}
