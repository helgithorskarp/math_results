#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <initializer_list>
#include <iostream>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

namespace {

constexpr int kOrder = 23;
constexpr std::int64_t kScale = 170492220;
constexpr std::int64_t kRecord = 2779447296000000LL;

constexpr std::int64_t kInverseNumerator[kOrder][kOrder] = {
    {8338950, -751275, -751275, 574605, 574605, -942930, -942930, 170595, 170595, 471105, 471105, 574605, 574605, -942930, -942930, 237375, 237375, 237375, 237375, 237375, 237375, 237375, 237375},
    {-751275, 8338950, -751275, 170595, 170595, 471105, 471105, 574605, 574605, -942930, -942930, 574605, 574605, -942930, -942930, 237375, 237375, 237375, 237375, 237375, 237375, 237375, 237375},
    {-751275, -751275, 8338950, 574605, 574605, -942930, -942930, 574605, 574605, -942930, -942930, 170595, 170595, 471105, 471105, 237375, 237375, 237375, 237375, 237375, 237375, 237375, 237375},
    {574605, 170595, 574605, 7970328, -554283, -784125, -784125, 374940, 374940, 225900, 225900, 374940, 374940, 225900, 225900, 341820, 341820, 341820, 341820, 341820, 341820, 341820, 341820},
    {574605, 170595, 574605, -554283, 7970328, -784125, -784125, 374940, 374940, 225900, 225900, 374940, 374940, 225900, 225900, 341820, 341820, 341820, 341820, 341820, 341820, 341820, 341820},
    {-942930, 471105, -942930, -784125, -784125, 8117658, -406953, 225900, 225900, 320265, 320265, 225900, 225900, 320265, 320265, 246870, 246870, 246870, 246870, 246870, 246870, 246870, 246870},
    {-942930, 471105, -942930, -784125, -784125, -406953, 8117658, 225900, 225900, 320265, 320265, 225900, 225900, 320265, 320265, 246870, 246870, 246870, 246870, 246870, 246870, 246870, 246870},
    {170595, 574605, 574605, 374940, 374940, 225900, 225900, 7970328, -554283, -784125, -784125, 374940, 374940, 225900, 225900, 341820, 341820, 341820, 341820, 341820, 341820, 341820, 341820},
    {170595, 574605, 574605, 374940, 374940, 225900, 225900, -554283, 7970328, -784125, -784125, 374940, 374940, 225900, 225900, 341820, 341820, 341820, 341820, 341820, 341820, 341820, 341820},
    {471105, -942930, -942930, 225900, 225900, 320265, 320265, -784125, -784125, 8117658, -406953, 225900, 225900, 320265, 320265, 246870, 246870, 246870, 246870, 246870, 246870, 246870, 246870},
    {471105, -942930, -942930, 225900, 225900, 320265, 320265, -784125, -784125, -406953, 8117658, 225900, 225900, 320265, 320265, 246870, 246870, 246870, 246870, 246870, 246870, 246870, 246870},
    {574605, 574605, 170595, 374940, 374940, 225900, 225900, 374940, 374940, 225900, 225900, 7970328, -554283, -784125, -784125, 341820, 341820, 341820, 341820, 341820, 341820, 341820, 341820},
    {574605, 574605, 170595, 374940, 374940, 225900, 225900, 374940, 374940, 225900, 225900, -554283, 7970328, -784125, -784125, 341820, 341820, 341820, 341820, 341820, 341820, 341820, 341820},
    {-942930, -942930, 471105, 225900, 225900, 320265, 320265, 225900, 225900, 320265, 320265, -784125, -784125, 8117658, -406953, 246870, 246870, 246870, 246870, 246870, 246870, 246870, 246870},
    {-942930, -942930, 471105, 225900, 225900, 320265, 320265, 225900, 225900, 320265, 320265, -784125, -784125, -406953, 8117658, 246870, 246870, 246870, 246870, 246870, 246870, 246870, 246870},
    {237375, 237375, 237375, 341820, 341820, 246870, 246870, 341820, 341820, 246870, 246870, 341820, 341820, 246870, 246870, 7898152, -626459, -626459, -626459, 320720, 320720, 320720, 320720},
    {237375, 237375, 237375, 341820, 341820, 246870, 246870, 341820, 341820, 246870, 246870, 341820, 341820, 246870, 246870, -626459, 7898152, -626459, -626459, 320720, 320720, 320720, 320720},
    {237375, 237375, 237375, 341820, 341820, 246870, 246870, 341820, 341820, 246870, 246870, 341820, 341820, 246870, 246870, -626459, -626459, 7898152, -626459, 320720, 320720, 320720, 320720},
    {237375, 237375, 237375, 341820, 341820, 246870, 246870, 341820, 341820, 246870, 246870, 341820, 341820, 246870, 246870, -626459, -626459, -626459, 7898152, 320720, 320720, 320720, 320720},
    {237375, 237375, 237375, 341820, 341820, 246870, 246870, 341820, 341820, 246870, 246870, 341820, 341820, 246870, 246870, 320720, 320720, 320720, 320720, 7898152, -626459, -626459, -626459},
    {237375, 237375, 237375, 341820, 341820, 246870, 246870, 341820, 341820, 246870, 246870, 341820, 341820, 246870, 246870, 320720, 320720, 320720, 320720, -626459, 7898152, -626459, -626459},
    {237375, 237375, 237375, 341820, 341820, 246870, 246870, 341820, 341820, 246870, 246870, 341820, 341820, 246870, 246870, 320720, 320720, 320720, 320720, -626459, -626459, 7898152, -626459},
    {237375, 237375, 237375, 341820, 341820, 246870, 246870, 341820, 341820, 246870, 246870, 341820, 341820, 246870, 246870, 320720, 320720, 320720, 320720, -626459, -626459, -626459, 7898152},
};

constexpr std::array<std::int64_t, 48> kPrimes = {
    1000000007, 999999937, 999999929, 999999893, 999999883, 999999797,
    999999761, 999999757, 999999751, 999999739, 999999733, 999999677,
    999999667, 999999613, 999999607, 999999599, 999999587, 999999541,
    999999527, 999999503, 999999491, 999999487, 999999433, 999999391,
    999999353, 999999337, 999999323, 999999229, 999999223, 999999197,
    999999193, 999999191, 999999181, 999999163, 999999151, 999999137,
    999999131, 999999113, 999999107, 999999103, 999999067, 999999059,
    999999043, 999999029, 999999017, 999999001, 999998981, 999998971,
};

constexpr std::array<std::uint64_t, 48> kExpectedOne = {
    1228, 832, 214, 126, 66, 42, 6, 0, 0, 0, 16, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
};
constexpr std::array<std::uint64_t, 48> kExpectedTwo = {
    1586991, 792930, 408387, 191970, 105141, 50106, 25896, 11109,
    6552, 3006, 1848, 996, 1296, 144, 0, 672,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
};
constexpr std::array<std::uint64_t, 48> kExpectedGraphThree = {
    1342206, 631588, 347564, 169797, 89512, 42078, 20955, 7316,
    5988, 2898, 1536, 5280, 0, 0, 384, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
};
constexpr std::array<std::uint64_t, 48> kExpectedGraphFour = {
    83035556, 42080074, 20554302, 10506903, 5233902, 2612088,
    1344108, 719934, 295314, 164928, 74106, 44304,
    13452, 7488, 3696, 144, 4608, 0,
    0, 0, 96, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
};
constexpr std::array<std::uint64_t, 48> kExpectedDeletionFour = {
    70761, 42720, 19497, 7782, 3129, 2784, 726, 612,
    816, 108, 60, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
};

struct Edge { int i; int j; int value; };
struct Edit { int edge_index; int new_value; };
struct Summary {
  std::uint64_t total = 0;
  std::array<std::uint64_t, kPrimes.size()> witness_counts{};
  std::uint64_t survivors = 0;
  std::vector<std::vector<Edit>> survivor_edits;
};

std::int64_t normalize(std::int64_t value, std::int64_t prime) {
  value %= prime;
  if (value < 0) value += prime;
  return static_cast<std::int64_t>(value);
}

std::int64_t mod_pow(std::int64_t base, std::int64_t exponent,
                     std::int64_t prime) {
  std::int64_t answer = 1;
  base = normalize(base, prime);
  while (exponent > 0) {
    if ((exponent & 1) != 0)
      answer = normalize(answer * base, prime);
    base = normalize(base * base, prime);
    exponent >>= 1;
  }
  return answer;
}

bool is_prime(std::int64_t value) {
  if (value < 2) return false;
  if ((value & 1) == 0) return value == 2;
  for (std::int64_t divisor = 3; divisor * divisor <= value; divisor += 2)
    if (value % divisor == 0) return false;
  return true;
}

std::int64_t determinant_mod(
    std::array<std::array<std::int64_t, 8>, 8> matrix, int size,
    std::int64_t prime) {
  std::int64_t determinant = 1;
  for (int column = 0; column < size; ++column) {
    int pivot = column;
    while (pivot < size && matrix[pivot][column] == 0) ++pivot;
    if (pivot == size) return 0;
    if (pivot != column) {
      std::swap(matrix[pivot], matrix[column]);
      determinant = prime - determinant;
    }
    const std::int64_t pivot_value = matrix[column][column];
    determinant = normalize(determinant * pivot_value, prime);
    const std::int64_t inverse = mod_pow(pivot_value, prime - 2, prime);
    for (int row = column + 1; row < size; ++row) {
      const std::int64_t multiplier = normalize(matrix[row][column] * inverse,
                                                prime);
      for (int col = column; col < size; ++col)
        matrix[row][col] = normalize(
            matrix[row][col] - multiplier * matrix[column][col], prime);
    }
  }
  return determinant;
}

std::vector<std::vector<int>> read_record(const std::string& path) {
  std::ifstream input(path);
  if (!input) throw std::runtime_error("cannot open record matrix: " + path);
  std::vector<std::vector<int>> matrix;
  std::string line;
  while (std::getline(input, line)) {
    std::vector<int> row;
    for (char symbol : line) {
      if (symbol == '+') row.push_back(1);
      if (symbol == '-') row.push_back(-1);
    }
    if (!row.empty()) {
      if (static_cast<int>(row.size()) != kOrder)
        throw std::runtime_error("record row has the wrong length");
      matrix.push_back(std::move(row));
    }
  }
  if (static_cast<int>(matrix.size()) != kOrder)
    throw std::runtime_error("record matrix has the wrong number of rows");
  return matrix;
}

std::vector<std::vector<int>> gram_matrix(
    const std::vector<std::vector<int>>& record) {
  std::vector<std::vector<int>> gram(kOrder, std::vector<int>(kOrder));
  for (int i = 0; i < kOrder; ++i)
    for (int j = 0; j < kOrder; ++j)
      for (int column = 0; column < kOrder; ++column)
        gram[i][j] += record[i][column] * record[j][column];
  return gram;
}

class Enumerator {
 public:
  explicit Enumerator(const std::vector<std::vector<int>>& gram)
      : gram_(gram) {
    for (int i = 0; i < kOrder; ++i) {
      for (int j = 0; j < i; ++j) {
        const int value = gram_[i][j];
        if (value != -1 && value != 3)
          throw std::runtime_error("record Gram matrix is not graph-valued");
        edges_.push_back({i, j, value});
        if (value == 3) three_edges_.push_back(static_cast<int>(edges_.size()) - 1);
      }
    }
    if (edges_.size() != 253 || three_edges_.size() != 45)
      throw std::runtime_error("unexpected record Gram edge counts");
    for (int i = 0; i < kOrder; ++i) {
      for (int j = 0; j < kOrder; ++j) {
        std::int64_t entry = 0;
        for (int k = 0; k < kOrder; ++k)
          entry += static_cast<std::int64_t>(gram_[i][k]) *
                   kInverseNumerator[k][j];
        if (entry != (i == j ? kScale : 0))
          throw std::runtime_error("inverse check failed");
      }
    }
  }

