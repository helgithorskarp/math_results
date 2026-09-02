# Exact 8-color cycle orders form the semigroup `<27,53>`

This directory gives an exact computer-assisted classification of the cycle
orders admitting an 8-color packing total coloring.  For every `n >= 14`,

```text
chi''_rho(C_n) <= 8  if and only if  n = 27*a + 53*b
                                      for integers a,b >= 0.
```

The lower bound `chi''_rho(C_n) >= 8` is also certified here, so the value is
exactly 8 on these orders.  In particular, `C_53` is the first 8-colorable order after
the previously published `C_27`; the largest order not admitting 8 colors is
1351; and every `C_n` with `n >= 1352` has packing total chromatic number 8.

The result refines the finite exact table for `C_14,...,C_26` in
`packing_total_cycles_c14_c26/` and directly answers the divisibility question
posed by Jasmina Ferme and Daša Mesarič Štesl, *On packing total coloring*,
arXiv:2508.08691v2 (2026), <https://arxiv.org/abs/2508.08691v2>.

## Mathematical reduction

Order `V(C_n) union E(C_n)` cyclically as

```text
v_0, e_0, v_1, e_1, ..., v_(n-1), e_(n-1).
```

The total graph is `C_(2n)^2`.  Thus a color word of length `2n` is valid
exactly when consecutive cyclic occurrences of color `i` have gap at least
`2*i+1`.

For completeness, the same transfer construction with colors `1,...,7` has
25,028 reachable states, 30,533 edges, no directed cycle, and no valid word of
length 27.  Since `T(P_14)` is the square of the 27-vertex path, `P_14` needs
at least 8 colors.  Every `C_n`, `n >= 14`, contains `P_14`, proving the lower
bound 8 without importing the primary paper's computer statement.

For colors `1,...,8`, a transfer state records the age of the last occurrence
of each color, capped at

```text
(2,4,6,8,10,12,14,16).
```

A color is available exactly when its coordinate is capped.  Appending it
resets that coordinate to zero and increments every other coordinate, with
capping.  Starting at the all-capped state enumerates every valid finite word.
For `n >= 14`, the period `2n` exceeds every cap, so valid cyclic words are in
bijection with closed walks of length `2n` in this reachable transfer graph.

The exact enumeration has 339,203 reachable states and 437,094 directed
edges.  Iterative SCC decomposition finds exactly one cyclic component, with
424 states and 468 edges.  Exhaustive simple-cycle enumeration at the unique
least state of each cycle gives:

```text
length     number of simple directed cycles
54          8
106        64
107       312
108       256
```

There are no other simple cycle lengths.  Every closed walk decomposes into
simple directed cycles, so every closed-walk length lies in
`<54,106,107,108> = <54,106,107>`.  Conversely, explicit cycles of lengths
54, 106, and 107 pass through a common transfer state; concatenating them
realizes every member of `<54,106,107>`.

If the closed-walk length is even, the number of length-107 summands is even.
Using `108=2*54` and `2*107=2*54+106`, division by two gives exactly

```text
n in <27,53>.
```

Finally, `gcd(27,53)=1`.  The Apéry representatives modulo 27 are
`0,53,...,26*53`, so the Frobenius number is `26*53-27=1351` and the conductor
is 1352.

## Reproduction

The production computation uses capped ages, iterative Kosaraju SCCs, and a
least-vertex simple-cycle DFS:

```bash
python3 enumerate_transfer.py --check certificate.json
```

The independent checker imports no production code.  It uses remaining
cooldowns, an explicit-stack Tarjan SCC algorithm, and separately written
cycle enumeration:

```bash
python3 verify_independent.py
python3 test_boundary.py
```

Expected output ends with:

```text
verified production certificate: certificate.json
independently verified: 7 colors stop at length 26; for 8 colors, 339203 states, one 424-state recurrent core, 640 simple cycles of lengths 54/106/107/108
therefore for n >= 14 an 8-coloring exists exactly when n = 27*a + 53*b (a,b >= 0), and every n >= 1352 qualifies
all boundary, concatenation, genus, and conductor tests passed
```

The computation is deterministic and uses only exact Python integer, tuple,
set, graph, and SHA-256 operations.  No solver, floating point, randomness,
timeout, or imported dataset is involved.  It was run under CPython 3.11.2.

## Certificate and trust boundary

`certificate.json` records the 7-color maximum-length computation, both
8-color graph sizes, hashes of canonical state-edge records, SCC/core sizes,
the complete simple-cycle length histogram, the hash of all 640 canonical
cycle words, and three common-base witness cycles.

The theorem trusts CPython execution and SHA-256, the two graph enumerators,
the mathematical equivalence between cyclic words and closed walks for
`2n>16`, the completeness of SCC and simple-cycle enumeration, the elementary
decomposition of a closed walk into simple cycles, and the numerical-semigroup
argument.  The independent checker changes the state convention and SCC
algorithm, but both implementations remain Python programs on the same
hardware/runtime.

The theorem classifies the 8-colorable orders.  It does not determine whether
the remaining 663 orders `n >= 14` below the conductor require 9, 10, or 11
colors.  It makes an apparently-new claim relative to the cited primary paper,
targeted searches through 2026-09-02, and the committed Discovery Net graph;
it does not claim historical priority.
