# Independent one-vertex obstruction and connectedness proof

Actual author six-reviewer-5, independent mathematical reviewer. The complete
defining proof of LEMMA9741 was visible. The following new argument and exact
core are written before reading that target's executable or certificate.
Unchanged owned REVIEW9717 routines are credited, not claimed freshly independent.

Let X be at least four distinct unit vectors, all pair products at most c,
0<c<1. Use the COMPLETE contact graph and minor geodesic edges. Every face
below is an actual simple disk. Quadrilaterals are convex in an open hemisphere.

Contact arcs embed: a transverse crossing and the nearer endpoints give a
strictly shorter pair; overlaps or interior point vertices do likewise. A
contact triple has Gram matrix (1-c)I+cJ. A normalized nonnegative combination
of its vertices has a weighted mean product at least sqrt((1+2c)/3)>c.
Thus no other packing point lies in the small triangle. Since N>=4, the other
disk contains another point. Actual triangles have angle
alpha=arccos(c/(1+c)), between pi/3 and pi/2. Tangent neighbor separation gives
degree at most five. These are ordinary spherical arguments, not code claims.

For a convex hemispheric equilateral quadrilateral all angles lie in (0,pi).
Zero would identify two neighbors. At a flat angle at A, its neighbors D,E
have D+E=2cA. The opposite vertex C contacts both, forcing C.A=1 and C=A,
contrary to distinct boundary points. Its minor diagonals are consequently
inside its disk, except at their endpoints. A diagonal cannot contact: that
would be an edge of the COMPLETE graph through the face interior. Thus its
diagonals have product STRICTLY less than c. At any corner b, its two adjacent
neighbors therefore have product c^2+(1-c^2)cos(b)<c, so b>alpha.

The classical spherical-rhombus identity is cot(a/2)cot(b/2)=c for adjacent
angles. To justify it here, reflect the two vertices off the diagonal in the
plane of that diagonal. The two unit solutions of the contact-plane equations
are precisely those distinct vertices. The diagonal lies in the convex disk
and splits it into congruent isosceles triangles. The angle cosine law in one
half gives cos(a/2)(1+cos b)=c sin(a/2)sin b; division uses positive factors.
No irreducibility theorem or optimizer hypothesis is imported.

NEW LEMMA: if a vertex has the entire star TQQ, then c<1/sqrt(5). In particular
for c>=1/sqrt(5) such a star is impossible, with NO assumption at any other
vertex, global connectivity, minimum degree, or face counts.

Indeed let a1,a2 be its quadrilateral angles, and choose an adjacent angle bi
in each quadrilateral. Put A=cot(alpha/2)=sqrt(1+2c), x=cot(a1/2), y=cot(a2/2).
Since bi>alpha, cot(bi/2)<A, and the rhombus identity gives x>c/A and y>c/A.
The complete star gives (a1+a2)/2=pi-alpha/2, hence xy+A(x+y)=1.
All variables are positive, so

\[
1=xy+A(x+y)>c^2/(1+2c)+2c.
\]

Clearing the positive denominator yields 5c^2<1. This includes the equality
threshold: strict actual-face diagonals make the last inequality strict.
The old 9/20 band lies strictly above the threshold, because
(9/20)^2-1/5=1/400. This proves original Lemma A after dropping its ENTIRE
second-endpoint requirement. We do not claim the threshold is physically sharp.

Boundary control: at c=1/sqrt(5), take A=(0,0,1) and five points
(2/sqrt(5) cos(2pi j/5), 2/sqrt(5) sin(2pi j/5),1/sqrt(5)). All five radial
and five consecutive rim pairs contact; other rim products are -c. The five
small triangles form A's full star. Merging two pairs into convex hemispheric
quadrilaterals gives a fake TQQ star only after deleting two actual radial
contacts. Those contacts are diagonals of the fake quadrilaterals. This is a
valid packing and an INCOMPLETE drawing control, not a counterexample to the
lemma. It explains why completeness is used at the threshold. At c=1/7 the
classical six-point triangular prism does have actual TQQ stars; the new
positive-c restriction cannot simply be deleted.

The original three second-endpoint systems remain valid. Write U=(x+y)/A,
B_t/A=1, c/(1+2c), (c-1)/(1+3c), for t=1,2,3. The two linear equations give
U=(1-c^2)/((1+2c)(1+c B_t/A)), P=1-(1+2c)U. Its discriminant is
(1+2c)U^2-4P. Degree-bounded exact interpolation after clearing the positive
denominators reconstructs the complete degree2,3,4 numerators; rational
Bernstein coefficients are strictly negative on [9/20,1]. Algebra at c=1
is a sign endpoint only, not a physical packing. This audits every original
case without using the original executable or certificate.

CONNECTEDNESS: retain all original N15/T11/Q3/P3 physical hypotheses: complete
contact graph connected, minimum degree3, every face simple disk length3..5,
nontriangles convex and hemispheric, c in CLOSED [9/20,19/31]. Import the
explicit wider parent facts from owned REVIEW9717/LEMMA9681. They give point
coverage; disconnected incidence has two disjoint three-face annuli; all pair
intersections in each are three full edges with disjoint endpoints and no
triple intersections; complement has two disk caps and a middle annulus with
no interior point vertices. Each boundary has three mixed vertices; each
mixed cap vertex has exactly one triangle sector and its two nontriangles.
These imported facts are already sufficiently reviewed. They are NOT
established here for arbitrary optimizers or a broader c band.

For every three-face annulus, orient each face coherently, normalize its
incoming edge to (0,1), and its disjoint outgoing edge to (k,k+1), where
q in {4,5}, 2<=k<=q-2. Reverse edge orientation in the gluing. The two unglued
tracks are 1->...->k and k+1->...->q-1->0. The first endpoints glue to first
endpoints and second to second, in opposite face-cycle order. Thus there are
two boundary cycles, and EVERY seam has one endpoint on each. No extra
identifications are permitted by the parent. The literal 3^3=27 typed-port
domain is complete, without any symmetry quotient. The owned dart successor
method independently records all quotient classes, every external successor,
both full cycles and all81 endpoint-to-boundary assignments.

If an annulus has two Qs, their common seam has a cap endpoint. Its full star
is TQQ, contradicting the new local lemma, since c>=9/20>1/sqrt(5). Each
annulus has at most one Q. Two annuli cannot contain the required Q3.
Nontriangle incidence is therefore connected throughout the original AND
expanded closed bands; point coverage is the credited parent fact.

This proves the target A--C in the stated scope and a stronger one-vertex
local filter. It says nothing about an optimizer satisfying the cohort,
any connected map containing G20/G22, the unfinished G20 interval census,
global Tammes15 optimality, or historical priority. All spherical, diagonal,
topological and finite-to-physical bridges remain ordinary unformalized proofs.
