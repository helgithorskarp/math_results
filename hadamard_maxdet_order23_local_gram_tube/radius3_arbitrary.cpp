// Exact covering search for all three-position legal Gram edits.
//
// The underlying three-edge edit sets are quotiented by Aut(G0).  For each
// of the 8,887 canonical representatives, all 10^3 assignments of alternative
// legal Gram values are tested.  Stabilizers may identify some assignments,
// but no assignment is omitted; the 8,887,000 tests are a symmetry-normalized
// cover rather than a claim of being the exact orbit count for valued edits.
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

namespace {

constexpr int kArbitraryRadius = 3;
constexpr std::uint64_t kExpectedUnderlyingOrbits = UINT64_C(8887);
constexpr std::uint64_t kExpectedInternallyColored3 = UINT64_C(73707);
constexpr std::uint64_t kExpectedAssignments = UINT64_C(8887000);
constexpr std::uint64_t kExpectedSurvivors = UINT64_C(4825);
constexpr std::array<std::uint64_t, order23::kPrimes.size()>
    kExpectedWitnessCounts = {
        4438897, 2221693, 1112675, 555172, 276468, 138696,
        69501,   34412,   17433,   8578,   4252,   2177,
        1100,    557,     285,     118,    82,     40,
        22,      11,      5,       1,      0,      0,
        0,       0,       0,       0,      0,      0,
        0,       0,       0,       0,      0,      0,
        0,       0,       0,       0,      0,      0,
        0,       0,       0,       0,      0,      0,
    };
constexpr std::array<int, 11> kLegalValues = {
    -21, -17, -13, -9, -5, -1, 3, 7, 11, 15, 19,
};

struct ArbitrarySurvivor3 {
  std::array<int, kArbitraryRadius> edges{};
  std::array<int, kArbitraryRadius> values{};
};

std::int64_t small_determinant_mod3(
    std::array<std::array<std::int64_t, 6>, 6> matrix, int size,
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

class ArbitrarySieve3 {
 public:
  ArbitrarySieve3(const ColoredComponents& components, const std::string& path)
      : components_(components), gram_(gram_matrix(path)),
        start_(std::chrono::steady_clock::now()) {
    initialize_bins();
    initialize_gram_data();
  }

  void evaluate_components(
      const std::array<std::uint32_t, kArbitraryRadius>& component_ids,
      std::size_t component_count) {
    const auto edit_indices = reconstruct(component_ids, component_count);
    ++underlying_representatives_;
    std::array<int, kArbitraryRadius> values{};
    assign_values(edit_indices, values, 0);
  }

  std::uint64_t underlying_representatives() const {
    return underlying_representatives_;
  }
  std::uint64_t total() const { return total_; }
  const std::array<std::uint64_t, order23::kPrimes.size()>& witness_counts()
      const {
    return witness_counts_;
  }
  std::vector<ArbitrarySurvivor3>& survivors() { return survivors_; }
  const std::vector<ArbitrarySurvivor3>& survivors() const {
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

  std::array<int, kArbitraryRadius> reconstruct(
      const std::array<std::uint32_t, kArbitraryRadius>& component_ids,
      std::size_t component_count) const {
    std::array<int, kColorCount> next_slot{};
    std::array<int, kArbitraryRadius> edit_indices{};
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
            if (edit_count >= kArbitraryRadius)
              throw std::runtime_error("too many reconstructed edges");
            edit_indices[edit_count++] =
                edge_index_[actual_vertices[left]][actual_vertices[right]];
          }
        }
      }
    }
    if (edit_count != kArbitraryRadius)
      throw std::runtime_error("wrong reconstructed edge count");
    std::sort(edit_indices.begin(), edit_indices.end());
    if (std::adjacent_find(edit_indices.begin(), edit_indices.end()) !=
        edit_indices.end())
      throw std::runtime_error("duplicate reconstructed edge");
    return edit_indices;
  }

  void assign_values(const std::array<int, kArbitraryRadius>& edit_indices,
                     std::array<int, kArbitraryRadius>& values,
                     int position) {
    if (position == kArbitraryRadius) {
      evaluate(edit_indices, values);
      return;
    }
    const int original = edges_[edit_indices[position]].value;
    for (const int value : kLegalValues) {
      if (value == original) continue;
      values[position] = value;
      assign_values(edit_indices, values, position + 1);
    }
  }

  void evaluate(const std::array<int, kArbitraryRadius>& edit_indices,
                const std::array<int, kArbitraryRadius>& values) {
    ++total_;
    if (total_ % UINT64_C(2000000) == 0) {
      const double elapsed = std::chrono::duration<double>(
                                 std::chrono::steady_clock::now() - start_)
                                 .count();
      std::cerr << "sieve: " << total_ << " assignments in " << elapsed
                << " seconds\n";
    }
    std::array<int, 6> vertices{};
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
    std::array<std::array<std::int64_t, 6>, 6> perturbation{};
    for (int edit = 0; edit < kArbitraryRadius; ++edit) {
      const GramEdge& edge = edges_[edit_indices[edit]];
      const std::int64_t delta = values[edit] - edge.value;
      const int left = position[edge.left];
      const int right = position[edge.right];
      perturbation[left][right] = delta;
      perturbation[right][left] = delta;
    }
    for (std::size_t prime_index = 0; prime_index < order23::kPrimes.size();
         ++prime_index) {
      const std::int64_t prime = order23::kPrimes[prime_index];
      std::array<std::array<std::int64_t, 6>, 6> update{};
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
          small_determinant_mod3(update, size, prime);
      const std::int64_t square_test = normalize(
          numerator * mod_pow(order23::kScale, size, prime), prime);
      if (square_test != 0 &&
          mod_pow(square_test, (prime - 1) / 2, prime) == prime - 1) {
        ++witness_counts_[prime_index];
        return;
      }
    }
    survivors_.push_back({edit_indices, values});
  }

  const ColoredComponents& components_;
  Gram gram_{};
  std::array<std::vector<int>, kColorCount> bin_vertices_;
  std::array<std::array<int, order23::kOrder>, order23::kOrder> edge_index_{};
  std::vector<GramEdge> edges_;
  std::uint64_t underlying_representatives_ = 0;
  std::uint64_t total_ = 0;
  std::array<std::uint64_t, order23::kPrimes.size()> witness_counts_{};
  std::vector<ArbitrarySurvivor3> survivors_;
  std::chrono::steady_clock::time_point start_;
};

