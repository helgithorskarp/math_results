// Exact heaviest-class recursion and two complete P84 packing traversals.
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
constexpr U universe = (U(1) << 84) - 1;
constexpr int cap = 2000000, total_weight = 15685948;
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
    if (x < 0 || x >= 84 || (mask & (U(1) << x)))
      throw std::runtime_error("point");
    mask |= U(1) << x;
  }
  if (!in.eof())
    throw std::runtime_error("set token");
  return mask;
}
struct Weights {
  std::array<int, 84> w{};
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
struct Catalog {
  const Weights &weight;
  int size, minweight, method;
  std::vector<U> masks;
  std::vector<int> weights;
  struct Node {
    U common;
    uint32_t left, right;
    int maximum;
  };
  std::vector<Node> nodes;
  static constexpr uint32_t leaf = uint32_t(1) << 31;
  uint32_t root = leaf;
  std::vector<size_t> order;
  std::vector<int> ordered_weights;
  std::array<std::vector<uint64_t>, 84> incidence;
  std::array<int, 84> point_order{};
  U common(uint32_t id) const {
    return id & leaf ? masks[id & ~leaf] : nodes[id].common;
  }
  int maximum(uint32_t id) const {
    return id & leaf ? weights[id & ~leaf] : nodes[id].maximum;
  }
  uint32_t build(size_t lo, size_t hi) {
    if (hi - lo == 1)
      return leaf | uint32_t(lo);
    U d = masks[lo] ^ masks[hi - 1];
    int bit = uint64_t(d >> 64) ? 127 - __builtin_clzll(uint64_t(d >> 64))
                                : 63 - __builtin_clzll(uint64_t(d));
    U target = (masks[lo] >> bit << bit) | (U(1) << bit);
    size_t mid =
        size_t(std::lower_bound(masks.begin() + std::ptrdiff_t(lo),
                                masks.begin() + std::ptrdiff_t(hi), target) -
               masks.begin());
    if (mid == lo || mid == hi)
      throw std::runtime_error("radix split");
    uint32_t id = uint32_t(nodes.size());
    nodes.push_back({0, 0, 0, 0});
    uint32_t l = build(lo, mid), r = build(mid, hi);
    nodes[id] = {common(l) & common(r), l, r, std::max(maximum(l), maximum(r))};
    return id;
  }
  Catalog(const char *path, const Weights &w, int k, int cut, int alg)
      : weight(w), size(k), minweight(cut), method(alg) {
    if (k < 2 || k > 12 || cut < 0 || (alg != 0 && alg != 1))
      throw std::runtime_error("catalog parameters");
    std::ifstream in(path, std::ios::binary);
    if (!in)
      throw std::runtime_error("catalog input");
    std::array<unsigned char, 12> a{};
    while (in.read(reinterpret_cast<char *>(a.data()), k)) {
      U m = 0;
      for (int i = 0; i < k; ++i) {
        if (a[size_t(i)] >= 84 || (i && a[size_t(i - 1)] >= a[size_t(i)]))
          throw std::runtime_error("catalog point");
        m |= U(1) << a[size_t(i)];
      }
      int v = weight(m);
      if (v < cut || !sidon(m, alg) || (!masks.empty() && m <= masks.back()))
        throw std::runtime_error("catalog set/order/weight");
      masks.push_back(m);
      weights.push_back(v);
    }
    if (!in.eof() || in.gcount() || masks.size() >= leaf)
      throw std::runtime_error("catalog read");
    if (masks.empty())
      return;
    if (!alg) {
      nodes.reserve(masks.size() - 1);
      root = build(0, masks.size());
      return;
    }
    order.resize(masks.size());
    std::iota(order.begin(), order.end(), 0);
    std::sort(order.begin(), order.end(), [&](size_t a0, size_t b) {
      return weights[a0] != weights[b] ? weights[a0] > weights[b] : a0 < b;
    });
    size_t words = (masks.size() + 63) / 64;
    for (auto &v : incidence)
      v.resize(words);
    std::array<size_t, 84> frequencies{};
    for (size_t i = 0; i < order.size(); ++i) {
      ordered_weights.push_back(weights[order[i]]);
      U m = masks[order[i]];
      while (m) {
        int p = first(m);
        m &= m - 1;
        incidence[size_t(p)][i / 64] |= uint64_t(1) << (i % 64);
        ++frequencies[size_t(p)];
      }
    }
    std::iota(point_order.begin(), point_order.end(), 0);
    std::stable_sort(point_order.begin(), point_order.end(),
                     [&](int a0, int b) {
                       return frequencies[size_t(a0)] > frequencies[size_t(b)];
                     });
  }
  void radix(uint32_t id, U forbidden, int lower, int upper,
             std::vector<U> &out) const {
    if (maximum(id) < lower || (common(id) & forbidden))
      return;
    if (id & leaf) {
      if (weights[id & ~leaf] <= upper)
        out.push_back(masks[id & ~leaf]);
      return;
    }
    radix(nodes[id].left, forbidden, lower, upper, out);
    radix(nodes[id].right, forbidden, lower, upper, out);
  }
  std::vector<U> query(U domain, int lower, int upper) const {
    std::vector<U> answer;
    if (masks.empty() || lower > upper)
      return answer;
    if (!method) {
      radix(root, universe ^ domain, lower, upper, answer);
      return answer;
    }
    auto begin =
        std::lower_bound(ordered_weights.begin(), ordered_weights.end(), upper,
                         std::greater<>());
    auto end = std::upper_bound(ordered_weights.begin(), ordered_weights.end(),
                                lower, std::greater<>());
    size_t lo = size_t(begin - ordered_weights.begin()),
           hi = size_t(end - ordered_weights.begin());
    if (lo >= hi)
      return answer;
    std::array<int, 84> forbidden{};
    size_t count = 0;
    for (int p : point_order)
      if (!(domain & (U(1) << p)))
        forbidden[count++] = p;
    for (size_t word = lo / 64; word < (hi + 63) / 64; ++word) {
      uint64_t bits = ~uint64_t(0);
      if (word == lo / 64)
        bits &= ~uint64_t(0) << (lo % 64);
      if (word == hi / 64)
        bits &= (uint64_t(1) << (hi % 64)) - 1;
      for (size_t i = 0; i < count && bits; ++i)
        bits &= ~incidence[size_t(forbidden[i])][word];
      while (bits) {
        int bit = __builtin_ctzll(bits);
        bits &= bits - 1;
        answer.push_back(masks[order[word * 64 + size_t(bit)]]);
      }
    }
    std::sort(answer.begin(), answer.end());
    return answer;
  }
};
struct Heavy {
  const Catalog &catalog;
  std::array<uint64_t, 5> calls{}, candidates{};
  std::array<size_t, 4> eleven_ids{};
  std::vector<U> chosen{};
  std::ostream *trace = nullptr, *terminal = nullptr;
  void word(uint64_t x) {
    for (int i = 0; i < 8; ++i)
      trace->put(char((x >> (8 * i)) & 255));
  }
  void mask(U x) {
    word(uint64_t(x));
    word(uint64_t(x >> 64));
  }
  std::vector<U> visit(U domain, int k, int upper) {
    if (k < 1 || k > 4 || pop(domain) != k * catalog.size)
      throw std::runtime_error("cover state");
    ++calls[size_t(k)];
    int sum = catalog.weight(domain);
    if (sum > k * upper)
      return {};
    if (k == 1) {
      bool good = sidon(domain, catalog.method);
      if (terminal) {
        *terminal << "{\"eleven_ids\":[";
        for (size_t i = 0; i < 4; ++i) {
          if (i)
            *terminal << ',';
          *terminal << eleven_ids[i];
        }
        *terminal << "],\"chosen_tens\":[";
        for (size_t i = 0; i < chosen.size(); ++i) {
          if (i)
            *terminal << ',';
          printset(chosen[i], *terminal);
        }
        *terminal << "],\"residual\":";
        printset(domain, *terminal);
        *terminal << ",\"sidon\":" << (good ? "true" : "false") << "}\n";
      }
      return good ? std::vector<U>{domain} : std::vector<U>{};
    }
    int lower = (sum + k - 1) / k;
    if (lower < catalog.minweight)
      throw std::runtime_error("insufficient catalog cutoff");
    auto options = catalog.query(domain, lower, upper);
    candidates[size_t(k)] += options.size();
    if (trace && !options.empty()) {
      mask(domain);
      word(uint64_t(k));
      word(uint64_t(upper));
      word(options.size());
      for (U a : options)
        mask(a);
    }
    for (U a : options) {
      chosen.push_back(a);
      auto answer = visit(domain ^ a, k - 1, catalog.weight(a));
      chosen.pop_back();
      if (!answer.empty()) {
        answer.push_back(a);
        return answer;
      }
    }
    return {};
  }
};
struct Packing {
  const Weights &weight;
  Heavy &heavy;
  int method, shard, parts;
  std::vector<U> sets;
  std::vector<int> weights;
  std::array<size_t, 4> ids{};
  uint64_t packings = 0, found = 0;
  std::ostream &out;
  Packing(const char *path, const Weights &w, Heavy &h, int alg, int s, int n,
          std::ostream &o)
      : weight(w), heavy(h), method(alg), shard(s), parts(n), out(o) {
    if (n < 1 || s < 0 || s >= n || weight(universe) != total_weight ||
        !std::equal(w.w.begin(), w.w.end(), w.w.rbegin()))
      throw std::runtime_error("packing parameters");
    std::ifstream in(path);
    if (!in)
      throw std::runtime_error("eleven input");
    std::string line;
    while (std::getline(in, line)) {
      U m = readset(line);
      if (pop(m) != 11 || !sidon(m, alg) || weight(m) > cap)
        throw std::runtime_error("eleven set");
      sets.push_back(m);
      weights.push_back(weight(m));
    }
    if (!in.eof() || sets.size() != 30510 ||
        !std::is_sorted(weights.begin(), weights.end(), std::greater<>()))
      throw std::runtime_error("eleven catalog");
    for (size_t a = 0; a < sets.size(); a += 2) {
      U r = 0;
      for (int x = 0; x < 84; ++x)
        if (sets[a] & (U(1) << x))
          r |= U(1) << (83 - x);
      if (r != sets[a + 1] || sets[a] >= sets[a + 1] ||
          (a && weights[a] == weights[a - 2] && sets[a] <= sets[a - 2]))
        throw std::runtime_error("orbit order");
    }
  }
  void leaf(U used, int w) {
    if (w < threshold || pop(used) != 44)
      throw std::runtime_error("packing leaf");
    ++packings;
    heavy.eleven_ids = ids;
    auto answer = heavy.visit(universe ^ used, 4, cap);
    if (!answer.empty()) {
      ++found;
      std::cerr << "P84 witness eleven IDs:";
      for (size_t i : ids)
        std::cerr << ' ' << i;
      std::cerr << '\n';
      for (U a : answer) {
        printset(a, std::cerr);
        std::cerr << '\n';
      }
    }
  }
  void recursive(const std::vector<size_t> &cand, int need, U used, int w) {
    if (cand.size() < size_t(need))
      return;
    int bound = w;
    for (int i = 0; i < need; ++i)
      bound += weights[cand[size_t(i)]];
    if (bound < threshold)
      return;
    for (size_t i = 0; i + size_t(need) <= cand.size(); ++i) {
      size_t b = cand[i];
      if (w + need * weights[b] < threshold)
        break;
      ids[size_t(4 - need)] = b;
      if (need == 1) {
        leaf(used | sets[b], w + weights[b]);
        continue;
      }
      std::vector<size_t> next;
      for (size_t j = i + 1; j < cand.size(); ++j)
        if (!(sets[b] & sets[cand[j]]))
          next.push_back(cand[j]);
      recursive(next, need - 1, used | sets[b], w + weights[b]);
    }
  }
  void fixed(size_t a, const std::vector<size_t> &cand) {
    for (size_t i = 0; i + 2 < cand.size(); ++i) {
      size_t b = cand[i];
      if (weights[a] + 3 * weights[b] < threshold)
        break;
      ids[1] = b;
      for (size_t j = i + 1; j + 1 < cand.size(); ++j) {
        size_t c = cand[j];
        if (weights[a] + weights[b] + 2 * weights[c] < threshold)
          break;
        if (sets[b] & sets[c])
          continue;
        ids[2] = c;
        U used = sets[a] | sets[b] | sets[c];
        int need = threshold - weights[a] - weights[b] - weights[c];
        for (size_t k = j + 1; k < cand.size(); ++k) {
          size_t d = cand[k];
          if (weights[d] < need)
            break;
          if (sets[d] & used)
            continue;
          ids[3] = d;
          leaf(used | sets[d],
               weights[a] + weights[b] + weights[c] + weights[d]);
        }
      }
    }
  }
  void run() {
    out << "orbit,packings,calls1,calls2,calls3,calls4,candidates1,candidates2,"
           "candidates3,candidates4,found\n";
    for (size_t a = 0; a < sets.size(); a += 2) {
      if (4 * weights[a] < threshold)
        break;
      if ((a / 2) % size_t(parts) != size_t(shard))
        continue;
      uint64_t oldpack = packings, oldfound = found;
      auto oldcalls = heavy.calls, oldcand = heavy.candidates;
      ids[0] = a;
      std::vector<size_t> cand;
      for (size_t b = a + 1; b < sets.size(); ++b)
        if (!(sets[a] & sets[b]))
          cand.push_back(b);
      if (method)
        recursive(cand, 3, sets[a], weights[a]);
      else
        fixed(a, cand);
      out << a / 2 << ',' << packings - oldpack;
      for (int k = 1; k <= 4; ++k)
        out << ',' << heavy.calls[size_t(k)] - oldcalls[size_t(k)];
      for (int k = 1; k <= 4; ++k)
        out << ',' << heavy.candidates[size_t(k)] - oldcand[size_t(k)];
      out << ',' << found - oldfound << '\n';
      out.flush();
      if (!out)
        throw std::runtime_error("case write");
    }
  }
};
void filter(const char *input, const char *output, const Weights &w) {
  std::ifstream in(input, std::ios::binary);
  std::ofstream out(output, std::ios::binary);
  if (!in || !out)
    throw std::runtime_error("filter IO");
  std::array<unsigned char, 10> a{};
  uint64_t count = 0, kept = 0;
  U previous = 0;
  int maximum = 0;
  while (in.read(reinterpret_cast<char *>(a.data()), 10)) {
    U m = 0;
    int sum = 0;
    for (int i = 0; i < 10; ++i) {
      if (a[size_t(i)] >= 84 || (i && a[size_t(i - 1)] >= a[size_t(i)]))
        throw std::runtime_error("filter point");
      m |= U(1) << a[size_t(i)];
      sum += w.w[a[size_t(i)]];
    }
    if (count && m <= previous)
      throw std::runtime_error("filter order");
    previous = m;
    ++count;
    maximum = std::max(maximum, sum);
    if (sum >= cutoff) {
      out.write(reinterpret_cast<char *>(a.data()), 10);
      ++kept;
    }
  }
  out.flush();
  if (!in.eof() || in.gcount() || !out)
    throw std::runtime_error("filter completion");
  std::cout << "{\"sets\":" << count << ",\"kept\":" << kept
            << ",\"cutoff\":" << cutoff << ",\"maximum\":" << maximum
            << ",\"complete\":true}\n";
}
int main(int argc, char **argv) {
  try {
    auto start = std::chrono::steady_clock::now();
    if (argc == 5 && std::string(argv[1]) == "filter") {
      Weights w(argv[2]);
      filter(argv[3], argv[4], w);
      return 0;
    }
    if (argc >= 2 && std::string(argv[1]) == "control") {
      if (argc != 8)
        throw std::runtime_error(
            "control method weights catalog size domains output");
      int method = integer(argv[2]), size = integer(argv[5]);
      Weights w(argv[3]);
      Catalog c(argv[4], w, size, 0, method);
      Heavy h{c};
      std::ifstream in(argv[6]);
      std::ofstream out(argv[7]);
      if (!in || !out)
        throw std::runtime_error("control IO");
      std::string line;
      size_t n = 0;
      while (std::getline(in, line)) {
        U r = readset(line);
        if (!pop(r) || pop(r) % size || pop(r) / size > 4)
          throw std::runtime_error("control domain");
        auto answer = h.visit(r, pop(r) / size, 12000000);
        out << "{\"found\":" << (!answer.empty() ? "true" : "false")
            << ",\"partition\":[";
        for (size_t i = 0; i < answer.size(); ++i) {
          if (i)
            out << ',';
          printset(answer[i], out);
        }
        out << "]}\n";
        ++n;
      }
      out.flush();
      if (!in.eof() || !out)
        throw std::runtime_error("control completion");
      std::cout << "{\"complete\":true,\"domains\":" << n << "}\n";
      return 0;
    }
    if (argc != 11)
      throw std::runtime_error(
          "exclude method orbit_catalog weights heavy.bin shard parts "
          "cases.csv trace.bin terminal.jsonl done.txt");
    int method = integer(argv[1]);
    Weights w(argv[3]);
    Catalog c(argv[4], w, 10, cutoff, method);
    if (c.masks.size() != 901286 ||
        *std::max_element(c.weights.begin(), c.weights.end()) > cap)
      throw std::runtime_error("heavy catalog");
    Heavy h{c};
    std::ofstream cases(argv[7]), trace(argv[8], std::ios::binary),
        terminal(argv[9]);
    // The final argument is an explicit completion marker path, created only on
    // success.
    if (!cases || !trace || !terminal)
      throw std::runtime_error("outputs");
    h.trace = &trace;
    h.terminal = &terminal;
    Packing p(argv[2], w, h, method, integer(argv[5]), integer(argv[6]), cases);
    p.run();
    trace.flush();
    terminal.flush();
    if (!trace || !terminal)
      throw std::runtime_error("trace completion");
    std::ofstream done(argv[10]);
    if (!done)
      throw std::runtime_error("marker output");
    done << "complete\n";
    done.flush();
    if (!done)
      throw std::runtime_error("marker write");
    std::cout << "{\"method\":" << method
              << ",\"complete\":true,\"packings\":" << p.packings
              << ",\"found\":" << p.found << ",\"seconds\":"
              << std::chrono::duration<double>(
                     std::chrono::steady_clock::now() - start)
                     .count()
              << "}\n";
    return p.found ? 2 : 0;
  } catch (const std::exception &e) {
    std::cerr << e.what() << '\n';
    return 1;
  }
}
