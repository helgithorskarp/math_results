// Clean-room exact audit of the P82 reflection-normalized anchor ledgers.
#include <algorithm>
#include <array>
#include <bit>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <numeric>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

using Mask = __uint128_t;

static int first(Mask x) {
  const auto low = static_cast<std::uint64_t>(x);
  return low ? std::countr_zero(low)
             : 64 + std::countr_zero(static_cast<std::uint64_t>(x >> 64));
}

static int pop(Mask x) {
  return std::popcount(static_cast<std::uint64_t>(x)) +
         std::popcount(static_cast<std::uint64_t>(x >> 64));
}

static bool sidon_by_differences(Mask x) {
  std::array<bool, 82> seen{};
  std::vector<int> points;
  while (x) {
    points.push_back(first(x));
    x &= x - 1;
  }
  for (std::size_t j = 0; j < points.size(); ++j)
    for (std::size_t i = 0; i < j; ++i) {
      const int d = points[j] - points[i];
      if (seen[static_cast<std::size_t>(d)])
        return false;
      seen[static_cast<std::size_t>(d)] = true;
    }
  return true;
}

static std::vector<Mask> read_sets(const std::string &path) {
  std::ifstream input(path);
  if (!input)
    throw std::runtime_error("cannot open set catalog");
  std::vector<Mask> sets;
  std::string line;
  while (std::getline(input, line)) {
    std::istringstream row(line);
    int point;
    Mask mask = 0;
    while (row >> point) {
      if (point < 0 || point >= 82 || (mask & (Mask(1) << point)))
        throw std::runtime_error("invalid catalog point");
      mask |= Mask(1) << point;
    }
    if (!row.eof() || pop(mask) != 11 || !sidon_by_differences(mask))
      throw std::runtime_error("invalid catalog row");
    sets.push_back(mask);
  }
  if (!input.eof() || sets.size() != 8214)
    throw std::runtime_error("invalid catalog length");
  return sets;
}

static std::vector<int> read_weights(const std::string &path) {
  std::ifstream input(path);
  std::vector<int> weights;
  int value;
  while (input >> value) {
    if (value < 0 || value > 1000000)
      throw std::runtime_error("invalid weight");
    weights.push_back(value);
  }
  if (!input.eof() || weights.size() != 82)
    throw std::runtime_error("invalid weights file");
  return weights;
}

static int weight(Mask x, const std::vector<int> &weights) {
  int answer = 0;
  while (x) {
    const int point = first(x);
    x &= x - 1;
    answer += weights[static_cast<std::size_t>(point)];
  }
  return answer;
}

static std::vector<std::uint64_t> read_expected(const std::string &path) {
  std::ifstream input(path);
  std::string line;
  if (!std::getline(input, line) || line.rfind("orbit,packings", 0) != 0)
    throw std::runtime_error("invalid case header");
  std::vector<std::uint64_t> answer;
  while (std::getline(input, line)) {
    std::istringstream row(line);
    std::string orbit_text, packing_text;
    if (!std::getline(row, orbit_text, ',') ||
        !std::getline(row, packing_text, ','))
      throw std::runtime_error("invalid case row");
    const auto orbit = std::stoull(orbit_text);
    const auto packings = std::stoull(packing_text);
    if (orbit != answer.size())
      throw std::runtime_error("nonconsecutive case index");
    answer.push_back(packings);
  }
  if (!input.eof())
    throw std::runtime_error("case input failure");
  return answer;
}

struct Counter {
  const std::vector<Mask> &sets;
  const std::vector<int> &weights;
  std::size_t words;
  std::vector<std::uint64_t> disjoint;

  Counter(const std::vector<Mask> &set_catalog,
          const std::vector<int> &set_weights)
      : sets(set_catalog), weights(set_weights),
        words((sets.size() + 63) / 64),
        disjoint(sets.size() * words, 0) {
    for (std::size_t i = 0; i < sets.size(); ++i)
      for (std::size_t j = i + 1; j < sets.size(); ++j)
        if (!(sets[i] & sets[j])) {
          disjoint[i * words + j / 64] |= std::uint64_t(1) << (j % 64);
          disjoint[j * words + i / 64] |= std::uint64_t(1) << (i % 64);
        }
  }

  bool compatible(std::size_t i, std::size_t j) const {
    return disjoint[i * words + j / 64] & (std::uint64_t(1) << (j % 64));
  }

  std::size_t weight_limit(int minimum) const {
    std::size_t lo = 0, hi = weights.size();
    while (lo < hi) {
      const std::size_t mid = lo + (hi - lo) / 2;
      if (weights[mid] >= minimum)
        lo = mid + 1;
      else
        hi = mid;
    }
    return lo;
  }

