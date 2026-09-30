// Independent Algorithm X using doubly linked sparse columns (Dancing Links).
// The Python checker generates the complete input and checks every output cover.
#include <algorithm>
#include <chrono>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

using Clock = std::chrono::steady_clock;

struct DLX {
    std::vector<int> left, right, up, down, column, row, size;
    std::vector<int> selected;
    std::vector<std::vector<int>> answers;
    const std::vector<int>& words;
    unsigned long long nodes = 0;
    unsigned long long cap;
    Clock::time_point started;

    int add_node(int c, int r) {
        int i = static_cast<int>(left.size());
        left.push_back(i); right.push_back(i); up.push_back(i); down.push_back(i);
        column.push_back(c); row.push_back(r); size.push_back(0);
        return i;
    }

    DLX(int count, const std::vector<std::vector<int>>& pairs,
        const std::vector<bool>& forbidden, const std::vector<int>& masks,
        unsigned long long limit) : words(masks), cap(limit), started(Clock::now()) {
        add_node(0, -1);
        std::vector<int> headers(count, -1);
        for (int p = 0; p < count; ++p) {
            if (forbidden[p]) continue;
            int h = add_node(0, -1);
            column[h] = h;
            headers[p] = h;
            left[h] = left[0]; right[h] = 0;
            right[left[0]] = h; left[0] = h;
        }
        for (int r = 0; r < static_cast<int>(pairs.size()); ++r) {
            bool usable = true;
            for (int p : pairs[r]) if (forbidden[p]) usable = false;
            if (!usable) continue;
            int first = -1;
            for (int p : pairs[r]) {
                int h = headers[p];
                if (h < 0) throw std::runtime_error("missing column header");
                int i = add_node(h, r);
                up[i] = up[h]; down[i] = h;
                down[up[h]] = i; up[h] = i; ++size[h];
                if (first < 0) first = i;
                else {
                    left[i] = left[first]; right[i] = first;
                    right[left[first]] = i; left[first] = i;
                }
            }
        }
        if (left.size() > 10000) throw std::runtime_error("sparse matrix capacity");
    }

    void cover(int c) {
        right[left[c]] = right[c]; left[right[c]] = left[c];
        for (int i = down[c]; i != c; i = down[i]) {
            for (int j = right[i]; j != i; j = right[j]) {
                down[up[j]] = down[j]; up[down[j]] = up[j]; --size[column[j]];
            }
        }
    }

    void uncover(int c) {
        for (int i = up[c]; i != c; i = up[i]) {
            for (int j = left[i]; j != i; j = left[j]) {
                ++size[column[j]]; down[up[j]] = j; up[down[j]] = j;
            }
        }
        right[left[c]] = c; left[right[c]] = c;
    }

    void visit() {
        ++nodes;
        if (nodes > cap || ((nodes & 255ULL) == 0 &&
            std::chrono::duration<double>(Clock::now() - started).count() > 10.0))
            throw std::runtime_error("INCOMPLETE Algorithm-X node/time guard");
        if (right[0] == 0) {
            std::vector<int> answer;
            for (int r : selected) answer.push_back(words[r]);
            std::sort(answer.begin(), answer.end());
            answers.push_back(answer);
            return;
        }
        int c = right[0];
        for (int h = right[c]; h != 0; h = right[h]) {
            if (size[h] < size[c]) c = h;
            if (size[c] == 0) break;
        }
        cover(c);
        for (int i = down[c]; i != c; i = down[i]) {
            selected.push_back(row[i]);
            for (int j = right[i]; j != i; j = right[j]) cover(column[j]);
            visit();
            for (int j = left[i]; j != i; j = left[j]) uncover(column[j]);
            selected.pop_back();
        }
        uncover(c);
    }
};

int read_int(std::istream& input) {
    int value;
    if (!(input >> value)) throw std::runtime_error("truncated or malformed input");
    return value;
}

int main(int argc, char** argv) {
    try {
        if (argc < 3 || argc > 4) throw std::runtime_error("usage: cover INPUT OUTPUT [NODE_CAP]");
        unsigned long long cap = argc == 4 ? std::stoull(argv[3]) : 200000ULL;
        if (cap == 0 || cap > 200000ULL) throw std::runtime_error("invalid node cap");
        std::ifstream input(argv[1]);
        std::ofstream output(argv[2]);
        if (!input || !output) throw std::runtime_error("input/output unavailable");
        int ncols = read_int(input), nrows = read_int(input), width = read_int(input);
        if (ncols < 0 || ncols > 120 || nrows < 0 || nrows > 840 || width < 1 || width > 6)
            throw std::runtime_error("invalid sparse matrix dimensions");
        std::vector<int> words(nrows);
        std::vector<std::vector<int>> pairs(nrows);
        for (int r = 0; r < nrows; ++r) {
            words[r] = read_int(input);
            if (words[r] < 0 || words[r] >= 65536) throw std::runtime_error("invalid word mask");
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
            DLX search(ncols, pairs, forbidden, words, cap);
            search.visit();
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
