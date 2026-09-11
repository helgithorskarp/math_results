#pragma once
#include "core.hpp"
#include <memory>
struct Limit {};
// Canonical little-endian trace, buffered independently of the search.
struct Trace {
  std::ostream &out;
  std::array<char, 65536> buffer{};
  size_t used = 0;
  uint64_t bytes = 0;
  void flush() {
    out.write(buffer.data(), std::streamsize(used));
    used = 0;
    if (!out)
      throw std::runtime_error("trace write");
  }
  void word(uint64_t x) {
    if (used + 8 > buffer.size())
      flush();
    for (int i = 0; i < 8; ++i)
      buffer[used++] = char((x >> (8 * i)) & 255);
    if (bytes > UINT64_MAX - 8)
      throw std::runtime_error("trace byte overflow");
    bytes += 8;
  }
  void mask(U x) {
    word(uint64_t(x));
    word(uint64_t(x >> 64));
  }
};
struct Search {
  const Weights &w;
  const Catalog &parent;
  int method;
  uint64_t budget;
  Trace *trace = nullptr;
  uint64_t calls = 0, queries = 0, options = 0, leaves = 0;
  std::vector<U> chosen = {};
  std::vector<U> query(U d, int lo, int hi) const {
    if (lo < parent.minweight)
      throw std::runtime_error("parent cutoff");
    if (method)
      return parent.query(d, lo, hi);
    std::vector<U> out;
    auto begin =
        std::lower_bound(parent.ordered_weights.begin(),
                         parent.ordered_weights.end(), hi, std::greater<>());
    auto end =
        std::upper_bound(parent.ordered_weights.begin(),
                         parent.ordered_weights.end(), lo, std::greater<>());
    for (auto it = begin; it < end; ++it) {
      U a =
          parent
              .masks[parent.order[size_t(it - parent.ordered_weights.begin())]];
      if (!(a & ~d))
        out.push_back(a);
    }
    std::sort(out.begin(), out.end());
    return out;
  }
  bool visit(U d, int r, int upper) {
    if (++calls > budget)
      throw Limit{};
    if (r < 1 || r > 6 || pop(d) != 10 * r || upper < 0 || upper > cap)
      throw std::runtime_error("state");
    int total = w(d);
    if (total > r * upper)
      return false;
    if (r == 1) {
      ++leaves;
      bool ok = sidon(d, method);
      if (trace) {
        trace->word(3);
        trace->mask(d);
        trace->word(uint64_t(upper));
        trace->word(ok);
      }
      if (ok)
        chosen.push_back(d);
      return ok;
    }
    ++queries;
    auto a = query(d, (total + r - 1) / r, upper);
    options += a.size();
    if (trace && !a.empty()) {
      trace->word(2);
      trace->mask(d);
      trace->word(uint64_t(r));
      trace->word(uint64_t(upper));
      trace->word(a.size());
      for (U b : a)
        trace->mask(b);
    }
    for (U b : a) {
      chosen.push_back(b);
      if (visit(d ^ b, r - 1, w(b)))
        return true;
      chosen.pop_back();
    }
    return false;
  }
};
