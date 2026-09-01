#include <algorithm>
#include <array>
#include <bit>
#include <cstdint>
#include <iostream>
#include <map>
#include <set>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

// Exhaustive classifier for Hamming-translation-invariant square-saturated
// subgraphs of Q_7.  An H-orbit of Q_7 edges is an edge of the complete graph
// on the syndrome space F_2^3.  A square orbit is one of the 42 Hamilton cycles
// inside the 14 affine planes of F_2^3.

namespace {

using Mask = std::uint32_t;

struct Quotient {
  std::array<std::array<int, 8>, 8> edge_index{};
  std::vector<std::pair<int, int>> edges;
  std::vector<Mask> planes;
  std::vector<Mask> cycles;
  std::array<std::vector<Mask>, 28> witness_triples;
};

void require(bool condition, const std::string &message) {
  if (!condition) throw std::runtime_error(message);
}

Quotient make_quotient() {
  Quotient quotient;
  for (int x = 0; x < 8; ++x) {
    for (int y = x + 1; y < 8; ++y) {
      quotient.edge_index[x][y] = quotient.edge_index[y][x] =
          static_cast<int>(quotient.edges.size());
      quotient.edges.emplace_back(x, y);
    }
  }
  require(quotient.edges.size() == 28, "K_8 should have 28 edges");

  std::set<std::array<int, 4>> plane_set;
  for (int x = 0; x < 8; ++x) {
    for (int a = 1; a < 8; ++a) {
      for (int b = a + 1; b < 8; ++b) {
        std::array<int, 4> plane{x, x ^ a, x ^ b, x ^ a ^ b};
        std::sort(plane.begin(), plane.end());
        plane_set.insert(plane);
      }
    }
  }
  require(plane_set.size() == 14, "AG(3,2) should have 14 affine planes");

  std::set<Mask> cycle_set;
  for (const auto &plane_vertices : plane_set) {
    Mask plane_mask = 0;
    for (int i = 0; i < 4; ++i) {
      for (int j = i + 1; j < 4; ++j) {
        plane_mask |= Mask{1} << quotient.edge_index[plane_vertices[i]][plane_vertices[j]];
      }
    }
    quotient.planes.push_back(plane_mask);

    // Fix the least vertex and permute the other three.  Reversal duplicates
    // each cycle, and the set removes those duplicates, leaving three cycles.
    std::array<int, 3> tail{plane_vertices[1], plane_vertices[2], plane_vertices[3]};
    do {
      const std::array<int, 4> order{
          plane_vertices[0], tail[0], tail[1], tail[2]};
      Mask cycle_mask = 0;
      for (int i = 0; i < 4; ++i) {
        cycle_mask |= Mask{1} << quotient.edge_index[order[i]][order[(i + 1) % 4]];
      }
      cycle_set.insert(cycle_mask);
    } while (std::next_permutation(tail.begin(), tail.end()));
  }
  quotient.cycles.assign(cycle_set.begin(), cycle_set.end());
  require(quotient.cycles.size() == 42, "there should be 42 affine 4-cycles");

  for (Mask cycle : quotient.cycles) {
    require(std::popcount(cycle) == 4, "cycle mask should contain four edges");
    for (int edge = 0; edge < 28; ++edge) {
      const Mask bit = Mask{1} << edge;
      if (cycle & bit) quotient.witness_triples[edge].push_back(cycle ^ bit);
    }
  }
  for (const auto &triples : quotient.witness_triples) {
    require(triples.size() == 6, "every quotient edge should have six witnesses");
  }
  return quotient;
}

bool square_free(const Quotient &quotient, Mask selected) {
  for (Mask cycle : quotient.cycles) {
    if ((selected & cycle) == cycle) return false;
  }
  return true;
}

Mask witnessed_missing_edges(const Quotient &quotient, Mask selected) {
  const Mask universe = (Mask{1} << 28) - 1;
  const Mask missing = universe ^ selected;
  Mask witnessed = 0;
  for (int edge = 0; edge < 28; ++edge) {
    const Mask bit = Mask{1} << edge;
    if (!(missing & bit)) continue;
    for (Mask triple : quotient.witness_triples[edge]) {
      if ((selected & triple) == triple) {
        witnessed |= bit;
        break;
      }
    }
  }
  return witnessed;
}

bool saturated(const Quotient &quotient, Mask selected) {
  const Mask universe = (Mask{1} << 28) - 1;
  return square_free(quotient, selected) &&
         witnessed_missing_edges(quotient, selected) == (universe ^ selected);
}

struct Census {
  std::uint64_t examined = 0;
  std::uint64_t square_free = 0;
  std::uint64_t saturated = 0;
  int maximum_witnessed = 0;
  std::set<Mask> solutions;
};

Census census_weight(const Quotient &quotient, int weight, bool save_solutions) {
  Census result;
  Mask combination = (Mask{1} << weight) - 1;
  const Mask limit = Mask{1} << 28;
  const Mask universe = limit - 1;
  while (combination < limit) {
    ++result.examined;
    if (square_free(quotient, combination)) {
      ++result.square_free;
      const Mask witnessed = witnessed_missing_edges(quotient, combination);
      result.maximum_witnessed = std::max(result.maximum_witnessed,
                                           static_cast<int>(std::popcount(witnessed)));
      if (witnessed == (universe ^ combination)) {
        ++result.saturated;
        if (save_solutions) result.solutions.insert(combination);
      }
    }

    // Gosper's hack: the next 28-bit word of the same Hamming weight.
    const Mask low = combination & -combination;
    const Mask ripple = combination + low;
    if (ripple == 0 || ripple >= limit) break;
    combination = ripple | (((ripple ^ combination) >> 2) / low);
  }
  return result;
}

Mask edge_mask(const Quotient &quotient, int x, int y) {
  require(x != y, "loops are not quotient edges");
  return Mask{1} << quotient.edge_index[x][y];
}

bool linearly_independent(int a, int b, int c) {
  std::set<int> span{0, a, b, c, a ^ b, a ^ c, b ^ c, a ^ b ^ c};
  return span.size() == 8;
}

Mask family_member(const Quotient &quotient, int pendant, int universal,
                   const std::array<int, 3> &basis) {
  require(pendant != universal, "distinguished vertices must differ");
  require(linearly_independent(basis[0], basis[1], basis[2]), "basis must have rank three");
  require((basis[0] ^ basis[1] ^ basis[2]) == (pendant ^ universal),
          "basis sum must equal the distinguished difference");

  Mask selected = 0;
  for (int vertex = 0; vertex < 8; ++vertex) {
    if (vertex != universal) selected |= edge_mask(quotient, universal, vertex);
  }
  std::array<int, 3> leaves;
  std::array<int, 3> triangle;
  for (int i = 0; i < 3; ++i) {
    leaves[i] = pendant ^ basis[i];
    triangle[i] = universal ^ basis[i];
    selected |= edge_mask(quotient, leaves[i], triangle[i]);
  }
  for (int i = 0; i < 3; ++i) {
    for (int j = i + 1; j < 3; ++j) {
      selected |= edge_mask(quotient, triangle[i], triangle[j]);
    }
  }
  require(std::popcount(selected) == 13, "family member should have 13 quotient edges");
  return selected;
}

std::set<Mask> explicit_family(const Quotient &quotient) {
  std::set<Mask> family;
  for (int pendant = 0; pendant < 8; ++pendant) {
    for (int universal = 0; universal < 8; ++universal) {
      if (pendant == universal) continue;
      const int difference = pendant ^ universal;
      for (int a = 1; a < 8; ++a) {
        for (int b = a + 1; b < 8; ++b) {
          for (int c = b + 1; c < 8; ++c) {
            if ((a ^ b ^ c) != difference || !linearly_independent(a, b, c)) continue;
            family.insert(family_member(quotient, pendant, universal, {a, b, c}));
          }
        }
      }
    }
  }
  return family;
}

std::vector<std::array<int, 8>> affine_permutations() {
  std::set<std::array<int, 8>> linear_maps;
  for (int a = 1; a < 8; ++a) {
    for (int b = 1; b < 8; ++b) {
      for (int c = 1; c < 8; ++c) {
        if (!linearly_independent(a, b, c)) continue;
        std::array<int, 8> map{};
        for (int x = 0; x < 8; ++x) {
          map[x] = ((x & 1) ? a : 0) ^ ((x & 2) ? b : 0) ^ ((x & 4) ? c : 0);
        }
        linear_maps.insert(map);
      }
    }
  }
  require(linear_maps.size() == 168, "GL(3,2) should have order 168");

  std::vector<std::array<int, 8>> affine_maps;
  for (const auto &linear : linear_maps) {
    for (int translation = 0; translation < 8; ++translation) {
      auto affine = linear;
      for (int &image : affine) image ^= translation;
      affine_maps.push_back(affine);
    }
  }
  require(affine_maps.size() == 1344, "AGL(3,2) should have order 1344");
  return affine_maps;
}

Mask transform(const Quotient &quotient, Mask selected, const std::array<int, 8> &map) {
  Mask image = 0;
  for (int edge = 0; edge < 28; ++edge) {
    if (!(selected & (Mask{1} << edge))) continue;
    const auto [x, y] = quotient.edges[edge];
    image |= edge_mask(quotient, map[x], map[y]);
  }
  return image;
}

std::array<int, 8> degree_sequence(const Quotient &quotient, Mask selected) {
  std::array<int, 8> degrees{};
  for (int edge = 0; edge < 28; ++edge) {
    if (!(selected & (Mask{1} << edge))) continue;
    const auto [x, y] = quotient.edges[edge];
    ++degrees[x];
    ++degrees[y];
  }
  std::sort(degrees.begin(), degrees.end());
  return degrees;
}

std::array<int, 5> plane_profile(const Quotient &quotient, Mask selected) {
  std::array<int, 5> profile{};
  for (Mask plane : quotient.planes) {
    const int count = std::popcount(selected & plane);
    require(count <= 4, "square-free plane cannot contain more than four edges");
    ++profile[count];
  }
  return profile;
}

}  // namespace

