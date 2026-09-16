# Exact equilateral-`sqrt(2)` triple-lens orbit stop

This directory certifies one frozen plane unit-distance construction for the
Hadwiger--Nelson sub-509 campaign. It is a **scoped negative result**, not a
record candidate.

Take three independent centres forming an equilateral triangle of side
`sqrt(2)`. For each centre pair, include both common points of its two unit
circles. Around each of the two owners of each common point, close the
corresponding unit direction under all six rotations through 60 degrees. The
raw architecture has

```text
3 + 3 centre pairs * 2 intersections * 2 owners * 6 rotations = 75
```

formal addresses, so its physical order was capped before any colour query.
Exact collision merging and a complete all-pairs unit-distance reconstruction
give:

- 33 distinct physical points and 78 unit edges;
- 3 points of provenance multiplicity 1, 24 of multiplicity 2, and 6 of
  multiplicity 4;
- one connected component, no articulation vertex, and no bridge;
- the entire 33-point graph in the 3-core and 9 points in the 4-core;
- chromatic number exactly **3**; and
- every canonical four-colour pattern `000,001,010,011,012` on the three
  independent centres extends to the complete graph.

Thus the unrestricted centre relation is exactly the neutral relation of
three independent vertices. The construction fails the campaign's first
chromatic gate and is retired without changing the centre separation, adding
another orbit shell, or selecting a subset of the closure.

## Exact arithmetic

A row `(a,b,c,d)` represents

```text
(a*sqrt(2) + b*sqrt(6)) + i*(c*sqrt(2) + d*sqrt(6)).
```

The centres are

```text
0,
sqrt(2),
sqrt(2)/2 + i*sqrt(6)/2.
```

For centres `p,q` at distance `sqrt(2)`, their two unit-circle intersections
are

```text
(p+q)/2 + i*(q-p)/2,
(p+q)/2 - i*(q-p)/2.
```

For a coordinate difference `(a,b,c,d)`, squared distance has rational and
`sqrt(3)` coefficients

```text
(2*a^2 + 6*b^2 + 2*c^2 + 6*d^2,
 4*a*b + 4*c*d).
```

It is a unit pair exactly when those coefficients are `(1,0)`. The checker
uses this test on all 528 physical pairs. The closed-form colouring

```text
colour(a,b,c,d) = 4*c mod 3
```

is a proper three-colouring; all generated `c` have denominator dividing
four. The stored triangle `[0,3,8]` supplies the matching lower bound.

## Reproduction

Python 3.11 or later and the standard library suffice:

```sh
python3 -B verify.py
python3 -O -B verify.py
python3 -B controls.py
sha256sum -c SHA256SUMS
```

`verify.py` independently regenerates the 75 formal addresses, merges exact
coordinates, checks all physical pairs, verifies the formula colouring and
triangle, and checks literal extensions for the five canonical centre
patterns. `controls.py` confirms that malformed positive witnesses and altered
expected invariants are rejected.

## Scope

The result concerns only this equilateral-`sqrt(2)` frame and its complete
first sixfold lens-orbit closure. It does not classify other centre triangles,
later shells, selected circle points, or arbitrary graphs dominated by three
vertices. It is distinct from the previously closed equilateral-`sqrt(3)`
orbit collapse and is not a strengthening of the general open-collar theorem.