  Summary arbitrary_one_edit() const {
    Summary summary;
    for (int edge = 0; edge < static_cast<int>(edges_.size()); ++edge)
      for (int value = -21; value <= 19; value += 4)
        if (value != edges_[edge].value) evaluate({{edge, value}}, summary);
    return summary;
  }

  Summary arbitrary_two_edits() const {
    Summary summary;
    for (int first = 0; first < static_cast<int>(edges_.size()); ++first) {
      for (int second = first + 1; second < static_cast<int>(edges_.size());
           ++second) {
        for (int first_value = -21; first_value <= 19; first_value += 4) {
          if (first_value == edges_[first].value) continue;
          for (int second_value = -21; second_value <= 19; second_value += 4)
            if (second_value != edges_[second].value)
              evaluate({{first, first_value}, {second, second_value}}, summary);
        }
      }
    }
    return summary;
  }

  Summary graph_three_edits() const {
    Summary summary;
    const int count = static_cast<int>(edges_.size());
    for (int first = 0; first < count; ++first)
      for (int second = first + 1; second < count; ++second)
        for (int third = second + 1; third < count; ++third)
          evaluate({{first, toggle(first)}, {second, toggle(second)},
                    {third, toggle(third)}}, summary);
    return summary;
  }

  Summary graph_four_edits() const {
    Summary summary;
    const int count = static_cast<int>(edges_.size());
    for (int first = 0; first < count; ++first)
      for (int second = first + 1; second < count; ++second)
        for (int third = second + 1; third < count; ++third)
          for (int fourth = third + 1; fourth < count; ++fourth)
            evaluate({{first, toggle(first)}, {second, toggle(second)},
                      {third, toggle(third)}, {fourth, toggle(fourth)}},
                     summary);
    return summary;
  }

