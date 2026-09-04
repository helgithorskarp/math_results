# Propagation constraints from a doubly exact `R(5,5;43)` anchor

This directory strengthens the companion 21-by-21 cross-matrix normal form.
In the hard branch of the local-deficiency dichotomy, fixing one doubly exact
vertex does not merely fix two `(4,5;21,100)` cores.  The cross matrix also
determines the order and edge count of both color-neighborhoods at every one
of the other 42 vertices.  All 84 of those local graphs must have deficiency
at least seven.  A linear degree-weight test already forces at least 29 of the
42 vertices to have degree 21.  In fact, if the red cross-edge count is `M`,
at least `241-M` of them must reproduce the full doubly exact signature of the
chosen anchor: between 27 and 21 secondary anchors as `M` runs from 214 to
220.

This is a necessary pruning theorem for the hard construction branch.  It is
not a 43-vertex Ramsey graph, an enumeration of the local cores, or a solver
feasibility result.

## Setting

Let `G` be a red graph on 43 vertices with no clique or independent set of
size five.  Assume the hard branch: every red or blue color-neighborhood has
deficiency at least seven relative to the exact `(4,5)` extremal edge counts.
Choose one of the doubly exact vertices `v` forced in that branch, and put

```text
A = N_G(v),                  |A|=21,
B = N_complement(G)(v),      |B|=21,
H = G[A],
K = complement(G)[B].
```

Both `H` and `K` are `(4,5;21,100)` graphs.  For `a in A`, `b in B`, let

```text
x_ab = 1 iff ab is red.
```

The prior normal form gives all mixed-`K_5` clauses, 214--220 red cross
edges, and the first-degree row and column bounds.  The formulas below expose
the previously unused second-neighborhood information.

Write `e_L(S)` for the number of edges of graph `L` induced by `S`, and write
`x(S,T)` and `bar_x(S,T)` for the numbers of red and blue cross edges between
`S subseteq A` and `T subseteq B`.

## Exact row formulas

Fix `a in A`.  Define

```text
P_a = N_H(a),                         h_a = |P_a|,
Pbar_a = A minus ({a} union P_a),
R_a = {b in B : x_ab=1},              r_a = |R_a|,
Rbar_a = B minus R_a.
```

Let `d_a` be the red degree of `a`.  Let `t_R(a)` be the number of red edges
inside its red neighborhood, and `t_B(a)` the number of blue edges inside its
blue neighborhood.  Directly partitioning those two neighborhoods gives

```text
d_a = 1 + h_a + r_a,

t_R(a) = h_a
           + e_H(P_a)
           + e_complement(K)(R_a)
           + x(P_a,R_a),                                      (A_R)

t_B(a) = e_complement(H)(Pbar_a)
           + e_K(Rbar_a)
           + bar_x(Pbar_a,Rbar_a).                             (A_B)
```

The first term `h_a` in `(A_R)` counts the red edges from `v` to `P_a`.
There is no corresponding anchor term in `(A_B)`, because `v` is a red
neighbor of `a`.

## Exact column formulas

Fix `b in B`.  Define

```text
Q_b = N_K(b),                         k_b = |Q_b|,
Qbar_b = B minus ({b} union Q_b),
C_b = {a in A : x_ab=1},              c_b = |C_b|,
Cbar_b = A minus C_b.
```

Since red edges inside `B` are the nonedges of `K`, the analogous partition
gives

```text
d_b = 20 - k_b + c_b,

t_R(b) = e_complement(K)(Qbar_b)
           + e_H(C_b)
           + x(C_b,Qbar_b),                                    (B_R)

t_B(b) = k_b
           + e_K(Q_b)
           + e_complement(H)(Cbar_b)
           + bar_x(Cbar_b,Q_b).                                (B_B)
```

Here the term `k_b` counts the blue edges from `v` to `Q_b`.

## Linear degree propagation

Let `M=sum_(a,b) x_ab`, so `214 <= M <= 220`.  Summing the displayed degree
formulas and using

```text
sum_a h_a = 2|E(H)| = 200,
sum_b k_b = 2|E(K)| = 200
```

gives the two exact deviation identities

```text
sum_(a in A) (d_a-21) = M-220,
sum_(b in B) (d_b-21) = M-221.                         (S)
```

Thus the total deviations on the `A` and `B` sides lie in `[-6,0]` and
`[-7,-1]`, respectively.  These equations couple the row and column degree
patterns more sharply than treating their intervals independently.

Define the symmetric degree weight

```text
w(18)=w(24)=21,  w(19)=w(23)=12,
w(20)=w(22)=3,   w(21)=0.
```

The hard-branch deficiency identity from the companion theorem gives

```text
W = sum_(u in A union B) w(d_u)
    in {3,9,15,21,27,33,39}.                            (W39)
```

