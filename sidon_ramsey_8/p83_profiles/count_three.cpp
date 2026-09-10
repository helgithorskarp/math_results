#include "common.hpp"
int main(int argc, char **argv) {
  try {
    if (argc != 5)
      throw std::runtime_error("method orbit weights output.csv");
    int method = integer(argv[1]);
    if (method < 0 || method > 1)
      throw std::runtime_error("method");
    Weights pw(argv[3]);
    std::ifstream in(argv[2]);
    std::ofstream out(argv[4]);
    if (!in || !out)
      throw std::runtime_error("IO");
    std::vector<U> m;
    std::vector<int> w;
    std::string line;
    while (std::getline(in, line)) {
      U a = readset(line);
      if (pop(a) != 11 || !sidon(a, method) || (a & ~universe))
        throw std::runtime_error("eleven");
      m.push_back(a);
      w.push_back(pw(a));
    }
    if (!in.eof() || m.size() != 15958 ||
        !std::is_sorted(w.begin(), w.end(), std::greater<>()))
      throw std::runtime_error("catalog");
    const int t = 31134774 - 5 * 4000000;
    size_t words = (m.size() + 63) / 64;
    std::vector<uint64_t> adj;
    auto start = std::chrono::steady_clock::now();
    if (method) {
      adj.resize(m.size() * words);
      for (size_t i = 0; i < m.size(); ++i)
        for (size_t j = i + 1; j < m.size(); ++j)
          if (!(m[i] & m[j]))
            adj[i * words + j / 64] |= uint64_t(1) << (j % 64);
    }
    uint64_t total = 0;
    size_t cases = 0, nonempty = 0;
    out << "orbit,weight,packings\n";
    for (size_t a = 0; a < m.size() && 3 * w[a] >= t; a += 2) {
      U reflected = 0;
      for (int x = 0; x < 83; ++x)
        if (m[a] & (U(1) << x))
          reflected |= U(1) << (82 - x);
      if (reflected != m[a + 1] || m[a] >= m[a + 1])
        throw std::runtime_error("orbit");
      uint64_t count = 0;
      std::vector<size_t> cand;
      for (size_t b = a + 1; b < m.size(); ++b)
        if (!(m[a] & m[b]))
          cand.push_back(b);
      for (size_t i = 0; i + 1 < cand.size(); ++i) {
        size_t b = cand[i];
        if (w[a] + 2 * w[b] < t)
          break;
        int need = t - w[a] - w[b];
        if (method) {
          size_t hi = size_t(
              std::upper_bound(w.begin(), w.end(), need, std::greater<>()) -
              w.begin());
          for (size_t k = b / 64; k < (hi + 63) / 64; ++k) {
            uint64_t bits = adj[a * words + k] & adj[b * words + k];
            if (k == hi / 64)
              bits &= (uint64_t(1) << (hi % 64)) - 1;
            count += uint64_t(__builtin_popcountll(bits));
          }
        } else
          for (size_t j = i + 1; j < cand.size(); ++j) {
            size_t c = cand[j];
            if (w[c] < need)
              break;
            if (!(m[b] & m[c]))
              ++count;
          }
      }
      ++cases;
      if (count)
        ++nonempty;
      total += count;
      out << a / 2 << ',' << w[a] << ',' << count << '\n';
      out.flush();
      if (!out)
        throw std::runtime_error("write");
    }
    std::cout << "{\"method\":" << method << ",\"cases\":" << cases
              << ",\"nonempty\":" << nonempty << ",\"packings\":" << total
              << ",\"complete\":true,\"seconds\":"
              << std::chrono::duration<double>(
                     std::chrono::steady_clock::now() - start)
                     .count()
              << "}\n";
    return 0;
  } catch (const std::exception &e) {
    std::cerr << e.what() << '\n';
    return 1;
  }
}
