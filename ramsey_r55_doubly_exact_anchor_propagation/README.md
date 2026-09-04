# Propagation constraints from a doubly exact `R(5,5;43)` anchor

This directory strengthens the companion 21-by-21 cross-matrix normal form.
In the hard branch of the local-deficiency dichotomy, fixing one doubly exact
vertex does not merely fix two `(4,5;21,100)` cores.  The cross matrix also
determines the order and edge count of both color-neighborhoods at every one
of the other 42 vertices.  All 84 of those local graphs must have deficiency
at least seven, and at least nine of the 42 vertices must reproduce the same
doubly exact signature as the chosen anchor.

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

There is also a global propagation condition:

```text
at least 9 vertices u in A union B satisfy
       (d_u, t_R(u), t_B(u)) = (21,100,100).             (P9)
```

The local-deficiency theorem forces at least ten doubly exact vertices in the
hard branch.  The selected `v` is one of them, so at least nine remain.  A
vertex is doubly exact exactly when its displayed triple is `(21,100,100)`:
red degree 21 makes both local orders 21, and the two local edge counts are
then seven below `U(21)=107`.  Thus `(P9)` follows without choosing or labeling
the other anchors in advance.

For a hard-branch cross search, `(D7)` and `(P9)` are lossless.  A general
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
bounds, but have no secondary doubly exact vertex and violate `(D7)`.  They
are deliberately not claimed to satisfy the mixed-`K_5` clauses.  Their role
is a regression witness that the new tests contain information absent from
the inexpensive cardinality/degree filter, not evidence about feasibility.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 verify_anchor_propagation.py \
  | cmp - EXPECTED_OUTPUT.txt
```

Expected output is

```text
PASS exact row/column formulas on 7 matrices and 294 vertex profiles
PASS exact one-cross-flip updates on 14 flips and 588 vertex profiles
PASS all test matrices satisfy cross cardinality and first-degree bounds
PASS first-degree-feasible tests have 0 secondary exact anchors
PASS hard branch propagates 84 deficiency inequalities and at least 9 anchors
```

The audit uses CPython 3.11 or later, the standard library, exact integer
arithmetic, and no solver, randomness, floating point, network, or external
data.  It takes well under one second.

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
