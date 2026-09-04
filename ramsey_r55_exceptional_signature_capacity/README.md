# Exceptional-neighborhood capacities exclude seven more hard Ramsey profiles

A signature-capacity obstruction reduces the team's remaining hard-branch
degree candidates from **88 to 81 global profiles**, and from **321 to 307
anchored splits**. It applies without an automorphism assumption.

The completed census tests the 32 inherited profiles with at most six
exceptional vertices (degree different from 21). Seven are excluded. The
other 25 have witnesses only for the stated marginal necessary-condition
screen. The 56 larger profiles are not classified by this census and remain
in the list of 81 candidates. No complete signature assignment, central
graph, or 43-vertex Ramsey graph is claimed.

The mechanism is combinatorial: degree-21 vertices sharing a fixed
exceptional-neighborhood pattern have restricted clique and independence
numbers. Their multiplicity is therefore bounded. This catches information
lost by aggregate edge counts and even by individual weighted degrees.

## Inputs and exact scope

Let `G` be a red graph on 43 vertices with no red or blue `K_5`; blue means
the complement. Assume the hard branch, where every color-neighborhood
has deficiency at least seven relative to its maximum possible edge count.
The inherited extrema are

```text
d       18  19  20  21  22  23  24
U(d)    85  92 100 107 114 122 132.
```

Normalize red to be the sparser color and write `m=231+M`, `214<=M<=220`.
The [local-deficiency theory](../ramsey_r55_local_extremal_deficiency/README.md)
and [vertexwise identity](../ramsey_r55_one_defect_anchor_localization/README.md)
give

```text
S(v) = sum_(w in N_R(v)) (d(w)-21) <= M-b(d(v)),
d       18   19   20   21   22   23   24
b(d)   220  221  220  220  221  223  223.                (1)
```

The [aggregate sieve](../ramsey_r55_exceptional_degree_sieve/README.md)
left 88 of 104 global profiles and 321 of 349 anchored splits. Its complete
certificate `PROFILES.tsv` is the input here. Its separate
[independent review](../ramsey_r55_exceptional_degree_sieve_review3/README.md)
accepts that scope, including the distinction between count vectors and
graph realizations.

Let `E={v:d(v)!=21}`, `k=|E|`, `C=V(G)\E`, and `N=43-k`. Order `E` by
nondecreasing global degree, with equal-degree vertices still labeled.
Let `F=G[E]`, write `d_i` for a vertex's degree in `G` (not in `F`), and
`epsilon_i=d_i-21`. Then every actual core must satisfy

```text
sum_(j in N_F(i)) epsilon_j <= M-b(d_i),                 (2)
sum_i epsilon_i * (d_i-deg_F(i)) <= N*(M-220).           (3)
```

Equation (2) is now individual, not averaged over a degree class. Equation
(3) sums (1) over all central vertices: `d_i-deg_F(i)` is the exact number
of red incidences from exceptional vertex `i` into `C`. Also, `F` itself
has neither a red nor a blue `K_5`.

## Signature-capacity lemma

For `v in C`, define its signature `X=N_R(v) intersect E`. Let `C_X` be
the central vertices with this signature and `y_X=|C_X|`. Put

```text
r_X = omega(F[X]),       s_X = alpha(F[E\X]),
omega(empty)=alpha(empty)=0.
```

The following are necessary:

1. `sum_(i in X) epsilon_i <= M-220`, by (1) at `v`.
2. If `r_X>=4` or `s_X>=4`, then `y_X=0`: any such central vertex completes
   a monochromatic `K_5` with four exceptional vertices.
3. Otherwise `G[C_X]` has no red `K_(5-r_X)` and no blue `K_(5-s_X)`.
   A forbidden clique in `C_X`, together with a maximum corresponding
   clique in its common exceptional neighborhood, would be a `K_5`.

Only the elementary Ramsey upper bound is needed:

```text
R(a,b) <= choose(a+b-2,a-1).
```

