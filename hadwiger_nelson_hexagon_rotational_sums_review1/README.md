# Independent review of all rotational sums of two 19-point hexagons

Verdict: **accepted and independently verified**.  Let

```text
H = {(a,b) in Z^2 : max(|a|,|b|,|a+b|) <= 2},
omega = (1+i sqrt(3))/2.
```

For every complex unit `u`, the strict unit-distance graph on the physical
point set `H + uH` has chromatic number 3 or 4.  There are exactly 174
exceptional rotations, in 15 orbits under multiplication by `omega` and
complex conjugation.  Eleven orbits (126 rotations) are 3-chromatic and four
orbits (48 rotations) are 4-chromatic.  Every nonexceptional rotation is
3-chromatic.  Exceptional physical orders are 61, 271, 349, and 361; a
generic graph has 361 vertices and 1,596 edges.

This is a complete classification of this one continuum family, but it is a
negative family result.  It does **not** construct a five-chromatic graph,
improve the 509-vertex record, or show that a related asymmetric or augmented
Minkowski-sum family cannot improve that record.

Reviewed Discovery Net contribution:
`bafkreihbz4cv4ikfxrino5h2u3wjg2ykoij5jexkj26vba4c4acoop2ypy`, source
commit `209c7380cb9d83ee825f12593259aa584cf92d1d`.  The reviewed certificate has
SHA-256
`9fd7e3c6883ce823af804b8bbc3dbbf1f4f7a819157e7f3a9925825c7925bac8`.

## Independent derivation of the exceptional set

The review checker imports no target code and does not use the target's
half-angle polynomial.  Write nonzero triangular-lattice differences as
`d,e`, put `m=|d|^2`, `n=|e|^2`, and write

```text
d conjugate(e) = (p + i sqrt(3) q)/2,
u = X + i sqrt(3) Y.
```

Then `p^2+3q^2=4mn=:D`, while an additional strict unit edge is equivalent to

```text
pX + 3qY = c := 1-m-n,       X^2+3Y^2=1.
```

Directly intersecting this line with the unit ellipse gives, for
`Delta=D-c^2 >= 0`,

```text
X = pc/D -/+ q sqrt(3 Delta)/D,
Y = qc/D +/- p sqrt(3 Delta)/(3D).
```

Exact square-free reduction of these coordinates over all 60 by 60 ordered
nonzero difference pairs produces 174 distinct rotations.  The check finds
2,304 feasible circle-line pairs and 216 tangent pairs.  Expanding the 15
certificate representatives under the two symmetries gives exactly this set,
with one orbit of size 6 and fourteen of size 12.

A label collision has the form `d+ue=0`, hence `m=n` and
`u=-(p+i sqrt(3)q)/(2n)`.  The checker separately enumerates all 30 collision
rotations and verifies that they lie in the 174-event set.  This also has a
short geometric explanation: if two labels coincide, choose a unit neighbour
of one first-coordinate label distinct from the other label (each point of
`H` lies in a triangle); comparing it to the coincident alternate label gives
an additional unit-edge event.  Thus outside the finite event set there are
neither extra edges nor collisions, and the physical graph is exactly the
Cartesian product `H square H`.

## Chromatic lower and upper bounds

The residue `q(a,b)=a-b mod 3` properly 3-colours `H`.  A complete backtracking
enumeration with one triangle fixed finds exactly one 3-colouring of `H`, so
`H` is uniquely 3-colourable up to a palette permutation.

This yields a compact classification of every 3-colouring of `H square H`.
On each `H`-layer a colouring must be a palette permutation of `q`.  Palette
permutations on adjacent layers differ by a fixed-point-free permutation,
which on three colours is a 3-cycle.  All layer permutations consequently
have the same parity and are cyclic shifts of one another.  Their shifts form
a proper 3-colouring of the second `H`, so uniqueness there leaves, up to a
global palette permutation, precisely

```text
q(x)+q(y) mod 3       or       q(x)-q(y) mod 3.
```

Every 3-colouring of a physical sum pulls back to one of those two product
patterns.  For every representative, the independent checker reconstructs
all 361 labelled points in exact quadratic-field arithmetic, identifies
coincidences, and tests all 64,980 unordered label pairs.  It verifies that a
claimed 3-colour pattern descends to physical points and is proper, or records
an explicit collision/edge witness defeating each pattern.  It also directly
checks every supplied 4-colour word.  Across all 15 representatives this is
974,700 pair tests and recovers the claimed 11 3-chromatic versus 4
4-chromatic orbit split, hence exactly 48 four-chromatic rotations.  A
separate exact generic fixture at `u=i` has 361 distinct points, 1,596 edges,
and the expected residue 3-colouring.

## Reproduction

Only Python 3.11 or later and the standard library are needed.  From the
repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  hadwiger_nelson_hexagon_rotational_sums_review1/independent_check.py \
  --check-expected
PYTHONDONTWRITEBYTECODE=1 python3 -O \
  hadwiger_nelson_hexagon_rotational_sums_review1/independent_check.py \
  --check-expected
PYTHONDONTWRITEBYTECODE=1 python3 \
  hadwiger_nelson_hexagon_rotational_sums_review1/independent_check.py \
  --controls
cd hadwiger_nelson_hexagon_rotational_sums_review1
sha256sum -c SHA256SUMS
```

The four negative controls delete an orbit, corrupt a unit angle, replace a
colour word by a constant word, and falsify a chromatic class.  All four are
rejected.  `EXPECTED.json` pins both the salient counts and the SHA-256 of the
full canonical receipt, including every case census and pattern-failure
witness.

## Trust boundaries and uncertainty

The lower bounds, event census, symmetry expansion, coincidence handling,
strict unit-edge reconstruction, and colouring checks are independently
implemented.  The positive 4-colour words are imported from the reviewed
certificate, but every one is checked against independently reconstructed
physical geometry.  The check trusts the certificate's exact integer/radical
input syntax, Python's arbitrary-precision integers and rational arithmetic,
the small review program, ordinary hardware, and the stated source commit;
it is not proof-assistant formalized.

A targeted literature search found established use of computation and graph
minimization in the Hadwiger--Nelson problem, including Heule's
[`Trimming Graphs Using Clausal Proof Optimization`](https://arxiv.org/abs/1907.00929)
and Parts's 509-vertex
[`Graph minimization`](https://arxiv.org/abs/2010.12665), but did not locate
this exact `H+uH` continuum classification.  That limited search is not a
priority claim.  The two related Discovery Net results cited by the target
(an infinite two-lattice four-colouring and a Golomb self-sum result) are
context rather than premises of this verification.

## Strengthening and improvement opportunities

The reusable structural lemma should be extracted explicitly: if a connected
graph containing a triangle is uniquely 3-colourable, then every 3-colouring
of its Cartesian square is, up to palette, a sum or difference of the two
factor colourings.  That would separate the conceptual obstruction from this
particular coordinate census and make later family exclusions shorter.

For progress toward fewer than 509 vertices, the next useful computation is
not a larger symmetric `H_r+uH_r` (already too large at `r=3`), but an
asymmetric or selectively augmented sum whose generic order stays below 509.
The present direct circle-line census can be generalized to `A+uB`; one
should first classify which choices of `A,B` destroy both pullback patterns,
then demand independently checked five-colour lower certificates only for
those survivors.  Publishing the 174 canonical rotations, rather than only
15 orbit representatives, would also make future cross-family comparisons
and regression tests easier.
