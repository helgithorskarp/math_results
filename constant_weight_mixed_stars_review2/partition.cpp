// six-reviewer-2: point-neighbor partitions followed by complete residual pair covers.
#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <string>
#include <tuple>
#include <vector>

constexpr int MAXCOL = 840;
constexpr int CW = (MAXCOL + 63) / 64;
using Cols = std::array<std::uint64_t, CW>;
struct Rows {
    std::uint64_t lo = 0, hi = 0;
    bool empty() const { return lo == 0 && hi == 0; }
    bool has(int j) const { return ((j < 64 ? lo : hi) >> (j % 64) & 1U) != 0; }
    void add(int j) { (j < 64 ? lo : hi) |= std::uint64_t{1} << (j % 64); }
    void remove(int j) { (j < 64 ? lo : hi) &= ~(std::uint64_t{1} << (j % 64)); }
    Rows without(Rows q) const { return {lo & ~q.lo, hi & ~q.hi}; }
    bool contains(Rows q) const { return (lo & q.lo) == q.lo && (hi & q.hi) == q.hi; }
};
static int pop(std::uint64_t x) { return __builtin_popcountll(x); }
static int first(std::uint64_t x) {
    if (!x) throw std::runtime_error("zero first-bit input");
    return __builtin_ctzll(x);
}
static Cols intersect(const Cols &a, const Cols &b) {
    Cols r{};
    for (int j = 0; j < CW; ++j) r[j] = a[j] & b[j];
    return r;
}
static Cols exclude(const Cols &a, const Cols &b) {
    Cols r{};
    for (int j = 0; j < CW; ++j) r[j] = a[j] & ~b[j];
    return r;
}
static void add(Cols &a, int j) { a[j / 64] |= std::uint64_t{1} << (j % 64); }
static bool has(const Cols &a, int j) { return ((a[j / 64] >> (j % 64)) & 1U) != 0; }

class Census {
public:
    int n, k, nr;
    std::vector<unsigned> words;
    std::vector<Rows> columns;
    std::vector<Cols> at, conflicts;
    std::vector<std::pair<int, int>> pairs;
    Cols all{};
    std::uint64_t cap, states = 0;
    std::chrono::steady_clock::time_point started;
    std::vector<std::vector<unsigned>> answers;
    std::vector<int> chosen;
    std::array<std::vector<std::pair<unsigned, int>>, 16> tails;

    Census(int nv, std::vector<unsigned> input, std::uint64_t limit)
        : n(nv), k(static_cast<int>(input.size())), nr(nv * (nv - 1) / 2),
          words(std::move(input)), columns(k), at(nr), conflicts(k), cap(limit) {
        for (int x = 0; x < n; ++x) for (int y = x + 1; y < n; ++y) pairs.emplace_back(x, y);
        for (int i = 0; i < k; ++i) {
            if (words[i] >= (1U << n) || __builtin_popcount(words[i]) != 4)
                throw std::runtime_error("malformed four-point column");
            if (std::find(words.begin(), words.begin() + i, words[i]) != words.begin() + i)
                throw std::runtime_error("duplicate column");
            add(all, i);
            for (int j = 0; j < nr; ++j) {
                const auto [x, y] = pairs[j];
                if ((words[i] >> x & 1U) && (words[i] >> y & 1U)) {
                    columns[i].add(j);
                    add(at[j], i);
                }
            }
        }
        for (int i = 0; i < k; ++i) for (int j = 0; j < nr; ++j)
            if (columns[i].has(j)) for (int b = 0; b < CW; ++b) conflicts[i][b] |= at[j][b];
    }

