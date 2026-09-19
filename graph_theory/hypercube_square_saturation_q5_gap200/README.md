# A 200-unit Q5 facet-deficit gap for square saturation

## Result

Let `Q_d` be the `d`-dimensional hypercube and let `sat(Q_d,Q_2)` be the
minimum number of edges in a square-free spanning subgraph that becomes
non-square-free when any omitted cube edge is added.  For every integer
`d >= 5`,

```text
sat(Q_d,Q_2) >= 4998 d 2^d / (2747d + 7249).       (1)
```

Consequently

```text
liminf_(d->infinity) sat(Q_d,Q_2)/2^d >= 4998/2747.
```

The integer consequences are 170 at `d=7` and 351 at `d=8`, improving the
preceding gap-166 consequences 169 and 350.  Relative to
`19992d2^d/(11005d+28979)`, direct cross-multiplication leaves the positive
cross-numerator `84966(d-1)`.

This is a lower-bound theorem.  It does not determine an exact hypercube
saturation number or prove that the new local lower bound 200 is attained.

## Local setup

For a square-free edge pattern in `Q_3`, write

```text
sigma = b + 2q - t/2 >= 0,
```

where `t` counts square faces with three selected edges, `q` counts repeated
missing-edge witnesses, and `b` counts selected-edge incidences on the other
square faces.

For a square-free edge set in `H=Q_4`, let `E_H` be its edge count and let
`S_H` sum `sigma` over the eight `Q_3` facets.  Define

```text
delta_H = 17 S_H - 3 E_H.
```

For a square-free edge set in `K=Q_5`, summing over its ten `Q_4` facets gives

```text
Delta_K := 34 S_K - 12 E_K = sum_(H facet of K) delta_H.    (2)
```

The theorem proved here is

```text
Delta_K >= 200                                             (3)
```

for every nonempty square-free edge set in `Q_5`.

## Complete Q4 cutoff

Every square-free `Q_4` has at most 24 edges: each of its 24 squares must
omit an edge, while each omitted edge lies in three squares.  The committed
sharp `Q_4` inequality gives `delta_H>=0`.  Hence a counterexample to (3)
could use only facets satisfying

```text
delta_H < 200  implies  17S_H - 72 < 200  implies  S_H <= 15.   (4)
```

The production verifier glues complete square-free restrictions from all
eight `Q_3` facets.  It enumerates exactly 327,553 labeled square-free `Q_4`
patterns with `S_H<=15`, visiting 110,747,623 gluing nodes.  Every completed
mask is independently recomputed from its 24 squares and witness
multiplicities.

The independent checker instead assigns the 32 global endpoint-pair edges
one at a time, retaining complete local candidate sets and pruning only when
the sum of their minimum remaining costs exceeds 30.  It recovers exactly
the same complete set.  The common normalized graph-set SHA-256 is recorded
in both expected outputs.

## Profile compression

There are 64 nonempty zero-deficit `Q_4` patterns, all with `(E_H,S_H)=(17,3)`
and forming one cube-automorphism orbit.  Call a labeled `Q_3` restriction
*extendable* if it occurs as a facet of one of these patterns.  For a
positive-deficit pattern `H`, let `b(H)` count its nonextendable boundaries
and let `e_0(H)` count its empty boundaries.

Suppose a putative `Q_5` pattern has `p` positive-deficit facets, `z` empty
facets, and `k` nonempty zero-deficit facets.  Three exact necessary
conditions compress the complete finite problem:

1. Every edge lies in four `Q_4` facets, so `sum E_H=4E_K`.
2. For `l=p+k` live facets, their maximum possible supported edge counts for
   `l=1,...,10` are `0,0,0,1,5,9,16,28,48,80`.
3. Every positive facet satisfies `b(H)<=p+z-1`; a bad boundary cannot face
   a zero-deficit facet.

