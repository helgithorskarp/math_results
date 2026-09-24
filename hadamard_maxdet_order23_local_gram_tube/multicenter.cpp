#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <set>
#include <stdexcept>
#include <string>
#include <vector>

namespace {

constexpr int kOrder = 23;
using Matrix = std::array<std::array<int, kOrder>, kOrder>;
using Gram = std::array<std::array<int, kOrder>, kOrder>;

constexpr std::int64_t kRecord = INT64_C(2779447296000000);
constexpr std::array<std::array<std::array<int, 2>, 2>, 3> kBlocks = {{
    {{{7, 8}, {9, 10}}},
    {{{3, 4}, {5, 6}}},
    {{{11, 12}, {13, 14}}},
}};

Matrix read_matrix(const std::string& path) {
  std::ifstream input(path);
  if (!input) throw std::runtime_error("cannot open " + path);
  Matrix matrix{};
  std::string line;
  for (int row = 0; row < kOrder; ++row) {
    if (!std::getline(input, line) || line.size() != kOrder)
      throw std::runtime_error("bad matrix row in " + path);
    for (int column = 0; column < kOrder; ++column) {
      if (line[column] != '+' && line[column] != '-')
        throw std::runtime_error("bad matrix entry in " + path);
      matrix[row][column] = line[column] == '+' ? 1 : -1;
    }
  }
  if (std::getline(input, line) && !line.empty())
    throw std::runtime_error("trailing matrix data in " + path);
  return matrix;
}

bool prime(std::int64_t value) {
  if (value < 2) return false;
  for (std::int64_t divisor = 2; divisor * divisor <= value; ++divisor)
    if (value % divisor == 0) return value == divisor;
  return true;
}

std::int64_t mod_pow(std::int64_t base, std::int64_t exponent,
                     std::int64_t modulus) {
  std::int64_t answer = 1;
  while (exponent > 0) {
    if (exponent & 1) answer = answer * base % modulus;
    base = base * base % modulus;
    exponent >>= 1;
  }
  return answer;
}

std::int64_t determinant_mod(const Matrix& matrix, std::int64_t modulus) {
  std::array<std::array<std::int64_t, kOrder>, kOrder> work{};
  for (int row = 0; row < kOrder; ++row)
    for (int column = 0; column < kOrder; ++column)
      work[row][column] = matrix[row][column] < 0 ? modulus - 1 : 1;
  std::int64_t answer = 1;
  for (int column = 0; column < kOrder; ++column) {
    int pivot = column;
    while (pivot < kOrder && work[pivot][column] == 0) ++pivot;
    if (pivot == kOrder) return 0;
    if (pivot != column) {
      std::swap(work[pivot], work[column]);
      answer = (modulus - answer) % modulus;
    }
    const std::int64_t pivot_value = work[column][column];
    answer = answer * pivot_value % modulus;
    const std::int64_t inverse = mod_pow(pivot_value, modulus - 2, modulus);
    for (int row = column + 1; row < kOrder; ++row) {
      const std::int64_t multiplier = work[row][column] * inverse % modulus;
      for (int other = column; other < kOrder; ++other) {
        work[row][other] =
            (work[row][other] - multiplier * work[column][other]) % modulus;
        if (work[row][other] < 0) work[row][other] += modulus;
      }
    }
  }
  return answer;
}

std::int64_t determinant(const Matrix& matrix) {
  // The two-prime product exceeds twice Hadamard's order-23 bound.  Thus
  // signed CRT reconstruction is the exact integer determinant, not merely
  // a congruence.  All products stay below INT64_MAX.
  constexpr std::int64_t first_prime = INT64_C(1000000007);
  constexpr std::int64_t second_prime = INT64_C(1000000009);
  static const bool checked_primes =
      prime(first_prime) && prime(second_prime);
  if (!checked_primes) throw std::runtime_error("bad CRT prime");
  const std::int64_t first = determinant_mod(matrix, first_prime);
  const std::int64_t second = determinant_mod(matrix, second_prime);
  std::int64_t difference = (second - first) % second_prime;
  if (difference < 0) difference += second_prime;
  const std::int64_t inverse =
      mod_pow(first_prime % second_prime, second_prime - 2, second_prime);
  const std::int64_t coefficient = difference * inverse % second_prime;
  constexpr std::int64_t modulus = first_prime * second_prime;
  std::int64_t result = first + first_prime * coefficient;
  if (result > modulus / 2) result -= modulus;
  if (result <= -INT64_C(10000000000000000) ||
      result >= INT64_C(10000000000000000))
    throw std::runtime_error("CRT result outside order-23 Hadamard bound");
  return result;
}

std::int64_t absolute(std::int64_t value) { return value < 0 ? -value : value; }

Gram gram(const Matrix& matrix, bool transpose) {
  Gram answer{};
  for (int left = 0; left < kOrder; ++left) {
    for (int right = 0; right < kOrder; ++right) {
      for (int coordinate = 0; coordinate < kOrder; ++coordinate) {
        answer[left][right] +=
            transpose ? matrix[coordinate][left] * matrix[coordinate][right]
                      : matrix[left][coordinate] * matrix[right][coordinate];
      }
    }
  }
  return answer;
}

void verify_gram_map(const Gram& source, const Gram& target,
                     const std::array<int, kOrder>& permutation,
                     const std::array<int, kOrder>& signs) {
  for (int left = 0; left < kOrder; ++left)
    for (int right = 0; right < kOrder; ++right)
      if (source[left][right] != signs[left] * signs[right] *
                                     target[permutation[left]][permutation[right]])
        throw std::runtime_error("bad signed Gram congruence");
}

Matrix switched(const Matrix& base,
                const std::array<std::array<int, 3>, 3>& choices) {
  Matrix answer = base;
  for (int core = 0; core < 3; ++core) {
    const int block = choices[core][0];
    const int column_kind = choices[core][1];
    const int row_kind = choices[core][2];
    for (const int column : kBlocks[block][column_kind])
      answer[core][column] *= -1;
    for (const int row : kBlocks[block][row_kind])
      answer[row][core] *= -1;
  }
  return answer;
}

std::vector<std::array<int, 4>> four_subsets() {
  std::vector<std::array<int, 4>> answer;
  for (int a = 0; a < kOrder; ++a)
    for (int b = a + 1; b < kOrder; ++b)
      for (int c = b + 1; c < kOrder; ++c)
        for (int d = c + 1; d < kOrder; ++d)
          answer.push_back({a, b, c, d});
  return answer;
}

int determinant3(const std::array<std::array<int, 3>, 3>& a) {
  return a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1]) -
         a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0]) +
         a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0]);
}

