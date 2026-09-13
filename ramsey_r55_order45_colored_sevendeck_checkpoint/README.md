# Order-45 colored seven-deck checkpoint (no certified bound)

## Status

This package does **not** certify an occurrence bound and does **not** improve
the published range for `R(5,5)`.  It preserves a complete symmetry-free
order-seven occurrence relaxation, its exact rational LP, positive controls,
and the failed solver attempts needed to resume or change the approach.

An unnormalized HiGHS run reported infeasibility, but the exactly equivalent
probability-normalized model did not reproduce that conclusion: normalized
primal and dual runs reached their time limits, and no Farkas ray was found.
The unnormalized status is therefore treated as a numerical artifact, not as
mathematical evidence.

## Mathematical model

Fix a hypothetical good graph `G` on 45 vertices and a degree-24 root `r`.
Color the 24 vertices in `H=N(r)` by `H` and the remaining 20 vertices in
`X` by `X`.  Edges in every type are edges of `G`.

For each valid colored graph type `T` on at most seven vertices, let `p_T` be
the probability that a uniformly chosen color-respecting vertex subset
induces `T`.  Types are excluded exactly when they contain one of the
following forbidden configurations:

- a `K4` wholly in `H` (it forms a `K5` with `r`);
- an independent four-set wholly in `X` (it forms an independent five-set
  with `r`);
- a `K5` or independent five-set in the colored type itself.

The variables obey exact one-vertex deletion equations.  If `T` has `a`
`H`-vertices and deleting its `H`-vertices gives a lower type `S` with total
multiplicity `d_H(T,S)`, then

```
sum_T d_H(T,S)/a * p_T = p_S.
```

The analogous identity holds for `X` deletions.  These equations are purely
incidence-counting identities and use no automorphism assumption.

The ten pure-`H` four-type probabilities are constrained to the exact convex
hull of the four-decks of the complete catalogued `(4,5,24)` tail with at
least 126 edges.  The imported tail contains 15,913 graphs in 10,009 distinct
four-deck rows.  Finally, if `Y=G[X]` and `Q` is its complement, the classical
order-20 edge range `68 <= e(Q) <= 100` becomes

```
9/19 <= p_(X-edge) <= 61/95.
```

Consequently every dense order-24 graph that actually occurs as a degree-24
neighborhood supplies a feasible point of this LP.  Infeasibility, if proved
exactly, would imply `beta(24) <= 125`; by complementation the same statement
covers a dense order-24 complementary nonneighborhood at a degree-20 root.

## Enumeration and model size

`colored_types.cpp` canonically enumerates colored isomorphism types under
`S_a x S_(n-a)`.  The order-seven counts for `a=0,...,7` are

```
627, 3848, 11314, 18726, 18726, 11314, 3848, 627.
```

There are 74,332 colored types through order seven.  With the dense-tail
selectors, the complete LP has:

```
84,341 nonnegative variables
10,617 equalities
2 inequalities
574,669 nonzero coefficients
```

`colored_sevendeck_normalized.lp` contains literal rational coefficients.
SoPlex 9.0.0 read it in rational mode and confirmed the above dimensions.

## Controls and failed decision attempts

- The normalized order-six model is feasible at the expected relaxation
  value `e(H)+e(Q)=232`.
- Every tested single, pair, triple, and central four-composition order-seven
  subsystem is feasible at 232.  In particular the `a={2,3,4,5}` subsystem
  is feasible, so any real obstruction must couple a wider set of color
  compositions.
- The complete normalized HiGHS optimization and pure-feasibility runs timed
  out without a primal point or a dual certificate.
- SoPlex 9.0.0 with exact rational input/check mode, Devex pricing, and a
  900-second limit stopped after 68,290 iterations without a decision.  A
  Harris-ratio variant stopped after 93,391 iterations, also without a
  decision.

The logs are retained to prevent the unnormalized false-positive status from
being mistaken for a theorem.

## Reproduction

Build the type table:

```bash
g++ -O3 -std=c++17 colored_types.cpp -o colored_types
./colored_types > colored_types7.tsv 2> colored_types7.meta
```

Run the normalized order-six control and export the exact full LP:

```bash
python colored_fivedeck_lp.py --order 6 --normalized --method highs-ipm
python colored_fivedeck_lp.py --order 7 --types-file colored_types7.tsv \
  --normalized --zero-objective --export-lp colored_sevendeck_normalized.lp
```

The Python environment used SciPy 1.16.3 and HiGHS 1.15.1.  The exact-backend
run used SoPlex commit `7418b737e675b0f533e8743c2992763c318a911b`,
compiled with Boost 1.74.0 and GMP 6.2.1:

```bash
soplex -v4 -t900 -p3 --readmode=1 --solvemode=1 -c \
  colored_sevendeck_normalized.lp
```

## Imported trust boundaries

- Completeness of the `(4,5,24)` catalogue and of its 15,913-member
  `e>=126` tail is imported.
- The classical `(4,5,20)` edge range, in particular `e(Q)<=100`, is
  imported.
- `scan24e126plus.tsv` is the previously checked aggregate tail table; the
  model asserts its row count, multiplicity sum, order, edge range, and
  forbidden-`K4` column.
