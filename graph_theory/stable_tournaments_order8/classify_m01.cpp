#include <algorithm>
#include <array>
#include <bit>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <numeric>
#include <stdexcept>
#include <string>
#include <unordered_set>
#include <unordered_map>
#include <vector>

#ifdef _OPENMP
#include <omp.h>
#endif

using Clock = std::chrono::steady_clock;

namespace {

constexpr int n = 8;
constexpr int edge_count = n * (n - 1) / 2;
constexpr std::uint32_t full_mask = (std::uint32_t{1} << edge_count) - 1U;

struct Order {
    std::array<std::uint8_t, n> low_to_high{};
    std::uint32_t mask = 0;
};

int edge_index(int i, int j) {
    if (!(0 <= i && i < j && j < n)) throw std::runtime_error("bad edge");
    int result = 0;
    for (int a = 0; a < i; ++a) result += n - a - 1;
    return result + j - i - 1;
}

std::vector<Order> make_orders() {
    std::array<int, n> p{};
    std::iota(p.begin(), p.end(), 0);
    std::vector<Order> result;
    do {
        std::array<int, n> rank{};
        Order order;
        for (int r = 0; r < n; ++r) {
            rank[p[r]] = r;
            order.low_to_high[r] = static_cast<std::uint8_t>(p[r]);
        }
        for (int i = 0; i < n; ++i) {
            for (int j = i + 1; j < n; ++j) {
                if (rank[i] > rank[j]) order.mask |= std::uint32_t{1} << edge_index(i, j);
            }
        }
        result.push_back(order);
    } while (std::next_permutation(p.begin(), p.end()));
    return result;
}

std::uint32_t relabel(std::uint32_t mask, const Order& relabeling) {
    // New vertex i is old vertex relabeling.low_to_high[i].
    std::uint32_t result = 0;
    for (int i = 0; i < n; ++i) {
        for (int j = i + 1; j < n; ++j) {
            const int old_i = relabeling.low_to_high[i];
            const int old_j = relabeling.low_to_high[j];
            const int a = std::min(old_i, old_j);
            const int b = std::max(old_i, old_j);
            const bool a_beats_b = ((mask >> edge_index(a, b)) & 1U) != 0;
            const bool old_i_beats_old_j = old_i < old_j ? a_beats_b : !a_beats_b;
            if (old_i_beats_old_j) result |= std::uint32_t{1} << edge_index(i, j);
        }
    }
    return result;
}

std::uint32_t parse_tournament(const std::string& line) {
    if (line.size() != edge_count) throw std::runtime_error("bad tournament line length");
    std::uint32_t result = 0;
    for (int bit = 0; bit < edge_count; ++bit) {
        if (line[bit] == '1') result |= std::uint32_t{1} << bit;
        else if (line[bit] != '0') throw std::runtime_error("bad tournament character");
    }
    return result;
}

std::string print_order(const Order& order) {
    std::string result;
    for (int i = 0; i < n; ++i) {
        if (i != 0) result.push_back(',');
        result += std::to_string(order.low_to_high[i]);
    }
    return result;
}

bool get_bit(const std::vector<std::uint64_t>& bits, std::uint32_t index) {
    return ((bits[index >> 6U] >> (index & 63U)) & 1U) != 0;
}

void set_bit(std::vector<std::uint64_t>& bits, std::uint32_t index) {
    bits[index >> 6U] |= std::uint64_t{1} << (index & 63U);
}

}  // namespace

