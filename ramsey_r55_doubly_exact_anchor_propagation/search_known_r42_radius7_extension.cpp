// Native implementation of the exact radius-seven decomposition in
// search_known_r42_radius7_extension.py.  Use the Python orchestration driver
// for a complete claim: it pins the catalog, runs the reference self-tests,
// derives all eligible orientations independently, and audits these PASS
// records.  This executable deliberately handles one orientation per call.

#include <algorithm>
#include <array>
#include <bit>
#include <cstdint>
#include <cstdlib>
#include <fstream>
#include <functional>
#include <iostream>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

namespace {

constexpr int kOrder = 42;
constexpr int kExtendedOrder = 43;
constexpr int kRadius = 7;
constexpr int kTargetEdges = 430;
constexpr std::uint64_t kProgressEvery = 5'000'000;
constexpr int kCacheBlock = 256;

using Graph = std::array<std::uint64_t, kExtendedOrder>;
using Requirements = std::array<std::uint8_t, kOrder>;

struct Repair {
  std::array<std::uint16_t, kRadius> edges{};
  std::uint8_t size = 0;
};

using RepairCache = std::unordered_map<std::string, std::vector<Repair>>;

std::uint16_t edge_code(int first, int second) {
  if (first > second) std::swap(first, second);
  return static_cast<std::uint16_t>(first * kOrder + second);
}

std::pair<int, int> decode_edge(std::uint16_t code) {
  return {code / kOrder, code % kOrder};
}

Graph decode_graph6(const std::string& encoded) {
  if (encoded.empty() || static_cast<unsigned char>(encoded.front()) == 126) {
    throw std::runtime_error("only short graph6 records are supported");
  }
  const int order = static_cast<unsigned char>(encoded.front()) - 63;
  if (order != kOrder) throw std::runtime_error("wrong catalog order");
  const int bit_count = order * (order - 1) / 2;
  const int payload = (bit_count + 5) / 6;
  if (static_cast<int>(encoded.size()) != 1 + payload) {
    throw std::runtime_error("wrong graph6 record length");
  }
  std::vector<bool> bits;
  bits.reserve(payload * 6);
  for (int index = 1; index < static_cast<int>(encoded.size()); ++index) {
    const int value = static_cast<unsigned char>(encoded[index]) - 63;
    if (value < 0 || value > 63) throw std::runtime_error("bad graph6 byte");
    for (int shift = 5; shift >= 0; --shift) {
      bits.push_back((value >> shift) & 1);
    }
  }
  Graph graph{};
  int position = 0;
  for (int second = 1; second < order; ++second) {
    for (int first = 0; first < second; ++first) {
      if (bits[position++]) {
        graph[first] |= std::uint64_t{1} << second;
        graph[second] |= std::uint64_t{1} << first;
      }
    }
  }
  return graph;
}

Graph complement(const Graph& graph, int order) {
  Graph result{};
  const std::uint64_t mask = (std::uint64_t{1} << order) - 1;
  for (int vertex = 0; vertex < order; ++vertex) {
    result[vertex] = mask ^ (std::uint64_t{1} << vertex) ^ graph[vertex];
  }
  return result;
}

bool clique_search(const Graph& graph, std::uint64_t candidates, int remaining) {
  if (std::popcount(candidates) < remaining) return false;
  if (remaining == 1) return candidates != 0;
  while (std::popcount(candidates) >= remaining) {
    const std::uint64_t bit = candidates & (~candidates + 1);
    candidates ^= bit;
    const int vertex = std::countr_zero(bit);
    if (clique_search(graph, candidates & graph[vertex], remaining - 1)) {
      return true;
    }
  }
  return false;
}

bool contains_clique(const Graph& graph, int order, int wanted,
                     std::uint64_t vertices = 0) {
  if (vertices == 0) vertices = (std::uint64_t{1} << order) - 1;
  return clique_search(graph, vertices, wanted);
}

bool contains_triangle(const Graph& graph, std::uint64_t candidates) {
  while (candidates) {
    const std::uint64_t vertex_bit = candidates & (~candidates + 1);
    candidates ^= vertex_bit;
    const int vertex = std::countr_zero(vertex_bit);
    std::uint64_t neighbors = candidates & graph[vertex];
    while (neighbors) {
      const std::uint64_t neighbor_bit = neighbors & (~neighbors + 1);
      neighbors ^= neighbor_bit;
      const int neighbor = std::countr_zero(neighbor_bit);
      if (graph[neighbor] & neighbors) return true;
    }
  }
  return false;
}

std::string encode_graph6(const Graph& graph, int order) {
  if (order > 62) throw std::runtime_error("short graph6 overflow");
  std::vector<int> bits;
  bits.reserve(order * (order - 1) / 2 + 5);
  for (int second = 1; second < order; ++second) {
    for (int first = 0; first < second; ++first) {
      bits.push_back((graph[first] >> second) & 1U);
    }
  }
  while (bits.size() % 6) bits.push_back(0);
  std::string answer(1, static_cast<char>(63 + order));
  for (std::size_t start = 0; start < bits.size(); start += 6) {
    int value = 0;
    for (int offset = 0; offset < 6; ++offset) {
      value |= bits[start + offset] << (5 - offset);
    }
    answer.push_back(static_cast<char>(63 + value));
  }
  return answer;
}

std::string requirement_key(const Requirements& requirements) {
  return std::string(reinterpret_cast<const char*>(requirements.data()),
                     requirements.size());
}

void generate_repairs_recursive(const Graph& parent, bool want_edge,
                                Requirements& requirements, Repair& current,
                                std::vector<Repair>& output) {
  int first = -1;
  int endpoint_sum = 0;
  for (int vertex = 0; vertex < kOrder; ++vertex) {
    endpoint_sum += requirements[vertex];
    if (first < 0 && requirements[vertex]) first = vertex;
  }
  if (endpoint_sum == 0) {
    output.push_back(current);
    return;
  }
  if (endpoint_sum % 2) return;
  const int needed = requirements[first];
  std::vector<int> candidates;
  for (int vertex = 0; vertex < kOrder; ++vertex) {
    if (vertex == first || requirements[vertex] == 0) continue;
    const bool edge = (parent[first] >> vertex) & 1U;
    if (edge == want_edge) candidates.push_back(vertex);
  }
  if (static_cast<int>(candidates.size()) < needed) return;
  requirements[first] = 0;
  std::function<void(int, int)> choose = [&](int start, int remaining) {
    if (remaining == 0) {
      generate_repairs_recursive(parent, want_edge, requirements, current,
                                 output);
      return;
    }
    if (static_cast<int>(candidates.size()) - start < remaining) return;
    for (int index = start;
         index <= static_cast<int>(candidates.size()) - remaining; ++index) {
      const int neighbor = candidates[index];
      if (requirements[neighbor] == 0) continue;
      --requirements[neighbor];
      current.edges[current.size++] = edge_code(first, neighbor);
      choose(index + 1, remaining - 1);
      --current.size;
      ++requirements[neighbor];
    }
  };
  choose(0, needed);
  requirements[first] = static_cast<std::uint8_t>(needed);
}

const std::vector<Repair>& repair_realizations(const Graph& parent,
                                               bool want_edge,
                                               const Requirements& requirements,
                                               RepairCache& cache) {
  const std::string key = requirement_key(requirements);
  const auto found = cache.find(key);
  if (found != cache.end()) return found->second;
  Requirements mutable_requirements = requirements;
  Repair current;
  std::vector<Repair> output;
  generate_repairs_recursive(parent, want_edge, mutable_requirements, current,
                             output);
  return cache.emplace(key, std::move(output)).first->second;
}

Graph apply_repairs(const Graph& parent, const Repair& additions,
                    const Repair& deletions) {
  Graph result = parent;
  auto apply = [&](const Repair& repair) {
    for (int index = 0; index < repair.size; ++index) {
      const auto [first, second] = decode_edge(repair.edges[index]);
      result[first] ^= std::uint64_t{1} << second;
      result[second] ^= std::uint64_t{1} << first;
    }
  };
  apply(additions);
  apply(deletions);
  return result;
}

bool is_ramsey_local(const Graph& repaired, const Repair& additions,
                     const Repair& deletions) {
  for (int index = 0; index < additions.size; ++index) {
    const auto [first, second] = decode_edge(additions.edges[index]);
    if (contains_triangle(repaired, repaired[first] & repaired[second])) {
      return false;
    }
  }
  const Graph blue = complement(repaired, kOrder);
  for (int index = 0; index < deletions.size; ++index) {
    const auto [first, second] = decode_edge(deletions.edges[index]);
    if (contains_triangle(blue, blue[first] & blue[second])) return false;
  }
  return true;
}

std::vector<int> extension_vertices(const Graph& graph) {
  std::vector<int> low;
  for (int vertex = 0; vertex < kOrder; ++vertex) {
    const int degree = std::popcount(graph[vertex]);
    if (degree == 20) low.push_back(vertex);
    else if (degree != 21) throw std::runtime_error("wrong target degree");
  }
  if (low.size() != 22) throw std::runtime_error("wrong target degree counts");
  std::uint64_t low_mask = 0;
  for (int vertex : low) low_mask |= std::uint64_t{1} << vertex;
  const std::uint64_t all = (std::uint64_t{1} << kOrder) - 1;
  const Graph blue = complement(graph, kOrder);
  std::vector<int> answer;
  for (int z : low) {
    const std::uint64_t red_side = low_mask ^ (std::uint64_t{1} << z);
    const std::uint64_t blue_side = all ^ red_side;
    if (contains_clique(graph, kOrder, 4, red_side)) continue;
    if (contains_clique(blue, kOrder, 4, blue_side)) continue;
    answer.push_back(z);
  }
  return answer;
}

Graph extend_and_validate(const Graph& graph, int z) {
  if (contains_clique(graph, kOrder, 5) ||
      contains_clique(complement(graph, kOrder), kOrder, 5)) {
    throw std::runtime_error("local/global Ramsey disagreement");
  }
  Graph extended = graph;
  for (int vertex = 0; vertex < kOrder; ++vertex) {
    if (std::popcount(graph[vertex]) == 20 && vertex != z) {
      extended[vertex] |= std::uint64_t{1} << kOrder;
      extended[kOrder] |= std::uint64_t{1} << vertex;
    }
  }
  if (std::popcount(extended[kOrder]) != 21) {
    throw std::runtime_error("wrong singleton degree");
  }
  if (contains_clique(extended, kExtendedOrder, 5) ||
      contains_clique(complement(extended, kExtendedOrder), kExtendedOrder, 5)) {
    throw std::runtime_error("invalid 43-vertex extension");
  }
  return extended;
}

void choose_subset(const std::vector<int>& pool, int needed, int start,
                   std::vector<int>& chosen,
                   const std::function<void(const std::vector<int>&)>& emit) {
  if (needed == 0) {
    emit(chosen);
    return;
  }
  if (static_cast<int>(pool.size()) - start < needed) return;
  for (int index = start; index <= static_cast<int>(pool.size()) - needed;
       ++index) {
    chosen.push_back(pool[index]);
    choose_subset(pool, needed - 1, index + 1, chosen, emit);
    chosen.pop_back();
  }
}

std::string repair_text(const Repair& repair) {
  std::string answer;
  for (int index = 0; index < repair.size; ++index) {
    const auto [first, second] = decode_edge(repair.edges[index]);
    if (!answer.empty()) answer += ';';
    answer += std::to_string(first) + ',' + std::to_string(second);
  }
  return answer;
}

struct SearchResult {
  std::uint64_t candidates = 0;
  std::uint64_t ramsey42 = 0;
  std::uint64_t extensions = 0;
};

SearchResult search(const Graph& parent, int parent_index,
                    const std::string& orientation) {
  std::array<int, kOrder> degrees{};
  std::vector<int> high;
  std::vector<int> low;
  int all_low_cost = 0;
  for (int vertex = 0; vertex < kOrder; ++vertex) {
    degrees[vertex] = std::popcount(parent[vertex]);
    all_low_cost += std::abs(20 - degrees[vertex]);
    (degrees[vertex] >= 21 ? high : low).push_back(vertex);
  }
  const int minimum_low = std::max(0, 20 - static_cast<int>(high.size()));
  const int maximum_low = std::min(static_cast<int>(low.size()), 20);
  RepairCache additions_cache;
  RepairCache deletions_cache;
  int requirement_index = 0;
  SearchResult result;

  for (int low_chosen_count = minimum_low; low_chosen_count <= maximum_low;
       ++low_chosen_count) {
    const int high_chosen_count = 20 - low_chosen_count;
    const int endpoint_cost =
        all_low_cost + low_chosen_count - high_chosen_count;
    if (endpoint_cost > 2 * kRadius) break;
    if ((2 * kRadius - endpoint_cost) % 2) {
      throw std::runtime_error("endpoint parity mismatch");
    }
    const int cancellations = (2 * kRadius - endpoint_cost) / 2;
    if (cancellations < 0 || cancellations > 2) {
      throw std::runtime_error("unsupported cancellation total");
    }
    std::vector<int> chosen_high;
    choose_subset(high, high_chosen_count, 0, chosen_high,
      [&](const std::vector<int>& high_choice) {
        std::vector<int> chosen_low;
        choose_subset(low, low_chosen_count, 0, chosen_low,
          [&](const std::vector<int>& low_choice) {
            std::array<bool, kOrder> target_high{};
            for (int vertex : high_choice) target_high[vertex] = true;
            for (int vertex : low_choice) target_high[vertex] = true;
            std::array<int, kOrder> changes{};
            int checked_cost = 0;
            for (int vertex = 0; vertex < kOrder; ++vertex) {
              changes[vertex] = (target_high[vertex] ? 21 : 20) - degrees[vertex];
              checked_cost += std::abs(changes[vertex]);
            }
            if (checked_cost != endpoint_cost) {
              throw std::runtime_error("target assignment cost mismatch");
            }
            auto process_cancellation = [&](int first, int second) {
              Requirements add{};
              Requirements del{};
              for (int vertex = 0; vertex < kOrder; ++vertex) {
                int q = 0;
                if (first == vertex) ++q;
                if (second == vertex) ++q;
                add[vertex] = static_cast<std::uint8_t>(
                    std::max(changes[vertex], 0) + q);
                del[vertex] = static_cast<std::uint8_t>(
                    std::max(-changes[vertex], 0) + q);
              }
              if (requirement_index && requirement_index % kCacheBlock == 0) {
                additions_cache.clear();
                deletions_cache.clear();
              }
              ++requirement_index;
              const auto& additions = repair_realizations(
                  parent, false, add, additions_cache);
              const auto& deletions = repair_realizations(
                  parent, true, del, deletions_cache);
              for (const Repair& addition : additions) {
                for (const Repair& deletion : deletions) {
                  if (addition.size + deletion.size != kRadius) {
                    throw std::runtime_error("wrong repair size");
                  }
                  ++result.candidates;
                  const Graph repaired = apply_repairs(parent, addition, deletion);
                  if (is_ramsey_local(repaired, addition, deletion)) {
                    ++result.ramsey42;
                    std::cout << "RAMSEY42 parent=" << parent_index
                              << " orientation=" << orientation
                              << " additions=" << repair_text(addition)
                              << " deletions=" << repair_text(deletion)
                              << " graph6=" << encode_graph6(repaired, kOrder)
                              << '\n';
                    for (int z : extension_vertices(repaired)) {
                      ++result.extensions;
                      const Graph extended = extend_and_validate(repaired, z);
                      std::cout << "CERTIFIED R55_43 parent=" << parent_index
                                << " orientation=" << orientation << " z=" << z
                                << " graph6="
                                << encode_graph6(extended, kExtendedOrder) << '\n';
                    }
                    std::cout.flush();
                  }
                  if (result.candidates % kProgressEvery == 0) {
                    std::cout << "PROGRESS parent=" << parent_index
                              << " orientation=" << orientation
                              << " candidates=" << result.candidates
                              << " ramsey42=" << result.ramsey42
                              << " extensions=" << result.extensions << '\n';
                    std::cout.flush();
                  }
                }
              }
            };
            if (cancellations == 0) {
              process_cancellation(-1, -1);
            } else if (cancellations == 1) {
              for (int first = 0; first < kOrder; ++first) {
                process_cancellation(first, -1);
              }
            } else {
              for (int first = 0; first < kOrder; ++first) {
                for (int second = first; second < kOrder; ++second) {
                  process_cancellation(first, second);
                }
              }
            }
          });
      });
  }
  return result;
}

}  // namespace

