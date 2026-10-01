# Curvature resources and a circular-hex corona obstruction

Actual author: **six-heesch-3**, role **researcher**, 2026-10-01.

These are written proofs with compact exact finite certificates. They are
not proof-assistant formalizations or independent reviewer verdicts. No
seven-corona construction or height-record improvement is claimed.

## Conventions and results

A tile is a compact Jordan disk of positive area. Its boundary is a finite
union of regular C2 arcs, with their finitely many endpoints excluded when
measuring smooth curvature. All translations, rotations and reflections
are allowed. A complete H-corona patch consists of finite collections C_i,
0<=i<=H, where C_0 contains the root, distinct copies have disjoint interiors,
each tile in C_i touches C_(i-1), and the cumulative union P_(i-1) is contained
in the interior of P_i. The hole-free convention also requires every P_i to
be a Jordan disk. The upper arguments below allow holes in any prefix, and
therefore apply to both Hc and Hh, including holes allowed only in the last
prefix.

The first result supplies a resource without a finite port table:

**Curvature resource lemma.** Parametrize the smooth boundary
counterclockwise by arclength, and let kappa be its signed curvature.
For any bounded Borel odd function f, set

    p = integral max(f(kappa),0) ds,
    q = integral max(-f(kappa),0) ds.

If p>q, this tile has finite Heesch number. If q=0, it has no complete first
corona. If q>0, every complete patch satisfies

    p*N_(i-1) <= q*N_i,

where N_i counts copies in P_i. For certified area a>0 and squared diameter
d2, the integer lower recurrence and area upper capacity are

    m_0=1,  m_i=ceil((p/q)*m_(i-1)),
    N_i <= floor((22/7)*(d2/a)*(i+1)^2).

Any contradiction excludes depth i. A certified rational 1<alpha<=p/q may
replace p/q. In particular, the two arclength measures recording positive
curvature magnitudes and negative curvature magnitudes must agree for a
tile with arbitrarily many complete coronas. Agreement is only a necessary
condition.

The second result is a more restrictive sharp obstruction:

**Circular-hex lemma.** Let 0<beta<pi/6.

Start with a regular hexagon of side one. Assign each of its six sides a
sign sigma in {-1,0,+1}. Leave zero sides flat. Replace a nonzero side by
the circular bow of sign sigma with chord one and half central angle beta.
Let delta be the absolute difference between positive and negative side
counts. Then

    delta=1:  Hc<=Hh<=3;
    delta=2:  Hc<=Hh<=1;
    delta>=3: Hc=Hh=0.

The first two bounds are sharp, uniformly over all beta in this parameter
range: the words (0,+,+,+,-,-) and (+,+,+,+,-,-), respectively, have checked
three-corona and one-corona patches. Balanced sign counts are not classified.
Angle sums alone leave five possible exceptional parameters, but local
curvature matching at a filled junction excludes all of them. There are
no angle exceptions in the stated open interval.

## 1. Regular interfaces, including partial contacts

Let A be one tile strictly inside a finite patch. Remove from its boundary
the finite set consisting of its own arc endpoints and every arc endpoint
of every other tile in the patch. Consider a remaining point x of dA.
No other tile containing x can contain x in its interior: a small open
neighborhood would then intersect the interior of A. Thus every other tile
through x has a regular smooth boundary there.

There is at least one other tile through x. Otherwise, by finiteness and
closedness the other tiles have positive distance from x, leaving an
uncovered part of a small neighborhood on the exterior side of A. This
contradicts x being an interior point of the patch.

There is at most one other tile through x. For disjoint interiors the
tangent halfplane of any such tile must be the halfplane opposite the
interior tangent halfplane of A; a nonopposite tangent would produce an
open overlap sector. Two other regular tiles with that same interior
halfplane would overlap each other. This follows directly by representing
each regular boundary as a local graph: both interiors contain a point
in the common open halfplane sufficiently near x.

Call the unique other tile B. Tiles not containing x can be excluded from
a sufficiently small ball about x, again by finite closedness. A and B
must cover that ball and have disjoint interiors. Their boundary graphs
therefore coincide on a neighborhood of x. Their CCW orientations along
this interface are opposite, hence

    kappa_B(x) = -kappa_A(x).

This is a local argument. A single prototype arc may be subdivided among
many neighbors. It requires neither an analytic curve equation nor
coincidence of prototype arc endpoints, a lattice, or connected intersections
of pairs of tiles.

Under a reflection, the CCW traversal is reversed as well as the ambient
orientation. These two sign changes cancel: the curvature distribution of
one copy is the same as that of the prototype. In contrast, the two CCW
traversals of a common interface reverse each other, giving the displayed
minus sign even when one tile is a reflected copy.

