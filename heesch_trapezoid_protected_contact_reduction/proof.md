# Protected corona contacts are discrete for the bowed trapezoid family

Actual author **six-heesch-3**, role **researcher**, 2026-10-01.
This is an author-validated geometric reduction, with exact finite arithmetic
and written all-motion bridges. It is not an independent review, formalization,
Heesch record or global upper bound for a changed tile.

## Shape, motions and hypotheses

Axial coordinates (q,r) mean (q+r/2,sqrt(3)r/2) in the Euclidean plane.
For an integer n>=8 let S_n be the counterclockwise convex quadrilateral

    (0,-1), (n,-1), (n-1,1), (0,1).

Subdivide its bottom into n unit chords, its top into n-1 and left side into
two. Its remaining right side has length sqrt(3) and stays straight. On each
counterclockwise unit chord v->v+e put the physical arc

    v+z*e+(s/100)*z^2*(1-z)^2*(e_y,-e_x), 0<=z<=1,

where s=-1 on the bottom and +1 on the top and left. The resulting unmarked
connected Jordan disc is T_n. These signs describe physical inward/outward
bowing; they are not externally imposed matching rules. The labelled points
are precisely the endpoints of these unit ports and of the single flat port.
All derivatives at port endpoints agree with their chord tangents.

Write R(q,r)=(-r,q+r), J(q,r)=(q+r,-r). A D6 lattice pose means R^k J^h
followed by an integer axial translation, h=0,1 and k=0,...,5. A common
Euclidean isometry transports the lattice and every statement below.

A packing is finite and has pairwise disjoint physical interiors. If A is
a subcollection write U(A) for its union. "Strict" means containment of
the entire closed union in the interior of the larger union. No disc or
hole restriction is needed for the reduction.

**Protected-contact theorem.** Let A subset B subset C be subcollections
of a finite packing by arbitrary real congruent copies of T_n, with

    U(A) subset int U(B),  U(B) subset int U(C).

Every copy in C meeting a copy of A already belongs to B. It shares, relative
to that contacted old copy, a D6 orientation and integer axial endpoint
translation. If all copies of A use one common D6 lattice, every copy of
B meeting U(A) uses that lattice. Each such additional copy has a labelled
endpoint contact with a labelled endpoint on boundary U(A).

Consequently, in any ordinary H-corona chain with H>=1 rooted at one T_n, every copy
through corona H-1 is in the root's D6 lattice. The last corona is not
asserted to be aligned. A later strict surround is an essential hypothesis
of this proof, including for copies touching only at a point.

## Atomic unit contacts and local analytic stars

We use the credited
[whole-unit quartic coincidence lemma](../heesch_weighted_matching_obstruction/quartic_realization.md),
graph7146. If physical boundary germs coincide along a nonzero interval,
the entire two unit arcs coincide, including both labelled endpoints and
opposite intrinsic bow states. It permits arbitrary real rotations,
translations and reflections. Polynomial coefficient comparison fixes the
unit tangent axis, its parameter or reversal and its endpoint pair. A flat
cannot coincide with a nontrivial quartic interval. The mechanism is
independent of n. Reflection preserves intrinsic bow state, with reversed
counterclockwise order taken into account.

If a copy is strictly interior to a finite packing union, every open unit
arc has a whole mate. No other tile can contain a point of that boundary
in its interior, since it would overlap the old interior nearby. Finitely
many noncoincident algebraic boundary arcs have only finitely many
intersections with the given arc and cannot cover it. A coincident interval
exists, hence a whole opposite mate by the atomic lemma. This applies to
both inward and outward units.

We also use the following elementary finite local-star argument explicitly.
At a point interior to a finite packing union, copies not containing that
point have positive distance and may be omitted in a small ball. Incident
copies have one-sided tangent sectors; their interiors are disjoint and
the sectors cover the tangent circle. Otherwise an open angular wedge is
overlapped or uncovered arbitrarily close to the point. For T_n the sectors
have angles60,90,120 or180, and never angle zero. The four genuine corners
have60,90,90,120, and all other boundary points are regular of angle180.

Two adjacent sectors' analytic boundary germs along their common ray must
coincide. Rotate the tangent ray to be the positive coordinate axis and
write both branches locally as analytic graphs. If they differ, the first
nonzero coefficient of their difference orders them strictly near the
point, creating a curvilinear gap or overlap. A third incident copy cannot
occupy that zero-angle gap: its sector has positive angle and would overlap
one of the already adjacent sectors. Nonincident copies are excluded by
positive distance. Thus adjacent germs coincide as physical arcs. This
argument applies also to a regular labelled unit junction, using the
separate analytic branch on each ray; global analyticity across a junction
is not assumed.

## Whole flat mating for every interior copy

The
[width-uniform three-copy obstruction](../heesch_trapezoid_uniform_strip_obstruction/proof.md),
source e91d2f09df7b46ccc1d0050648019d66d11fe5ad, graph8134, proves that a
packing containing

    O=(0,0,0,0), U=(0,0,-1,2), L=(0,0,1,-2)

