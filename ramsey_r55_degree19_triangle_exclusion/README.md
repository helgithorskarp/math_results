# A cell-edge density obstruction excludes degree profile 19^1 20^3 21^39

The hard-branch degree profile **`19^1 20^3 21^39` is impossible**. This
removes one more global candidate and its two anchored splits, reducing the
team's counts from **68 to 67 globals** and **275 to 273 splits**.

The new step is an edge-density obstruction, not another cell-size bound.
In the sole core retained by the preceding union screen, a 16-vertex central
neighborhood must span at least **77 red edges**, but a rooted `(4,4)`
constraint bounds it by **75**. The proof covers every possible assignment
of cell sizes and edges, not only the earlier stored primal witness.

This is not a 43-vertex construction or a Ramsey lower-bound improvement.
Eleven small global profiles remain, along with the 56 larger exceptional
profiles unclassified by these small-core reductions. The low-deficiency
branch and the target graph remain unresolved. No automorphism assumption
or catalog-radius search is used.

## 1. A localized theorem

Let `G` be a red graph on 43 vertices, blue its complement, with no
monochromatic five-clique. Suppose its degrees are `19^1 20^3 21^39`.
Let `z` have degree 19 and let `L={1,2,3}` consist of the degree-20 vertices.
Assume only the following local edge-count caps:

```text
t_R(z)<=85,       t_B(z)<=115,
t_R(v)<=100,      t_B(v)<=100 for every degree-21 vertex v.      (1)
```

Here `t_R(v)` counts red edges induced by the red neighbors of `v`, and
`t_B(v)` counts blue edges induced by its blue neighbors. Under these
hypotheses, **no such graph exists**. No local cap at the three degree-20
vertices is needed.

In the hard branch every color-neighborhood is at least seven edges below
its maximum for its order. The
[upstream extrema](../ramsey_r55_local_extremal_deficiency/README.md)
`U(19)=92`, `U(21)=107` and `U(23)=122` imply (1), so the localized theorem excludes the entire
hard-branch profile. The conditional theorem with (1) stated explicitly
needs no extremal catalog, and can be read independently of the campaign.

## 2. Force the exceptional star and central incidence constraints

Handshaking gives `m=(19+3*20+39*21)/2=449` red edges. The elementary
[vertex identity](../ramsey_r55_one_defect_anchor_localization/README.md) is

```text
t_R(v)+t_B(v)=choose(42-d(v),2)-m+sum_(w in N_R(v))d(w).         (2)
```

It follows by partitioning red edges into a vertex's two neighborhoods and
their cross edges, then subtracting the red degree sum of its red neighbors.
Write `epsilon(w)=d(w)-21`. At `z`, (2) and (1) give

```text
203+sum_(w in N_R(z))epsilon(w) <= 200.
```

The only available nonzero weights are the three degree-20 vertices, of
weight `-1` each. Thus **all three edges z--L are red**. Equality holds,
forcing `(t_R(z),t_B(z))=(85,115)`.

Set `E={z,1,2,3}`, `C=V(G)\E`, so `|C|=39`, and label `z=0`.
For `v in C`, the identity gives

```text
202+sum_(w in N_R(v))epsilon(w) <= 200.
```

Consequently its signature `X=N_R(v) intersect E`, with indicators `I_i`,
obeys

```text
2I_0+I_1+I_2+I_3 >= 2.                                      (3)
```

The possible exceptional cores are the star from 0 to `L`, with any of the
eight graphs on `L`. Up to relabeling 1,2,3, they are distinguished by
`e(G[L])=0,1,2,3`. This quotient uses only names, not a graph automorphism.

## 3. Close the three nontriangle cores

These are the core obstructions already implicit in the previous
[coupled counts](../ramsey_r55_coupled_signature_counts/README.md) and
[union cuts](../ramsey_r55_signature_union_cuts/README.md). They are given
explicitly here, so the new profile theorem does not depend on a large
enumeration.

For disjoint red-clique `A` and blue-clique `B` in `E`, write
`W(A;B)` for the number of central vertices red to all of `A` and blue
to all of `B`. It is at most `R(5-|A|,5-|B|)-1`, since either forbidden
clique in that common neighborhood extends through the roots.

Only `R(3,4)<=9` and its color reversal are needed below. A self-contained
proof uses `R(2,4)=4`, `R(3,3)<=6`: a putative `(3,4)` graph on nine vertices
has red degree at most three and blue degree at most five at every vertex.
Both bounds must be equalities, giving an odd-order 3-regular graph, a
handshaking contradiction. The six-vertex bound follows from the usual
three-neighbors-in-one-color argument.

