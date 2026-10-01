// Single-thread, resumable six-state construction search. No exclusion claim.
#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <fstream>
#include <iostream>
#include <limits>
#include <random>
#include <stdexcept>
#include <string>
#include <vector>

constexpr int M = 207, N = 621;
using States = std::array<int, M>;
using Scores = std::array<std::array<int, 6>, M>;
using Tabu = std::array<std::array<std::uint64_t, 6>, M>;
struct Edge { std::array<int, 7> point; int count; };
int bit(int state, int y) { return (state / 3) ^ static_cast<int>(state % 3 == y); }
int mono(int count) { return static_cast<int>(count == 0 || count == 7); }

struct Search {
    States state{}, best{};
    Scores score{};
    Tabu tabu{};
    std::vector<Edge> edge;
    std::array<std::vector<int>, M> incident;
    std::vector<int> bad, slot;
    std::mt19937_64 rng{1729};
    std::uint64_t iteration = 0;
    int best_cost = std::numeric_limits<int>::max();

    void initialize(const std::string& checkpoint) {
        std::vector<int> saved_bad;
        bool restore_order = false;
        std::ifstream in(checkpoint);
        if (in) {
            std::string header;
            in >> header >> iteration >> best_cost;
            if ((header != "VDW621SEARCH1" && header != "VDW621SEARCH2") || iteration > 1000000000000ULL)
                throw std::runtime_error("invalid checkpoint header");
            for (int& s : state) in >> s;
            for (int& s : best) in >> s;
            for (auto& row : tabu) for (auto& value : row) in >> value;
            if (header == "VDW621SEARCH2") {
                int count = -1;
                in >> count;
                if (count < 0 || count > 190026) throw std::runtime_error("invalid bad-list size");
                saved_bad.resize(static_cast<std::size_t>(count));
                for (int& id : saved_bad) in >> id;
                restore_order = true;
            }
            in >> rng;
            if (!in) throw std::runtime_error("truncated checkpoint");
            std::string extra;
            if (in >> extra) throw std::runtime_error("trailing checkpoint data");
            for (int s : state) if (s < 0 || s > 5) throw std::runtime_error("bad state");
            for (int s : best) if (s < 0 || s > 5) throw std::runtime_error("bad best state");
        } else {
            std::array<int, 617> qr{};
            qr.fill(1); qr[0] = 0;
            for (int x = 1; x < 617; ++x) qr[(x * x) % 617] = 0;
            for (int x = 0; x < M; ++x) {
                std::array<int, 3> c{};
                int ones = 0;
                for (int y = 0; y < 3; ++y) { c[y] = qr[(x + M * y) % 617]; ones += c[y]; }
                if (ones == 0 || ones == 3) {
                    state[x] = 3 * static_cast<int>(ones == 3) + static_cast<int>(rng() % 3);
                } else {
                    const int majority = static_cast<int>(ones == 2);
                    int minority = 0;
                    while (c[minority] == majority) ++minority;
                    state[x] = 3 * majority + minority;
                }
            }
        }
        for (int d = 1; d <= 310; ++d) {
            if (d % 69 == 0) continue; // automatic order-three/order-nine safety
            for (int a = 0; a < N; ++a) {
                Edge row{};
                for (int j = 0; j < 7; ++j) row.point[j] = (a + j * d) % N;
                const int id = static_cast<int>(edge.size());
                for (int p : row.point) incident[p % M].push_back(id);
                edge.push_back(row);
            }
        }
        if (edge.size() != 190026) throw std::runtime_error("edge coverage mismatch");
        slot.assign(edge.size(), -1);
        for (int id = 0; id < static_cast<int>(edge.size()); ++id) {
            Edge& e = edge[id];
            for (int p : e.point) e.count += bit(state[p % M], p / M);
            set_bad(id);
        }
        if (restore_order) {
            if (saved_bad.size() != bad.size()) throw std::runtime_error("bad-list coverage mismatch");
            std::vector<int> seen(edge.size(), 0);
            for (int id : saved_bad) {
                if (id < 0 || id >= static_cast<int>(edge.size()) || slot[id] == -1 || seen[id]++)
                    throw std::runtime_error("invalid bad-list record");
            }
            bad = saved_bad;
            std::fill(slot.begin(), slot.end(), -1);
            for (int i = 0; i < static_cast<int>(bad.size()); ++i) slot[bad[i]] = i;
        }
        rebuild_scores(score);
        const int old_best = best_cost;
        if (old_best == std::numeric_limits<int>::max()) { best = state; best_cost = cost(best); }
        else if (cost(best) != old_best) throw std::runtime_error("best checkpoint cost mismatch");
    }

    int cost(const States& candidate) const {
        int result = 0;
        for (const Edge& e : edge) {
            int count = 0;
            for (int p : e.point) count += bit(candidate[p % M], p / M);
            result += mono(count);
        }
        return result;
    }

    void set_bad(int id) {
        const bool wanted = mono(edge[id].count) != 0;
        if (wanted && slot[id] == -1) {
            slot[id] = static_cast<int>(bad.size()); bad.push_back(id);
        } else if (!wanted && slot[id] != -1) {
            const int index = slot[id], last = bad.back();
            bad[index] = last; slot[last] = index; bad.pop_back(); slot[id] = -1;
        }
    }

