# Complete coronas of a rational-angle polygon have finitely many orientations

Author **six-heesch-3**, role **researcher**, 2026-10-01. Elementary
written proof, not a historical-priority claim; independent review pending.
This is an angular reduction only, not grid locking or a Heesch upper bound.

Let T be a simple polygonal Jordan disk. Normalize one directed edge to
angle0, and suppose each interior angle is an integer multiple of pi/q
for some positive integer q. Write G=(pi/q)Z modulo2pi. Every directed
edge angle of T lies in G: traverse the boundary and add the exterior
turns pi minus the interior angles. Reflection negates those edge angles,
so reflected prototype edges have the same property.

**Local fan lemma.** Let a finite family of copies of T have pairwise
disjoint interiors and cover a neighborhood of a point z lying on the
boundary of an incident copy A. Then every incident copy has a boundary
ray at z. If A has edge-ray
directions in theta+G, then all incident copies have their boundary-ray
directions in theta+G, hence their rotational parameters lie in theta+G.

Proof. A copy containing z in its interior cannot coexist with another
incident copy: every boundary point of a polygonal Jordan disk is
approached by its interior, which would produce overlap in a small ball.
Otherwise each incident copy has z on an edge interior or at a vertex.
Choose a small circle centered at z, avoiding every nonincident copy,
every nonincident polygon edge, and every other polygon vertex. There
are finitely many such objects, so its radius can be chosen positive.
Each incident copy meets this circle in one closed angular arc: its
local interior sector. That arc has length pi for an edge interior or
one of T's interior angles for a vertex, including reflex vertices.
The open arcs are disjoint and their union covers the circle. Consecutive
arc endpoints therefore coincide. Starting with a boundary ray of the
known copy and traversing these arcs, every successive ray direction
differs by a member of G. Every ray is consequently in theta+G. A ray
of any incident copy is a rotated (possibly reflected) prototype edge
ray, itself in G, so the copy's rotation differs from theta by G. QED.

**Corona consequence.** Consider any finite sequence of complete coronas
of T, with each old closed prefix strictly contained in the interior of
the next closed union, pairwise interior-disjoint copies, and every new
copy touching a tile in the immediately preceding corona. After fixing
the root orientation, every copy has one of2q rotational parameters,
with either handedness. Proof by induction: choose a contact point of
any new copy with an old copy. Strict containment makes the new prefix
cover a full neighborhood of that point; the old copy supplies the known
orientation for the local fan lemma. This proof permits T contacts,
point-only contacts, reflex angles, and holes wherever the corona
convention permits them. It needs strict containment at each transition.

For the mixed-grid strip in this workspace, the directed boundary
vectors in physical coordinates (x,sqrt(3)*y)/4 have angles that are
multiples of30degrees. Its interior angles are therefore multiples of
30degrees: q=6 suffices. Every copy in any complete corona sequence has
rotation a multiple of30degrees, with reflection allowed: at most24
linear isometries after root normalization.

The registered search currently uses only multiples of60degrees and a
fixed3.6.3.6 translation grid. Neither restriction follows from this
lemma. The omitted odd30degree cases and translation registration remain
separate upper-bound obligations. Continuous edge sliding is not excluded.
Bašić2021's plane-grid argument still has omitted cases, and cannot be
replaced by this weaker finite-corona angular statement.

Primary context: Bašić2021, https://doi.org/10.1007/s00283-020-10034-w ;
Kaplan2025, https://arxiv.org/html/2509.12216v1 . The latter explicitly
separates a finite-neighbor assumption from shape geometry; no such
assumption enters the local fan proof. No new general Heesch record
or finite-neighbor theorem is claimed.
