// Verify a Boolean obstruction by recursive evaluation of circuit ports.
// The generator instead edits a sequential word and evaluates all 8192 inputs.
#include <algorithm>
#include <array>
#include <bit>
#include <cstdint>
#include <fstream>
#include <functional>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>
using Gate = std::pair<int, int>;
using Net = std::vector<Gate>;
using Truth = std::vector<std::uint64_t>;
constexpr int channels = 13;

class Circuit {
  const Net& net;
  std::size_t words;
  std::vector<Truth> ports;
  std::vector<Gate> parents;
  std::vector<int> visited;
  std::array<int, channels> outputs{};

  void evaluate(int port) {
    if (port < channels) return;
    const int j = (port - channels) / 2;
    auto k = static_cast<std::size_t>(j);
    if (visited[k] == 2) return;
    if (visited[k] == 1 || parents[k].first < 0)
      throw std::runtime_error("cycle or deleted port reached");
    visited[k] = 1;
    auto [left, right] = parents[k];
    evaluate(left);
    evaluate(right);
    const auto& a = ports[static_cast<std::size_t>(left)];
    const auto& b = ports[static_cast<std::size_t>(right)];
    auto& lo = ports[static_cast<std::size_t>(channels + 2*j)];
    auto& hi = ports[static_cast<std::size_t>(channels + 2*j + 1)];
    for (std::size_t w = 0; w < words; ++w) {
      lo[w] = a[w] & b[w];
      hi[w] = a[w] | b[w];
    }
    visited[k] = 2;
  }

 public:
  Circuit(const Net& input, const std::vector<unsigned>& witnesses)
      : net(input), words((witnesses.size()+63)/64),
        ports(static_cast<std::size_t>(channels)+2*net.size(), Truth(words)),
        parents(net.size(), {-1,-1}), visited(net.size()) {
    for (std::size_t x = 0; x < witnesses.size(); ++x)
      for (int wire = 0; wire < channels; ++wire)
        if ((witnesses[x] >> wire) & 1U)
          ports[static_cast<std::size_t>(wire)][x/64] |=
              std::uint64_t{1} << (x%64);
  }

  int failed(int remove_a, int remove_b) {
    for (int i = 0; i < channels; ++i) outputs[static_cast<std::size_t>(i)] = i;
    std::fill(visited.begin(), visited.end(), 0);
    std::fill(parents.begin(), parents.end(), Gate{-1,-1});
    for (std::size_t j = 0; j < net.size(); ++j) {
      if (static_cast<int>(j) == remove_a || static_cast<int>(j) == remove_b)
        continue;
      auto [a,b] = net[j];
      parents[j] = {outputs[static_cast<std::size_t>(a)],
                    outputs[static_cast<std::size_t>(b)]};
      if (parents[j].first >= channels+2*static_cast<int>(j) ||
          parents[j].second >= channels+2*static_cast<int>(j))
        throw std::runtime_error("invalid port ordering");
      outputs[static_cast<std::size_t>(a)] = channels+2*static_cast<int>(j);
      outputs[static_cast<std::size_t>(b)] = channels+2*static_cast<int>(j)+1;
    }
    for (int port : outputs) evaluate(port);
    int failed_inputs = 0;
    for (std::size_t w = 0; w < words; ++w) {
      std::uint64_t inversion = 0;
      for (int i = 0; i < channels-1; ++i)
        inversion |= ports[static_cast<std::size_t>(outputs[static_cast<std::size_t>(i)])][w] &
            ~ports[static_cast<std::size_t>(outputs[static_cast<std::size_t>(i+1)])][w];
      failed_inputs += std::popcount(inversion);
    }
    return failed_inputs;
  }
};

int main(int argc, char** argv) {
  try {
    if (argc != 4)
      throw std::runtime_error("usage: check_circuit SEEDS WITNESSES FULL_0_OR_1");
    std::string mode = argv[3];
    if (mode != "0" && mode != "1") throw std::runtime_error("bad full flag");
    std::ifstream wfile(argv[2]);
    std::size_t wcount = 0;
    if (!(wfile >> wcount) || wcount == 0 || wcount > 8192)
      throw std::runtime_error("bad witness count");
    std::vector<unsigned> witnesses;
    std::array<bool,8192> seen{};
    for (std::size_t j = 0; j < wcount; ++j) {
      unsigned x = 8192;
      if (!(wfile >> x) || x >= 8192 || seen[x])
        throw std::runtime_error("bad or duplicate witness");
      witnesses.push_back(x);
      seen[x] = true;
    }
    std::string extra;
    if (wfile >> extra) throw std::runtime_error("trailing witness data");
    if (mode == "1") {
      witnesses.clear();
      for (unsigned x = 0; x < 8192; ++x) witnesses.push_back(x);
    }
    std::ifstream file(argv[1]);
    std::size_t seeds = 0;
    if (!(file >> seeds) || seeds == 0) throw std::runtime_error("missing seeds");
    std::uint64_t checked44 = 0, checked45 = 0;
    int minimum44 = std::numeric_limits<int>::max();
    bool control = false;
    for (std::size_t r = 0; r < seeds; ++r) {
      int n = 0, m = 0;
      if (!(file >> n >> m) || n != channels || (m != 45 && m != 46))
        throw std::runtime_error("bad seed dimensions");
      Net net;
      for (int j = 0; j < m; ++j) {
        int a = 0, b = 0;
        if (!(file >> a >> b) || a < 0 || a >= b || b >= channels)
          throw std::runtime_error("bad comparator");
        net.emplace_back(a,b);
      }
      Circuit circuit(net, witnesses);
      if (circuit.failed(-1,-1)) throw std::runtime_error("seed fails witness");
      if (m == 45) {
        // A redundant extra comparator gives a planted positive deletion case.
        Net augmented = net;
        augmented.emplace_back(0,1);
        Circuit planted(augmented, witnesses);
        if (planted.failed(45,-1) != 0)
          throw std::runtime_error("planted positive deletion was missed");
        control = true;
      }
      if (m == 46) {
        for (int a = 0; a < m; ++a) {
          if (circuit.failed(a,-1) == 0)
            throw std::runtime_error("certificate fails to exclude a size45 deletion");
          ++checked45;
        }
      }
      for (int a = 0; a < m; ++a) {
        const int stop = m == 45 ? 0 : m;
        for (int b = m == 45 ? -1 : a+1; b < stop; ++b) {
          int failures = circuit.failed(a,b);
          if (failures == 0)
            throw std::runtime_error("certificate fails to exclude a size44 deletion");
          minimum44 = std::min(minimum44, failures);
          ++checked44;
        }
      }
    }
    if (file >> extra) throw std::runtime_error("trailing seed data");
    if (!control) throw std::runtime_error("missing positive control");
    std::cout << "ALL_DELETIONS_EXCLUDED seeds=" << seeds
              << " size44=" << checked44 << " size45=" << checked45
              << " witnesses=" << witnesses.size()
              << " minimum44_failures=" << minimum44
              << " positive_control=PASS\n";
  } catch (const std::exception& e) {
    std::cerr << "ERROR: " << e.what() << '\n';
    return 2;
  }
}