The omitted anchor `v` has degree 21 and weight zero, so this is exactly the
global weight.  Every non-21 degree costs at least three; consequently at
most 13 of the 42 secondary vertices have noncentral degree, and

```text
at least 29 vertices in A union B have degree 21.        (P29)
```

There is also an `M`-dependent lower bound on the weight.  Pointwise,
`w(d) >= 3|d-21|`; summing and applying `(S)` gives

```text
W >= 3 sum_u |d_u-21|
  >= 3 |sum_u (d_u-21)|
   = 3(441-2M).                                          (WM)
```

Conditions `(S)`, `(W39)`, and `(P29)` use only row and column sums.  They can
therefore reject a cross matrix before the quadratic local counts below are
computed.

Enumerating the nonnegative degree-count vectors on the two labeled sides,
subject only to 21 vertices per side, `(S)`, and `(W39)`, leaves the following
exact numbers of ordered `(A,B)` profile pairs:

```text
M       W=3  W=9  W=15  W=21  W=27  W=33  W=39   total
214       0    0     0     0     0     0     1       1
215       0    0     0     0     0     1     4       5
216       0    0     0     0     1     4    12      17
217       0    0     0     1     4    11    24      40
218       0    0     1     4     9    19    36      69
219       0    1     3     6    13    25    47      95
220       1    2     4     9    17    32    57     122
total     1    3     8    20    44    92   181     349
```

Here a side profile is the seven-tuple of counts of degrees 18 through 24;
vertices within a side are not assigned or labeled.  This is an exact
integer-profile superset, not a claim that any of the 349 pairs is graphical
or compatible with a chosen core.  At the lowest cross total the superset is
a singleton:

```text
M=214:
(x_18,...,x_24 on A) = (0,0,6,15,0,0,0),
(x_18,...,x_24 on B) = (0,0,7,14,0,0,0).
```

Thus a search at `M=214` has no degree-count branching at all; the other six
cross totals together have only 348 possible ordered side-count pairs before
core-specific row and column feasibility is imposed.

## Hard-branch propagation theorem

For `18 <= q <= 24`, the exact maximum edge counts in an order-`q`
`(4,5)` graph are

```text
q       18  19  20  21  22  23  24
U(q)    85  92 100 107 114 122 132.
```

Every row and column profile computed above must satisfy

```text
18 <= d_u <= 24,
t_R(u) <= U(d_u)-7,
t_B(u) <= U(42-d_u)-7.                                (D7)
```

Indeed, `t_R(u)` and `t_B(u)` are exactly the edge counts of the two local
`(4,5)` graphs at `u`; `(D7)` is precisely the definition of the hard branch.
This supplies 84 exact local inequalities in addition to the mixed-clique
clauses.  The left sides are explicit quadratic functions of the cross bits,
or can be maintained as local-repair scores under a single-bit flip.

There is also a much stronger global propagation condition:

```text
at least 241-M vertices u in A union B satisfy
       (d_u, t_R(u), t_B(u)) = (21,100,100).             (PM)
```

To prove `(PM)`, the exact deficiency identity gives

```text
Delta = (1247-W)/2.
```

The 86 local sides have baseline deficiency `86*7=602`, so at most

```text
E = Delta-602 = (43-W)/2
```

of them can have deficiency greater than seven.  Meanwhile, at most `W/3`
vertices have nonzero degree weight, hence at least `42-W/3` secondary
vertices have degree 21.  A degree-21 vertex can fail to be doubly exact only
if at least one of its two local sides is among those `E` exceptional sides.
Therefore the number of secondary doubly exact vertices is at least

```text
42 - W/3 - (43-W)/2 = (123+W)/6
                          >= 241-M,
```

where the last step is `(WM)`.  A vertex is doubly exact exactly when its
displayed triple is `(21,100,100)`: red degree 21 makes both local orders 21,
and the two local edge counts are then seven below `U(21)=107`.  Thus `(PM)`
does not choose or label the secondary anchors in advance.

There are also side-specific guarantees.  Write `s=220-M` and split
`W=W_A+W_B` over the two sides.  Equation `(S)` and the pointwise weight
bound give `W_A>=3s` and `W_B>=3(s+1)`.  Subtracting the same exceptional-side
budget `E` separately from the degree-21 population on either side yields

```text
exact vertices in A >= 21-W_A/3-E
                    = -1/2+W_A/6+W_B/2 >= 2s+1,
exact vertices in B >= 21-W_B/3-E
                    = -1/2+W_A/2+W_B/6 >= 2s,

number of doubly exact vertices in A >= 2s+1 = 441-2M,
number of doubly exact vertices in B >= 2s   = 440-2M.   (PM_side)
```

