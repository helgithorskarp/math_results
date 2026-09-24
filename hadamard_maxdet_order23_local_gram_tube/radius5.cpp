#include <algorithm>
#include <array>
#include <bit>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <numeric>
#include <set>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

#include "order23_inverse.hpp"

namespace {

constexpr int kMaximumEdges = 5;
constexpr int kColorCount = 11;
constexpr std::array<int, kColorCount> kCapacities = {
    1, 2, 2, 1, 2, 2, 1, 2, 2, 4, 4,
};
constexpr std::array<std::uint64_t, kMaximumEdges + 1> kExpectedOrbits = {
    1, 16, 380, 8887, 197931, 4132509,
};
constexpr std::array<std::uint64_t, kMaximumEdges + 1>
    kExpectedInternallyColored = {
        1, 63, 2445, 73707, 1886683, 42883999,
    };
constexpr std::array<std::uint64_t, 48> kExpectedRadius5WitnessCounts = {
    2063869, 1034219, 517699, 258601, 128993, 64392, 32222, 16102,
    8137, 4138, 2054, 1003, 497, 287, 124, 72,
    38, 18, 7, 7, 1, 2, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
};

using Gram = std::array<std::array<int, order23::kOrder>, order23::kOrder>;

struct GramEdge {
  int left;
  int right;
  int value;
};

struct Shape {
  int edge_count;
  int vertex_count;
  std::uint16_t graph_code;
  std::vector<std::vector<int>> automorphisms;
};

struct Variant {
  std::uint16_t shape_index;
  std::uint32_t color_code;
  std::uint64_t occupancy;
  std::array<std::uint32_t, 12> outer_images{};
};

std::vector<std::vector<int>> permutations(int size) {
  std::vector<int> permutation(static_cast<std::size_t>(size));
  std::iota(permutation.begin(), permutation.end(), 0);
  std::vector<std::vector<int>> answer;
  do {
    answer.push_back(permutation);
  } while (std::next_permutation(permutation.begin(), permutation.end()));
  return answer;
}

int pair_bit(int left, int right) {
  if (left < right) std::swap(left, right);
  if (left == right) throw std::runtime_error("loop in simple graph");
  return left * (left - 1) / 2 + right;
}

std::uint16_t permute_graph(std::uint16_t graph, int vertex_count,
                            const std::vector<int>& permutation) {
  std::uint16_t image = 0;
  for (int left = 0; left < vertex_count; ++left) {
    for (int right = 0; right < left; ++right) {
      if ((graph >> pair_bit(left, right)) & 1U) {
        image |= static_cast<std::uint16_t>(
            1U << pair_bit(permutation[left], permutation[right]));
      }
    }
  }
  return image;
}

bool connected(std::uint16_t graph, int vertex_count) {
  std::array<bool, 6> seen{};
  std::array<int, 6> stack{};
  int stack_size = 1;
  stack[0] = 0;
  seen[0] = true;
  int seen_count = 1;
  while (stack_size > 0) {
    const int vertex = stack[--stack_size];
    for (int other = 0; other < vertex_count; ++other) {
      if (other == vertex || seen[other]) continue;
      if ((graph >> pair_bit(vertex, other)) & 1U) {
        seen[other] = true;
        ++seen_count;
        stack[stack_size++] = other;
      }
    }
  }
  return seen_count == vertex_count;
}

std::vector<Shape> generate_shapes() {
  std::vector<Shape> shapes;
  for (int edge_count = 1; edge_count <= kMaximumEdges; ++edge_count) {
    for (int vertex_count = 2; vertex_count <= edge_count + 1;
         ++vertex_count) {
      const int pair_count = vertex_count * (vertex_count - 1) / 2;
      const auto vertex_permutations = permutations(vertex_count);
      std::set<std::uint16_t> canonical_graphs;
      for (std::uint16_t graph = 0; graph < (1U << pair_count); ++graph) {
        if (std::popcount(graph) != edge_count ||
            !connected(graph, vertex_count))
          continue;
        std::uint16_t canonical = graph;
        for (const auto& permutation : vertex_permutations)
          canonical = std::min(
              canonical, permute_graph(graph, vertex_count, permutation));
        canonical_graphs.insert(canonical);
      }
      for (const std::uint16_t graph : canonical_graphs) {
        Shape shape{edge_count, vertex_count, graph, {}};
        for (const auto& permutation : vertex_permutations) {
          if (permute_graph(graph, vertex_count, permutation) == graph)
            shape.automorphisms.push_back(permutation);
        }
        shapes.push_back(std::move(shape));
      }
    }
  }
  const std::array<int, kMaximumEdges + 1> expected = {0, 1, 1, 3, 5, 12};
  for (int edge_count = 1; edge_count <= kMaximumEdges; ++edge_count) {
    const int observed = static_cast<int>(std::count_if(
        shapes.begin(), shapes.end(), [edge_count](const Shape& shape) {
          return shape.edge_count == edge_count;
        }));
    if (observed != expected[edge_count])
      throw std::runtime_error("connected shape count mismatch");
  }
  return shapes;
}

std::uint32_t encode_colors(const std::array<int, 6>& colors,
                            int vertex_count) {
  std::uint32_t code = 0;
  std::uint32_t multiplier = 1;
  for (int vertex = 0; vertex < vertex_count; ++vertex) {
    code += static_cast<std::uint32_t>(colors[vertex]) * multiplier;
    multiplier *= kColorCount;
  }
  return code;
}

std::array<int, 6> decode_colors(std::uint32_t code, int vertex_count) {
  std::array<int, 6> colors{};
  for (int vertex = 0; vertex < vertex_count; ++vertex) {
    colors[vertex] = static_cast<int>(code % kColorCount);
    code /= kColorCount;
  }
  return colors;
}

std::uint32_t permute_colors(const std::array<int, 6>& colors,
                             int vertex_count,
                             const std::vector<int>& permutation) {
  std::array<int, 6> image{};
  for (int vertex = 0; vertex < vertex_count; ++vertex)
    image[permutation[vertex]] = colors[vertex];
  return encode_colors(image, vertex_count);
}

std::uint32_t canonical_color_code(const Shape& shape,
                                   const std::array<int, 6>& colors) {
  std::uint32_t canonical = encode_colors(colors, shape.vertex_count);
  for (const auto& automorphism : shape.automorphisms)
    canonical = std::min(
        canonical,
        permute_colors(colors, shape.vertex_count, automorphism));
  return canonical;
}

std::uint64_t pack_occupancy(const std::array<int, 6>& colors,
                             int vertex_count) {
  std::uint64_t packed = 0;
  for (int vertex = 0; vertex < vertex_count; ++vertex)
    packed += UINT64_C(1) << (4 * colors[vertex]);
  return packed;
}

int occupancy(std::uint64_t packed, int color) {
  return static_cast<int>((packed >> (4 * color)) & UINT64_C(15));
}

bool occupancy_fits(std::uint64_t current, std::uint64_t addition) {
  for (int color = 0; color < kColorCount; ++color) {
    if (occupancy(current, color) + occupancy(addition, color) >
        kCapacities[color])
      return false;
  }
  return true;
}

std::vector<std::array<int, kColorCount>> outer_color_actions() {
  std::vector<std::array<int, kColorCount>> actions;
  for (const auto& core_permutation : permutations(3)) {
    for (int swap_k4 = 0; swap_k4 < 2; ++swap_k4) {
      std::array<int, kColorCount> action{};
      for (int core = 0; core < 3; ++core) {
        for (int kind = 0; kind < 3; ++kind)
          action[3 * core + kind] = 3 * core_permutation[core] + kind;
      }
      action[9] = 9 + swap_k4;
      action[10] = 10 - swap_k4;
      actions.push_back(action);
    }
  }
  if (actions.size() != 12) throw std::runtime_error("outer action mismatch");
  return actions;
}

class ColoredComponents {
 public:
  explicit ColoredComponents(std::vector<Shape> shapes)
      : shapes_(std::move(shapes)), actions_(outer_color_actions()) {
    generate_variants();
  }

