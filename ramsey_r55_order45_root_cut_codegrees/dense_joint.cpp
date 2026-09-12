#include <algorithm>
#include <array>
#include <bit>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>

using Mask = std::uint32_t;
constexpr int MAX_N = 24;
struct Graph { int n; std::array<Mask, MAX_N> adj; };

static Graph decode(const std::string &line) {
  if (line.empty()) throw std::runtime_error("empty graph6 record");
  const int n = static_cast<unsigned char>(line[0]) - 63;
  const std::size_t bits = static_cast<std::size_t>(n) * (n - 1) / 2;
  if (n <= 0 || n > MAX_N || line.size() != 1 + (bits + 5) / 6)
    throw std::runtime_error("bad graph6 record");
  std::array<Mask, MAX_N> adj{};
  int pos = 0;
  for (int j = 1; j < n; ++j) for (int i = 0; i < j; ++i, ++pos) {
    const int x = static_cast<unsigned char>(line[1 + pos / 6]) - 63;
    if ((x >> (5 - pos % 6)) & 1) {
      adj[i] |= Mask{1} << j;
      adj[j] |= Mask{1} << i;
    }
  }
  return {n, adj};
}

static int class4(int edges, std::array<int, 4> degree) {
  std::sort(degree.begin(), degree.end());
  if (edges == 0) return 0;
  if (edges == 1) return 1;
  if (edges == 2 && degree == std::array<int,4>{1,1,1,1}) return 2;
  if (edges == 2) return 3;
  if (edges == 3 && degree == std::array<int,4>{0,2,2,2}) return 4;
  if (edges == 3 && degree == std::array<int,4>{1,1,1,3}) return 5;
  if (edges == 3) return 6;
  if (edges == 4 && degree == std::array<int,4>{2,2,2,2}) return 7;
  if (edges == 4) return 8;
  if (edges == 5) return 9;
  if (edges == 6) return 10;
  throw std::runtime_error("unclassified four-vertex graph");
}

int main(int argc, char **argv) {
  if (argc != 2) {
    std::cerr << "usage: dense_joint G6_FILE\n";
    return 2;
  }
  std::ifstream input(argv[1]);
  if (!input) throw std::runtime_error("cannot open input");
  std::string line;
  std::uint64_t source_index = 0, dense_index = 0;
  while (std::getline(input, line)) {
    if (line.empty()) continue;
    const auto g = decode(line);
    std::array<int, MAX_N> degree{};
    int degree_sum = 0;
    for (int v = 0; v < g.n; ++v) {
      degree[v] = std::popcount(g.adj[v]);
      degree_sum += degree[v];
    }
    const int edges = degree_sum / 2;
    if (edges < 126) { ++source_index; continue; }
    std::uint64_t triangles = 0, independent3 = 0;
    for (int a = 0; a < g.n; ++a) for (int b = a + 1; b < g.n; ++b)
      for (int c = b + 1; c < g.n; ++c) {
        const int e = ((g.adj[a] >> b) & 1U) + ((g.adj[a] >> c) & 1U)
                    + ((g.adj[b] >> c) & 1U);
        triangles += e == 3;
        independent3 += e == 0;
      }
    std::array<std::uint64_t, 11> patterns{};
    for (int a = 0; a < g.n; ++a) for (int b = a + 1; b < g.n; ++b)
      for (int c = b + 1; c < g.n; ++c) for (int d = c + 1; d < g.n; ++d) {
        const std::array<int,4> v{a,b,c,d};
        std::array<int,4> local_degree{};
        int e = 0;
        for (int i = 0; i < 4; ++i) for (int j = i + 1; j < 4; ++j)
          if ((g.adj[v[i]] >> v[j]) & 1U) {
            ++e; ++local_degree[i]; ++local_degree[j];
          }
        ++patterns[class4(e, local_degree)];
      }
    if (patterns[10]) throw std::runtime_error("dense tail contains K4");
    std::sort(degree.begin(), degree.begin() + g.n);
    std::cout << dense_index << ' ' << source_index << ' ' << edges << ' '
              << triangles << ' ' << independent3;
    for (int i = 0; i < 10; ++i) std::cout << ' ' << patterns[i];
    for (int v = 0; v < g.n; ++v) std::cout << ' ' << degree[v];
    std::cout << '\n';
    ++dense_index;
    ++source_index;
  }
  std::cerr << "columns=dense_index source_index e tri i3 i4 k2ii 2k2 p3i k3i k13 p4 c4 t31 t32 degrees[24]\n";
  std::cerr << "complete=1 source_records=" << source_index
            << " dense_records=" << dense_index << '\n';
}