    void rebuild_scores(Scores& target) const {
        target = {};
        for (const Edge& e : edge) {
            for (int p : e.point) {
                const int x = p % M, y = p / M, old_bit = bit(state[x], y);
                for (int s = 0; s < 6; ++s)
                    target[x][s] += mono(e.count + bit(s, y) - old_bit) - mono(e.count);
            }
        }
    }

    void audit() const {
        Scores fresh{};
        rebuild_scores(fresh);
        if (fresh != score || cost(state) != static_cast<int>(bad.size()))
            throw std::runtime_error("cached score/cost mismatch");
        for (int x = 0; x < M; ++x)
            if (score[x][state[x]] != 0) throw std::runtime_error("nonzero identity move");
    }

    void move(int x, int next) {
        const int previous = state[x], delta = score[x][next];
        for (int id : incident[x]) {
            Edge& e = edge[id];
            int own = -1;
            for (int p : e.point) if (p % M == x) {
                if (own != -1) throw std::runtime_error("repeated projected vertex");
                own = p;
            }
            if (own == -1) throw std::runtime_error("missing incident vertex");
            const int change = bit(next, own / M) - bit(previous, own / M);
            if (!change) continue;
            const int old_count = e.count, new_count = e.count + change;
            if (new_count < 0 || new_count > 7) throw std::runtime_error("invalid AP count");
            for (int p : e.point) if (p % M != x) {
                const int z = p % M, y = p / M, current_bit = bit(state[z], y);
                const int old_gradient = mono(old_count + 1 - 2 * current_bit) - mono(old_count);
                const int new_gradient = mono(new_count + 1 - 2 * current_bit) - mono(new_count);
                const int difference = new_gradient - old_gradient;
                if (difference) for (int s = 0; s < 6; ++s)
                    if (bit(s, y) != current_bit) score[z][s] += difference;
            }
            e.count = new_count;
            set_bad(id);
        }
        state[x] = next;
        for (int s = 0; s < 6; ++s) score[x][s] -= delta;
        tabu[x][previous] = iteration + 8 + rng() % 18;
        if (static_cast<int>(bad.size()) < best_cost) {
            best_cost = static_cast<int>(bad.size()); best = state;
            std::cout << "best " << best_cost << " iteration " << iteration << '\n' << std::flush;
        }
    }

    void step() {
        ++iteration;
        const Edge& selected = edge[bad[rng() % bad.size()]];
        int best_delta = std::numeric_limits<int>::max(), chosen_x = -1, chosen_state = -1;
        std::uint64_t ties = 0;
        for (int pass = 0; pass < 2 && chosen_x == -1; ++pass) {
            for (int p : selected.point) {
                const int x = p % M;
                for (int s = 0; s < 6; ++s) if (s != state[x]) {
                    const int delta = score[x][s];
                    if (pass == 0 && tabu[x][s] > iteration &&
                        static_cast<int>(bad.size()) + delta >= best_cost) continue;
                    if (delta < best_delta) { best_delta = delta; ties = 0; }
                    if (delta == best_delta && rng() % (++ties) == 0) { chosen_x = x; chosen_state = s; }
                }
            }
        }
        if (chosen_x == -1) throw std::runtime_error("no local move");
        move(chosen_x, chosen_state);
    }

    void save(const std::string& path) const {
        std::ofstream out(path + ".partial");
        out << "VDW621SEARCH2 " << iteration << ' ' << best_cost << '\n';
        for (int s : state) out << s << ' ';
        out << '\n';
        for (int s : best) out << s << ' ';
        out << '\n';
        for (const auto& row : tabu) for (auto v : row) out << v << ' ';
        out << '\n' << bad.size() << ' ';
        for (int id : bad) out << id << ' ';
        out << '\n' << rng << '\n';
        out.close();
        if (!out) throw std::runtime_error("checkpoint write failed");
        if (std::rename((path + ".partial").c_str(), path.c_str()))
            throw std::runtime_error("checkpoint rename failed");
        std::ofstream bits(path + ".best.bits");
        for (int n = 0; n < N; ++n) bits << bit(best[n % M], n / M);
        bits << '\n'; bits.close();
        if (!bits) throw std::runtime_error("best-word write failed");
    }
};

int main(int argc, char** argv) {
    try {
        if (argc != 4) throw std::runtime_error("usage: search621 CHECKPOINT STEPS SECONDS");
        const std::uint64_t steps = std::stoull(argv[2]);
        const double seconds = std::stod(argv[3]);
        if (steps == 0 || steps > 1000000 || !(seconds > 0 && seconds <= 55))
            throw std::runtime_error("bounded invocation requires steps<=1000000, 0<seconds<=55");
        Search search;
        search.initialize(argv[1]);
        search.audit();
        const auto start = std::chrono::steady_clock::now();
        const std::uint64_t first = search.iteration;
        while (!search.bad.empty() && search.iteration - first < steps) {
            if (std::chrono::duration<double>(std::chrono::steady_clock::now() - start).count() >= seconds) break;
            search.step();
            if (search.iteration % 1000 == 0) search.audit();
        }
        search.audit(); search.save(argv[1]);
        std::cout << "checkpoint iteration=" << search.iteration << " best=" << search.best_cost
                  << " current=" << search.bad.size() << " status="
                  << (search.best_cost == 0 ? "UNVERIFIED_PROPOSAL" : "NO_WITNESS_FOUND") << '\n';
        return 0;
    } catch (const std::exception& e) { std::cerr << e.what() << '\n'; return 1; }
}