  std::uint64_t count_common(std::size_t a, std::size_t b, std::size_t c,
                             std::size_t lo, std::size_t hi) const {
    if (lo >= hi)
      return 0;
    std::uint64_t answer = 0;
    const std::size_t first_word = lo / 64;
    const std::size_t last_word = (hi - 1) / 64;
    for (std::size_t word = first_word; word <= last_word; ++word) {
      std::uint64_t bits = disjoint[a * words + word] &
                           disjoint[b * words + word] &
                           disjoint[c * words + word];
      if (word == first_word)
        bits &= ~std::uint64_t(0) << (lo % 64);
      if (word == last_word && hi % 64)
        bits &= (std::uint64_t(1) << (hi % 64)) - 1;
      answer += std::popcount(bits);
    }
    return answer;
  }

  std::uint64_t count_for_anchor(std::size_t anchor, int k,
                                 int threshold) const {
    const int wa = weights[anchor];
    std::uint64_t answer = 0;
    for (std::size_t b = anchor + 1; b < sets.size(); ++b) {
      if (wa + (k - 1) * weights[b] < threshold)
        break;
      if (!compatible(anchor, b))
        continue;
      if (k == 2) {
        ++answer;
        continue;
      }
      for (std::size_t c = b + 1; c < sets.size(); ++c) {
        if (wa + weights[b] + (k - 2) * weights[c] < threshold)
          break;
        if (!compatible(anchor, c) || !compatible(b, c))
          continue;
        if (k == 3) {
          ++answer;
          continue;
        }
        const int needed = threshold - wa - weights[b] - weights[c];
        answer += count_common(anchor, b, c, c + 1, weight_limit(needed));
      }
    }
    return answer;
  }
};

int main(int argc, char **argv) {
  try {
    if (argc != 6)
      throw std::runtime_error(
          "usage: checker orbit11 weights cases2 cases3 cases4");
    const auto sets = read_sets(argv[1]);
    const auto point_weights = read_weights(argv[2]);
    if (!std::equal(point_weights.begin(), point_weights.end(),
                    point_weights.rbegin()))
      throw std::runtime_error("weights are not reflection symmetric");
    if (std::accumulate(point_weights.begin(), point_weights.end(), 0) !=
        30884468)
      throw std::runtime_error("wrong total point weight");

    std::vector<int> set_weights;
    set_weights.reserve(sets.size());
    for (Mask set : sets)
      set_weights.push_back(weight(set, point_weights));
    if (!std::is_sorted(set_weights.begin(), set_weights.end(),
                        std::greater<>()))
      throw std::runtime_error("catalog not weight ordered");
    for (std::size_t i = 0; i < sets.size(); i += 2) {
      Mask reflected = 0;
      for (int point = 0; point < 82; ++point)
        if (sets[i] & (Mask(1) << point))
          reflected |= Mask(1) << (81 - point);
      if (sets[i] >= sets[i + 1] || sets[i + 1] != reflected ||
          set_weights[i] != set_weights[i + 1])
        throw std::runtime_error("invalid reflection orbit");
    }

    Counter counter(sets, set_weights);
    std::uint64_t remaining_cases = 0, remaining_packings = 0;
    for (int k = 2; k <= 4; ++k) {
      const auto expected = read_expected(argv[k + 1]);
      const int threshold = 30884468 - (8 - k) * 4000000;
      std::vector<std::uint64_t> actual;
      for (std::size_t anchor = 0; anchor < sets.size(); anchor += 2) {
        if (k * set_weights[anchor] < threshold)
          break;
        actual.push_back(counter.count_for_anchor(anchor, k, threshold));
      }
      if (actual != expected)
        throw std::runtime_error("case ledger mismatch for k=" +
                                 std::to_string(k));
      const auto nonempty = static_cast<std::uint64_t>(
          std::count_if(actual.begin(), actual.end(),
                        [](std::uint64_t x) { return x != 0; }));
      const auto total = std::accumulate(actual.begin(), actual.end(),
                                         std::uint64_t(0));
      const auto maximum = *std::max_element(actual.begin(), actual.end());
      std::cout << "k=" << k << " eligible=" << actual.size()
                << " nonempty=" << nonempty << " packings=" << total
                << " max_case=" << maximum << '\n';
      if (k <= 3) {
        remaining_cases += nonempty;
        remaining_packings += total;
      }
    }
    if (remaining_cases != 6444 || remaining_packings != 7916363)
      throw std::runtime_error("remaining frontier mismatch");
    std::cout << "independent_anchor_cover=PASS remaining_cases="
              << remaining_cases << " remaining_packings="
              << remaining_packings << '\n';
  } catch (const std::exception &error) {
    std::cerr << error.what() << '\n';
    return 1;
  }
}
