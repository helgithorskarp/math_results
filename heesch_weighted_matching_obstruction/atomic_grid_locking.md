# Atomic curved edges lock all three polyform grids

Author: **six-heesch-3**, role: researcher.

This extends the geometric method of [hex_grid_locking.md](hex_grid_locking.md)
to fully decorated polyominoes and polyiamonds as well as polyhexes. The
whole-edge hypothesis is essential. Flat ports in the earlier square and
triangular constructions remain outside this theorem. The use of geometric
matching rules and the straight-polyhex angle argument are prior art; no
priority claim is made here.

## Hypotheses and claim

Let `S` be a simple edge-connected polyomino, polyiamond or regular polyhex,
with unit cell sides and a boundary subdivided into unit edges. Replace
**every** boundary unit edge by a regular nonstraight polynomial graph,
measured in the edge's tangent/outward-normal frame. Assume:

* the profile and its derivative vanish at both endpoints;
* a Euclidean isometry identifying two nontrivial profile subarcs identifies
  their whole closed unit arcs and their endpoint pairs;
* noncoincident transformed arcs have only finitely many intersections;
* the profiles have displacement at most `delta<1/160`, and lie in endpoint
  cones of half-angle less than `pi/6`, throughout scaling from zero;
* a consistently paired finite grid-edge network preserves its incidence
  and cyclic order during that scaling.

The specified quartics with **no flat ports** in
[quartic_realization.md](quartic_realization.md) meet these hypotheses. So do
all the quintics in [quintic_realization.md](quintic_realization.md).

A complete corona is finite, its tiles have disjoint interiors, every new
tile touches the preceding patch, and the preceding patch lies in the
interior of the enlarged patch. Arbitrary Euclidean isometries, including
reflections, are permitted. Every tile in every such corona has its
underlying cell grid aligned with that of the central tile. The assertion
does not require the last patch to be a disc.

## Local lemma: a filled contact propagates whole unit chords

Let `p` be in the interior of a finite patch union. All tiles containing `p`
have `p` on their boundaries if at least one has it on its boundary: another
tile's interior there would overlap that first tile. Tiles not containing
`p` have positive distance from it and can be excluded by a small disk.

For any boundary edge germ incident with `p`, a small positive-length part
of that germ is interior to the patch union. It is covered by boundaries of
the other tiles. None can contain such a point in its interior without
overlap. There are only finitely many polynomial arcs. Finitely many finite
intersection sets cannot cover the germ, so some other arc coincides with
it on a nontrivial subarc. Atomicity makes this a common whole unit port,
with coincident endpoint pairs. Interiors lie on opposite local sides;
otherwise the two tiles overlap. A third tile cannot occupy that same side.

There is a connected cycle of these germ pairings through the tiles at `p`.
Here is a local justification that covers straight 180-degree joins and
reflex corners. For a sufficiently small circle centered at `p`, each
incident tile occupies one nonempty connected angular interval: its boundary
has two regular germs with the original cell-grid tangent rays, and its
interior angle is strictly between zero and `2*pi`. Their intervals have
disjoint interiors and partition the circle. Consecutive tile intervals
abut along a boundary germ. The preceding argument pairs that germ, giving
the adjacency cycle. A cusp between distinct unpaired germs cannot be left
uncovered, or filled by another incident tile with a zero angular interval:
all cell-grid corner angles and smooth-point angles are positive. The same
argument applies for all sufficiently small circle radii.

If `p` is an interior point of one port, its mate is the same whole port and
also has `p` in its interior. The two smooth sectors already fill the small
circle. If `p` is a unit-edge endpoint of one tile, atomicity prevents its
germ mate from having `p` strictly inside a port. Iterating around the cycle
propagates endpoint membership as well. Collinear successive unit edges are
treated as separate ports, even if their union happens to be differentiable
at the join. The proof uses the endpoint property, not a claim that such a
join must be an angular corner.

## Grid alignment

A common whole unit port has a common undeformed chord. The cell incident
with that port in each tile lies on its prescribed side of the chord. A
unit square, unit equilateral triangle or unit regular hexagon is uniquely
determined by one side and the choice of side containing its interior.
Thus a whole-port pairing fixes a common cell grid. This also applies to
reflected copies; grid alignment does not require a common handedness.

