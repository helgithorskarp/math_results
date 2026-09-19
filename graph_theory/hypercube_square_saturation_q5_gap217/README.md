# A 217-unit Q5 facet-deficit gap for square saturation

## Result

Let `Q_d` be the `d`-dimensional hypercube and let `sat(Q_d,Q_2)` be the
minimum number of edges in a square-free spanning subgraph that becomes
non-square-free when any omitted cube edge is added.  For every integer
`d >= 5`,

```text
sat(Q_d,Q_2) >= 5712 d 2^d / (3137d + 8287).       (1)
```

Consequently

```text
liminf_(d->infinity) sat(Q_d,Q_2)/2^d >= 5712/3137.
```

Relative to the preceding gap-200 bound
`4998d2^d/(2747d+7249)`, direct cross-multiplication leaves the positive
cross-numerator `12138(d-1)`.  The integer consequences at `d=7,8` remain
170 and 351; the first integer improvement is at `d=11`, from 3006 to 3007.

This is a lower-bound theorem.  It does not determine an exact hypercube
saturation number or prove that the new local lower bound 217 is attained.

## Local setup

Use the nonnegative `Q_3`-facet slack

```text
sigma = b + 2q - t/2,
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

The exact finite theorem proved here is

```text
Delta_K >= 217                                             (3)
```

for every nonempty square-free edge set in `Q_5`.

## Complete Q4 cutoff

Every square-free `Q_4` has at most 24 edges, and the committed sharp `Q_4`
inequality gives `delta_H>=0`.  Therefore a facet in a counterexample to (3)
would satisfy

```text
17S_H - 3E_H < 217,
E_H <= 24,
```

which implies `17S_H<289` and hence `S_H<=16`.  This cutoff is exact: the
next slack layer has minimum possible deficit

```text
17*17 - 3*24 = 217.
```

The production verifier glues complete square-free restrictions from all
eight `Q_3` facets.  It enumerates exactly 490,753 labeled square-free `Q_4`
patterns with `S_H<=16`, visiting 146,812,464 gluing nodes.  Every completed
mask is recomputed directly from its 24 squares and witness multiplicities.

The independent checker instead assigns the 32 global endpoint-pair edges
one at a time, retaining complete local candidate sets and pruning only when
the sum of their minimum remaining costs exceeds 32.  It visits 10,642,534
nodes, prunes 4,190,645, and recovers exactly the same complete set.  The
common normalized graph-set SHA-256 is

```text
9274309488ef16e6e49a2066e83a364e704d99b716f271740427421ca90b5189.
```

## Structural compression

As in the corrected gap-200 proof, call a labeled `Q_3` restriction
*extendable* if it occurs on a facet of a nonempty zero-deficit `Q_4`
pattern.  For a positive-deficit pattern `H`, let `b(H)` count its
nonextendable boundaries and let `e_0(H)` count its empty boundaries.

For a putative `Q_5` pattern with `p` positive-deficit, `k` nonempty
zero-deficit, and `z` empty facets, the verifier imposes three exact necessary
conditions:

1. `sum E_H=4E_K`, because every edge lies in four `Q_4` facets.
2. For `l=p+k` live facets, the exact maximum supported edge counts for
   `l=1,...,10` are `0,0,0,1,5,9,16,28,48,80`.
3. Every positive facet satisfies `b(H)<=p+z-1`, because a nonextendable
   boundary cannot face a zero-deficit facet.

No parity restriction is used.  The complete cutoff has 180 positive
boundary-profile classes below 217.  The production and independent
derivations have common profile-table SHA-256

```text
a252509f19f7f818c3b992adb7f7ce62760946158e0e330805d719c8b272b9ea.
```

The necessary conditions retain the thirteen already excluded sub-200 rows
and precisely twelve new rows:

| total | positive profiles `(delta,E,b,e_0)` | `k` | `z` | `E_K` |
|---:|---|---:|---:|---:|
| 203 | `42_0,42_0,48,71` | 6 | 0 | 44 |
| 205 | `28` five times; `65` | 3 | 1 | 41 |
| 208 | `42_0,42_0,124` | 7 | 0 | 45 |
| 210 | `28` six times; one of `42_0,42_6,42_7` | 2 | 1 | 42 |
| 210 | `28` three times; three `42` profiles with badness `000,006,066,666` | 3 | 1 | 42 |
| 210 | `42_0` five times | 4 | 1 | 42 |
| 215 | `48` three times; `71` | 6 | 0 | 43 |

Here `42_j` abbreviates `(42,20,j,0)`; the remaining abbreviations retain
their unique displayed deficit and profile from the preceding package.  The
eight total-210 rows are counted separately.  No structural row has total
200, 201, 202, 204, 206, 207, 209, 211, 212, 213, 214, or 216.  Moreover,
the complete `Q_4` census contains no individual facet of deficit 200.

## Exact residual closure

Every proof-critical catalog is decomposed into complete `Aut(Q_4)` orbits.
The only new splits are:

| profile | catalog size | orbit sizes |
|---|---:|---|
| `(65,18,4,0)` | 576 | 192, 384 |
| `(42,20,6,0)` | 32 | 32 |
| `(42,20,7,0)` | 896 | 384, 384, 128 |

All other used catalogs remain the single orbits already recorded in the
gap-200 package.  Facet transitivity allows one positive facet to be fixed;
the stabilizer acts as the full `Aut(Q_4)`, so one canonical representative
from every orbit suffices.  The production verifier then enforces exact
agreement on every shared `Q_3` boundary.  The independent checker instead
propagates values on all 80 global `Q_5` edges.

The new window closes as follows:

| total | structural rows | fixed-orbit placement cases | production nodes | solutions |
|---:|---:|---:|---:|---:|
| 203 | 1 | 252 | 252 | 0 |
| 205 | 1 | 1,008 | 1,008 | 0 |
| 208 | 1 | 36 | 36 | 0 |
| 210 | 8 | 27,090 | 27,361 | 0 |
| 215 | 1 | 84 | 84 | 0 |

Thus 28,470 new cases are checked.  Including the 2,430 parity-free cases
below 200, both implementations exclude all 30,900 residual cases.  The
independent checker uses 28,470 nodes for the new rows; the small difference
from the production count reflects its global-edge propagation order.

The zero-total case remains impossible separately: incidence forces 4 or 8
live facets and 17 or 34 edges, while those live-facet sets support at most 1
or 28 edges.  Every positive total below 217 is therefore absent after
structural compression or is one of the exactly excluded rows, proving (3).

The searches remain shallow because they expose boundary-signature
incompatibilities.  They are not an undirected enumeration of all `2^80`
edge sets.

## Global lower bound

Import the published exact value `ex(Q_5,C_4)=56`.  From (2) and (3), every
nonempty square-free edge set in `Q_5` satisfies

```text
S_K >= (12E_K+217)/34 >= (127/272)E_K.              (4)
```

The last inequality is tightest at `E_K=56` and also holds for the empty
set.  Each `Q_3` in `Q_d` lies in `binom(d-3,2)` five-subcubes and each edge
lies in `binom(d-1,4)`, so summing (4) gives

```text
S >= 127 E(d-1)(d-2)/3264.                          (5)
```

For a square-saturated graph put `N=d2^(d-1)`, `E=|E(G)|`, and `M=N-E`.
The established active-square identities are

```text
B+3A = (d-1)E - 3M,
B+3A >= M/2 + S/(d-2).
```

Substitution of (5) gives

```text
3137(d-1)E >= 11424M.
```

Replacing `M` by `d2^(d-1)-E` proves

```text
(3137d+8287)E >= 5712d2^d,
```

which is (1).

## Reproduction

Python 3.11 or later is sufficient; no third-party package, solver, network,
randomness, floating point, or external data file is used.  The two entry
points load the reviewed, corrected definition-level engines from the
adjacent gap-200 directory and independently recompute the enlarged cutoff.

```bash
cd graph_theory/hypercube_square_saturation_q5_gap217

