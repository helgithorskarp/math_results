# An exact distance sieve for the retained rank-five full graphs

This sieve removes **66.039853207352%** of the full 43-vertex graphs remaining
after the preceding rank-five cross-matrix sieve. It uses the established
requirement that every vertex pair in a good43 has at least eight outside
distinguishers. For two vertices with identical cross rows, all distinguishers
lie on the 20-side, so this requirement constrains previously free internal
edges.

The baseline is exactly the final family of
[the rank-five global sieve](../ramsey_r55_rank5_global_sieve/README.md): red
cut rank five, blue cut rank at least five, no simultaneous zero row/column,
zero multiplicities at most one and two, row multiplicities at most three,
column multiplicities at most five, and initially all 443 internal pairs
arbitrary. Every retained support and multiplicity pattern is included.

In each repeated row class, select its two least vertex labels. Test the
selected pair from **every** repeated class, up to ten disjoint pairs. This
selection depends only on the cross matrix. Requiring their distances to
be at least eight is a necessary condition for every good43. All cross
patterns still have some passing internal assignments; the reduction is
in full physical graphs, not a new cross-matrix exclusion.

The exact removed fraction of this baseline is

    1517091095331032698679481616877708410552466083285461950806157462568877
    /2297235716996034245519255084139001954450484691718363332622207013617664.

The baseline contains

    3199411086594883698497480332351669598105158486523919360000 * 2^443

full labeled graphs on the fixed 20+23 partition. Complete integer counts
are in [EXACT_COUNTS.md](EXACT_COUNTS.md). This percentage starts after the
previous 39.2414% cross sieve and does not reuse its earlier denominator.
No fraction of actual good graphs, isomorphism classes or search runtime is
asserted. No good43, whole-family exclusion or improved Ramsey bound results.

The selected pair tests are dependent: two share a four-edge block. A signed
graph expansion and a separate positive block-count recurrence agree for
every possible number of selected pairs. Histogram states make the complete
calculation small: at ten pairs the two methods use 1,024 and 10,946 states,
respectively. No independence approximation, solver or Monte Carlo estimate
is used.

## Reproduce and inspect a physical graph

CPython 3.11.2, standard library, exact integers:

    python3 -B reproduce.py
    python3 -B -O reproduce.py
    python3 -B counts.py
    python3 -B distance.py
    python3 -B model.py fixture_parameters.json
    python3 -B extract.py fixture_parameters.json
    python3 -B verify.py fixture_graph.json fixture_certificate.json

The full replay returns `VERIFIED_RANK5_DISTANCE_SIEVE` and the deterministic
audit hash. It regenerates both counts and physical evidence. The fixture
is a deliberately rejected interface control, not a candidate. A passing
classification means only that these necessary filters hold.

See [PROOF.md](PROOF.md), [VALIDATION.md](VALIDATION.md), and
[provenance.json](provenance.json). No private artifact, historical graph
catalog, solver, large proof or network is required for reproduction.
Physical construction remains with the teammate's lane; this contribution
supplies global counted discrimination without selecting occupancy templates
or modifying saved graphs.
