#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <numeric>
#include <sstream>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

namespace {

constexpr int kVertices = 8;
constexpr int kOrders = 40320;
constexpr int kPairs = 28;
constexpr int kFixed = 20;
constexpr int kMissing = 8;
constexpr int kMaxProfile = 20;

using Permutation = std::array<std::uint8_t, kVertices>;
using Profile = std::array<std::uint16_t, kMaxProfile>;

struct Move {
  std::uint16_t replacement;
  std::uint8_t coordinate;
  std::int8_t delta;
};

constexpr std::array<std::pair<int, int>, kPairs> pairs = {{
    {0, 1}, {0, 2}, {0, 3}, {0, 4}, {0, 5}, {0, 6}, {0, 7},
    {1, 2}, {1, 3}, {1, 4}, {1, 5}, {1, 6}, {1, 7},
    {2, 3}, {2, 4}, {2, 5}, {2, 6}, {2, 7},
    {3, 4}, {3, 5}, {3, 6}, {3, 7},
    {4, 5}, {4, 6}, {4, 7},
    {5, 6}, {5, 7},
    {6, 7},
}};

constexpr std::array<std::pair<int, int>, kFixed> fixed_arcs = {{
    {0, 1}, {0, 2}, {0, 3}, {4, 0}, {6, 0}, {7, 0}, {1, 3},
    {1, 4}, {5, 1}, {1, 6}, {7, 1}, {2, 3}, {2, 4}, {5, 2},
    {6, 2}, {2, 7}, {3, 5}, {3, 6}, {3, 7}, {4, 5},
}};

constexpr std::array<std::pair<int, int>, kMissing> missing_pairs = {{
    {0, 5}, {1, 2}, {3, 4}, {4, 6},
    {4, 7}, {5, 6}, {5, 7}, {6, 7},
}};

int pair_index(int first, int second) {
  if (first > second) std::swap(first, second);
  for (int edge = 0; edge < kPairs; ++edge) {
    if (pairs[edge] == std::pair<int, int>{first, second}) return edge;
  }
  throw std::logic_error("pair is outside K8");
}

int permutation_rank(const Permutation& permutation) {
  constexpr std::array<int, kVertices> factorial = {5040, 720, 120, 24, 6, 2, 1, 1};
  int rank = 0;
  for (int i = 0; i < kVertices; ++i) {
    int smaller = 0;
    for (int j = i + 1; j < kVertices; ++j) {
      smaller += permutation[j] < permutation[i];
    }
    rank += smaller * factorial[i];
  }
  return rank;
}

std::array<Permutation, kOrders> enumerate_permutations() {
  std::array<Permutation, kOrders> result{};
  Permutation permutation = {0, 1, 2, 3, 4, 5, 6, 7};
  int count = 0;
  do {
    if (count >= kOrders) throw std::logic_error("too many permutations");
    result[count++] = permutation;
  } while (std::next_permutation(permutation.begin(), permutation.end()));
  if (count != kOrders) throw std::logic_error("incomplete permutation enumeration");
  return result;
}

std::array<std::uint32_t, kOrders> make_masks(
    const std::array<Permutation, kOrders>& permutations) {
  std::array<std::uint32_t, kOrders> masks{};
  for (int index = 0; index < kOrders; ++index) {
    std::array<int, kVertices> position{};
    for (int rank = 0; rank < kVertices; ++rank) {
      position[permutations[index][rank]] = rank;
    }
    for (int edge = 0; edge < kPairs; ++edge) {
      masks[index] |= std::uint32_t(position[pairs[edge].first] < position[pairs[edge].second])
                      << edge;
    }
  }
  return masks;
}

int predicts_arc(std::uint32_t mask, std::pair<int, int> arc) {
  int edge = pair_index(arc.first, arc.second);
  int increasing = int((mask >> edge) & 1U);
  return arc.first < arc.second ? increasing : 1 - increasing;
}

std::array<std::vector<Move>, kOrders> make_transitions(
    const std::array<Permutation, kOrders>& permutations,
    const std::array<std::uint32_t, kOrders>& masks) {
  std::array<std::vector<Move>, kOrders> transitions;
  std::size_t count = 0;
  for (int index = 0; index < kOrders; ++index) {
    for (int position = 0; position + 1 < kVertices; ++position) {
      int first = permutations[index][position];
      int second = permutations[index][position + 1];
      std::pair<int, int> pair = std::minmax(first, second);
      int coordinate = -1;
      for (int candidate = 0; candidate < kMissing; ++candidate) {
        if (missing_pairs[candidate] == pair) coordinate = candidate;
      }
      if (coordinate < 0) continue;

      Permutation changed = permutations[index];
      std::swap(changed[position], changed[position + 1]);
      int replacement = permutation_rank(changed);
      if (permutations[replacement] != changed) {
        throw std::logic_error("permutation rank disagrees with enumeration");
      }
      int edge = pair_index(first, second);
      if ((masks[index] ^ masks[replacement]) != (std::uint32_t(1) << edge)) {
        throw std::logic_error("adjacent swap changed more than one pair");
      }
      int before = int((masks[index] >> edge) & 1U);
      int after = int((masks[replacement] >> edge) & 1U);
      transitions[index].push_back(
          {static_cast<std::uint16_t>(replacement),
           static_cast<std::uint8_t>(coordinate),
           static_cast<std::int8_t>(after - before)});
      ++count;
    }
  }
  if (count != 80640) throw std::logic_error("wrong adjacent-swap transition count");
  return transitions;
}

std::uint32_t integer_power(std::uint32_t base, int exponent) {
  std::uint32_t result = 1;
  while (exponent-- > 0) result *= base;
  return result;
}

struct BoxSummary {
  int degree;
  int stabilizer;
  int profile_size;
  std::uint32_t targets;
  std::uint32_t processed;
  std::uint32_t residual_queue;
};

BoxSummary verify_box(
    const std::string& path,
    int expected_degree,
    const std::array<std::uint32_t, kOrders>& masks,
    const std::array<int, kOrders>& fixed_hits,
    const std::array<std::vector<Move>, kOrders>& transitions) {
  std::ifstream input(path);
  if (!input) throw std::runtime_error("cannot open " + path);
  std::string line;
  if (!std::getline(input, line)) throw std::runtime_error("empty corner file");
  std::istringstream header(line);
  std::string tag, degree_field, size_field;
  header >> tag >> degree_field >> size_field;
  if (tag != "G8_CORNERS") throw std::runtime_error("wrong corner header");
  int degree = std::stoi(degree_field.substr(degree_field.find('=') + 1));
  int profile_size = std::stoi(size_field.substr(size_field.find('=') + 1));
  int stabilizer = (7 * degree + 5) / 6;
  if (degree != expected_degree || degree < 1 || degree > 6 ||
      profile_size != degree + 2 * stabilizer || profile_size > kMaxProfile) {
    throw std::runtime_error("inconsistent corner parameters");
  }

  int base = degree + 1;
  std::array<std::uint32_t, kMissing> stride{};
  stride[0] = 1;
  for (int coordinate = 1; coordinate < kMissing; ++coordinate) {
    stride[coordinate] = stride[coordinate - 1] * std::uint32_t(base);
  }
  std::uint32_t total = integer_power(base, kMissing);
  std::vector<Profile> profiles(total);
  std::vector<std::uint8_t> visited(total, 0);
  std::vector<std::uint32_t> queue;
  queue.reserve(total);

  int seeds = 0;
  while (std::getline(input, line)) {
    if (line.empty()) continue;
    if (line.rfind("TARGET ", 0) != 0) throw std::runtime_error("malformed corner row");
    std::size_t separator = line.find(" profile=");
    if (separator == std::string::npos) throw std::runtime_error("corner row has no profile");
    std::string target = line.substr(7, separator - 7);
    if (target.size() != kMissing) throw std::runtime_error("corner target has wrong length");
    std::uint32_t code = 0;
    std::array<int, kMissing> digits{};
    for (int coordinate = 0; coordinate < kMissing; ++coordinate) {
      digits[coordinate] = target[coordinate] - '0';
      if (digits[coordinate] != 0 && digits[coordinate] != degree) {
        throw std::runtime_error("seed target is not a box corner");
      }
      code += std::uint32_t(digits[coordinate]) * stride[coordinate];
    }
    if (visited[code]) throw std::runtime_error("duplicate corner target");

    std::stringstream profile_stream(line.substr(separator + 9));
    std::string term;
    int count = 0;
    while (std::getline(profile_stream, term, ',')) {
      if (count >= profile_size) throw std::runtime_error("corner profile is too long");
      int index = std::stoi(term);
      if (index < 0 || index >= kOrders) throw std::runtime_error("order index out of range");
      profiles[code][count++] = static_cast<std::uint16_t>(index);
    }
    if (count != profile_size ||
        !std::is_sorted(profiles[code].begin(), profiles[code].begin() + profile_size)) {
      throw std::runtime_error("corner profile has wrong size or order");
    }

    for (auto arc : fixed_arcs) {
      int predictions = 0;
      for (int slot = 0; slot < profile_size; ++slot) {
        predictions += predicts_arc(masks[profiles[code][slot]], arc);
      }
      if (predictions != degree + stabilizer) {
        throw std::runtime_error("corner profile fails a fixed arc");
      }
    }
    for (int coordinate = 0; coordinate < kMissing; ++coordinate) {
      int edge = pair_index(missing_pairs[coordinate].first, missing_pairs[coordinate].second);
      int predictions = 0;
      for (int slot = 0; slot < profile_size; ++slot) {
        predictions += int((masks[profiles[code][slot]] >> edge) & 1U);
      }
      if (predictions != stabilizer + digits[coordinate]) {
        throw std::runtime_error("corner profile fails a missing-pair count");
      }
    }
    int defect = 0;
    for (int slot = 0; slot < profile_size; ++slot) {
      defect += 13 - fixed_hits[profiles[code][slot]];
    }
    if (defect != 6 * stabilizer - 7 * degree) {
      throw std::runtime_error("corner profile has wrong total G8 defect");
    }

    visited[code] = 1;
    queue.push_back(code);
    ++seeds;
  }
  if (seeds != 256) throw std::runtime_error("corner coverage is not exactly 256");

  std::uint32_t reached = 256;
  std::uint32_t head = 0;
  while (head < queue.size() && reached < total) {
    std::uint32_t code = queue[head++];
    Profile current = profiles[code];
    for (int slot = 0; slot < profile_size; ++slot) {
      for (const Move& move : transitions[current[slot]]) {
        int digit = int((code / stride[move.coordinate]) % std::uint32_t(base));
        int changed_digit = digit + move.delta;
        if (changed_digit < 0 || changed_digit > degree) continue;
        std::uint32_t next = static_cast<std::uint32_t>(
            std::int64_t(code) + std::int64_t(move.delta) * stride[move.coordinate]);
        if (visited[next]) continue;

        Profile changed = current;
        changed[slot] = move.replacement;
        std::sort(changed.begin(), changed.begin() + profile_size);
        profiles[next] = changed;
        visited[next] = 1;
        queue.push_back(next);
        ++reached;
      }
    }
  }
  if (reached != total) {
    throw std::runtime_error("exchange closure did not cover the complete box");
  }
  return {degree, stabilizer, profile_size, total, head,
          static_cast<std::uint32_t>(queue.size() - head)};
}

}  // namespace

