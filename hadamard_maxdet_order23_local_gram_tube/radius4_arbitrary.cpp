// Exact sharded covering search for all four-position legal Gram edits.
//
// The underlying four-edge edit sets are quotiented by Aut(G0).  For every
// canonical representative, all 10^4 assignments of alternative legal Gram
// values are tested.  Stabilizers can identify assignments, so this is a
// symmetry-normalized cover, not the exact orbit set of valued edits.
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
#include <sstream>

namespace {

constexpr int kArbitraryRadius4 = 4;
constexpr std::uint64_t kExpectedUnderlyingOrbits4 = UINT64_C(197931);
constexpr std::uint64_t kExpectedInternallyColored4 = UINT64_C(1886683);
constexpr std::uint64_t kAssignmentsPerRepresentative4 = UINT64_C(10000);
constexpr std::uint64_t kExpectedAssignments4 = UINT64_C(1979310000);
constexpr std::uint64_t kCoveredLabeledMatrices4 = UINT64_C(1666953750000);
constexpr std::uint64_t kRecordDeterminant23 = UINT64_C(2779447296000000);
constexpr std::array<int, 11> kLegalValues4 = {
    -21, -17, -13, -9, -5, -1, 3, 7, 11, 15, 19,
};

using EditSet4 = std::array<int, kArbitraryRadius4>;
using ValueSet4 = std::array<int, kArbitraryRadius4>;

struct Survivor4 {
  EditSet4 edges{};
  ValueSet4 values{};
};

std::int64_t small_determinant_mod4(
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

class ArbitrarySieve4 {
 public:
  ArbitrarySieve4(const ColoredComponents& components, const std::string& path,
                  std::size_t shard, std::size_t shard_count)
      : components_(components), gram_(gram_matrix(path)), shard_(shard),
        shard_count_(shard_count), start_(std::chrono::steady_clock::now()) {
    initialize_bins();
    initialize_gram_data();
  }

  void evaluate_components(
      const std::array<std::uint32_t, kArbitraryRadius4>& component_ids,
      std::size_t component_count) {
    const EditSet4 edit_indices = reconstruct(component_ids, component_count);
    ++underlying_representatives_;
    ValueSet4 values{};
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
  std::uint64_t modular_survivors() const { return modular_survivors_; }
  std::vector<Survivor4>& survivors() { return survivors_; }

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

  EditSet4 reconstruct(
      const std::array<std::uint32_t, kArbitraryRadius4>& component_ids,
      std::size_t component_count) const {
    std::array<int, kColorCount> next_slot{};
    EditSet4 edit_indices{};
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
            if (edit_count >= kArbitraryRadius4)
              throw std::runtime_error("too many reconstructed edges");
            edit_indices[edit_count++] =
                edge_index_[actual_vertices[left]][actual_vertices[right]];
          }
        }
      }
    }
    if (edit_count != kArbitraryRadius4)
      throw std::runtime_error("wrong reconstructed edge count");
    std::sort(edit_indices.begin(), edit_indices.end());
    if (std::adjacent_find(edit_indices.begin(), edit_indices.end()) !=
        edit_indices.end())
      throw std::runtime_error("duplicate reconstructed edge");
    return edit_indices;
  }

  void assign_values(const EditSet4& edit_indices, ValueSet4& values,
                     int position) {
    if (position == kArbitraryRadius4) {
      evaluate(edit_indices, values);
      return;
    }
    const int original = edges_[edit_indices[position]].value;
    for (const int value : kLegalValues4) {
      if (value == original) continue;
      values[position] = value;
      assign_values(edit_indices, values, position + 1);
    }
  }

  void retain_survivor(const EditSet4& edit_indices, const ValueSet4& values) {
    ++modular_survivors_;
    survivors_.push_back({edit_indices, values});
  }

  void evaluate(const EditSet4& edit_indices, const ValueSet4& values) {
    ++total_;
    if (total_ % UINT64_C(2000000) == 0) {
      const double elapsed = std::chrono::duration<double>(
                                 std::chrono::steady_clock::now() - start_)
                                 .count();
      std::cerr << "shard " << shard_ << '/' << shard_count_ << ": sieve "
                << total_ << " assignments in " << elapsed << " seconds\n";
    }
    std::array<int, 8> vertices{};
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
    std::array<std::array<std::int64_t, 8>, 8> perturbation{};
    for (int edit = 0; edit < kArbitraryRadius4; ++edit) {
      const GramEdge& edge = edges_[edit_indices[edit]];
      const std::int64_t delta = values[edit] - edge.value;
      const int left = position[edge.left];
      const int right = position[edge.right];
      perturbation[left][right] = delta;
      perturbation[right][left] = delta;
    }

    std::array<std::array<std::int64_t, 8>, 8> raw_update{};
    for (int row = 0; row < size; ++row) {
      for (int column = 0; column < size; ++column) {
        std::int64_t value = row == column ? order23::kScale : 0;
        for (int middle = 0; middle < size; ++middle) {
          value += order23::kInverseNumerator[vertices[row]][vertices[middle]] *
                   perturbation[middle][column];
        }
        raw_update[row][column] = value;
      }
    }
    for (std::size_t prime_index = 0; prime_index < order23::kPrimes.size();
         ++prime_index) {
      const std::int64_t prime = order23::kPrimes[prime_index];
      std::array<std::array<std::int64_t, 8>, 8> update{};
      for (int row = 0; row < size; ++row)
        for (int column = 0; column < size; ++column)
          update[row][column] = normalize(raw_update[row][column], prime);
      const std::int64_t numerator =
          small_determinant_mod4(update, size, prime);
      const std::int64_t square_test = normalize(
          numerator * mod_pow(order23::kScale, size, prime), prime);
      if (square_test != 0 &&
          mod_pow(square_test, (prime - 1) / 2, prime) == prime - 1) {
        ++witness_counts_[prime_index];
        return;
      }
    }
    retain_survivor(edit_indices, values);
  }

  const ColoredComponents& components_;
  Gram gram_{};
  std::array<std::vector<int>, kColorCount> bin_vertices_;
  std::array<std::array<int, order23::kOrder>, order23::kOrder> edge_index_{};
  std::vector<GramEdge> edges_;
  std::size_t shard_;
  std::size_t shard_count_;
  std::uint64_t underlying_representatives_ = 0;
  std::uint64_t total_ = 0;
  std::array<std::uint64_t, order23::kPrimes.size()> witness_counts_{};
  std::uint64_t modular_survivors_ = 0;
  std::vector<Survivor4> survivors_;
  std::chrono::steady_clock::time_point start_;
};