int main(int argc, char** argv) {
    if (argc != 2) {
        std::cerr << "usage: search_n8 TOURNAMENT_REPRESENTATIVES\n";
        return 2;
    }
    const auto started = Clock::now();
    const auto orders = make_orders();
    if (orders.size() != 40320 || orders.front().mask != 0) {
        throw std::runtime_error("order generation failed");
    }
    std::unordered_set<std::uint32_t> order_masks;
    std::unordered_map<std::uint32_t, std::size_t> order_index;
    order_masks.reserve(orders.size());
    order_index.reserve(orders.size());
    for (std::size_t i = 0; i < orders.size(); ++i) {
        order_masks.insert(orders[i].mask);
        order_index.emplace(orders[i].mask, i);
    }
    if (order_masks.size() != orders.size()) throw std::runtime_error("order mask collision");

    // A naturally labeled relation P (all its comparisons agree with the
    // identity order) has dimension at most two iff there are two total
    // orders whose inversion sets are disjoint and whose union is exactly
    // the incomparability set of P.  Mark all such comparison masks.
    const std::size_t word_count = (std::size_t{1} << edge_count) / 64U;
    std::vector<std::uint64_t> dimension_two(word_count, 0);
#ifdef _OPENMP
#pragma omp parallel
    {
        std::vector<std::uint64_t> local(word_count, 0);
#pragma omp for schedule(dynamic, 8)
        for (std::int64_t yi = 0; yi < static_cast<std::int64_t>(orders.size()); ++yi) {
            const std::uint32_t y = orders[static_cast<std::size_t>(yi)].mask;
            for (std::size_t zi = static_cast<std::size_t>(yi); zi < orders.size(); ++zi) {
                const std::uint32_t z = orders[zi].mask;
                if ((y & z) != 0U) continue;
                set_bit(local, full_mask ^ (y | z));
            }
        }
#pragma omp critical
        {
            for (std::size_t i = 0; i < word_count; ++i) dimension_two[i] |= local[i];
        }
    }
#else
    for (std::size_t yi = 0; yi < orders.size(); ++yi) {
        const std::uint32_t y = orders[yi].mask;
        for (std::size_t zi = yi; zi < orders.size(); ++zi) {
            const std::uint32_t z = orders[zi].mask;
            if ((y & z) != 0U) continue;
            set_bit(dimension_two, full_mask ^ (y | z));
        }
    }
#endif
    std::uint64_t marked = 0;
    for (const auto word : dimension_two) marked += std::popcount(word);
    std::cerr << "dimension_two_natural_posets=" << marked
              << " precompute_seconds="
              << std::chrono::duration<double>(Clock::now() - started).count() << '\n';

    std::ifstream input(argv[1]);
    if (!input) throw std::runtime_error("could not open input");
    std::vector<std::uint32_t> representatives;
    std::string line;
    while (std::getline(input, line)) {
        if (!line.empty()) representatives.push_back(parse_tournament(line));
    }
    if (representatives.size() != 6880) throw std::runtime_error("expected 6880 representatives");

    std::uint64_t transitive = 0;
    std::uint64_t stabilized = 0;
    std::uint64_t failed = 0;
    std::uint64_t relabelings_tested = 0;
    std::cout << "CERTIFICATE stable_tournaments_n8_v1 classes=" << representatives.size() << '\n';
    for (std::size_t class_index = 0; class_index < representatives.size(); ++class_index) {
        const std::uint32_t tournament = representatives[class_index];
        if (order_masks.contains(tournament)) {
            ++transitive;
            std::cout << "CLASS " << class_index << " tournament=" << tournament
                      << " m=0\n";
            continue;
        }
        bool found = false;
        for (std::size_t pi = 0; pi < orders.size(); ++pi) {
            ++relabelings_tested;
            const std::uint32_t image = relabel(tournament, orders[pi]);
            const std::uint32_t comparisons = full_mask ^ image;
            if (!get_bit(dimension_two, comparisons)) continue;

            const std::uint32_t incomparabilities = image;
            for (std::size_t yi = 0; yi < orders.size(); ++yi) {
                const std::uint32_t y = orders[yi].mask;
                if ((y & comparisons) != 0U) continue;
                const std::uint32_t z = incomparabilities ^ y;
                const auto zit = order_index.find(z);
                if (zit == order_index.end()) continue;
                const auto zi = zit->second;
                std::cout << "CLASS " << class_index << " tournament=" << tournament
                          << " m=1 relabel=" << print_order(orders[pi])
                          << " y=" << print_order(orders[yi])
                          << " z=" << print_order(orders[zi]) << '\n';
                found = true;
                ++stabilized;
                break;
            }
            if (!found) throw std::runtime_error("marked poset lacked witness");
            break;
        }
        if (!found) {
            ++failed;
            std::cout << "FAIL " << class_index << " tournament=" << tournament << '\n';
        }
        if ((class_index + 1U) % 500U == 0U) {
            std::cerr << "classes_checked=" << (class_index + 1U)
                      << " failed=" << failed << '\n';
        }
    }
    std::cout << "SUMMARY classes=" << representatives.size()
              << " m0=" << transitive << " m1=" << stabilized << " m2_candidates=" << failed
              << " relabelings_tested=" << relabelings_tested << '\n';
    std::cerr << "total_seconds="
              << std::chrono::duration<double>(Clock::now() - started).count() << '\n';
    return 0;
}
