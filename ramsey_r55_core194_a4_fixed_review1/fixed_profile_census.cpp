#include <algorithm>
#include <array>
#include <iostream>
#include <map>
#include <set>
#include <tuple>
#include <vector>

struct Row {
  long words = 0;
  int red_u = 0;
  int red_v = 0;
};

int main() {
  std::map<std::tuple<int, int, int>, Row> rows;
  std::set<std::array<int, 8>> sorting_permutations;
  long allowed = 0;

  for (int encoded = 0; encoded < 6561; ++encoded) {
    int value = encoded;
    std::array<int, 8> word{};
    std::array<int, 3> count{};
    for (int i = 0; i < 8; ++i) {
      word[i] = value % 3;
      value /= 3;
      ++count[word[i]];
    }
    const int x = count[0];
    const int y = count[1];
    const int z = count[2];
    const int red_u = 15 + x + y;
    const int red_v = 18 + x + z;
    if (red_u < 18 || red_u > 24 || red_v < 18 || red_v > 24) continue;
    ++allowed;

    std::vector<int> order{0, 1, 2, 3, 4, 5, 6, 7};
    std::stable_sort(order.begin(), order.end(),
                     [&](int i, int j) { return word[i] < word[j]; });
    std::array<int, 8> permutation{};
    for (int destination = 0; destination < 8; ++destination) {
      permutation[order[destination]] = destination;
    }
    sorting_permutations.insert(permutation);

    auto &row = rows[{x, y, z}];
    ++row.words;
    row.red_u = red_u;
    row.red_v = red_v;
  }

  std::cout << "summary total 6561 allowed " << allowed
            << " profiles " << rows.size()
            << " permutations " << sorting_permutations.size()
            << " labeled " << 210 * allowed << '\n';
  for (const auto &[counts, row] : rows) {
    const auto [x, y, z] = counts;
    std::cout << "row " << x << ' ' << y << ' ' << z << ' ' << row.words
              << ' ' << row.red_u << ' ' << row.red_v << ' '
              << 210 * row.words << '\n';
  }
  return 0;
}
