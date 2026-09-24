#include <algorithm>
#include <array>
#include <bit>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <queue>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

#include "order23_inverse.hpp"

namespace {

constexpr int kOrder = order23::kOrder;
constexpr int kCandidateLimit = 1400;
constexpr int kWordCount = (kCandidateLimit + 63) / 64;
constexpr int kCliqueSize = kOrder;
constexpr std::uint64_t kAutomorphismGroupOrder = UINT64_C(442368);

using Matrix = std::array<std::array<int, kOrder>, kOrder>;
using Gram = std::array<std::array<int, kOrder>, kOrder>;
using Vector = std::array<int, kOrder>;
using SolutionKey = std::array<std::uint16_t, kCliqueSize>;
using MaskKey = std::array<std::uint32_t, kCliqueSize>;

constexpr std::array<std::array<int, kOrder>, 13> kGenerators = {{
    {{0, 1, 2, 3, 4, 5, 6, 8, 7, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22}},
    {{0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22}},
    {{0, 1, 2, 4, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22}},
    {{0, 1, 2, 3, 4, 6, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22}},
    {{0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 11, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22}},
    {{0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 13, 15, 16, 17, 18, 19, 20, 21, 22}},
    {{1, 0, 2, 7, 8, 9, 10, 3, 4, 5, 6, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22}},
    {{0, 2, 1, 11, 12, 13, 14, 7, 8, 9, 10, 3, 4, 5, 6, 15, 16, 17, 18, 19, 20, 21, 22}},
    {{0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 15, 17, 18, 19, 20, 21, 22}},
    {{0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 17, 18, 15, 19, 20, 21, 22}},
    {{0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 20, 19, 21, 22}},
    {{0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 20, 21, 22, 19}},
    {{0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 19, 20, 21, 22, 15, 16, 17, 18}},
}};

constexpr std::array<int, kOrder> kSecondRowPermutation = {
    0, 1, 2, 5, 6, 11, 12, 9, 10, 3, 4, 13,
    14, 7, 8, 15, 16, 17, 18, 19, 20, 21, 22};
constexpr std::array<int, kOrder> kSecondRowSigns = {
    1, 1, 1, -1, -1, 1, 1, -1, -1, 1, 1, -1,
    -1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1};

struct Bits {
  std::array<std::uint64_t, kWordCount> words{};

  bool any() const {
    return std::any_of(words.begin(), words.end(),
                       [](std::uint64_t word) { return word != 0; });
  }

  int count() const {
    int answer = 0;
    for (const std::uint64_t word : words) answer += std::popcount(word);
    return answer;
  }

  int first() const {
    for (int index = 0; index < kWordCount; ++index) {
      if (words[index] != 0)
        return 64 * index + std::countr_zero(words[index]);
    }
    return -1;
  }

  void set(int index) {
    words[index / 64] |= UINT64_C(1) << (index % 64);
  }