  const std::vector<Shape>& shapes() const { return shapes_; }
  const std::vector<Variant>& variants() const { return variants_; }
  const std::vector<std::uint32_t>& variants_with_edges(int count) const {
    return by_edge_count_[count];
  }

 private:
  void generate_variants() {
    std::array<std::uint32_t, 7> powers11{};
    powers11[0] = 1;
    for (int exponent = 1; exponent <= 6; ++exponent)
      powers11[exponent] = powers11[exponent - 1] * kColorCount;

    for (std::size_t shape_index = 0; shape_index < shapes_.size();
         ++shape_index) {
      const Shape& shape = shapes_[shape_index];
      const std::size_t begin = variants_.size();
      const std::uint32_t code_count = powers11[shape.vertex_count];
      std::vector<std::uint8_t> visited(code_count, 0);
      for (std::uint32_t code = 0; code < code_count; ++code) {
        if (visited[code]) continue;
        const auto colors = decode_colors(code, shape.vertex_count);
        const std::uint64_t packed =
            pack_occupancy(colors, shape.vertex_count);
        bool valid = true;
        for (int color = 0; color < kColorCount; ++color)
          valid = valid && occupancy(packed, color) <= kCapacities[color];
        if (!valid) continue;
        for (const auto& automorphism : shape.automorphisms)
          visited[permute_colors(colors, shape.vertex_count, automorphism)] = 1;
        variants_.push_back(
            {static_cast<std::uint16_t>(shape_index), code, packed, {}});
      }
      const std::size_t end = variants_.size();
      std::vector<std::int32_t> lookup(code_count, -1);
      for (std::size_t index = begin; index < end; ++index)
        lookup[variants_[index].color_code] = static_cast<std::int32_t>(index);
      for (std::size_t index = begin; index < end; ++index) {
        const auto colors =
            decode_colors(variants_[index].color_code, shape.vertex_count);
        for (std::size_t action_index = 0; action_index < actions_.size();
             ++action_index) {
          std::array<int, 6> transformed{};
          for (int vertex = 0; vertex < shape.vertex_count; ++vertex)
            transformed[vertex] = actions_[action_index][colors[vertex]];
          const std::uint32_t canonical =
              canonical_color_code(shape, transformed);
          const std::int32_t image = lookup[canonical];
          if (image < 0) throw std::runtime_error("missing outer image");
          variants_[index].outer_images[action_index] =
              static_cast<std::uint32_t>(image);
        }
        by_edge_count_[shape.edge_count].push_back(
            static_cast<std::uint32_t>(index));
      }
    }
  }