struct PartitionCounts4 {
  std::string name;
  std::uint64_t internally_colored = 0;
  std::uint64_t accepted = 0;
};

class UnderlyingOrbitEnumerator4 {
 public:
  UnderlyingOrbitEnumerator4(const ColoredComponents& components,
                             ArbitrarySieve4& sieve, std::size_t shard,
                             std::size_t shard_count)
      : components_(components), sieve_(sieve), shard_(shard),
        shard_count_(shard_count) {}

  std::vector<PartitionCounts4> run() {
    std::vector<std::vector<int>> partitions;
    std::vector<int> prefix;
    integer_partitions(kArbitraryRadius4, kArbitraryRadius4, prefix, partitions);
    for (const auto& partition : partitions) {
      partition_ = &partition;
      selected_.assign(partition.size(), 0);
      selected_offsets_.assign(partition.size(), 0);
      current_ = {};
      std::ostringstream name;
      for (std::size_t index = 0; index < partition.size(); ++index) {
        if (index != 0) name << '+';
        name << partition[index];
      }
      current_.name = name.str();
      extend(0, 0);
      std::cerr << "shard " << shard_ << '/' << shard_count_ << ": partition "
                << current_.name << ": " << current_.internally_colored
                << " internal, " << current_.accepted << " accepted\n";
      answer_.push_back(current_);
    }
    return answer_;
  }