  void clear(int index) {
    words[index / 64] &= ~(UINT64_C(1) << (index % 64));
  }
};

Bits operator&(Bits left, const Bits& right) {
  for (int index = 0; index < kWordCount; ++index)
    left.words[index] &= right.words[index];
  return left;
}

void remove_neighbors(Bits& left, const Bits& neighbors) {
  for (int index = 0; index < kWordCount; ++index)
    left.words[index] &= ~neighbors.words[index];
}

struct SolutionHash {
  std::size_t operator()(const SolutionKey& key) const noexcept {
    std::size_t value = UINT64_C(0xcbf29ce484222325);
    for (const std::uint16_t entry : key) {
      value ^= static_cast<std::size_t>(entry + 1);
      value *= UINT64_C(0x100000001b3);
    }
    return value;
  }
};

struct OrbitReport {
  std::uint64_t size;
  MaskKey representative;
  bool contains_first;
  bool contains_second;
};

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

Gram gram(const Matrix& matrix) {
  Gram answer{};
  for (int left = 0; left < kOrder; ++left)
    for (int right = 0; right < kOrder; ++right)
      for (int coordinate = 0; coordinate < kOrder; ++coordinate)
        answer[left][right] +=
            matrix[left][coordinate] * matrix[right][coordinate];
  return answer;
}

void verify_inverse(const Gram& matrix) {
  for (int row = 0; row < kOrder; ++row) {
    for (int column = 0; column < kOrder; ++column) {
      std::int64_t value = 0;
      for (int middle = 0; middle < kOrder; ++middle)
        value += matrix[row][middle] *
                 order23::kInverseNumerator[middle][column];
      if (value != order23::kScale * (row == column))
        throw std::runtime_error("inverse table mismatch");
    }
  }
}

std::uint32_t vector_mask(Vector vector) {
  if (vector[0] < 0)
    for (int& entry : vector) entry = -entry;
  std::uint32_t mask = 0;
  for (int coordinate = 1; coordinate < kOrder; ++coordinate)
    if (vector[coordinate] < 0)
      mask |= UINT32_C(1) << (coordinate - 1);
  return mask;
}

std::pair<std::vector<std::uint32_t>, std::vector<Vector>>
enumerate_columns() {
  Vector vector{};
  vector.fill(1);
  std::array<std::int64_t, kOrder> row_sums{};
  for (int row = 0; row < kOrder; ++row)
    for (int column = 0; column < kOrder; ++column)
      if (row != column)
        row_sums[row] += order23::kInverseNumerator[row][column];
  std::int64_t value = 0;
  for (int row = 0; row < kOrder; ++row)
    for (int column = 0; column < kOrder; ++column)
      value += order23::kInverseNumerator[row][column];

  std::vector<std::uint32_t> masks;
  std::vector<Vector> vectors;
  std::uint32_t gray = 0;
  constexpr std::uint32_t limit = UINT32_C(1) << (kOrder - 1);
  for (std::uint32_t step = 0; step < limit; ++step) {
    if (value == order23::kScale) {
      masks.push_back(gray);
      vectors.push_back(vector);
    }
    if (step + 1 == limit) break;
    const std::uint32_t transition = step + 1;
    const int bit = std::countr_zero(transition);
    const int coordinate = bit + 1;
    const int old_sign = vector[coordinate];
    value -= 4LL * old_sign * row_sums[coordinate];
    for (int row = 0; row < kOrder; ++row) {
      if (row != coordinate)
        row_sums[row] -=
            2LL * order23::kInverseNumerator[row][coordinate] * old_sign;
    }
    vector[coordinate] = -old_sign;
    gray ^= UINT32_C(1) << bit;
  }
  return {std::move(masks), std::move(vectors)};
}

std::vector<Bits> compatibility_graph(const std::vector<Vector>& vectors) {
  std::vector<std::array<std::int64_t, kOrder>> transformed(vectors.size());
  for (std::size_t index = 0; index < vectors.size(); ++index)
    for (int row = 0; row < kOrder; ++row)
      for (int column = 0; column < kOrder; ++column)
        transformed[index][row] +=
            order23::kInverseNumerator[row][column] * vectors[index][column];

  std::vector<Bits> adjacency(vectors.size());
  for (int left = 0; left < static_cast<int>(vectors.size()); ++left) {
    for (int right = 0; right < left; ++right) {
      std::int64_t product = 0;
      for (int coordinate = 0; coordinate < kOrder; ++coordinate)
        product += vectors[left][coordinate] * transformed[right][coordinate];
      if (product == 0) {
        adjacency[left].set(right);
        adjacency[right].set(left);
      }
    }
  }
  return adjacency;
}

class CliqueEnumerator {
 public:
  explicit CliqueEnumerator(const std::vector<Bits>& adjacency)
      : adjacency_(adjacency) {}

  void run() {
    Bits all;
    for (int vertex = 0; vertex < static_cast<int>(adjacency_.size()); ++vertex)
      all.set(vertex);
    expand(all, 0);
  }

  std::uint64_t nodes() const { return nodes_; }
  const std::vector<SolutionKey>& solutions() const { return solutions_; }

