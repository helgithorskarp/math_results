# Common-neighbour phase sumsets: a geometry-first sub-509 search

This package records a bounded Hadwiger--Nelson construction search outside
the Parts and A5 families.  It does **not** contain a five-chromatic graph and
does **not** improve the 509-vertex record.  Its purpose is to close one
natural physical architecture cleanly enough that the construction lane can
pivot without later mistaking the same restricted negative result for global
progress.

## Record and scope

The live literature check on 2026-09-13 found that Parts' strict plane
unit-distance graph on 509 vertices and 2442 edges remains the published
order record.  Haugland's 2026 graph has 2131 vertices and improves the
Moser-spindle-free record, not the unrestricted vertex record.  URLs and the
precise claims used here are in `SOURCE_PINS.json`.

Every support in this package is generated from plane coordinates before its
chromatic number is tested.  No abstract graph is treated as a construction
candidate.

## Architecture

Put

```
omega = exp(pi*i/3),       U = <omega>,
rho   = (5+i*sqrt(11))/6,  eta = exp(pi*i/6).
```

For a finite set `D` of unit directions and unit centres `C`, the basic
support is

```
X(C,D) = {0} union C union {c+d : c in C, d in D}.
```

Thus `0` is a genuine common unit neighbour of every centre and every rim
point is a genuine point of a unit circle about its owner.  The natural four
centres `{1,omega,rho,rho*omega}` already contain a Moser spindle in the
39-point two-phase support, so that support is exactly four-chromatic.

The mixed all-centre variant takes `C=D` with

```
D(S) = union_{(k,e) in S} rho^k eta^e U,
```

and hence has an exact realization in
`Q(sqrt(3),sqrt(11),i)`.  Global phase rotation lets the search normalize
`(0,0) in S`.

## Results

The following are restricted-family results only.

1. **Exact two-phase quartet boundary.**  For
   `D=U union rho*U`, all `binom(12,4)=495` choices of four centres were
   reconstructed using exact arithmetic.  Every strict graph is
   four-colourable; 483 are not three-colourable.  The natural case has 39
   vertices and 111 edges.

2. **Exact power ladder through the record boundary.**  With the natural four
   centres fixed and `D=union_{0<=k<=K} rho^k U`, every `1<=K<=20` member is
   explicitly four-colourable.  Its order is `24*K+15`, so `K=20` has 495
   vertices and 1251 edges.  The next member has 519 vertices.  The linear
   edge and vertex increments show that pure orbit accumulation contributes
   no new cross-layer forcing in this ladder.

3. **Physical circle-intersection closure screen.**  Starting from each of
   the 495 two-phase quartets, two rounds add every intersection between an
   owner unit circle and a unit circle about every current point.  All 495
   resulting physical supports (at most 303 vertices) have directly checked
   four-colour words.  This is a floating-point discovery screen, not an
   exact theorem; the smallest observed nonedge gap from unit distance was
   about `3.14e-5`.

4. **Mixed phase screen.**  The normalized searches tested 528 three-orbit
   sets (`|k|<=8`), 680 four-orbit sets (`|k|<=4`), and 715 five-orbit sets
   (`|k|<=3`).  Every support was physically formed as `X(D,D)` and had a
   checked four-colour word, with no timeout.  Maximum orders were 163, 289,
   and 451 respectively.  The coordinates are exact algebraic expressions,
   but edge discovery in this broad screen used double precision; the
   smallest observed nonedge gap was about `2.51e-5`.  These 1923 cases are
   therefore reproducible experimental exclusions, not a formal whole-family
   theorem.

Six generic phase orbits give 649 vertices, above the target.  Together these
tests meet the predeclared pivot condition: neither choosing another quartet,
adding pure Moser-angle layers, taking two rounds of complete physical circle
closure, nor using up to five mixed phase orbits produced a sub-509
non-four-colourable support.

## Interpretation and next move

This does not exclude arbitrary common-neighbour constructions, arbitrary
phase sets, or any graph outside the tested supports.  In particular, a
positive result from a numerical script would still require exact coordinate,
strict-edge, distinctness, and non-four-colourability certificates.

The observed failure mode is useful for construction design: orbit layers
that only attach translated six-cycles enlarge a fixed four-chromatic core
without increasing its colour demand.  A successor architecture should add
selected points whose unit incidences couple *different* translate layers,
or should abandon the common-neighbour sumset form entirely.  Merely widening
the exponent window is not a credible next pass.

## Files

- `scratch_common_neighbor_sumsets.py`: exact 495-quartet sweep.
- `scratch_common_neighbor_power_ladder.py`: exact natural-centre ladder.
- `scratch_fixed_circle_closure_sweep.py`: two-round physical closure sweep.
- `scratch_mixed_phase_sumset_search.py`: normalized mixed-phase screen.
- `scratch_fixed_circle_geometric_closure.py`: one-seed closure diagnostics.
- `scratch_four_circle_moser_layers.py`: exact field/DSATUR library and the
  rejected first four-circle pilot.
- `EXPECTED.json`: compact expected summaries.
- `REPRODUCE.md`: commands and trust boundaries.