  Summary delete_four_three_edges() const {
    Summary summary;
    const int count = static_cast<int>(three_edges_.size());
    for (int a = 0; a < count; ++a)
      for (int b = a + 1; b < count; ++b)
        for (int c = b + 1; c < count; ++c)
          for (int d = c + 1; d < count; ++d)
            evaluate({{three_edges_[a], -1}, {three_edges_[b], -1},
                      {three_edges_[c], -1}, {three_edges_[d], -1}}, summary);
    return summary;
  }

 private:
  int toggle(int edge) const { return edges_[edge].value == -1 ? 3 : -1; }

  void evaluate(std::initializer_list<Edit> edits, Summary& summary) const {
    ++summary.total;
    std::array<int, 8> vertices{};
    int vertex_count = 0;
    for (const Edit& edit : edits) {
      vertices[vertex_count++] = edges_[edit.edge_index].i;
      vertices[vertex_count++] = edges_[edit.edge_index].j;
    }
    std::sort(vertices.begin(), vertices.begin() + vertex_count);
    const int size = static_cast<int>(
        std::unique(vertices.begin(), vertices.begin() + vertex_count) -
        vertices.begin());
    std::array<int, kOrder> position{};
    position.fill(-1);
    for (int i = 0; i < size; ++i) position[vertices[i]] = i;
    std::array<std::array<std::int64_t, 8>, 8> perturbation{};
    for (const Edit& edit : edits) {
      const Edge& edge = edges_[edit.edge_index];
      const std::int64_t delta = edit.new_value - edge.value;
      const int i = position[edge.i];
      const int j = position[edge.j];
      perturbation[i][j] = delta;
      perturbation[j][i] = delta;
    }
    for (std::size_t prime_index = 0; prime_index < kPrimes.size();
         ++prime_index) {
      const std::int64_t prime = kPrimes[prime_index];
      std::array<std::array<std::int64_t, 8>, 8> update{};
      for (int row = 0; row < size; ++row) {
        for (int column = 0; column < size; ++column) {
          std::int64_t value = row == column ? kScale : 0;
          for (int middle = 0; middle < size; ++middle)
            value += kInverseNumerator[vertices[row]][vertices[middle]] *
                     perturbation[middle][column];
          update[row][column] = normalize(value, prime);
        }
      }
      const std::int64_t numerator = determinant_mod(update, size, prime);
      const std::int64_t square_test = normalize(
          numerator * mod_pow(kScale, size, prime), prime);
      if (square_test != 0 &&
          mod_pow(square_test, (prime - 1) / 2, prime) == prime - 1) {
        ++summary.witness_counts[prime_index];
        return;
      }
    }
    ++summary.survivors;
    summary.survivor_edits.push_back(std::vector<Edit>(edits));
  }