 private:
  void color_sort(const Bits& input, std::vector<int>& order,
                  std::vector<int>& bounds) const {
    Bits remaining = input;
    int color = 0;
    order.clear();
    bounds.clear();
    while (remaining.any()) {
      ++color;
      Bits available = remaining;
      while (available.any()) {
        const int vertex = available.first();
        order.push_back(vertex);
        bounds.push_back(color);
        remaining.clear(vertex);
        available.clear(vertex);
        remove_neighbors(available, adjacency_[vertex]);
        available = available & remaining;
      }
    }
  }

  void expand(Bits candidates, int size) {
    ++nodes_;
    std::vector<int> order;
    std::vector<int> bounds;
    color_sort(candidates, order, bounds);
    for (int position = static_cast<int>(order.size()) - 1; position >= 0;
         --position) {
      if (size + bounds[position] < kCliqueSize) return;
      const int vertex = order[position];
      clique_[size] = vertex;
      const Bits next = candidates & adjacency_[vertex];
      if (size + 1 == kCliqueSize) {
        SolutionKey key{};
        for (int index = 0; index < kCliqueSize; ++index)
          key[index] = static_cast<std::uint16_t>(clique_[index]);
        std::sort(key.begin(), key.end());
        solutions_.push_back(key);
      } else if (size + 1 + next.count() >= kCliqueSize) {
        expand(next, size + 1);
      }
      candidates.clear(vertex);
    }
  }

