#include <algorithm>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <queue>
#include <random>
#include <stdexcept>
#include <vector>

namespace {

std::vector<int> radius_sphere(int order, const std::vector<int>& generators,
                               int radius) {
  std::vector<int> distance(order, -1);
  std::queue<int> queue;
  distance[0] = 0;
  queue.push(0);
  while (!queue.empty()) {
    const int vertex = queue.front();
    queue.pop();
    if (distance[vertex] == radius) {
      continue;
    }
    for (int generator : generators) {
      for (int sign : {-1, 1}) {
        int next = (vertex + sign * generator) % order;
        if (next < 0) {
          next += order;
        }
        if (distance[next] == -1) {
          distance[next] = distance[vertex] + 1;
          queue.push(next);
        }
      }
    }
  }
  std::vector<int> sphere;
  for (int vertex = 0; vertex < order; ++vertex) {
    if (distance[vertex] == radius) {
      sphere.push_back(vertex);
    }
  }
  return sphere;
}

bool tile_recursively(int order, const std::vector<int>& sphere,
                      std::vector<bool>& covered, std::vector<int>& shifts,
                      int remaining) {
  if (remaining == 0) {
    return std::all_of(covered.begin(), covered.end(), [](bool x) { return x; });
  }
  int first_uncovered = 0;
  while (first_uncovered < order && covered[first_uncovered]) {
    ++first_uncovered;
  }
  if (first_uncovered == order) {
    return false;
  }
  for (int element : sphere) {
    int shift = first_uncovered - element;
    if (shift < 0) {
      shift += order;
    }
    bool disjoint = true;
    for (int x : sphere) {
      if (covered[(x + shift) % order]) {
        disjoint = false;
        break;
      }
    }
    if (!disjoint) {
      continue;
    }
    for (int x : sphere) {
      covered[(x + shift) % order] = true;
    }
    shifts.push_back(shift);
    if (tile_recursively(order, sphere, covered, shifts, remaining - 1)) {
      return true;
    }
    shifts.pop_back();
    for (int x : sphere) {
      covered[(x + shift) % order] = false;
    }
  }
  return false;
}

bool four_translate_tiling(int order, const std::vector<int>& sphere,
                           std::vector<int>& shifts) {
  if (static_cast<int>(sphere.size()) * 4 != order) {
    return false;
  }
  std::vector<bool> covered(order, false);
  for (int x : sphere) {
    covered[x] = true;
  }
  shifts = {0};
  return tile_recursively(order, sphere, covered, shifts, 3);
}

std::vector<int> normalize(int order, std::vector<int> generators) {
  for (int& generator : generators) {
    generator %= order;
    if (generator < 0) {
      generator += order;
    }
    generator = std::min(generator, order - generator);
  }
  std::sort(generators.begin(), generators.end());
  generators.erase(std::unique(generators.begin(), generators.end()),
                   generators.end());
  return generators;
}

bool connected(int order, const std::vector<int>& generators) {
  int divisor = order;
  for (int generator : generators) {
    divisor = std::gcd(divisor, generator);
  }
  return divisor == 1;
}

void print_vector(const std::vector<int>& values) {
  std::cout << "[";
  for (std::size_t i = 0; i < values.size(); ++i) {
    std::cout << (i == 0 ? "" : ",") << values[i];
  }
  std::cout << "]";
}

}  // namespace

int main(int argc, char** argv) {
  if (argc != 5) {
    std::cerr << "usage: search_circulant_tiling GENERATOR_COUNT TRIALS SEED MAX_ORDER\n";
    return 2;
  }
  const int generator_count = std::stoi(argv[1]);
  const std::uint64_t trials = std::stoull(argv[2]);
  const std::uint64_t seed = std::stoull(argv[3]);
  const int max_order = std::stoi(argv[4]);
  std::mt19937_64 random(seed);
  int best_error = 1000000000;

  for (std::uint64_t trial = 0; trial < trials; ++trial) {
    const int order = 32 + 4 * static_cast<int>(random() % ((max_order - 28) / 4));
    std::vector<int> generators;
    do {
      generators.clear();
      for (int i = 0; i < generator_count; ++i) {
        generators.push_back(1 + static_cast<int>(random() % (order / 2)));
      }
      generators = normalize(order, generators);
    } while (static_cast<int>(generators.size()) != generator_count ||
             !connected(order, generators));

    const std::vector<int> sphere = radius_sphere(order, generators, 7);
    const int error = std::abs(4 * static_cast<int>(sphere.size()) - order);
    if (error < best_error) {
      best_error = error;
      std::cout << "trial=" << trial << " order=" << order << " generators=";
      print_vector(generators);
      std::cout << " sphere_size=" << sphere.size() << " size_error=" << error
                << "\n" << std::flush;
    }
    if (error != 0) {
      continue;
    }
    std::vector<int> shifts;
    if (four_translate_tiling(order, sphere, shifts)) {
      std::cout << "FOUND order=" << order << " generators=";
      print_vector(generators);
      std::cout << " centers=";
      print_vector(shifts);
      std::cout << " sphere=";
      print_vector(sphere);
      std::cout << "\n" << std::flush;
      return 0;
    }
  }
  return 1;
}