## 2. Resource injection and finite capacity

At every regular point carrying positive density f(kappa) on a tile in
P_(i-1), the unique matched point carries the same magnitude of negative
density on another tile in P_i. This pairing is one-to-one almost everywhere:
the same negative boundary point cannot face two distinct positive tiles,
by the preceding uniqueness argument. The finitely many deleted endpoints
have zero arclength. Integrating on the disjoint union of tile boundaries
gives p*N_(i-1)<=q*N_i.

For q=0 and p>0 a strictly surrounded root is immediately impossible.
Otherwise integrality gives N_i>=m_i. Fix a point in the root. Every point
of a tile in corona i is joined back to it by a contact chain of at most
i+1 tiles; the triangle inequality bounds its distance by (i+1)*sqrt(d2).
Disjoint interiors and zero-area piecewise smooth boundaries give

    a*N_i <= pi*d2*(i+1)^2 < (22/7)*d2*(i+1)^2.

Thus the stated upper bound holds. Since m_i>=(p/q)^i with p/q>1, this
exponential eventually exceeds the quadratic capacity. The upper depth
exists by proof, rather than by interpreting an unsuccessful search.

To obtain the curvature-distribution assertion, put

    mu_+(E) = length{kappa>0, kappa in E},
    mu_-(E) = length{kappa<0, -kappa in E},    E subset (0,infinity).

If these finite Borel measures differ, some Borel E has a nonzero difference.
The bounded odd function sign(t)*1_E(|t|), or its negative, then has p>q.
So arbitrarily deep coronas force equality of the measures. The straight
part has curvature zero and contributes nothing.

The same argument excludes a whole-plane tiling directly. Congruent
positive-area, bounded-diameter tiles meeting a fixed disk form a finite
collection: all such tiles fit in a disk enlarged by the diameter, so their
disjoint areas bound their number. Contact-graph balls are therefore finite.
Every boundary point of a tile in graph ball i is surrounded by neighbors
in ball i+1. Applying the same resource and spatial capacity inequalities
again contradicts exponential growth. No global averaging assumption is
used.

## 3. The circular-hex geometry

Write unit hexagon vertices as

    v_j=(cos(j*pi/3), sin(j*pi/3)), j=0,...,5.

Side j goes from v_j to v_(j+1) in CCW order, has unit tangent e_j, and
outward unit normal n_j. Put

    R=1/(2*sin(beta)), d=R*cos(beta),
    g(t)=sqrt(R^2-(t-1/2)^2)-d,  0<=t<=1.

The signed side is v_j+t*e_j+sigma_j*g(t)*n_j. The zero side stays the
chord. The bow height is

    h=R-d=(1/2)*tan(beta/2)<(1/2)*tan(pi/12)<1/7,

and |g'(t)|<=tan(beta)<1/sqrt(3). A positive bow has signed CCW curvature
+1/R; a negative bow has -1/R. All nonzero sides have the same arclength.

The replacement makes a Jordan disk. Each bow stays within distance h of
its original side. Disjoint, nonincident edges of the honeycomb have
distance at least sqrt(3)/2, while 2h<2/7. For edges at a common vertex,
their rays are separated by 2pi/3. Each curved ray stays in the angular
cone of half-width beta around its chord ray: use
g(t)<=t*tan(beta) and g(t)<=(1-t)*tan(beta). Since 2beta<pi/3, these cones
are disjoint except at the vertex. The same argument holds while multiplying
all displacements by a parameter in [0,1]. It proves simplicity, preserves
cyclic orders, and also proves a matched honeycomb patch keeps its planar
cell embedding throughout this deformation. Its filled faces and boundary
cycle retain their disk topology.

The corner preceding side j has interior angle

    2pi/3 + (sigma_(j-1)+sigma_j)*beta.

Indeed, the outgoing tangent on side j rotates -sigma_j*beta from its chord,
and the incoming tangent rotates +sigma_(j-1)*beta from its chord. Every
corner is genuine, with angle strictly between pi/3 and pi. All other
boundary points have interior angle pi. These are intrinsic angles and
hold for reflected copies as well.

## 4. Angle-only exceptions disappear under curvature matching

At a point strictly inside a patch, the incident tile sectors fill the
whole angular circle with disjoint interiors. Let c count true corners
and s count smooth boundary points there. There is an integer M with
|M|<=2c for which

    (2c/3+s)*pi + M*beta = 2pi.                  (1)

Every corner is >pi/3, so c<=5. Also s<=2. If M=0, (1) gives exactly

    (c,s)=(3,0) or (0,2).

If M is nonzero, enumerate c=0,...,5, s=0,1,2 and -2c<=M<=2c. The
positive values (2-2c/3-s)/M below 1/6 are exactly

    1/12, 2/21, 1/9, 2/15, 4/27.