int main(int argc, char** argv) {
  try {
    if (argc != 4) {
      std::cerr << "usage: " << argv[0]
                << " CATALOG.g6 PARENT (base|complement)\n";
      return 2;
    }
    const int wanted_parent = std::stoi(argv[2]);
    const std::string orientation = argv[3];
    if (wanted_parent < 0 || wanted_parent >= 328 ||
        (orientation != "base" && orientation != "complement")) {
      throw std::runtime_error("bad parent or orientation argument");
    }
    std::ifstream input(argv[1]);
    if (!input) throw std::runtime_error("cannot open catalog");
    std::string line;
    Graph parent{};
    int index = 0;
    bool found = false;
    while (std::getline(input, line)) {
      if (index == wanted_parent) {
        parent = decode_graph6(line);
        found = true;
      }
      ++index;
    }
    if (index != 328 || !found) throw std::runtime_error("wrong catalog count");
    if (orientation == "complement") parent = complement(parent, kOrder);

    std::vector<int> degrees;
    int degree_sum = 0;
    for (int vertex = 0; vertex < kOrder; ++vertex) {
      degrees.push_back(std::popcount(parent[vertex]));
      degree_sum += degrees.back();
    }
    std::sort(degrees.begin(), degrees.end());
    std::vector<int> target(22, 20);
    target.insert(target.end(), 20, 21);
    int l1 = 0;
    for (int vertex = 0; vertex < kOrder; ++vertex) {
      l1 += std::abs(degrees[vertex] - target[vertex]);
    }
    const int lower_bound = l1 / 2;
    const int edges = degree_sum / 2;
    const int edge_difference = kTargetEdges - edges;
    if (l1 % 2 || lower_bound > kRadius ||
        std::abs(edge_difference) > kRadius ||
        std::abs(edge_difference) % 2 != kRadius % 2) {
      throw std::runtime_error("selected orientation is not radius-seven eligible");
    }
    const SearchResult result = search(parent, wanted_parent, orientation);
    std::cout << "PASS parent=" << wanted_parent
              << " orientation=" << orientation << " edges=" << edges
              << " degree_lower_bound=" << lower_bound
              << " candidates=" << result.candidates
              << " Ramsey42=" << result.ramsey42
              << " extensions=" << result.extensions << '\n';
  } catch (const std::exception& error) {
    std::cerr << "ERROR " << error.what() << '\n';
    return 1;
  }
  return 0;
}