For completeness, take `R(1,b)=R(a,1)=1`. At
`R(a-1,b)+R(a,b-1)` vertices, a chosen vertex has either at least
`R(a-1,b)` red neighbors or at least `R(a,b-1)` blue neighbors. In either
case extend a clique in that neighborhood or obtain a forbidden clique of
the opposite color there. Induction and Pascal's identity give the displayed
bound. No exact higher Ramsey number or new catalog input is needed.

Consequently an admissible signature has the conservative capacity

```text
c_X = min(N, choose(8-r_X-s_X,4-r_X)-1),                 (4)
0 <= y_X <= c_X.
```

Set `c_X=0` for signatures failing either condition 1 or 2. The full
signature-count system necessarily satisfies

```text
sum_X y_X = N,
sum_(X containing i) y_X = d_i-deg_F(i)  for every i,    (5)
y_X integral.
```

This pass uses only the following marginal projections, not the full
integer system (5):

```text
sum_X c_X >= N,
sum_(X containing i) c_X >= d_i-deg_F(i),
sum_(X not containing i) c_X >= N-d_i+deg_F(i).          (6)
```

Passing (2), (3), and (6) is not proof that a joint vector `y` exists.
Even a joint vector would not specify the edges within or between the
signature cells, or enforce the original local edge-count caps.

## Completed finite classification

For each of the 32 inherited profiles with `k<=6`, enumerate all
`2^choose(k,2)` red graphs on its labeled exceptional vertices. There is no
isomorphism quotient and no search timeout. Test (2)--(3), reject any core
`K_5`, then compute every signature capacity and test (6).

| Stage | Labeled core instances |
|---|---:|
| Entire universe over 32 profiles | 209,443 |
| Pass individual/central weighted inequalities | 5,114 |
| Rejected for a core monochromatic `K_5` | 159 |
| Rejected next for red signature capacity | 5 |
| Rejected next for blue signature capacity | 13 |
| Pass the stated marginal screen | 4,937 |

No core reaches a rejection at the total-capacity inequality in this census.
The stages are ordered: core `K_5`, total capacity, then increasing vertex
index with its red capacity before blue capacity. Counts are labeled core
instances, not nonisomorphic graphs. The 4,937 survivors belong to 25
profiles; seven profiles have no survivor:

| Global degree multiset | M | Weighted cores | Decisive obstruction | Removed splits |
|---|---:|---:|---|---:|
| `20^3 21^39 23^1` | 220 | 1 | red demand 20, capacity 9 | 2 |
| `20^4 21^38 24^1` | 220 | 5 | four red-capacity failures; one core `K_5` | 2 |
| `19^1 20^1 21^39 22^2` | 220 | 1 | blue demand 21, capacity 17 | 3 |
| `19^2 21^38 22^3` | 220 | 0 | individual weighted rows incompatible | 2 |
| `18^1 20^1 21^38 22^3` | 220 | 7 | blue capacity fails in all seven cores | 3 |
| `18^1 20^2 21^40` | 218 | 2 | blue demand 24, capacity 19 or 9 | 1 |
| `18^1 19^1 21^41` | 218 | 1 | blue demand 24, capacity 19 | 1 |

Thus seven additional global profiles and 14 anchored splits are excluded
relative to the pinned aggregate sieve. The remaining global counts by
`M=214,...,220` are `1,3,7,13,19,20,18`; the remaining split counts are
`1,5,17,39,67,85,93`. These sum to 81 and 307, respectively.

### Two short structural examples

For `20^3 21^39 23^1`, the degree-23 vertex `h` has weight 2 and requires
weighted neighbor sum at most -3. It must be red to all three weight-minus-one
vertices. Each such vertex then needs red edges to the other two to offset
the weight 2. Hence `F=K_4`. A central red neighbor of `h` must be red to at
least two of the three low vertices by its weighted inequality, but not all
three because that gives a red `K_5`. There are only three signatures.
Each has `r_X=3,s_X=1`, hence capacity three: two red-adjacent central
vertices complete a red `K_5`, and four blue-cliqued ones complete a blue
`K_5` with the omitted exceptional vertex. The total capacity is nine,
but `h` needs `23-3=20` central red neighbors.

