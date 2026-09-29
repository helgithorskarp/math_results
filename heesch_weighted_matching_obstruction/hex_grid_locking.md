# Complete coronas of quartic decorated polyhexes

Author: **six-heesch-3**, role: researcher.

This supplies a converse to the construction transfer in
[quartic_realization.md](quartic_realization.md) for regular polyhexes. The
120/240-degree argument for straight polyhex tilings is prior art: Paul
Church, *Snakes in the Plane*, Waterloo thesis (2008), Proposition 2.2.1.1,
pp. 30–31. See the [primary thesis](https://www.collectionscanada.gc.ca/obj/thesescanada/vol2/OWTU/TC-OWTU-3517.pdf)
and the [Waterloo thesis listing](https://cgl.uwaterloo.ca/thesis.html).
The argument below includes curved atomic ports, flat ports, finite complete
coronas, reflected copies and the hole convention. No priority claim is made
for the angle mechanism or the existing hexapillar record.

## Theorem and conventions

Let `S` be a simple unit-side regular polyhex. Replace its signed colored
edges by the exact quartic profiles of [quartic_realization.md](quartic_realization.md),
with distinct amplitudes `0 < lambda_j < 1/10`, leaving its flat edges
straight. Call the resulting unmarked disk `T`.

Start with one copy. Each new corona is finite, consists of copies with
disjoint interiors, and each new copy touches the preceding patch. The
preceding patch is contained in the interior of the enlarged patch. Arbitrary
Euclidean rotations, translations and reflections are permitted.

1. Every tile in every such complete corona patch has its **underlying**
   hexagonal cell grid aligned with that of the central tile. This assertion
   does not require the outer patch to be hole-free.
2. If every prefix, including the last one, is a topological disk, the patch
   corresponds exactly to a signed marked-grid patch of `S`, with every
   shared unit edge matched: complementary signs of the same color, or two
   flat edges. Conversely, every such marked-grid patch transfers to `T`.

Thus, under this complete-disc convention, `H_c(T)` equals the marked-grid
`H_c(S)`. If holes are allowed only in the outermost corona, this does not
assert that all same-layer contacts there satisfy the marked table. It does
give `H_h(T) <= H_c(T)+1`, by discarding that outermost layer.

The result is specific to regular polyhexes and these profiles. The
corresponding equality is not asserted for decorated polyominoes or
polyiamonds.

## 1. Angles at a locally filled contact

A boundary vertex of a simple polyhex has interior angle 120 or 240 degrees:
one or two of the three unit hexagons at a grid vertex are occupied. The
quartic profile has derivative zero at both endpoints, so these angles are
unchanged. Every other boundary point is regular and has interior angle
180 degrees. There are no straight 180-degree joins between consecutive
polyhex boundary edges: the honeycomb has three incident rays, separated
by 120 degrees.

Suppose a contact point `p` lies in the interior of the union of a finite
patch. A tile containing `p` cannot contain it in its interior when another
tile has a boundary there, since that would overlap the other's interior.
The open angular sectors of the incident tiles therefore have pairwise
disjoint interiors and fill the full circle. The piecewise regular boundary
germs justify this statement by taking directions of points approaching
`p`; finitely many closed tiles not containing `p` have positive distance
from it and cannot fill a missing sector. The only possible angle lists are

`(180,180)`, `(120,240)`, `(120,120,120)`.

In particular, a vertex cannot meet an interior point of any boundary arc.

At a smooth-smooth contact there are exactly two incident tiles. In a small
disk no other tile is present. Full local coverage and disjoint interiors
force their boundary germs to coincide: a discrepancy would produce a gap
or an overlap. The polynomial contact lemma makes a nonflat common germ a
common **whole** unit port, with the same amplitude, opposite signs and
identical chord endpoints. A flat germ can only coincide with another flat
germ.

If a tile strictly inside the patch has a flat unit edge, its flat mate
cannot be shifted along it. Two distinct overlapping unit segments have an
endpoint of the second strictly inside the first. That point is still in
the interior of the enlarged patch, and would give the forbidden
vertex-smooth angle list. Hence the flat mate has the same endpoint pair.
This excludes split flat edges as well.

## 2. Alignment, including copies touching only at a vertex

Proceed by induction over the coronas. For a new copy `Q`, choose a point
where it touches the preceding patch, and an earlier tile `P` containing
that point. Completeness makes the point interior to the enlarged patch.
Assume that `P`'s underlying grid is already aligned.

At a smooth contact the preceding argument supplies a common whole unit
edge chord. Its two underlying regular hexagons lie on opposite sides of
that chord. A unit regular hexagon is uniquely determined by a side and the
choice of side containing its interior, so the underlying grids coincide.

At a vertex contact, the angle lists are `(120,240)` or three copies of
120 degrees. The two rays of the known tile determine the three 120-degree
hexagon sectors at that vertex. Every other incident tile occupies one or
two of those exact sectors; there is no freedom to slide or rotate a sector.
A regular unit hexagon is also uniquely determined by its corner and its
two edge rays. Consequently `Q` contains an underlying hexagon of the known
grid. One common underlying hexagon fixes the entire regular hexagonal
grid. This reasoning uses sectors rather than orientation and includes
reflections.

Every new copy touches an earlier one, so the induction covers the whole
patch. Allowed placements are consequently the twelve hexagonal-grid
orientations and integer axial translations.

## 3. Underlying cells cannot overlap

Write `delta=max(lambda_j)/16 < 1/160`. During the profile deformation every
boundary stays within distance `delta` of its original unit edge. Every
underlying hexagon center is initially inside its tile, at distance at least
`sqrt(3)/2` from the original boundary. It never crosses the moving boundary
and remains in the interior of the curved tile. If two aligned underlying
cell sets shared a cell, its center would therefore lie inside both curved
tiles. This contradicts disjoint interiors. The cell sets are disjoint.

## 4. A wrong shared-edge pair makes an overlap or a bounded hole

Consider two adjacent underlying cells belonging to different tiles. Let
their common chord be parametrized by `t`, and use the outward normal of
the first tile. Its boundary is the graph `a*f(t)` and the second boundary
is `b*f(t)` in that normal coordinate, where `f=t^2*(1-t)^2` and `a,b`
include their signed amplitudes; the first interior is below its graph and
the second is above its graph.

If `a>b`, the tiles overlap near the chord midpoint. If `a<b`, the two
distinct graphs form a Jordan lens with both endpoints on the tiles. Its
middle point is outside both tiles. No third tile can cover that point:
the only base cells incident with the chord interior are the two already
occupied ones, and every other base cell is at distance at least `1/2`
from the chord midpoint. The lens middle point is displaced by at most
`delta`, while any other tile boundary moves by at most `delta`. Since
`2*delta<1/2`, it remains outside every third tile throughout deformation.
The closed lens boundary belongs to the patch, so this uncovered point is
in a bounded component of its complement. A disk patch cannot contain
such a hole.

Therefore `a=b`. This is precisely complementary signs of equal amplitude
or two flats. Distinct amplitudes identify the same color. The argument
applies to **all** shared unit edges in the final disk patch, including
contacts within its outermost layer.

For clarity, the distance `1/2` follows directly from the unit honeycomb:
the two endpoints are the nearest points of any third incident hexagon to
the edge midpoint; nonincident cells are farther away. A point at distance
greater than `delta` from a tile's original boundary cannot change its
inside/outside status during this boundary deformation.

## 5. Transfer back and computational use

All shared edges now have a single consistently assigned profile. The
small-profile embedded-network isotopy in [quartic_realization.md](quartic_realization.md)
maps the entire finite underlying cell patch to the actual curved patch.
It maps each individual tile and every prefix, preserving contacts, holes,
disk topology and strict containment. The underlying cells therefore give
a complete marked-grid corona witness. The forward transfer was already
proved in that file. This proves the claimed equality for `H_c`.

A checked UNSAT certificate for a **complete** marked-grid encoding can
thus provide a Euclidean upper bound for this class. A timeout, UNKNOWN,
incomplete candidate universe or unchecked solver report still cannot.
The SAT implementation and its explicit finite candidate proof are
described in [marked_corona.md](marked_corona.md).

The five-corona hexapillar fixture there is a reproduction of a published
baseline. This theorem supplies an exact bridge for the specified curved
profile; it supplies no seventh-corona construction.
