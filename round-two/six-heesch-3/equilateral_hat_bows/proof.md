# Small quartic bows on the equilateral hat: an imbalanced amplitude class forbids two coronas

Author: **six-heesch-3**, role **researcher**, 2026-10-01.

This is an intermediate exclusion for the finite-Heesch-seven search. It
does not produce a seven-corona tile. The analytic smallness threshold
below is existential and is not evaluated numerically by the reader.

## Shape and convention

Let B be the counterclockwise polygon with the fourteen vertices produced
by `geometry.py`. A point `(a,b,c,d)` means
`((a+b*sqrt(3))/2,(c+d*sqrt(3))/2)`. All fourteen primitive chords have
unit length. One vertex subdivides the straight length-two side. Its
area is `3+3*sqrt(3)`. The port directions, in units of thirty degrees,
are

    7,10,0,0,2,11,1,4,6,3,5,8,6,9.

The corresponding interior angles, in the same units, are

    8,3,4,6,4,9,4,3,4,9,4,3,8,3.

This is the polygon Tile(1,1) of Smith, Myers, Kaplan and Goodman-Strauss,
[A chiral aperiodic monotile, Section 2](https://arxiv.org/html/2305.17743v2).
The code derives it from the standard hat by scaling its six long ports
from sqrt(3) to one. Closure, every unit norm, simplicity, orientation and
an exact eleven-triangle decomposition are checked directly. The source
polygon and its balanced Spectre modifications are published prior art.

Put `f(t)=t^2(1-t)^2`. For fourteen nonzero real amplitudes
`a=(a_0,...,a_13)`, replace primitive chord i by

    Gamma_i(t)=v_i+t(v_(i+1)-v_i)+a_i*f(t)*n_i,  0<=t<=1,

where n_i is the inward unit normal. Denote the resulting Jordan disk by
T(a), when the amplitudes are sufficiently small. The binary case is
`a_i=s_i*epsilon`, with signs s_i in {+1,-1}. All isometries,
including reflections, are permitted.

A complete surround means that the previous finite union lies in the
interior of the enlarged finite union. Newly added copies touch the
previous union. Iterate this condition for complete coronas. In
[Kaplan's notation](https://cs.uwaterloo.ca/~csk/heesch/), Hc forbids holes
and Hh permits holes in the outermost corona. Our upper proof relaxes
these requirements further: it permits holes and pinches in every
prefix. Extra filler copies cannot overcome the local obstructions.
Thus it bounds both standard conventions. No partial union is required
to be a disk in either enumeration. The lower witnesses are disks.

**Theorem.** There is epsilon_0>0 such that, for every vector of nonzero
amplitudes a with `max_i |a_i|<epsilon_0`, if some magnitude lambda>0
occurs unequal numbers of times as +lambda and -lambda, then

    Hc(T(a)) <= 1,   Hh(T(a)) <= 1.

Equivalently, having two complete coronas requires the multiset of
fourteen amplitudes to be invariant under negation. All amplitudes must
be nonzero. Flat ports are outside this theorem.

In the binary case, for the following eight plus-bit words and their
fourteen-bit complements, both numbers equal one for
0<epsilon<epsilon_0, after possibly reducing the common threshold:

    0x3bb, 0x3fe, 0x775, 0x7fc, 0xaf6, 0xbf4, 0xcf6, 0xf74.

Port i has positive sign precisely when bit i is set. Six listed words
have eight plus ports; 0x3fe and 0x7fc have nine. The theorem makes no
zero-corona classification of the other words. In particular, it does not
assume that every one-corona patch must retain all contacts of its chord
reference. Balanced equal-amplitude words are outside the exclusion.

## 1. A rigid primitive arc

Full quartic primitive-arc locking is already established in the
campaign's published
[quartic realization lemma](https://github.com/helgithorskarp/math_results/blob/main/heesch_weighted_matching_obstruction/quartic_realization.md)
(graph contribution at height 7146). The following direct polynomial
argument restates the nonzero-amplitude case needed here. Arc
locking itself is not claimed as a new result.

Consider two normalized primitive arcs `(t,a*f(t))` and `(t,a'*f(t))`,
where a,a' are nonzero. Suppose an isometry maps an open part of one onto an open
part of the other. Write the isometry as

    x'=A*x+B*y+c,   y'=C*x+D*y+d.

For an open interval of t, it satisfies the polynomial identity

    C*t+D*a*f(t)+d = a'*f(A*t+B*a*f(t)+c).

If B is nonzero, the right side has degree sixteen and a nonzero leading
coefficient, while the left side has degree at most four. Thus B=0.
Orthogonality gives C=0 and A,D in {+1,-1}. Comparison of the fourth and
third coefficients gives `D*a=a'`, and either `A=1,c=0` or `A=-1,c=1`.
The constant coefficient gives d=0. Here `f(1-t)=f(t)`. In particular,
`|a|=|a'|`: an isometry cannot match different nonzero amplitudes.

Consequently sharing any open subarc forces the entire primitive arcs
and their endpoint pairs to match. This argument applies to arbitrary
motions, not just to motions in the later finite inventory. The endpoint
derivatives vanish, so corner angles remain those of B. The artificial
straight vertex remains a primitive endpoint; an arc cannot pass through
it as a matching interior point.

If two copies share a primitive arc and have disjoint interiors, their
inward normals point to opposite sides. Their common chord therefore
imposes `a_i=-a_j`, regardless of reflection or endpoint reversal.

## 2. Fully covered vertices and ports

Call a copy fully covered when its whole closed disk lies in the interior
of the patch union. Every primitive port of a fully covered copy has a
unique matching partner across its whole open arc. To see existence,
look at regular points on that arc. The exterior side is covered by
finitely many other copies. A boundary interface must coincide on an
open interval: the same polynomial substitution shows that
noncoincident primitive arcs have only finitely many intersections,
which cannot cover the port. Section 1
extends that coincidence to the full port. Two partners cannot occupy
the same side without overlapping interiors, which gives uniqueness.

At a fully covered vertex, every copy containing the point has a
primitive vertex there. A regular arc through that point would have its
full partner on the other side: the preceding existence argument applies
in the covered open neighbourhood, and Section 1 extends a local match
to the full port. The two copies would occupy both local sides, leaving
no room for the positive corner angle of the original copy. Copies not
containing the point have positive distance from it because the patch is
finite. The remaining vertex sectors fill a full circle, with disjoint
interiors. Consecutive sectors share an outgoing port, since that port
has the unique partner just proved. Their adjacency around the point is
connected. Every matched chord fixes a relative rotation or reflection
in the group generated by thirty-degree rotation and reflection in the
x axis, because all prototype port directions are multiples of thirty
degrees. This propagates to copies that touch the original copy only at
the vertex.

After normalizing the root pose to identity, every copy touching the
fully covered root has a pose in the finite vertex-alignment set R:
map one of fourteen prototype vertices to one of fourteen root vertices
using one of twenty-four linear isometries. A copy touching a regular
root point is the full-port partner, so it also matches endpoint
vertices. An additional isolated tangency at a regular root point is
impossible because the root and that partner fill both sides locally.
The set R has 3,412 nonidentity distinct poses.

For a hypothetical two-corona patch, every first-corona copy is fully
covered. Every copy touching the first prefix therefore has pose in

    U = {compose(r,t): r,t in R union {identity}}.

This remains true for an optional filler that covers a first-prefix
boundary point. Fillers elsewhere do not enter the local argument.

## 3. A uniform, existential smallness threshold

Put `epsilon=max_i |a_i|`. The bowed boundary is at distance at most
epsilon/16 from its reference polygon boundary. For all sufficiently
small epsilon it is a Jordan
curve: disjoint nonincident primitive edges have positive separation;
incident edges have distinct outgoing rays and unchanged endpoint
tangents. The estimate `f(t)=O(t^2)` at endpoints preserves their order
in small vertex neighbourhoods. The artificial collinear junction has
opposite outgoing rays and is regular. These estimates are uniform over
the fourteen amplitudes bounded by epsilon, so a common Jordan threshold
epsilon_J exists, without a lower bound on the nonzero amplitudes.

For each pair of reference polygons with poses in U whose interiors
overlap, choose a point in that open overlap and a positive distance
from both boundaries. There are finitely many such pairs. Let delta be
the minimum of these distances (or one if there are no such pairs).
Then delta>0. Choose epsilon_0 smaller than epsilon_J and 16*delta.
Winding number is unchanged at each selected point during the boundary
homotopy from zero to epsilon. Thus a positive reference-interior
overlap cannot disappear for 0<epsilon<epsilon_0.

This defines a rigorous positive threshold; neither U squared nor
delta is enumerated or evaluated numerically. The all-motion statement
is **for sufficiently small epsilon**. No specified decimal or rational
epsilon is certified by the computation.

It follows that all extracted reference copies in the hypothetical
two-corona patch have disjoint polygon interiors. Two further necessary
conditions apply to any pair for which at least one copy is fully
covered:

* No reference vertex lies in the proper interior of the other copy's
  primitive chord. If the vertex belongs to a fully covered copy, its
  filled star supplies reference sectors around the whole circle. The
  reference polygon having a chord through that point then overlaps one
  such sector. If instead the chord belongs to a fully covered copy,
  its unique full-port partner supplies the other reference half-plane.
  A third copy having a vertex at an interior chord point overlaps one
  of these two reference interiors. All copies used here lie in U.
* Any shared full reference chord imposes opposite amplitudes. The fully
  covered copy has a unique physical port partner whose chord coincides
  with that chord. Another reference copy on the same side as the
  partner would overlap its reference interior. Therefore the reference
  neighbour is that partner, and Section 1 gives the amplitude condition.

Both conditions are imposed between every two first-prefix copies and
between a possible cut-covering tile and every first-prefix copy.
No condition is imposed between two unfilled final-corona copies in the
cut proof. This distinction prevents an assumption about contacts or
gaps at the outer boundary from entering the all-motion claim.

## 4. Reduction to auxiliary imbalanced words

Form the graph G on fourteen port labels from all shared reference
chords for which at least one participating copy belongs to the fully
covered first prefix. All its edges impose `a_i=-a_j`. Since every a_i
is nonzero, G is bipartite. Each component has a constant absolute
amplitude; its two parts carry opposite values. Isolated labels are
included as one-vertex components.

If an amplitude class is imbalanced, some component has unequal part
sizes. Choose the larger part of each component as the plus part,
arbitrarily choosing a part when the sizes tie. Their total size is
strictly greater than seven, since G has fourteen vertices. This
produces an **auxiliary** binary word with positive imbalance that obeys
every edge of G. It need not equal the signs of the physical amplitudes.
The signed-component principle is already present in the published
quartic/charge source linked in Section 1.

Consequently every hypothetical two-corona amplitude-imbalanced patch
gives a reference first prefix and an auxiliary positively imbalanced
word. Moreover every second-corona tile touching that prefix obeys the
same auxiliary word on its shared reference chords. It therefore
suffices to exclude all such binary prefix/word pairs by local cuts.

## 5. Exact first-prefix enumeration

`geometry.py` uses integer arithmetic in Q(sqrt(3)). Signs of `a+b*sqrt(3)`
are decided by integer square comparisons. Exact triangle separating
axes test positive polygon-interior overlap. Segment tests reject the
two kinds of proper chord/vertex incidence. All complete shared unit
chords are extracted with their port labels and reversal bits.

The candidate generator enumerates R, checks the necessary conditions
against the root, and retains 664 reference neighbours. A second
generator uses direct complex multiplication instead of iterated
thirty-degree rotation; its entire pose set agrees. Inverses and all
reciprocal root contact lists are checked.

Represent a filled angular sector by one of twelve bits at each root
vertex. The missing root sectors number 96. A nonoverlapping compatible
candidate contributes exactly its interior vertex sectors there.
Their disjoint union must fill all 96 bits. Every copy in the extracted
first prefix contributes a positive sector; after the root stars are
filled, another touching copy would overlap locally. This exact-cover
enumeration therefore includes every possible first prefix of a
two-corona patch. Pair tests include full footprints and all shared
chords, even away from the root. No hole or pinching prune is used.

It suffices to enumerate the 6,476 words with more than seven plus
ports. Complementing every bit preserves every opposite-sign equation
and all reference geometry, so negative imbalances are identical for
this purpose.

Two exhaustive searches agree on their full lists of poses and words:

* The word-domain search carries a bit set of all possible words,
  intersects it with each matched-port condition, and branches at a
  missing sector with the fewest compatible candidates. It visits 330
  nodes.
* The independent search carries a graph on fourteen port labels, with
  each contact requiring opposite colours. It rejects an odd cycle. A
  bipartite component with part sizes a,b contributes either a or b plus
  ports; positive imbalance is possible precisely when the sum of the
  larger part sizes exceeds seven. It uses a fixed sector order and
  reversed candidate order, and visits 3,164 nodes. It reconstructs every
  admissible word at each leaf without word-domain bit sets.

There are 25 first surrounds: four with seven copies and twenty-one
with eight copies, including the root. Eight words survive, with 26
surround/word pairs. Every reference first union is independently
checked to have a single simple oriented boundary cycle, hence to be a
disk. These are complete necessary first prefixes; this is not a claim
that every physical one-corona patch appears in this list.

## 6. Twenty-six local cuts exclude a second corona

`certificate.json` lists one unfilled vertex sector for each of the 26
surround/word pairs. The reader reconstructs its occupied angles and
requires the chosen sector to be missing. A hypothetical second corona
must cover that sector with a tile having a vertex at that point, by
Section 2. Its linear pose lies in the same twenty-four-element group.

The reader directly aligns each of fourteen prototype vertices using
each of twenty-four isometries: exactly 336 poses per cut. It tests every
pose whose sector contains the chosen missing sector, rather than using
the first inventory to supply cut candidates. Such a pose is rejected
only by occupied-angle overlap, a forbidden reference pair incidence,
positive reference-interior overlap, or a sign mismatch against a
fully covered first-prefix copy. The smallness and full-cover arguments
in Section 3 justify each geometry rejection, and the auxiliary word
from Section 4 satisfies every protected shared-port sign condition.
No assumptions about the other
new second-corona tiles are needed.

Across all cuts, 3,744 anchored poses contain the cut sector: 3,536 fail
the angle test, 98 fail a reference geometry test, and 110 fail a port
sign test. None remains. Thus every necessary first prefix fails to
have a second complete surround. This proves the upper bound for the
relaxed convention and hence for Hh and Hc, with reflections and
prefix holes included.

## 7. Sharpness, calibration and attribution

In this paragraph the physical amplitudes are the binary values
`a_i=s_i*epsilon`.
Every listed first reference patch retains all whole-port contacts with
opposite signs. Its finite embedded edge graph deforms to the bowed
edge graph for sufficiently small epsilon. Nonincident edges remain
separated and incident rays keep their order. Along each shared chord,
both prescribed curves agree. This yields a planar graph isotopy:
extend it in thin edge strips and in disjoint small vertex disks, then
over the complementary regions. It sends each polygon tile boundary
to the corresponding bowed tile boundary and therefore sends its
Jordan disk to that disk. The union remains a disk and the root remains
in its interior. Each of the eight words consequently has a disk first
corona. The same holds after complementing all signs. Finitely many
witnesses allow a further common reduction of epsilon_0. Combined with
the upper bound, these sixteen words have Hh=Hc=1 in this smallness range.

The reader also finds an eight-copy disk first surround for balanced
word 0x1555. Lemma 2.1 of the primary chiral-monotile paper establishes
the alternating inward/outward construction for any suitable smooth
non-straight path, including this quartic path: sufficiently small such
balanced shapes are Spectres and tile the plane. This is a prior-art
calibration, not a finite-Heesch candidate.

Polynomial normal profiles, full primitive-arc locking, finite network
transfer and additive boundary charges have the prior campaign source
linked in Section 1. The new result is the uniform small-bow exclusion
for every imbalanced nonzero amplitude class on Tile(1,1), with the
complete auxiliary-binary-word certificate and the explicit finite-pose
and protected-interface bridge used here. The related earlier
[standard-hat profile obstruction](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-heesch-3/hat_corona_profiles/proof.md)
is conditional on retained reference incidences and has different
geometry and depth. It does not imply this result. The earlier
[curvature resource](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-heesch-3/curvature_capacity/proof.md)
motivated imbalanced words; the present sharper local upper bound does
not require that resource theorem.

The trust boundaries are the written analytic locking, uniform
smallness and isotopy arguments, and exact standard-library Python
enumeration. No solver, external patch atlas or formal proof assistant
is used. Seven malformed certificate controls reject. All negative
searches terminate exhaustively; the checker contains no timeout.
