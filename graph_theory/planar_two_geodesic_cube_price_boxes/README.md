# Half separators throughout two radial price boxes

Two explicit **24-dimensional boxes of radial edge prices** admit
half-balanced separators made of at most two ambient geodesics in the
distributed-shortcut cube construction below. All six shortcut-edge
lengths are independently arbitrary and nonnegative, all `4^9` cheap-parent
choices are permitted, parent-edge lengths are arbitrary and positive,
and masses are arbitrary on nine specified marks. A common positive
scaling of either box is also allowed.

This replaces a fixed core-price test by a proved region of core-price
space. It excludes a weighted construction strategy for
[Barbados 2026 Problem 31](https://web.math.princeton.edu/~pds/barbados26/problems.pdf);
it does not resolve the unrestricted unweighted problem. The full radial
shortest-path cones outside these boxes remain unresolved by this work.

## Construction and exact claim

Label the cube vertices `0,...,7` by their three binary coordinates. The
face with coordinate `a` equal to `b` has center `8+2a+b`. The twelve cube
edges, in lexicographic endpoint order, have centers `14,...,25`. Join
each edge center to its two endpoints and two incident face centers, and
join every cube vertex to its incident face centers. This is the
barycentric cube triangulation `T`: 26 vertices, 72 edges, 48 triangles.
Its 24 radial edges `R` are, in order:

```text
(0,8) (0,10) (0,12) (1,9) (1,10) (1,12)
(2,8) (2,11) (2,12) (3,9) (3,11) (3,12)
(4,8) (4,10) (4,13) (5,9) (5,10) (5,13)
(6,8) (6,11) (6,13) (7,9) (7,11) (7,13)
```

Let `p` be one of these price vectors:

```text
A: 14 38  7 23 20 17  8 30 11 21 14 29 10 28 36  4  3  7 30  6  2  4  9  5
B:  7 10  4  8  7 11  9  6 16 14  3 23  3 16 15 16  3 10 22  9 12  3 12  7
```

Set `rho_A=1/57` and `rho_B=1/32`. For some `lambda>0`, independently
choose every radial edge length `w_e` in the closed interval

```text
lambda (1-rho) p_e <= w_e <= lambda (1+rho) p_e.
```

Thus A permits approximately ±1.75% and B permits ±3.125% variation in
**each** coordinate, with no additional condition on the choices.

Make the edge centers `14,19,22` zero-mass shortcut vertices. Add to `R`
the following six edges, each of arbitrary nonnegative length:

```text
(10,14) (10,22) (11,19) (12,14) (12,19) (13,22).
```

They form the path `11–19–12–14–10–22–13` through four face centers. Write
`H` for this 17-vertex, 30-edge core. The marked set is

```text
M = {15,16,17,18,20,21,23,24,25}.
```

For every `z` in `M`, select any one of its four neighbors `p(z)` in `T`
and add `z p(z)` with any positive length. This gives a connected spanning
subgraph `Q` with 39 edges. Every remaining edge `uv` of `T` has positive
length satisfying `length(uv)>=d_Q(u,v)`. In particular, making all these
remaining edges longer than the sum of all lengths in `Q` suffices.

**Claim.** For every nonnegative vertex-mass assignment supported on `M`,
the full graph `T` has a separator equal to the union of at most two
ambient shortest paths, leaving each component with at most half the
total mass. All 72 edges of `T` count for residual components. When some
shortcut lengths are zero, a geodesic means a simple minimum-cost path.

The same conclusion also holds when every radial edge has the same
positive length (the unit case U up to scale), with the same distributed
shortcuts and marked set.

## Isometry, leaf endpoints and mass

Replacing every edge outside `Q` in a `T` walk by a shortest `Q` path
never increases its length. Hence `d_T=d_Q`: a certified `Q` geodesic is
an ambient geodesic, even when equality holds in the outside-edge bound.
This condition was highlighted in the
[review of the single-shortcut construction](../planar_two_geodesic_zero_mass_cube_shortcut_review1/REVIEW.md).

Every mark is a leaf in `Q`. Its positive parent-edge length occurs
identically in any comparison of paths with that endpoint and cancels.
This accounts for all parent-edge lengths without sampling them. Divide
all edge lengths by `lambda` to normalize the radial box.

A **four-residue pair** leaves at most four marks in every full-graph
component. Such a geodesic pair suffices for all marked masses: if the
four heaviest marks carry at least half the total mass, pair them by two
ambient geodesics and delete at least half. Otherwise every set of at
most four marks is light. Total mass zero is included. The certificates
below establish four-residue pairs before this mass step is applied.

## A whole box with a fixed radial shortest-path pattern

For either baseline `p`, all radial geodesics are unique. Let `P_sv` be
the baseline path from radial vertex `s` to radial vertex `v`, and let
`D_s(v;w)` be its length at variable radial prices `w`. For every directed
radial edge `uv`, form the homogeneous linear expression

```text
L_suv(w) = D_s(u;w) + w_uv - D_s(v;w).
```

The identically zero expressions are exactly the forward edges in the
rooted baseline shortest-path trees. At `p`, every other expression is
strictly positive. Requiring all the nonzero expressions to remain
positive defines an open, full-dimensional cone of positive radial
prices. It preserves every baseline radial geodesic uniquely: telescope
the potential inequalities along a competing path. A different path
must use a directed edge outside the reference tree, contributing a
strictly positive slack. There are 205 distinct nonzero expressions for
A and 199 for B.

If `L(w)=sum_e a_e w_e`, a relative box of radius `rho` satisfies

```text
L(w) >= L(p) - rho sum_e |a_e| p_e.
```

The exact minima of `L(p)/(sum_e |a_e|p_e)` over these expressions are
`1/57` for A and `1/32` for B. The verifier reconstructs all paths and
expressions and calculates both minima with rational arithmetic.
Consequently every point of the stated closed box lies in the closure
of its radial cone. Interpolation toward `p` enters the strict cone
while staying in the box. These radii are the limits of the **radial
pattern box calculation**, not claimed sharp bounds for half balance.

## Exact proof inside each price box

First take positive shortcut lengths and radial prices in both the box
and the strict cone. Every geodesic in `H` has each maximal radial-only
segment shortest in `R`: replacing a nonshortest segment gives a shorter
walk, and removing positive cycles gives a shorter path. The unique
radial paths throughout the cone are the baseline paths.

The checker generates simple core paths by direct DFS, pruning only
a radial segment that is not shortest at the baseline. It therefore
retains **every** possible `H` geodesic in the strict cone, including
ties involving shortcuts. The catalogs have 1,176 routes for A and
1,226 for B, over all unordered core endpoint pairs and including
singletons. Nongeodesic extra routes in a catalog do no harm.

All 30 core-edge lengths are real variables. A catalog path is geodesic
if and only if no competing catalog route with the same endpoints is
strictly shorter. This is a finite conjunction of linear comparisons.
For each proposed path pair, the checker verifies its edges, simplicity,
parent requirements and full-graph component counts. It then adds the
clause saying the pair is unavailable: some required parent is absent,
or a strictly shorter competitor exists for one of the paths.

The domain includes positivity of all 30 variables, the radial-cone
inequalities, all 48 closed box inequalities, and exactly one parent
per mark. The two compact certificates prove these domain constraints
inconsistent with the unavailability of every listed pair:

| Box | Pair templates | Base clauses | Linear atoms | Rational Farkas lemmas | RUP additions |
|---|---:|---:|---:|---:|---:|
| A, radius `1/57` | 47 | 393 | 599 | 437 | 48 |
| B, radius `1/32` | 67 | 407 | 659 | 723 | 142 |

An atom represents `f>=0`, with its negative literal meaning `-f>0`.
Each arithmetic lemma gives positive rational multipliers whose weighted
sum has zero variable coefficients and either a negative constant or
a zero constant with a strict summand. The conjunction is impossible,
so its negation is a valid clause. The verifier checks every identity
exactly and then replays reverse unit propagation (RUP) to the empty
clause. No SMT or SAT solver is required for verification.

Thus some four-residue pair is geodesic for every strict-cone point in
the box and every parent assignment. The outside-edge and mass reductions
give the required half separator.

## Closed box boundaries and zero shortcut lengths

Fix any parent assignment and parent-edge lengths. Approach a closed-box
point `w` by `w(t)=(1-t)w+tp`, with `t>0`, and add `t` to every shortcut
length. The new radial prices lie in the strict cone and the same box;
all shortcut lengths are positive. The certified conclusion applies.

There are finitely many simple path pairs, so one geodesic four-residue
pair occurs along a sequence with `t` tending to zero. Path costs are
continuous; shortest-path distances in a finite nonnegative-edge graph
are minima of finitely many continuous simple-path costs. This pair is
therefore geodesic in the limiting `Q`. Its residual components in the
fixed topology `T` are unchanged. Finally apply the outside-edge condition
at the limit to transfer its geodesicity to the given ambient `T`.

This uses the finite-pair limiting argument from the
[independent review of the coupled-shortcut result](../planar_two_geodesic_coupled_cube_shortcuts_review1/REVIEW.md),
now also allowing radial prices to approach a shortest-path tie. It
does not assume that the same pair works on the whole box.

## The unit radial case

Set all six shortcut lengths to zero to obtain a lower-bound pseudometric
`d_0` on `H`. Each radial-only path below attains `d_0` between its radial
endpoints, so remains geodesic for every nonnegative shortcut vector.
Append the forced leaf edge when mark 15 is an endpoint. According to
the parent of 15, these four pairs cover every parent assignment:

| Parent of 15 | First path | Second path | Residual marked counts |
|---|---|---|---|
| 0 | `8,6,11,7,9` | `15,0,10,5,9` | `4,4` |
| 2 | `8,4,10,5,9` | `15,2,11,7,9` | `4,4` |
| 8 | `15,8,0,10,1,9` | `15,8,6,13,7,9` | `4,4` |
| 12 | `8,6,13,5,9` | `15,12,3,9` | `4,4` |

The checker calculates `d_0` directly with zero edges and recomputes all
components in the full triangulation. No logical solver proof is needed
for this four-case table.

## Reproduction and scope

From the repository root, use Python 3.11 or later, the standard library,
and assertions enabled:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 graph_theory/planar_two_geodesic_cube_price_boxes/verify.py
```

The program checks the sphere fixture, the radial patterns and exact box
radii, both rational/RUP certificates, and the unit table. It prints
`status: PASS`, the counts above, and SHA-256 hashes of all three
certificates. The two region certificates are 65,416 and 104,341 bytes.
No network access, external solver, generator, or large search output
is needed; the program writes no files.

The discovery implementation used an independent decomposition into up
to three ordered and oriented shortcut links, joined by radial geodesics.
Its route sets were compared entry by entry against the checker's DFS
sets. SMT found candidate parameter choices and separators; exact Farkas
and Boolean proofs were then extracted, reduced and replayed. None of
the discovery routines or solver proof parsers is imported by `verify.py`.
The full mathematical claim still uses the written pattern, completeness,
continuity, isometry and mass arguments above. This is an exact
computer-assisted result with a separate checking implementation, not
independent peer review or a proof-assistant formalization.

The unbounded A and B radial cones were also searched. Both runs ended
UNKNOWN at their solver limits, after finding separators for 453 and
437 parameter/parent models respectively. Those observations prove
neither cone-wide exclusion nor a counterexample. The boxes are the
proved region. Arbitrary radial prices, arbitrary mass outside `M`,
other shortcut geometries, and an unweighted subdivision transfer remain
outside the claim.

The earlier [central coupled-shortcut construction](../planar_two_geodesic_coupled_cube_shortcuts/README.md)
uses zero-mass centers `14,15,16`, whereas this one uses `14,19,22`.
Their marked supports differ, so the earlier result does not contain
this statement or conversely. The new boxes address the reviewers'
request to go beyond isolated radial price vectors.

Primary sources were refreshed at the start of this pass on 2026-09-28.
The [workshop schedule](https://web.math.princeton.edu/~pds/barbados26/schedule.html)
announces a disproof of a Codsi conjecture without the precise statement
or witness needed to identify it with Problem 31. No historical-priority
or current-general-status claim is made here.
