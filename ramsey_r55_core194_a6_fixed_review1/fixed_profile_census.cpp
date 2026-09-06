#include <array>
#include <cstdint>
#include <iostream>
#include <map>
#include <set>

using Profile = std::array<int, 3>;
using Permutation = std::array<int, 8>;

int main() {
  constexpr std::uint64_t total = 6561;  // 3^8 fixed contact words.
  std::map<Profile, std::uint64_t> profiles;
  std::set<Permutation> sorting_permutations;
  std::uint64_t allowed = 0;

  for (std::uint64_t code = 0; code < total; ++code) {
    std::uint64_t value = code;
    std::array<int, 8> word{};
    Profile counts{};
    for (int position = 0; position < 8; ++position) {
      word[position] = static_cast<int>(value % 3);
      value /= 3;
      ++counts[word[position]];
    }

    // Moving contacts are six RR triangles and one BR triangle.
    const int red_u = 18 + counts[0] + counts[1];
    const int red_v = 21 + counts[0] + counts[2];
    if (red_u < 18 || red_u > 24 || red_v < 18 || red_v > 24) continue;

    ++allowed;
    ++profiles[counts];
    Permutation sorted_positions{};
    std::array<int, 3> next{0, counts[0], counts[0] + counts[1]};
    for (int old_position = 0; old_position < 8; ++old_position) {
      sorted_positions[old_position] = next[word[old_position]]++;
    }
    sorting_permutations.insert(sorted_positions);
  }

  std::cout << "total " << total << '\n';
  std::cout << "allowed " << allowed << '\n';
  std::cout << "profiles " << profiles.size() << '\n';
  std::cout << "sorting_permutations " << sorting_permutations.size() << '\n';
  for (const auto &[profile, weight] : profiles) {
    const auto [x, y, z] = profile;
    std::cout << "row " << x << ' ' << y << ' ' << z << ' ' << weight << ' '
              << 18 + x + y << ' ' << 21 + x + z << '\n';
  }
}