  std::vector<Shape> shapes_;
  std::vector<Variant> variants_;
  std::array<std::vector<std::uint32_t>, kMaximumEdges + 1> by_edge_count_;
  std::vector<std::array<int, kColorCount>> actions_;
};

std::array<std::array<int, order23::kOrder>, order23::kOrder> read_record(
    const std::string& path) {
  std::ifstream input(path);
  if (!input) throw std::runtime_error("cannot open record matrix: " + path);
  std::array<std::array<int, order23::kOrder>, order23::kOrder> record{};
  std::string line;
  int row = 0;
  while (std::getline(input, line)) {
    int column = 0;
    for (const char symbol : line) {
      if (symbol != '+' && symbol != '-') continue;
      if (row >= order23::kOrder || column >= order23::kOrder)
        throw std::runtime_error("record matrix is too large");
      record[row][column++] = symbol == '+' ? 1 : -1;
    }
    if (column != 0) {
      if (column != order23::kOrder)
        throw std::runtime_error("record row has wrong length");
      ++row;
    }
  }
  if (row != order23::kOrder)
    throw std::runtime_error("record matrix has wrong number of rows");
  return record;
}

Gram gram_matrix(const std::string& path) {
  const auto record = read_record(path);
  Gram gram{};
  for (int row = 0; row < order23::kOrder; ++row) {
    for (int other = 0; other < order23::kOrder; ++other) {
      for (int column = 0; column < order23::kOrder; ++column)
        gram[row][other] += record[row][column] * record[other][column];
    }
  }
  return gram;
}

std::int64_t normalize(std::int64_t value, std::int64_t prime) {
  value %= prime;
  if (value < 0) value += prime;
  return value;
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

std::int64_t small_determinant_mod(
    std::array<std::array<std::int64_t, 10>, 10> matrix, int size,
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
      const std::int64_t multiplier = normalize(
          matrix[row][column] * inverse, prime);
      for (int other = column; other < size; ++other) {
        matrix[row][other] = normalize(
            matrix[row][other] - multiplier * matrix[column][other], prime);
      }
    }
  }
  return determinant;
}

