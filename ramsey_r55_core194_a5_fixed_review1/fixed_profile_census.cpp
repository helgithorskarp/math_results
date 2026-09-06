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
  const std::array<std::array<int, 3>, 2> types{{{{5, 0, 2}}, {{5, 1, 1}}}};
  long grand_labeled = 0;
  int grand_profiles = 0;

  for (const auto &moving : types) {
    std::map<std::tuple<int, int, int>, Row> rows;
    std::set<std::array<int, 9>> normalizers;
    long allowed = 0;
    long swaps = 0;

    for (int encoded = 0; encoded < 6561; ++encoded) {
      int value = encoded;
      std::array<int, 8> word{};
      std::array<int, 3> count{};
      for (int i = 0; i < 8; ++i) {
        word[i] = value % 3;
        value /= 3;
        ++count[word[i]];
      }

      const int red_u = 3 * (moving[0] + moving[1]) + count[0] + count[1];
      const int red_v = 3 * (moving[0] + moving[2]) + count[0] + count[2];
      if (red_u < 18 || red_u > 24 || red_v < 18 || red_v > 24) continue;
      ++allowed;

      bool swapped = moving[1] == moving[2] && count[1] > count[2];
      if (swapped) {
        ++swaps;
        for (int &contact : word) {
          if (contact != 0) contact = 3 - contact;
        }
        std::swap(count[1], count[2]);
      }

      std::vector<int> order{0, 1, 2, 3, 4, 5, 6, 7};
      std::stable_sort(order.begin(), order.end(),
                       [&](int i, int j) { return word[i] < word[j]; });
      std::array<int, 9> signature{};
      signature[0] = swapped ? 1 : 0;
      for (int destination = 0; destination < 8; ++destination) {
        signature[1 + order[destination]] = destination;
      }
      normalizers.insert(signature);

      const int canonical_u = 3 * (moving[0] + moving[1]) + count[0] + count[1];
      const int canonical_v = 3 * (moving[0] + moving[2]) + count[0] + count[2];
      auto &row = rows[{count[0], count[1], count[2]}];
      ++row.words;
      row.red_u = canonical_u;
      row.red_v = canonical_v;
    }

    const long labeled = 42 * allowed;
    std::cout << "type " << moving[0] << ' ' << moving[1] << ' ' << moving[2]
              << " total 6561 allowed " << allowed << " profiles " << rows.size()
              << " swaps " << swaps << " permutations " << normalizers.size()
              << " labeled " << labeled << '\n';
    for (const auto &[fixed, row] : rows) {
      const auto [x, y, z] = fixed;
      std::cout << "row " << moving[0] << ' ' << moving[1] << ' ' << moving[2]
                << ' ' << x << ' ' << y << ' ' << z << ' ' << row.words
                << ' ' << row.red_u << ' ' << row.red_v << ' ' << 42 * row.words
                << '\n';
    }
    grand_profiles += static_cast<int>(rows.size());
    grand_labeled += labeled;
  }

  std::cout << "grand profiles " << grand_profiles << " labeled " << grand_labeled << '\n';
  return 0;
}
