#include <array>
#include <bit>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <set>
#include <string_view>

namespace {

constexpr std::array<std::string_view, 58> kWords = {
    "00000000", "00000001", "00000110", "00000111", "00010100",
    "00011010", "00011011", "00011100", "00011101", "00101000",
    "00101110", "00101111", "00110000", "00110001",
    "01001110", "01001111", "01010000", "01010001", "01010100",
    "01010101", "01011000", "01011001", "01100010", "01100011",
    "01100100", "01100101", "01110110", "01110111", "01111001", "01111100",
    "01111101", "10000101", "10001010", "10001011", "10010010",
    "10010011", "10011000", "10011001", "10100010", "10100011",
    "10101100", "10101101", "10110101", "10111110", "10111111",
    "11000010", "11000011", "11001100", "11001101", "11011110",
    "11011111", "11100110", "11100111", "11101000",
    "11110000", "11110001", "11111010", "11111011",
};

constexpr unsigned Parse(std::string_view word) {
  unsigned value = 0;
  for (const char bit : word) value = 2 * value + static_cast<unsigned>(bit - '0');
  return value;
}

}  // namespace

int main() {
  std::array<bool, 256> in_code{};
  std::array<unsigned, 58> code{};
  for (std::size_t index = 0; index < kWords.size(); ++index) {
    code[index] = Parse(kWords[index]);
    assert(!in_code[code[index]]);
    in_code[code[index]] = true;
  }

  std::set<std::uint64_t> seen;
  std::array<unsigned, 9> signature_counts{};
  for (unsigned vertex = 0; vertex < 256; ++vertex) {
    if (in_code[vertex]) continue;
    std::uint64_t signature = 0;
    for (std::size_t index = 0; index < code.size(); ++index) {
      if (std::popcount(vertex ^ code[index]) <= 1) {
        signature |= std::uint64_t{1} << index;
      }
    }
    assert(signature != 0);
    assert(seen.insert(signature).second);
    ++signature_counts[std::popcount(signature)];
  }
  assert(seen.size() == 198);
  assert(signature_counts[1] == 56);
  assert(signature_counts[2] == 102);
  assert(signature_counts[3] == 24);
  assert(signature_counts[4] == 16);

  std::array<unsigned, 9> distance_counts{};
  for (std::size_t first = 0; first < code.size(); ++first) {
    for (std::size_t second = first + 1; second < code.size(); ++second) {
      ++distance_counts[std::popcount(code[first] ^ code[second])];
    }
  }
  assert(distance_counts[1] == 34);
  assert(distance_counts[2] == 144);
  assert(distance_counts[3] == 428);
  assert(distance_counts[4] == 470);
  assert(distance_counts[5] == 305);
  assert(distance_counts[6] == 198);
  assert(distance_counts[7] == 74);

  std::cout << "verified: 58-word locating-dominating code in Q_8\n"
            << "non-codewords: 198; distinct nonempty signatures: 198\n"
            << "signature sizes: 1:56 2:102 3:24 4:16\n"
            << "pair distances: 1:34 2:144 3:428 4:470 5:305 6:198 7:74\n";
}