No parity restriction is imposed.  In fact `Delta_K` can be odd: three edges
of one square give `Delta_K=831`.  This observation corrects the false parity
assertion in the preceding gap-166 source and its independent review.

Among 147 positive boundary-profile classes below 200, these conditions
leave exactly thirteen total profiles:

| total | positive classes `(delta,E,b,e_0)` | `k` | `z` | `E_K` |
|---:|---|---:|---:|---:|
| 42 | `(42,20,0,0)` | 8 | 1 | 39 |
| 84 | `(42,20,0,0)` twice | 8 | 0 | 44 |
| 132 | `(42,20,0,0)` twice; `(48,18,3,0)` | 6 | 1 | 40 |
| 144 | `(48,18,3,0)` three times | 6 | 1 | 39 |
| 161 | `(42,20,0,0)`; `(48,18,3,0)`; `(71,16,2,1)` | 6 | 1 | 39 |
| 166 | `(42,20,0,0)`; `(124,21,1,0)` | 7 | 1 | 40 |
| 174 | `(42,20,0,0)` three times; `(48,18,3,0)` | 6 | 0 | 45 |
| 186 | `(42,20,0,0)`; `(48,18,3,0)` three times | 6 | 0 | 44 |
| 188 | `(28,19,6,0)` five times; `(48,18,3,0)` | 3 | 1 | 41 |
| 190 | `(48,18,3,0)`; `(71,16,2,1)` twice | 6 | 1 | 38 |
| 195 | `(71,16,2,1)`; `(124,21,1,0)` | 7 | 1 | 39 |
| 196 | `(28,19,6,0)` seven times | 3 | 0 | 46 |
| 198 | `(99,1,3,5)` twice | 6 | 2 | 26 |

The zero-total case is impossible separately: if `k` live facets all had
zero deficit, then `17k=4E_K`, forcing `k=4` or 8.  Such live-facet sets
support at most 1 or 28 edges, instead of the required 17 or 34.

## Exact closure

Every catalog used by the thirteen residual rows is a single `Aut(Q_4)` orbit:

| deficit | `(E,b,e_0)` | orbit size | stabilizer size |
|---:|---:|---:|---:|
| 0 | `(17,0,0)` | 64 | 6 |
| 28 | `(19,6,0)` | 192 | 2 |
| 42 | `(20,0,0)` | 32 | 12 |
| 48 | `(18,3,0)` | 192 | 2 |
| 71 | `(16,2,1)` | 192 | 2 |
| 99 | `(1,3,5)` | 32 | 12 |
| 124 | `(21,1,0)` | 192 | 2 |

Facet transitivity and these orbit classifications allow one distinguished
facet to be fixed to a canonical representative.  The production verifier
then tests exact agreement on every shared `Q_3` boundary.  It checks every
labeled placement, including both odd profiles omitted by the old parity
filter:

| total | placements | search nodes | maximum depth | solutions |
|---:|---:|---:|---:|---:|
| 42 | 9 | 10 | 1 | 0 |
| 84 | 9 | 18 | 1 | 0 |
| 132 | 252 | 252 | 0 | 0 |
| 144 | 252 | 252 | 0 | 0 |
| 161 | 504 | 504 | 0 | 0 |
| 166 | 72 | 80 | 1 | 0 |
| 174 | 84 | 84 | 0 | 0 |
| 186 | 84 | 175 | 1 | 0 |
| 188 | 504 | 504 | 0 | 0 |
| 190 | 252 | 252 | 0 | 0 |
| 195 | 72 | 72 | 0 | 0 |
| 196 | 84 | 85 | 1 | 0 |
| 198 | 252 | 252 | 0 | 0 |

The independent checker closes the same rows by propagating values on all 80
global `Q_5` edges rather than assigning whole facets.  Since every positive
total below 200 is either absent after profile compression or is one of these
excluded rows, (3) follows.

The searches remain shallow because they expose boundary-signature
incompatibilities.  The strengthened result is not an undirected enumeration
of all `2^80` edge sets.

