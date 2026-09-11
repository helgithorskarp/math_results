#include <algorithm>
#include <array>
#include <bit>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <limits>
#include <map>
#include <numeric>
#include <stdexcept>
#include <string>
#include <vector>

namespace {

constexpr int N = 32;
constexpr int W = 8;
constexpr int T = 5;
constexpr int EXPECTED_CODE_SIZE = 1667;

std::array<std::array<std::uint32_t, W + 1>, N + 1> choose_table{};

struct LowCandidate {
    std::uint32_t word{};
    std::array<std::uint16_t, 2> blockers{};
    std::uint8_t blocker_count{};

    friend bool operator==(const LowCandidate&, const LowCandidate&) = default;
};

bool low_candidate_less(const LowCandidate& left, const LowCandidate& right) {
    if (left.word != right.word) {
        return left.word < right.word;
    }
    if (left.blocker_count != right.blocker_count) {
        return left.blocker_count < right.blocker_count;
    }
    return left.blockers < right.blockers;
}

void initialize_choose_table() {
    choose_table[0][0] = 1;
    for (int n = 1; n <= N; ++n) {
        choose_table[n][0] = 1;
        for (int k = 1; k <= W; ++k) {
            choose_table[n][k] = choose_table[n - 1][k - 1] + choose_table[n - 1][k];
        }
    }
}

std::uint32_t combinadic_rank(std::uint32_t word, int weight) {
    std::uint32_t rank = 0;
    int selected = 0;
    while (word != 0) {
        const int position = std::countr_zero(word);
        word &= word - 1;
        ++selected;
        rank += choose_table[position][selected];
    }
    if (selected != weight) {
        throw std::runtime_error("word has unexpected weight in combinadic_rank");
    }
    return rank;
}

std::vector<std::uint32_t> load_code(const std::string& path) {
    std::ifstream input(path);
    if (!input) {
        throw std::runtime_error("cannot open code file: " + path);
    }
    std::vector<std::uint32_t> code;
    std::string line;
    int line_number = 0;
    while (std::getline(input, line)) {
        ++line_number;
        if (!line.empty() && line.back() == '\r') {
            line.pop_back();
        }
        if (line.empty()) {
            continue;
        }
        if (line.size() != N) {
            throw std::runtime_error("line " + std::to_string(line_number) + " does not have length 32");
        }
        std::uint32_t word = 0;
        for (int i = 0; i < N; ++i) {
            if (line[i] == '1') {
                word |= std::uint32_t{1} << i;
            } else if (line[i] != '0') {
                throw std::runtime_error("nonbinary character on line " + std::to_string(line_number));
            }
        }
        if (std::popcount(word) != W) {
            throw std::runtime_error("line " + std::to_string(line_number) + " does not have weight 8");
        }
        code.push_back(word);
    }
    if (code.size() != EXPECTED_CODE_SIZE) {
        throw std::runtime_error("expected 1667 codewords, found " + std::to_string(code.size()));
    }
    std::vector<std::uint32_t> sorted = code;
    std::sort(sorted.begin(), sorted.end());
    if (std::adjacent_find(sorted.begin(), sorted.end()) != sorted.end()) {
        throw std::runtime_error("duplicate incumbent word");
    }
    int minimum_distance = N + 1;
    for (std::size_t i = 0; i < code.size(); ++i) {
        for (std::size_t j = i + 1; j < code.size(); ++j) {
            minimum_distance = std::min(minimum_distance, std::popcount(code[i] ^ code[j]));
        }
    }
    if (minimum_distance < 8) {
        throw std::runtime_error("incumbent minimum distance is below 8");
    }
    std::cerr << "verified incumbent: size=" << code.size()
              << " minimum_distance=" << minimum_distance << '\n';
    return code;
}

template <class Function>
void for_each_five_subset_rank(const std::array<int, W>& positions, Function function) {
    for (int a = 0; a <= W - T; ++a) {
        for (int b = a + 1; b <= W - T + 1; ++b) {
            for (int c = b + 1; c <= W - T + 2; ++c) {
                for (int d = c + 1; d <= W - T + 3; ++d) {
                    for (int e = d + 1; e < W; ++e) {
                        const std::uint32_t rank =
                            choose_table[positions[a]][1] +
                            choose_table[positions[b]][2] +
                            choose_table[positions[c]][3] +
                            choose_table[positions[d]][4] +
                            choose_table[positions[e]][5];
                        function(rank);
                    }
                }
            }
        }
    }
}

std::array<int, W> positions_of(std::uint32_t word) {
    std::array<int, W> positions{};
    int index = 0;
    while (word != 0) {
        positions[index++] = std::countr_zero(word);
        word &= word - 1;
    }
    if (index != W) {
        throw std::runtime_error("unexpected weight in positions_of");
    }
    return positions;
}

std::uint64_t next_same_weight(std::uint64_t word) {
    const std::uint64_t low = word & (~word + 1);
    const std::uint64_t ripple = word + low;
    return ripple + (((ripple ^ word) / low) >> 2);
}

struct Prepared {
    std::vector<std::uint32_t> code;
    std::vector<std::int16_t> five_owner;
    std::vector<std::uint8_t> is_incumbent_rank;
};

Prepared prepare(const std::string& path) {
    Prepared prepared;
    prepared.code = load_code(path);
    prepared.five_owner.assign(choose_table[N][T], -1);
    prepared.is_incumbent_rank.assign(choose_table[N][W], 0);

    for (std::size_t index = 0; index < prepared.code.size(); ++index) {
        const std::uint32_t word = prepared.code[index];
        const std::uint32_t word_rank = combinadic_rank(word, W);
        if (word_rank >= prepared.is_incumbent_rank.size() || prepared.is_incumbent_rank[word_rank]) {
            throw std::runtime_error("invalid or duplicate incumbent rank");
        }
        prepared.is_incumbent_rank[word_rank] = 1;
        const auto positions = positions_of(word);
        for_each_five_subset_rank(positions, [&](std::uint32_t rank) {
            if (rank >= prepared.five_owner.size()) {
                throw std::runtime_error("five-subset rank outside table");
            }
            if (prepared.five_owner[rank] != -1) {
                throw std::runtime_error("a five-subset occurs in two incumbent words");
            }
            prepared.five_owner[rank] = static_cast<std::int16_t>(index);
        });
    }
    const std::size_t occupied = static_cast<std::size_t>(std::count_if(
        prepared.five_owner.begin(), prepared.five_owner.end(), [](std::int16_t x) { return x >= 0; }));
    if (occupied != prepared.code.size() * choose_table[W][T]) {
        throw std::runtime_error("unexpected number of occupied five-subsets");
    }
    std::cerr << "occupied five-subsets=" << occupied << '/' << prepared.five_owner.size() << '\n';
    return prepared;
}

std::vector<LowCandidate> five_subset_profile(const Prepared& prepared, bool emit_candidates) {
    std::array<std::uint64_t, 57> histogram{};
    std::vector<std::uint32_t> marks(prepared.code.size(), 0);
    std::array<std::uint16_t, 56> blockers{};
    std::vector<LowCandidate> low;
    std::uint64_t candidate_count = 0;
    std::uint64_t outsider_count = 0;
    std::uint64_t total_blocker_incidences = 0;
    int minimum = 57;
    std::uint32_t minimum_word = 0;
    const auto started = std::chrono::steady_clock::now();

    std::uint64_t current = (std::uint64_t{1} << W) - 1;
    while ((current >> N) == 0) {
        const std::uint32_t word = static_cast<std::uint32_t>(current);
        if (candidate_count >= prepared.is_incumbent_rank.size()) {
            throw std::runtime_error("enumerated too many words");
        }
        if (!prepared.is_incumbent_rank[candidate_count]) {
            ++outsider_count;
            const auto positions = positions_of(word);
            const std::uint32_t stamp = static_cast<std::uint32_t>(candidate_count + 1);
            int blocker_count = 0;
            for_each_five_subset_rank(positions, [&](std::uint32_t rank) {
                const std::int16_t owner = prepared.five_owner[rank];
                if (owner >= 0 && marks[owner] != stamp) {
                    marks[owner] = stamp;
                    blockers[blocker_count++] = static_cast<std::uint16_t>(owner);
                }
            });
            if (blocker_count < 0 || blocker_count > 56) {
                throw std::runtime_error("invalid blocker count");
            }
            ++histogram[blocker_count];
            total_blocker_incidences += static_cast<std::uint64_t>(blocker_count);
            if (blocker_count < minimum) {
                minimum = blocker_count;
                minimum_word = word;
            }
            if (blocker_count <= 2) {
                std::sort(blockers.begin(), blockers.begin() + blocker_count);
                LowCandidate candidate;
                candidate.word = word;
                candidate.blocker_count = static_cast<std::uint8_t>(blocker_count);
                for (int i = 0; i < blocker_count; ++i) {
                    candidate.blockers[i] = blockers[i];
                }
                low.push_back(candidate);
            }
        }
        ++candidate_count;
        current = next_same_weight(current);
    }

    if (candidate_count != choose_table[N][W]) {
        throw std::runtime_error("weight-eight enumeration is incomplete");
    }
    const std::uint64_t histogram_sum =
        std::accumulate(histogram.begin(), histogram.end(), std::uint64_t{0});
    if (histogram_sum != outsider_count) {
        throw std::runtime_error("blocker histogram does not sum to outsider count");
    }
    std::uint64_t words_conflicting_with_one_incumbent = 0;
    for (int intersection = 5; intersection <= 8; ++intersection) {
        words_conflicting_with_one_incumbent +=
            static_cast<std::uint64_t>(choose_table[W][intersection]) *
            choose_table[N - W][W - intersection];
    }
    const std::uint64_t expected_outsider_incidences =
        prepared.code.size() * (words_conflicting_with_one_incumbent - 1);
    if (total_blocker_incidences != expected_outsider_incidences) {
        throw std::runtime_error("blocker incidences fail the independent double-count identity");
    }
    const auto elapsed = std::chrono::duration<double>(std::chrono::steady_clock::now() - started).count();
    std::cout << "algorithm=five_subset_owner\n";
    std::cout << "all_words=" << candidate_count << '\n';
    std::cout << "outsider_words=" << outsider_count << '\n';
    std::cout << "minimum_blockers=" << minimum << '\n';
    std::cout << "minimum_word_hex=" << std::hex << std::setw(8) << std::setfill('0') << minimum_word
              << std::dec << std::setfill(' ') << '\n';
    std::cout << "total_blocker_incidences=" << total_blocker_incidences << '\n';
    for (int i = 0; i <= 56; ++i) {
        if (histogram[i] != 0) {
            std::cout << "blocker_histogram[" << i << "]=" << histogram[i] << '\n';
        }
    }
    std::cout << "low_candidate_count=" << low.size() << '\n';
    if (emit_candidates) {
        for (const auto& candidate : low) {
            std::cout << "low=" << std::hex << std::setw(8) << std::setfill('0') << candidate.word
                      << std::dec << std::setfill(' ') << ':' << static_cast<int>(candidate.blocker_count);
            for (int i = 0; i < candidate.blocker_count; ++i) {
                std::cout << ':' << candidate.blockers[i];
            }
            std::cout << '\n';
        }
    }
    std::cerr << "five_subset_elapsed_seconds=" << std::fixed << std::setprecision(6) << elapsed << '\n';
    return low;
}

void write_low_candidates(const std::string& path, const std::vector<LowCandidate>& low) {
    std::ofstream output(path);
    if (!output) {
        throw std::runtime_error("cannot write low-candidate file: " + path);
    }
    output << "word_hex\tblocker_count\tblockers_zero_based\n";
    for (const auto& candidate : low) {
        output << std::hex << std::setw(8) << std::setfill('0') << candidate.word
               << std::dec << std::setfill(' ') << '\t' << static_cast<int>(candidate.blocker_count) << '\t';
        for (int i = 0; i < candidate.blocker_count; ++i) {
            if (i != 0) {
                output << ',';
            }
            output << candidate.blockers[i];
        }
        output << '\n';
    }
    if (!output) {
        throw std::runtime_error("failed while writing low-candidate file: " + path);
    }
}

bool compatible(std::uint32_t left, std::uint32_t right) {
    return std::popcount(left & right) <= 4;
}

void decide_small_exchanges(const Prepared& prepared, const std::vector<LowCandidate>& low) {
    std::vector<std::vector<std::uint32_t>> singleton(prepared.code.size());
    std::map<std::pair<int, int>, std::vector<std::uint32_t>> pairs;
    for (const auto& candidate : low) {
        if (candidate.blocker_count == 0) {
            throw std::runtime_error("direct insertion exists; incumbent was not maximal");
        }
        if (candidate.blocker_count == 1) {
            singleton[candidate.blockers[0]].push_back(candidate.word);
        } else if (candidate.blocker_count == 2) {
            const int first = candidate.blockers[0];
            const int second = candidate.blockers[1];
            if (first >= second) {
                throw std::runtime_error("noncanonical blocker pair");
            }
            pairs[{first, second}].push_back(candidate.word);
        } else {
            throw std::runtime_error("unexpected candidate in low list");
        }
    }

    std::uint64_t one_removal_add_pairs = 0;
    std::uint64_t singleton_buckets = 0;
    for (std::size_t removed = 0; removed < singleton.size(); ++removed) {
        const auto& candidates = singleton[removed];
        if (!candidates.empty()) {
            ++singleton_buckets;
        }
        for (std::size_t first = 0; first < candidates.size(); ++first) {
            for (std::size_t second = first + 1; second < candidates.size(); ++second) {
                ++one_removal_add_pairs;
                if (compatible(candidates[first], candidates[second])) {
                    std::cout << "one_removal_exchange=FOUND:" << removed << ':'
                              << std::hex << candidates[first] << ':' << candidates[second] << std::dec << '\n';
                    throw std::runtime_error("unexpected size-increasing one-removal exchange");
                }
            }
        }
    }

    std::uint64_t removal_pairs = 0;
    std::uint64_t nontrivial_pools = 0;
    std::uint64_t add_triples = 0;
    for (int first_removed = 0; first_removed < static_cast<int>(prepared.code.size()); ++first_removed) {
        for (int second_removed = first_removed + 1;
             second_removed < static_cast<int>(prepared.code.size()); ++second_removed) {
            ++removal_pairs;
            std::vector<std::uint32_t> candidates;
            candidates.insert(candidates.end(), singleton[first_removed].begin(), singleton[first_removed].end());
            candidates.insert(candidates.end(), singleton[second_removed].begin(), singleton[second_removed].end());
            const auto pair_it = pairs.find({first_removed, second_removed});
            if (pair_it != pairs.end()) {
                candidates.insert(candidates.end(), pair_it->second.begin(), pair_it->second.end());
            }
            if (candidates.size() < 3) {
                continue;
            }
            ++nontrivial_pools;
            for (std::size_t first = 0; first < candidates.size(); ++first) {
                for (std::size_t second = first + 1; second < candidates.size(); ++second) {
                    for (std::size_t third = second + 1; third < candidates.size(); ++third) {
                        ++add_triples;
                        if (compatible(candidates[first], candidates[second]) &&
                            compatible(candidates[first], candidates[third]) &&
                            compatible(candidates[second], candidates[third])) {
                            std::cout << "two_removal_exchange=FOUND:" << first_removed << ':' << second_removed
                                      << ':' << std::hex << candidates[first] << ':' << candidates[second]
                                      << ':' << candidates[third] << std::dec << '\n';
                            throw std::runtime_error("unexpected size-increasing two-removal exchange");
                        }
                    }
                }
            }
        }
    }
    std::cout << "singleton_candidate_count="
              << std::count_if(low.begin(), low.end(), [](const LowCandidate& candidate) {
                     return candidate.blocker_count == 1;
                 }) << '\n';
    std::cout << "singleton_blocker_buckets=" << singleton_buckets << '\n';
    std::cout << "double_blocker_candidate_count="
              << std::count_if(low.begin(), low.end(), [](const LowCandidate& candidate) {
                     return candidate.blocker_count == 2;
                 }) << '\n';
    std::cout << "double_blocker_buckets=" << pairs.size() << '\n';
    std::cout << "one_removal_add_pairs_tested=" << one_removal_add_pairs << '\n';
    std::cout << "one_removal_exchange=NONE\n";
    std::cout << "removal_pairs_tested=" << removal_pairs << '\n';
    std::cout << "two_removal_pools_with_at_least_three_candidates=" << nontrivial_pools << '\n';
    std::cout << "two_removal_add_triples_tested=" << add_triples << '\n';
    std::cout << "two_removal_exchange=NONE\n";
    std::cout << "conclusion=incumbent_is_2_exchange_maximal\n";
}

std::vector<LowCandidate> direct_threshold_scan(const Prepared& prepared) {
    std::array<std::uint64_t, 4> truncated_histogram{};
    std::vector<LowCandidate> low;
    std::uint64_t candidate_count = 0;
    std::uint64_t outsider_count = 0;
    const auto started = std::chrono::steady_clock::now();

    std::uint64_t current = (std::uint64_t{1} << W) - 1;
    while ((current >> N) == 0) {
        const std::uint32_t word = static_cast<std::uint32_t>(current);
        if (!prepared.is_incumbent_rank[candidate_count]) {
            ++outsider_count;
            LowCandidate candidate;
            candidate.word = word;
            int blocker_count = 0;
            for (std::size_t index = 0; index < prepared.code.size(); ++index) {
                if (std::popcount(word & prepared.code[index]) >= 5) {
                    if (blocker_count < 2) {
                        candidate.blockers[blocker_count] = static_cast<std::uint16_t>(index);
                    }
                    ++blocker_count;
                    if (blocker_count == 3) {
                        break;
                    }
                }
            }
            ++truncated_histogram[std::min(blocker_count, 3)];
            if (blocker_count <= 2) {
                candidate.blocker_count = static_cast<std::uint8_t>(blocker_count);
                low.push_back(candidate);
            }
        }
        ++candidate_count;
        current = next_same_weight(current);
    }
    if (candidate_count != choose_table[N][W]) {
        throw std::runtime_error("direct enumeration is incomplete");
    }
    const std::uint64_t histogram_sum = std::accumulate(
        truncated_histogram.begin(), truncated_histogram.end(), std::uint64_t{0});
    if (histogram_sum != outsider_count) {
        throw std::runtime_error("truncated histogram does not sum to outsider count");
    }
    const auto elapsed = std::chrono::duration<double>(std::chrono::steady_clock::now() - started).count();
    std::cout << "algorithm=direct_popcount_threshold\n";
    std::cout << "all_words=" << candidate_count << '\n';
    std::cout << "outsider_words=" << outsider_count << '\n';
    for (int i = 0; i <= 3; ++i) {
        const char* label = i == 3 ? "3_or_more" : nullptr;
        if (label != nullptr) {
            std::cout << "truncated_blocker_histogram[" << label << "]=" << truncated_histogram[i] << '\n';
        } else {
            std::cout << "truncated_blocker_histogram[" << i << "]=" << truncated_histogram[i] << '\n';
        }
    }
    std::cout << "low_candidate_count=" << low.size() << '\n';
    std::cerr << "direct_elapsed_seconds=" << std::fixed << std::setprecision(6) << elapsed << '\n';
    return low;
}

void run_self_test() {
    if (choose_table[32][8] != 10518300 || choose_table[32][5] != 201376 || choose_table[8][5] != 56) {
        throw std::runtime_error("binomial table self-test failed");
    }
    std::uint64_t current = (std::uint64_t{1} << W) - 1;
    std::uint32_t rank = 0;
    while ((current >> N) == 0) {
        if (combinadic_rank(static_cast<std::uint32_t>(current), W) != rank) {
            throw std::runtime_error("Gosper/combinadic order self-test failed");
        }
        ++rank;
        current = next_same_weight(current);
    }
    if (rank != choose_table[N][W]) {
        throw std::runtime_error("enumeration count self-test failed");
    }
    std::cout << "self_test=PASS\n";
}

}  // namespace

