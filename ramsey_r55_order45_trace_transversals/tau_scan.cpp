#include <algorithm>
#include <array>
#include <bit>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <iomanip>
#include <stdexcept>
#include <string>
#include <unordered_set>
#include <vector>

// Exact minimum hitting sets of the independent 4-sets of (4,5,24)-graphs.
// A hitting set is precisely an exterior adjacency trace whose complement has
// independence number at most three.  All bit masks use the low 24 bits.

using Mask = std::uint32_t;

static std::array<Mask, 24> decode_g6(const std::string &line) {
  if (line.empty()) throw std::runtime_error("empty graph6 line");
  const int n = static_cast<unsigned char>(line[0]) - 63;
  if (n != 24) throw std::runtime_error("expected graph6 order 24");
  if (line.size() != 47) throw std::runtime_error("malformed order-24 graph6 record");
  std::array<Mask, 24> adj{};
  int pos = 0;
  for (int j = 1; j < n; ++j) {
    for (int i = 0; i < j; ++i, ++pos) {
      const int word = pos / 6;
      const int shift = pos % 6;
      const int val = static_cast<unsigned char>(line[1 + word]) - 63;
      if ((val >> (5 - shift)) & 1) {
        adj[i] |= Mask{1} << j;
        adj[j] |= Mask{1} << i;
      }
    }
  }
  return adj;
}

static bool has_clique(const std::array<Mask, 24> &adj, Mask cand, int k) {
  if (k == 0) return true;
  while (cand) {
    const int v = std::countr_zero(cand);
    cand &= cand - 1;
    if (std::popcount(cand & adj[v]) >= k - 1 &&
        has_clique(adj, cand & adj[v], k - 1)) return true;
  }
  return false;
}

static bool is_45_graph(const std::array<Mask, 24> &adj) {
  constexpr Mask full = (Mask{1} << 24) - 1;
  if (has_clique(adj, full, 4)) return false;
  std::array<Mask, 24> comp{};
  for (int v = 0; v < 24; ++v)
    comp[v] = full & ~adj[v] & ~(Mask{1} << v);
  return !has_clique(comp, full, 5);
}

static int edges(const std::array<Mask, 24> &adj) {
  int sum = 0;
  for (Mask a : adj) sum += std::popcount(a);
  return sum / 2;
}

static std::vector<Mask> independent_fours(const std::array<Mask, 24> &adj) {
  std::vector<Mask> out;
  for (int a = 0; a < 24; ++a)
    for (int b = a + 1; b < 24; ++b) {
      if ((adj[a] >> b) & 1U) continue;
      for (int c = b + 1; c < 24; ++c) {
        const Mask abc = (Mask{1} << a) | (Mask{1} << b) | (Mask{1} << c);
        if ((adj[c] & abc) || (adj[b] & (Mask{1} << c))) continue;
        for (int d = c + 1; d < 24; ++d) {
          if (adj[d] & abc) continue;
          out.push_back(abc | (Mask{1} << d));
        }
      }
    }
  return out;
}

class HittingSearch {
 public:
  explicit HittingSearch(const std::vector<Mask> &all) : all_(all) {}

  bool at_most(int k) {
    failed_.clear();
    nodes_ = 0;
    witness_ = 0;
    return recurse(Mask{0}, k);
  }
  std::uint64_t nodes() const { return nodes_; }
  Mask witness() const { return witness_; }

 private:
  const std::vector<Mask> &all_;
  std::unordered_set<Mask> failed_;
  std::uint64_t nodes_ = 0;
  Mask witness_ = 0;

