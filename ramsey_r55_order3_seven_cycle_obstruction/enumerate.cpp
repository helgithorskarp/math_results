// Direct enumeration of C3-equivariant perfect-matching covers of K7.
// Does not read CNF clauses or call a solver. Each complete-fiber rejection
// represents all 3^(15-assigned) ways to choose the remaining matching shifts.
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>

using Bits = uint32_t;  // only the low 21 bits are used
std::array<Bits, 21> blue{};
std::array<uint64_t, 8> tested{}, rejected{}, survived{};
std::array<Bits, 21> fixture{};
uint64_t represented = 0;
bool saved = false;

uint64_t power3(int exponent) {
    uint64_t answer = 1;
    while (exponent--) answer *= 3;
    return answer;
}

// Choose vertices in increasing order. Every clique is considered once;
// all recursive candidates must be adjacent to every previously chosen vertex.
bool clique(Bits candidates, int need, const std::array<Bits, 21>& graph) {
    if (need == 0) return true;
    while (__builtin_popcount(candidates) >= need) {
        int vertex = __builtin_ctz(candidates);
        candidates &= candidates - 1;
        if (clique(candidates & graph[vertex], need - 1, graph)) return true;
    }
    return false;
}

bool forbidden(int fibers) {
    int vertices = 3 * fibers;
    Bits mask = (Bits(1) << vertices) - 1;
    std::array<Bits, 21> red{};
    for (int i = 0; i < vertices; ++i)
        red[i] = (mask & ~blue[i]) & ~(Bits(1) << i);
    return clique(mask, 5, red) || clique(mask, 5, blue);
}

void matching(int left, int right, int shift, bool add) {
    for (int position = 0; position < 3; ++position) {
        int a = 3 * left + position;
        int b = 3 * right + (position + shift) % 3;
        if (add) {
            blue[a] |= Bits(1) << b;
            blue[b] |= Bits(1) << a;
        } else {
            blue[a] &= ~(Bits(1) << b);
            blue[b] &= ~(Bits(1) << a);
        }
    }
}

// Fibers 0,...,new_fiber-1 are complete; the new fiber's matching to fiber
// zero is fixed to shift zero. Assign the other matchings in increasing order.
void extend(int new_fiber, int previous) {
    if (previous < new_fiber) {
        for (int shift = 0; shift < 3; ++shift) {
            matching(previous, new_fiber, shift, true);
            extend(new_fiber, previous + 1);
            matching(previous, new_fiber, shift, false);
        }
        return;
    }
    int fibers = new_fiber + 1;
    ++tested[fibers];
    if (forbidden(fibers)) {
        ++rejected[fibers];
        int assigned = new_fiber * (new_fiber - 1) / 2;
        represented += power3(15 - assigned);
        return;
    }
    ++survived[fibers];
    if (fibers == 6 && !saved) {
        fixture = blue;
        saved = true;
    }
    if (new_fiber == 6) {
        ++represented;
        return;
    }
    matching(0, new_fiber + 1, 0, true);
    extend(new_fiber + 1, 1);
    matching(0, new_fiber + 1, 0, false);
}

int main(int argc, char** argv) {
    if (argc > 2) return 2;
    matching(0, 1, 0, true);
    extend(1, 1);
    for (int n = 2; n <= 7; ++n)
        std::cout << "fibers=" << n << " tested=" << tested[n]
                  << " rejected=" << rejected[n] << " survivors=" << survived[n] << '\n';
    std::cout << "represented=" << represented << " full_survivors=" << survived[7] << '\n';
    if (argc == 2) {
        std::ofstream output(argv[1]);
        if (!output || !saved) return 2;
        output << "18 45\n";
        for (int a = 0; a < 18; ++a)
            for (int b = a + 1; b < 18; ++b)
                if (fixture[a] & (Bits(1) << b)) output << a << ' ' << b << '\n';
        if (!output) return 2;
    }
    return represented == power3(15) && survived[7] == 0 && saved ? 0 : 1;
}
