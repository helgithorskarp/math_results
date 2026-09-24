// Exact radius-six extension of radius5.cpp.
//
// The radius-five implementation is included (with its entry point renamed)
// so this file reuses the audited Gram, inverse, component, and quotient
// primitives without maintaining a second copy.  Connected components with
// at most five edges use its stored catalogue.  A connected six-edge
// component is deliberately streamed shape by shape, keeping memory bounded.
#if defined(__GNUC__)
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Warray-bounds"
#endif
#define main radius5_embedded_main
#include "radius5.cpp"
#undef main
#if defined(__GNUC__)
#pragma GCC diagnostic pop
#endif

#include <chrono>
#include <limits>

namespace {

constexpr int kRadius6 = 6;
constexpr std::uint64_t kExpectedRadius6Orbits = UINT64_C(81094402);
constexpr std::uint64_t kExpectedRadius6InternallyColored = UINT64_C(888540494);
constexpr std::uint64_t kExpectedConnectedInternallyColored = UINT64_C(43702833);
constexpr std::uint64_t kExpectedConnectedOrbits = UINT64_C(4361518);
constexpr std::uint64_t kExpectedDisconnectedInternallyColored =
    UINT64_C(844837661);
constexpr std::uint64_t kExpectedDisconnectedOrbits = UINT64_C(76732884);
constexpr std::array<std::uint64_t, 48> kExpectedRadius6WitnessCounts = {
    40543321, 20275304, 10136653, 5068257, 2534288, 1267587,
    635409,   315794,   158803,   79487,   39455,   19665,
    9999,     4998,     2558,     1159,    642,     330,
    167,      87,       51,       15,       9,       1,
    1,        2,        1,        0,        0,       0,
    0,        0,        0,        0,        0,       0,
    0,        0,        0,        0,        0,       0,
    0,        0,        0,        0,        0,       0,
};
constexpr std::size_t kExpectedRadius6Survivors = 359;

using EditSet6 = std::array<int, kRadius6>;

struct Shape6 {
  int vertex_count;
  std::uint32_t graph_code;
  std::vector<std::vector<int>> automorphisms;
};

std::uint32_t permute_graph6(std::uint32_t graph, int vertex_count,
                             const std::vector<int>& permutation) {
  std::uint32_t image = 0;
  for (int left = 0; left < vertex_count; ++left) {
    for (int right = 0; right < left; ++right) {
      if ((graph >> pair_bit(left, right)) & 1U) {
        image |= UINT32_C(1)
                 << pair_bit(permutation[left], permutation[right]);
      }
    }
  }
  return image;
}

std::uint32_t canonical_graph6(std::uint32_t graph, int vertex_count) {
  std::uint32_t canonical = graph;
  for (const auto& permutation : permutations(vertex_count))
    canonical =
        std::min(canonical, permute_graph6(graph, vertex_count, permutation));
  return canonical;
}

std::vector<Shape6> generate_shapes6(const std::vector<Shape>& smaller) {
  // Every connected six-edge graph is obtained from a connected five-edge
  // graph either by adding a missing edge, or by adjoining one leaf.  For a
  // cyclic graph remove a cycle edge; for a tree remove a leaf edge and its
  // isolated endpoint.  This is a complete canonical augmentation.
  std::array<std::set<std::uint32_t>, 8> by_vertex_count;
  for (const Shape& shape : smaller) {
    if (shape.edge_count != 5) continue;
    const int size = shape.vertex_count;
    for (int left = 0; left < size; ++left) {
      for (int right = 0; right < left; ++right) {
        const std::uint32_t bit = UINT32_C(1) << pair_bit(left, right);
        if ((static_cast<std::uint32_t>(shape.graph_code) & bit) != 0) continue;
        const std::uint32_t graph =
            static_cast<std::uint32_t>(shape.graph_code) | bit;
        by_vertex_count[size].insert(canonical_graph6(graph, size));
      }
    }
    if (size < 7) {
      for (int neighbor = 0; neighbor < size; ++neighbor) {
        const std::uint32_t graph =
            static_cast<std::uint32_t>(shape.graph_code) |
            (UINT32_C(1) << pair_bit(size, neighbor));
        by_vertex_count[size + 1].insert(canonical_graph6(graph, size + 1));
      }
    }
  }

  std::vector<Shape6> answer;
  for (int size = 2; size <= 7; ++size) {
    const auto vertex_permutations = permutations(size);
    for (const std::uint32_t graph : by_vertex_count[size]) {
      if (std::popcount(graph) != kRadius6)
        throw std::runtime_error("bad six-edge shape");
      Shape6 shape{size, graph, {}};
      for (const auto& permutation : vertex_permutations) {
        if (permute_graph6(graph, size, permutation) == graph)
          shape.automorphisms.push_back(permutation);
      }
      answer.push_back(std::move(shape));
    }
  }
  return answer;
}

std::uint32_t encode_colors6(const std::array<int, 7>& colors,
                             int vertex_count) {
  std::uint32_t code = 0;
  std::uint32_t multiplier = 1;
  for (int vertex = 0; vertex < vertex_count; ++vertex) {
    code += static_cast<std::uint32_t>(colors[vertex]) * multiplier;
    multiplier *= kColorCount;
  }
  return code;
}

std::array<int, 7> decode_colors6(std::uint32_t code, int vertex_count) {
  std::array<int, 7> colors{};
  for (int vertex = 0; vertex < vertex_count; ++vertex) {
    colors[vertex] = static_cast<int>(code % kColorCount);
    code /= kColorCount;
  }
  return colors;
}

std::uint32_t permute_colors6(const std::array<int, 7>& colors,
                              int vertex_count,
                              const std::vector<int>& permutation) {
  std::array<int, 7> image{};
  for (int vertex = 0; vertex < vertex_count; ++vertex)
    image[permutation[vertex]] = colors[vertex];
  return encode_colors6(image, vertex_count);
}

std::uint32_t canonical_color_code6(const Shape6& shape,
                                    const std::array<int, 7>& colors) {
  std::uint32_t canonical = encode_colors6(colors, shape.vertex_count);
  for (const auto& automorphism : shape.automorphisms) {
    canonical = std::min(
        canonical,
        permute_colors6(colors, shape.vertex_count, automorphism));
  }
  return canonical;
}

std::uint64_t pack_occupancy6(const std::array<int, 7>& colors,
                              int vertex_count) {
  std::uint64_t packed = 0;
  for (int vertex = 0; vertex < vertex_count; ++vertex)
    packed += UINT64_C(1) << (4 * colors[vertex]);
  return packed;
}

bool valid_colors6(const std::array<int, 7>& colors, int vertex_count) {
  const std::uint64_t packed = pack_occupancy6(colors, vertex_count);
  for (int color = 0; color < kColorCount; ++color) {
    if (occupancy(packed, color) > kCapacities[color]) return false;
  }
  return true;
}

std::int64_t small_determinant_mod6(
    std::array<std::array<std::int64_t, 12>, 12> matrix, int size,
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
      const std::int64_t multiplier =
          normalize(matrix[row][column] * inverse, prime);
      for (int other = column; other < size; ++other) {
        matrix[row][other] = normalize(
            matrix[row][other] - multiplier * matrix[column][other], prime);
      }
    }
  }
  return determinant;
}