class SquareSieve {
 public:
  SquareSieve(const ColoredComponents& components, const std::string& path)
      : components_(components), gram_(gram_matrix(path)) {
    initialize_bins();
    initialize_gram_data();
  }

  void evaluate(const std::array<std::uint32_t, kMaximumEdges>& component_ids,
                std::size_t component_count) {
    ++total_;
    const auto edit_indices = reconstruct(component_ids, component_count);
    std::array<int, 10> vertices{};
    int vertex_count = 0;
    for (const int edit_index : edit_indices) {
      vertices[vertex_count++] = edges_[edit_index].left;
      vertices[vertex_count++] = edges_[edit_index].right;
    }
    std::sort(vertices.begin(), vertices.begin() + vertex_count);
    const int size = static_cast<int>(
        std::unique(vertices.begin(), vertices.begin() + vertex_count) -
        vertices.begin());
    std::array<int, order23::kOrder> position{};
    position.fill(-1);
    for (int index = 0; index < size; ++index)
      position[vertices[index]] = index;
    std::array<std::array<std::int64_t, 10>, 10> perturbation{};
    for (const int edit_index : edit_indices) {
      const GramEdge& edge = edges_[edit_index];
      const std::int64_t delta = edge.value == -1 ? 4 : -4;
      const int left = position[edge.left];
      const int right = position[edge.right];
      perturbation[left][right] = delta;
      perturbation[right][left] = delta;
    }
    for (std::size_t prime_index = 0; prime_index < order23::kPrimes.size();
         ++prime_index) {
      const std::int64_t prime = order23::kPrimes[prime_index];
      std::array<std::array<std::int64_t, 10>, 10> update{};
      for (int row = 0; row < size; ++row) {
        for (int column = 0; column < size; ++column) {
          std::int64_t value = row == column ? order23::kScale : 0;
          for (int middle = 0; middle < size; ++middle) {
            value += order23::kInverseNumerator[vertices[row]][vertices[middle]] *
                     perturbation[middle][column];
          }
          update[row][column] = normalize(value, prime);
        }
      }
      const std::int64_t numerator =
          small_determinant_mod(update, size, prime);
      const std::int64_t square_test = normalize(
          numerator * mod_pow(order23::kScale, size, prime), prime);
      if (square_test != 0 &&
          mod_pow(square_test, (prime - 1) / 2, prime) == prime - 1) {
        ++witness_counts_[prime_index];
        return;
      }
    }
    survivors_.push_back(edit_indices);
  }

  std::uint64_t total() const { return total_; }
  const std::array<std::uint64_t, order23::kPrimes.size()>& witness_counts()
      const {
    return witness_counts_;
  }
  const std::vector<std::array<int, kMaximumEdges>>& survivors() const {
    return survivors_;
  }

 private:
  void initialize_bins() {
    bin_vertices_[0] = {0};
    bin_vertices_[1] = {7, 8};
    bin_vertices_[2] = {9, 10};
    bin_vertices_[3] = {1};
    bin_vertices_[4] = {3, 4};
    bin_vertices_[5] = {5, 6};
    bin_vertices_[6] = {2};
    bin_vertices_[7] = {11, 12};
    bin_vertices_[8] = {13, 14};
    bin_vertices_[9] = {15, 16, 17, 18};
    bin_vertices_[10] = {19, 20, 21, 22};
    for (int color = 0; color < kColorCount; ++color) {
      if (static_cast<int>(bin_vertices_[color].size()) != kCapacities[color])
        throw std::runtime_error("bin capacity mismatch");
    }
  }

