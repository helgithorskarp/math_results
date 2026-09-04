# Exceptional-degree adjacency sieve for the hard Ramsey-43 branch

An exact aggregate-adjacency test reduces the hard branch from 104 global
degree-count profiles to 88, and from 349 anchored split profiles to 321.
It excludes 16 global profiles by coupling reciprocal edges between degree
classes. Thirteen exclusions admit short real-valued linear contradictions;
the other three require integrality and have explicit half-integral solutions
to the same relaxation. One of the 16 global exclusions was already absent
from the anchored 349-profile list. The other 15 remove 28 anchored profiles.

This is a necessary-condition theorem, not a graph construction or a complete
feasibility classification for Ramsey graphs. Every surviving entry is only
an integer **edge-count matrix**, not a realized graph. The low-deficiency
branch and the general `R(5,5)>=44` construction target remain unresolved.

## Hypotheses and the vertexwise input

Let `G` be a red graph on 43 vertices with no red or blue `K_5`, with blue
meaning the complement. We assume the hard branch: every color-neighborhood
has at least seven fewer edges than the maximum for its order. The inherited
[local-deficiency theorem](../ramsey_r55_local_extremal_deficiency/README.md)
then gives degrees 18 through 24, extrema

```text
d                 18  19  20  21  22  23  24
U(d)              85  92 100 107 114 122 132
w(d)              21  12   3   0   3  12  21,
```

and `W=sum_v w(d(v)) in {3,9,...,39}`. Choose the sparser color to be red.
Its edge count is `m=231+M` for `M=214,...,220`. If `n_d` counts degree-`d`
vertices, these arithmetic conditions leave the 104 global profiles. There
are at most 13 exceptional vertices (those of degree different from 21).

Put `epsilon_d=d-21`. The [vertexwise neighborhood identity](../ramsey_r55_one_defect_anchor_localization/README.md)
and hard-branch local caps imply, at each degree-`d` vertex `v`,

```text
sum_(w in N_R(v)) (d(w)-21) <= t_d = M-b(d),
d                 18   19   20   21   22   23   24
b(d)             220  221  220  220  221  223  223.        (1)
```

For completeness, the identity is
`t_R(v)+t_B(v)=choose(42-d,2)-m+sum_(w in N_R(v))d(w)`.
The two local edge counts are at most `U(d)-7` and `U(42-d)-7`.
Subtracting `21d` gives (1). Its nonnegative slack is exactly the sum of
the two local deficiencies beyond seven at `v`.

## Eliminate the degree-21 vertices from the count constraints

Let `I={d != 21 : n_d>0}` and let `n_0=n_21`. For `i<=j` in `I`, let
`q_ij` be the number of red edges between these degree classes, counting
an edge within one class once. These integers obey

```text
0 <= q_ii <= choose(n_i,2),
0 <= q_ij <= n_i*n_j  for i<j.                          (2)
```

Define the total internal exceptional incidence and weighted neighbor sum
at class `i` by

```text
J_i = 2q_ii + sum_(j!=i) q_ij,
S_i = 2(i-21)q_ii + sum_(j!=i) (j-21)q_ij.
```

Summing (1) over that class, while noting that degree-21 neighbors have
weight zero, gives

```text
S_i <= n_i*t_i                  for every i in I.       (3)
```

Class `i` has exactly `n_i*i-J_i` red incidences to degree-21 vertices.
Consequently the sum of the weighted neighborhood degrees over all
degree-21 vertices is

```text
P - sum_i (i-21)J_i,
where P = sum_i (i-21)n_i*i.
```

Each exceptional edge contributes the sum of its endpoint weights to both
`sum_i (i-21)J_i` and `sum_i S_i`. Thus the degree-21 class supplies

```text
sum_i S_i >= P - n_0*t_21.                              (4)
```

Equations (2)--(4) are the entire relaxation classified here. No clique
constraint, individual exceptional-vertex row constraint, graph realization,
or individual degree-21 neighborhood constraint is silently imposed. All
are candidates for a subsequent strengthening, not part of this theorem.

The class margins `n_i*t_i-S_i` and the central margin
`n_0*t_21-P+sum_i S_i` sum to `(43-W)/2`, the total paired excess. This gives
an exact audit of signs and factors of two. It also explains why the central
inequality can matter even when each exceptional class separately passes.

## Exact classification

| M | input global | excluded global | retained global | input split | excluded split | retained split |
|---:|---:|---:|---:|---:|---:|---:|
| 214 | 1 | 0 | 1 | 1 | 0 | 1 |
| 215 | 3 | 0 | 3 | 5 | 0 | 5 |
| 216 | 7 | 0 | 7 | 17 | 0 | 17 |
| 217 | 14 | 1 | 13 | 40 | 1 | 39 |
| 218 | 21 | 0 | 21 | 69 | 0 | 69 |
| 219 | 27 | 7 | 20 | 95 | 10 | 85 |
| 220 | 31 | 8 | 23 | 122 | 17 | 105 |
| total | 104 | 16 | 88 | 349 | 28 | 321 |

The complete certificate is [PROFILES.tsv](PROFILES.tsv): one row per global
profile, an integer witness for every feasible count system, and a rejection
classification for every excluded system. All boxes for the 16 excluded
profiles together contain only **819** integer tuples. The checker visits
every one directly, without using the searcher's interval pruning.