 private:
  static void sort_prefix(
      std::array<std::uint32_t, kArbitraryRadius4>& values, std::size_t size) {
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
      const std::array<std::uint32_t, kArbitraryRadius4>& original) const {
    for (int action = 1; action < 12; ++action) {
      std::array<std::uint32_t, kArbitraryRadius4> image{};
      for (std::size_t index = 0; index < selected_.size(); ++index) {
        image[index] =
            components_.variants()[selected_[index]].outer_images[action];
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
      std::array<std::uint32_t, kArbitraryRadius4> canonical_components{};
      std::copy(selected_.begin(), selected_.end(),
                canonical_components.begin());
      sort_prefix(canonical_components, selected_.size());
      std::uint64_t hash = UINT64_C(1469598103934665603);
      for (std::size_t index = 0; index < selected_.size(); ++index) {
        hash ^= canonical_components[index];
        hash *= UINT64_C(1099511628211);
      }
      if (hash % shard_count_ != shard_) return;
      ++current_.internally_colored;
      if (outer_canonical(canonical_components)) {
        ++current_.accepted;
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
  ArbitrarySieve4& sieve_;
  std::size_t shard_;
  std::size_t shard_count_;
  const std::vector<int>* partition_ = nullptr;
  std::vector<std::uint32_t> selected_;
  std::vector<std::size_t> selected_offsets_;
  PartitionCounts4 current_;
  std::vector<PartitionCounts4> answer_;
};

std::size_t parse_size4(const char* text, const char* label) {
  std::string value(text);
  std::size_t consumed = 0;
  const unsigned long long parsed = std::stoull(value, &consumed);
  if (consumed != value.size())
    throw std::runtime_error(std::string("invalid ") + label);
  return static_cast<std::size_t>(parsed);
}

}  // namespace

int main(int argc, char** argv) {
  try {
    if (argc < 3 || argc > 4)
      throw std::runtime_error(
          "usage: radius4_arbitrary SHARD SHARD_COUNT [record23.txt]");
    const std::size_t shard = parse_size4(argv[1], "shard");
    const std::size_t shard_count = parse_size4(argv[2], "shard count");
    if (shard_count == 0 || shard >= shard_count)
      throw std::runtime_error("shard must satisfy 0 <= SHARD < SHARD_COUNT");
    const std::string record_path = argc == 4 ? argv[3] : "record23.txt";

    auto shapes = generate_shapes();
    shapes.erase(
        std::remove_if(shapes.begin(), shapes.end(), [](const Shape& shape) {
          return shape.edge_count > kArbitraryRadius4;
        }),
        shapes.end());
    const ColoredComponents components(std::move(shapes));
    if (components.shapes().size() != 10 ||
        components.variants().size() != 152305)
      throw std::runtime_error("connected component catalogue mismatch");
    std::cerr << "shard " << shard << '/' << shard_count << ": "
              << components.shapes().size() << " connected shapes, "
              << components.variants().size() << " colored variants\n";

    ArbitrarySieve4 sieve(components, record_path, shard, shard_count);
    UnderlyingOrbitEnumerator4 enumerator(components, sieve, shard, shard_count);
    const std::vector<PartitionCounts4> partitions = enumerator.run();
    std::uint64_t internally_colored = 0;
    std::uint64_t accepted = 0;
    for (const PartitionCounts4& partition : partitions) {
      internally_colored += partition.internally_colored;
      accepted += partition.accepted;
    }
    if (accepted != sieve.underlying_representatives() ||
        sieve.total() != accepted * kAssignmentsPerRepresentative4)
      throw std::runtime_error("shard coverage accounting mismatch");
    const std::uint64_t rejected = std::accumulate(
        sieve.witness_counts().begin(), sieve.witness_counts().end(),
        UINT64_C(0));
    if (rejected + sieve.modular_survivors() != sieve.total())
      throw std::runtime_error("shard modular sieve accounting mismatch");
    std::sort(sieve.survivors().begin(), sieve.survivors().end(),
              [](const Survivor4& left, const Survivor4& right) {
                if (left.edges != right.edges) return left.edges < right.edges;
                return left.values < right.values;
              });

    std::cout << "{\n  \"schema\": \"radius4-arbitrary-shard-v1\",\n"
              << "  \"order\": 23,\n  \"radius\": 4,\n"
              << "  \"shard\": " << shard << ",\n"
              << "  \"shard_count\": " << shard_count << ",\n"
              << "  \"expected_global_internally_colored\": "
              << kExpectedInternallyColored4 << ",\n"
              << "  \"expected_global_underlying_edit_set_orbits\": "
              << kExpectedUnderlyingOrbits4 << ",\n"
              << "  \"expected_global_normalized_cover_evaluations\": "
              << kExpectedAssignments4 << ",\n"
              << "  \"connected_shapes_through_four\": "
              << components.shapes().size() << ",\n"
              << "  \"colored_connected_variants_through_four\": "
              << components.variants().size() << ",\n"
              << "  \"legal_values\": [";
    for (std::size_t index = 0; index < kLegalValues4.size(); ++index) {
      if (index != 0) std::cout << ", ";
      std::cout << kLegalValues4[index];
    }
    std::cout << "],\n  \"value_assignments_per_representative\": "
              << kAssignmentsPerRepresentative4
              << ",\n  \"covered_labeled_matrices\": "
              << kCoveredLabeledMatrices4 << ",\n  \"partitions\": [";
    for (std::size_t index = 0; index < partitions.size(); ++index) {
      if (index != 0) std::cout << ", ";
      std::cout << "{\"partition\": \"" << partitions[index].name
                << "\", \"internally_colored_graphs\": "
                << partitions[index].internally_colored
                << ", \"underlying_edit_set_orbits\": "
                << partitions[index].accepted << '}';
    }
    std::cout << "],\n  \"internally_colored_underlying_graphs\": "
              << internally_colored
              << ",\n  \"underlying_edit_set_orbits\": " << accepted
              << ",\n  \"normalized_cover_evaluations\": " << sieve.total()
              << ",\n  \"witness_primes\": [";
    for (std::size_t index = 0; index < order23::kPrimes.size(); ++index) {
      if (index != 0) std::cout << ", ";
      std::cout << order23::kPrimes[index];
    }
    std::cout << "],\n  \"witness_counts\": [";
    for (std::size_t index = 0; index < sieve.witness_counts().size(); ++index) {
      if (index != 0) std::cout << ", ";
      std::cout << sieve.witness_counts()[index];
    }
    std::cout << "],\n  \"survives_48_nonsquare_tests\": "
              << sieve.modular_survivors()
              << ",\n  \"record_threshold\": "
              << kRecordDeterminant23
              << ",\n  \"survivor_edits\": [";
    for (std::size_t index = 0; index < sieve.survivors().size(); ++index) {
      if (index != 0) std::cout << ", ";
      const Survivor4& survivor = sieve.survivors()[index];
      std::cout << '[';
      for (int edit = 0; edit < kArbitraryRadius4; ++edit) {
        if (edit != 0) std::cout << ", ";
        std::cout << '[' << survivor.edges[edit] << ", "
                  << survivor.values[edit] << ']';
      }
      std::cout << ']';
    }
    std::cout << "]\n}\n";
    std::cerr << "shard " << shard << '/' << shard_count << ": complete, "
              << accepted << " underlying representatives, " << sieve.total()
              << " assignments, " << sieve.modular_survivors()
              << " modular survivors\n";
    return 0;
  } catch (const std::exception& error) {
    std::cerr << "error: " << error.what() << '\n';
    return 1;
  }
}