  void initialize_gram_data() {
    int three_edges = 0;
    for (int left = 0; left < order23::kOrder; ++left) {
      if (gram_[left][left] != order23::kOrder)
        throw std::runtime_error("bad Gram diagonal");
      for (int right = 0; right < left; ++right) {
        const int value = gram_[left][right];
        if (value != -1 && value != 3)
          throw std::runtime_error("record Gram matrix is not graph-valued");
        edge_index_[left][right] = edge_index_[right][left] =
            static_cast<int>(edges_.size());
        edges_.push_back({left, right, value});
        three_edges += value == 3;
      }
    }
    if (edges_.size() != 253 || three_edges != 45)
      throw std::runtime_error("record Gram edge count mismatch");
    for (int row = 0; row < order23::kOrder; ++row) {
      for (int column = 0; column < order23::kOrder; ++column) {
        std::int64_t value = 0;
        for (int middle = 0; middle < order23::kOrder; ++middle) {
          value += static_cast<std::int64_t>(gram_[row][middle]) *
                   order23::kInverseNumerator[middle][column];
        }
        const std::int64_t expected =
            row == column ? order23::kScale : 0;
        if (value != expected)
          throw std::runtime_error("scaled inverse check failed");
      }
    }
    for (const std::int64_t prime : order23::kPrimes) {
      if (!is_prime(prime) || order23::kScale % prime == 0)
        throw std::runtime_error("invalid witness prime");
    }
  }

  std::array<int, kMaximumEdges> reconstruct(
      const std::array<std::uint32_t, kMaximumEdges>& component_ids,
      std::size_t component_count) const {
    std::array<int, kColorCount> next_slot{};
    std::array<int, kMaximumEdges> edit_indices{};
    int edit_count = 0;
    for (std::size_t component = 0; component < component_count; ++component) {
      const Variant& variant = components_.variants()[component_ids[component]];
      const Shape& shape = components_.shapes()[variant.shape_index];
      const auto colors = decode_colors(variant.color_code, shape.vertex_count);
      std::array<int, 6> actual_vertices{};
      for (int vertex = 0; vertex < shape.vertex_count; ++vertex) {
        const int color = colors[vertex];
        const int slot = next_slot[color]++;
        if (slot >= static_cast<int>(bin_vertices_[color].size()))
          throw std::runtime_error("component reconstruction exceeds bin");
        actual_vertices[vertex] = bin_vertices_[color][slot];
      }
      for (int left = 0; left < shape.vertex_count; ++left) {
        for (int right = 0; right < left; ++right) {
          if ((shape.graph_code >> pair_bit(left, right)) & 1U) {
            if (edit_count >= kMaximumEdges)
              throw std::runtime_error("too many reconstructed edges");
            edit_indices[edit_count++] =
                edge_index_[actual_vertices[left]][actual_vertices[right]];
          }
        }
      }
    }
    if (edit_count != kMaximumEdges)
      throw std::runtime_error("wrong reconstructed edge count");
    std::sort(edit_indices.begin(), edit_indices.end());
    if (std::adjacent_find(edit_indices.begin(), edit_indices.end()) !=
        edit_indices.end())
      throw std::runtime_error("duplicate reconstructed edge");
    return edit_indices;
  }

  const ColoredComponents& components_;
  Gram gram_{};
  std::array<std::vector<int>, kColorCount> bin_vertices_;
  std::array<std::array<int, order23::kOrder>, order23::kOrder> edge_index_{};
  std::vector<GramEdge> edges_;
  std::uint64_t total_ = 0;
  std::array<std::uint64_t, order23::kPrimes.size()> witness_counts_{};
  std::vector<std::array<int, kMaximumEdges>> survivors_;
};