The total guarantee `(PM)` is stronger than adding these two separate bounds,
because the exceptional sides cannot simultaneously be spent twice.  The
three guarantees specialize as follows:

```text
M                             214 215 216 217 218 219 220
forced exact vertices in A     13  11   9   7   5   3   1
forced exact vertices in B     12  10   8   6   4   2   0
forced exact vertices in A+B   27  26  25  24  23  22  21
```

For a hard-branch cross search, `(D7)` and `(PM)` are lossless.  A general
construction search must retain the complementary branch in which some
local deficiency is at most six.

## Exact single-cross-flip update

The propagated scores also admit a simple local-repair rule.  Toggle one
cross edge `ab`, and put

```text
sigma = +1 for blue-to-red,  -1 for red-to-blue,
c_R(a,b) = |N_G(a) intersect N_G(b)|,
c_B(a,b) = |N_complement(G)(a) intersect N_complement(G)(b)|.
```

The common-neighbor counts exclude `a,b` and do not depend on the color of
`ab`.  At each endpoint `u in {a,b}`, the profile changes by

```text
(d_u, t_R(u), t_B(u))
    -> (d_u + sigma,
        t_R(u) + sigma*c_R(a,b),
        t_B(u) - sigma*c_B(a,b)).                       (F_end)
```

For a third vertex `u`, its degree is unchanged.  Its red-local count changes
by `sigma` exactly when both `ua` and `ub` are red; its blue-local count
changes by `-sigma` exactly when both are blue.  Otherwise neither changes.
The chosen anchor `v` always sees one red and one blue edge to `a,b`, so its
profile remains `(21,100,100)`.

This follows because only the membership of one endpoint in the other
endpoint's color-neighborhood changes, while at a third vertex only the
color of the single internal edge `ab` changes.  Thus a local-repair program
can update all 42 propagated profiles in one linear scan after a cross flip;
it need not rebuild the 43-vertex graph or rescan five-sets.

## Definition-level audit

`verify_anchor_propagation.py` uses the same embedded `(4,5;21,100)` sample
core as the cross-normal-form artifact, with a nontrivial deterministic
relabeling on the blue side.  It builds seven deterministic
21-by-21 matrices with 214 through 220 red entries.  For every matrix and all
42 non-anchor vertices, it compares `(A_R)`--`(B_B)` against a direct scan of
the resulting labeled 43-vertex coloring.  It also audits `(F_end)` and the
third-vertex rule on 14 toggles, once in each direction for every matrix.

All seven matrices satisfy the earlier cardinality and row/column degree
bounds, but have degree weights from 99 through 111, only 17 through 21
degree-21 vertices, no secondary doubly exact vertex, and violations of
`(D7)`.  They are deliberately not claimed to satisfy the mixed-`K_5`
clauses.  Their role is a regression witness that the new tests contain
information absent from the earlier independent cardinality/degree intervals,
not evidence about feasibility.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 verify_anchor_propagation.py \
  | cmp - EXPECTED_OUTPUT.txt
```

Expected output is

```text
PASS exact row/column formulas on 7 matrices and 294 vertex profiles
PASS exact one-cross-flip updates on 14 flips and 588 vertex profiles
PASS all test matrices satisfy cross cardinality and first-degree bounds
PASS split degree deviations equal M-220 and M-221
PASS first-degree-feasible test weights=99,...,111 exceed hard limit 39
PASS hard split degree-profile counts=1,5,17,40,69,95,122 total=349
PASS first-degree-feasible tests have 0 secondary exact anchors
PASS side anchor minima A=13,11,9,7,5,3,1 B=12,10,8,6,4,2,0
PASS hard branch forces secondary exact anchors=27,26,25,24,23,22,21
```

The audit uses CPython 3.11 or later, the standard library, exact integer
arithmetic, and no solver, randomness, floating point, network, or external
data.  It took about 1.3 seconds under CPython 3.11.2 on the research host.

## Scope, provenance, and trust boundary

The formulas are elementary partitions and are checked independently against
the definition of a local color-neighborhood.  The count of nine secondary
anchors imports the companion
[`ramsey_r55_local_extremal_deficiency`](../ramsey_r55_local_extremal_deficiency)
theorem, including its stated trust in the completeness of the pinned McKay
`(4,5)` extremal catalogs.  The anchored representation and mixed-clique
constraints come from
[`ramsey_r55_doubly_exact_cross_normal_form`](../ramsey_r55_doubly_exact_cross_normal_form).

Discovery Net was searched through indexed height 2034 for the `R(5,5)`
problem neighborhood and for cross-matrix, transversal, covering, local, and
deficiency results.  It contained extensive cyclic-search and one-vertex
extension work, but no two-core local-count propagation statement.  Novelty
is asserted only relative to that search; no historical-priority claim is
made.
