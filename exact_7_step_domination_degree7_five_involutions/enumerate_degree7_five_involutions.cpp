#include <algorithm>
#include <array>
#include <bit>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <queue>
#include <set>
#include <stdexcept>
#include <vector>

namespace {

constexpr int kRadius = 7;
constexpr int kMaximumOrder = 6 * 64;

std::vector<std::uint32_t> binary_subspaces() {
  std::set<std::uint32_t> subspaces = {1U};
  for (int dimension = 0; dimension < 5; ++dimension) {
    auto enlarged = subspaces;
    for (std::uint32_t subspace : subspaces) {
      std::vector<int> elements;
      for (int value = 0; value < 32; ++value) {
        if (subspace & (1U << value)) elements.push_back(value);
      }
      for (int vector = 1; vector < 32; ++vector) {
        if (subspace & (1U << vector)) continue;
        std::uint32_t span = subspace;
        for (int element : elements) span |= 1U << (element ^ vector);
        enlarged.insert(span);
      }
    }
    subspaces = std::move(enlarged);
  }
  return {subspaces.begin(), subspaces.end()};
}

bool distinct_nonzero_basis_images(std::uint32_t kernel) {
  for (int i = 0; i < 5; ++i) {
    if (kernel & (1U << (1 << i))) return false;
    for (int j = i + 1; j < 5; ++j) {
      if (kernel & (1U << ((1 << i) ^ (1 << j)))) return false;
    }
  }
  return true;
}

class BinaryQuotient {
 public:
  explicit BinaryQuotient(std::uint32_t kernel) : kernel_(kernel) {
    representative_.fill(-1);
    index_.fill(-1);
    for (int value = 0; value < 32; ++value) {
      int representative = 32;
      for (int element = 0; element < 32; ++element) {
        if (kernel_ & (1U << element)) {
          representative = std::min(representative, value ^ element);
        }
      }
      representative_[value] = representative;
    }
    for (int value = 0; value < 32; ++value) {
      if (representative_[value] == value) {
        index_[value] = static_cast<int>(representatives_.size());
        representatives_.push_back(value);
      }
    }
    for (int value = 0; value < 32; ++value) {
      index_[value] = index_[representative_[value]];
    }
  }

  int order() const { return static_cast<int>(representatives_.size()); }
  std::uint32_t kernel() const { return kernel_; }
  int coset(int vector) const { return index_[vector]; }
  int representative(int coset) const { return representatives_[coset]; }
  int add(int left, int right) const {
    return coset(representative(left) ^ representative(right));
  }

 private:
  std::uint32_t kernel_;
  std::array<int, 32> representative_{};
  std::array<int, 32> index_{};
  std::vector<int> representatives_;
};

class Model {
 public:
  Model(BinaryQuotient quotient, int generator_order, int intersection_vector)
      : quotient_(std::move(quotient)),
        generator_order_(generator_order),
        intersection_coset_(intersection_vector < 0
                                ? -1
                                : quotient_.coset(intersection_vector)),
        cyclic_size_(intersection_vector < 0 ? generator_order
                                             : generator_order / 2) {
    if (generator_order_ < 3 || cyclic_size_ < 2) {
      throw std::runtime_error("invalid generator order");
    }
    if (intersection_coset_ == 0) {
      throw std::runtime_error("trivial intersection vector");
    }
  }

  int order() const { return cyclic_size_ * quotient_.order(); }
  int generator_order() const { return generator_order_; }
  int intersection_vector() const {
    return intersection_coset_ < 0
               ? -1
               : quotient_.representative(intersection_coset_);
  }
  const BinaryQuotient& quotient() const { return quotient_; }

  int encode(int cyclic, int binary_coset) const {
    return cyclic * quotient_.order() + binary_coset;
  }
  std::array<int, 2> decode(int element) const {
    return {element / quotient_.order(), element % quotient_.order()};
  }
  int add(int left, int right) const {
    const auto a = decode(left);
    const auto b = decode(right);
    int cyclic = a[0] + b[0];
    int binary = quotient_.add(a[1], b[1]);
    if (cyclic >= cyclic_size_) {
      cyclic -= cyclic_size_;
      if (intersection_coset_ >= 0) {
        binary = quotient_.add(binary, intersection_coset_);
      }
    }
    return encode(cyclic, binary);
  }
  int inverse(int element) const {
    const auto value = decode(element);
    if (value[0] == 0) return element;
    int binary = value[1];
    if (intersection_coset_ >= 0) {
      binary = quotient_.add(binary, intersection_coset_);
    }
    return encode(cyclic_size_ - value[0], binary);
  }
  int subtract(int left, int right) const { return add(left, inverse(right)); }

  std::vector<int> steps() const {
    const int generator = encode(1, 0);
    std::vector<int> result = {generator, inverse(generator)};
    for (int i = 0; i < 5; ++i) {
      result.push_back(encode(0, quotient_.coset(1 << i)));
    }
    std::sort(result.begin(), result.end());
    result.erase(std::unique(result.begin(), result.end()), result.end());
    if (result.size() != 7 || result.front() == 0) {
      throw std::runtime_error("connection set is not simple degree seven");
    }
    return result;
  }