The standalone checker enumerates these rationals exactly. They are
possible exceptions for angle arithmetic alone. To remove them, use the
following local geometric condition, which is stronger than (1).

At a filled junction every sector has a positive angle. Adjacent sectors'
bounding half-arcs must coincide on an initial interval. Otherwise their
local graphs produce either an overlap or a gap. All incident tiles are
finite in number, and nonincident tiles can be excluded from a sufficiently
small neighborhood, so neither is admissible. This remains valid when
one sector is a smooth halfplane. Each coincident half-arc pair has opposite
signed curvature; in this family that means opposite side signs, with flat
matching flat. Therefore all branch signs cancel in pairs around the junction.

Each true corner contributes its two adjacent signs to M. A smooth point
of a tile contributes twice the sign tau of its one prototype side.
Writing S for the sum of these smooth-side signs, pair cancellation gives

    M + 2S = 0.                                (3)

If s=0, (3) gives M=0, and (1) forces c=3. If s=2, positivity of every
corner angle forces c=0; these are the two-smooth interfaces. Three smooth
halfplanes are impossible. If s=1, then S=tau in {-1,0,1}, and (1),(3)
give

    (2c/3-1)*pi = 2*tau*beta.

For integer c the left side has absolute value at least pi/3. The right
side has absolute value strictly less than pi/3 because beta<pi/6. This
is impossible. Thus throughout the entire stated interval the only filled
stars are three true corners with M=0, or two smooth boundaries. The
argument is uniform over all sign words. The reader also checks that
adding (3) to the finite angle enumeration leaves no exceptional ratios.
This checks the symbolic bookkeeping; the local half-arc argument remains
a written geometric proof.

For the concrete certificates take R=13/10 and d=6/5. Then h=1/10 and
tan(beta)=5/12. The parameter lies below pi/6 since 25/144<1/3. No
irrational-angle assumption or approximate trigonometric value is needed.

## 5. Whole-side and lattice locking from angles

Take one tile strictly interior to a patch. Along the open part of any
of its sides the regular-interface neighbor is locally constant. No
neighbor's true corner can occur there: a smooth point of the chosen
tile permits only the two-smooth star. The open side is connected, so
one neighbor shares it throughout.

At each endpoint there is a three-corner star. In particular both endpoints
are true corners of the side's neighbor. Since no neighbor corner occurs
inside the side, this is a whole-side correspondence. Circular signs are
opposite by curvature, while a straight side matches a straight side.

The two corresponding endpoint pairs determine a common unit chord. A
regular hexagon has exactly two possible centers adjacent to that chord.
The centers cannot be on the same side: the hexagonal skeletons would
coincide and the small bows would leave an open neighborhood of that center
inside both tiles. Therefore the neighboring centers are the two standard
honeycomb centers on opposite sides. Their hexagonal skeletons belong to
the same grid. Reflections remain allowed and only permute the sign word.

Any newly added tile touches the preceding, strictly interior prefix.
At a smooth point it is the just-described side neighbor. At a corner,
the three-corner star makes every pair of its three sectors share a local
edge; it therefore shares an initial subarc of one of that preceding tile's
sides, and the same whole-side argument applies. A tile touching only at
a point with no angular sector cannot occur, since all true corner angles
are positive. This covers the last corona, not just the interior coronas.

Consequently the grid propagates through every layer. A strictly interior
copy must have all six honeycomb neighbors present. Any new copy touches
the preceding layer, and in a hexagonal grid vertex-neighbor cells also
share a side. Induction gives exactly the honeycomb cell ball B_i in P_i,
and exactly its outer shell in C_i. In axial cell coordinates,

    B_i={(x,y): max(|x|,|y|,|x+y|)<=i},
    |B_i|=1+3i(i+1),  boundary_side_count=6(2i+1).

This assertion does not assume the final union is hole-free.

## 6. Force the remaining final-shell matches and count

Side matches incident to B_(H-1) have already been proved. At radii
H=1,2,4, every interface between two cells of the final shell has an
endpoint incident to a cell of B_(H-1). This finite geometric property is
checked using exact vertex incidences in check.py. The respective numbers
of such interfaces are 6,12,24.

At that endpoint the interior tile's two adjacent side matches cancel
their signs. The three-corner star has M=0, which is the sum of the six
incident side signs. The only two remaining signs, on the interface
between the two shell tiles, must therefore cancel too. Since the
skeletons are aligned and the two arcs have the same radius, cancelling
signs makes that whole interface coincide. Zero signs coincide as chords.
Thus all internal interfaces of B_H are matched at these radii. An
unmatched final-shell lens cannot evade the argument by becoming a hole:
it would fail the strict-interiority condition at its guarded endpoint.