### No edges in L

The central red-incidence targets at 0,1,2,3 are `(16,19,19,19)`.
The only allowed one-element signature is `{0}`. Since
`2-|X|<=1[X={0}]` for all signatures allowed by (3), summing gives

```text
5=2*39-16-19-19-19 <= y_{ {0} }.
```

But this cell is blue to the independent triple `L`, so it must be a red
clique; and it is red to 0, so it has at most three vertices. Contradiction.

### One edge in L

Normalize that edge to `12`. The central incidence targets are
`(16,18,18,19)`. The pointwise inequality corresponding to (3) is

```text
3-I_0-I_1-I_2-2I_3
 <= 1[X contains {0}, avoids {1,3}]
   +1[X contains {0}, avoids {2,3}]
   +1[X contains {1,2}, avoids {0}].                         (4)
```

The three root pairs are valid, and their bounds are eight each. Summing
(4) over `C` gives `27=117-16-18-18-38 <= 8+8+8=24`, impossible.

### Two edges in L

Normalize them to `12,13`. The targets are `(16,17,18,18)`. Now use

```text
2-I_0-I_2-I_3
 <= 1[X contains {0}, avoids {2,3}]
   +1[X contains {1,2}, avoids {0}]
   +1[X contains {1,3}, avoids {2}].                         (5)
```

Again all three common-neighborhood bounds are eight. Summing gives
`26=78-16-18-18 <= 24`, impossible.

For full transparency, here is the complete pointwise check of (4)--(5).
Signature mask bit `i` is `I_i`; these are all 12 masks allowed by (3).

| mask | left (4) | right (4) | left (5) | right (5) |
|---:|---:|---:|---:|---:|
| 1 | 2 | 2 | 1 | 1 |
| 3 | 1 | 1 | 1 | 1 |
| 5 | 1 | 1 | 0 | 0 |
| 6 | 1 | 1 | 1 | 1 |
| 7 | 0 | 0 | 0 | 0 |
| 9 | 0 | 0 | 0 | 0 |
| 10 | 0 | 0 | 1 | 1 |
| 11 | -1 | 0 | 0 | 1 |
| 12 | 0 | 0 | 0 | 0 |
| 13 | -1 | 0 | -1 | 0 |
| 14 | -1 | 1 | 0 | 1 |
| 15 | -2 | 0 | -1 | 0 |

## 4. The new triangle-core obstruction

Only `G[L]=K_3` remains, so `G[E]=K_4`. Let

```text
J=N_R(z) intersect C,       |J|=19-3=16,
K=C\J,                     |K|=23,
h_i=|N_R(i) intersect J|,   H=h_1+h_2+h_3.
```

Each vertex in `L` has three red neighbors in `E`, leaving 17 in `C`.
Thus there are 51 red incidences from `L` to `C`. Every vertex of `K` is
blue to `z`, so (3) requires at least two red neighbors in `L`. Therefore

```text
H <= 51-2*23=5.                                             (6)
```

Since `t_R(z)=85`, partitioning edges inside its red neighborhood gives

```text
85=e_R(L)+e_R(L,J)+e_R(J)=3+H+e_R(J),
e_R(J)=82-H >= 77.                                          (7)
```

Choose `i in L` with `h_i<=1`, possible by (6). Let
`Y=N_R(i) intersect J` and `Q=J\Y`. The graph on `Q` has no red four-clique,
as it lies in `N_R(z)`, and no blue four-clique, as it lies in `N_B(i)`.
Every red neighborhood inside this `(4,4)` graph has type `(3,4)`, so every
red degree inside `Q` is at most eight.

If `|Y|=0`, this gives `e_R(J)<=16*8/2=64`. If `|Y|=1`, it gives

```text
e_R(J) <= 15*8/2+15=75.                                    (8)
```

Equations (7) and (8) contradict one another. This completes every core
case and proves the localized theorem and the hard-branch corollary.

### Reusable edge-lifting inequality

More generally, in any `(5,5)` graph take distinct vertices `z,w` and any
`J subset N_R(z)\{w}` with `n=|J|`. Put `s=|J intersect N_R(w)|`.
The same `(4,4)` degree bound gives

```text
e_R(J) <= 4(n-s)+s(n-s)+choose(s,2).                         (9)
```