int main() try {
  const Quotient quotient = make_quotient();
  const Census weight12 = census_weight(quotient, 12, false);
  const Census weight13 = census_weight(quotient, 13, true);

  require(weight12.examined == 30421755, "wrong binomial count at weight 12");
  require(weight12.square_free == 9207240, "unexpected square-free count at weight 12");
  require(weight12.saturated == 0, "a 12-edge saturated quotient was found");
  require(weight12.maximum_witnessed == 13, "unexpected weight-12 witness maximum");
  require(weight13.examined == 37442160, "wrong binomial count at weight 13");
  require(weight13.square_free == 6124832, "unexpected square-free count at weight 13");
  require(weight13.saturated == 224, "unexpected number of weight-13 optima");

  const std::set<Mask> family = explicit_family(quotient);
  require(family.size() == 224, "explicit parameterization should contain 224 members");
  require(family == weight13.solutions, "explicit family does not equal exhaustive census");

  const Mask canonical = family_member(quotient, 0, 7, {1, 2, 4});
  require(saturated(quotient, canonical), "canonical family member is not saturated");
  const auto affine_maps = affine_permutations();
  std::set<Mask> orbit;
  int stabilizer_order = 0;
  for (const auto &map : affine_maps) {
    const Mask image = transform(quotient, canonical, map);
    orbit.insert(image);
    if (image == canonical) ++stabilizer_order;
  }
  require(orbit == weight13.solutions, "the optima do not form one AGL(3,2) orbit");
  require(stabilizer_order == 6, "unexpected affine stabilizer order");

  const std::array<int, 8> expected_degrees{1, 2, 2, 2, 4, 4, 4, 7};
  const std::array<int, 5> expected_planes{3, 0, 0, 5, 6};
  for (Mask solution : weight13.solutions) {
    require(degree_sequence(quotient, solution) == expected_degrees,
            "an optimum has the wrong degree sequence");
    require(plane_profile(quotient, solution) == expected_planes,
            "an optimum has the wrong affine-plane profile");
  }

  std::cout << "{\n"
            << "  \"affine_planes\": 14,\n"
            << "  \"affine_square_cycles\": 42,\n"
            << "  \"quotient_edges\": 28,\n"
            << "  \"weight_12_examined\": " << weight12.examined << ",\n"
            << "  \"weight_12_square_free\": " << weight12.square_free << ",\n"
            << "  \"weight_12_saturated\": " << weight12.saturated << ",\n"
            << "  \"weight_12_maximum_witnessed_missing_edges\": "
            << weight12.maximum_witnessed << ",\n"
            << "  \"weight_13_examined\": " << weight13.examined << ",\n"
            << "  \"weight_13_square_free\": " << weight13.square_free << ",\n"
            << "  \"weight_13_saturated\": " << weight13.saturated << ",\n"
            << "  \"explicit_family_size\": " << family.size() << ",\n"
            << "  \"agl_order\": " << affine_maps.size() << ",\n"
            << "  \"single_agl_orbit_size\": " << orbit.size() << ",\n"
            << "  \"affine_stabilizer_order\": " << stabilizer_order << ",\n"
            << "  \"quotient_degree_sequence\": [1, 2, 2, 2, 4, 4, 4, 7],\n"
            << "  \"affine_plane_edge_profile_n0_to_n4\": [3, 0, 0, 5, 6],\n"
            << "  \"status\": \"VERIFIED\"\n"
            << "}\n";
  return 0;
} catch (const std::exception &error) {
  std::cerr << "ERROR: " << error.what() << '\n';
  return 1;
}
