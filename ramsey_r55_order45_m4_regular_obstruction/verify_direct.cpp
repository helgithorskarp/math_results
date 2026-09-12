#include <array>
#include <bit>
#include <cstdint>
#include <fstream>
#include <iostream>
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

static bool has_clique(const std::array<Mask, ORDER> &adj, Mask candidates,
                       int need) {
  if (need == 0) return true;
  if (std::popcount(candidates) < need) return false;
  while (candidates) {
    const int v = std::countr_zero(candidates);
    candidates &= candidates - 1;
    if (has_clique(adj, candidates & adj[v], need - 1)) return true;
    if (std::popcount(candidates) < need) break;
  }
  return false;
}

static std::uint64_t induced_edges(const std::array<Mask, ORDER> &adj, Mask set) {
  std::uint64_t twice = 0;
  Mask rest = set;
  while (rest) {
    const int v = std::countr_zero(rest);
    rest &= rest - 1;
    twice += std::popcount(adj[v] & set);
  }
  return twice / 2;
}

int main(int argc, char **argv) {
  if (argc != 2) {
    std::cerr << "usage: verify_direct CATALOGUE.g6\n";
    return 2;
  }
  std::ifstream input(argv[1]);
  if (!input) throw std::runtime_error("cannot open catalogue");
  constexpr Mask all = (Mask{1} << ORDER) - 1;
  std::string line;
  std::uint64_t index = 0;
  while (std::getline(input, line)) {
    if (!line.empty() && line.back() == '\r') line.pop_back();
    if (line.empty()) throw std::runtime_error("empty catalogue record");
    const Graph graph = decode_graph6(line);
    const auto &adj = graph.adj;

    if (has_clique(adj, all, 4)) throw std::runtime_error("catalogue contains K4");
    std::array<Mask, ORDER> complement{};
    for (int v = 0; v < ORDER; ++v)
      complement[v] = all & ~(Mask{1} << v) & ~adj[v];
    if (has_clique(complement, all, 5))
      throw std::runtime_error("catalogue contains independent 5-set");

    int degree_sum = 0;
    std::uint64_t triangle_incidence = 0;
    for (int v = 0; v < ORDER; ++v) {
      degree_sum += std::popcount(adj[v]);
      triangle_incidence += induced_edges(adj, adj[v]);
    }
    const int edges = degree_sum / 2;
    if (triangle_incidence % 3) throw std::runtime_error("bad triangle incidence");
    const std::uint64_t triangles = triangle_incidence / 3;

    // A T32=K4-e has a unique missing edge.  Its other two vertices form an
    // edge in the common neighbourhood of that nonedge.
    std::uint64_t t32 = 0;
    for (int a = 0; a < ORDER; ++a) {
      for (int b = a + 1; b < ORDER; ++b) {
        if ((adj[a] >> b) & 1U) continue;
        t32 += induced_edges(adj, adj[a] & adj[b]);
      }
    }

    // In a T31, the pendant vertex x and its unique triangle neighbour a are
    // distinguished.  The opposite triangle edge lies inside
    // N(a) minus (N(x) union {x}).
    std::uint64_t t31 = 0;
    for (int x = 0; x < ORDER; ++x) {
      Mask neighbours = adj[x];
      while (neighbours) {
        const int a = std::countr_zero(neighbours);
        neighbours &= neighbours - 1;
        const Mask opposite = adj[a] & ~adj[x] & ~(Mask{1} << x);
        t31 += induced_edges(adj, opposite);
      }
    }

    const std::int64_t r12 = -129 * static_cast<std::int64_t>(triangles)
                           + 6 * static_cast<std::int64_t>(t31)
                           + 16 * static_cast<std::int64_t>(t32);
    std::cout << index << ' ' << edges << ' ' << triangles << ' ' << t31
              << ' ' << t32 << ' ' << r12 << '\n';
    ++index;
  }
  std::cerr << "complete=1 records=" << index << '\n';
}
