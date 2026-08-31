#include <algorithm>
#include <array>
#include <bitset>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <random>
#include <string>
#include <vector>

using namespace std;

static constexpr int DIMENSION = 7;
static constexpr int VERTEX_COUNT = 1 << DIMENSION;

vector<int> ball(int vertex) {
    vector<int> result{vertex};
    for (int coordinate = 0; coordinate < DIMENSION; ++coordinate)
        result.push_back(vertex ^ (1 << coordinate));
    sort(result.begin(), result.end());
    return result;
}

int main(int argc, char** argv) {
    const int target = argc > 1 ? stoi(argv[1]) : 30;
    const uint64_t iterations = argc > 2 ? stoull(argv[2]) : 100000ULL;
    const uint64_t seed = argc > 3 ? stoull(argv[3]) : 1;
    mt19937_64 generator(seed);

    array<vector<int>, VERTEX_COUNT> balls;
    for (int vertex = 0; vertex < VERTEX_COUNT; ++vertex)
        balls[vertex] = ball(vertex);

    // Location-domination is a hitting-set problem.  The domination clause
    // for v is N[v].  The separation clause for u,v is
    // {u,v} union (N[u] symmetric_difference N[v]).
    vector<vector<int>> clauses;
    for (int vertex = 0; vertex < VERTEX_COUNT; ++vertex)
        clauses.push_back(balls[vertex]);
    for (int first = 0; first < VERTEX_COUNT; ++first) {
        for (int second = first + 1; second < VERTEX_COUNT; ++second) {
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
    vector<vector<int>> incident(VERTEX_COUNT);
    for (int clause = 0; clause < static_cast<int>(clauses.size()); ++clause)
        for (int vertex : clauses[clause]) incident[vertex].push_back(clause);

    vector<char> chosen(VERTEX_COUNT);
    vector<int> cover(clauses.size());
    vector<int> break_score(VERTEX_COUNT);
    vector<int> uncovered;
    vector<int> uncovered_position(clauses.size(), -1);

    auto add_uncovered = [&](int clause) {
        if (uncovered_position[clause] >= 0) return;
        uncovered_position[clause] = static_cast<int>(uncovered.size());
        uncovered.push_back(clause);
    };
    auto remove_uncovered = [&](int clause) {
        int position = uncovered_position[clause];
        if (position < 0) return;
        int moved = uncovered.back();
        uncovered[position] = moved;
        uncovered_position[moved] = position;
        uncovered.pop_back();
        uncovered_position[clause] = -1;
    };
    auto sole_chosen = [&](int clause, int except) {
        for (int vertex : clauses[clause])
            if (vertex != except && chosen[vertex]) return vertex;
        return -1;
    };
    auto insert = [&](int vertex) {
        chosen[vertex] = true;
        break_score[vertex] = 0;
        for (int clause : incident[vertex]) {
            if (cover[clause] == 0) {
                remove_uncovered(clause);
                ++break_score[vertex];
            } else if (cover[clause] == 1) {
                int old = sole_chosen(clause, vertex);
                if (old >= 0) --break_score[old];
            }
            ++cover[clause];
        }
    };
    auto erase = [&](int vertex) {
        for (int clause : incident[vertex]) {
            if (cover[clause] == 1) {
                add_uncovered(clause);
                --break_score[vertex];
            } else if (cover[clause] == 2) {
                int remaining = sole_chosen(clause, vertex);
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
        uncovered.clear();
        fill(uncovered_position.begin(), uncovered_position.end(), -1);
        for (int clause = 0; clause < static_cast<int>(clauses.size()); ++clause)
            add_uncovered(clause);
        vector<int> order(VERTEX_COUNT);
        iota(order.begin(), order.end(), 0);
        shuffle(order.begin(), order.end(), generator);
        for (int index = 0; index < target; ++index) insert(order[index]);
    };

    reset();
    size_t best = uncovered.size();
    for (uint64_t step = 0; step < iterations; ++step) {
        if (uncovered.empty()) {
            cerr << "FOUND step=" << step << " seed=" << seed << '\n';
            for (int vertex = 0; vertex < VERTEX_COUNT; ++vertex)
                if (chosen[vertex]) cout << bitset<DIMENSION>(vertex) << ' ';
            cout << '\n';
            return 0;
        }
        if (uncovered.size() < best) {
            best = uncovered.size();
            cerr << "best=" << best << " step=" << step << " seed=" << seed << '\n';
        }

        int clause = uncovered[generator() % uncovered.size()];
        int add = -1;
        int best_gain = -1;
        bool random_add = (generator() % 100) < 3;
        for (int vertex : clauses[clause]) {
            if (chosen[vertex]) continue;
            int gain = 0;
            for (int other_clause : incident[vertex])
                gain += (cover[other_clause] == 0);
            if (random_add) {
                if (add < 0 || (generator() & 1)) add = vertex;
            } else if (gain > best_gain ||
                       (gain == best_gain && (generator() & 1))) {
                best_gain = gain;
                add = vertex;
            }
        }
        if (add < 0) {
            reset();
            continue;
        }
        insert(add);

        int remove = -1;
        int best_break = 1 << 30;
        bool random_remove = (generator() % 100) < 5;
        for (int vertex = 0; vertex < VERTEX_COUNT; ++vertex) {
            if (!chosen[vertex] || vertex == add) continue;
            if (random_remove) {
                if (remove < 0 || (generator() & 1)) remove = vertex;
            } else if (break_score[vertex] < best_break ||
                       (break_score[vertex] == best_break && (generator() & 1))) {
                best_break = break_score[vertex];
                remove = vertex;
            }
        }
        erase(remove);
        if (step > 0 && step % 1000000ULL == 0) reset();
    }

    cerr << "NOT FOUND best=" << best << " iterations=" << iterations
         << " seed=" << seed << '\n';
    return 1;
}