cannot make O strictly interior for any integer n>=8. Other motions/topology
are unrestricted and U,L need no interiority. We now derive a new consequence.

Normalize any strictly interior old copy to O. Its flat is covered by
coincident straight-side intervals of other copies: noncoincident lines or
quartics can contribute only finitely many intersection points. The finite
union of coincident closed intervals covers the old open interval and its
closure. They all occupy the opposite local side of the line. Two such
intervals cannot overlap in positive length, since their copy interiors
would overlap on that side. All have length sqrt(3).

Equal-length intervals with disjoint interiors covering an interval of
that length give one aligned full mate, or exactly two positive-length
contributors meeting at an interior cut. In the second case both old
endpoints lie inside the new flat intervals. This is an all-offset interval
argument, not a sampled phase enumeration.

Suppose there is a split. At either old endpoint the old90 sector and a
new flat-interior180 sector leave exactly90 degrees. The complete local
star has exactly one further90 corner, since no sector is smaller than60.
The coincident-germ argument makes its charged boundary a whole opposite
unit mate and its other boundary a flat germ.

Let B0=(n,-1) and C0=(n-1,1). At B0 the remaining sector is southwest:
charged ray west, flat ray down, and charged state positive, opposite the
old bottom negative unit. At C0 it is northwest: charged ray west, flat ray
up, state negative, opposite the old top positive unit. The only90 prototype
corners are B0 (negative, flat up) and C0 (positive, flat down); both have
charged ray west. The atomic unit match restricts the filler's orientation
to D6 and fixes its endpoint translation. Checking both corners under all
twelve motions at each endpoint gives exactly

    B0 filler L=(0,0,1,-2), C0 filler U=(0,0,-1,2).

The reader checks all48 cases with coordinates affine in n. The translations
have zero n coefficient, so this is uniform, not a width sample. O,U,L then
contradict8134. A split is impossible: every strictly interior copy has an
aligned whole-flat mate. A patch covering only the root flat and leaving
another root arc exposed does not satisfy this lemma's interiority hypothesis.

## From protected vertex stars to arbitrary contact locking

First, every copy of C meeting U(A) belongs to B. A contact point x lies
in int U(B). If a copy not in B passed through x, its positive interior
sector would meet a small ball covered by U(B). The finitely many B-boundaries
have empty interior, so an interior point of a B-copy would be overlapped.
All incident copies at x are therefore in B, and strictly interior in C.

Consider a labelled vertex x of a copy P in A. All incident copies are
protected and have whole unit and flat mates in C. If x lay in the relative
interior of a smooth unit or flat port of some incident Q, Q and its whole
mate would fill a sufficiently small ball about x. A third incident copy
would overlap their interiors. P must be one of this pair. But P cannot
have a labelled endpoint at x while the other member has x in a port's
interior: whole unit mating aligns its two endpoints, and whole flat mating
does likewise. Genuine old corners are also not regular points of a mate.
This contradiction proves that x is labelled for every incident copy.

The filled star's adjacent sectors have coincident germs. Shared charged
germs give whole endpoint-aligned unit mates. Shared flat germs start at
the common labelled endpoint and both flats have length sqrt(3), so their
other endpoints align too. Unit directions in a prototype are multiples
of60degrees, and flat directions differ from90degrees by multiples of60.
Either endpoint match therefore fixes a relative D6 motion. The shared
labelled endpoint fixes an integer axial translation. Following the finite
cyclic star propagates alignment from P to every participant, including
participants that meet P only at x.

For an arbitrary additional contact Q with P, its contact point is either
labelled for P, covered above, or in an open smooth port of P. In the latter
case P and its whole mate fill a small ball there. Q must be that mate.
Its endpoints and D6 orientation are fixed, so it too contacts a labelled
endpoint of P and is aligned. Extra isolated tangencies cannot supply a
third positive-angle tile in an already filled ball.

For the corona consequence, apply the theorem successively to cumulative
prefixes P_i,P_(i+1),P_(i+2), i=0,...,H-2. Every new copy in P_(i+1) touches
the preceding corona, hence P_i. Induction from the root gives common
lattice alignment through P_(H-1). Only this direction is claimed; discrete
models need separate physical topology and corona checks for existence.

## Uniform skeleton-overlap buffer, including rational phases

For all n>=8 the primitive side directions of D6 skeletons have squared
axial norm1 or3. Their nonparallel determinants have magnitude1,2 or3.
The reader verifies the complete oriented direction set and all48 positive
affine side factors. An edge factor c+m*n has m>=0 and c+8m>0; hence the
normalization stays valid for every n>=8.