class SquareSieve6 {
 public:
  SquareSieve6(const ColoredComponents& components, const std::string& path)
      : components_(components), gram_(gram_matrix(path)),
        start_(std::chrono::steady_clock::now()) {
    initialize_bins();
    initialize_gram_data();
  }

  void evaluate_components(const std::array<std::uint32_t, kRadius6>& ids,
                           std::size_t component_count) {
    std::array<int, kColorCount> next_slot{};
    EditSet6 edits{};
    int edit_count = 0;
    for (std::size_t component = 0; component < component_count; ++component) {
      const Variant& variant = components_.variants()[ids[component]];
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
            if (edit_count >= kRadius6)
              throw std::runtime_error("too many reconstructed edges");
            edits[edit_count++] =
                edge_index_[actual_vertices[left]][actual_vertices[right]];
          }
        }
      }
    }
    finish_reconstruction(edits, edit_count);
    evaluate(edits);
  }

  void evaluate_connected(const Shape6& shape,
                          const std::array<int, 7>& colors) {
    std::array<int, kColorCount> next_slot{};
    std::array<int, 7> actual_vertices{};
    for (int vertex = 0; vertex < shape.vertex_count; ++vertex) {
      const int color = colors[vertex];
      const int slot = next_slot[color]++;
      if (slot >= static_cast<int>(bin_vertices_[color].size()))
        throw std::runtime_error("connected reconstruction exceeds bin");
      actual_vertices[vertex] = bin_vertices_[color][slot];
    }
    EditSet6 edits{};
    int edit_count = 0;
    for (int left = 0; left < shape.vertex_count; ++left) {
      for (int right = 0; right < left; ++right) {
        if ((shape.graph_code >> pair_bit(left, right)) & 1U) {
          edits[edit_count++] =
              edge_index_[actual_vertices[left]][actual_vertices[right]];
        }
      }
    }
    finish_reconstruction(edits, edit_count);
    evaluate(edits);
  }

  std::uint64_t total() const { return total_; }
  const std::array<std::uint64_t, order23::kPrimes.size()>& witness_counts()
      const {
    return witness_counts_;
  }
  std::vector<EditSet6>& survivors() { return survivors_; }
  const std::vector<EditSet6>& survivors() const { return survivors_; }

 private:
  static void finish_reconstruction(EditSet6& edits, int edit_count) {
    if (edit_count != kRadius6)
      throw std::runtime_error("wrong reconstructed edge count");
    std::sort(edits.begin(), edits.end());
    if (std::adjacent_find(edits.begin(), edits.end()) != edits.end())
      throw std::runtime_error("duplicate reconstructed edge");
  }

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
        const std::int64_t expected = row == column ? order23::kScale : 0;
        if (value != expected)
          throw std::runtime_error("scaled inverse check failed");
      }
    }
    for (const std::int64_t prime : order23::kPrimes) {
      if (!is_prime(prime) || order23::kScale % prime == 0)
        throw std::runtime_error("invalid witness prime");
    }
  }

  void evaluate(const EditSet6& edits) {
    ++total_;
    if (total_ % UINT64_C(10000000) == 0) {
      const double elapsed = std::chrono::duration<double>(
                                 std::chrono::steady_clock::now() - start_)
                                 .count();
      std::cerr << "sieve: " << total_ << " classes in " << elapsed
                << " seconds\n";
    }
    std::array<int, 12> vertices{};
    int vertex_count = 0;
    for (const int edit_index : edits) {
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
    std::array<std::array<std::int64_t, 12>, 12> perturbation{};
    for (const int edit_index : edits) {
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
      std::array<std::array<std::int64_t, 12>, 12> update{};
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
          small_determinant_mod6(update, size, prime);
      const std::int64_t square_test = normalize(
          numerator * mod_pow(order23::kScale, size, prime), prime);
      if (square_test != 0 &&
          mod_pow(square_test, (prime - 1) / 2, prime) == prime - 1) {
        ++witness_counts_[prime_index];
        return;
      }
    }
    survivors_.push_back(edits);
  }

  const ColoredComponents& components_;
  Gram gram_{};
  std::array<std::vector<int>, kColorCount> bin_vertices_;
  std::array<std::array<int, order23::kOrder>, order23::kOrder> edge_index_{};
  std::vector<GramEdge> edges_;
  std::uint64_t total_ = 0;
  std::array<std::uint64_t, order23::kPrimes.size()> witness_counts_{};
  std::vector<EditSet6> survivors_;
  std::chrono::steady_clock::time_point start_;
};

