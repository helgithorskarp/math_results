// Exact, restartable radius-seven extension of radius6.cpp.
//
// Each invocation handles one deterministic shard.  Connected seven-edge
// graphs and the exceptional 6+1 component partition use a multiplicity-first
// color quotient.  All other disconnected partitions use the stored
// connected-component catalogue through five edges.  The shard outputs are
// merged and checked by merge_radius7.py.
#define RADIUS6_NO_MAIN
#include "radius6.cpp"

#include <chrono>
#include <functional>
#include <sstream>

namespace {

constexpr int kRadius7 = 7;
constexpr std::uint64_t kExpectedRadius7Orbits = UINT64_C(1503560419);

using EditSet7 = std::array<int, kRadius7>;

struct OrbitShape7 {
  int vertex_count;
  std::uint64_t graph_code;
  std::vector<std::vector<int>> automorphisms;
};

std::uint64_t permute_graph7(std::uint64_t graph, int vertex_count,
                             const std::vector<int>& permutation) {
  std::uint64_t image = 0;
  for (int left = 0; left < vertex_count; ++left) {
    for (int right = 0; right < left; ++right) {
      if ((graph >> pair_bit(left, right)) & UINT64_C(1)) {
        image |= UINT64_C(1)
                 << pair_bit(permutation[left], permutation[right]);
      }
    }
  }
  return image;
}

std::uint64_t canonical_graph7(std::uint64_t graph, int vertex_count) {
  std::uint64_t canonical = graph;
  for (const auto& permutation : permutations(vertex_count))
    canonical =
        std::min(canonical, permute_graph7(graph, vertex_count, permutation));
  return canonical;
}

std::vector<OrbitShape7> generate_connected_shapes7(
    const std::vector<Shape6>& smaller) {
  std::array<std::set<std::uint64_t>, 9> by_vertex_count;
  for (const Shape6& shape : smaller) {
    const int size = shape.vertex_count;
    for (int left = 0; left < size; ++left) {
      for (int right = 0; right < left; ++right) {
        const std::uint64_t bit = UINT64_C(1) << pair_bit(left, right);
        if ((shape.graph_code & bit) != 0) continue;
        by_vertex_count[size].insert(
            canonical_graph7(shape.graph_code | bit, size));
      }
    }
    if (size < 8) {
      for (int neighbor = 0; neighbor < size; ++neighbor) {
        const std::uint64_t graph =
            shape.graph_code | (UINT64_C(1) << pair_bit(size, neighbor));
        by_vertex_count[size + 1].insert(canonical_graph7(graph, size + 1));
      }
    }
  }

  std::vector<OrbitShape7> answer;
  for (int size = 2; size <= 8; ++size) {
    const auto vertex_permutations = permutations(size);
    for (const std::uint64_t graph : by_vertex_count[size]) {
      if (std::popcount(graph) != kRadius7)
        throw std::runtime_error("bad seven-edge shape");
      OrbitShape7 shape{size, graph, {}};
      for (const auto& permutation : vertex_permutations) {
        if (permute_graph7(graph, size, permutation) == graph)
          shape.automorphisms.push_back(permutation);
      }
      answer.push_back(std::move(shape));
    }
  }
  const std::array<std::size_t, 9> expected = {0, 0, 0, 0, 0, 4, 19, 33, 23};
  std::array<std::size_t, 9> observed{};
  for (const auto& shape : answer) ++observed[shape.vertex_count];
  if (observed != expected || answer.size() != 79)
    throw std::runtime_error("connected seven-edge shape census mismatch");
  return answer;
}

OrbitShape7 six_plus_one_shape(const Shape6& connected_shape) {
  const int size = connected_shape.vertex_count;
  OrbitShape7 answer{size + 2, connected_shape.graph_code, {}};
  answer.graph_code |= UINT64_C(1) << pair_bit(size + 1, size);
  for (const auto& source : connected_shape.automorphisms) {
    for (int swap = 0; swap < 2; ++swap) {
      std::vector<int> automorphism(static_cast<std::size_t>(size + 2));
      for (int vertex = 0; vertex < size; ++vertex)
        automorphism[vertex] = source[vertex];
      automorphism[size] = size + swap;
      automorphism[size + 1] = size + 1 - swap;
      answer.automorphisms.push_back(std::move(automorphism));
    }
  }
  return answer;
}

std::uint64_t encode_colors7(const std::array<int, 9>& colors,
                             int vertex_count) {
  std::uint64_t code = 0;
  std::uint64_t multiplier = 1;
  for (int vertex = 0; vertex < vertex_count; ++vertex) {
    code += static_cast<std::uint64_t>(colors[vertex]) * multiplier;
    multiplier *= kColorCount;
  }
  return code;
}

std::int64_t small_determinant_mod7(
    std::array<std::array<std::int64_t, 14>, 14> matrix, int size,
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

class SquareSieve7 {
 public:
  SquareSieve7(const ColoredComponents& components, const std::string& path,
               std::size_t shard, std::size_t shard_count)
      : components_(components), gram_(gram_matrix(path)), shard_(shard),
        shard_count_(shard_count), start_(std::chrono::steady_clock::now()) {
    initialize_bins();
    initialize_gram_data();
  }

  void evaluate_components(const std::array<std::uint32_t, kRadius7>& ids,
                           std::size_t component_count) {
    std::array<int, kColorCount> next_slot{};
    EditSet7 edits{};
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
            if (edit_count >= kRadius7)
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

  void evaluate_shape(const OrbitShape7& shape,
                      const std::array<int, 9>& colors) {
    std::array<int, kColorCount> next_slot{};
    std::array<int, 9> actual_vertices{};
    for (int vertex = 0; vertex < shape.vertex_count; ++vertex) {
      const int color = colors[vertex];
      const int slot = next_slot[color]++;
      if (slot >= static_cast<int>(bin_vertices_[color].size()))
        throw std::runtime_error("shape reconstruction exceeds bin");
      actual_vertices[vertex] = bin_vertices_[color][slot];
    }
    EditSet7 edits{};
    int edit_count = 0;
    for (int left = 0; left < shape.vertex_count; ++left) {
      for (int right = 0; right < left; ++right) {
        if ((shape.graph_code >> pair_bit(left, right)) & UINT64_C(1)) {
          if (edit_count >= kRadius7)
            throw std::runtime_error("too many reconstructed shape edges");
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
  std::vector<EditSet7>& survivors() { return survivors_; }

 private:
  static void finish_reconstruction(EditSet7& edits, int edit_count) {
    if (edit_count != kRadius7)
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

  void evaluate(const EditSet7& edits) {
    ++total_;
    if (total_ % UINT64_C(10000000) == 0) {
      const double elapsed = std::chrono::duration<double>(
                                 std::chrono::steady_clock::now() - start_)
                                 .count();
      std::cerr << "shard " << shard_ << '/' << shard_count_ << ": sieve "
                << total_ << " classes in " << elapsed << " seconds\n";
    }
    std::array<int, 14> vertices{};
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
    std::array<std::array<std::int64_t, 14>, 14> perturbation{};
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
      std::array<std::array<std::int64_t, 14>, 14> update{};
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
      const std::int64_t numerator = small_determinant_mod7(update, size, prime);
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
  std::size_t shard_;
  std::size_t shard_count_;
  std::uint64_t total_ = 0;
  std::array<std::uint64_t, order23::kPrimes.size()> witness_counts_{};
  std::vector<EditSet7> survivors_;
  std::chrono::steady_clock::time_point start_;
};

struct MultiplicityCounts7 {
  std::uint64_t canonical_count_vectors = 0;
  std::uint64_t assigned_count_vectors = 0;
  std::uint64_t assignment_leaves = 0;
  std::uint64_t accepted = 0;

  MultiplicityCounts7& operator+=(const MultiplicityCounts7& other) {
    canonical_count_vectors += other.canonical_count_vectors;
    assigned_count_vectors += other.assigned_count_vectors;
    assignment_leaves += other.assignment_leaves;
    accepted += other.accepted;
    return *this;
  }
};

class MultiplicityEnumerator7 {
 public:
  MultiplicityEnumerator7(const OrbitShape7& shape, std::size_t shard,
                          std::size_t shard_count, SquareSieve7* sieve)
      : shape_(shape), actions_(outer_color_actions()), shard_(shard),
        shard_count_(shard_count), sieve_(sieve) {
    if (shape.vertex_count > static_cast<int>(colors_.size()))
      throw std::runtime_error("multiplicity shape has too many vertices");
  }

  MultiplicityCounts7 run() {
    count_vectors(0, shape_.vertex_count);
    return result_;
  }

 private:
  bool canonical_count_vector() const {
    for (std::size_t action = 1; action < actions_.size(); ++action) {
      std::array<int, kColorCount> image{};
      for (int color = 0; color < kColorCount; ++color)
        image[actions_[action][color]] = counts_[color];
      if (image < counts_) return false;
    }
    return true;
  }

  void finish_count_vector() {
    if (!canonical_count_vector()) return;
    const std::uint64_t ordinal = result_.canonical_count_vectors++;
    if (ordinal % shard_count_ != shard_) return;
    ++result_.assigned_count_vectors;
    stabilizer_.clear();
    for (std::size_t action = 0; action < actions_.size(); ++action) {
      bool fixes = true;
      for (int color = 0; color < kColorCount; ++color) {
        if (counts_[actions_[action][color]] != counts_[color]) {
          fixes = false;
          break;
        }
      }
      if (fixes) stabilizer_.push_back(action);
    }
    assignments(0);
  }

  void count_vectors(int color, int remaining) {
    if (color == kColorCount) {
      if (remaining == 0) finish_count_vector();
      return;
    }
    const int maximum = std::min(remaining, kCapacities[color]);
    for (int count = 0; count <= maximum; ++count) {
      counts_[color] = count;
      count_vectors(color + 1, remaining - count);
    }
  }

  void assignments(int vertex) {
    if (vertex == shape_.vertex_count) {
      finish_assignment();
      return;
    }
    for (int color = 0; color < kColorCount; ++color) {
      if (counts_[color] == 0) continue;
      --counts_[color];
      colors_[vertex] = color;
      assignments(vertex + 1);
      ++counts_[color];
    }
  }

  void finish_assignment() {
    ++result_.assignment_leaves;
    const std::uint64_t original =
        encode_colors7(colors_, shape_.vertex_count);
    for (const auto& automorphism : shape_.automorphisms) {
      for (const std::size_t action : stabilizer_) {
        std::array<int, 9> image{};
        for (int vertex = 0; vertex < shape_.vertex_count; ++vertex) {
          image[automorphism[vertex]] = actions_[action][colors_[vertex]];
        }
        if (encode_colors7(image, shape_.vertex_count) < original) return;
      }
    }
    ++result_.accepted;
    if (sieve_ != nullptr) sieve_->evaluate_shape(shape_, colors_);
  }

  const OrbitShape7& shape_;
  std::vector<std::array<int, kColorCount>> actions_;
  std::size_t shard_;
  std::size_t shard_count_;
  SquareSieve7* sieve_;
  std::array<int, kColorCount> counts_{};
  std::array<int, 9> colors_{};
  std::vector<std::size_t> stabilizer_;
  MultiplicityCounts7 result_;
};

struct PartitionCounts7 {
  std::string name;
  std::uint64_t internally_colored = 0;
  std::uint64_t accepted = 0;
};

class StoredDisconnectedEnumerator7 {
 public:
  StoredDisconnectedEnumerator7(const ColoredComponents& components,
                                std::size_t shard, std::size_t shard_count)
      : components_(components), shard_(shard), shard_count_(shard_count) {}

  std::vector<PartitionCounts7> run(SquareSieve7& sieve) {
    sieve_ = &sieve;
    std::vector<std::vector<int>> partitions;
    std::vector<int> prefix;
    integer_partitions(kRadius7, kRadius7, prefix, partitions);
    for (const auto& partition : partitions) {
      if (partition.size() == 1 || partition.front() == 6) continue;
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
      std::cerr << "shard " << shard_ << '/' << shard_count_
                << ": partition " << current_.name << ": "
                << current_.internally_colored << " internal, "
                << current_.accepted << " full classes\n";
      answer_.push_back(current_);
    }
    return answer_;
  }

 private:
  static void sort_prefix(std::array<std::uint32_t, kRadius7>& values,
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
      const std::array<std::uint32_t, kRadius7>& original) const {
    for (int action = 1; action < 12; ++action) {
      std::array<std::uint32_t, kRadius7> image{};
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
      ++current_.internally_colored;
      std::array<std::uint32_t, kRadius7> canonical_components{};
      std::copy(selected_.begin(), selected_.end(),
                canonical_components.begin());
      sort_prefix(canonical_components, selected_.size());
      if (outer_canonical(canonical_components)) {
        ++current_.accepted;
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
      if (position == 0 && offset % shard_count_ != shard_) continue;
      const std::uint32_t choice = choices[offset];
      const std::uint64_t addition = components_.variants()[choice].occupancy;
      if (!occupancy_fits(used, addition)) continue;
      selected_[position] = choice;
      selected_offsets_[position] = offset;
      extend(position + 1, used + addition);
    }
  }

  const ColoredComponents& components_;
  std::size_t shard_;
  std::size_t shard_count_;
  SquareSieve7* sieve_ = nullptr;
  const std::vector<int>* partition_ = nullptr;
  std::vector<std::uint32_t> selected_;
  std::vector<std::size_t> selected_offsets_;
  PartitionCounts7 current_;
  std::vector<PartitionCounts7> answer_;
};

std::uint64_t validate_multiplicity_generator(
    const std::vector<Shape6>& shapes6) {
  std::uint64_t accepted = 0;
  for (const Shape6& source : shapes6) {
    OrbitShape7 shape{source.vertex_count, source.graph_code,
                      source.automorphisms};
    MultiplicityEnumerator7 enumerator(shape, 0, 1, nullptr);
    accepted += enumerator.run().accepted;
  }
  if (accepted != kExpectedConnectedOrbits)
    throw std::runtime_error(
        "multiplicity generator fails radius-six regression check");
  return accepted;
}

std::size_t parse_size(const char* text, const char* label) {
  std::string value(text);
  std::size_t consumed = 0;
  const unsigned long long parsed = std::stoull(value, &consumed);
  if (consumed != value.size())
    throw std::runtime_error(std::string("invalid ") + label);
  return static_cast<std::size_t>(parsed);
}

void print_multiplicity_counts(const MultiplicityCounts7& counts) {
  std::cout << "{\"canonical_count_vectors\": "
            << counts.canonical_count_vectors
            << ", \"assigned_count_vectors\": "
            << counts.assigned_count_vectors
            << ", \"assignment_leaves\": " << counts.assignment_leaves
            << ", \"symmetry_classes\": " << counts.accepted << '}';
}

}  // namespace

int main(int argc, char** argv) {
  try {
    if (argc < 3 || argc > 4)
      throw std::runtime_error(
          "usage: radius7 SHARD SHARD_COUNT [record23.txt]");
    const std::size_t shard = parse_size(argv[1], "shard");
    const std::size_t shard_count = parse_size(argv[2], "shard count");
    if (shard_count == 0 || shard >= shard_count)
      throw std::runtime_error("shard must satisfy 0 <= SHARD < SHARD_COUNT");
    const std::string record_path = argc == 4 ? argv[3] : "record23.txt";

    const ColoredComponents components(generate_shapes());
    const std::vector<Shape6> shapes6 = generate_shapes6(components.shapes());
    const std::uint64_t regression = validate_multiplicity_generator(shapes6);
    const std::vector<OrbitShape7> shapes7 =
        generate_connected_shapes7(shapes6);
    std::cerr << "shard " << shard << '/' << shard_count << ": "
              << components.variants().size() << " stored variants, "
              << shapes6.size() << " six-edge shapes, " << shapes7.size()
              << " seven-edge shapes; radius-six regression " << regression
              << "\n";

    SquareSieve7 sieve(components, record_path, shard, shard_count);
    MultiplicityCounts7 connected;
    for (std::size_t index = 0; index < shapes7.size(); ++index) {
      MultiplicityEnumerator7 enumerator(shapes7[index], shard, shard_count,
                                         &sieve);
      const MultiplicityCounts7 shape_counts = enumerator.run();
      connected += shape_counts;
      std::cerr << "shard " << shard << '/' << shard_count
                << ": connected shape " << (index + 1) << '/'
                << shapes7.size() << " (v=" << shapes7[index].vertex_count
                << "): " << shape_counts.assignment_leaves << " leaves, "
                << shape_counts.accepted << " full classes\n";
    }

    MultiplicityCounts7 six_plus_one;
    for (std::size_t index = 0; index < shapes6.size(); ++index) {
      const OrbitShape7 shape = six_plus_one_shape(shapes6[index]);
      MultiplicityEnumerator7 enumerator(shape, shard, shard_count, &sieve);
      const MultiplicityCounts7 shape_counts = enumerator.run();
      six_plus_one += shape_counts;
      std::cerr << "shard " << shard << '/' << shard_count
                << ": six-plus-one shape " << (index + 1) << '/'
                << shapes6.size() << " (v=" << shape.vertex_count << "): "
                << shape_counts.assignment_leaves << " leaves, "
                << shape_counts.accepted << " full classes\n";
    }

    StoredDisconnectedEnumerator7 stored_enumerator(components, shard,
                                                     shard_count);
    const std::vector<PartitionCounts7> partitions =
        stored_enumerator.run(sieve);
    std::uint64_t stored_internal = 0;
    std::uint64_t stored_accepted = 0;
    for (const auto& partition : partitions) {
      stored_internal += partition.internally_colored;
      stored_accepted += partition.accepted;
    }
    if (connected.accepted + six_plus_one.accepted + stored_accepted !=
        sieve.total())
      throw std::runtime_error("shard category accounting mismatch");
    const std::uint64_t rejected = std::accumulate(
        sieve.witness_counts().begin(), sieve.witness_counts().end(),
        UINT64_C(0));
    if (rejected + sieve.survivors().size() != sieve.total())
      throw std::runtime_error("shard sieve accounting mismatch");
    std::sort(sieve.survivors().begin(), sieve.survivors().end());

    std::cout << "{\n  \"schema\": \"radius7-shard-v1\",\n"
              << "  \"order\": 23,\n  \"radius\": 7,\n"
              << "  \"shard\": " << shard << ",\n"
              << "  \"shard_count\": " << shard_count << ",\n"
              << "  \"expected_global_symmetry_classes\": "
              << kExpectedRadius7Orbits << ",\n"
              << "  \"radius_six_connected_regression\": " << regression
              << ",\n  \"stored_connected_shapes_through_five\": "
              << components.shapes().size()
              << ",\n  \"stored_colored_connected_variants_through_five\": "
              << components.variants().size()
              << ",\n  \"connected_six_edge_shapes\": " << shapes6.size()
              << ",\n  \"connected_seven_edge_shapes\": " << shapes7.size()
              << ",\n  \"connected\": ";
    print_multiplicity_counts(connected);
    std::cout << ",\n  \"six_plus_one\": ";
    print_multiplicity_counts(six_plus_one);
    std::cout << ",\n  \"stored_partitions\": [";
    for (std::size_t index = 0; index < partitions.size(); ++index) {
      if (index != 0) std::cout << ", ";
      std::cout << "{\"partition\": \"" << partitions[index].name
                << "\", \"internally_colored_graphs\": "
                << partitions[index].internally_colored
                << ", \"symmetry_classes\": "
                << partitions[index].accepted << '}';
    }
    std::cout << "],\n  \"stored_partition_internally_colored_graphs\": "
              << stored_internal
              << ",\n  \"stored_partition_symmetry_classes\": "
              << stored_accepted << ",\n  \"symmetry_classes\": "
              << sieve.total() << ",\n  \"witness_primes\": [";
    for (std::size_t index = 0; index < order23::kPrimes.size(); ++index) {
      if (index != 0) std::cout << ", ";
      std::cout << order23::kPrimes[index];
    }
    std::cout << "],\n  \"witness_counts\": [";
    for (std::size_t index = 0; index < sieve.witness_counts().size();
         ++index) {
      if (index != 0) std::cout << ", ";
      std::cout << sieve.witness_counts()[index];
    }
    std::cout << "],\n  \"survivor_edge_indices\": [";
    for (std::size_t survivor = 0; survivor < sieve.survivors().size();
         ++survivor) {
      if (survivor != 0) std::cout << ", ";
      std::cout << '[';
      for (int edge = 0; edge < kRadius7; ++edge) {
        if (edge != 0) std::cout << ", ";
        std::cout << sieve.survivors()[survivor][edge];
      }
      std::cout << ']';
    }
    std::cout << "]\n}\n";
    std::cerr << "shard " << shard << '/' << shard_count << ": complete, "
              << sieve.total() << " symmetry classes, "
              << sieve.survivors().size() << " survivors\n";
    return 0;
  } catch (const std::exception& error) {
    std::cerr << "error: " << error.what() << '\n';
    return 1;
  }
}
