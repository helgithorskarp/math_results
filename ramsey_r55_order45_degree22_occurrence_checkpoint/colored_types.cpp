#include <algorithm>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <stdexcept>
#include <vector>

using Mask = std::uint32_t;

static int bit_index(int i, int j) {
  if (i > j) std::swap(i, j);
  return j * (j - 1) / 2 + i;
}

static bool adjacent(Mask mask, int i, int j) {
  return (mask >> bit_index(i, j)) & 1U;
}

static bool valid(Mask mask, int n, int a) {
  // H contains no K4.
  for (int i = 0; i < a; ++i) for (int j = i + 1; j < a; ++j)
    for (int k = j + 1; k < a; ++k) for (int l = k + 1; l < a; ++l)
      if (adjacent(mask,i,j) && adjacent(mask,i,k) && adjacent(mask,i,l)
          && adjacent(mask,j,k) && adjacent(mask,j,l) && adjacent(mask,k,l))
        return false;
  // X contains no independent four-set.
  for (int i = a; i < n; ++i) for (int j = i + 1; j < n; ++j)
    for (int k = j + 1; k < n; ++k) for (int l = k + 1; l < n; ++l)
      if (!adjacent(mask,i,j) && !adjacent(mask,i,k) && !adjacent(mask,i,l)
          && !adjacent(mask,j,k) && !adjacent(mask,j,l) && !adjacent(mask,k,l))
        return false;
  // The colored graph itself contains neither K5 nor I5.
  for (int i = 0; i < n; ++i) for (int j = i + 1; j < n; ++j)
    for (int k = j + 1; k < n; ++k) for (int l = k + 1; l < n; ++l)
      for (int m = l + 1; m < n; ++m) {
        const int e = adjacent(mask,i,j)+adjacent(mask,i,k)+adjacent(mask,i,l)+adjacent(mask,i,m)
                    + adjacent(mask,j,k)+adjacent(mask,j,l)+adjacent(mask,j,m)
                    + adjacent(mask,k,l)+adjacent(mask,k,m)+adjacent(mask,l,m);
        if (e == 0 || e == 10) return false;
      }
  return true;
}

static void make_permutations(int a, int b, std::vector<std::vector<int>> &out) {
  std::vector<int> hp(a), xp(b);
  std::iota(hp.begin(), hp.end(), 0);
  do {
    std::iota(xp.begin(), xp.end(), a);
    do {
      std::vector<int> p = hp;
      p.insert(p.end(), xp.begin(), xp.end());
      out.push_back(std::move(p));
    } while (std::next_permutation(xp.begin(), xp.end()));
  } while (std::next_permutation(hp.begin(), hp.end()));
}

static Mask image(Mask mask, int n, const std::vector<int> &p) {
  Mask out = 0;
  for (int j = 1; j < n; ++j) for (int i = 0; i < j; ++i)
    if (adjacent(mask, p[i], p[j])) out |= Mask{1} << bit_index(i, j);
  return out;
}

int main(int argc, char **argv) {
  int maximum = 7;
  if (argc == 2) maximum = std::stoi(argv[1]);
  if (argc > 2 || maximum < 1 || maximum > 7) {
    std::cerr << "usage: colored_types [MAX_ORDER<=7]\n";
    return 2;
  }
  for (int n = 1; n <= maximum; ++n) for (int a = 0; a <= n; ++a) {
    const int bits = n * (n - 1) / 2;
    const std::uint64_t total = std::uint64_t{1} << bits;
    std::vector<bool> seen(total, false);
    std::vector<std::vector<int>> group;
    make_permutations(a, n-a, group);
    std::uint64_t retained = 0;
    for (std::uint64_t raw = 0; raw < total; ++raw) {
      if (seen[raw]) continue;
      Mask representative = static_cast<Mask>(raw);
      for (const auto &p : group) {
        const Mask transformed = image(static_cast<Mask>(raw), n, p);
        seen[transformed] = true;
        representative = std::min(representative, transformed);
      }
      if (valid(representative, n, a)) {
        std::cout << n << ' ' << a << ' ' << representative << '\n';
        ++retained;
      }
    }
    std::cerr << "n=" << n << " a=" << a << " retained=" << retained << '\n';
  }
}
