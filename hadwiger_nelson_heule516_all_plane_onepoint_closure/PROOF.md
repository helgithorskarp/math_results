# Complete whole-plane one-point closure

Fix the labelled point set B specified by the pinned source table. Its
coordinates are integer coefficient vectors divided by 96 in the basis

    1, sqrt(3), sqrt(5), sqrt(15), sqrt(11), sqrt(33), sqrt(55), sqrt(165).

All square roots are positive. The independent square classes of 3, 5 and
11 give degree eight over Q, so coefficientwise equality is exact.
The auditor reconstructs all 132,870 unordered base distances and obtains
exactly the 2,538 declared unit edges. It also checks the base's coordinate
identity within H632.

## Completeness of the exterior candidate set

Three distinct points on a circle are noncollinear and determine its centre
uniquely. If an arbitrary real point q has at least four unit neighbours in
B, any three of them determine q. The two perpendicular-bisector equations
have coefficients in the coordinate field and a nonzero determinant. Thus
q itself belongs to that field; this is a consequence, not a restriction
on the initial candidate space.

For squared side lengths s,t,u, the condition that a nondegenerate triangle
has circumradius one is

    s*t*u = 4*s*t - (s+t-u)^2.

At coordinate denominator D=96, let S,T,U be squared-distance numerators.
The cleared polynomial condition is

    S*T*U = D^2 * (4*S*T - (S+T-U)^2).

Every unit-circle triple satisfies this identity after any ring
homomorphism evaluating the radical generators modulo an integer.
Consequently a nonzero modular evaluation can reject a triple soundly.
No modular zero is used as exact acceptance.

The C++ filter enumerates all C(516,3)=22,765,060 unordered base triples.
It uses the two homomorphisms from the earlier
[Heule510 census](../hadwiger_nelson_heule510_completion_frontier), with
moduli 60289 and 1000081 and respective images of `(sqrt(3),sqrt(5),sqrt(11))`
equal to `(4799,25141,4267)` and `(964569,816716,970601)`. The required root
squares are checked before enumeration. The first filter retains 105,930
triples and the second retains 105,755.

The producer lifts candidate centres exactly by field inversion and the
perpendicular-bisector equations. The separate auditor imports no producer
field arithmetic: it expands products by monomial exponents and verifies
all 890,616 centre-to-base distances. It checks complete neighbour lists,
forms every neighbour triple, rejects a triple assigned to distinct
centres, and compares the resulting set entrywise with the freshly
enumerated modular survivor stream. All 105,755 survivors are accounted
for; there are no modular false positives.

Any omitted real centre with at least three neighbours would supply a
surviving triple. That triple already belongs to a checked centre, which
must coincide with the proposed centre by uniqueness. This proves
whole-plane completeness. The 1,726 centres have coordinate denominators
dividing 96 in 1,714 cases and dividing 288 in the remaining twelve.
Exact comparison with the H632 coordinate set leaves 558 exterior centres
of degree at least four.

## Colouring coverage and target order

Every supplied word is checked as a proper four-colouring of B-v for its
named omitted vertex v. All 516 possible omitted vertices are represented.
For each exterior centre q, a word extends to q precisely when the base
neighbours of q other than v use at most three colours. The checker
recomputes these colour sets and records distinct covered vertices v.
The minimum coverage over all 558 centres is 508.

Let J be any subgraph of the unit-distance graph on B union {q} with at
most 508 vertices, where q is outside H632.

- If q is absent, J omits some v in B. A checked colouring of B-v
  restricts to J.
- If q has at most three unit neighbours in B, a colouring of the proper
  base subgraph J-q extends to q by choosing a missing neighbour colour.
- Otherwise q is one of the 558 certified centres. If q is in J, J uses
  at most 507 base vertices and omits at least nine. At most eight base
  vertices are uncovered. Some omitted v is covered, so a checked
  colouring of B-v+q restricts to J.

Every case gives a proper four-colouring. Edge deletions cause no difficulty
because proper colourings restrict to subgraphs.

The published h3991 theorem gives the same conclusion for all 116 points
of H632 outside B. A point already in B adds no vertex and is handled by a
base-deletion colouring. These cases complete the corollary for every
q in R^2.

The claim keeps B at its specified exact positions and adds at most one
new point. No conclusion about multipoint augmentations, moved base
vertices, or a five-chromatic target graph follows.
