#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

using namespace std;

struct Writer {
    fstream out;
    long long clauses = 0;
    int variables = 0;

    explicit Writer(const string& path) : out(path, ios::in | ios::out | ios::trunc) {
        if (!out) throw runtime_error("cannot open output");
        out << "p cnf " << setw(10) << setfill('0') << 0 << " "
            << setw(10) << 0 << "\n" << setfill(' ');
    }
    int fresh() { return ++variables; }
    void clause(initializer_list<int> values) {
        for (int x : values) out << x << ' ';
        out << "0\n";
        ++clauses;
    }
    void clause(const vector<int>& values) {
        for (int x : values) out << x << ' ';
        out << "0\n";
        ++clauses;
    }
    void finish() {
        out.seekp(0);
        out << "p cnf " << setw(10) << setfill('0') << variables << " "
            << setw(10) << clauses << "\n";
        out.close();
    }
};

// Sinz sequential encoding of sum_i [literal xs[i] is true] <= k.
// Auxiliary s[i][j] records the forward implication that the first i+1
// literals contain at least j+1 true literals.  Equivalence is unnecessary:
// the clauses are satisfiable in the auxiliaries iff the cardinality bound is.
static void at_most(Writer& w, const vector<int>& xs, int k) {
    const int n = static_cast<int>(xs.size());
    assert(0 <= k && k <= n);
    if (k == n) return;
    if (k == 0) {
        for (int x : xs) w.clause({-x});
        return;
    }
    vector<vector<int>> s(n-1, vector<int>(k));
    for (auto& row : s) for (int& v : row) v = w.fresh();
    for (int i = 0; i < n-1; ++i) w.clause({-xs[i], s[i][0]});
    for (int i = 1; i < n-1; ++i) w.clause({-s[i-1][0], s[i][0]});
    for (int i = 1; i < n-1; ++i) {
        for (int j = 1; j < k; ++j) {
            w.clause({-xs[i], -s[i-1][j-1], s[i][j]});
            w.clause({-s[i-1][j], s[i][j]});
        }
    }
    for (int i = 1; i < n; ++i) w.clause({-xs[i], -s[i-1][k-1]});
}

int main(int argc, char** argv) {
    if (argc != 2 && argc != 3) {
        cerr << "usage: " << argv[0] << " OUTPUT.cnf [EXACT_EH]\n";
        return 2;
    }
    int exact_eh = -1;
    if (argc == 3) {
        exact_eh = stoi(argv[2]);
        if (exact_eh < 110 || exact_eh > 114) {
            cerr << "EXACT_EH must lie in 110..114\n";
            return 2;
        }
    }
    Writer w(argv[1]);
    array<array<int,44>,44> edge{};
    for (int j = 1; j < 44; ++j)
        for (int i = 0; i < j; ++i)
            edge[i][j] = edge[j][i] = w.fresh();
    assert(w.variables == 946);

    // Every five nonroot vertices contain both an edge and a nonedge.
    for (int a = 0; a < 40; ++a)
    for (int b = a+1; b < 41; ++b)
    for (int c = b+1; c < 42; ++c)
    for (int d = c+1; d < 43; ++d)
    for (int e = d+1; e < 44; ++e) {
        array<int,5> v{a,b,c,d,e};
        vector<int> no_k5, no_i5;
        for (int j = 1; j < 5; ++j) for (int i = 0; i < j; ++i) {
            no_k5.push_back(-edge[v[i]][v[j]]);
            no_i5.push_back(edge[v[i]][v[j]]);
        }
        w.clause(no_k5);
        w.clause(no_i5);
    }

    // The fixed root is adjacent to H={0,...,21} and to no X={22,...,43}.
    // Hence H has no K4 and X has no independent four-set.
    for (int a = 0; a < 19; ++a)
    for (int b = a+1; b < 20; ++b)
    for (int c = b+1; c < 21; ++c)
    for (int d = c+1; d < 22; ++d) {
        array<int,4> v{a,b,c,d};
        vector<int> clause;
        for (int j = 1; j < 4; ++j) for (int i = 0; i < j; ++i)
            clause.push_back(-edge[v[i]][v[j]]);
        w.clause(clause);
    }
    for (int a = 22; a < 41; ++a)
    for (int b = a+1; b < 42; ++b)
    for (int c = b+1; c < 43; ++c)
    for (int d = c+1; d < 44; ++d) {
        array<int,4> v{a,b,c,d};
        vector<int> clause;
        for (int j = 1; j < 4; ++j) for (int i = 0; i < j; ++i)
            clause.push_back(edge[v[i]][v[j]]);
        w.clause(clause);
    }

    vector<int> h_success, paired_success;
    for (int j = 1; j < 22; ++j) for (int i = 0; i < j; ++i) {
        h_success.push_back(edge[i][j]);
        paired_success.push_back(edge[i][j]);
    }
    for (int j = 23; j < 44; ++j) for (int i = 22; i < j; ++i)
        paired_success.push_back(-edge[i][j]); // a Q-edge is a Y-nonedge
    assert(h_success.size() == 231 && paired_success.size() == 462);

    vector<int> h_fail, paired_fail;
    transform(h_success.begin(), h_success.end(), back_inserter(h_fail), [](int x){return -x;});
    transform(paired_success.begin(), paired_success.end(), back_inserter(paired_fail), [](int x){return -x;});
    at_most(w, h_fail, 231-(exact_eh < 0 ? 110 : exact_eh));
    if (exact_eh >= 0) at_most(w, h_success, exact_eh);
    at_most(w, paired_fail, 462-220);  // e(H)+e(Q) >= 220

    const int original = 946;
    const int auxiliaries = w.variables-original;
    const long long clauses = w.clauses;
    w.finish();
    cerr << "original_variables " << original << "\n"
         << "auxiliary_variables " << auxiliaries << "\n"
         << "variables " << original+auxiliaries << "\n"
         << "clauses " << clauses << "\n"
         << "exact_eH " << exact_eh << "\n";
}
