// Same-author independent literal enumeration: no CRT/gcd/matching cuts.
// All generated bit tables stay outside the publication directory.
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <set>
#include <stdexcept>
#include <string>
#include <vector>

using Mask = std::uint32_t;

static void require(bool condition, const std::string& message) {
    if (!condition) throw std::runtime_error(message);
}

struct Family {
    std::vector<std::vector<Mask>> masks;
    std::vector<std::size_t> positive_counts;
    std::vector<std::size_t> union_counts;
    std::set<Mask> unions;
};

static Family family(const std::vector<int>& points, const std::vector<int>& moduli) {
    Family result;
    result.unions.insert(0);
    for (int n : moduli) {
        require(n > 0 && 1680 % n == 0, "original modulus outside period");
        std::set<Mask> distinct;
        for (int a = 0; a < n; ++a) {
            Mask mask = 0;
            for (std::size_t i = 0; i < points.size(); ++i) {
                if (points[i] % n == a) mask |= Mask{1} << i;
            }
            distinct.insert(mask);
        }
        result.positive_counts.push_back(distinct.size() - distinct.count(0));
        result.masks.emplace_back(distinct.begin(), distinct.end());
        std::set<Mask> next;
        for (Mask old : result.unions) {
            for (Mask added : distinct) next.insert(old | added);
        }
        result.unions = std::move(next);
        result.union_counts.push_back(result.unions.size());
        require(result.unions.size() <= 50000, "union-family guard exceeded");
    }
    return result;
}

static bool brute_small(const Family& first, const Family& last, Mask full) {
    for (Mask a : first.unions) {
        for (Mask b : last.unions) if ((a | b) == full) return true;
    }
    return false;
}

static void print_array(const std::vector<std::size_t>& data) {
    std::cout << '[';
    for (std::size_t i = 0; i < data.size(); ++i) {
        if (i != 0) std::cout << ',';
        std::cout << data[i];
    }
    std::cout << ']';
}

static void run_case(const std::string& name, bool one_parent, bool one_point,
                     bool expected) {
    std::vector<int> points;
    for (int x = 0; x < 1680; ++x) {
        const bool parent = x % 4 == 1 || (!one_parent && x % 4 == 2);
        const bool triangle =
            (x % 3 == 0 && x % 5 == 1 && x % 7 == 0) ||
            (x % 3 == 0 && x % 5 == 0 && x % 7 == 1) ||
            (x % 3 == 1 && x % 5 == 0 && x % 7 == 0);
        if (parent && (one_point ? x % 105 == 0 : triangle)) points.push_back(x);
    }
    require(!points.empty() && points.size() <= 24, "demand-bit guard exceeded");
    const std::vector<int> first_moduli{8, 24, 40, 56};
    const std::vector<int> last_moduli{16, 48, 80, 112};
    Family first = family(points, first_moduli);
    Family last = family(points, last_moduli);
    const std::size_t states = std::size_t{1} << points.size();
    const Mask full = (Mask{1} << points.size()) - 1;
    // zeta[q]=1 exactly when some complete last-layer tuple covers q.
    std::vector<std::uint8_t> zeta(states, 0);
    for (Mask mask : last.unions) zeta[mask] = 1;
    for (std::size_t bit = 0; bit < points.size(); ++bit) {
        const std::size_t step = std::size_t{1} << bit;
        for (std::size_t block = 0; block < states; block += 2 * step) {
            for (std::size_t j = 0; j < step; ++j) {
                zeta[block + j] |= zeta[block + j + step];
            }
        }
    }
    std::size_t successful_first_unions = 0;
    for (Mask mask : first.unions) successful_first_unions += zeta[full ^ mask];
    const bool exists = successful_first_unions != 0;
    require(exists == expected, "unexpected full-tuple result");
    if (points.size() <= 12) {
        require(brute_small(first, last, full) == exists, "small superset lookup mismatch");
        // Entry-level check of every lookup against literal final unions.
        for (std::size_t q = 0; q < states; ++q) {
            bool contains = false;
            for (Mask b : last.unions) {
                if ((b & static_cast<Mask>(q)) == q) { contains = true; break; }
            }
            require((zeta[q] != 0) == contains, "superset table control mismatch");
        }
    }
    std::cout << "{\"case\":\"" << name << "\",\"points\":" << points.size()
              << ",\"raw_phases\":384,\"first_phase_masks\":";
    print_array(first.positive_counts);
    std::cout << ",\"last_phase_masks\":";
    print_array(last.positive_counts);
    std::cout << ",\"first_union_counts\":";
    print_array(first.union_counts);
    std::cout << ",\"last_union_counts\":";
    print_array(last.union_counts);
    std::cout << ",\"superset_states\":" << states
              << ",\"successful_first_unions\":" << successful_first_unions
              << ",\"integer_completion\":" << (exists ? "true" : "false") << '}';
}

int main() {
    try {
        std::cout << "[";
        run_case("two-parent-triangle", false, false, false);
        std::cout << ',';
        run_case("one-parent-triangle", true, false, true);
        std::cout << ',';
        run_case("two-parent-singleton", false, true, true);
        std::cout << "]\n";
        return 0;
    } catch (const std::exception& exc) {
        std::cerr << "incomplete/failed: " << exc.what() << '\n';
        return 1;
    }
}
