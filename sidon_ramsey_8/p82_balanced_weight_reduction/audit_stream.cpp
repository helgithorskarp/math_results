// Definition-level stream audit, independent of the catalog and recursion code.
#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <vector>
using Mask = __uint128_t;
uint64_t bytes = 0;
uint64_t word() {
  std::array<unsigned char, 8> b{};
  if (!std::cin.read(reinterpret_cast<char *>(b.data()), 8))
    throw std::runtime_error("truncated word");
  uint64_t x = 0;
  for (int i = 0; i < 8; ++i)
    x |= uint64_t(b[size_t(i)]) << (8 * i);
  bytes += 8;
  return x;
}
Mask mask() {
  uint64_t a = word(), b = word();
  return Mask(a) | (Mask(b) << 64);
}
std::vector<int> points(Mask a) {
  if (a >> 82)
    throw std::runtime_error("point range");
  std::vector<int> p;
  for (int i = 0; i < 82; ++i)
    if (a & (Mask(1) << i))
      p.push_back(i);
  return p;
}
bool sidon(const std::vector<int> &p) {
  std::array<bool, 163> used{};
  for (size_t i = 0; i < p.size(); ++i)
    for (size_t j = i; j < p.size(); ++j) {
      size_t s = size_t(p[i] + p[j]);
      if (used[s])
        return false;
      used[s] = true;
    }
  return true;
}
int main(int argc, char **argv) {
  try {
    if (argc != 8)
      throw std::runtime_error(
          "weights orbit minimum maximum shard parts budget");
    std::array<int, 82> w{};
    std::ifstream in(argv[1]);
    for (int &x : w)
      if (!(in >> x) || x < 0 || x > 1000000)
        throw std::runtime_error("weights");
    std::string extra;
    if (in >> extra)
      throw std::runtime_error("weight length");
    auto weight = [&](Mask a) {
      int z = 0;
      for (int x : points(a))
        z += w[size_t(x)];
      return z;
    };
    std::vector<Mask> sets;
    std::ifstream orbit(argv[2]);
    std::string line;
    while (std::getline(orbit, line)) {
      std::istringstream row(line);
      int x;
      Mask a = 0;
      while (row >> x) {
        if (x < 0 || x >= 82 || (a & (Mask(1) << x)))
          throw std::runtime_error("orbit point");
        a |= Mask(1) << x;
      }
      if (!row.eof() || points(a).size() != 11 || !sidon(points(a)))
        throw std::runtime_error("orbit row");
      sets.push_back(a);
    }
    if (!orbit.eof() || sets.size() != 8214)
      throw std::runtime_error("orbit input");
    int minimum = std::stoi(argv[3]), maximum = std::stoi(argv[4]),
        shard = std::stoi(argv[5]), parts = std::stoi(argv[6]);
    uint64_t budget = std::stoull(argv[7]);
    if (minimum < 0 || minimum > maximum || maximum > 4107 || parts < 1 ||
        shard < 0 || shard >= parts || !budget)
      throw std::runtime_error("parameters");
    std::vector<int> ws;
    for (Mask a : sets)
      ws.push_back(weight(a));
    std::vector<std::array<size_t, 2>> expected;
    for (int q = maximum; q-- > minimum;)
      if (q % parts == shard)
        for (size_t j = size_t(2 * q + 1); j < sets.size(); ++j)
          if (!(sets[size_t(2 * q)] & sets[j]) &&
              ws[size_t(2 * q)] + ws[j] >= 6884468)
            expected.push_back({size_t(2 * q), j});
    bool active = false;
    Mask root = 0;
    uint64_t pairs = 0, records = 0, options = 0, leaves = 0, largest = 0,
             pair_options = 0, pair_leaves = 0, pair_records = 0, unsat = 0,
             unknown = 0, sat = 0, calls = 0, queries = 0;
    while (std::cin.peek() != std::char_traits<char>::eof()) {
      uint64_t type = word();
      if (type == 1) {
        if (active || pairs >= expected.size())
          throw std::runtime_error("pair nesting/count");
        uint64_t i = word(), j = word();
        if (i != expected[size_t(pairs)][0] || j != expected[size_t(pairs)][1])
          throw std::runtime_error("pair cover/order");
        root = ((Mask(1) << 82) - 1) ^ (sets[size_t(i)] | sets[size_t(j)]);
        pair_options = pair_leaves = pair_records = 0;
        active = true;
      } else if (type == 2) {
        if (!active)
          throw std::runtime_error("query outside pair");
        Mask d = mask();
        uint64_t r = word(), upper = word(), count = word();
        if (r < 2 || r > 6 || points(d).size() != 10 * r || (d & ~root) ||
            upper > 4000000 || !count || count > 17249580)
          throw std::runtime_error("query parameters");
        int total = weight(d), lower = (total + int(r) - 1) / int(r);
        if (uint64_t(total) > r * upper)
          throw std::runtime_error("unpruned query");
        Mask previous = 0;
        for (uint64_t k = 0; k < count; ++k) {
          Mask a = mask();
          auto p = points(a);
          if (p.size() != 10 || (a & ~d) || a <= previous)
            throw std::runtime_error("candidate set/order");
          int value = weight(a);
          if (value < lower || uint64_t(value) > upper)
            throw std::runtime_error("candidate weight");
          if (!sidon(p))
            throw std::runtime_error("candidate pair-sum collision");
          previous = a;
        }
        ++records;
        ++pair_records;
        options += count;
        pair_options += count;
        largest = std::max(largest, count);
      } else if (type == 3) {
        if (!active)
          throw std::runtime_error("leaf outside pair");
        Mask d = mask();
        uint64_t upper = word(), ok = word();
        auto p = points(d);
        if (p.size() != 10 || (d & ~root) || upper > 4000000 ||
            uint64_t(weight(d)) > upper || ok > 1 || bool(ok) != sidon(p))
          throw std::runtime_error("terminal check");
        ++leaves;
        ++pair_leaves;
      } else if (type == 4) {
        if (!active)
          throw std::runtime_error("result outside pair");
        uint64_t status = word(), c = word(), q = word(), o = word(),
                 l = word();
        if (status > 2 || o != pair_options || l != pair_leaves ||
            q < pair_records || c < 1 || c > budget + 1)
          throw std::runtime_error("pair accounting");
        if (status == 0) {
          ++unsat;
          if (c != o + 1)
            throw std::runtime_error("unsat call identity");
        } else if (status == 1) {
          ++unknown;
          if (c != budget + 1)
            throw std::runtime_error("unknown call limit");
        } else
          ++sat;
        calls += c;
        queries += q;
        ++pairs;
        active = false;
      } else
        throw std::runtime_error("record type");
    }
    if (std::cin.bad() || active || pairs != expected.size())
      throw std::runtime_error("incomplete stream");
    std::cout << "{\"verified\":true,\"bytes\":" << bytes
              << ",\"pairs\":" << pairs << ",\"unsat\":" << unsat
              << ",\"unknown\":" << unknown << ",\"sat\":" << sat
              << ",\"records\":" << records << ",\"options\":" << options
              << ",\"leaves\":" << leaves << ",\"calls\":" << calls
              << ",\"queries\":" << queries
              << ",\"largest_option_list\":" << largest << "}\n";
  } catch (std::exception &e) {
    std::cerr << e.what() << '\n';
    return 1;
  }
}