  const std::vector<Bits>& adjacency_;
  std::array<int, kCliqueSize> clique_{};
  std::uint64_t nodes_ = 0;
  std::vector<SolutionKey> solutions_;
};

Matrix center_second(const Matrix& second) {
  Matrix result{};
  for (int source = 0; source < kOrder; ++source) {
    const int target = kSecondRowPermutation[source];
    for (int column = 0; column < kOrder; ++column)
      result[target][column] = kSecondRowSigns[source] * second[source][column];
  }
  return result;
}

SolutionKey matrix_key(
    const Matrix& matrix,
    const std::unordered_map<std::uint32_t, int>& mask_index) {
  SolutionKey answer{};
  for (int column = 0; column < kOrder; ++column) {
    Vector vector{};
    for (int row = 0; row < kOrder; ++row)
      vector[row] = matrix[row][column];
    answer[column] =
        static_cast<std::uint16_t>(mask_index.at(vector_mask(vector)));
  }
  std::sort(answer.begin(), answer.end());
  if (std::adjacent_find(answer.begin(), answer.end()) != answer.end())
    throw std::runtime_error("dependent repeated columns");
  return answer;
}

MaskKey mask_key(const SolutionKey& solution,
                 const std::vector<std::uint32_t>& masks) {
  MaskKey answer{};
  for (int index = 0; index < kCliqueSize; ++index)
    answer[index] = masks[solution[index]];
  std::sort(answer.begin(), answer.end());
  return answer;
}

std::vector<OrbitReport> classify_orbits(
    const std::vector<SolutionKey>& solutions,
    const std::vector<std::uint32_t>& masks,
    const std::vector<Vector>& vectors, const Gram& base,
    const SolutionKey& first, const SolutionKey& second,
    std::vector<int>& candidate_orbit_sizes) {
  for (const auto& generator : kGenerators)
    for (int left = 0; left < kOrder; ++left)
      for (int right = 0; right < kOrder; ++right)
        if (base[generator[left]][generator[right]] != base[left][right])
          throw std::runtime_error("bad Gram automorphism generator");

  std::unordered_map<std::uint32_t, int> mask_index;
  for (int index = 0; index < static_cast<int>(masks.size()); ++index)
    mask_index.emplace(masks[index], index);
  std::array<std::vector<int>, kGenerators.size()> actions;
  for (auto& action : actions) action.resize(masks.size());
  for (int generator_index = 0;
       generator_index < static_cast<int>(kGenerators.size());
       ++generator_index) {
    for (int index = 0; index < static_cast<int>(vectors.size()); ++index) {
      Vector image{};
      for (int coordinate = 0; coordinate < kOrder; ++coordinate)
        image[kGenerators[generator_index][coordinate]] =
            vectors[index][coordinate];
      actions[generator_index][index] = mask_index.at(vector_mask(image));
    }
  }

  std::vector<bool> candidate_seen(masks.size());
  for (int seed = 0; seed < static_cast<int>(masks.size()); ++seed) {
    if (candidate_seen[seed]) continue;
    int orbit_size = 0;
    std::queue<int> queue;
    queue.push(seed);
    candidate_seen[seed] = true;
    while (!queue.empty()) {
      const int current = queue.front();
      queue.pop();
      ++orbit_size;
      for (const auto& action : actions) {
        const int image = action[current];
        if (!candidate_seen[image]) {
          candidate_seen[image] = true;
          queue.push(image);
        }
      }
    }
    candidate_orbit_sizes.push_back(orbit_size);
  }
  std::sort(candidate_orbit_sizes.begin(), candidate_orbit_sizes.end());

  std::unordered_map<SolutionKey, std::uint32_t, SolutionHash> solution_index;
  solution_index.reserve(2 * solutions.size());
  for (std::uint32_t index = 0; index < solutions.size(); ++index)
    if (!solution_index.emplace(solutions[index], index).second)
      throw std::runtime_error("duplicate clique");
  const std::uint32_t first_index = solution_index.at(first);
  const std::uint32_t second_index = solution_index.at(second);

  std::vector<bool> seen(solutions.size());
  std::vector<OrbitReport> reports;
  for (std::uint32_t seed = 0; seed < solutions.size(); ++seed) {
    if (seen[seed]) continue;
    OrbitReport report{0, mask_key(solutions[seed], masks), false, false};
    std::queue<std::uint32_t> queue;
    queue.push(seed);
    seen[seed] = true;
    while (!queue.empty()) {
      const std::uint32_t current = queue.front();
      queue.pop();
      ++report.size;
      report.representative =
          std::min(report.representative, mask_key(solutions[current], masks));
      report.contains_first |= current == first_index;
      report.contains_second |= current == second_index;
      for (const auto& action : actions) {
        SolutionKey image{};
        for (int index = 0; index < kCliqueSize; ++index)
          image[index] = static_cast<std::uint16_t>(
              action[solutions[current][index]]);
        std::sort(image.begin(), image.end());
        const auto found = solution_index.find(image);
        if (found == solution_index.end())
          throw std::runtime_error("solution orbit left clique census");
        if (!seen[found->second]) {
          seen[found->second] = true;
          queue.push(found->second);
        }
      }
    }
    if (kAutomorphismGroupOrder % report.size != 0)
      throw std::runtime_error("bad orbit size");
    reports.push_back(report);
  }
  std::sort(reports.begin(), reports.end(),
            [](const OrbitReport& left, const OrbitReport& right) {
              return left.representative < right.representative;
            });
  return reports;
}

void print_json(const std::vector<std::uint32_t>& masks,
                const std::vector<Bits>& adjacency,
                const CliqueEnumerator& enumerator,
                const std::vector<int>& candidate_orbit_sizes,
                const std::vector<OrbitReport>& orbits) {
  std::uint64_t edge_count = 0;
  std::map<int, int> degree_counts;
  for (const Bits& neighbors : adjacency) {
    const int degree = neighbors.count();
    edge_count += static_cast<std::uint64_t>(degree);
    ++degree_counts[degree];
  }
  if (edge_count % 2 != 0) throw std::runtime_error("odd degree sum");
  edge_count /= 2;

  std::cout << "{\n";
  std::cout << "  \"order\": 23,\n";
  std::cout << "  \"inverse_scale\": " << order23::kScale << ",\n";
  std::cout << "  \"normalized_columns\": " << masks.size() << ",\n";
  std::cout << "  \"candidate_column_orbit_sizes\": [";
  for (std::size_t index = 0; index < candidate_orbit_sizes.size(); ++index) {
    if (index != 0) std::cout << ", ";
    std::cout << candidate_orbit_sizes[index];
  }
  std::cout << "],\n";
  std::cout << "  \"compatibility_edges\": " << edge_count << ",\n";
  std::cout << "  \"degree_counts\": {";
  bool first_degree = true;
  for (const auto& [degree, count] : degree_counts) {
    if (!first_degree) std::cout << ", ";
    first_degree = false;
    std::cout << '\"' << degree << "\": " << count;
  }
  std::cout << "},\n";
  std::cout << "  \"clique_size\": " << kCliqueSize << ",\n";
  std::cout << "  \"cliques\": " << enumerator.solutions().size() << ",\n";
  std::cout << "  \"search_nodes\": " << enumerator.nodes() << ",\n";
  std::cout << "  \"automorphism_generators\": " << kGenerators.size()
            << ",\n";
  std::cout << "  \"automorphism_group_order\": "
            << kAutomorphismGroupOrder << ",\n";
  std::cout << "  \"decomposition_classes\": " << orbits.size() << ",\n";
  std::cout << "  \"orbits\": [\n";
  for (std::size_t orbit_index = 0; orbit_index < orbits.size();
       ++orbit_index) {
    const OrbitReport& orbit = orbits[orbit_index];
    std::cout << "    {\"class\": " << orbit_index + 1
              << ", \"orbit_size\": " << orbit.size
              << ", \"stabilizer_order\": "
              << kAutomorphismGroupOrder / orbit.size
              << ", \"contains_record23\": "
              << (orbit.contains_first ? "true" : "false")
              << ", \"contains_record23_class2\": "
              << (orbit.contains_second ? "true" : "false")
              << ", \"column_masks\": [";
    for (int index = 0; index < kCliqueSize; ++index) {
      if (index != 0) std::cout << ", ";
      std::cout << orbit.representative[index];
    }
    std::cout << "]}";
    if (orbit_index + 1 != orbits.size()) std::cout << ',';
    std::cout << '\n';
  }
  std::cout << "  ]\n";
  std::cout << "}\n";
}

}  // namespace