Suppose two such skeletons with translations in (1/d)Z^2 have positive-area
intersection. Their primitive supporting-line offsets lie in (1/d)Z.
The intersection is a bounded convex polygon with at most8 extreme vertices.
At every vertex two nonparallel supporting lines meet; Cramer's rule makes
their coordinate denominators divide d times1,2 or3. For each of the eight
original half-planes some intersection vertex has strictly positive slack,
since the intersection has positive area. That slack is at least1/(3d).
The average of all extreme vertices therefore has slack at least1/(24d)
in every primitive half-plane. Coincident/redundant supporting lines and
collinear nonextreme points only reduce the number of extreme vertices;
they do not invalidate this argument.

For primitive direction v, Euclidean boundary distance is

    sqrt(3)*det(v,w-a)/(2*sqrt(v_q^2+v_q*v_r+v_r^2)).

The average point is consequently at least1/(48d) inside both quadrilaterals.
For 1<=d<=33 this is at least1/1584>1/1600, the maximum quartic displacement.
During the continuous physical boundary deformation no boundary crosses
that point; winding number one is preserved, so it is in both physical
interiors. Positive-area skeleton overlap therefore implies physical
overlap on every such common rational grid. In particular the integer-grid
distance bound is1/48. The threshold33 is sufficient for this bound and is
not asserted optimal. Failure of the inequality at34 gives no conclusion
about physical overlap or packing existence.

Simple prototype boundaries throughout the homotopy and the1/1600 bound
are established in the credited8134 physical proof. The winding-number
margin mechanism also credits
[six-reviewer-4's independent shrink proof](../heesch_trapezoid_six_review4/PROOF.md),
graph8040. No reviewer executable or finite T8 classification is imported.

## Why protected shared units have complementary states

Take two protected copies in the same D6 integer grid sharing a skeleton
unit chord. If their counterclockwise chord directions agree, their skeleton
interiors overlap near its midpoint, and the buffer proves physical overlap.
They must occupy opposite sides.

If their intrinsic states agree, the first copy's whole opposite unit mate
exists in C and has D6 integer pose by the unit endpoint match. Its skeleton
occupies the same local side of the chord as the second copy's skeleton.
These two skeletons have positive-area intersection, so the integer buffer
again forces physical overlap. The mate is distinct from that second copy,
whose state on this chord was assumed equal to the first's. A single
prototype has no two distinct ports on the same unit chord. Thus shared
protected unit chords must have opposite states. Inward/inward profiles
alone leave a gap; their rejection here uses the later whole mate explicitly.
This is not a rule for two unprotected inward units in an outermost patch.

## Necessary finite inventory with one later surround

Let a fixed old subpacking A have known D6 integer poses and an embedded
full-port boundary network. Form all poses putting any prototype labelled
vertex on any labelled vertex of boundary U(A), in all twelve orientations.
This finite endpoint list contains every additional B-copy touching A in
the theorem's two-strict-surround setting. An endpoint in int U(A) cannot
be used by a distinct new copy, by the same small-ball packing argument.

The following are necessary constraints on selected new poses:

- cover every exposed old unit by a whole opposite-state unit, and every
  old flat by a whole flat with opposite counterclockwise direction;
- cover every missing old tangent-star sector at every old labelled point;
- exclude positive-area skeleton overlaps;
- exclude coincident shared chords with equal counterclockwise directions,
  or coincident shared unit chords with noncomplementary states.

The proofs above justify all four requirements under the protected-stage
hypothesis. The12 open30degree sector slots suffice after D6 alignment.
Logical unit consequences of this necessary full-arc relaxation may be used
to force mates or prune incompatible candidates. Such preprocessing requires
the same future license; it cannot silently apply to an arbitrary last layer.

An independently checked UNSAT certificate for a completely generated
inventory would thus rule out B followed by C over that specified A.
For a fixed fourth prefix this would rule out sixth-corona continuation.
It would not alone prove no fifth, a global height bound or exhaust all
fourth prefixes. This publication supplies the geometric reduction; it
does not claim a checked particular native inventory or such a new closure.

## Exact reader, scope and literature

[check.py](check.py) uses only Python's standard library and exact integer/
fraction arithmetic. It rederives all48 affine edge factors, twelve primitive
directions, determinant magnitudes, the rational margin and48 endpoint cases,
then compares [certificate.json](certificate.json). Seven malformed controls
alter critical states/endpoints/width slopes/directions/margins and must fail.
Optimized Python is explicitly rejected. The reader does not encode the
finite-cover, analytic-star, arbitrary convex-intersection or winding-number
proofs; those are the written trust boundaries above. No native solver,
constructor, old neighborhood catalog or external geometry code is imported.

[Kaplan2021/2022](https://arxiv.org/abs/2105.09438),
[the author's Hc/Hh dataset](https://cs.uwaterloo.ca/~csk/heesch/) and the full
[2025 Heesch section](https://arxiv.org/html/2509.12216v1) were refreshed live.
The connected finite-six context retains Bašić2021 credit. This reduction
neither constructs seven coronas nor settles the Euclidean finite-seven
target. No exhaustive2026 priority claim is made.
