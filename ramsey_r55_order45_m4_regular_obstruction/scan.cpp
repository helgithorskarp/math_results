#include <array>
#include <bit>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <string>

using Mask = std::uint32_t;
constexpr int ORDER = 24;

struct Graph {
  std::array<Mask, ORDER> adj{};
};

static Graph decode_graph6(const std::string &line) {
  if (line.empty() || static_cast<unsigned char>(line[0]) - 63 != ORDER)
    throw std::runtime_error("record is not short graph6 of order 24");
  constexpr std::size_t bits = ORDER * (ORDER - 1) / 2;
  if (line.size() != 1 + (bits + 5) / 6)
    throw std::runtime_error("malformed graph6 record");
  Graph graph;
  int pos = 0;
  for (int j = 1; j < ORDER; ++j) {
    for (int i = 0; i < j; ++i, ++pos) {
      const int x = static_cast<unsigned char>(line[1 + pos / 6]) - 63;
      if (x < 0 || x > 63) throw std::runtime_error("bad graph6 byte");
      if ((x >> (5 - pos % 6)) & 1) {
        graph.adj[i] |= Mask{1} << j;
        graph.adj[j] |= Mask{1} << i;
      }
    }
  }
  return graph;
}

int main(int argc, char **argv) {
  if (argc != 2) {
    std::cerr << "usage: scan CATALOGUE.g6\n";
    return 2;
  }
  std::ifstream input(argv[1]);
  if (!input) throw std::runtime_error("cannot open catalogue");

  constexpr Mask all = (Mask{1} << ORDER) - 1;
  std::string line;
  std::uint64_t index = 0;
  std::int64_t minimum = std::numeric_limits<std::int64_t>::max();
  std::int64_t maximum = std::numeric_limits<std::int64_t>::min();
  while (std::getline(input, line)) {
    if (!line.empty() && line.back() == '\r') line.pop_back();
    if (line.empty()) throw std::runtime_error("empty catalogue record");
    const Graph graph = decode_graph6(line);
    const auto &adj = graph.adj;

    int degree_sum = 0;
    for (int v = 0; v < ORDER; ++v) degree_sum += std::popcount(adj[v]);
    if (degree_sum % 2) throw std::runtime_error("odd degree sum");
    const int edges = degree_sum / 2;

    std::uint64_t triangles = 0;
    std::uint64_t t31 = 0;
    std::uint64_t t32_incidence = 0;
    for (int a = 0; a < ORDER; ++a) {
      for (int b = a + 1; b < ORDER; ++b) {
        if (!((adj[a] >> b) & 1U)) continue;
        for (int c = b + 1; c < ORDER; ++c) {
          if (!((adj[a] >> c) & 1U) || !((adj[b] >> c) & 1U)) continue;
          ++triangles;
          const Mask triple = (Mask{1} << a) | (Mask{1} << b) | (Mask{1} << c);
          for (int x = 0; x < ORDER; ++x) {
            if ((triple >> x) & 1U) continue;
            const int joined = std::popcount(adj[x] & triple);
            if (joined == 1) ++t31;
            else if (joined == 2) ++t32_incidence;
            else if (joined == 3) throw std::runtime_error("catalogue contains K4");
          }
        }
      }
    }
    if (t32_incidence % 2) throw std::runtime_error("odd T32 incidence count");
    const std::uint64_t t32 = t32_incidence / 2;

    // Check alpha < 5 while enumerating independent four-sets.  The count is
    // not needed for the theorem, but this verifies the catalogue records are
    // (4,5)-graphs rather than merely K4-free graphs.
    for (int a = 0; a < ORDER; ++a) {
      for (int b = a + 1; b < ORDER; ++b) {
        if ((adj[a] >> b) & 1U) continue;
        for (int c = b + 1; c < ORDER; ++c) {
          if (((adj[a] | adj[b]) >> c) & 1U) continue;
          for (int d = c + 1; d < ORDER; ++d) {
            if (((adj[a] | adj[b] | adj[c]) >> d) & 1U) continue;
            const Mask four = (Mask{1} << a) | (Mask{1} << b) |
                              (Mask{1} << c) | (Mask{1} << d);
            const Mask common_non = all & ~four &
                ~(adj[a] | adj[b] | adj[c] | adj[d]);
            if (common_non) throw std::runtime_error("catalogue contains independent 5-set");
          }
        }
      }
    }

    // Twelve times the right-hand summand in the m=4 identity at ambient
    // order 45.  Since the neighbourhood is K4-free, its K4 term vanishes:
    // 12 R(H) = -129 K3(H) + 6 T31(H) + 16 T32(H).
    const std::int64_t r12 = -129 * static_cast<std::int64_t>(triangles)
                           + 6 * static_cast<std::int64_t>(t31)
                           + 16 * static_cast<std::int64_t>(t32);
    minimum = std::min(minimum, r12);
    maximum = std::max(maximum, r12);
    std::cout << index << ' ' << edges << ' ' << triangles << ' ' << t31
              << ' ' << t32 << ' ' << r12 << '\n';
    ++index;
  }
  std::cerr << "complete=1 records=" << index << " min_r12=" << minimum
            << " max_r12=" << maximum << '\n';
}