No color is prescribed for edge `zw`. This inequality is valid regardless
of the campaign's degree profile or hard-branch caps. The first term bounds
edges on the common red-z/blue-w part; the other terms restore the removed
vertices with all possible edges. It is not claimed sharp for `(n,s)=(16,1)`.
It supplies an edge-count constraint that signature multiplicities alone
do not enforce.

## 5. What the old cell-size system actually admitted

For the triangle core set

```text
a=y[{0}],                d=y[L],
c_i=y[{0,i}],            e_i=y[{0} union (L\{i})],
b_i=y[L\{i}],            Csum=sum c_i,  Esum=sum e_i.
```

Here `y[S]` denotes the multiplicity of the set signature `S`. All other cells are zero:
(3) rules out the small signatures and the red `K_4` rules out the full
signature. The total and incidence equations reduce exactly to

```text
Csum+d+2Esum=5,
a=16-Csum-Esum,
b_i=6+c_i+Esum-e_i.                                        (10)
```

All entries are nonnegative integers; `d<=3`, since its vertices and 0
are common red neighbors of the red triangle `L`, and hence form an
independent set of order at most four. Thus `Esum<=2` and `c_i<=5`.
These bounds give a complete small enumeration, not a timeout search.

Applying all preceding union bounds to (10) leaves exactly six labeled
vectors, in two three-element orbits under permutations of `L`:

| representative | nonzero `signature mask:count` pairs |
|---|---|
| A | `1:11, 3:1, 5:2, 6:8, 9:2, 10:8, 12:7` |
| B | `1:12, 3:1, 5:1, 6:7, 7:1, 9:1, 10:8, 12:8` |

Both have `H=5` and require `e_R(J)=77`. They certify feasibility only
of the old union-count relaxation. The new proof eliminates all six and
does not rely on their enumeration. In particular, this is more than a
rejection of the earlier chosen primal vector.

## 6. Reproduction, provenance and boundary

[verify.py](verify.py) is a standard-library exact audit, not a solver or
a proof-assistant formalization. It checks all 64 exceptional graphs, the
eight forced-star cores and their four classes, every entry of the two
pointwise tables, the star bound, all `H=0,...,5` density contradictions,
and the six-vector cell census. Its compact generated data is
[CERTIFICATE.json](CERTIFICATE.json).

It also tests (9) on all rooted subsets in every labeled `(5,5)` graph
on five vertices. A literal 19-vertex Ramsey fixture, obtained by adjoining
two roots to the quadratic-residue graph on 17 vertices, saturates (9) at
`(n,s)=(17,0)` with 68 edges. Every five-set is checked directly; its name
or a catalog is not trusted. A rooted red ten-clique violates (9), testing
that the no-monochromatic-five hypothesis cannot be silently discarded.
These are validation fixtures, not target witnesses.

Requirements: CPython 3.11.2 and its standard library. From the repo root:

```bash
set -o pipefail
python3 ramsey_r55_degree19_triangle_exclusion/verify.py \
  | cmp - ramsey_r55_degree19_triangle_exclusion/EXPECTED_OUTPUT.txt
python3 -O ramsey_r55_degree19_triangle_exclusion/verify.py --emit-certificate \
  | cmp - ramsey_r55_degree19_triangle_exclusion/CERTIFICATE.json
python3 -O ramsey_r55_degree19_triangle_exclusion/verify.py --replay-parent \
  | cmp - ramsey_r55_degree19_triangle_exclusion/EXPECTED_OUTPUT.txt
cd ramsey_r55_degree19_triangle_exclusion
sha256sum -c SHA256SUMS
```

The optional parent replay reruns the prior solver-free union checker;
it is not needed for the new localized mathematical argument. Cumulative
counts use pinned upstream profiles and summaries, and hence inherit their
scope and completeness boundaries. The new counts for `M214,...,M220` are
`1,3,7,11,13,15,17` globals and `1,5,17,35,54,72,89` anchored splits.

An exploratory cell-edge LP found the obstruction in both cell-size orbits;
the combinatorial approach reduced it to (6)--(8). No LP verdict or trace
is used in this theorem or required for reproduction. The source does not
claim that its own generated table comparison is independent peer review.
The mathematical proof remains unformalized, and its finite audits trust
the source and Python runtime. No historical priority is claimed for the
common-neighborhood, degree-sum, or deletion-bound principles.

The preceding nontriangle cases are reused with explicit credit to the
coupled and union artifacts linked above. The new information is closure
of the triangle core and therefore of the entire profile, plus the reusable
cell-edge constraint (9). We do not start another profile, larger exceptional
stratum, catalog radius, or symmetry search in this pass.
