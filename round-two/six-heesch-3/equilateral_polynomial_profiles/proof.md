# Whole-port anchoring and arbitrary-degree polynomial profiles on Tile(1,1)

Author: **six-heesch-3**, role **researcher**, 2026-10-01.

The previously published nonflat quartic classification extends to nonzero
polynomial profiles of arbitrary degree. The new ingredient is a covered
120/240-degree endpoint that forces a whole unit-port partner. In particular,
asymmetric profiles and profiles with zero even part do not provide an escape.
This is an obstruction within one family, not a finite-Heesch record.

## Statement

Let B be the counterclockwise fourteen-unit-port polygon Tile(1,1), with
vertices and exact coordinates specified in the
[previous source](https://github.com/helgithorskarp/math_results/blob/49358db0759947485f64216bdd384b49f368b3ca/round-two/six-heesch-3/equilateral_nonflat_classification/geometry.py).
The primary polygon and the Spectre constructions are due to Smith, Myers,
Kaplan and Goodman-Strauss,
[A chiral aperiodic monotile, Section 2](https://arxiv.org/html/2305.17743v2).

For each primitive port i, choose a nonzero real polynomial P_i satisfying

    P_i(0)=P_i(1)=P_i'(0)=P_i'(1)=0.

Replace its unit chord v_i+t*(v_(i+1)-v_i) by

    v_i+t*(v_(i+1)-v_i)+P_i(t)*n_i,  0<=t<=1,

where n_i is its inward unit normal. Write R(P)(t)=P(1-t) and

    F_i = P_i       if i is even,
    F_i = R(P_i)    if i is odd.

**Theorem.** There is a constant delta>0, independent of the polynomial
degrees, such that, if

    max_i max_(0<=t<=1) (|P_i(t)|+|P_i'(t)|) < delta,

the deformed boundary is a Jordan disk T. If T admits two complete coronas,
then the functions F_i satisfy at least one of the following four systems:

* A: F_i=-F_j on the pairs
  `(0,8),(1,9),(2,6),(3,12),(4,11),(5,10),(7,13)`;
* B: F_i=-F_j on the pairs
  `(0,2),(1,13),(3,12),(4,11),(5,10),(6,8),(7,9)`;
* C: F_i=-F_j on the pairs
  `(0,8),(1,9),(2,3),(4,10),(5,11),(6,12),(7,13)`;
* S: F_i=(-1)^i*Q for one nonzero polynomial Q.

Each system supplies a tiling of the plane. Consequently every non-tiler
in this family has Hc,Hh<=1. The three periodic systems are necessary as
a union, rather than a claim that every two-corona tile is a Spectre.

Copies may undergo all Euclidean motions, including reflections. A complete
corona strictly places the preceding closed union in the interior of the
enlarged union, and its added copies touch the preceding corona. The upper
argument permits holes even in intermediate prefixes, so it applies to both
[Kaplan's Hc and Hh conventions](https://cs.uwaterloo.ca/~csk/heesch/).
Zero polynomials, nonpolynomial profiles, and amplitudes outside the uniform
small neighborhood are not covered. No numerical delta is supplied.

## 1. Covered corner angles anchor one end of each port

In units of thirty degrees, B has consecutive corner angles

    8,3,4,6,4,9,4,3,4,9,4,3,8,3.

The endpoint slope conditions preserve these angles under deformation.
Call the even-index vertices red: their angles are 120 or 240 degrees.
The odd-index vertices are blue: their angles are 90, 180 or 270 degrees.
Every primitive port has exactly one red endpoint.

At a point strictly inside a finite union of copies with disjoint interiors,
the tangent sectors of all incident copies partition the full circle. Each
sector has angle at least ninety degrees. An interior point of a primitive
arc has sector angle 180 degrees. At a red corner, an incident copy cannot
have such a regular point: a 240-degree corner already overlaps its
180-degree sector; a 120-degree corner would leave sixty degrees, smaller
than any possible further incident sector.

Thus at a covered red vertex all incident copies have primitive vertices
there. The complete lists of angle partitions of a full circle are

    120+120+120; 120+240;
    90+90+90+90; 90+90+180; 90+270; 180+180.

No partition mixes red and blue angles. Accordingly covered vertices
preserve the red/blue endpoint type. The exact reader derives the corner
angles from the polygon's chord directions and exhausts these partitions.
The prohibition of a smooth neighbor at a covered 120/240-degree corner
also appears in the team's
[unmarked-polyhex geometry](https://github.com/helgithorskarp/math_results/blob/dc503e7c728a11e64d7e3cd715134718fa3373cd/round-two/six-heesch-2/proof.md).
Here half of the corners have different angles, and the polynomial
coincidence argument below is needed to anchor every primitive port.

## 2. Polynomial coincidence and the whole-port partner

Every nonzero P_i has degree at least four. In orthonormal coordinates
attached to one source chord, its arc is the graph `(t,P(t))`. An isometry
gives coordinates

    X=alpha*t+beta*P(t)+c,
    Y=gamma*t+zeta*P(t)+d.

Suppose an open part of this arc coincides with a target graph `(s,Q(s))`.
The polynomial identity `Y=Q(X)` then holds for all real t. If beta is
nonzero, its right side has degree `degree(P)*degree(Q)>degree(P)`, whereas
the left side has degree at most degree(P), a contradiction. Orthogonality
therefore forces beta=gamma=0 and alpha,zeta in `{+1,-1}`. The two unit
chords are parallel, and their parameter intervals project to intervals
of length one on the same chord line. This proof allows different degrees
and does not require an even profile.

Now fully surround a copy of T. Fix one port and its red endpoint v.
The old port is covered by the boundaries of finitely many neighboring
copies: its boundary cannot lie inside any neighbor's interior without
an interior overlap. Distinct polynomial arcs either have an open
coincidence or finitely many intersections, as also follows by substituting
one polynomial parametrization into the other's graph equation.
Hence some coincident neighbor primitive arc covers an interval of the
old port approaching v. By closedness that neighbor arc contains v.
Section 1 forces v to be its primitive endpoint, rather than an interior
point of its arc.

The two coincident unit parameter intervals therefore share that endpoint
and overlap on the old port's side of it. Parallel unit chords of this
kind have the same endpoints. Polynomial identity then makes their
entire arcs coincide. The neighbor interiors must be on opposite sides.
Every port of a fully covered copy consequently has a unique whole-port
partner. Uniqueness follows from disjoint interiors near any regular
point of the port.

The endpoint step matters. Set f(t)=t^2*(1-t)^2 and
P_(a,b)(t)=f(t)*(a+b*(2t-1)). For a=sqrt(5), b=1, the exact identity

    P_(a,1)(t-a/5) = P_(-a,1)(t) + 8*a/125

gives a partial coincidence of different unit primitive arcs. It does not
give a split covered port: a neighbor arc passing through a covered red
endpoint as a regular point is forbidden. The reader checks this identity
in Q(sqrt(5)); no assertion that every open coincidence is automatically
a whole-port match is used.

Once both ports adjoining a covered blue corner have their whole
partners, a regular neighboring arc cannot pass through that corner
either. For a 270-degree old corner, the 180-degree regular sector is
already too large. For old angle 90 or 180, the displayed partitions
show that any incident regular sector would be adjacent to an old port
in the cyclic star. It would then be that old port's whole partner and
have a primitive endpoint there, a contradiction. All copies incident
at any fully covered primitive vertex thus have primitive vertices there.

At a filled vertex, consecutive sectors share an open boundary arc near
the vertex. The polynomial coincidence argument makes their chord axes
parallel. Since all prototype chord directions are multiples of thirty
degrees, it propagates the thirty-degree rotation/reflection group
through the cyclic star, including a copy touching an old tile only at
that vertex.

## 3. Uniform transfer to the existing finite reference domain

Normalize the root to identity. Every incident neighbor of a fully
covered tile is now aligned at a primitive vertex and belongs to the
same finite reference pose set R as in the
[quartic proof, Section 1](https://github.com/helgithorskarp/math_results/blob/49358db0759947485f64216bdd384b49f368b3ca/round-two/six-heesch-3/equilateral_nonflat_classification/proof.md).
Any tile touching an old port at a non-vertex point is its whole partner
and also touches its endpoints. Other incident tiles occur at old
vertices. Extra copies touching only a covered regular old point have
no free tangent sector. The normalized first-prefix poses are therefore
in R; second-layer poses used to cover them belong to the finite set
`U={compose(r,s): r,s in R union {identity}}`.

Uniform smallness has no degree dependence. The C1 bound gives

    |P_i(t)| <= delta*min(t,1-t),

so every endpoint arc lies in a narrow cone around its chord. Distinct
incident chord rays stay separated. Distinct nonincident edges of the
single prototype have positive separation. This supplies a positive
uniform Jordan threshold. For each reference pair from U with positive
interior overlap, fix a point a positive distance inside both reference
interiors. The minimum of these finitely many distances is positive.
Small boundary displacement preserves winding number at these points,
so a hypothetical deformed packing cannot have such a reference overlap.
These are the same finite-overlap witnesses used in the preceding proof;
only the bound on displacement has changed.

Between a fully covered old copy and an incident copy, a proper reference
vertex/chord T incidence is excluded by the covered reference star and
the chord's full partner, exactly as in that proof. Full shared old
chords carry the actual opposite profile equations. This gives all
necessary protected relations used by the existing certificate.
No whole-port or profile equality is imposed between two unfilled
final-corona copies. They may leave gaps, holes or pinches; the upper
certificate tests only their positive reference overlaps and occupied
angles at tested old vertices.

## 4. Removing reversal by endpoint color

If ports i,j have a protected match with equal parameter directions,
their two red endpoints coincide in the same order, so i,j have the
same parity. If their parameter directions are reversed, i,j have
opposite parity. Therefore the reversal bit is `(i+j) mod 2`, and

    P_i(t) = -P_j(t)       for equal parity,
    P_i(t) = -P_j(1-t)     for opposite parity.

Both are precisely `F_i=-F_j`. Let G be the graph of all such protected
port-label relations in a hypothetical two-corona patch. Each F_i is a
nonzero polynomial. An odd cycle in G would force F_i=-F_i and is
impossible. Thus G is bipartite. A generic t0 in `(0,1)` avoids the
finitely many zeros of all fourteen F_i and supplies a nonzero scalar
label `c_i=F_i(t0)` with `c_i=-c_j` on every edge.

The finite certificate in
[the previous proof, Sections 4--5](https://github.com/helgithorskarp/math_results/blob/49358db0759947485f64216bdd384b49f368b3ca/round-two/six-heesch-3/equilateral_nonflat_classification/proof.md)
depends only on these opposite-sign equations and the protected
reference geometry. Its purely graph-theoretic conclusion is that G
entails one of the seven-pair systems A,B,C or the alternating system S.
For clarity, its logic is:

1. The positive-imbalance auxiliary-word cuts force every component of G
   to have equal bipartition sizes. They use the earlier
   [complete quartic sign certificate](https://github.com/helgithorskarp/math_results/blob/94a706a0394f2142641896b71aa422db9d586979/round-two/six-heesch-3/equilateral_hat_bows/proof.md).
2. All 842 balanced first prefixes are exhausted. The local and
   three-node sector cuts force every binary coloring of G into the
   union of three periodic color classes and the alternating pair.
3. The complete balanced-component coarsening check has only four
   exceptional first prefixes; their covered-sector cuts force a
   component merger. This places the full color cube in a single class.
4. Two labels opposite in every independent component coloring must be
   in opposite sides of the same component. The corresponding equation
   therefore holds for functions F_i, not just for the evaluated c_i.

These steps require no quartic curvature, equal physical amplitudes, or
assumption about final/final profile coincidences. The original reader
must be run as a dependency; the new reader does not replace its census.

## 5. Exact matching of the plane constructions

The previous source proves three whole-port periodic reference tilings.
For each listed partner pair its reversal is exactly `(i+j) mod 2`.
The new reader directly checks these reversal bits and all 28,28,56
base-port partners from the literal periodic fixtures. Accordingly
systems A,B,C make the actual polynomial arcs coincide in those same
periodic tilings.

A sufficiently small C1 deformation preserves their periodic embedded
edge graphs: finitely many nonincident edge pairs in a fundamental
neighborhood have positive separation, and endpoint cones preserve
cyclic order. Shared edges receive the same polynomial arc. The periodic
graph deformation extends to its faces, maintaining the tiling of the
plane. Its uniform threshold also has no degree dependence; include it
in the choice of delta. No bounded patch is used as evidence of a plane
tiling here; the complete repeated reference systems are already proved.

For S the original profiles are

    P_i=Q           for even i,
    P_i=-Q(1-t)     for odd i.

This is precisely the alternating common-path Spectre construction in
the primary Lemma 2.1. Since Q is nonzero and the small deformation gives
a simple boundary, that published construction supplies a plane tiling.
In particular an antisymmetric Q, with Q(1-t)=-Q(t), puts the same
nonzero profile on every port; it is the primary s-curve construction.
Neither construction is claimed as new.

This completes the theorem. The new result is the degree-independent
covered-endpoint bridge and its combination with the existing two-corona
sign-graph classification. It closes the sufficiently small all-nonflat
polynomial lane. A finite-seven construction must use a different
reference geometry, a flat or nonpolynomial interface, or leave this
small neighborhood.

## Reproduction and status

From the repository root run the complete existing reader, then the new
finite-hypothesis reader:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
python3 -B round-two/six-heesch-3/equilateral_nonflat_classification/check.py --expected
python3 -B round-two/six-heesch-3/equilateral_polynomial_profiles/check.py --expected
```

The second command checks polygon corner types, every full-circle angle
partition, all periodic reversal conditions, and the exact partial-alias
identity. The unbounded polynomial-degree argument, covered-star
topology and uniform-smallness proof are written arguments, not claims
of proof-assistant formalization. The dependency's exhaustive finite
certificate is unchanged. Author proof; independent review pending.
