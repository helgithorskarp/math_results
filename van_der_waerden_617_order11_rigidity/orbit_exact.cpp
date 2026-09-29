// Exact, bounded exhaustive checker for punctured F_617 orbit colorings.
// Independent of the SAT exploration. No solver or external library is used.
#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <limits>
#include <random>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

using Mask = std::uint64_t;
using Clock = std::chrono::steady_clock;
constexpr int P = 617;

void require(bool condition, const std::string &message) {
    if (!condition) throw std::runtime_error(message);
}

int weight(Mask x) { return __builtin_popcountll(x); }

struct BudgetExceeded {
    std::string status;
};

struct Answer {
    bool satisfiable = false;
    Mask assigned = 0;
    Mask ones = 0;
};

struct Search {
    std::uint64_t limit;
    double seconds;
    Clock::time_point start = Clock::now();
    std::uint64_t nodes = 0, conflicts = 0, propagations = 0;

    Answer run(const std::vector<Mask> &edges, Mask assigned, Mask ones) {
        ++nodes;
        if (nodes > limit) throw BudgetExceeded{"INCOMPLETE_NODE_BUDGET"};
        if (std::chrono::duration<double>(Clock::now()-start).count() > seconds)
            throw BudgetExceeded{"INCOMPLETE_TIME_BUDGET"};
        require((ones & ~assigned) == 0, "invalid partial assignment");
        std::vector<Mask> active(edges);
        for (;;) {
            std::vector<Mask> todo;
            todo.reserve(active.size());
            Mask force_zero = 0, force_one = 0;
            const Mask zeros = assigned ^ ones;
            for (Mask edge : active) {
                const bool has_one = (edge & ones) != 0;
                const bool has_zero = (edge & zeros) != 0;
                if (has_one && has_zero) continue;
                const Mask free = edge & ~assigned;
                if (free == 0) { ++conflicts; return {}; }
                if ((free & (free-1)) == 0) {
                    // An unassigned singleton can never be non-monochromatic.
                    if (!(has_one || has_zero)) { ++conflicts; return {}; }
                    if (has_one) force_zero |= free;
                    else force_one |= free;
                } else todo.push_back(edge);
            }
            if ((force_zero & force_one) != 0) { ++conflicts; return {}; }
            active = std::move(todo);
            if ((force_zero | force_one) == 0) break;
            assigned |= force_zero | force_one;
            ones |= force_one;
            propagations += static_cast<std::uint64_t>(weight(force_zero | force_one));
        }
        if (active.empty()) return {true,assigned,ones};
        int shortest = 65;
        for (Mask edge : active) shortest = std::min(shortest,weight(edge & ~assigned));
        std::array<std::uint64_t,64> frequencies{};
        for (Mask edge : active) {
            Mask free = edge & ~assigned;
            if (weight(free) != shortest) continue;
            while (free != 0) {
                const unsigned index = static_cast<unsigned>(__builtin_ctzll(free));
                ++frequencies[index];
                free &= free-1;
            }
        }
        unsigned choice = 0;
        for (unsigned i=1; i<64; ++i)
            if (frequencies[i] > frequencies[choice]) choice = i;
        require(frequencies[choice] > 0, "missing branching variable");
        const Mask variable = Mask{1} << choice;
        Answer answer = run(active,assigned | variable,ones);
        if (answer.satisfiable) return answer;
        return run(active,assigned | variable,ones | variable);
    }
};

std::vector<Mask> direct_edges(int m) {
    require(m > 0 && m <= 62 && 616 % m == 0, "index must divide 616 and be at most 62");
    // Enumerate all powers of the primitive root: no scaling reduction is used.
    std::array<int,P> ids;
    ids.fill(-1);
    ids[0] = m;
    int x = 1;
    for (int exponent=0; exponent<616; ++exponent) {
        require(ids[static_cast<std::size_t>(x)] == -1, "3 has repeated power before 616");
        ids[static_cast<std::size_t>(x)] = exponent % m;
        x = x * 3 % P;
    }
    require(x == 1, "power cycle did not close");
    require(std::all_of(ids.begin(),ids.end(),[](int v){return v >= 0;}), "missing field element");
    std::vector<Mask> edges;
    edges.reserve(static_cast<std::size_t>(P*(P-1)));
    for (int d=1; d<P; ++d) for (int a=0; a<P; ++a) {
        Mask mask = 0;
        for (int j=0; j<7; ++j)
            mask |= Mask{1} << ids[static_cast<std::size_t>((a+j*d)%P)];
        edges.push_back(mask);
    }
    std::sort(edges.begin(),edges.end());
    edges.erase(std::unique(edges.begin(),edges.end()),edges.end());
    return edges;
}

bool brute(const std::vector<Mask> &edges, unsigned n, Mask assigned, Mask ones) {
    for (Mask colors=0; colors<(Mask{1}<<n); ++colors) {
        if ((colors & assigned) != ones) continue;
        bool valid = true;
        for (Mask edge : edges)
            if ((edge & colors) == 0 || (edge & ~colors) == 0) { valid=false; break; }
        if (valid) return true;
    }
    return false;
}