PYTHONDONTWRITEBYTECODE=1 python3 verify.py > /tmp/q5-gap217.out
diff -u EXPECTED_OUTPUT.txt /tmp/q5-gap217.out

PYTHONDONTWRITEBYTECODE=1 python3 independent_check.py > /tmp/q5-gap217-independent.out
diff -u EXPECTED_INDEPENDENT_OUTPUT.txt /tmp/q5-gap217-independent.out

PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_verify.py
sha256sum -c SHA256SUMS
```

The global-edge checker is deliberately slower than the facet-gluing
verifier.  Runtime measurements are operational information, not proof data.

## Review correction, literature, and scope

The independent review of the gap-200 theorem accepted its mathematics and
identified a documentation-only inconsistency: the equality orbit has
`(E,b,e_0)=(17,0,1)`, not `(17,0,0)`.  That correction was applied to the
parent package at verified commit
`f6aab54626b590ff60623eb02fb71d90cc9558bd`; the present package inherits and
tests the corrected profile.

Primary context checked on 2026-09-19:

- Johnson and Pinto, [*Saturated Subgraphs of the Hypercube*](https://arxiv.org/abs/1406.1766).
- Morrison, Noel, and Scott, [*Saturation in the Hypercube and Bootstrap Percolation*](https://arxiv.org/abs/1408.5488).
- Dejter, Emamy-K, and Guan, [*On the fault tolerance in a 5-cube*](https://www.researchgate.net/publication/265697468_On_the_fault_tolerance_in_a_5-cube), for the imported exact value `ex(Q_5,C_4)=56`.

Focused live searches for the exact constant, theorem text, and distinctive
phrases found no published 217-unit facet gap or `5712/3137` lower constant.
This supports “apparently new relative to the searched sources,” not a
historical-priority claim.

The finite theorem trusts readable CPython integer, set, tuple, hash, and bit
semantics; the pinned parent engines; and the written completeness and
symmetry reductions.  The all-dimensional theorem additionally trusts the
displayed human incidence argument and the imported `ex(Q_5,C_4)=56`
theorem.  The computation does not reprove that external extremal value,
formalize the universal double counts, determine exact saturation numbers,
or prove that the `Q_5` deficit lower bound 217 is attained.  Advancing past
217 requires admitting the new `S_H=17` facet layer and is therefore a
genuine next frontier rather than another row in the present cutoff.
