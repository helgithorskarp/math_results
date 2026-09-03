#include <algorithm>
#include <chrono>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <stdexcept>
#include <string>
#include <sys/resource.h>
#include <unordered_map>
#include <unordered_set>
#include <vector>

using Clock = std::chrono::steady_clock;

struct Order {
    std::vector<std::uint8_t> low_to_high;
    std::uint32_t mask;
};

static int edge_index(int n, int i, int j) {
    if (!(0 <= i && i < j && j < n)) throw std::runtime_error("bad edge");
    int result = 0;
    for (int a = 0; a < i; ++a) result += n - a - 1;
    return result + j - i - 1;
}

static std::uint64_t spread(std::uint32_t mask, int edges) {
    std::uint64_t result = 0;
    for (int e = 0; e < edges; ++e) {
        result |= std::uint64_t((mask >> e) & 1U) << (2 * e);
    }
    return result;
}

static std::vector<Order> make_orders(int n) {
    std::vector<int> p(n);
    std::iota(p.begin(), p.end(), 0);
    std::vector<Order> result;
    do {
        std::vector<int> rank(n);
        std::vector<std::uint8_t> saved(n);
        for (int r = 0; r < n; ++r) {
            rank[p[r]] = r;
            saved[r] = static_cast<std::uint8_t>(p[r]);
        }
        std::uint32_t mask = 0;
        for (int i = 0; i < n; ++i) {
            for (int j = i + 1; j < n; ++j) {
                if (rank[i] > rank[j]) mask |= std::uint32_t{1} << edge_index(n, i, j);
            }
        }
        result.push_back({saved, mask});
    } while (std::next_permutation(p.begin(), p.end()));
    return result;
}

static std::uint32_t relabel(std::uint32_t mask, const Order& relabeling, int n) {
    // New vertex i is old vertex relabeling.low_to_high[i].
    std::uint32_t result = 0;
    for (int i = 0; i < n; ++i) {
        for (int j = i + 1; j < n; ++j) {
            const int old_i = relabeling.low_to_high[i];
            const int old_j = relabeling.low_to_high[j];
            const int a = std::min(old_i, old_j);
            const int b = std::max(old_i, old_j);
            const bool a_beats_b = ((mask >> edge_index(n, a, b)) & 1U) != 0;
            const bool old_i_beats_old_j = old_i < old_j ? a_beats_b : !a_beats_b;
            if (old_i_beats_old_j) result |= std::uint32_t{1} << edge_index(n, i, j);
        }
    }
    return result;
}

static std::string print_order(const Order& order) {
    std::string result;
    for (std::size_t i = 0; i < order.low_to_high.size(); ++i) {
        if (i != 0) result.push_back(',');
        result += std::to_string(order.low_to_high[i]);
    }
    return result;
}

int main(int argc, char** argv) {
    const int n = argc >= 2 ? std::stoi(argv[1]) : 7;
    if (n < 1 || n > 7) {
        std::cerr << "usage: generate_certificates N, where 1 <= N <= 7\n";
        return 2;
    }
    const auto started = Clock::now();
    const int edges = n * (n - 1) / 2;
    const std::uint32_t tournament_count = std::uint32_t{1} << edges;
    const auto orders = make_orders(n);
    std::vector<std::uint64_t> spread_orders;
    spread_orders.reserve(orders.size());
    std::unordered_set<std::uint32_t> transitive;
    transitive.reserve(orders.size());
    for (const auto& order : orders) {
        spread_orders.push_back(spread(order.mask, edges));
        transitive.insert(order.mask);
    }
    if (transitive.size() != orders.size()) throw std::runtime_error("order mask collision");

    const std::size_t unordered_pairs = orders.size() * (orders.size() + 1ULL) / 2ULL;
    std::unordered_map<std::uint64_t, std::uint32_t> sums2;
    sums2.reserve(unordered_pairs);
    for (std::uint32_t y = 0; y < orders.size(); ++y) {
        for (std::uint32_t z = y; z < orders.size(); ++z) {
            const std::uint64_t sum = spread_orders[y] + spread_orders[z];
            sums2.emplace(sum, y * static_cast<std::uint32_t>(orders.size()) + z);
        }
    }

    std::vector<bool> covered(tournament_count, false);
    std::uint64_t covered_count = 0;
    std::uint64_t class_count = 0;
    std::uint64_t transitive_classes = 0;
    std::uint64_t stabilized_classes = 0;
    std::cout << "CERTIFICATE stable_tournaments_v1 n=" << n << '\n';
    for (std::uint32_t t = 0; t < tournament_count; ++t) {
        if (covered[t]) continue;
        ++class_count;
        std::unordered_set<std::uint32_t> orbit;
        orbit.reserve(orders.size());
        for (const auto& p : orders) orbit.insert(relabel(t, p, n));
        for (const std::uint32_t image : orbit) {
            if (covered[image]) throw std::runtime_error("isomorphism orbits overlap");
            covered[image] = true;
            ++covered_count;
        }

        if (transitive.count(t) != 0U) {
            ++transitive_classes;
            std::cout << "CLASS " << t << " orbit=" << orbit.size() << " m=0\n";
            continue;
        }
        bool found = false;
        const std::uint64_t encoded_t = spread(t, edges);
        for (std::uint32_t x = 0; x < orders.size(); ++x) {
            const auto it = sums2.find(encoded_t + spread_orders[x]);
            if (it == sums2.end()) continue;
            const std::uint32_t y = it->second / static_cast<std::uint32_t>(orders.size());
            const std::uint32_t z = it->second % static_cast<std::uint32_t>(orders.size());
            std::cout << "CLASS " << t << " orbit=" << orbit.size() << " m=1 x="
                      << print_order(orders[x]) << " y=" << print_order(orders[y])
                      << " z=" << print_order(orders[z]) << '\n';
            found = true;
            ++stabilized_classes;
            break;
        }
        if (!found) {
            std::cerr << "No one-summand witness for representative " << t << '\n';
            return 1;
        }
    }
    if (covered_count != tournament_count) throw std::runtime_error("incomplete class coverage");
    struct rusage usage {};
    if (getrusage(RUSAGE_SELF, &usage) != 0) throw std::runtime_error("getrusage failed");
    std::cout << "SUMMARY n=" << n << " tournaments=" << tournament_count
              << " classes=" << class_count << " transitive_classes=" << transitive_classes
              << " stabilized_classes=" << stabilized_classes
              << " distinct_pair_sums=" << sums2.size() << '\n';
    std::cerr << "elapsed_seconds="
              << std::chrono::duration<double>(Clock::now() - started).count()
              << " max_rss_kib=" << usage.ru_maxrss << '\n';
    return 0;
}
