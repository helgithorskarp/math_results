// Exact finite falsification of the proposed balanced-tree join bound.
// One thread; m<=7, <=43 input permutations, <=6345768 candidate joins.
#include <algorithm>
#include <array>
#include <bit>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <set>
#include <stdexcept>
#include <string>
#include <vector>

using Perm = std::vector<int>;

bool avoids(const Perm& p) {
    const int n = static_cast<int>(p.size());
    for (int i = 0; i < n; ++i) {
        for (int j = i + 1; j < n; ++j) {
            if (p[static_cast<std::size_t>(j)] >= p[static_cast<std::size_t>(i)]) continue;
            for (int k = j + 1; k < n; ++k) {
                if (p[static_cast<std::size_t>(k)] <= p[static_cast<std::size_t>(i)]) continue;
                for (int l = k + 1; l < n; ++l) {
                    if (!(p[static_cast<std::size_t>(i)] < p[static_cast<std::size_t>(l)] &&
                          p[static_cast<std::size_t>(l)] < p[static_cast<std::size_t>(k)])) continue;
                    bool empty = true;
                    for (int h = i + 1; h < l; ++h) {
                        if (h == j || h == k) continue;
                        if (p[static_cast<std::size_t>(j)] < p[static_cast<std::size_t>(h)] &&
                            p[static_cast<std::size_t>(h)] < p[static_cast<std::size_t>(k)]) {
                            empty = false;
                            break;
                        }
                    }
                    if (empty) return false;
                }
            }
        }
    }
    return true;
}

void array_json(std::ostream& out, const Perm& p) {
    out << '[';
    for (std::size_t i = 0; i < p.size(); ++i) {
        if (i != 0U) out << ',';
        out << p[i];
    }
    out << ']';
}

int main(int argc, char** argv) {
    try {
        if (argc != 3) throw std::runtime_error("usage: balanced_join INPUT OUTPUT");
        std::ifstream in(argv[1]);
        if (!in) throw std::runtime_error("cannot read input");
        int m = 0;
        int count = 0;
        if (!(in >> m >> count) || m < 1 || m > 7 || count < 1 || count > 43)
            throw std::runtime_error("input scope requires 1<=m<=7 and1<=count<=43");
        std::vector<Perm> fiber;
        std::set<Perm> unique;
        for (int row = 0; row < count; ++row) {
            Perm p(static_cast<std::size_t>(m));
            std::vector<bool> seen(static_cast<std::size_t>(m + 1), false);
            for (int& value : p) {
                if (!(in >> value) || value < 1 || value > m || seen[static_cast<std::size_t>(value)])
                    throw std::runtime_error("input is not a permutation");
                seen[static_cast<std::size_t>(value)] = true;
            }
            if (!avoids(p) || !unique.insert(p).second)
                throw std::runtime_error("input contains forbidden pattern or duplicate");
            fiber.push_back(p);
        }
        std::string extra;
        if (in >> extra) throw std::runtime_error("unparsed trailing input");
        std::vector<std::pair<Perm, Perm>> partitions;
        const auto limit = 1U << static_cast<unsigned>(2 * m);
        for (unsigned mask = 0U; mask < limit; ++mask) {
            if (std::popcount(mask) != m) continue;
            Perm left, right;
            for (int j = 0; j < 2 * m; ++j) {
                ((mask & (1U << static_cast<unsigned>(j))) != 0U ? left : right).push_back(j + 1);
            }
            partitions.emplace_back(left, right);
        }
        std::uint64_t total = 0U;
        std::uint64_t minimum = static_cast<std::uint64_t>(partitions.size()) + 1U;
        Perm min_alpha, min_beta;
        std::vector<std::uint64_t> pair_counts;
        std::uint64_t candidate_joins = 0U;
        for (const auto& alpha : fiber) {
            for (const auto& beta : fiber) {
                std::uint64_t good = 0U;
                for (const auto& [left, right] : partitions) {
                    Perm p(static_cast<std::size_t>(2 * m + 1));
                    for (int j = 0; j < m; ++j) {
                        p[static_cast<std::size_t>(j)] = left[static_cast<std::size_t>(alpha[static_cast<std::size_t>(j)] - 1)];
                        p[static_cast<std::size_t>(m + j + 1)] = right[static_cast<std::size_t>(beta[static_cast<std::size_t>(j)] - 1)];
                    }
                    p[static_cast<std::size_t>(m)] = 2 * m + 1;
                    if (avoids(p)) ++good;
                    ++candidate_joins;
                }
                total += good;
                pair_counts.push_back(good);
                if (good < minimum) {
                    minimum = good;
                    min_alpha = alpha;
                    min_beta = beta;
                }
            }
        }
        const std::uint64_t proposed = 1ULL << static_cast<unsigned>((m - 1) / 2);
        std::ofstream out(argv[2]);
        if (!out) throw std::runtime_error("cannot write output");
        out << "{\n\"status\":\"complete exact finite join calculation; no uniform growth conclusion\",\n";
        out << "\"full_growth_target_solved\":false,\n\"m\":" << m;
        out << ",\n\"input_fiber_size\":" << count;
        out << ",\n\"rank_partitions_per_pair\":" << partitions.size();
        out << ",\n\"candidate_joins_checked\":" << candidate_joins;
        out << ",\n\"sum_valid_joins\":" << total;
        out << ",\n\"minimum_valid_joins\":" << minimum;
        out << ",\n\"first_minimizing_alpha\":";
        array_json(out, min_alpha);
        out << ",\n\"first_minimizing_beta\":";
        array_json(out, min_beta);
        out << ",\n\"proposed_uniform_bound\":" << proposed;
        out << ",\n\"bound_holds_for_all_tested_pairs\":" << (minimum >= proposed ? "true" : "false");
        out << ",\n\"pair_counts_in_input_order\":[";
        for (std::size_t i = 0; i < pair_counts.size(); ++i) {
            if (i != 0U) out << ',';
            out << pair_counts[i];
        }
        out << "],\n\"processes\":1,\"native_threads\":1\n}\n";
        if (!out) throw std::runtime_error("output write failed");
        std::cout << "m=" << m << " candidates=" << candidate_joins << " valid=" << total
                  << " minimum=" << minimum << " proposed=" << proposed << '\n';
        return 0;
    } catch (const std::exception& e) {
        std::cerr << "ERROR: " << e.what() << '\n';
        return 1;
    }
}
