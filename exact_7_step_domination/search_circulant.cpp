#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <numeric>
#include <queue>
#include <random>
#include <set>
#include <stdexcept>
#include <tuple>
#include <vector>

namespace {

struct Evaluation {
  int error;
  int sphere_size;
  int diameter_lower_bound;
};

Evaluation evaluate(int order, const std::vector<int>& generators, int radius) {
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
  const int quotient_order = order / 4;
  std::vector<int> count(quotient_order, 0);
  int sphere_size = 0;
  for (int vertex = 0; vertex < order; ++vertex) {
    if (distance[vertex] == radius) {
      ++count[vertex % quotient_order];
      ++sphere_size;
    }
  }
  int error = 0;
  for (int multiplicity : count) {
    error += std::abs(multiplicity - 1);
  }
  return {error, sphere_size,
          *std::max_element(distance.begin(), distance.end())};
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

void print_result(int order, const std::vector<int>& generators,
                  const Evaluation& evaluation) {
  std::cout << "order=" << order << " generators=";
  for (std::size_t i = 0; i < generators.size(); ++i) {
    std::cout << (i == 0 ? "[" : ",") << generators[i];
  }
  std::cout << "] error=" << evaluation.error
            << " sphere_size=" << evaluation.sphere_size << "\n";
}

}  // namespace

int main(int argc, char** argv) {
  if (argc != 5) {
    std::cerr << "usage: search_circulant GENERATOR_COUNT TRIALS SEED MAX_ORDER\n";
    return 2;
  }
  const int generator_count = std::stoi(argv[1]);
  const std::uint64_t trials = std::stoull(argv[2]);
  const std::uint64_t seed = std::stoull(argv[3]);
  const int max_order = std::stoi(argv[4]);
  if (generator_count < 2 || generator_count > 8 || max_order < 32) {
    throw std::invalid_argument("unsupported parameter");
  }

  std::mt19937_64 random(seed);
  Evaluation best{1000000000, 0, 0};
  int best_order = 0;
  std::vector<int> best_generators;
  for (std::uint64_t trial = 0; trial < trials; ++trial) {
    int order = 32 + 4 * static_cast<int>(random() % ((max_order - 28) / 4));
    std::vector<int> generators;
    do {
      generators.clear();
      for (int i = 0; i < generator_count; ++i) {
        generators.push_back(1 + static_cast<int>(random() % (order / 2)));
      }
      generators = normalize(order, generators);
    } while (static_cast<int>(generators.size()) != generator_count ||
             !connected(order, generators));

    Evaluation current = evaluate(order, generators, 7);
    if (current.error < best.error ||
        (current.error == best.error && current.sphere_size > best.sphere_size)) {
      best = current;
      best_order = order;
      best_generators = generators;
      print_result(best_order, best_generators, best);
    }
    if (current.error == 0) {
      std::cout << "FOUND exact radius-7 transversal\n";
      return 0;
    }
  }
  std::cout << "BEST ";
  print_result(best_order, best_generators, best);
  return 1;
}