  const std::vector<std::vector<int>>& gram_;
  std::vector<Edge> edges_;
  std::vector<int> three_edges_;
};

std::int64_t full_determinant_mod(std::vector<std::vector<std::int64_t>> matrix,
                                  std::int64_t prime) {
  std::int64_t determinant = 1;
  for (int column = 0; column < kOrder; ++column) {
    int pivot = column;
    while (pivot < kOrder && matrix[pivot][column] == 0) ++pivot;
    if (pivot == kOrder) return 0;
    if (pivot != column) {
      std::swap(matrix[pivot], matrix[column]);
      determinant = prime - determinant;
    }
    const std::int64_t pivot_value = matrix[column][column];
    determinant = normalize(determinant * pivot_value, prime);
    const std::int64_t inverse = mod_pow(pivot_value, prime - 2, prime);
    for (int row = column + 1; row < kOrder; ++row) {
      const std::int64_t multiplier = normalize(matrix[row][column] * inverse,
                                                prime);
      for (int col = column; col < kOrder; ++col)
        matrix[row][col] = normalize(
            matrix[row][col] - multiplier * matrix[column][col], prime);
    }
  }
  return determinant;
}

void validate_primes_and_record(const std::vector<std::vector<int>>& gram) {
  for (const std::int64_t prime : kPrimes) {
    if (!is_prime(prime) || kScale % prime == 0)
      throw std::runtime_error("invalid witness prime");
    std::vector<std::vector<std::int64_t>> matrix(
        kOrder, std::vector<std::int64_t>(kOrder));
    for (int i = 0; i < kOrder; ++i)
      for (int j = 0; j < kOrder; ++j)
        matrix[i][j] = normalize(gram[i][j], prime);
    const std::int64_t determinant = full_determinant_mod(matrix, prime);
    const std::int64_t record_mod = kRecord % prime;
    const std::int64_t expected = normalize(record_mod * record_mod, prime);
    if (determinant != expected)
      throw std::runtime_error("record determinant modular check failed");
  }
}

void print_summary(const std::string& name, const Summary& summary,
                   bool trailing_comma) {
  std::cout << "    \"" << name << "\": {\n"
            << "      \"total\": " << summary.total << ",\n"
            << "      \"survives_48_nonsquare_tests\": "
            << summary.survivors << ",\n"
            << "      \"witness_counts\": [";
  for (std::size_t i = 0; i < summary.witness_counts.size(); ++i) {
    if (i != 0) std::cout << ", ";
    std::cout << summary.witness_counts[i];
  }
  std::cout << "],\n      \"survivor_edits\": [";
  for (std::size_t i = 0; i < summary.survivor_edits.size(); ++i) {
    if (i != 0) std::cout << ", ";
    std::cout << '[';
    for (std::size_t j = 0; j < summary.survivor_edits[i].size(); ++j) {
      if (j != 0) std::cout << ", ";
      std::cout << '[' << summary.survivor_edits[i][j].edge_index << ", "
                << summary.survivor_edits[i][j].new_value << ']';
    }
    std::cout << ']';
  }
  std::cout << "]\n    }" << (trailing_comma ? "," : "") << '\n';
}

}  // namespace

