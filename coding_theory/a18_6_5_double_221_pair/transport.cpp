// Guarded exact template transport with partial-intersection pruning.
#include <algorithm>
#include <array>
#include <chrono>
#include <fstream>
#include <iostream>
#include <set>
#include <stdexcept>
#include <vector>
using Clock = std::chrono::steady_clock;
using Mask = unsigned int;

std::vector<int> points(Mask w) {
    std::vector<int> out;
    for (int z = 0; z < 18; ++z) if ((w >> z) & 1U) out.push_back(z);
    return out;
}

struct Transport {
    std::vector<Mask> first, second, partial;
    std::array<int, 17> mapping{};
    std::vector<int> source_free, target_free;
    std::vector<std::vector<int>> incident;
    std::set<std::vector<Mask>> answers;
    unsigned long long anchors = 0, rejected_anchors = 0, nodes = 0, leaves = 0;
    unsigned long long case_nodes = 0;
    Clock::time_point started;

    bool valid(Mask word) const {
        for (Mask fixed : first) if (__builtin_popcount(word & fixed) > 2) return false;
        return true;
    }

    void visit(int depth, unsigned int used) {
        ++nodes; ++case_nodes;
        if (case_nodes > 200000ULL || ((case_nodes & 255ULL) == 0 &&
            std::chrono::duration<double>(Clock::now() - started).count() > 10.0))
            throw std::runtime_error("INCOMPLETE transport node/time guard");
        if (depth == static_cast<int>(source_free.size())) {
            ++leaves;
            std::vector<Mask> star;
            for (Mask word : second) {
                Mask image = 1U;
                for (int z : points(word)) image |= 1U << mapping[z];
                star.push_back(image);
            }
            std::sort(star.begin(), star.end());
            answers.insert(star);
            if (answers.size() > 100000U) throw std::runtime_error("INCOMPLETE output guard");
            return;
        }
        int source = source_free[depth];
        for (int j = 0; j < static_cast<int>(target_free.size()); ++j) {
            if ((used >> j) & 1U) continue;
            Mask bit = 1U << target_free[j];
            bool good = true;
            for (int row : incident[source]) if (!valid(partial[row] | bit)) { good = false; break; }
            if (!good) continue;
            mapping[source] = target_free[j];
            for (int row : incident[source]) partial[row] |= bit;
            visit(depth + 1, used | (1U << j));
            for (int row : incident[source]) partial[row] ^= bit;
        }
    }

    void run(const std::vector<Mask>& f, const std::vector<Mask>& s) {
        for (Mask w : f) first.push_back(w | (1U << 17));
        second = s;
        mapping.fill(-1); mapping[0] = 17;
        std::vector<std::vector<int>> ft, st;
        Mask fcovered = 0, scovered = 0;
        for (Mask w : f) if (w & 1U) { ft.push_back(points(w ^ 1U)); fcovered |= w ^ 1U; }
        for (Mask w : s) if (w & 1U) { st.push_back(points(w ^ 1U)); scovered |= w ^ 1U; }
        std::sort(ft.begin(), ft.end()); std::sort(st.begin(), st.end());
        if (ft.size() != 3 || st.size() != 3 || __builtin_popcount(fcovered) != 9 || __builtin_popcount(scovered) != 9)
            throw std::runtime_error("invalid common-triple input");
        for (int z = 1; z < 17; ++z) {
            if (!((scovered >> z) & 1U)) source_free.push_back(z);
            if (!((fcovered >> z) & 1U)) target_free.push_back(z);
        }
        if (source_free.size() != 7 || target_free.size() != 7) throw std::runtime_error("wrong free domain");
        incident.resize(17);
        for (int r = 0; r < static_cast<int>(s.size()); ++r) {
            if (s[r] & 1U) continue; // the three common words are already in first
            for (int z : source_free) if ((s[r] >> z) & 1U) incident[z].push_back(r);
        }
        std::array<int, 3> order{0, 1, 2};
        do {
            auto p0 = ft[order[0]];
            do {
                auto p1 = ft[order[1]];
                do {
                    auto p2 = ft[order[2]];
                    do {
                        ++anchors;
                        for (int i = 0; i < 3; ++i) {
                            mapping[st[0][i]] = p0[i]; mapping[st[1][i]] = p1[i]; mapping[st[2][i]] = p2[i];
                        }
                        partial.assign(s.size(), 1U);
                        bool good = true;
                        for (int r = 0; r < static_cast<int>(s.size()); ++r) {
                            if (s[r] & 1U) continue;
                            for (int z : points(s[r])) if ((scovered >> z) & 1U) partial[r] |= 1U << mapping[z];
                            if (!valid(partial[r])) { good = false; break; }
                        }
                        if (!good) { ++rejected_anchors; continue; }
                        case_nodes = 0; started = Clock::now();
                        visit(0, 0U);
                    } while (std::next_permutation(p2.begin(), p2.end()));
                } while (std::next_permutation(p1.begin(), p1.end()));
            } while (std::next_permutation(p0.begin(), p0.end()));
        } while (std::next_permutation(order.begin(), order.end()));
        if (anchors != 1296ULL) throw std::runtime_error("incomplete triple anchor domain");
    }
};

int main(int argc, char** argv) {
    try {
        if (argc != 3) throw std::runtime_error("usage: couple INPUT OUTPUT");
        std::ifstream input(argv[1]); std::ofstream output(argv[2]);
        if (!input || !output) throw std::runtime_error("input/output unavailable");
        int count;
        if (!(input >> count) || count != 3) throw std::runtime_error("expected three templates");
        std::vector<std::vector<Mask>> templates(3, std::vector<Mask>(20));
        for (auto& star : templates) for (Mask& word : star) {
            if (!(input >> word) || word >= (1U << 17) || __builtin_popcount(word) != 4)
                throw std::runtime_error("invalid template word");
        }
        std::string extra; if (input >> extra) throw std::runtime_error("trailing input");
        for (int f = 0; f < 3; ++f) for (int s = 0; s < 3; ++s) {
            Transport search; search.run(templates[f], templates[s]);
            output << "{\"first\":" << f << ",\"second\":" << s
                   << ",\"anchors\":" << search.anchors << ",\"rejected_anchors\":" << search.rejected_anchors
                   << ",\"nodes\":" << search.nodes << ",\"maps\":" << search.leaves << ",\"stars\":[";
            bool first = true;
            for (const auto& star : search.answers) {
                if (!first) output << ',';
                first = false;
                output << '[';
                for (std::size_t j = 0; j < star.size(); ++j) { if (j) output << ','; output << star[j]; }
                output << ']';
            }
            output << "]}\n"; output.flush();
            if (!output) throw std::runtime_error("output write failure");
            std::cout << "case " << f << ',' << s << " COMPLETE stars=" << search.answers.size()
                      << " maps=" << search.leaves << " nodes=" << search.nodes << '\n' << std::flush;
        }
        return 0;
    } catch (const std::exception& e) { std::cerr << e.what() << '\n'; return 2; }
}