Assign charge +1 to a positive side, -1 to a negative side and 0 to a
flat side. Internal sides cancel. The absolute total charge is delta*|B_H|,
while the exposed unit sides have absolute total charge at most their
number. Necessarily

    delta*(1+3H(H+1)) <= 6(2H+1).                (2)

This marked-hex counting obstruction is established prior art: Mann2004,
Section2, attributes the four-corona 61-versus54 argument to Epstein.
The present contribution is the preceding all-motion circular geometry
and final-shell justification, not a new marked-hex count.

For delta>=3, H=1 violates (2): 3*7>18. For delta>=2, H=2 violates it:
2*19>30. For delta>=1, H=4 violates it: 61>54. Any deeper complete patch
has the relevant shallower complete prefix, so these exclusions prove
the circular-hex bounds, including Hh and arbitrary allowed prefix topology.

## 7. Sharp lower witnesses and checks

three_coronas.json lists 37 copies for word (0,+,+,+,-,-), grouped by their
cell distance from the root. one_corona.json lists 7 copies for
(+,+,+,+,-,-). A world-side sign array is a rotation or reflection of the
prototype word; its cell determines its translation. The exact reader
verifies every array belongs to that dihedral orbit and every internal
side pair has opposite signs.

It reconstructs vertex and side incidences from integer axial coordinates,
checks a single boundary cycle and Euler number one at every prefix,
checks that every previous vertex star is fully filled in the next prefix,
and checks that every added copy touches the previous corona. Every old
side is also filled, since a unit edge's two endpoint stars determine both
incident cells. The matched-embedding deformation in Section 3 then
transfers these cell facts to disjoint circular tiles, disk prefixes and
strict containment. This transfer is a written geometric proof; the
integer mesh checker alone does not prove continuous geometry.

The three-corona counts are 1,7,19,37 cumulative tiles with 6,18,30,42
boundary sides. There are 90 matched internal sides in the 37-copy patch.
The fixture with excess two has one complete corona and the proved upper
one. Both witnesses work for every beta permitted by the circular-hex lemma.

For the three-corona fixture the generic curvature lemma also gives a
separate, weaker finite bound without the angle argument: all five bowed
sides have equal arclength, so p/q=3/2. The area is the regular-hex area
plus one positive circular-segment area, hence exceeds 5/2. Diameter is
at most 2+2h=11/5, so d2<=121/25. The exact lower recurrence reaches
2397 required copies at depth18, exceeding capacity2196. This independently
illustrates that the general curvature criterion remains useful even
when whole-side locking has not been established.

## Prior art and trust boundaries

- G. Domokos, A. G. Horvath, K. Regos, *A two-vertex theorem for normal
  tilings*, Aequationes Mathematicae97 (2023),185--197, first published2022.
  [Primary full text](https://link.springer.com/article/10.1007/s00010-022-00888-0),
  Section3.1 uses smooth-curvature cancellation for monohedral normal
  tilings. Cancellation is prior art. Here we give a bounded odd-curvature
  resource, a finite-corona inequality without normality/averaging, and
  a concrete angle-based circular family obstruction. No priority claim
  is made for the general cancellation principle.
- C. Mann, *Heesch's Tiling Problem*, American Mathematical Monthly111
  (2004),509--517,
  [author manuscript](https://faculty.washington.edu/cemann/Heesch.pdf).
  The bump/nick imbalance mechanism, Epstein's marked-hex upper3 count,
  and examples up to five are prior art.
  Our circular calibration at height three is not a new attainable height.
- The campaign's [earlier additive-charge certificate](../../../heesch_weighted_matching_obstruction/README.md)
  gives the contact-chain area bound and integer recurrence for atomic
  ports. We reuse that quantitative mechanism and prove a different
  continuous interface resource and an angle-based locking criterion.
- B. Basic, [six-corona construction](https://pmc.ncbi.nlm.nih.gov/articles/PMC7812982/),
  and C. S. Kaplan,
  [unmarked-polyform paper](https://arxiv.org/abs/2105.09438),
  [2025 exposition](https://arxiv.org/html/2509.12216v1), remain record context.
  The present lemmas do not improve the general finite-six record.

The proofs use standard local Jordan-boundary geometry, arclength measure,
angle sums, and elementary exact arithmetic. The checker uses CPython3.11.2
and its standard library. It does not trust the search that found the
witnesses, an external solver, approximate curvature integration, or any
published certificate executable. Six malformed controls are rejected and
a globally reflected positive control passes. The finite star/endpoint
checks and witness decoding are reproducible; the C2 interface and
deformation arguments remain unformalized written bridges. No large
artifact, private ledger, imported data corpus or generated proof log is
required.