class DisconnectedEnumerator6 {
 public:
  explicit DisconnectedEnumerator6(const ColoredComponents& components)
      : components_(components) {}

  void run(SquareSieve6& sieve) {
    sieve_ = &sieve;
    std::vector<std::vector<int>> partitions;
    std::vector<int> prefix;
    integer_partitions(kRadius6, kRadius6, prefix, partitions);
    for (const auto& partition : partitions) {
      if (partition.size() == 1) continue;  // streamed separately
      partition_ = &partition;
      selected_.assign(partition.size(), 0);
      selected_offsets_.assign(partition.size(), 0);
      extend(0, 0);
    }
  }

  std::uint64_t internally_colored() const { return colored_; }
  std::uint64_t accepted() const { return accepted_; }

 private:
  static void sort_prefix(std::array<std::uint32_t, kRadius6>& values,
                          std::size_t size) {
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
      const std::array<std::uint32_t, kRadius6>& original) const {
    for (int action = 1; action < 12; ++action) {
      std::array<std::uint32_t, kRadius6> image{};
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
      std::array<std::uint32_t, kRadius6> canonical_components{};
      std::copy(selected_.begin(), selected_.end(),
                canonical_components.begin());
      sort_prefix(canonical_components, selected_.size());
      if (outer_canonical(canonical_components)) {
        ++accepted_;
        sieve_->evaluate_components(canonical_components, selected_.size());
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
  SquareSieve6* sieve_ = nullptr;
};

struct ConnectedCounts6 {
  std::uint64_t internally_colored = 0;
  std::uint64_t accepted = 0;
};

[[maybe_unused]] ConnectedCounts6 stream_connected6(
    const std::vector<Shape6>& shapes, SquareSieve6& sieve) {
  const auto actions = outer_color_actions();
  ConnectedCounts6 counts;
  std::uint32_t power11 = 1;
  for (int exponent = 0; exponent < 7; ++exponent) power11 *= kColorCount;
  for (std::size_t shape_index = 0; shape_index < shapes.size();
       ++shape_index) {
    const Shape6& shape = shapes[shape_index];
    std::uint32_t code_count = 1;
    for (int exponent = 0; exponent < shape.vertex_count; ++exponent)
      code_count *= kColorCount;
    if (code_count > power11) throw std::runtime_error("bad color-code bound");
    std::vector<std::uint8_t> visited(code_count, 0);
    std::uint64_t shape_colored = 0;
    std::uint64_t shape_accepted = 0;
    for (std::uint32_t code = 0; code < code_count; ++code) {
      if (visited[code]) continue;
      const auto colors = decode_colors6(code, shape.vertex_count);
      for (const auto& automorphism : shape.automorphisms) {
        visited[permute_colors6(colors, shape.vertex_count, automorphism)] = 1;
      }
      if (!valid_colors6(colors, shape.vertex_count)) continue;
      if (canonical_color_code6(shape, colors) != code)
        throw std::runtime_error("noncanonical streamed color orbit");
      ++shape_colored;
      bool canonical = true;
      for (std::size_t action = 1; action < actions.size(); ++action) {
        std::array<int, 7> transformed{};
        for (int vertex = 0; vertex < shape.vertex_count; ++vertex)
          transformed[vertex] = actions[action][colors[vertex]];
        if (canonical_color_code6(shape, transformed) < code) {
          canonical = false;
          break;
        }
      }
      if (canonical) {
        ++shape_accepted;
        sieve.evaluate_connected(shape, colors);
      }
    }
    counts.internally_colored += shape_colored;
    counts.accepted += shape_accepted;
    std::cerr << "connected shape " << (shape_index + 1) << '/' << shapes.size()
              << " (v=" << shape.vertex_count << "): " << shape_colored
              << " internal, " << shape_accepted << " full classes\n";
  }
  return counts;
}

}  // namespace

#ifndef RADIUS6_NO_MAIN
int main(int argc, char** argv) {
  try {
    if (argc > 2)
      throw std::runtime_error("usage: radius6 [record23.txt]");
    const std::string record_path = argc == 2 ? argv[1] : "record23.txt";
    const ColoredComponents components(generate_shapes());
    const std::vector<Shape6> shapes6 = generate_shapes6(components.shapes());
    std::array<std::uint64_t, 8> shapes_by_vertices{};
    for (const Shape6& shape : shapes6) ++shapes_by_vertices[shape.vertex_count];
    std::cerr << components.shapes().size() << " stored connected shapes, "
              << components.variants().size() << " stored colored variants; "
              << shapes6.size() << " streamed six-edge shapes\n";

    SquareSieve6 sieve(components, record_path);
    const ConnectedCounts6 connected = stream_connected6(shapes6, sieve);
    DisconnectedEnumerator6 disconnected(components);
    disconnected.run(sieve);
    const std::uint64_t internally_colored =
        connected.internally_colored + disconnected.internally_colored();
    const std::uint64_t accepted = connected.accepted + disconnected.accepted();
    std::cerr << "k=6: " << internally_colored
              << " internally colored graphs, " << accepted
              << " full symmetry classes\n";
    if (accepted != kExpectedRadius6Orbits || sieve.total() != accepted)
      throw std::runtime_error("radius-six count disagrees with Burnside result");
    if (internally_colored != kExpectedRadius6InternallyColored ||
        connected.internally_colored !=
            kExpectedConnectedInternallyColored ||
        connected.accepted != kExpectedConnectedOrbits ||
        disconnected.internally_colored() !=
            kExpectedDisconnectedInternallyColored ||
        disconnected.accepted() != kExpectedDisconnectedOrbits)
      throw std::runtime_error("radius-six component census mismatch");
    const std::uint64_t rejected = std::accumulate(
        sieve.witness_counts().begin(), sieve.witness_counts().end(),
        UINT64_C(0));
    if (rejected + sieve.survivors().size() != sieve.total())
      throw std::runtime_error("radius-six sieve accounting mismatch");
    if (sieve.witness_counts() != kExpectedRadius6WitnessCounts ||
        sieve.survivors().size() != kExpectedRadius6Survivors)
      throw std::runtime_error("radius-six sieve disagrees with certificate");
    std::sort(sieve.survivors().begin(), sieve.survivors().end());

    std::cout << "{\n  \"order\": 23,\n  \"witness_primes\": [";
    for (std::size_t index = 0; index < order23::kPrimes.size(); ++index) {
      if (index != 0) std::cout << ", ";
      std::cout << order23::kPrimes[index];
    }
    std::cout << "],\n  \"stored_connected_shapes_through_five\": "
              << components.shapes().size()
              << ",\n  \"stored_colored_connected_variants_through_five\": "
              << components.variants().size()
              << ",\n  \"connected_six_edge_shapes\": " << shapes6.size()
              << ",\n  \"connected_six_edge_shapes_by_vertex_count\": [";
    for (std::size_t index = 0; index < shapes_by_vertices.size(); ++index) {
      if (index != 0) std::cout << ", ";
      std::cout << shapes_by_vertices[index];
    }
    std::cout << "],\n  \"radius_six\": {\n"
              << "    \"internally_colored_graphs\": " << internally_colored
              << ",\n    \"connected_internally_colored_graphs\": "
              << connected.internally_colored
              << ",\n    \"connected_symmetry_classes\": "
              << connected.accepted
              << ",\n    \"disconnected_internally_colored_graphs\": "
              << disconnected.internally_colored()
              << ",\n    \"disconnected_symmetry_classes\": "
              << disconnected.accepted()
              << ",\n    \"symmetry_classes\": " << sieve.total()
              << ",\n    \"witness_counts\": [";
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
      for (int edge = 0; edge < kRadius6; ++edge) {
        if (edge != 0) std::cout << ", ";
        std::cout << sieve.survivors()[survivor][edge];
      }
      std::cout << ']';
    }
    std::cout << "]\n  }\n}\n";
    std::cerr << "radius-six canonical orbit enumeration and modular sieve "
                 "verified\n";
    return 0;
  } catch (const std::exception& error) {
    std::cerr << "error: " << error.what() << '\n';
    return 1;
  }
}
#endif
