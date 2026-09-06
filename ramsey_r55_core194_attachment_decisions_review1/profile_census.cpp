#include <array>
#include <cstdint>
#include <iostream>
#include <map>

using Profile = std::array<int, 6>;

int main() {
  constexpr std::uint64_t total = 14348907;  // 3^15
  std::map<Profile, std::uint64_t> profiles;
  std::uint64_t allowed = 0;
  for (std::uint64_t code = 0; code < total; ++code) {
    std::uint64_t value = code;
    Profile counts{};
    for (int position = 0; position < 15; ++position) {
      const int contact = static_cast<int>(value % 3);
      value /= 3;
      ++counts[position < 7 ? contact : 3 + contact];
    }
    const int red_u = 3 * (counts[0] + counts[1]) + counts[3] + counts[4];
    const int red_v = 3 * (counts[0] + counts[2]) + counts[3] + counts[5];
    if (red_u < 18 || red_u > 24 || red_v < 18 || red_v > 24) continue;
    ++allowed;
    const Profile swapped{counts[0], counts[2], counts[1], counts[3], counts[5], counts[4]};
    ++profiles[std::min(counts, swapped)];
  }
  std::cout << "total " << total << '\n';
  std::cout << "allowed " << allowed << '\n';
  std::cout << "profiles " << profiles.size() << '\n';
  for (const auto &[profile, weight] : profiles) {
    std::cout << "row";
    for (const int count : profile) std::cout << ' ' << count;
    std::cout << ' ' << weight << '\n';
  }
}