int main(int argc, char** argv) {
  if (argc != 3) {
    std::cerr << "usage: gram_decompositions RECORD0.txt RECORD1.txt\n";
    return 2;
  }
  try {
    const Matrix first_matrix = read_matrix(argv[1]);
    const Matrix second_matrix = center_second(read_matrix(argv[2]));
    const Gram base = gram(first_matrix);
    if (gram(second_matrix) != base)
      throw std::runtime_error("second matrix does not map to the base Gram");
    verify_inverse(base);

    auto [masks, vectors] = enumerate_columns();
    if (masks.size() != 1382)
      throw std::runtime_error("normalized column count mismatch");
    std::unordered_map<std::uint32_t, int> mask_index;
    for (int index = 0; index < static_cast<int>(masks.size()); ++index)
      mask_index.emplace(masks[index], index);
    const SolutionKey first = matrix_key(first_matrix, mask_index);
    const SolutionKey second = matrix_key(second_matrix, mask_index);

    const std::vector<Bits> adjacency = compatibility_graph(vectors);
    CliqueEnumerator enumerator(adjacency);
    enumerator.run();
    if (enumerator.solutions().size() != 552960 ||
        enumerator.nodes() != 9804083)
      throw std::runtime_error("clique census mismatch");

    std::vector<int> candidate_orbit_sizes;
    const std::vector<OrbitReport> orbits = classify_orbits(
        enumerator.solutions(), masks, vectors, base, first, second,
        candidate_orbit_sizes);
    const std::map<std::uint64_t, int> expected_orbit_counts = {
        {UINT64_C(18432), 6}, {UINT64_C(55296), 8}};
    std::map<std::uint64_t, int> observed_orbit_counts;
    for (const OrbitReport& orbit : orbits) ++observed_orbit_counts[orbit.size];
    if (orbits.size() != 14 ||
        observed_orbit_counts != expected_orbit_counts ||
        candidate_orbit_sizes != std::vector<int>({6, 432, 432, 512}))
      throw std::runtime_error("orbit census mismatch");
    if (std::count_if(orbits.begin(), orbits.end(),
                      [](const OrbitReport& orbit) {
                        return orbit.contains_first;
                      }) != 1 ||
        std::count_if(orbits.begin(), orbits.end(),
                      [](const OrbitReport& orbit) {
                        return orbit.contains_second;
                      }) != 1)
      throw std::runtime_error("known matrix class mismatch");

    print_json(masks, adjacency, enumerator, candidate_orbit_sizes, orbits);
  } catch (const std::exception& error) {
    std::cerr << error.what() << '\n';
    return 1;
  }
}