int main(int argc, char** argv) {
  try {
    int max_degree = 6;
    if (argc == 9 && std::string(argv[7]) == "--max-degree") {
      max_degree = std::stoi(argv[8]);
    } else if (argc != 7) {
      std::cerr << "usage: verify_boxes corners_d1.txt ... corners_d6.txt "
                   "[--max-degree 1..6]\n";
      return 2;
    }
    if (max_degree < 1 || max_degree > 6) {
      throw std::runtime_error("max degree is outside 1,...,6");
    }
    const auto permutations = enumerate_permutations();
    const auto masks = make_masks(permutations);
    const auto transitions = make_transitions(permutations, masks);

    std::array<int, kOrders> fixed_hits{};
    std::array<int, 7> layers{};
    for (int index = 0; index < kOrders; ++index) {
      for (auto arc : fixed_arcs) fixed_hits[index] += predicts_arc(masks[index], arc);
      int defect = 13 - fixed_hits[index];
      if (defect < 0 || defect > 6) throw std::logic_error("G8 hit count outside 7,...,13");
      ++layers[defect];
    }
    const std::array<int, 7> expected_layers = {832, 4192, 9344, 11584, 9344, 4192, 832};
    if (layers != expected_layers) throw std::logic_error("wrong G8 defect layers");

    std::cout << "orders=40320 adjacent_missing_swaps=80640 maximum_g8_hits=13\n";
    std::cout << "g8_defect_layers=0:832,1:4192,2:9344,3:11584,4:9344,5:4192,6:832\n";
    for (int degree = 1; degree <= max_degree; ++degree) {
      BoxSummary summary = verify_box(argv[degree], degree, masks, fixed_hits, transitions);
      std::cout << "degree=" << summary.degree
                << " stabilizer=" << summary.stabilizer
                << " profile_size=" << summary.profile_size
                << " targets=" << summary.targets
                << " processed=" << summary.processed
                << " residual_queue=" << summary.residual_queue << "\n";
    }
    if (max_degree == 6) {
      std::cout << "THEOREM m(W)=ceil(7k/6) for every degree-k extension of G8 "
                   "and every k>=1\n";
    } else {
      std::cout << "PARTIAL_CHECK verified residue boxes through degree="
                << max_degree << "\n";
    }
    return 0;
  } catch (const std::exception& error) {
    std::cerr << "ERROR: " << error.what() << "\n";
    return 1;
  }
}