class UnderlyingOrbitEnumerator3 {
 public:
  UnderlyingOrbitEnumerator3(const ColoredComponents& components,
                             ArbitrarySieve3& sieve)
      : components_(components), sieve_(sieve) {}

  void run() {
    std::vector<std::vector<int>> partitions;
    std::vector<int> prefix;
    integer_partitions(kArbitraryRadius, kArbitraryRadius, prefix, partitions);
    for (const auto& partition : partitions) {
      partition_ = &partition;
      selected_.assign(partition.size(), 0);
      selected_offsets_.assign(partition.size(), 0);
      extend(0, 0);
    }
  }

  std::uint64_t internally_colored() const { return colored_; }
  std::uint64_t accepted() const { return accepted_; }

 private:
  static void sort_prefix(
      std::array<std::uint32_t, kArbitraryRadius>& values, std::size_t size) {
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
      const std::array<std::uint32_t, kArbitraryRadius>& original) const {
    for (int action = 1; action < 12; ++action) {
      std::array<std::uint32_t, kArbitraryRadius> image{};
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
      std::array<std::uint32_t, kArbitraryRadius> canonical_components{};
      std::copy(selected_.begin(), selected_.end(),
                canonical_components.begin());
      sort_prefix(canonical_components, selected_.size());
      if (outer_canonical(canonical_components)) {
        ++accepted_;
        sieve_.evaluate_components(canonical_components, selected_.size());
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
  ArbitrarySieve3& sieve_;
  const std::vector<int>* partition_ = nullptr;
  std::vector<std::uint32_t> selected_;
  std::vector<std::size_t> selected_offsets_;
  std::uint64_t colored_ = 0;
  std::uint64_t accepted_ = 0;
};

}  // namespace

int main(int argc, char** argv) {
  try {
    if (argc > 2)
      throw std::runtime_error("usage: radius3_arbitrary [record23.txt]");
    const std::string record_path = argc == 2 ? argv[1] : "record23.txt";
    auto shapes = generate_shapes();
    shapes.erase(
        std::remove_if(shapes.begin(), shapes.end(), [](const Shape& shape) {
          return shape.edge_count > kArbitraryRadius;
        }),
        shapes.end());
    const ColoredComponents components(std::move(shapes));
    std::cerr << components.shapes().size() << " connected shapes, "
              << components.variants().size() << " colored variants\n";

    ArbitrarySieve3 sieve(components, record_path);
    UnderlyingOrbitEnumerator3 enumerator(components, sieve);
    enumerator.run();
    std::cerr << "k=3: " << enumerator.internally_colored()
              << " internally colored graphs, " << enumerator.accepted()
              << " underlying symmetry classes\n";
    if (enumerator.internally_colored() != kExpectedInternallyColored3 ||
        enumerator.accepted() != kExpectedUnderlyingOrbits ||
        sieve.underlying_representatives() != kExpectedUnderlyingOrbits ||
        sieve.total() != kExpectedAssignments)
      throw std::runtime_error("arbitrary radius-three coverage mismatch");
    const std::uint64_t rejected = std::accumulate(
        sieve.witness_counts().begin(), sieve.witness_counts().end(),
        UINT64_C(0));
    if (rejected + sieve.survivors().size() != sieve.total())
      throw std::runtime_error("arbitrary radius-three sieve accounting mismatch");
    if (sieve.witness_counts() != kExpectedWitnessCounts ||
        sieve.survivors().size() != kExpectedSurvivors)
      throw std::runtime_error("arbitrary radius-three output mismatch");
    std::sort(sieve.survivors().begin(), sieve.survivors().end(),
              [](const ArbitrarySurvivor3& left,
                 const ArbitrarySurvivor3& right) {
                if (left.edges != right.edges) return left.edges < right.edges;
                return left.values < right.values;
              });

    std::cout << "{\n  \"order\": 23,\n  \"witness_primes\": [";
    for (std::size_t index = 0; index < order23::kPrimes.size(); ++index) {
      if (index != 0) std::cout << ", ";
      std::cout << order23::kPrimes[index];
    }
    std::cout << "],\n  \"connected_shapes_through_three\": "
              << components.shapes().size()
              << ",\n  \"colored_connected_variants_through_three\": "
              << components.variants().size()
              << ",\n  \"internally_colored_underlying_graphs\": "
              << enumerator.internally_colored()
              << ",\n  \"underlying_edit_set_orbits\": "
              << enumerator.accepted()
              << ",\n  \"value_assignments_per_representative\": 1000,\n"
              << "  \"covered_labeled_matrices\": 2667126000,\n"
              << "  \"normalized_cover_evaluations\": " << sieve.total()
              << ",\n  \"witness_counts\": [";
    for (std::size_t index = 0; index < sieve.witness_counts().size();
         ++index) {
      if (index != 0) std::cout << ", ";
      std::cout << sieve.witness_counts()[index];
    }
    std::cout << "],\n  \"survives_48_nonsquare_tests\": "
              << sieve.survivors().size()
              << ",\n  \"survivor_edits\": [";
    for (std::size_t survivor = 0; survivor < sieve.survivors().size();
         ++survivor) {
      if (survivor != 0) std::cout << ", ";
      std::cout << '[';
      for (int edit = 0; edit < kArbitraryRadius; ++edit) {
        if (edit != 0) std::cout << ", ";
        std::cout << '[' << sieve.survivors()[survivor].edges[edit] << ", "
                  << sieve.survivors()[survivor].values[edit] << ']';
      }
      std::cout << ']';
    }
    std::cout << "]\n}\n";
    std::cerr << "arbitrary radius-three covering quotient and modular sieve "
                 "verified\n";
    return 0;
  } catch (const std::exception& error) {
    std::cerr << "error: " << error.what() << '\n';
    return 1;
  }
}
