#include <algorithm>
#include <array>
#include <bit>
#include <cstdint>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

namespace {

constexpr int N = 43;
constexpr int FREE_EDGES = 861;
constexpr int WORDS = (FREE_EDGES + 63) / 64;
constexpr int PARITY_RANK = 829;
constexpr uint64_t SEED = 400517;
constexpr uint64_t VERTEX_MASK = (UINT64_C(1) << N) - 1;

using Row = std::array<uint64_t, WORDS>;

uint64_t splitmix64(uint64_t &state) {
  uint64_t z = (state += UINT64_C(0x9e3779b97f4a7c15));
  z = (z ^ (z >> 30)) * UINT64_C(0xbf58476d1ce4e5b9);
  z = (z ^ (z >> 27)) * UINT64_C(0x94d049bb133111eb);
  return z ^ (z >> 31);
}

bool get_bit(const Row &row, int column) {
  return (row[column / 64] >> (column % 64)) & UINT64_C(1);
}

void toggle_bit(Row &row, int column) {
  row[column / 64] ^= UINT64_C(1) << (column % 64);
}

std::vector<Row> make_rows() {
  uint64_t state = SEED;
  std::vector<Row> rows(PARITY_RANK);
  for (Row &row : rows)
    for (int column = 0; column < FREE_EDGES; ++column)
      if (splitmix64(state) & 1) toggle_bit(row, column);
  return rows;
}

std::vector<int> reduce(std::vector<Row> &rows) {
  int rank = 0;
  std::vector<int> pivots;
  for (int column = 0; column < FREE_EDGES && rank < PARITY_RANK; ++column) {
    int pivot = rank;
    while (pivot < PARITY_RANK && !get_bit(rows[pivot], column)) ++pivot;
    if (pivot == PARITY_RANK) continue;
    std::swap(rows[rank], rows[pivot]);
    for (int other = 0; other < PARITY_RANK; ++other) {
      if (other == rank || !get_bit(rows[other], column)) continue;
      for (int word = 0; word < WORDS; ++word)
        rows[other][word] ^= rows[rank][word];
    }
    pivots.push_back(column);
    ++rank;
  }
  if (rank != PARITY_RANK) throw std::runtime_error("parity matrix rank failure");
  return pivots;
}

std::vector<Row> null_basis(const std::vector<Row> &rows,
                            const std::vector<int> &pivots) {
  std::array<bool, FREE_EDGES> is_pivot{};
  for (int pivot : pivots) is_pivot[pivot] = true;
  std::vector<Row> basis;
  for (int free = 0; free < FREE_EDGES; ++free) {
    if (is_pivot[free]) continue;
    Row vector{};
    toggle_bit(vector, free);
    for (int r = 0; r < PARITY_RANK; ++r)
      if (get_bit(rows[r], free)) toggle_bit(vector, pivots[r]);
    basis.push_back(vector);
  }
  if (basis.size() != FREE_EDGES - PARITY_RANK)
    throw std::runtime_error("nullity failure");
  return basis;
}

std::vector<std::pair<int, int>> free_pairs() {
  std::vector<std::pair<int, int>> result;
  for (int a = 1; a < N; ++a)
    for (int b = a + 1; b < N; ++b) result.emplace_back(a, b);
  if (result.size() != FREE_EDGES) throw std::runtime_error("edge count failure");
  return result;
}

std::array<int, 5> clique5(const std::array<uint64_t, N> &red, bool blue,
                           int first_vertex = 0) {
  auto neighbors = [&](int vertex) {
    if (!blue) return red[vertex];
    return (~red[vertex]) & VERTEX_MASK & ~(UINT64_C(1) << vertex);
  };
  auto greater = [](int vertex) {
    return VERTEX_MASK & ~((UINT64_C(1) << (vertex + 1)) - 1);
  };
  for (int a = first_vertex; a < N; ++a) {
    uint64_t bs = neighbors(a) & greater(a);
    while (bs) {
      const int b = std::countr_zero(bs);
      bs &= bs - 1;
      uint64_t cs = neighbors(a) & neighbors(b) & greater(b);
      while (cs) {
        const int c = std::countr_zero(cs);
        cs &= cs - 1;
        uint64_t ds = neighbors(a) & neighbors(b) & neighbors(c) & greater(c);
        while (ds) {
          const int d = std::countr_zero(ds);
          ds &= ds - 1;
          const uint64_t es = neighbors(a) & neighbors(b) & neighbors(c) &
                              neighbors(d) & greater(d);
          if (es) return {a, b, c, d, std::countr_zero(es)};
        }
      }
    }
  }
  return {-1, -1, -1, -1, -1};
}

uint32_t encode_clique(const std::array<int, 5> &vertices, bool blue) {
  uint32_t result = blue ? UINT32_C(1) << 30 : 0;
  for (int i = 0; i < 5; ++i)
    result |= static_cast<uint32_t>(vertices[i]) << (6 * i);
  return result;
}

std::string graph_hex(const std::array<uint64_t, N> &red) {
  static constexpr char alphabet[] = "0123456789abcdef";
  std::string result;
  int digit = 0, shift = 0;
  for (int a = 0; a < N; ++a)
    for (int b = a + 1; b < N; ++b) {
      if ((red[a] >> b) & 1) digit |= 1 << shift;
      if (++shift == 4) {
        result.push_back(alphabet[digit]);
        digit = shift = 0;
      }
    }
  if (shift) result.push_back(alphabet[digit]);
  return result;
}

uint64_t mix64(uint64_t value) {
  value = (value ^ (value >> 30)) * UINT64_C(0xbf58476d1ce4e5b9);
  value = (value ^ (value >> 27)) * UINT64_C(0x94d049bb133111eb);
  return value ^ (value >> 31);
}

}  // namespace

