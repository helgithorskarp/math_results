#include <algorithm>
#include <array>
#include <bit>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>

namespace {

constexpr int CODE_SIZE = 1667;

struct Candidate {
    std::uint32_t word{};
    std::array<std::uint16_t, 4> blockers{};
    int blocker_count{};
};

std::uint32_t pair_key(int first, int second) {
    if (first >= second) {
        throw std::runtime_error("invalid pair key");
    }
    return static_cast<std::uint32_t>(first) |
           (static_cast<std::uint32_t>(second) << 11);
}

std::uint64_t triple_key(int first, int second, int third) {
    if (first >= second || second >= third) {
        throw std::runtime_error("invalid triple key");
    }
    return static_cast<std::uint64_t>(first) |
           (static_cast<std::uint64_t>(second) << 11) |
           (static_cast<std::uint64_t>(third) << 22);
}

std::uint64_t quad_key(const std::array<int, 4>& values) {
    if (!std::is_sorted(values.begin(), values.end()) ||
        std::adjacent_find(values.begin(), values.end()) != values.end()) {
        throw std::runtime_error("invalid quadruple key");
    }
    return static_cast<std::uint64_t>(values[0]) |
           (static_cast<std::uint64_t>(values[1]) << 11) |
           (static_cast<std::uint64_t>(values[2]) << 22) |
           (static_cast<std::uint64_t>(values[3]) << 33);
}

std::array<int, 4> decode_quad(std::uint64_t key) {
    return {static_cast<int>(key & 2047),
            static_cast<int>((key >> 11) & 2047),
            static_cast<int>((key >> 22) & 2047),
            static_cast<int>((key >> 33) & 2047)};
}

std::vector<Candidate> load_candidates(const std::string& path) {
    std::ifstream input(path);
    if (!input) {
        throw std::runtime_error("cannot open candidate file");
    }
    std::string line;
    if (!std::getline(input, line) || line != "word_hex\tblocker_count\tblockers_zero_based") {
        throw std::runtime_error("unexpected candidate header");
    }
    std::vector<Candidate> candidates;
    while (std::getline(input, line)) {
        std::istringstream row(line);
        std::string word_text;
        std::string count_text;
        std::string blocker_text;
        if (!std::getline(row, word_text, '\t') || !std::getline(row, count_text, '\t') ||
            !std::getline(row, blocker_text)) {
            throw std::runtime_error("malformed candidate row");
        }
        Candidate candidate;
        candidate.word = static_cast<std::uint32_t>(std::stoul(word_text, nullptr, 16));
        candidate.blocker_count = std::stoi(count_text);
        std::istringstream blocker_stream(blocker_text);
        std::string value;
        int count = 0;
        while (std::getline(blocker_stream, value, ',')) {
            if (count >= 4) {
                throw std::runtime_error("too many blockers");
            }
            candidate.blockers[count++] = static_cast<std::uint16_t>(std::stoi(value));
        }
        if (count != candidate.blocker_count || count < 1 || count > 4 ||
            std::popcount(candidate.word) != 8 ||
            !std::is_sorted(candidate.blockers.begin(), candidate.blockers.begin() + count) ||
            std::adjacent_find(candidate.blockers.begin(), candidate.blockers.begin() + count) !=
                candidate.blockers.begin() + count) {
            throw std::runtime_error("invalid candidate row");
        }
        candidates.push_back(candidate);
    }
    if (candidates.size() != 6051) {
        throw std::runtime_error("expected 6051 candidates");
    }
    return candidates;
}

std::array<int, 4> add_to_triple(const std::array<int, 3>& triple, int value) {
    std::array<int, 4> result{triple[0], triple[1], triple[2], value};
    std::sort(result.begin(), result.end());
    return result;
}

std::vector<int> support_union(const std::array<int, 2>& left, const std::array<int, 2>& right) {
    std::vector<int> result{left[0], left[1], right[0], right[1]};
    std::sort(result.begin(), result.end());
    result.erase(std::unique(result.begin(), result.end()), result.end());
    return result;
}

bool contains(const std::vector<int>& values, int value) {
    return std::find(values.begin(), values.end(), value) != values.end();
}

bool compatible(std::uint32_t left, std::uint32_t right) {
    return std::popcount(left & right) <= 4;
}

template <class Map, class Key>
void append_bucket(const Map& map, const Key& key, std::vector<std::uint32_t>& destination) {
    const auto found = map.find(key);
    if (found != map.end()) {
        destination.insert(destination.end(), found->second.begin(), found->second.end());
    }
}

}  // namespace