void self_test() {
    std::mt19937_64 rng(617);
    unsigned checked = 0;
    for (unsigned n=1; n<=10; ++n) for (unsigned trial=0; trial<100; ++trial) {
        const Mask all = (Mask{1}<<n)-1;
        std::vector<Mask> edges;
        for (unsigned k=0; k<2*n; ++k) edges.push_back(1+rng()%all);
        const Mask assigned = rng() & all;
        const Mask ones = rng() & assigned;
        const bool expected = brute(edges,n,assigned,ones);
        Search search{1000000,60.0};
        const Answer actual = search.run(edges,assigned,ones);
        require(actual.satisfiable == expected, "brute-force disagreement");
        if (actual.satisfiable) {
            require((actual.assigned & assigned) == assigned, "lost assigned variables");
            require((actual.ones & assigned) == ones, "changed assigned color");
            for (Mask edge : edges)
                require((edge & actual.ones) != 0 && (edge & (actual.assigned ^ actual.ones)) != 0,
                        "returned partial coloring has an unsatisfied edge");
        }
        ++checked;
    }
    auto full = direct_edges(8);
    std::vector<Mask> nz;
    for (Mask edge : full) if ((edge & (Mask{1}<<8)) == 0) nz.push_back(edge);
    std::vector<Mask> survivors;
    for (Mask colors=0; colors<256; ++colors)
        if (std::all_of(nz.begin(),nz.end(),[colors](Mask edge){
            return (edge & colors) != 0 && (edge & ~colors) != 0;
        })) survivors.push_back(colors);
    require(survivors == std::vector<Mask>{85,170}, "unexpected index-eight words");
    std::cout << "{\"status\":\"SELF_TEST_PASSED\",\"random_brute_force_comparisons\":"
              << checked << ",\"index_eight_words_checked\":256,\"surviving_masks\":[85,170]}\n";
}

int main(int argc, char **argv) {
    try {
        int m=56, first=1, last=-1;
        std::uint64_t limit=1000000;
        double seconds=120;
        std::string dump;
        for (int i=1; i<argc; ++i) {
            const std::string arg(argv[i]);
            if (arg == "--self-test") { self_test(); return 0; }
            require(i+1 < argc, "option lacks a value");
            const std::string value(argv[++i]);
            if (arg == "--m") m=std::stoi(value);
            else if (arg == "--first") first=std::stoi(value);
            else if (arg == "--last") last=std::stoi(value);
            else if (arg == "--nodes") limit=std::stoull(value);
            else if (arg == "--seconds") seconds=std::stod(value);
            else if (arg == "--dump") dump=value;
            else throw std::runtime_error("unknown option: "+arg);
        }
        require(m%2 == 0, "first-deviation partition in this checker requires even index");
        require(limit > 0 && seconds > 0, "budgets must be positive");
        if (last == -1) last=m-1;
        require(1 <= first && first <= last && last < m, "invalid first-deviation range");
        const auto began = Clock::now();
        const auto full = direct_edges(m);
        if (!dump.empty()) {
            std::ofstream out(dump);
            require(out.good(), "cannot open edge-mask dump");
            for (Mask edge : full) out << edge << '\n';
            require(out.good(), "cannot write edge-mask dump");
        }
        std::vector<Mask> nz;
        for (Mask edge : full) if ((edge & (Mask{1}<<m)) == 0) nz.push_back(edge);
        Mask alternating = 0;
        for (int v=1; v<m; v+=2) alternating |= Mask{1} << v;
        for (Mask edge : nz)
            require((edge & alternating) != 0 && (edge & ~alternating) != 0,
                    "alternating word does not satisfy punctured constraints");
        std::cout << "{\"status\":\"CONSTRAINTS_READY\",\"m\":" << m
                  << ",\"full_edges\":" << full.size() << ",\"nonzero_edges\":" << nz.size()
                  << ",\"first\":" << first << ",\"last\":" << last << "}\n" << std::flush;
        Search search{limit,seconds};
        int current = first;
        try {
            for (; current<=last; ++current) {
                const Mask assigned = (Mask{1}<<(current+1))-1;
                Mask ones = alternating & ((Mask{1}<<current)-1);
                if (current%2 == 0) ones |= Mask{1}<<current;
                const auto before = search.nodes;
                const Answer answer = search.run(nz,assigned,ones);
                std::cout << "{\"status\":\"" << (answer.satisfiable ? "SAT" : "UNSAT")
                          << "\",\"first_deviation\":" << current
                          << ",\"nodes\":" << search.nodes-before;
                if (answer.satisfiable)
                    std::cout << ",\"assigned\":" << answer.assigned << ",\"ones\":" << answer.ones;
                std::cout << "}\n" << std::flush;
                if (answer.satisfiable) return 1;
            }
        } catch (const BudgetExceeded &e) {
            std::cout << "{\"status\":\"" << e.status << "\",\"m\":" << m
                      << ",\"unfinished_first_deviation\":" << current
                      << ",\"nodes\":" << search.nodes << ",\"conflicts\":" << search.conflicts
                      << ",\"seconds\":" << std::chrono::duration<double>(Clock::now()-began).count()
                      << "}\n" << std::flush;
            return 2;
        }
        std::cout << "{\"status\":\""
                  << (first==1 && last==m-1 ? "RIGIDITY_CERTIFIED" : "CASE_RANGE_CERTIFIED")
                  << "\",\"m\":" << m << ",\"first\":" << first << ",\"last\":" << last
                  << ",\"nodes\":" << search.nodes << ",\"conflicts\":" << search.conflicts
                  << ",\"propagations\":" << search.propagations << ",\"seconds\":"
                  << std::chrono::duration<double>(Clock::now()-began).count() << "}\n";
        return 0;
    } catch (const std::exception &e) {
        std::cerr << "ERROR: " << e.what() << '\n';
        return 3;
    }
}