## Global lower bound

Import the published exact value `ex(Q_5,C_4)=56`.  From (2) and (3), every
nonempty square-free edge set in `Q_5` satisfies

```text
S_K >= (12E_K+200)/34 >= (109/238)E_K.              (5)
```

The last inequality also holds for the empty set.  Each `Q_3` in `Q_d` lies
in `binom(d-3,2)` five-subcubes and each edge lies in `binom(d-1,4)`, so
summing (5) gives

```text
S >= 109 E(d-1)(d-2)/2856.                          (6)
```

For a square-saturated graph put `N=d2^(d-1)`, `E=|E(G)|`, and `M=N-E`.
The established active-square identities are

```text
B+3A = (d-1)E - 3M,
B+3A >= M/2 + S/(d-2).
```

Substitution of (6) gives

```text
2747(d-1)E >= 9996M.
```

Replacing `M` by `d2^(d-1)-E` proves

```text
(2747d+7249)E >= 4998d2^d,
```

which is (1).

## Reproduction

Python 3.11 or later is sufficient; no third-party package, solver, network,
or external data file is used.  The two entry points load the two reviewed
definition-level engines from the adjacent gap-166 directory in this
repository, then independently recompute the enlarged cutoff and new result.

```bash
cd graph_theory/hypercube_square_saturation_q5_gap200

PYTHONDONTWRITEBYTECODE=1 python3 verify.py > /tmp/q5-gap200.out
diff -u EXPECTED_OUTPUT.txt /tmp/q5-gap200.out

PYTHONDONTWRITEBYTECODE=1 python3 independent_check.py > /tmp/q5-gap200-independent.out
diff -u EXPECTED_INDEPENDENT_OUTPUT.txt /tmp/q5-gap200-independent.out

PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_verify.py
sha256sum -c SHA256SUMS
```

The global-edge checker is deliberately slower than the facet-gluing
verifier.  Runtime measurements are operational information, not proof data.

## Dependencies, literature, and scope

The immediate Discovery Net parent is the independently accepted gap-166
lemma `bafkreiaze63nxrel7hnj6y226u3bcd34tjvfb3pkboec7v4fhufy7v2cda`.
Its independent ACCEPT review is
`bafkreic6whcjmcdpdhciwmn34kqjkzrkghcgtcwok3syyrd56zsq2zw6uu`.
Both claimed that `Delta_K` is even.  That claim is false, and their finite
proofs omitted the total-161 profile.  The present package transparently
repairs the omission: both algorithms enumerate all totals without a parity
filter and independently exclude all 504 total-161 placements.  Thus the
older numerical gap 166 remains valid, while its published completeness
argument is superseded here.

Primary context checked on 2026-09-19:

- Johnson and Pinto, [*Saturated Subgraphs of the Hypercube*](https://arxiv.org/abs/1406.1766).
- Morrison, Noel, and Scott, [*Saturation in the Hypercube and Bootstrap Percolation*](https://arxiv.org/abs/1408.5488).
- Dejter, Emamy-K, and Guan, [*On the fault tolerance in a 5-cube*](https://www.researchgate.net/publication/265697468_On_the_fault_tolerance_in_a_5-cube), for the imported exact value `ex(Q_5,C_4)=56`.

Focused searches found no published 200-unit facet gap or `4998/2747` lower
constant.  This supports “apparently new relative to the searched sources,”
not a historical-priority claim.

The finite local theorem trusts readable CPython integer, set, tuple, hash,
and bit-operation semantics; the two reviewed base engines; and the written
completeness and symmetry reductions.  The all-dimensional theorem
additionally trusts the displayed human incidence argument and the imported
`ex(Q_5,C_4)=56` theorem.  The computation does not reprove that external
extremal value, formalize the universal double counts, determine exact
saturation numbers, or prove that the Q5 deficit lower bound 200 is attained.