void integer_partitions(int remaining, int maximum, std::vector<int>& prefix,
                        std::vector<std::vector<int>>& answer) {
  if (remaining == 0) {
    answer.push_back(prefix);
    return;
  }
  for (int part = std::min(remaining, maximum); part >= 1; --part) {
    prefix.push_back(part);
    integer_partitions(remaining - part, part, prefix, answer);
    prefix.pop_back();
  }
}

class OrbitEnumerator {
 public:
  explicit OrbitEnumerator(const ColoredComponents& components)
      : components_(components) {}

  std::uint64_t count(int edge_count, SquareSieve* sieve = nullptr) {
    if (edge_count == 0) return 1;
    accepted_ = 0;
    colored_ = 0;
    sieve_ = sieve;
    std::vector<std::vector<int>> partitions;
    std::vector<int> prefix;
    integer_partitions(edge_count, edge_count, prefix, partitions);
    for (const auto& partition : partitions) {
      partition_ = &partition;
      selected_.assign(partition.size(), 0);
      selected_offsets_.assign(partition.size(), 0);
      extend(0, 0);
    }
    std::cerr << "k=" << edge_count << ": " << colored_
              << " internally colored graphs, " << accepted_
              << " full symmetry classes\n";
    return accepted_;
  }

  std::uint64_t internally_colored_count() const { return colored_; }

 private:
  static void sort_prefix(
      std::array<std::uint32_t, kMaximumEdges>& values, std::size_t size) {
    if (size > values.size()) throw std::runtime_error("oversized partition");
    for (std::size_t index = 1; index < size; ++index) {
      const std::uint32_t value = values[index];
      std::size_t position = index;
      while (position > 0 && value < values[position - 1]) {
        values[position] = values[position - 1];
        --position;
      }
      values[position] = value;
    }
  }

  bool outer_canonical(
      const std::array<std::uint32_t, kMaximumEdges>& original) const {
    for (int action = 1; action < 12; ++action) {
      std::array<std::uint32_t, kMaximumEdges> image{};
      for (std::size_t index = 0; index < selected_.size(); ++index) {
        image[index] = components_.variants()[selected_[index]]
                           .outer_images[action];
      }
      sort_prefix(image, selected_.size());
      if (std::lexicographical_compare(
              image.begin(), image.begin() + selected_.size(), original.begin(),
              original.begin() + selected_.size()))
        return false;
    }
    return true;
  }

  void extend(std::size_t position, std::uint64_t used) {
    if (position == partition_->size()) {
      ++colored_;
      std::array<std::uint32_t, kMaximumEdges> canonical_components{};
      std::copy(selected_.begin(), selected_.end(),
                canonical_components.begin());
      sort_prefix(canonical_components, selected_.size());
      if (outer_canonical(canonical_components)) {
        ++accepted_;
        if (sieve_ != nullptr)
          sieve_->evaluate(canonical_components, selected_.size());
      }
      return;
    }
    const int edge_count = (*partition_)[position];
    const auto& choices = components_.variants_with_edges(edge_count);
    std::size_t start = 0;
    if (position > 0 && (*partition_)[position - 1] == edge_count)
      start = selected_offsets_[position - 1];
    for (std::size_t offset = start; offset < choices.size(); ++offset) {
      const std::uint32_t choice = choices[offset];
      const std::uint64_t addition = components_.variants()[choice].occupancy;
      if (!occupancy_fits(used, addition)) continue;
      selected_[position] = choice;
      selected_offsets_[position] = offset;
      extend(position + 1, used + addition);
    }
  }

  const ColoredComponents& components_;
  const std::vector<int>* partition_ = nullptr;
  std::vector<std::uint32_t> selected_;
  std::vector<std::size_t> selected_offsets_;
  std::uint64_t colored_ = 0;
  std::uint64_t accepted_ = 0;
  SquareSieve* sieve_ = nullptr;
};

}  // namespace