 private:
  BinaryQuotient quotient_;
  int generator_order_;
  int intersection_coset_;
  int cyclic_size_;
};

std::vector<int> radius_sphere(const Model& model) {
  const auto steps = model.steps();
  std::vector<int> distance(model.order(), -1);
  std::queue<int> queue;
  distance[0] = 0;
  queue.push(0);
  while (!queue.empty()) {
    const int element = queue.front();
    queue.pop();
    for (int step : steps) {
      const int neighbour = model.add(element, step);
      if (distance[neighbour] != -1) continue;
      distance[neighbour] = distance[element] + 1;
      queue.push(neighbour);
    }
  }
  std::vector<int> sphere;
  for (int element = 0; element < model.order(); ++element) {
    if (distance[element] == kRadius) sphere.push_back(element);
  }
  return sphere;
}

bool clique_search(const Model& model, const std::vector<int>& candidates,
                   const std::vector<std::uint8_t>& forbidden, int start,
                   int remaining, std::vector<int>& chosen) {
  if (remaining == 0) return true;
  if (static_cast<int>(candidates.size()) - start < remaining) return false;
  for (int index = start;
       index + remaining <= static_cast<int>(candidates.size()); ++index) {
    const int candidate = candidates[index];
    bool compatible = true;
    for (int previous : chosen) {
      if (forbidden[model.subtract(candidate, previous)]) {
        compatible = false;
        break;
      }
    }
    if (!compatible) continue;
    chosen.push_back(candidate);
    if (clique_search(model, candidates, forbidden, index + 1,
                      remaining - 1, chosen)) {
      return true;
    }
    chosen.pop_back();
  }
  return false;
}

bool has_translate_tiling(const Model& model, const std::vector<int>& sphere,
                          int center_count) {
  if (center_count * static_cast<int>(sphere.size()) != model.order()) {
    return false;
  }
  std::vector<std::uint8_t> forbidden(model.order(), 0);
  for (int left : sphere) {
    for (int right : sphere) {
      forbidden[model.subtract(left, right)] = 1;
    }
  }
  std::vector<int> candidates;
  for (int shift = 1; shift < model.order(); ++shift) {
    if (!forbidden[shift]) candidates.push_back(shift);
  }
  std::vector<int> chosen;
  return clique_search(model, candidates, forbidden, 0, center_count - 1,
                       chosen);
}

}  // namespace

int main(int argc, char** argv) {
  if (argc != 2) {
    throw std::runtime_error("usage: enumerator /scratch/candidates.txt");
  }
  std::ofstream output(argv[1]);
  if (!output) throw std::runtime_error("could not open candidate output");

  const auto all_subspaces = binary_subspaces();
  if (all_subspaces.size() != 374) {
    throw std::runtime_error("unexpected binary-subspace count");
  }
  std::uint64_t valid_kernels = 0;
  std::uint64_t split_models = 0;
  std::uint64_t nonsplit_models = 0;
  std::uint64_t four_candidates = 0;
  std::uint64_t six_candidates = 0;
  std::uint64_t four_tilings = 0;
  std::uint64_t six_tilings = 0;

  for (std::uint32_t kernel : all_subspaces) {
    if (!distinct_nonzero_basis_images(kernel)) continue;
    ++valid_kernels;
    const BinaryQuotient quotient(kernel);

    auto evaluate = [&](const Model& model, bool split) {
      if (model.order() % 4 != 0 && model.order() % 6 != 0) return;
      if (split) {
        ++split_models;
      } else {
        ++nonsplit_models;
      }
      const auto sphere = radius_sphere(model);
      auto candidate = [&](int center_count) {
        output << center_count << ' ' << model.generator_order() << ' '
               << model.quotient().kernel() << ' '
               << model.intersection_vector() << ' ' << sphere.size()
               << '\n';
        return has_translate_tiling(model, sphere, center_count);
      };
      if (4 * static_cast<int>(sphere.size()) == model.order()) {
        ++four_candidates;
        four_tilings += candidate(4) ? 1 : 0;
      }
      if (6 * static_cast<int>(sphere.size()) == model.order()) {
        ++six_candidates;
        six_tilings += candidate(6) ? 1 : 0;
      }
    };

    for (int generator_order = 3;
         generator_order * quotient.order() <= kMaximumOrder;
         ++generator_order) {
      evaluate(Model(quotient, generator_order, -1), true);
    }
    for (int intersection = 1; intersection < 32; ++intersection) {
      if (quotient.representative(quotient.coset(intersection)) !=
          intersection) {
        continue;
      }
      for (int generator_order = 4;
           generator_order * quotient.order() / 2 <= kMaximumOrder;
           generator_order += 2) {
        evaluate(Model(quotient, generator_order, intersection), false);
      }
    }
  }

  output.flush();
  if (!output) throw std::runtime_error("candidate output failure");
  std::cout << "radius=" << kRadius << '\n';
  std::cout << "maximum_group_order=" << kMaximumOrder << '\n';
  std::cout << "binary_subspaces=" << all_subspaces.size() << '\n';
  std::cout << "valid_relation_kernels=" << valid_kernels << '\n';
  std::cout << "split_models=" << split_models << '\n';
  std::cout << "nonsplit_models=" << nonsplit_models << '\n';
  std::cout << "four_center_counting_candidates=" << four_candidates << '\n';
  std::cout << "six_center_counting_candidates=" << six_candidates << '\n';
  std::cout << "four_center_tilings=" << four_tilings << '\n';
  std::cout << "six_center_tilings=" << six_tilings << '\n';
  if (valid_kernels != 32 || split_models != 1052 ||
      nonsplit_models != 10796 || four_candidates != 0 ||
      six_candidates != 61 || four_tilings != 0 || six_tilings != 0) {
    throw std::runtime_error("unexpected complete-enumeration result");
  }
}