std::map<int, std::uint64_t> minor4_census(const Matrix& matrix) {
  const auto subsets = four_subsets();
  std::map<int, std::uint64_t> counts;
  for (const auto& rows : subsets) {
    for (const auto& columns : subsets) {
      std::array<std::array<int, 3>, 3> binary{};
      for (int i = 1; i < 4; ++i) {
        for (int j = 1; j < 4; ++j) {
          const int normalized =
              matrix[rows[i]][columns[j]] * matrix[rows[i]][columns[0]] *
              matrix[rows[0]][columns[j]] * matrix[rows[0]][columns[0]];
          binary[i - 1][j - 1] = normalized == -1 ? 1 : 0;
        }
      }
      counts[8 * std::abs(determinant3(binary))] += 1;
    }
  }
  return counts;
}

}  // namespace

int main(int argc, char** argv) {
  if (argc != 3) {
    std::cerr << "usage: multicenter RECORD0.txt RECORD1.txt\n";
    return 2;
  }
  try {
    const Matrix base = read_matrix(argv[1]);
    const Matrix second = read_matrix(argv[2]);
    if (absolute(determinant(base)) != kRecord ||
        absolute(determinant(second)) != kRecord)
      throw std::runtime_error("record determinant mismatch");

    int hamming = 0;
    for (int row = 0; row < kOrder; ++row)
      for (int column = 0; column < kOrder; ++column)
        hamming += base[row][column] != second[row][column];
    if (hamming != 12) throw std::runtime_error("Hamming distance mismatch");

    const std::array<int, kOrder> row_permutation = {
        0, 1, 2, 5, 6, 11, 12, 9, 10, 3, 4, 13,
        14, 7, 8, 15, 16, 17, 18, 19, 20, 21, 22};
    const std::array<int, kOrder> row_signs = {
        1, 1, 1, -1, -1, 1, 1, -1, -1, 1, 1, -1,
        -1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1};
    const std::array<int, kOrder> column_permutation = {
        1, 2, 0, 5, 6, 11, 12, 9, 10, 3, 4, 13,
        14, 7, 8, 15, 16, 17, 18, 19, 20, 21, 22};
    const std::array<int, kOrder> column_signs = {
        1, 1, 1, 1, 1, -1, -1, 1, 1, -1, -1, 1,
        1, -1, -1, 1, 1, 1, 1, 1, 1, 1, 1};
    verify_gram_map(gram(second, false), gram(base, false), row_permutation,
                    row_signs);
    verify_gram_map(gram(second, true), gram(base, true), column_permutation,
                    column_signs);

    const std::array<std::array<int, 3>, 3> second_choice =
        {{{1, 1, 0}, {0, 1, 0}, {2, 1, 0}}};
    if (switched(base, second_choice) != second)
      throw std::runtime_error("second matrix is not the stated switch");

    std::uint64_t record_switches = 0;
    std::int64_t largest = 0;
    std::set<std::int64_t> determinant_values;
    for (int first = 0; first < 12; ++first) {
      for (int middle = 0; middle < 12; ++middle) {
        for (int last = 0; last < 12; ++last) {
          std::array<std::array<int, 3>, 3> choices{};
          const std::array<int, 3> encoded = {first, middle, last};
          for (int core = 0; core < 3; ++core) {
            choices[core] = {encoded[core] / 4,
                             (encoded[core] / 2) % 2,
                             encoded[core] % 2};
          }
          const std::int64_t value =
              absolute(determinant(switched(base, choices)));
          determinant_values.insert(value);
          largest = std::max(largest, value);
          record_switches += value == kRecord;
        }
      }
    }
    if (record_switches != 2 || largest != kRecord ||
        determinant_values.size() != 770)
      throw std::runtime_error("structured switch census mismatch");

    const auto base_minors = minor4_census(base);
    const auto second_minors = minor4_census(second);
    const std::map<int, std::uint64_t> expected_base = {
        {0, UINT64_C(45245701)}, {8, UINT64_C(31659704)},
        {16, UINT64_C(1505620)}};
    const std::map<int, std::uint64_t> expected_second = {
        {0, UINT64_C(45247429)}, {8, UINT64_C(31657400)},
        {16, UINT64_C(1506196)}};
    if (base_minors != expected_base || second_minors != expected_second)
      throw std::runtime_error("four-minor census mismatch");

    std::cout << "both exact determinants: " << kRecord << '\n';
    std::cout << "Hamming distance: " << hamming << '\n';
    std::cout << "structured switches: 1728; determinant values: "
              << determinant_values.size() << "; record switches: "
              << record_switches << '\n';
    std::cout << "base |4-minor| counts: 0:" << base_minors.at(0)
              << " 8:" << base_minors.at(8) << " 16:" << base_minors.at(16)
              << '\n';
    std::cout << "second |4-minor| counts: 0:" << second_minors.at(0)
              << " 8:" << second_minors.at(8) << " 16:"
              << second_minors.at(16) << '\n';
    std::cout << "second H-class and signed Gram-center equivalence verified\n";
  } catch (const std::exception& error) {
    std::cerr << error.what() << '\n';
    return 1;
  }
}