int main(int argc, char** argv) {
    try {
        initialize_choose_table();
        if (argc == 2 && std::string(argv[1]) == "--self-test") {
            run_self_test();
            return 0;
        }
        if (argc < 3 || argc > 4) {
            std::cerr << "usage: " << argv[0]
                      << " (--profile|--direct-low|--analyze) CODE_FILE [LOW_CANDIDATE_OUTPUT]\n";
            return 2;
        }
        const std::string mode = argv[1];
        const Prepared prepared = prepare(argv[2]);
        if (mode == "--profile") {
            five_subset_profile(prepared, true);
        } else if (mode == "--direct-low") {
            direct_threshold_scan(prepared);
        } else if (mode == "--analyze") {
            if (argc != 4) {
                throw std::runtime_error("--analyze requires LOW_CANDIDATE_OUTPUT");
            }
            std::vector<LowCandidate> owner_low = five_subset_profile(prepared, false);
            std::vector<LowCandidate> direct_low = direct_threshold_scan(prepared);
            std::sort(owner_low.begin(), owner_low.end(), low_candidate_less);
            std::sort(direct_low.begin(), direct_low.end(), low_candidate_less);
            if (owner_low != direct_low) {
                throw std::runtime_error("independent low-candidate enumerations disagree");
            }
            std::cout << "independent_low_candidate_comparison=PASS\n";
            write_low_candidates(argv[3], owner_low);
            decide_small_exchanges(prepared, owner_low);
        } else {
            throw std::runtime_error("unknown mode: " + mode);
        }
        return 0;
    } catch (const std::exception& error) {
        std::cerr << "ERROR: " << error.what() << '\n';
        return 1;
    }
}
