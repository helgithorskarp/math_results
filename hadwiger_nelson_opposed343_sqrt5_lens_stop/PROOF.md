# Proof and certificate semantics

## 1. Imported source theorem

The source verifier reconstructs `S343` from the ten Golomb points and two
fixed isometric copies of Parts's 214-point gadget.  It scans every physical
pair exactly, obtains 343 points and 1,782 unit edges, and proves that its
normalized Golomb relation consists of exactly 66 of the 95 bare patterns.
The 66 positive cases have literal words.  One CNF for the other 29 cases is
refuted by a 1,382-step deletion-free RUP trace.

This package hash-pins the source verifier, positive certificate, and RUP
trace and reruns the complete source proof.  Independent review of the source
used a different radical representation and RUP engine.  Source review is an
input trust fact; the present finishing calculation remains author-side.

## 2. Exact lens formula

Let `p,q` be source points with `|q-p|^2=16/9`, put `v=q-p`, and let `R` be a
counterclockwise quarter-turn.  Define

```text
x_+ = (p+q)/2 + (sqrt(5)/4) R(v),
x_- = (p+q)/2 - (sqrt(5)/4) R(v).
```

Because `v` and `R(v)` are perpendicular and have equal norm,

```text
|x_+ - p|^2 = |v|^2 (1/4 + 5/16)
              = (16/9)(9/16) = 1,
```

and the same calculation applies to `q` and to `x_-`.  These are precisely
the two intersections of the unit circles: their midpoint lies on the
perpendicular bisector and their perpendicular displacement has the required
length.

The checker exhausts all unordered pairs of source points and finds exactly
54 with squared distance `16/9`.  It adds both intersections for each pair.
Coefficient comparison proves that all 108 are distinct, none is an old
point, and every one has a nonzero coefficient in a basis term containing
`sqrt(5)`.  Thus all 108 leave the original
`Q(sqrt(3),sqrt(11))` coordinate field.

## 3. Complete strict graph

All coordinates have integer coefficient vectors at denominator 144 in the
basis indexed by the independent square classes 3, 5 and 11.  For basis
radicands `r_i,r_j`, multiplication uses

```text
sqrt(r_i) sqrt(r_j)
  = gcd(r_i,r_j) sqrt(r_i r_j / gcd(r_i,r_j)^2).
```

The eight square classes are distinct, so equality is coefficientwise.
Testing squared distance against the coefficient vector for one over all
`451 choose 2 = 101475` pairs therefore reconstructs the complete strict unit
graph, not an inherited or tolerance edge set.

The resulting edge partition is 1,782 old--old, 216 old--new, and 172
new--new edges.  The old neighbours of each new point are exactly its two
defining centres.  Direct deletion tests give zero articulation vertices and
zero bridges.  The new--new network is therefore physically active, even
though it ultimately fails to reduce the colour relation.

## 4. Relation equality and chromatic number

The complete graph contains `S343` as its induced first 343 vertices.  Hence
any four-colouring projects to one of the 66 source patterns; the inherited
RUP proof excludes all other normalized Golomb patterns.

Conversely, `certificate.json` has one 451-character word for each of the 66
source patterns.  The checker requires exactly those keys, checks that each
word begins with its key, and tests different colours at both endpoints of
every one of the 2,170 edges.  Thus all 66 patterns extend and the projected
relation is unchanged.

The Golomb subgraph has chromatic number four, rechecked by the source
verifier.  Any final colouring needs at least four colours, while any one of
the 66 positive words uses at most four.  Therefore the complete 451-point
graph has chromatic number exactly four.

## 5. Independent controls and trust boundary

The principal multiplication routine uses gcd and a radicand lookup.  The
control instead labels basis terms by three-bit square-class masks and uses
XOR for the resulting class and the repeated-prime product from mask
intersection.  All 64 basis products agree.  The control then rescans all
101,475 pairs by this second multiplication and recovers the edge stream
entry-for-entry.

The proof trusts Python arbitrary-precision integer arithmetic, JSON parsing,
and the published compact files.  It uses no floating-point comparison.  The
SAT generator is outside the trust boundary because every positive word is
checked directly.  No new negative solver result is asserted.  All mandatory
checks use explicit exceptions, so optimized Python cannot remove them.