int main(int argc, char** argv) {
  try {
    const std::string record_path = argc == 2 ? argv[1] : "record23.txt";
    const auto record = read_record(record_path);
    const auto gram = gram_matrix(record);
    validate_primes_and_record(gram);
    const Enumerator enumerator(gram);
    const Summary arbitrary_one = enumerator.arbitrary_one_edit();
    const Summary arbitrary_two = enumerator.arbitrary_two_edits();
    const Summary graph_three = enumerator.graph_three_edits();
    const Summary graph_four = enumerator.graph_four_edits();
    const Summary deletion_four = enumerator.delete_four_three_edges();
    if (arbitrary_one.total != 2530 || arbitrary_one.survivors != 0 ||
        arbitrary_one.witness_counts != kExpectedOne ||
        arbitrary_two.total != 3187800 || arbitrary_two.survivors != 756 ||
        arbitrary_two.witness_counts != kExpectedTwo ||
        graph_three.total != 2667126 || graph_three.survivors != 24 ||
        graph_three.witness_counts != kExpectedGraphThree ||
        graph_four.total != 166695375 || graph_four.survivors != 372 ||
        graph_four.witness_counts != kExpectedGraphFour ||
        deletion_four.total != 148995 || deletion_four.survivors != 0 ||
        deletion_four.witness_counts != kExpectedDeletionFour)
      throw std::runtime_error("enumeration result disagrees with certificate");
    std::cout << "{\n  \"order\": 23,\n  \"inverse_scale\": " << kScale
              << ",\n  \"witness_primes\": [";
    for (std::size_t i = 0; i < kPrimes.size(); ++i) {
      if (i != 0) std::cout << ", ";
      std::cout << kPrimes[i];
    }
    std::cout << "],\n  \"cases\": {\n";
    print_summary("arbitrary_one_edit", arbitrary_one, true);
    print_summary("arbitrary_two_edits", arbitrary_two, true);
    print_summary("graph_three_edits", graph_three, true);
    print_summary("graph_four_edits", graph_four, true);
    print_summary("delete_four_three_edges", deletion_four, false);
    std::cout << "  }\n}\n";
    std::cerr << "modular local Gram classification verified\n";
    return 0;
  } catch (const std::exception& error) {
    std::cerr << "error: " << error.what() << '\n';
    return 1;
  }
}