For a new tile `Q`, take a contact point `p` with the preceding patch and
an earlier tile `P` containing it. Completeness makes `p` interior to the
enlarged patch. The local pairing cycle connects `P` to `Q`, possibly through
other tiles of the same new corona. Inductively `P`'s grid is known; the
whole chords propagate that grid around the cycle to `Q`. Induction over
coronas proves the claim. This is why a new tile touching only at a vertex
cannot introduce an independent rotated or translated grid.

## Recovering the base cells and topology

Cell centers stay inside their deformed tiles. The inradii of the unit
square, triangle and hexagon are respectively `1/2`, `sqrt(3)/6` and
`sqrt(3)/2`, all greater than `delta`. A center never meets the moving
boundary. Shared underlying cells would put their center inside two tile
interiors, so underlying cell sets cannot overlap.

If all shared unit edges in an aligned patch have the same geometric
profile on their two sides, the embedded-network isotopy maps every base
tile to its curved tile. It also maps every prefix and therefore preserves
contacts, strict containment, holes, pinches and disc topology. This is a
forward-and-backward statement about a finite consistently paired network;
it does not assume that drawing approximately matching curves proves it.

The quintic matching proof excludes mismatched edges in a final disc and
thus gives an exact marked-grid correspondence for all three base families.
For fully decorated quartics the same conclusion follows from the
overlap-or-lens argument in [hex_grid_locking.md](hex_grid_locking.md), with
one uniform distance bound: the disk of radius `1/4` about a common unit-edge
midpoint lies in the union of its two incident cells. For square and hexagon
cells the maximal such radius is `1/2`; for triangular cells it is
`sqrt(3)/4`. Every other base cell stays at distance at least `1/4` from the
midpoint, and `2*delta<1/4` keeps the uncovered lens point outside every
third deformed tile. A final disc forbids that bounded complementary lens.

Consequently, for the fully nonflat quartic subclass, complete-disc Euclidean
coronas correspond exactly to complementary marked coronas on the relevant
grid, with rotations and reflections. If only the last corona may have
holes, the usual upper implication `H_h <= H_c+1` is retained. The earlier
hexagonal theorem is stronger in a different direction: it permits flat
ports. No general square/triangular claim with flat ports is inferred.

## Whole-plane counterpart

The same local locking argument applies to any whole-plane tiling by these
tiles. It is locally finite: every tile meeting a bounded set lies in that
set enlarged by the fixed tile diameter, and disjoint positive-area
interiors bound the number of such tiles. Filled-contact neighborhoods are
therefore finite. Their whole-port pairings propagate a common grid across
the tiling. The tile adjacency graph is connected: a generic finite path
between two tile interiors meets only finitely many regular boundary arcs
and can avoid vertices. Each crossing is a whole-port adjacency.

Retained cell centers exclude overlapping base cells. A missing base cell
would have its center outside all tiles throughout the small deformation,
since it stays farther than `delta` from every occupied base cell. That
contradicts coverage of the plane. Wrong shared-edge profiles either overlap
or leave an uncovered lens point, so they are forbidden in a plane tiling
as well. The base cells thus give a marked-grid plane tiling. Conversely a
valid grid tiling transfers by the same edge-network deformation, extended
over the grid faces. This locally finite deformation has uniformly bounded
displacement and gives a global homeomorphism.

For fully nonflat quartics this is plane-tiling equivalence with the
complementary marked model, with reflections. For the positive-odd-part
quintics it is equivalence with the rotations-only color/state model: every
paired edge has the same handedness, which propagates over the connected
adjacency graph. This is also a direct route for transferring a separately
proved nontiling obstruction, in addition to the finite-corona statements.

## Research use and trust boundary

A complete, independently checked finite grid exclusion now supplies a
geometric upper obstruction for these subclasses; a timeout or incomplete
candidate enumeration does not. Lower witnesses must satisfy the same
motions, labels and prefix topology as the theorem. The written local and
isotopy arguments are not proof-assistant formalizations. This result finds
no seven-corona shape and changes none of the published record claims.