To count anchored splits, fix a doubly exact degree-21 vertex `v`. Its red
and blue neighborhoods `A,B` both have size 21. If `a_i` exceptional
vertices of degree `i` lie in `A`, then

```text
0<=a_i<=n_i,        sum_i (i-21)a_i = M-220.              (5)
```

The remaining exceptional vertices lie in `B`, with deviation sum `M-221`;
degree-21 counts fill the two sides. These are exactly the inherited
349 split degree-count profiles. Each global rejection removes all its
splits. The profile `18^1 21^42` has no split satisfying (5), so its rejection
recovers an already implicit exclusion rather than adding a new one.

## Two illustrative obstructions

For degrees `19^1 20^1 21^41`, `M=219`. The unique degree-19 vertex needs
weighted red-neighbor sum at most `M-b(19)=-2`. Its only possible neighbor
of negative weight has degree 20 and weight `-1`. The minimum is therefore
`-1`, a contradiction. This needs no finite search.

An integrality-sensitive example has degrees `19^3 20^1 21^39`, `M=217`.
Write `a=q_19,19`, `b=q_19,20`, with integers `0<=a,b<=3`. Conditions (3)--(4)
become

```text
4a+b >= 12,       2b >= 3,       4a+3b <= 17.            (6)
```

Integrality forces `b>=2`, then `a=3` (since `b<=3`), contradicting the last
inequality, which now has left side at least 18. The fractional pair
`(a,b)=(5/2,2)` satisfies all three. Thus replacing integer edge counts by
real variables loses this exclusion.

The other two fractional-feasible but integer-infeasible profiles are
`19^1 20^3 21^38 23^1` at `M=219` and
`19^1 20^2 21^38 22^1 23^1` at `M=220`. Their half-integral witnesses are
included in the certificate, so this distinction is checked, not inferred
from failure of a linear-certificate search.

For the 13 real-infeasible cases, the certificate gives nonnegative
multipliers `lambda_i` of (3). If an edge variable has combined coefficient
`c_ij=lambda_i(j-21)+lambda_j(i-21)`, its minimum contribution over its box
is `capacity_ij*min(0,c_ij)`. In each case the sum of these lower bounds is
strictly greater than `sum_i lambda_i*n_i*t_i`, giving a direct contradiction.
No numerical linear-programming solver is used.

## Certificate format and reproduction

Use Python 3.11.2 (standard library only). From the repository root:

```bash
set -o pipefail
python3 ramsey_r55_exceptional_degree_sieve/classify_profiles.py \
  | cmp - ramsey_r55_exceptional_degree_sieve/PROFILES.tsv
python3 ramsey_r55_exceptional_degree_sieve/verify_certificate.py \
  | cmp - ramsey_r55_exceptional_degree_sieve/EXPECTED_OUTPUT.txt
cd ramsey_r55_exceptional_degree_sieve
sha256sum -c SHA256SUMS
```

Both commands finish in under a second on the research host. The certificate
SHA-256 is `a8bd3a7def8d719947e74601f410255856a309e7f66af0ee16227370b9a4f3fa`.
The independent checker does not import the classifier: it regenerates the
profile universe by a budget recursion, computes constraints from incidence
and the original extrema, verifies every witness and linear contradiction,
and brute-forces all rejected boxes. It rejects malformed count vectors,
missing or duplicated profiles, wrong multiplicities, false exclusions,
and out-of-capacity witnesses.

`counts_18_to_24` lists all seven degree multiplicities. Edge vectors use
lexicographic unordered degree pairs `(i,j)`, `i<=j`, with both degrees
exceptional and positive box capacity. `edge_counts` is an integer witness;
`half_counts` is twice a rational witness. Multipliers follow increasing
active exceptional degree. `-` denotes an empty vector. In particular the
one-defect `20^1 21^42` survivor legitimately has an empty edge vector.

## Scope, provenance, and next boundary

The mathematical inputs are the prior exact local extrema and hard-branch
degree/anchor reductions. The extrema manifest is
[`extrema.json`](../ramsey_r55_local_extremal_deficiency/extrema.json), SHA-256
`7233dd701f47de79c65ecccb6b06ad8f79b16b92c08cfcf73bcef1ed3b4d5b10`.
Its catalog-completeness boundary is inherited; the current computation does
not independently re-enumerate those Ramsey catalogs. The new finite check
uses only Python integer/rational arithmetic. The graph-to-count reduction
above is a hand proof, not a proof-assistant formalization.

Neighborhood-count methods for Ramsey bounds have a long history; see
[McKay and Radziszowski, Subgraph Counting Identities and Ramsey Numbers](https://users.cecs.anu.edu.au/~bdm/papers/r55.pdf).
The claimed progress here is the explicit, reproducible refinement of the
team's hard-branch profile list, not historical priority for degree counting,
integer feasibility, or the conservation identity.

The combinatorial method turns reciprocal adjacency into a small constraint
system, and the research-code audit separates exact exclusions from relaxed
witnesses. This does not supersede the previous all-profile connectivity
theorem: its conclusions still hold on every remaining profile. The next
structural boundary is realizing exceptional adjacency and the individual
degree-21 incidence patterns, or imposing additional Ramsey restrictions.
No such next-phase search is included or running in this checkpoint.
