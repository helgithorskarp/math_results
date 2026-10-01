// Independent sparse linked-list exact-cover replay, one process/thread.
// Matrix sizes are bounded; guards match production (200000 nodes,10s).
#include <algorithm>
#include <chrono>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

using Clock = std::chrono::steady_clock;

int integer(std::istream& in) {
    int value;
    if (!(in >> value)) throw std::runtime_error("malformed/truncated matrix");
    return value;
}

struct SparseCover {
    std::vector<int> left, right, up, down, column, row, size;
    const std::vector<int>& words;
    std::vector<int> chosen;
    std::vector<std::vector<int>> answers;
    unsigned long long nodes = 0, cap;
    Clock::time_point start = Clock::now();

    SparseCover(int ncols, const std::vector<std::vector<int>>& rows,
                const std::vector<int>& ids, const std::vector<bool>& forbidden,
                unsigned long long limit) : words(ids), cap(limit) {
        const int headers = ncols + 1;
        left.resize(headers); right.resize(headers);
        up.resize(headers); down.resize(headers);
        column.resize(headers); row.resize(headers, -1); size.resize(headers, 0);
        for (int k = 0; k < headers; ++k) {
            left[k] = right[k] = up[k] = down[k] = column[k] = k;
        }
        int previous = 0;
        for (int k = 1; k <= ncols; ++k) {
            if (forbidden[k - 1]) continue;
            right[previous] = k; left[k] = previous; previous = k;
        }
        right[previous] = 0; left[0] = previous;
        for (int r = 0; r < static_cast<int>(rows.size()); ++r) {
            bool usable = true;
            for (int k : rows[r]) if (forbidden[k]) usable = false;
            if (!usable) continue;
            int first = -1;
            for (int k : rows[r]) {
                const int c = k + 1, node = static_cast<int>(left.size());
                left.push_back(node); right.push_back(node);
                up.push_back(up[c]); down.push_back(c);
                column.push_back(c); row.push_back(r); size.push_back(0);
                down[up[c]] = node; up[c] = node; ++size[c];
                if (first < 0) first = node;
                else {
                    left[node] = left[first]; right[node] = first;
                    right[left[first]] = node; left[first] = node;
                }
            }
        }
        if (left.size() > 8125) throw std::runtime_error("linked matrix capacity exceeded");
    }

    void cover(int c) {
        right[left[c]] = right[c]; left[right[c]] = left[c];
        for (int r = down[c]; r != c; r = down[r]) {
            for (int j = right[r]; j != r; j = right[j]) {
                down[up[j]] = down[j]; up[down[j]] = up[j]; --size[column[j]];
            }
        }
    }

    void uncover(int c) {
        for (int r = up[c]; r != c; r = up[r]) {
            for (int j = left[r]; j != r; j = left[j]) {
                ++size[column[j]]; down[up[j]] = j; up[down[j]] = j;
            }
        }
        right[left[c]] = c; left[right[c]] = c;
    }

    void visit() {
        ++nodes;
        if (nodes > cap || ((nodes & 255ULL) == 0 &&
            std::chrono::duration<double>(Clock::now() - start).count() > 10.0))
            throw std::runtime_error("INCOMPLETE sparse cover node/time guard");
        if (right[0] == 0) {
            std::vector<int> answer;
            for (int r : chosen) answer.push_back(words[r]);
            std::sort(answer.begin(), answer.end()); answers.push_back(answer);
            return;
        }
        int best = right[0];
        for (int c = right[best]; c != 0; c = right[c])
            if (size[c] < size[best]) best = c;
        if (size[best] == 0) return;
        cover(best);
        for (int r = down[best]; r != best; r = down[r]) {
            chosen.push_back(row[r]);
            for (int j = right[r]; j != r; j = right[j]) cover(column[j]);
            visit();
            for (int j = left[r]; j != r; j = left[j]) uncover(column[j]);
            chosen.pop_back();
        }
        uncover(best);
    }
};

int main(int argc, char** argv) {
    try {
        if (argc < 3 || argc > 4) throw std::runtime_error("usage: dlx INPUT OUTPUT [NODE_CAP]");
        unsigned long long cap = argc == 4 ? std::stoull(argv[3]) : 200000ULL;
        if (cap < 1 || cap > 200000ULL) throw std::runtime_error("invalid node cap");
        std::ifstream in(argv[1]); std::ofstream out(argv[2]);
        if (!in || !out) throw std::runtime_error("matrix/output unavailable");
        const int ncols = integer(in), nrows = integer(in), width = integer(in);
        if (ncols < 0 || ncols > 120 || nrows < 0 || nrows > 1334 || width < 1 || width > 6)
            throw std::runtime_error("invalid matrix dimensions");
        std::vector<int> words(nrows);
        std::vector<std::vector<int>> rows(nrows);
        for (int r = 0; r < nrows; ++r) {
            words[r] = integer(in);
            if (words[r] < 0 || words[r] >= 131072) throw std::runtime_error("invalid word identifier");
            for (int j = 0; j < width; ++j) {
                int k = integer(in);
                if (k < 0 || k >= ncols || std::find(rows[r].begin(), rows[r].end(), k) != rows[r].end())
                    throw std::runtime_error("invalid/repeated matrix column");
                rows[r].push_back(k);
            }
        }
        auto ids = words; std::sort(ids.begin(), ids.end());
        if (std::adjacent_find(ids.begin(), ids.end()) != ids.end()) throw std::runtime_error("repeated word identifier");
        const int count = integer(in);
        if (count < 0 || count > 11855) throw std::runtime_error("invalid fiber count");
        unsigned long long total_nodes = 0, total_covers = 0;
        for (int k = 0; k < count; ++k) {
            const int index = integer(in), excluded = integer(in);
            if (index != k || excluded < 0 || excluded > ncols) throw std::runtime_error("invalid fiber header");
            std::vector<bool> forbidden(ncols, false);
            for (int j = 0; j < excluded; ++j) {
                int e = integer(in);
                if (e < 0 || e >= ncols || forbidden[e]) throw std::runtime_error("invalid/repeated excluded column");
                forbidden[e] = true;
            }
            SparseCover search(ncols, rows, words, forbidden, cap);
            search.visit();
            std::sort(search.answers.begin(), search.answers.end());
            if (std::adjacent_find(search.answers.begin(), search.answers.end()) != search.answers.end())
                throw std::runtime_error("repeated sparse cover");
            out << "{\"index\":" << k << ",\"covers\":[";
            for (std::size_t a = 0; a < search.answers.size(); ++a) {
                if (a) out << ',';
                out << '[';
                for (std::size_t j = 0; j < search.answers[a].size(); ++j) {
                    if (j) out << ',';
                    out << search.answers[a][j];
                }
                out << ']';
            }
            out << "],\"nodes\":" << search.nodes << "}\n";
            if (!out) throw std::runtime_error("failed sparse output write");
            total_nodes += search.nodes; total_covers += search.answers.size();
        }
        std::string extra;
        if (in >> extra) throw std::runtime_error("unexpected trailing matrix data");
        out.flush();
        if (!out) throw std::runtime_error("failed sparse output flush");
        std::cout << "{\"status\":\"COMPLETE\",\"cases\":" << count << ",\"covers\":"
                  << total_covers << ",\"nodes\":" << total_nodes << "}\n";
        return 0;
    } catch (const std::exception& e) {
        std::cerr << e.what() << '\n'; return 2;
    }
}