int main(int argc, char** argv) {
    try {
        if (argc != 2) {
            std::cerr << "usage: " << argv[0] << " LOW4_CANDIDATES_TSV\n";
            return 2;
        }
        const auto started = std::chrono::steady_clock::now();
        const std::vector<Candidate> candidates = load_candidates(argv[1]);
        std::vector<std::vector<std::uint32_t>> singletons(CODE_SIZE);
        std::unordered_map<std::uint32_t, std::vector<std::uint32_t>> pairs;
        std::unordered_map<std::uint64_t, std::vector<std::uint32_t>> triples;
        std::unordered_map<std::uint64_t, std::vector<std::uint32_t>> quads;
        std::vector<std::array<int, 2>> pair_supports;
        std::vector<std::array<int, 3>> triple_supports;
        std::vector<int> singleton_supports;
        std::array<bool, CODE_SIZE> active_flags{};

        for (const Candidate& candidate : candidates) {
            for (int index = 0; index < candidate.blocker_count; ++index) {
                active_flags[candidate.blockers[index]] = true;
            }
            if (candidate.blocker_count == 1) {
                singletons[candidate.blockers[0]].push_back(candidate.word);
            } else if (candidate.blocker_count == 2) {
                pairs[pair_key(candidate.blockers[0], candidate.blockers[1])].push_back(candidate.word);
            } else if (candidate.blocker_count == 3) {
                triples[triple_key(candidate.blockers[0], candidate.blockers[1], candidate.blockers[2])]
                    .push_back(candidate.word);
            } else {
                std::array<int, 4> support{candidate.blockers[0], candidate.blockers[1],
                                           candidate.blockers[2], candidate.blockers[3]};
                quads[quad_key(support)].push_back(candidate.word);
            }
        }
        for (int index = 0; index < CODE_SIZE; ++index) {
            if (!singletons[index].empty()) {
                singleton_supports.push_back(index);
            }
        }
        for (const auto& [key, words] : pairs) {
            if (words.empty()) {
                throw std::runtime_error("empty pair bucket");
            }
            pair_supports.push_back({static_cast<int>(key & 2047), static_cast<int>((key >> 11) & 2047)});
        }
        for (const auto& [key, words] : triples) {
            if (words.empty()) {
                throw std::runtime_error("empty triple bucket");
            }
            triple_supports.push_back({static_cast<int>(key & 2047),
                                       static_cast<int>((key >> 11) & 2047),
                                       static_cast<int>((key >> 22) & 2047)});
        }
        std::sort(pair_supports.begin(), pair_supports.end());
        std::sort(triple_supports.begin(), triple_supports.end());
        std::vector<int> active_blockers;
        for (int index = 0; index < CODE_SIZE; ++index) {
            if (active_flags[index]) {
                active_blockers.push_back(index);
            }
        }

        std::unordered_set<std::uint64_t> removal_set;
        removal_set.max_load_factor(0.7F);
        removal_set.reserve(8'000'000);
        for (const auto& [key, words] : quads) {
            if (words.empty()) {
                throw std::runtime_error("empty quadruple bucket");
            }
            removal_set.insert(key);
        }
        for (const auto& triple : triple_supports) {
            for (int blocker : active_blockers) {
                if (blocker != triple[0] && blocker != triple[1] && blocker != triple[2]) {
                    removal_set.insert(quad_key(add_to_triple(triple, blocker)));
                }
            }
        }
        const std::uint64_t after_triples = removal_set.size();

        for (std::size_t first = 0; first < pair_supports.size(); ++first) {
            for (std::size_t second = first + 1; second < pair_supports.size(); ++second) {
                const std::vector<int> combined = support_union(pair_supports[first], pair_supports[second]);
                if (combined.size() == 4) {
                    removal_set.insert(quad_key({combined[0], combined[1], combined[2], combined[3]}));
                } else if (combined.size() == 3) {
                    const std::array<int, 3> triple{combined[0], combined[1], combined[2]};
                    for (int blocker : active_blockers) {
                        if (!contains(combined, blocker)) {
                            removal_set.insert(quad_key(add_to_triple(triple, blocker)));
                        }
                    }
                } else {
                    throw std::runtime_error("distinct pair supports have union smaller than three");
                }
            }
        }
        const std::uint64_t after_pair_pairs = removal_set.size();

        for (const auto& pair : pair_supports) {
            for (std::size_t first = 0; first < singleton_supports.size(); ++first) {
                for (std::size_t second = first + 1; second < singleton_supports.size(); ++second) {
                    std::array<int, 4> combined{pair[0], pair[1], singleton_supports[first],
                                                singleton_supports[second]};
                    std::sort(combined.begin(), combined.end());
                    if (std::adjacent_find(combined.begin(), combined.end()) == combined.end()) {
                        removal_set.insert(quad_key(combined));
                    }
                }
            }
        }

        std::vector<std::uint64_t> removal_keys(removal_set.begin(), removal_set.end());
        std::sort(removal_keys.begin(), removal_keys.end());
        std::uint64_t pools_with_five = 0;
        std::uint64_t compatible_prefix_quintuples = 0;
        std::size_t maximum_pool_size = 0;
        for (std::uint64_t key : removal_keys) {
            const std::array<int, 4> removed = decode_quad(key);
            std::vector<std::uint32_t> pool;
            for (int blocker : removed) {
                pool.insert(pool.end(), singletons[blocker].begin(), singletons[blocker].end());
            }
            for (int first = 0; first < 4; ++first) {
                for (int second = first + 1; second < 4; ++second) {
                    append_bucket(pairs, pair_key(removed[first], removed[second]), pool);
                }
            }
            for (int omitted = 0; omitted < 4; ++omitted) {
                std::array<int, 3> support{};
                int position = 0;
                for (int index = 0; index < 4; ++index) {
                    if (index != omitted) {
                        support[position++] = removed[index];
                    }
                }
                append_bucket(triples, triple_key(support[0], support[1], support[2]), pool);
            }
            append_bucket(quads, key, pool);
            maximum_pool_size = std::max(maximum_pool_size, pool.size());
            if (pool.size() < 5) {
                continue;
            }
            ++pools_with_five;
            for (std::size_t first = 0; first < pool.size(); ++first) {
                for (std::size_t second = first + 1; second < pool.size(); ++second) {
                    if (!compatible(pool[first], pool[second])) continue;
                    for (std::size_t third = second + 1; third < pool.size(); ++third) {
                        if (!compatible(pool[first], pool[third]) || !compatible(pool[second], pool[third])) continue;
                        for (std::size_t fourth = third + 1; fourth < pool.size(); ++fourth) {
                            if (!compatible(pool[first], pool[fourth]) || !compatible(pool[second], pool[fourth]) ||
                                !compatible(pool[third], pool[fourth])) continue;
                            for (std::size_t fifth = fourth + 1; fifth < pool.size(); ++fifth) {
                                ++compatible_prefix_quintuples;
                                if (compatible(pool[first], pool[fifth]) && compatible(pool[second], pool[fifth]) &&
                                    compatible(pool[third], pool[fifth]) && compatible(pool[fourth], pool[fifth])) {
                                    std::cout << "radius_four_exchange=FOUND\nremoved=" << removed[0] << ','
                                              << removed[1] << ',' << removed[2] << ',' << removed[3] << '\n';
                                    for (std::uint32_t word : {pool[first], pool[second], pool[third],
                                                               pool[fourth], pool[fifth]}) {
                                        std::cout << "added=" << std::hex << std::setw(8) << std::setfill('0')
                                                  << word << std::dec << std::setfill(' ') << '\n';
                                    }
                                    return 0;
                                }
                            }
                        }
                    }
                }
            }
        }

        std::cout << "singleton_supports=" << singleton_supports.size() << '\n';
        std::cout << "pair_supports=" << pair_supports.size() << '\n';
        std::cout << "triple_supports=" << triple_supports.size() << '\n';
        std::cout << "quadruple_supports=" << quads.size() << '\n';
        std::cout << "active_blockers=" << active_blockers.size() << '\n';
        std::cout << "removal_sets_after_triples=" << after_triples << '\n';
        std::cout << "removal_sets_after_pair_pairs=" << after_pair_pairs << '\n';
        std::cout << "radius_four_removal_sets=" << removal_keys.size() << '\n';
        std::cout << "radius_four_pools_with_at_least_five_candidates=" << pools_with_five << '\n';
        std::cout << "maximum_pool_size=" << maximum_pool_size << '\n';
        std::cout << "radius_four_compatible_prefix_quintuples_tested=" << compatible_prefix_quintuples << '\n';
        std::cout << "radius_four_exchange=NONE\n";
        std::cout << "conclusion=incumbent_is_4_exchange_maximal\n";
        const auto elapsed = std::chrono::duration<double>(std::chrono::steady_clock::now() - started).count();
        std::cerr << "elapsed_seconds=" << elapsed << '\n';
        return 0;
    } catch (const std::exception& error) {
        std::cerr << "ERROR: " << error.what() << '\n';
        return 1;
    }
}
