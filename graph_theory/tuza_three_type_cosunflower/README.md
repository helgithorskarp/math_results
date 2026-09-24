# Three-neighborhood co-sunflower split graphs satisfy Tuza

For a split graph with clique `C` and independent side `I`, call a
neighborhood active if it has at least two vertices. This computer-assisted
proof establishes `tau(G)<=2nu(G)` when there are at most three active
neighborhood types and, if three occur, their pairwise unions are equal:

    S0 union S1 = S0 union S2 = S1 union S2.

Clique order, the three multiplicities, and clique vertices outside that
union are unrestricted. The complements of the neighborhoods inside the
union are pairwise disjoint; this is the co-sunflower condition. The
neighborhoods may cross. The arbitrary three-type problem remains open.

The [proof](PROOF.md) gives the all-order estimate

    2nu(G)-tau(G) >= k^2/400-k/2-1/4

for three active types with the stated condition, where `k=|C|`. This
settles all `k>=199`. A further analytic lemma handles `k>=55` when at
least three clique vertices lie outside the union. An exact integer checker
closes every remaining
parameter tuple. Cases with at most two types use the
[previous all-order theorem](../tuza_two_type_complete/README.md).
The [source notes](SOURCES.md) distinguish dependencies from context.
This is a complete author proof with exact computation, pending independent
review; it is not a formal proof-assistant certificate.

A concrete family beyond the two-type and nested cases has three disjoint
sets `P0,P1,P2` of size `t>=1`, clique `U=P0 union P1 union P2`, and types
`Si=U\Pi`, each with an arbitrary positive number of independent centers.
These neighborhoods cross. Large multiplicities can violate minimum-degree
hypotheses relative to total graph order, and here the support union is the
entire clique. The theorem applies without those restrictions.

## Reproduce

Only a C++20 compiler and standard-library Python 3 are required. Tested
with g++ 12.2.0 and Python 3.11.2 on Linux x86-64. From this directory:

```sh
mkdir -p build
g++ -std=c++20 -O3 -Wall -Wextra -Wconversion -pedantic verify.cpp -o build/verify
./build/verify > actual.txt
cmp actual.txt EXPECTED.txt
python3 audit.py ./build/verify actual.txt > actual-audit.json
cmp actual-audit.json AUDIT.json
sha256sum -c SHA256SUMS
```

The full run is deterministic and uses one CPU thread with shallow
recursion; its main memory is the process runtime. `EXPECTED.txt` is a
compact count table, not a dump of the parameter tuples. Its columns are
`ROW union_size shapes represented_tuples certified_boxes visited_boxes
analytic_tuples failures`; the final `TOTAL` omits the union-size column. `AUDIT.json`
records exact coverage and definition-level checks. Runtime and final
totals are recorded in `RUN.json`.

For a short check, `./build/verify 25` restricts the clique order to at most
25. `./build/verify --dump 7` emits every small tuple for the Python audit;
its columns are `p0 p1 p2 c d m0 m1 m2 h B Ubound`. The full report audit
expects the complete order-198 run. The supported domains are enforced by
argument validation.

The sanitizer check used:

```sh
g++ -std=c++20 -O1 -g -fsanitize=address,undefined -fno-omit-frame-pointer verify.cpp -o build/sanitize
./build/sanitize 55 > actual-sanitize.txt
```

The audit independently counts the complete domain in neighborhood-size
coordinates, compares 3,239 small tuples with rational arithmetic and every
clique cut, exhausts actual palettes for 992 tuples, and checks explicit
triangle-packing witnesses and exact triangle-cover optima on 237 graphs.
It also checks all matching
factorizations through order 198 and the rational quartic certificate.
These checks were performed by the author. The unformalized reductions,
classical clique-packing existence theorem, C++ compiler, Python runtime,
and hardware remain explicit trust boundaries. No external data, floating
point calculation, solver output, or large certificate is required.
