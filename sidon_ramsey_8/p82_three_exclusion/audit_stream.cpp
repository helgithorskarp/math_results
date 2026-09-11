// Independent parsing and pair-sum audit of the compared nonempty query stream.
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
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
  uint64_t lo = word(), hi = word();
  return Mask(lo) | (Mask(hi) << 64);
}
std::vector<int> points(Mask a) {
  if (a >> 82)
    throw std::runtime_error("point range");
  std::vector<int> r;
  for (int i = 0; i < 82; ++i)
    if (a & (Mask(1) << i))
      r.push_back(i);
  return r;
}
int main(int argc, char **argv) {
  try {
    if (argc != 2)
      throw std::runtime_error("weights path");
    std::array<int, 82> w{};
    std::ifstream in(argv[1]);
    for (int &x : w)
      if (!(in >> x) || x < 0 || x > 1000000)
        throw std::runtime_error("weights");
    std::string extra;
    if (in >> extra)
      throw std::runtime_error("weight length");
    uint64_t records = 0, options = 0, max_options = 0;
    while (std::cin.peek() != std::char_traits<char>::eof()) {
      Mask domain = mask();
      auto d = points(domain);
      uint64_t k = word();
      if (k < 2 || k > 5)
        throw std::runtime_error("profile count");
      for (uint64_t i = 0; i < k; ++i)
        if (word() != (i + 1 == k ? 9 : 10))
          throw std::runtime_error("profile");
      if (d.size() != 10 * (k - 1) + 9)
        throw std::runtime_error("domain size");
      uint64_t upper = word(), count = word();
      if (upper > 4000000 || count == 0 || count > 17249580)
        throw std::runtime_error("query range");
      int total = 0;
      for (int x : d)
        total += w[size_t(x)];
      int lower = std::max(0, (total - 3776423 + int(k) - 2) / int(k - 1));
      Mask previous = 0;
      for (uint64_t j = 0; j < count; ++j) {
        Mask a = mask();
        auto p = points(a);
        if ((a & ~domain) || a <= previous || p.size() != 10)
          throw std::runtime_error("candidate mask");
        previous = a;
        int value = 0;
        for (int x : p)
          value += w[size_t(x)];
        if (value < lower || uint64_t(value) > upper)
          throw std::runtime_error("candidate weight");
        std::array<bool, 163> used{};
        for (size_t i = 0; i < p.size(); ++i)
          for (size_t l = i; l < p.size(); ++l) {
            size_t z = size_t(p[i] + p[l]);
            if (used[z])
              throw std::runtime_error("pair-sum collision");
            used[z] = true;
          }
      }
      ++records;
      options += count;
      max_options = std::max(max_options, count);
    }
    if (std::cin.bad())
      throw std::runtime_error("input");
    std::cout << "{\"verified\":true,\"bytes\":" << bytes
              << ",\"records\":" << records << ",\"options\":" << options
              << ",\"largest_option_list\":" << max_options << "}\n";
  } catch (const std::exception &e) {
    std::cerr << e.what() << '\n';
    return 1;
  }
}