    void guard() {
        ++states;
        if (states > cap || ((states & 255U) == 0 &&
            std::chrono::duration<double>(std::chrono::steady_clock::now() - started).count() > 10.0))
            throw std::runtime_error("INCOMPLETE: point-partition guard");
    }
    void complete() {
        std::vector<unsigned> result;
        for (int i : chosen) result.push_back(words[i]);
        std::sort(result.begin(), result.end());
        answers.push_back(std::move(result));
    }
    void suffix(Rows rows, Cols active) {
        guard();
        if (rows.empty()) { complete(); return; }
        int best = std::numeric_limits<int>::max(), selected = -1;
        for (int j = nr - 1; j >= 0; --j) if (rows.has(j)) {
            int count = 0;
            for (int b = 0; b < CW; ++b) {
                count += pop(at[j][b] & active[b]);
                if (count >= best) break;
            }
            if (count == 0) return;
            if (count < best) { best = count; selected = j; }
            if (best == 1) break;
        }
        if (selected < 0) throw std::runtime_error("missing residual row");
        Cols choices = intersect(at[selected], active);
        for (int b = 0; b < CW; ++b) while (choices[b]) {
            const int i = b * 64 + first(choices[b]);
            choices[b] &= choices[b] - 1;
            if (i >= k || !rows.contains(columns[i])) throw std::runtime_error("invalid active column");
            chosen.push_back(i);
            suffix(rows.without(columns[i]), exclude(active, conflicts[i]));
            chosen.pop_back();
        }
    }
    void partition(unsigned remaining, Rows rows, Cols active) {
        guard();
        if (remaining == 0) { suffix(rows, active); return; }
        const int z = first(remaining);
        for (const auto &[tail, i] : tails[z]) if ((tail & remaining) == tail) {
            if (!has(active, i) || !rows.contains(columns[i]))
                throw std::runtime_error("disjoint tails unexpectedly conflict");
            chosen.push_back(i);
            partition(remaining ^ tail, rows.without(columns[i]), exclude(active, conflicts[i]));
            chosen.pop_back();
        }
    }
    void run(Rows rows) {
        started = std::chrono::steady_clock::now();
        states = 0; answers.clear(); chosen.clear();
        for (auto &list : tails) list.clear();
        Cols active = all;
        std::array<unsigned, 16> neighbors{};
        int required = 0;
        for (int j = 0; j < nr; ++j) {
            if (!rows.has(j)) active = exclude(active, at[j]);
            else {
                ++required;
                const auto [x, y] = pairs[j];
                neighbors[x] |= 1U << y; neighbors[y] |= 1U << x;
            }
        }
        if (rows.empty()) { guard(); complete(); }
        else if (required % 6 == 0) {
            int point = -1;
            std::tuple<int, int, int> best{100, 10000, 100};
            bool impossible = false;
            for (int z = 0; z < n; ++z) if (neighbors[z]) {
                const int degree = __builtin_popcount(neighbors[z]);
                if (degree % 3) { impossible = true; break; }
                int count = 0;
                for (int i = 0; i < k; ++i) if (has(active, i) && (words[i] >> z & 1U)) ++count;
                const auto choice = std::make_tuple(degree, count, z);
                if (choice < best) { best = choice; point = z; }
            }
            if (!impossible && point >= 0) {
                for (int i = 0; i < k; ++i) if (has(active, i) && (words[i] >> point & 1U)) {
                    const unsigned tail = words[i] ^ (1U << point);
                    for (int z = 0; z < n; ++z) if (tail >> z & 1U) tails[z].emplace_back(tail, i);
                }
                partition(neighbors[point], rows, active);
            }
        }
        if (std::chrono::duration<double>(std::chrono::steady_clock::now() - started).count() > 10.0)
            throw std::runtime_error("INCOMPLETE: final time guard");
        std::sort(answers.begin(), answers.end());
        if (std::adjacent_find(answers.begin(), answers.end()) != answers.end())
            throw std::runtime_error("duplicate complete cover");
        for (const auto &answer : answers) {
            if (answer.size() * 6 != static_cast<std::size_t>(required))
                throw std::runtime_error("wrong returned cover size");
            Rows covered{};
            for (unsigned w : answer) {
                const auto position = std::find(words.begin(), words.end(), w);
                if (position == words.end()) throw std::runtime_error("unknown witness column");
                const Rows r = columns[static_cast<std::size_t>(position - words.begin())];
                if ((covered.lo & r.lo) || (covered.hi & r.hi) || !rows.contains(r))
                    throw std::runtime_error("false cover witness");
                covered.lo |= r.lo; covered.hi |= r.hi;
            }
            if (covered.lo != rows.lo || covered.hi != rows.hi) throw std::runtime_error("incomplete witness rows");
        }
    }
};

int main(int argc, char **argv) {
    try {
        if (argc != 3 && argc != 4) throw std::runtime_error("usage: partition INPUT OUTPUT [state-cap<=200000]");
        std::uint64_t cap = 200000;
        if (argc == 4) {
            std::size_t used = 0;
            cap = std::stoull(argv[3], &used);
            if (used != std::string(argv[3]).size() || cap > 200000) throw std::runtime_error("invalid or raised state cap");
        }
        std::ifstream in(argv[1]); std::ofstream out(argv[2]);
        if (!in || !out) throw std::runtime_error("input/output open failure");
        long long n, k, cases;
        if (!(in >> n >> k >> cases) || n < 0 || n > 16 || k < 0 || k > MAXCOL || cases < 0 || cases > 1000)
            throw std::runtime_error("malformed dimensions");
        std::vector<unsigned> words;
        for (long long i = 0; i < k; ++i) {
            long long value;
            if (!(in >> value) || value < 0 || value >= (1LL << n)) throw std::runtime_error("malformed column mask");
            words.push_back(static_cast<unsigned>(value));
        }
        Census engine(static_cast<int>(n), words, cap);
        std::vector<long long> ids;
        std::uint64_t total_states = 0, total_covers = 0;
        for (long long test = 0; test < cases; ++test) {
            long long id, missing;
            if (!(in >> id >> missing) || id < 0 || id > 1000000000 || missing < 0 || missing > engine.nr ||
                std::find(ids.begin(), ids.end(), id) != ids.end()) throw std::runtime_error("malformed case header");
            ids.push_back(id);
            Rows target{};
            for (int j = 0; j < engine.nr; ++j) target.add(j);
            for (long long j = 0; j < missing; ++j) {
                long long r;
                if (!(in >> r) || r < 0 || r >= engine.nr || !target.has(static_cast<int>(r)))
                    throw std::runtime_error("invalid or repeated excluded pair");
                target.remove(static_cast<int>(r));
            }
            engine.run(target);
            total_states += engine.states; total_covers += engine.answers.size();
            out << "{\"index\":" << id << ",\"states\":" << engine.states << ",\"covers\":[";
            for (std::size_t j = 0; j < engine.answers.size(); ++j) {
                if (j) out << ',';
                out << '[';
                for (std::size_t z = 0; z < engine.answers[j].size(); ++z) {
                    if (z) out << ',';
                    out << engine.answers[j][z];
                }
                out << ']';
            }
            out << "]}\n";
            if (!out) throw std::runtime_error("output write failure");
        }
        std::string extra;
        if (in >> extra) throw std::runtime_error("unexpected trailing input");
        std::cout << "{\"status\":\"COMPLETE\",\"cases\":" << cases << ",\"states\":" << total_states
                  << ",\"covers\":" << total_covers << "}\n";
    } catch (const std::exception &error) {
        std::cerr << error.what() << '\n';
        return 2;
    }
    return 0;
}
