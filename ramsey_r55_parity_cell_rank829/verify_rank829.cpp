#include <array>
#include <bit>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <vector>

namespace {

constexpr int V = 42;
constexpr int LENGTH = V * (V - 1) / 2;
constexpr int RANK = 829;
constexpr int DIMENSION = LENGTH - RANK;
constexpr int WORDS = (LENGTH + 63) / 64;
constexpr uint64_t SEED = 400517;
constexpr uint64_t NONROOT_MASK = ((UINT64_C(1) << 43) - 1) ^ 1;
using Word = std::array<uint64_t, WORDS>;

uint64_t next_splitmix(uint64_t &state) {
  state += UINT64_C(0x9e3779b97f4a7c15);
  uint64_t value = state;
  value = (value ^ (value >> 30)) * UINT64_C(0xbf58476d1ce4e5b9);
  value = (value ^ (value >> 27)) * UINT64_C(0x94d049bb133111eb);
  return value ^ (value >> 31);
}

bool bit(const Word &word, int position) {
  return (word[position >> 6] >> (position & 63)) & 1;
}

void flip(Word &word, int position) {
  word[position >> 6] ^= UINT64_C(1) << (position & 63);
}

void xor_into(Word &left, const Word &right) {
  for (int i = 0; i < WORDS; ++i) left[i] ^= right[i];
}

int dot(const Word &left, const Word &right) {
  int parity = 0;
  for (int i = 0; i < WORDS; ++i)
    parity ^= std::popcount(left[i] & right[i]) & 1;
  return parity;
}

std::vector<Word> parity_checks() {
  uint64_t state = SEED;
  std::vector<Word> checks(RANK);
  for (Word &check : checks)
    for (int position = 0; position < LENGTH; ++position)
      if (next_splitmix(state) & 1) flip(check, position);
  return checks;
}

std::vector<Word> kernel_basis(const std::vector<Word> &input) {
  std::vector<Word> rows = input;
  std::vector<int> pivots;
  int used = 0;
  for (int position = 0; position < LENGTH && used < RANK; ++position) {
    int selected = used;
    while (selected < RANK && !bit(rows[selected], position)) ++selected;
    if (selected == RANK) continue;
    std::swap(rows[used], rows[selected]);
    for (int other = 0; other < RANK; ++other)
      if (other != used && bit(rows[other], position))
        xor_into(rows[other], rows[used]);
    pivots.push_back(position);
    ++used;
  }
  if (used != RANK) throw std::runtime_error("check matrix has wrong rank");

  std::array<bool, LENGTH> pivot{};
  for (int position : pivots) pivot[position] = true;
  std::vector<Word> basis;
  for (int free = 0; free < LENGTH; ++free) {
    if (pivot[free]) continue;
    Word vector{};
    flip(vector, free);
    for (int row = 0; row < RANK; ++row)
      if (bit(rows[row], free)) flip(vector, pivots[row]);
    basis.push_back(vector);
  }
  if (basis.size() != DIMENSION)
    throw std::runtime_error("kernel has wrong dimension");
  for (const Word &vector : basis)
    for (const Word &check : input)
      if (dot(vector, check)) throw std::runtime_error("false kernel vector");
  return basis;
}

std::vector<std::pair<int, int>> edge_order() {
  std::vector<std::pair<int, int>> edges;
  for (int a = 1; a <= V; ++a)
    for (int b = a + 1; b <= V; ++b) edges.emplace_back(a, b);
  if (edges.size() != LENGTH) throw std::runtime_error("edge order failure");
  return edges;
}

bool extend_clique(const std::array<uint64_t, 43> &adjacency,
                   uint64_t candidates, int still_needed) {
  if (still_needed == 0) return true;
  while (std::popcount(candidates) >= still_needed) {
    const int vertex = std::countr_zero(candidates);
    if (vertex >= 43) throw std::runtime_error("candidate mask out of range");
    candidates &= candidates - 1;
    if (extend_clique(adjacency, candidates & adjacency[vertex],
                      still_needed - 1)) return true;
  }
  return false;
}

bool has_five_clique(const std::array<uint64_t, 43> &adjacency) {
  return extend_clique(adjacency, NONROOT_MASK, 5);
}

}  // namespace

int main() {
  try {
    const std::vector<Word> checks = parity_checks();
    const std::vector<Word> basis = kernel_basis(checks);
    const std::vector<std::pair<int, int>> edges = edge_order();
    std::array<std::array<uint64_t, 43>, DIMENSION> toggles{};
    for (int coordinate = 0; coordinate < DIMENSION; ++coordinate)
      for (int position = 0; position < LENGTH; ++position)
        if (bit(basis[coordinate], position)) {
          const auto [a, b] = edges[position];
          toggles[coordinate][a] ^= UINT64_C(1) << b;
          toggles[coordinate][b] ^= UINT64_C(1) << a;
        }

    std::array<uint64_t, 43> red{};
    uint64_t coordinates = 0;
    uint64_t red_free = 0;
    constexpr uint64_t TOTAL = UINT64_C(1) << DIMENSION;
    for (uint64_t index = 0; index < TOTAL; ++index) {
      if (index) {
        const int changed = std::countr_zero(index);
        coordinates ^= UINT64_C(1) << changed;
        for (int vertex = 1; vertex <= V; ++vertex)
          red[vertex] ^= toggles[changed][vertex];
      }
      if (coordinates != (index ^ (index >> 1)))
        throw std::runtime_error("Gray traversal failure");
      const bool contains = has_five_clique(red);
      if (!contains) {
        ++red_free;
        if (index != 0)
          throw std::runtime_error("nonzero K5-free kernel word found");
      }
    }
    if (red_free != 1) throw std::runtime_error("zero-word count failure");

    // The unique red-K5-free word is zero, so vertices 1,...,5 form a blue K5.
    const std::array<uint64_t, 43> zero_red{};
    for (int a = 1; a <= 5; ++a)
      for (int b = a + 1; b <= 5; ++b)
        if ((zero_red[a] >> b) & 1)
          throw std::runtime_error("purported zero-word blue K5 is not blue");

    std::cout << "VERIFIED_EXHAUSTIVE_RANK829_CODE_THEOREM"
              << " length=" << LENGTH << " rank=" << RANK
              << " dimension=" << DIMENSION << " seed=" << SEED
              << " assignments=" << TOTAL
              << " nonzero_red_K5=" << TOTAL - 1
              << " zero_blue_K5=1\n";
    return 0;
  } catch (const std::exception &error) {
    std::cerr << "ERROR " << error.what() << "\n";
    return 2;
  }
}
