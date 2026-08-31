#include <algorithm>
#include <bitset>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <numeric>
#include <random>
#include <vector>

using namespace std;

namespace {

constexpr int kDimension = 9;
constexpr int kVertexCount = 1 << kDimension;

vector<int> closed_ball(int vertex) {
    vector<int> result{vertex};
    for (int coordinate = 0; coordinate < kDimension; ++coordinate) {
        result.push_back(vertex ^ (1 << coordinate));
    }
    sort(result.begin(), result.end());
    return result;
}

}  // namespace

int main(int argc, char** argv) {
    const int target = argc > 1 ? stoi(argv[1]) : 108;
    const uint64_t iterations = argc > 2 ? stoull(argv[2]) : 2000000ULL;
    const uint64_t seed = argc > 3 ? stoull(argv[3]) : 1;
    const uint64_t restart_interval = argc > 4 ? stoull(argv[4]) : 200000ULL;
    const string starting_file = argc > 5 ? argv[5] : "";
    mt19937_64 generator(seed);

    vector<int> starting_code;
    if (!starting_file.empty()) {
        ifstream input(starting_file);
        string word;
        while (input >> word) starting_code.push_back(stoi(word, nullptr, 2));
        sort(starting_code.begin(), starting_code.end());
        starting_code.erase(unique(starting_code.begin(), starting_code.end()), starting_code.end());
        if (static_cast<int>(starting_code.size()) < target) {
            cerr << "starting code is smaller than target\n";
            return 2;
        }
    }

    vector<vector<int>> balls(kVertexCount);
    for (int vertex = 0; vertex < kVertexCount; ++vertex) {
        balls[vertex] = closed_ball(vertex);
    }

    // Once domination is imposed, vertices at distance at least three have
    // nonempty signatures in disjoint closed balls and are automatically
    // separated.  Therefore only distance-one and distance-two pairs need
    // separation clauses.
    vector<vector<int>> clauses;
    clauses.reserve(kVertexCount * (1 + kDimension + kDimension * (kDimension - 1) / 2));
    for (int vertex = 0; vertex < kVertexCount; ++vertex) {
        clauses.push_back(balls[vertex]);
    }
    for (int first = 0; first < kVertexCount; ++first) {
        for (int second = first + 1; second < kVertexCount; ++second) {
            const int distance = __builtin_popcount(static_cast<unsigned>(first ^ second));
            if (distance > 2) continue;
            vector<int> clause{first, second};
            set_symmetric_difference(
                balls[first].begin(), balls[first].end(),
                balls[second].begin(), balls[second].end(),
                back_inserter(clause));
            sort(clause.begin(), clause.end());
            clause.erase(unique(clause.begin(), clause.end()), clause.end());
            clauses.push_back(move(clause));
        }
    }

    vector<vector<int>> incident(kVertexCount);
    for (int clause = 0; clause < static_cast<int>(clauses.size()); ++clause) {
        for (int vertex : clauses[clause]) incident[vertex].push_back(clause);
    }

    vector<char> chosen(kVertexCount);
    vector<int> cover(clauses.size());
    vector<int> break_score(kVertexCount);
    vector<int> make_score(kVertexCount);
    vector<int> uncovered;
    vector<int> uncovered_position(clauses.size(), -1);

    auto add_uncovered = [&](int clause) {
        if (uncovered_position[clause] >= 0) return;
        uncovered_position[clause] = static_cast<int>(uncovered.size());
        uncovered.push_back(clause);
        for (int vertex : clauses[clause]) ++make_score[vertex];
    };
    auto remove_uncovered = [&](int clause) {
        const int position = uncovered_position[clause];
        if (position < 0) return;
        for (int vertex : clauses[clause]) --make_score[vertex];
        const int moved = uncovered.back();
        uncovered[position] = moved;
        uncovered_position[moved] = position;
        uncovered.pop_back();
        uncovered_position[clause] = -1;
    };
    auto sole_chosen = [&](int clause, int except) {
        for (int vertex : clauses[clause]) {
            if (vertex != except && chosen[vertex]) return vertex;
        }
        return -1;
    };
    auto insert_vertex = [&](int vertex) {
        chosen[vertex] = true;
        break_score[vertex] = 0;
        for (int clause : incident[vertex]) {
            if (cover[clause] == 0) {
                remove_uncovered(clause);
                ++break_score[vertex];
            } else if (cover[clause] == 1) {
                const int old = sole_chosen(clause, vertex);
                if (old >= 0) --break_score[old];
            }
            ++cover[clause];
        }
    };
    auto erase_vertex = [&](int vertex) {
        for (int clause : incident[vertex]) {
            if (cover[clause] == 1) {
                add_uncovered(clause);
                --break_score[vertex];
            } else if (cover[clause] == 2) {
                const int remaining = sole_chosen(clause, vertex);
                if (remaining >= 0) ++break_score[remaining];
            }
            --cover[clause];
        }
        chosen[vertex] = false;
        break_score[vertex] = 0;
    };
    auto reset = [&]() {
        fill(chosen.begin(), chosen.end(), false);
        fill(cover.begin(), cover.end(), 0);
        fill(break_score.begin(), break_score.end(), 0);
        fill(make_score.begin(), make_score.end(), 0);
        uncovered.clear();
        fill(uncovered_position.begin(), uncovered_position.end(), -1);
        for (int clause = 0; clause < static_cast<int>(clauses.size()); ++clause) {
            add_uncovered(clause);
        }
        vector<int> order;
        if (starting_code.empty()) {
            order.resize(kVertexCount);
            iota(order.begin(), order.end(), 0);
        } else {
            order = starting_code;
        }
        shuffle(order.begin(), order.end(), generator);
        for (int index = 0; index < target; ++index) insert_vertex(order[index]);
    };

    cerr << "vertices=" << kVertexCount << " clauses=" << clauses.size()
         << " target=" << target << " seed=" << seed << '\n';
    reset();
    size_t best = uncovered.size();
    for (uint64_t step = 0; step < iterations; ++step) {
        if (uncovered.empty()) {
            cerr << "FOUND step=" << step << " seed=" << seed << '\n';
            for (int vertex = 0; vertex < kVertexCount; ++vertex) {
                if (chosen[vertex]) cout << bitset<kDimension>(vertex) << ' ';
            }
            cout << '\n';
            return 0;
        }
        if (uncovered.size() < best) {
            best = uncovered.size();
            cerr << "best=" << best << " step=" << step << " seed=" << seed << '\n';
        }

        const int clause = uncovered[generator() % uncovered.size()];
        int add = -1;
        int best_make = -1;
        const bool random_add = (generator() % 100) < 2;
        for (int vertex : clauses[clause]) {
            if (chosen[vertex]) continue;
            if (random_add) {
                if (add < 0 || (generator() & 1)) add = vertex;
            } else if (make_score[vertex] > best_make ||
                       (make_score[vertex] == best_make && (generator() & 1))) {
                best_make = make_score[vertex];
                add = vertex;
            }
        }
        if (add < 0) {
            reset();
            continue;
        }
        insert_vertex(add);

        int remove = -1;
        int best_break = 1 << 30;
        const bool random_remove = (generator() % 100) < 3;
        for (int vertex = 0; vertex < kVertexCount; ++vertex) {
            if (!chosen[vertex] || vertex == add) continue;
            if (random_remove) {
                if (remove < 0 || (generator() & 1)) remove = vertex;
            } else if (break_score[vertex] < best_break ||
                       (break_score[vertex] == best_break && (generator() & 1))) {
                best_break = break_score[vertex];
                remove = vertex;
            }
        }
        erase_vertex(remove);

        if (restart_interval > 0 && step > 0 && step % restart_interval == 0) reset();
    }

    cerr << "NOT FOUND best=" << best << " iterations=" << iterations
         << " seed=" << seed << '\n';
    return 1;
}
