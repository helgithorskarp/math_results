# Exact mass duality for a finite menu of geodesic pairs

Several positive approaches to [Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf)
first certify a **fixed menu** of ambient geodesic pairs and then argue that
one of them half-balances every assignment of vertex masses. The
[icosahedron price-region certificate](../planar_two_geodesic_icosahedron_price_region/README.md)
is a recent example. This note removes the universal real-mass quantifier
exactly: each menu either has a bounded integer counterweight, or every
possible selection of one residual component per pair has a bounded integer
dual certificate. The result applies to arbitrary finite graphs and fixed
vertex-deletion menus; the metric matters only when validating that the menu
sets are unions of at most two ambient geodesics.

## Finite-menu alternative

Let `G` have `n>=1` vertices and let `S_1,...,S_t` be a nonempty finite menu
of vertex sets. In separator applications, each `S_i` is the union of at
most two paths already checked to be geodesics in **the original graph**.
Write `R_i` for the family of vertex sets of connected components of
`G-S_i`. A nonnegative mass vector `w` has total `W=sum_v w_v`; `S_i` is
half-balanced when every `C in R_i` has `2w(C)<=W`.

**Theorem.** The following are equivalent.

1. For every nonnegative real mass vector `w`, some `S_i` is half-balanced.
2. For every tuple `(C_1,...,C_t)` with `C_i in R_i`, there are
   nonnegative **integer** numbers `a_1,...,a_t`, of positive total `A`, such
   that

       2 sum_(i: v in C_i) a_i <= A       for every vertex v.          (D)

   They can be chosen with at most `n+1` positive entries and with

       A <= b! 2^(b-1),       b=min(t,n+1).                          (B)

If one `R_i` is empty, `S_i` deletes every vertex and both conditions hold;
condition 2 then has no tuples to check. Otherwise the alternative is
two-sided: if condition 1 fails, there is a **positive integer** mass vector
with each entry at most `n!` for which every menu set fails half balance.
Thus a fixed menu has compact, exact certificates on both sides. It is not
claimed that the number of component tuples is small.

For a fixed edge metric, taking the menu to be **all** unions of at most two
ambient geodesics makes the positive-integer counterweight a genuine
weighted obstruction on that graph. Conversely, dual certificates for all
tuples prove the weighted half-separator property for that fixed metric.
The theorem alone gives no uniform result across all planar graphs or edge
metrics.

## Proof by a finite matrix game

Fix one component tuple `C=(C_1,...,C_t)` and normalize nonzero masses by
`sum_v w_v=1`. Let `M_iv=1` if `v in C_i`, and `0` otherwise. The maximum
simultaneous residual mass is

    alpha(C) = max_(w in Delta(V)) min_i sum_v M_iv w_v.

The finite matrix-game minimax theorem, or elementary linear-programming
duality, gives

    alpha(C) = min_(lambda in Delta([t])) max_v sum_i lambda_i M_iv.   (1)

The maxima and minima are attained because both simplices are compact.
There is a mass vector making **all** `C_i` strictly heavier than half
exactly when `alpha(C)>1/2`. By (1), no such vector exists exactly when
some probability vector `lambda` satisfies

    2 sum_(i:v in C_i) lambda_i <= 1        for every v.              (2)

For every `w`, a menu set fails precisely when at least one of its residual
components is strictly heavier than half. Therefore all menu sets fail for
some `w` precisely when **some** component tuple has all its sets heavy.
This establishes the real-valued equivalence, including masses with zeros.
The all-zero mass vector is balanced by every menu set and causes no issue.

It remains to bound exact integers. The feasible vectors in (2) form a
closed polytope inside `Delta([t])`. Choose a vertex with `s` positive
coordinates. On that support, the equation `sum lambda_i=1` and at most
`n` tight vertex inequalities must pin down all `s` coordinates, so
`s<=min(t,n+1)=b`. Choose `s` independent tight rows. Their integer matrix
has one all-one normalization row and `s-1` rows with entries `0` or `2`;
the right-hand side is all ones. Cramer's rule gives rational coordinates
with a common positive denominator `D`, the absolute basis determinant.
Each term of its Leibniz expansion has absolute value at most `2^(s-1)`,
so `1<=D<=s!2^(s-1)<=b!2^(b-1)`. Multiplying `lambda` by `D` gives (D)
and (B), with `A=D` because its coordinates sum to one.

If condition 1 fails, choose for each `i` a strictly heavy component
`C_i`. The strict inequalities are preserved by a small perturbation to
positive masses, followed by scaling so that

    w_v>=1,       2w(C_i)-sum_v w_v>=1            for all v,i.        (3)

This polyhedron is nonempty. Minimize `sum_v w_v`, take a vertex, and choose
`n` independent tight rows. Their coefficients are in `{-1,0,1}` and
their right-hand sides are all one. The same Cramer argument, now in
dimension `n`, scales the vertex to positive integer masses at most `n!`
per vertex while preserving (3). Every `C_i` stays heavy. `□`

## A genuinely fractional seven-pair control

Use the seven nonzero vectors of `F_2^3` as vertices of the **nonplanar**
unit-edge graph `K_7`. Its seven Fano lines are the sets
`{a,b,a xor b}` for distinct nonzero `a,b`. For each line `C_i`, pair the
four vertices outside it into two edges and let `S_i` be their union.
Each edge is an ambient geodesic, and `G-S_i` has the one component `C_i`.

Every vertex lies on exactly three lines. Taking `a_i=1` for all seven
lines satisfies (D) with `2*3<7`. Thus **the same seven prescribed pairs**
half-balance `K_7` for every nonnegative mass vector; in fact one leaves
mass at most `3W/7`. Every two Fano lines intersect, so no certificate
using only a pair of disjoint heavy-component candidates is available for
this menu. An exact basis search also finds a four-line certificate with
unit coefficients; four is the least possible support size here. Indeed,
two chosen lines meet, while three either meet at one point or have three
pairwise intersections whose three half-bound inequalities sum to the
impossible `2<=3/2`. This illustrates the extra reach of fractional
certificates, not a planar positive class or a counterexample to Problem 31.

As a negative set-system control, the three sets `{0,1}`, `{1,2}` and
`{0,2}` have no dual certificate: unit masses give every set mass `2>3/2`.
Their pairwise intersections do not prevent a simultaneous strict majority.

## Reproduction and scope

From the repository root, with Python 3.11 or later and no external
packages:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_mass_menu_duality/verify.py
```

The checker independently generates the Fano lines and the seven prescribed
`K_7` path pairs, checks each pair against full-graph distances and
components, enumerates exact rational bases to find dual or primal integer
certificates, and tests all `3^7` mass vectors with entries in `{0,1,2}`.
It also checks all `8^3=512` three-set systems on three vertices against
an independent brute search of positive masses bounded by `3!`. Its exact
output is:

```text
Fano lines and sampled mass vectors: (7, 2187, (1, 1, 0, 1, 0, 0, 1))
strict-majority sets: (3, (1, 1, 1))
three-by-three systems (dual, primal): (337, 175)
PASS
```

The arbitrary real-mass theorem follows from the written
minimax and determinant proof, not from that enumeration. No planarity or
unrestricted Problem 31 conclusion is inferred from `K_7`. Historical
priority for this elementary LP formulation is not asserted.
