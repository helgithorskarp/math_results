// Independent all-pairs strict-edge sieve for h3927, using a new prime.
#include <algorithm>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

namespace {
constexpr std::uint64_t kPrime = 1000000271ULL;
constexpr std::uint64_t kDenominator = 96ULL;

struct Point {
  std::int64_t x;
  std::int64_t y;
};

void WriteLittleEndian(std::ofstream& output, std::uint32_t value) {
  for (unsigned shift = 0; shift < 32; shift += 8) {
    output.put(static_cast<char>((value >> shift) & 255U));
  }
}
}  // namespace

int main(int argc, char** argv) {
  try {
    if (argc != 4) {
      throw std::runtime_error("usage: review_sieve residues.tsv maximum_n output.bin");
    }
    std::ifstream input(argv[1]);
    std::size_t total = 0;
    std::uint64_t prime = 0;
    std::uint64_t denominator = 0;
    if (!(input >> total >> prime >> denominator) || total != 64513 ||
        prime != kPrime || denominator != kDenominator) {
      throw std::runtime_error("residue header");
    }
    std::vector<Point> points(total);
    for (Point& point : points) {
      if (!(input >> point.x >> point.y) || point.x < 0 || point.y < 0 ||
          point.x >= static_cast<std::int64_t>(prime) ||
          point.y >= static_cast<std::int64_t>(prime)) {
        throw std::runtime_error("residue row/range");
      }
    }
    std::string extra;
    if (input >> extra) {
      throw std::runtime_error("extra residue data");
    }
    const std::size_t maximum = std::stoull(argv[2]);
    if (maximum < 2 || maximum > total) {
      throw std::runtime_error("vertex cap");
    }
    const std::uint64_t target = denominator * denominator % prime;
    std::vector<std::pair<std::uint32_t, std::uint32_t>> survivors;
    // Deliberately use high-endpoint-major traversal, unlike the reviewed scan.
    for (std::uint32_t high = 1; high < maximum; ++high) {
      for (std::uint32_t low = 0; low < high; ++low) {
        const std::int64_t dx = points[low].x - points[high].x;
        const std::int64_t dy = points[low].y - points[high].y;
        const std::int64_t squared = dx * dx + dy * dy;
        if (static_cast<std::uint64_t>(squared) % prime == target) {
          survivors.emplace_back(low, high);
        }
      }
    }
    std::sort(survivors.begin(), survivors.end());
    std::ofstream output(argv[3], std::ios::binary);
    if (!output) {
      throw std::runtime_error("output open");
    }
    for (const auto& edge : survivors) {
      WriteLittleEndian(output, edge.first);
      WriteLittleEndian(output, edge.second);
    }
    output.close();
    if (!output) {
      throw std::runtime_error("output write");
    }
    const std::uint64_t pairs =
        static_cast<std::uint64_t>(maximum) * (maximum - 1) / 2;
    std::cout << "{\"vertices\":" << maximum << ",\"pairs\":" << pairs
              << ",\"survivors\":" << survivors.size()
              << ",\"prime\":" << prime << "}\n";
  } catch (const std::exception& error) {
    std::cerr << "REJECTED: " << error.what() << '\n';
    return 1;
  }
}