int main(int argc, char **) {
  try {
    if (argc != 1)
      throw std::runtime_error("usage: enumerate_rank829");
    std::vector<Row> rows = make_rows();
    const std::vector<int> pivots = reduce(rows);
    const std::vector<Row> basis = null_basis(rows, pivots);
    const std::vector<std::pair<int, int>> pairs = free_pairs();

    std::array<std::array<uint64_t, N>, FREE_EDGES - PARITY_RANK> deltas{};
    for (int j = 0; j < static_cast<int>(basis.size()); ++j)
      for (int column = 0; column < FREE_EDGES; ++column)
        if (get_bit(basis[j], column)) {
          const auto [a, b] = pairs[column];
          deltas[j][a] ^= UINT64_C(1) << b;
          deltas[j][b] ^= UINT64_C(1) << a;
        }

    std::array<uint64_t, N> red{};
    uint64_t red_k5 = 0, blue_k5 = 0;
    uint64_t digest_xor = 0, digest_sum = 0;
    constexpr uint64_t ASSIGNMENTS = UINT64_C(1) << (FREE_EDGES - PARITY_RANK);
    for (uint64_t index = 0; index < ASSIGNMENTS; ++index) {
      if (index) {
        const int flip = std::countr_zero(index);
        for (int vertex = 0; vertex < N; ++vertex)
          red[vertex] ^= deltas[flip][vertex];
      }

      const std::array<int, 5> red_clique = clique5(red, false, 1);
      if (red_clique[0] >= 0) {
        const uint32_t code = encode_clique(red_clique, false);
        const uint64_t mixed = mix64((index << 32) ^ code);
        digest_xor ^= mixed;
        digest_sum += mixed;
        ++red_k5;
        continue;
      }
      const std::array<int, 5> blue_clique = clique5(red, true, 1);
      if (blue_clique[0] >= 0) {
        const uint32_t code = encode_clique(blue_clique, true);
        const uint64_t mixed = mix64((index << 32) ^ code);
        digest_xor ^= mixed;
        digest_sum += mixed;
        ++blue_k5;
        continue;
      }

      std::cout << "RESULT status=GOOD_GRAPH index=" << index
                << " graph_hex=" << graph_hex(red) << "\n";
      return 10;
    }
    std::cout << "RESULT status=EXHAUSTIVE_CODE_THEOREM"
              << " parity_rank=" << PARITY_RANK
              << " affine_dimension=" << basis.size()
              << " assignments=" << ASSIGNMENTS
              << " red_K5=" << red_k5 << " blue_K5=" << blue_k5
              << " digest_xor=" << std::hex << std::setw(16)
              << std::setfill('0') << digest_xor
              << " digest_sum=" << std::setw(16) << digest_sum << "\n";
    return 20;
  } catch (const std::exception &error) {
    std::cerr << "ERROR " << error.what() << "\n";
    return 2;
  }
}