  bool recurse(Mask chosen, int left) {
    ++nodes_;
    std::vector<Mask> remaining;
    remaining.reserve(all_.size());
    for (Mask e : all_) if ((e & chosen) == 0) remaining.push_back(e);
    if (remaining.empty()) {
      witness_ = chosen;
      return true;
    }
    if (left == 0) return false;
    if (failed_.contains(chosen)) return false;

    // A greedy disjoint packing is a valid lower bound on the number of
    // additional hitting vertices.  Repeat in two deterministic orders.
    auto packing_too_large = [&](bool reverse) {
      Mask used = 0;
      int count = 0;
      if (!reverse) {
        for (Mask e : remaining) if ((e & used) == 0) {
          used |= e;
          if (++count > left) return true;
        }
      } else {
        for (auto it = remaining.rbegin(); it != remaining.rend(); ++it)
          if ((*it & used) == 0) {
            used |= *it;
            if (++count > left) return true;
          }
      }
      return false;
    };
    if (packing_too_large(false) || packing_too_large(true)) {
      failed_.insert(chosen);
      return false;
    }

    std::array<int, 24> freq{};
    for (Mask e : remaining)
      for (int v = 0; v < 24; ++v) if ((e >> v) & 1U) ++freq[v];

    // Branch on the uncovered edge with the largest least-useful vertex;
    // this avoids a branch containing a very low-incidence escape vertex.
    Mask pivot = remaining.front();
    int best = -1;
    for (Mask e : remaining) {
      int score = 1000000000;
      for (int v = 0; v < 24; ++v) if ((e >> v) & 1U)
        score = std::min(score, freq[v]);
      if (score > best) { best = score; pivot = e; }
    }
    std::array<int, 4> branch{};
    int z = 0;
    for (int v = 0; v < 24; ++v) if ((pivot >> v) & 1U) branch[z++] = v;
    std::sort(branch.begin(), branch.end(), [&](int a, int b) {
      if (freq[a] != freq[b]) return freq[a] > freq[b];
      return a < b;
    });
    for (int v : branch)
      if (recurse(chosen | (Mask{1} << v), left - 1)) return true;
    failed_.insert(chosen);
    return false;
  }
};

int main(int argc, char **argv) {
  if (argc < 2 || argc > 4) {
    std::cerr << "usage: tau_scan CATALOGUE [START_DENSE_INDEX [END_DENSE_INDEX]]\n";
    return 2;
  }
  const std::uint64_t start = argc >= 3 ? std::stoull(argv[2]) : 0;
  const std::uint64_t end = argc >= 4 ? std::stoull(argv[3]) : UINT64_MAX;
  std::ifstream in(argv[1]);
  if (!in) throw std::runtime_error("cannot open catalogue");
  const auto began = std::chrono::steady_clock::now();
  std::string line;
  std::uint64_t dense = 0, emitted = 0, total_nodes = 0;
  while (std::getline(in, line)) {
    auto adj = decode_g6(line);
    const int e = edges(adj);
    if (e < 126) continue;
    if (!is_45_graph(adj)) throw std::runtime_error("tail record is not a (4,5)-graph");
    if (dense >= end) break;
    if (dense++ < start) continue;
    auto fours = independent_fours(adj);
    HittingSearch search(fours);
    int tau = 0;
    for (; tau <= 20 && !search.at_most(tau); ++tau) total_nodes += search.nodes();
    total_nodes += search.nodes();
    if (tau > 20) throw std::runtime_error("unexpected transversal number > 20");
    std::cout << (dense - 1) << ' ' << e << ' ' << fours.size() << ' ' << tau
              << ' ' << std::hex << std::setw(6) << std::setfill('0')
              << search.witness() << std::dec << std::setfill(' ') << '\n';
    ++emitted;
  }
  if (dense < end && end != UINT64_MAX)
    throw std::runtime_error("requested range exceeds dense tail");
  const double seconds = std::chrono::duration<double>(
      std::chrono::steady_clock::now() - began).count();
  std::cerr << "complete=1 start=" << start << " end=" << dense
            << " emitted=" << emitted << " search_nodes=" << total_nodes
            << " seconds=" << seconds << '\n';
  return 0;
}