For `19^2 21^38 22^3`, each weight-minus-two vertex must be adjacent to the
other and can then have at most one weight-one neighbor: its target is -1.
So there can be at most two red incidences between the two low and three
high vertices. Each high vertex also has target -1, so needs at least one
low neighbor. Three required incidences cannot fit into two. This example
needs individual rows but no signature capacity.

## Reproduction, labels, and compact evidence

Python 3.11.2, standard library only. From the repository root:

```bash
set -o pipefail
python3 ramsey_r55_exceptional_signature_capacity/classify_small_cores.py \
  | cmp - ramsey_r55_exceptional_signature_capacity/CENSUS.tsv
python3 ramsey_r55_exceptional_signature_capacity/classify_small_cores.py --json \
  | cmp - ramsey_r55_exceptional_signature_capacity/REJECTIONS.json
python3 ramsey_r55_exceptional_signature_capacity/check_small_cores.py \
  | cmp - ramsey_r55_exceptional_signature_capacity/EXPECTED_OUTPUT.txt
cd ramsey_r55_exceptional_signature_capacity
sha256sum -c SHA256SUMS
```

The classifier takes about 1.5 seconds; the separate checker about 3.2 seconds
on the research host. The files contain no large search dump. Input SHA-256:
`a8bd3a7def8d719947e74601f410255856a309e7f66af0ee16227370b9a4f3fa`.
Rejection-certificate SHA-256:
`aea17f9d5ad50f0dbeadb281e14306ab179b1eaf33ec2084ac938e72c845d53b`.

`CENSUS.tsv` records every stage count and the smallest passing red-edge
mask for all 32 profiles. Edge bits follow lexicographic pairs `(i,j)`,
`i<j`, of degree-sorted exceptional vertices. Equal-degree vertices remain
distinct. `REJECTIONS.json` lists every weighted core of the seven excluded
profiles and its explicit blocking capacity or core-`K_5` verdict. For the
profile with no weighted core, the exhaustive universe and the short
argument above certify the empty list. `-` is the absent-witness marker.

The checker imports no classifier code. It traverses graphs in Gray-code
order, uses neighbor sets, computes weighted central incidence directly,
enumerates literal clique subsets, and obtains capacities from the Ramsey
recurrence instead of the classifier's clique DP and binomial expression.
It compares every field of the full census and every rejection record,
including the smallest survivor masks. Four deliberate certificate changes
are rejected. Normal and assertion-disabled executions reproduce the files.

## Trust boundary and next use

The 104-profile universe, earlier 16 exclusions, exact extrema, and
hard-branch graph-to-degree reductions are imported. Their catalog and
unformalized-proof boundaries are inherited; the current pass does not
re-enumerate those catalogs. The new capacity lemma has an elementary proof;
its finite classification trusts exact CPython integer arithmetic and the
small programs. The proof is not proof-assistant formalized, and the
separate checker is an internal validation, not an independent peer review.

Neighborhood counting has a long history in Ramsey bounds; see
[McKay and Radziszowski, Subgraph Counting Identities and Ramsey Numbers](https://www.cs.umd.edu/~gasarch/BLOGPAPERS/Rof5LE49.pdf).
No historical priority for this counting principle or the elementary Ramsey
bound is claimed. The contribution is the explicit capacity interface and
its reproducible refinement of the team's surviving profile list.

The reviewed [no-order-five theorem](../ramsey_r55_no_order5_automorphism_review3/README.md)
motivated the switch away from that symmetry branch but is not a mathematical
dependency of this result. No automorphism or catalog-neighborhood sweep is
duplicated. The earlier order-five artifacts are preserved.

The natural next step is a coupled use of (5), possibly with constraints
between signature cells, or a separately scoped larger-core census. Neither
is launched here. The low-deficiency branch and the general 43-vertex
construction target remain unresolved. This pass stops at its completed
small-core milestone.