int main(int argc, char** argv) {
  try {
    if (argc > 2)
      throw std::runtime_error("usage: radius5 [record23.txt]");
    const std::string record_path = argc == 2 ? argv[1] : "record23.txt";
    const ColoredComponents components(generate_shapes());
    std::cerr << components.shapes().size() << " connected shapes, "
              << components.variants().size() << " colored variants\n";
    SquareSieve sieve(components, record_path);
    OrbitEnumerator enumerator(components);
    std::array<std::uint64_t, kMaximumEdges + 1> orbit_counts{};
    std::array<std::uint64_t, kMaximumEdges + 1> internally_colored_counts{};
    internally_colored_counts[0] = 1;
    for (int edge_count = 0; edge_count <= kMaximumEdges; ++edge_count) {
      orbit_counts[edge_count] = enumerator.count(
          edge_count, edge_count == kMaximumEdges ? &sieve : nullptr);
      if (edge_count != 0)
        internally_colored_counts[edge_count] =
            enumerator.internally_colored_count();
      if (orbit_counts[edge_count] != kExpectedOrbits[edge_count])
        throw std::runtime_error("orbit count disagrees with Burnside result");
      if (internally_colored_counts[edge_count] !=
          kExpectedInternallyColored[edge_count])
        throw std::runtime_error("internal colored-graph count mismatch");
    }
    if (sieve.total() != orbit_counts[kMaximumEdges])
      throw std::runtime_error("sieve coverage mismatch");
    const std::uint64_t rejected = std::accumulate(
        sieve.witness_counts().begin(), sieve.witness_counts().end(),
        UINT64_C(0));
    if (rejected + sieve.survivors().size() != sieve.total())
      throw std::runtime_error("sieve accounting mismatch");
    if (sieve.witness_counts() != kExpectedRadius5WitnessCounts ||
        sieve.survivors().size() != 27)
      throw std::runtime_error("radius-five sieve disagrees with certificate");

    std::cout << "{\n  \"order\": 23,\n  \"witness_primes\": [";
    for (std::size_t index = 0; index < order23::kPrimes.size(); ++index) {
      if (index != 0) std::cout << ", ";
      std::cout << order23::kPrimes[index];
    }
    std::cout << "],\n"
              << "  \"connected_unlabeled_shapes\": 22,\n"
              << "  \"colored_connected_variants\": "
              << components.variants().size()
              << ",\n  \"internally_colored_graph_counts\": [";
    for (std::size_t index = 0; index < internally_colored_counts.size();
         ++index) {
      if (index != 0) std::cout << ", ";
      std::cout << internally_colored_counts[index];
    }
    std::cout << "],\n  \"canonical_orbit_counts\": [";
    for (std::size_t index = 0; index < orbit_counts.size(); ++index) {
      if (index != 0) std::cout << ", ";
      std::cout << orbit_counts[index];
    }
    std::cout << "],\n  \"radius_five\": {\n"
              << "    \"symmetry_classes\": " << sieve.total() << ",\n"
              << "    \"witness_counts\": [";
    for (std::size_t index = 0; index < sieve.witness_counts().size();
         ++index) {
      if (index != 0) std::cout << ", ";
      std::cout << sieve.witness_counts()[index];
    }
    std::cout << "],\n    \"survives_48_nonsquare_tests\": "
              << sieve.survivors().size()
              << ",\n    \"survivor_edge_indices\": [";
    for (std::size_t survivor = 0; survivor < sieve.survivors().size();
         ++survivor) {
      if (survivor != 0) std::cout << ", ";
      std::cout << '[';
      for (int edge = 0; edge < kMaximumEdges; ++edge) {
        if (edge != 0) std::cout << ", ";
        std::cout << sieve.survivors()[survivor][edge];
      }
      std::cout << ']';
    }
    std::cout << "]\n  }\n}\n";
    std::cerr << "radius-five canonical orbit enumeration and modular sieve "
                 "verified\n";
    return 0;
  } catch (const std::exception& error) {
    std::cerr << "error: " << error.what() << '\n';
    return 1;
  }
}
