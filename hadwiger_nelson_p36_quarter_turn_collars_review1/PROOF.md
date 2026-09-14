# Review proof and scope audit

## 1. Statement under review

Let `P=P36` be the 127 Eisenstein integers `a+b*omega` satisfying
`a^2+a*b+b^2 <= 36`.  For `p,q in P`, put

```text
c=(p-i*q)/(1-i),
Q_k=c+i^k(P-c),  0 <= k < 4.
```

The target asserts that the complete strict unit-distance graph on the
physical union of the four `Q_k` is four-colourable for all `127^2` ordered
pairs.  It additionally asserts that every off-diagonal pair gives empty
fourfold intersection, 504 distinct physical points, and 1,368--1,592
edges.  These are the claims accepted here.

## 2. Exact coordinate model

Write a point as the integer quadruple `(r,s,u,v)` meaning

```text
((r+s*sqrt(3))/4, (u+v*sqrt(3))/4).
```

Then multiplication by `i`, complex conjugation, and multiplication by
`omega` are exact integral transformations on the collar module.  The center
is independently computed from

```text
c=(p+q+i*(p-q))/2,
```

which follows by rationalizing `(1-i)^{-1}`.

For a difference `(r,s,u,v)`, basis independence over the rationals gives

```text
16*|x|^2 =
  r^2+3*s^2+u^2+3*v^2 + 2*(r*s+u*v)*sqrt(3).
```

It is a unit exactly when the rational coefficient is 16 and the
`sqrt(3)` coefficient is zero.  The first coefficient is a sum of
nonnegative terms, so `|r|,|u| <= 4` and `|s|,|v| <= 2`.  Exhausting this
finite box gives 12 oriented or six unoriented unit steps.  Looking up those
six translates of every physical point therefore produces every strict unit
edge exactly once; no numerical tolerance or supplied edge list is used.

As a second route, the checker compares this lookup graph with all
`n choose 2` exact squared distances for all 58 off-diagonal representatives
having extra contacts and all 16 diagonal representatives.  The edge sets
agree in every case.

## 3. Coverage of centers and collisions

The checker independently enumerates all ordered patch-point pairs and finds
16,129 distinct centers.  Exact multiplication by the six powers of `omega`,
with and without conjugation, partitions them into 1,408 representatives
with orbit-size histogram

```text
1^1, 6^126, 12^1281.
```

Unlike the target's representative-only proof route, the review reconstructs
the physical graph separately at every raw center.  In every off-diagonal
case, the occurrence multiplicities are exactly 500 singleton points and
four double points.  Hence the union has `500+4=504` physical points, has no
triple or fourfold point, and has empty total intersection.  There are 16,002
such cases.  Every one of the 127 diagonal cases has exactly one fourfold
common point.

The off-diagonal edge census independently gives 15,342 placements with
1,368 edges and 660 with additional contacts.  The latter form 58 symmetry
orbits, and the maximum edge count is 1,592.

## 4. Independent positive colour cover

For each representative graph, the checker finds its lexicographically first
triangle and fixes its vertices to colours `0,1,2`.  This loses no solutions,
because any proper colouring assigns three distinct colours to a triangle
and the colour names can be permuted.  It then runs deterministic DSATUR:
choose an uncoloured vertex of maximum saturation, then maximum degree, then
minimum index, and try available colours in increasing order.

All 1,408 searches return a proper four-colour word.  They visit 705,568
search nodes in total, at most 503 for one graph, with zero backtracks.  Each
word is checked on the complete independently reconstructed edge set.

For each of the 16,129 raw centers, the checker finds an explicit dihedral
map to its representative, verifies that this maps the raw physical point
set bijectively to the representative point set, transports the fresh word,
and checks it on every edge of the separately reconstructed raw graph.  This
direct final check makes correctness of every raw positive word explicit; an
unproved appeal to representative counts is not being used to skip raw graph
verification.

The target's 611 literal words are also independently decoded and checked on
the reconstructed representative graphs.  Their file hash is
`aaa9a6813981c01d69e4ca278a6e882dbee0de6d27b30b57f8a567662e1a8221`.
They corroborate the target, but the fresh DSATUR cover proves the same upper
bounds without relying on those stored words or on the target's residue
ansatz.  A forced monochromatic edge is rejected as a negative control.

## 5. Verdict and limitations

The exact point construction, collision claims, complete strict graph
reconstruction, family coverage, and positive four-colourability witnesses
all survive independent checking.  The appropriate verdict is therefore
**ACCEPT with high confidence for the stated fixed-family theorem**.

Nothing in this evidence applies to another relative angle, arbitrary
translations, a non-cyclic choice of patch motions, five or more patches, or
general plane unit-distance graphs.  In particular, the result does not
lower the 509-vertex five-chromatic record and is not a global order lower
bound.  Its mathematical value is as a complete restricted-family exclusion
at 504 points.
