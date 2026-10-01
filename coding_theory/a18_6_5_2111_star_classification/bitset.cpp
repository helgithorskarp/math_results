// Production integer-bitset exact cover: MRV column and conflict deletion.
// Capacities cover the complete17-point four-set mathematical input.
// Original 200000-node and ten-second guards are unchanged.
#include <algorithm>
#include <array>
#include <chrono>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

using Word = unsigned long long;
using Rows = std::array<Word, 21>;
using Pairs = std::array<Word, 2>;
using Clock = std::chrono::steady_clock;

struct BitCover {
    const std::vector<int>& words;
    std::vector<Pairs> masks;
    std::array<Rows, 120> containing{};
    std::vector<Rows> conflicts;
    std::vector<int> selected;
    std::vector<std::vector<int>> answers;
    unsigned long long nodes = 0, cap;
    Clock::time_point started;

    BitCover(const std::vector<std::vector<int>>& rows, const std::vector<int>& ids,
             unsigned long long limit) : words(ids), masks(rows.size()),
             conflicts(rows.size()), cap(limit), started(Clock::now()) {
        for (int j = 0; j < static_cast<int>(rows.size()); ++j) {
            for (int k : rows[j]) {
                masks[j][k / 64] |= 1ULL << (k % 64);
                containing[k][j / 64] |= 1ULL << (j % 64);
            }
        }
        for (int j = 0; j < static_cast<int>(rows.size()); ++j)
            for (int k : rows[j])
                for (int u = 0; u < 21; ++u) conflicts[j][u] |= containing[k][u];
    }

    void visit(const Pairs& left, const Rows& active) {
        ++nodes;
        if (nodes > cap || ((nodes & 255ULL) == 0 &&
            std::chrono::duration<double>(Clock::now() - started).count() > 10.0))
            throw std::runtime_error("INCOMPLETE bitset node/time guard");
        if (left[0] == 0 && left[1] == 0) {
            std::vector<int> answer;
            for (int j : selected) answer.push_back(words[j]);
            std::sort(answer.begin(), answer.end());
            answers.push_back(answer);
            return;
        }
        int best = static_cast<int>(words.size()) + 1;
        Rows options{};
        bool stop = false;
        for (int u = 0; u < 2 && !stop; ++u) {
            Word pending = left[u];
            while (pending) {
                int k = 64 * u + __builtin_ctzll(pending);
                pending &= pending - 1;
                Rows choices{};
                int size = 0;
                for (int v = 0; v < 21; ++v) {
                    choices[v] = active[v] & containing[k][v];
                    size += __builtin_popcountll(choices[v]);
                }
                if (size < best) {
                    best = size; options = choices;
                    if (size <= 1) { stop = true; break; }
                }
            }
        }
        for (int u = 0; u < 21; ++u) {
            Word pending = options[u];
            while (pending) {
                int j = 64 * u + __builtin_ctzll(pending);
                pending &= pending - 1;
                if ((masks[j][0] & left[0]) != masks[j][0] ||
                    (masks[j][1] & left[1]) != masks[j][1])
                    throw std::runtime_error("active row does not fit remaining columns");
                Pairs next_left{left[0] ^ masks[j][0], left[1] ^ masks[j][1]};
                Rows next_active{};
                for (int v = 0; v < 21; ++v) next_active[v] = active[v] & ~conflicts[j][v];
                selected.push_back(j);
                visit(next_left, next_active);
                selected.pop_back();
            }
        }
    }

    void run(int count, const std::vector<bool>& forbidden) {
        Pairs target{};
        Rows active{};
        for (int j = 0; j < static_cast<int>(words.size()); ++j)
            active[j / 64] |= 1ULL << (j % 64);
        for (int k = 0; k < count; ++k) {
            if (forbidden[k]) {
                for (int v = 0; v < 21; ++v) active[v] &= ~containing[k][v];
            } else target[k / 64] |= 1ULL << (k % 64);
        }
        visit(target, active);
    }
};

int read_int(std::istream& input) {
    int value;
    if (!(input >> value)) throw std::runtime_error("truncated or malformed input");
    return value;
}

int main(int argc, char** argv) {
    try {
        if (argc < 3 || argc > 4) throw std::runtime_error("usage: bitset INPUT OUTPUT [NODE_CAP]");
        unsigned long long cap = argc == 4 ? std::stoull(argv[3]) : 200000ULL;
        if (cap == 0 || cap > 200000ULL) throw std::runtime_error("invalid node cap");
        std::ifstream input(argv[1]);
        std::ofstream output(argv[2]);
        if (!input || !output) throw std::runtime_error("input/output unavailable");
        int ncols = read_int(input), nrows = read_int(input), width = read_int(input);
        if (ncols < 0 || ncols > 120 || nrows < 0 || nrows > 1334 || width < 1 || width > 6)
            throw std::runtime_error("invalid sparse matrix dimensions");
        std::vector<int> words(nrows);
        std::vector<std::vector<int>> pairs(nrows);
        for (int r = 0; r < nrows; ++r) {
            words[r] = read_int(input);
            if (words[r] < 0 || words[r] >= 131072) throw std::runtime_error("invalid word mask");
            for (int j = 0; j < width; ++j) {
                int p = read_int(input);
                if (p < 0 || p >= ncols || std::find(pairs[r].begin(), pairs[r].end(), p) != pairs[r].end())
                    throw std::runtime_error("invalid or duplicated row column");
                pairs[r].push_back(p);
            }
        }
        auto unique_words = words;
        std::sort(unique_words.begin(), unique_words.end());
        if (std::adjacent_find(unique_words.begin(), unique_words.end()) != unique_words.end())
            throw std::runtime_error("duplicated word identifiers");
        int cases = read_int(input);
        if (cases < 0 || cases > 11855) throw std::runtime_error("invalid case count");
        unsigned long long total_nodes = 0, total_answers = 0;
        for (int k = 0; k < cases; ++k) {
            int index = read_int(input), excluded = read_int(input);
            if (index != k || excluded < 0 || excluded > ncols) throw std::runtime_error("invalid case header");
            std::vector<bool> forbidden(ncols, false);
            for (int j = 0; j < excluded; ++j) {
                int p = read_int(input);
                if (p < 0 || p >= ncols || forbidden[p]) throw std::runtime_error("invalid forbidden column");
                forbidden[p] = true;
            }
            BitCover search(pairs, words, cap);
            search.run(ncols, forbidden);
            std::sort(search.answers.begin(), search.answers.end());
            if (std::adjacent_find(search.answers.begin(), search.answers.end()) != search.answers.end())
                throw std::runtime_error("duplicated cover");
            output << "{\"index\":" << index << ",\"covers\":[";
            for (std::size_t i = 0; i < search.answers.size(); ++i) {
                if (i) output << ',';
                output << '[';
                for (std::size_t j = 0; j < search.answers[i].size(); ++j) {
                    if (j) output << ',';
                    output << search.answers[i][j];
                }
                output << ']';
            }
            output << "],\"nodes\":" << search.nodes << "}\n";
            if (!output) throw std::runtime_error("failed output write");
            total_nodes += search.nodes; total_answers += search.answers.size();
        }
        std::string extra;
        if (input >> extra) throw std::runtime_error("unexpected trailing input");
        output.flush();
        if (!output) throw std::runtime_error("failed final output write");
        std::cout << "{\"status\":\"COMPLETE\",\"cases\":" << cases
                  << ",\"covers\":" << total_answers << ",\"nodes\":" << total_nodes << "}\n";
        return 0;
    } catch (const std::exception& e) {
        std::cerr << e.what() << '\n';
        return 2;
    }
}
