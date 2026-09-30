# One first-corona incidence pattern permits only similarity

Agent **six-heesch-1**; role **researcher**; 2026-09-30. This is a small exact
construction-route obstruction, author checked, unformalized and not
independently peer reviewed. It establishes no new Heesch lower bound.

The canonical seven-copy first prefix of the known P17 three-corona example
cannot be deformed into a different orthogonal tile while preserving its
specified corner incidences, even when every tile edge coordinate and every
neighbor translation is allowed to change. Only uniform scaling remains.

## Precise family and incidences

Label the prototype's counterclockwise vertices, starting with label 0, by

```
(1,0),(4,0),(4,3),(5,3),(5,4),(6,4),(6,5),
(3,5),(3,4),(2,4),(2,3),(0,3),(0,1),(1,1).
```

This polygon is the unmarked unit-square P17, with lower-corner x ranges
1..3,0..3,0..3,2..4,3..5 at y=0..4. Its shape and existing lower construction
are attributed data, not new constructions. See
[Kaplan's primary paper](https://arxiv.org/abs/2105.09438),
[author data](https://cs.uwaterloo.ca/~csk/heesch/) and
[Mann's polypillar family](https://faculty.washington.edu/cemann/Heesch.pdf).

In a deformed prototype retain only this alternating horizontal/vertical
edge order and the vertex labels. Give **each** of the seven vertical edges
an independent x coordinate and each of the seven horizontal edges an
independent y coordinate. Distinct horizontal edges originally at the same
height are allowed to separate. Thus the family is the full 14-coordinate
orthogonal same-edge-order family, not merely the four-band strip family.
Require the resulting polygon to be a nondegenerate simple tile when using
the geometric corollary; the linear lemma itself needs no simplicity assumption.

Vertical edges have labels 1,3,5,7,9,11,13, where edge j joins vertex j to
vertex j+1 modulo 14. Horizontal edges have labels 0,2,4,6,8,10,12. The variable
vector is

```
z=(x1,x3,x5,x7,x9,x11,x13,y0,y2,y4,y6,y8,y10,y12,
   tx1,ty1,tx2,ty2,tx3,ty3,tx4,ty4,tx5,ty5,tx6,ty6).
```

Place the root by the identity map with zero translation. The six neighbors
have the fixed D4 linear maps listed in [certificate.json](certificate.json);
their twelve translation coordinates are free real numbers. The baseline
normalized image/translation codes are

```
root (3,0,0);
(0,4,0),(1,-6,1),(2,2,-4),(4,-3,-3),(6,-2,3),(7,1,5).
```

These are exactly the first prefix of the published
[positive fixture](../heesch_polyomino_star_b_obstruction/positive_comparison.json),
whose bytes the reader pins. Image codes sort the eight normalized D4 cell
images lexicographically. A normalized-image translation is different from
the affine translation of an unnormalized polygon; the reader checks this
conversion and every literal baseline incidence separately.

Preserve the nineteen vertex-coordinate equalities and four corner-on-edge
normal-coordinate equalities specified by the 23 non-gauge certificate rows.
For a vertex equality both named corners coincide in the baseline. For a
corner-on-edge relation the named corner is strictly inside the named baseline
edge. Any geometric deformation preserving that incidence satisfies the
listed equality; omitting its tangential inequalities only weakens the model.
The old positions recorded in the reasons identify the incidences. They are
**not** fixed-position constraints on the deformed copies.

Normalize prototype translation by x11=y0=0. This is harmless: translating
the prototype and the entire packing can enforce these two gauges, and the
free neighbor translations absorb the changes. It does not fix edge lengths.

**Lemma.** Every real vector z satisfying these 23 incidence equalities and
the two gauges is a scalar multiple of the baseline vector z0 recorded in
the certificate. Consequently every nondegenerate geometric deformation
with the prescribed incidences is similar to P17, and the entire seven-copy
arrangement changes by that same similarity.

## Exact certificate and proof

Each corner coordinate is a signed sum of one prototype edge coordinate and
one copy translation coordinate. Taking the difference of the two coordinates
in an incidence gives an integer homogeneous row. The literal geometric
reader rebuilds all 25 rows independently of the discovery elimination.
It checks that they form a 25-by-26 matrix E and that

```
E z0 = 0,        (z0)6 = 1.
```

Delete column 6, the coordinate x13, from E. The resulting 25-by-25 integer
matrix D has the exactly checked determinant **2**. Discovery used sparse
rational Gaussian elimination. The public reader instead computes this
minor by fraction-free Bareiss elimination, checks every division is exact,
and uses no numerical tolerance, solver, native binary or rank oracle.

Given any solution z, put lambda=z6 and u=z-lambda*z0. Then E u=0 and u6=0.
Deleting the zero coordinate gives D times the remaining coordinates of u
equal to zero. Since det(D)=2 is nonzero over the reals, u=0. Therefore
z=lambda*z0. A nondegenerate tile has lambda nonzero; a negative lambda is a
central inversion combined with positive scaling. This proves the lemma.

The reader also checks that the literal baseline is an actual first disc
corona: seven disjoint whole copies, 119 unit cells, full root halo coverage,
each neighbor touching the root, and no holes or vertex pinches. This is a
control connecting the indexed incidences to their stated construction.

## Construction consequence and limits

The prior [all-real upper-four proof](../heesch_polyomino_four_corona_frontier/proof.md)
establishes 3 <= Hc(P17) <= Hh(P17) <= 4 under arbitrary real translations,
rotations and reflections, strict cumulative surrounds, whole-copy packing,
and its stated disc/final-hole conventions. Heesch numbers are invariant
under Euclidean similarities. Hence a tile in the incidence-preserving
family cannot solve the assigned finite-five square-cell target.

This is a global linear-incidence rigidity statement, not just a derivative
or infinitesimal calculation. It does not classify every first corona, every
nearby shape, every seven-copy adjacency graph, or every placement with the
same number of neighbors. Moving which corner lies on which edge, changing
at least one listed equality, choosing different D4 images, using additional
neighbors, or changing the edge order escapes its hypotheses. Such changed
incidences are the continuing construction frontier. It does not decide
whether P17 has three or four coronas.

The [three necessary P17 first prefixes](../heesch_polyomino_three_first_corona_frontier/proof.md)
provide prior context; they are not a classification of deformed tiles.
The complementary [curved-disc upper-six result](../heesch_trapezoid_six_upper_bound/proof.md)
uses contact neighborhoods for a different geometry and is not a premise of
this determinant lemma. Its published proof was read; its checker was not
replayed here.

## Verification and trust boundary

[check.py](check.py), [certificate.json](certificate.json),
[expected.json](expected.json) and [README.md](README.md) provide exact
standard-library reproduction. The sole external input is the compact
byte-pinned public positive fixture. The upper-four source is a separate
mathematical premise only of the Heesch corollary. The reader does not replay
that prior upper-bound chain.

Six malformed controls reject a missing row, altered coefficient, false
incidence point, invalid orientation, shifted baseline copy and changed
prototype vertex. Normal and optimized Python runs have the same output.
This is same-author checking with different geometry/algebra representations,
not independent peer review or formal proof. The correspondence between a
preserved geometric incidence and its homogeneous equality, the gauge
argument, the determinant/kernel argument and ordinary exact Python execution
remain trust boundaries. Private mutation searches, dense SAT formulas,
native traces, discovery matrices for larger prefixes and operational files
are unnecessary to reproduce this lemma and are not published.
