#include <algorithm>
#include <chrono>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <vector>

using Clock = std::chrono::steady_clock;

struct Order {
    std::vector<std::uint8_t> low_to_high;
    std::uint32_t mask;
};

static int edge_index(int n, int i, int j) {
    int index = 0;
    for (int a = 0; a < i; ++a) index += n - a - 1;
    return index + j - i - 1;
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
        std::vector<std::uint8_t> stored(n);
        for (int r = 0; r < n; ++r) {
            rank[p[r]] = r;
            stored[r] = static_cast<std::uint8_t>(p[r]);
        }
        std::uint32_t mask = 0;
        for (int i = 0; i < n; ++i) {
            for (int j = i + 1; j < n; ++j) {
                if (rank[i] > rank[j]) mask |= std::uint32_t{1} << edge_index(n, i, j);
            }
        }
        result.push_back({stored, mask});
    } while (std::next_permutation(p.begin(), p.end()));
    return result;
}

int main(int argc, char** argv) {
    const int n = argc > 1 ? std::stoi(argv[1]) : 7;
    if (n < 1 || n > 7) {
        std::cerr << "require 1 <= n <= 7\n";
        return 2;
    }
    const int edges = n * (n - 1) / 2;
    const std::uint32_t tournament_count = std::uint32_t{1} << edges;
    const auto started = Clock::now();
    const auto orders = make_orders(n);
    std::vector<std::uint64_t> spread_orders;
    spread_orders.reserve(orders.size());
    for (const auto& order : orders) spread_orders.push_back(spread(order.mask, edges));

    // A value is the lexicographic pair of order indices giving the sum.
    std::unordered_map<std::uint64_t, std::uint32_t> sums2;
    const std::size_t pair_count = orders.size() * (orders.size() + 1ULL) / 2ULL;
    sums2.reserve(pair_count);
    for (std::uint32_t i = 0; i < orders.size(); ++i) {
        for (std::uint32_t j = i; j < orders.size(); ++j) {
            sums2.emplace(spread_orders[i] + spread_orders[j],
                          i * static_cast<std::uint32_t>(orders.size()) + j);
        }
    }
    std::cerr << "n=" << n << " orders=" << orders.size()
              << " unordered_pairs=" << pair_count
              << " distinct_pair_sums=" << sums2.size() << '\n';

    std::vector<std::uint64_t> spread_tournaments(tournament_count);
    for (std::uint32_t t = 0; t < tournament_count; ++t) {
        spread_tournaments[t] = spread(t, edges);
    }

    std::uint64_t represented = 0;
    std::uint64_t lookup_count = 0;
    std::uint64_t witness_hash = 1469598103934665603ULL;
    std::vector<std::uint32_t> failures;
    for (std::uint32_t t = 0; t < tournament_count; ++t) {
        bool found = false;
        for (std::uint32_t x = 0; x < orders.size(); ++x) {
            ++lookup_count;
            const auto it = sums2.find(spread_tournaments[t] + spread_orders[x]);
            if (it == sums2.end()) continue;
            const std::uint32_t y = it->second / static_cast<std::uint32_t>(orders.size());
            const std::uint32_t z = it->second % static_cast<std::uint32_t>(orders.size());
            // Deterministic compact digest of every labeled witness.
            for (const std::uint32_t word : {t, x, y, z}) {
                witness_hash ^= word;
                witness_hash *= 1099511628211ULL;
            }
            found = true;
            ++represented;
            break;
        }
        if (!found) {
            failures.push_back(t);
            std::cout << "FAIL " << t << '\n';
        }
        if ((t + 1U) % 262144U == 0U) {
            std::cerr << "checked=" << (t + 1U) << '/' << tournament_count
                      << " failures=" << failures.size() << '\n';
        }
    }
    std::cout << "SUMMARY n=" << n
              << " represented=" << represented
              << " failures=" << failures.size()
              << " lookups=" << lookup_count
              << " witness_fnv64=" << witness_hash << '\n';
    if (!failures.empty()) {
        const std::uint32_t t = failures.front();
        std::cout << "FIRST_FAILURE " << t << '\n';
    }
    std::cerr << "elapsed_seconds="
              << std::chrono::duration<double>(Clock::now() - started).count() << '\n';
    return 0;
}
