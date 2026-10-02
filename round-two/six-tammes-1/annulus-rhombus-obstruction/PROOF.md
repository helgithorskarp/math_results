# A quadrilateral seam obstruction forces connected nontriangle incidence

Actual author **six-tammes-1**, role **researcher**, 2026-10-02, pass20.
The local obstruction below is proved by spherical geometry and exact
algebra. Its application refines committed LEMMA9681; all of that map
cohort's geometric hypotheses remain explicit. The two exact implementations
here are by the same researcher. Independent review of this new packet is
pending. No global Tammes-15 upper bound is claimed.

## 1. Statements and physical conventions

Let \(X\subset S^2\subset\mathbb R^3\) be a finite set of distinct unit
vectors, with \(|X|\ge4\) and
\[
 x\cdot y\le c\quad(x\ne y).
\]
The **complete contact graph** has every point of \(X\) as a vertex and
every pair with dot product exactly \(c\) as an edge. Draw its edges as
the minor geodesic arcs of length \(d=\arccos c\). A triangular or
quadrilateral face below is an actual face of this drawing, whose closure
is a simple disk with respectively three or four distinct boundary
vertices. Sectors in a vertex's star mean all consecutive sectors of this
complete drawing, counted once each.

**Lemma A (shared quadrilateral edge).** Suppose \(9/20\le c<1\).
Two distinct quadrilateral faces \(Q_1,Q_2\), each geodesically convex
and contained in an open hemisphere, cannot share an edge \(AB\) with
both of the following properties:

1. The entire star at \(A\) consists of \(Q_1,Q_2\) and one actual
   triangular face.
2. Every sector at \(B\) other than \(Q_1,Q_2\) is an actual triangular
   face.

Convexity initially permits flat corners; the proof excludes them for an
equilateral quadrilateral at positive \(c\). There is no assumption about
optimizer irreducibility or global face counts in Lemma A.

Define the **nontriangle incidence graph** to have one vertex per actual
nontriangular face, with two vertices adjacent when the closures share a
point vertex of \(X\).

**Theorem B (conditional fifteen-point connectedness).** Suppose
\(|X|=15\), \(1/2\le c\le3/5\), and its complete contact drawing is
connected, has minimum degree three, and satisfies:

- Every face closure is a simple disk with three, four or five distinct
  boundary vertices.
- Every nontriangle closure is geodesically convex and contained in an
  open hemisphere.
- There are exactly eleven triangular, three quadrilateral and three
  pentagonal faces, denoted T11/Q3/P3.

Then the nontriangle incidence graph is connected. Every point belongs to
the union of these six nontriangle boundaries. The theorem applies to all
degree profiles in this stated cohort, removing the degree-profile caveat
in LEMMA9681's earlier connectedness consequence.

The hypotheses of Theorem B have not been established for every optimizer.
The conclusion does not supply a particular G20 or G22 subgraph, a joint
neighbor, or a global optimality proof.

## 2. Contact angles and the rhombus identity

Throughout Lemma A, \(0<c<1\), so \(0<d<\pi/2\). Distinct contact
arcs cannot cross: at an interior crossing choose the nearer endpoint of
each arc. Their distances to the crossing sum to at most \(d\); the
geodesic triangle inequality is strict for transverse great circles,
giving a forbidden pair at distance less than \(d\). Collinear overlap
of distinct edges would put one endpoint in another edge's interior,
also producing a shorter pair. A third point cannot lie in an edge's
interior for the same reason. Thus the drawing is embedded.

A contact triple \(u,v,w\) has Gram matrix
\((1-c)I+cJ\), which is positive definite. Its smaller hemispheric
triangle contains no other packing point. Indeed a unit point in that
triangle is \(z=r/\|r\|\), with
\(r=\lambda_1u+\lambda_2v+\lambda_3w\), \(\lambda_i\ge0\),
\(\sum\lambda_i=1\). If \(z\cdot u,z\cdot v,z\cdot w\le c\),
then \(\|r\|=z\cdot r\le c\). But
\[
 \|r\|^2=c+(1-c)\sum\lambda_i^2\ge(1+2c)/3>c^2,
\]
where the final strict inequality is
\((1-c)(1+3c)>0\). The larger complementary disk contains the fourth
packing point and therefore cannot be an actual triangular face. Hence
every actual triangle has angle
\[
 \alpha=\arccos\frac{c}{1+c},\qquad \pi/3<\alpha<\pi/2.       \tag{1}
\]

At any contact vertex two different contact neighbors have tangent
directions separated by a smaller angle at least \(\alpha\): their dot
product is \(c^2+(1-c^2)\cos\gamma\le c\). Each successive directed
gap is therefore at least \(\alpha\). The degree is at most five, since
\(6\alpha>2\pi\).

For a convex hemispheric equilateral quadrilateral every angle is in
\((0,\pi]\). A zero angle would identify its two neighboring vertices
(same tangent direction and distance \(d\)). A flat angle at \(A\)
would give neighbors \(D,E\) with opposite tangent directions and
\(D+E=2cA\). The quadrilateral's opposite vertex \(C\) contacts both,
so \(C\cdot(D+E)=2c\) and \(C\cdot A=1\), forcing \(C=A\),
contrary to the simple boundary. Thus all its angles lie in \((0,\pi)\).

If \(a,b\) are adjacent angles of such a quadrilateral, its diagonal
splits it into two congruent isosceles triangles. Opposite quadrilateral
angles are equal; in one triangle the angles are \(a/2,b,a/2\).
The spherical cosine law for angles, applied to a side of length \(d\),
gives
\[
 \cos(a/2)(1+\cos b)=c\sin(a/2)\sin b,
 \qquad \boxed{\cot(a/2)\cot(b/2)=c}.                        \tag{2}
\]
All divisions here are by positive quantities. This is the classical
spherical-rhombus identity, also recorded in Musin--Tarasov,
[Proposition 4.1(5)](https://arxiv.org/pdf/1312.5450). It is not claimed
as a new result. The explicit convex hemispheric conditions above justify
its use without importing an irreducibility theorem.

## 3. Exact proof of Lemma A on the broader interval

Let \(a_i\) and \(b_i\) be \(Q_i\)'s angles at \(A\) and \(B\),
respectively, and write
\[
 \phi=\alpha/2,\quad A_0=\cot\phi=\sqrt{1+2c},\quad
 x=\cot(a_1/2)>0,\quad y=\cot(a_2/2)>0,\quad S=x+y,\ P=xy.
\]
The full star at \(A\) gives \(a_1+a_2=2\pi-\alpha\), hence
\[
 P+A_0S=1.                                                  \tag{3}
\]
At \(B\), let \(t\) be the number of triangular sectors. There is at
least one, since the two quadrilateral angles are each less than \(\pi\).
The degree bound gives \(t\le3\). Thus **all possibilities are**
\(t\in\{1,2,3\}\). From (2) the cotangents at \(B\) are \(c/x,c/y\),
and \(b_1+b_2=2\pi-t\alpha\) gives
\[
 P-c^2=cS B_t,\qquad B_t=\cot(t\phi).                       \tag{4}
\]
Cotangent addition gives the exact values
\[
 B_1=A_0,\qquad B_2=c/A_0,\qquad
 B_3=A_0(c-1)/(1+3c).
\]
No pole is crossed: \(\phi\in(\pi/6,\pi/4)\) and
\(t\phi\in(0,3\pi/4)\). In particular
\[
 A_0+cB_1=A_0(1+c),\quad
 A_0+cB_2=(1+c)^2/A_0,\quad
 A_0+cB_3=A_0(1+c)^2/(1+3c)
\]
are strictly positive. Solving (3)--(4) gives
\(S=(1-c^2)/(A_0+cB_t)\), \(P=1-A_0S\). Necessarily
\(S^2-4P=(x-y)^2\ge0\). Substitution yields:

| \(t\) | \(S\) | \(P\) | \(S^2-4P\) |
|---:|:---|:---|:---|
| 1 | \((1-c)/A_0\) | \(c\) | \((1-6c-7c^2)/(1+2c)\) |
| 2 | \((1-c)A_0/(1+c)\) | \(2c^2/(1+c)\) | \((1-11c^2-6c^3)/(1+c)^2\) |
| 3 | \((1-c)(1+3c)/(A_0(1+c))\) | \(c(3c-1)/(1+c)\) | \((1+8c-2c^2-40c^3-15c^4)/((1+2c)(1+c)^2)\) |

Each denominator is positive on the closed algebraic interval
\([9/20,1]\). Each numerator is strictly negative there. For example,
at \(9/20\) their values are, respectively,
\(-1247/400,-7097/4000,-2083/32000\). Their derivatives are strictly
negative on \([9/20,1]\); for the third,
\(8-4c-120c^2-60c^3<0\), already because
\(120(9/20)^2>8\). The first two derivative signs follow immediately
from \(-6-14c<0\) and \(-22c-18c^2<0\).

Alternatively, their Bernstein coefficients on \([9/20,1]\) are:

| \(t\) | exact Bernstein coefficients of the numerator |
|---:|:---|
| 1 | \(-1247/400,\ -13/2,\ -12\) |
| 2 | \(-7097/4000,\ -1703/400,\ -26/3,\ -16\) |
| 3 | \(-2083/32000,\ -5289/1600,\ -6173/600,\ -119/5,\ -48\) |

Since the Bernstein basis is nonnegative and sums to one on the closed
interval, these certify the strict signs including its endpoints. This
contradicts \((x-y)^2\ge0\) in all three cases and proves Lemma A.
The certificate's algebra includes \(c=1\) only as a sign-check endpoint;
physical Lemma A excludes \(c=1\) and its coincident-point degeneracy.

## 4. A second geometric proof for \(1/2\le c<1\)

For one quadrilateral put \(u=\cot(a/2)>0\), \(v=\cot(b/2)>0\).
Equation (2) gives \(uv=c\), \(u+v\ge2\sqrt c\) and
\[
 \cot((a+b)/2)=\frac{c-1}{u+v}\ge\frac{c-1}{2\sqrt c}.
\]
The cotangent is strictly decreasing on \((0,\pi)\), so
\[
 a+b\le4\operatorname{arccot}\sqrt c\le2\pi-2\alpha
       \quad(c\ge1/2).                                    \tag{5}
\]
The second inequality follows by comparing cotangents on
\((\pi/2,\pi)\) and squaring positive quantities:
\[
 (1-c)^2(1+2c)\le4c^3
 \quad\Longleftrightarrow\quad
 4c^3-(1-c)^2(1+2c)=(2c-1)(1+c)^2\ge0.                     \tag{6}
\]
It is strict for \(c>1/2\). The two endpoint stars in Lemma A have total
quadrilateral angle sum \(4\pi-(1+t)\alpha\ge4\pi-4\alpha\)
because \(t\le3\). Summing (5) for the two quadrilaterals contradicts
this when \(c>1/2\). At \(c=1/2\) equality would be necessary in both
rhombi, so \(u=v=\sqrt c\) in each. Their angles at \(A\) would both
equal \(\pi-\alpha\), whereas the actual star requires their sum to be
\(2\pi-\alpha\), again impossible. This independently proves the part
of Lemma A used in Theorem B.

## 5. Every annulus seam joins its two boundary components

The earlier source for committed LEMMA9681 is
[two-corner-incidence/PROOF.md](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-1/two-corner-incidence/PROOF.md).
Under exactly Theorem B's hypotheses it proves these necessary facts:

- Every packing point lies on a nontriangle, and every nontriangle
  incidence component has at least three faces.
- Disconnected incidence therefore consists of two components of three
  faces. In each, every pair of faces shares exactly one whole edge.
  The three shared edges have disjoint endpoints, there are no triple
  point intersections, and all other boundary vertices remain distinct.
- Each three-face union is an annulus. The two annuli have disjoint
  physical point sets; their complement is two triangulated disk caps
  and one triangulated annulus, with no interior point vertices.
- Each annulus boundary has exactly three mixed vertices, belonging to
  two of its nontriangles. At the boundary adjacent to its disk cap,
  each mixed vertex has exactly one triangular sector and hence degree
  three. Each annulus borders one of the two disk caps.

These are premises from that committed source, not fresh global-map
coverage claims. For completeness, the cap conclusion follows from
\(\ell-2\) triangles in a disk with \(\ell\) boundary points and no
interior points. Its \(3\ell-6\) corner incidences are at least one
at each of the three mixed vertices and at least three at each of the
\(\ell-3\) single-nontriangle vertices (whose complementary star has
angle at least \(\pi>2\alpha\)). Equality forces every mixed vertex
to have exactly one cap triangle. All other sectors at that point are
the two nontriangles in its component.

The new seam fact is elementary and holds for this normalized gluing.
Orient the sphere and label the three faces cyclically. On face \(i\)
let the incoming edge be \((0,1)\), the outgoing edge
\((k_i,k_i+1)\), where \(q_i\in\{4,5\}\) and
\(2\le k_i\le q_i-2\). Orientation reversal along a common edge gives
\[
 (i,k_i)\sim(i+1,1),\qquad (i,k_i+1)\sim(i+1,0),
 \quad i+1\pmod3.                                         \tag{7}
\]
The unglued boundary of each face has two tracks:
\[
 1\longrightarrow2\longrightarrow\cdots\longrightarrow k_i,
 \qquad
 k_i+1\longrightarrow\cdots\longrightarrow q_i-1
                  \longrightarrow0.
\]
The first identification in (7) connects only first-track endpoints;
the second connects only second-track endpoints. First tracks run around
the faces in order \(0,1,2\), and second tracks in order \(0,2,1\).
They give two disjoint simple boundary cycles. **The two endpoints of
every shared edge lie on different cycles.** No extra identifications are
available under the preceding physical incidence facts.

There are exactly \(27\) labeled port triples, without any symmetry
quotient: each face has the three typed-port choices \((4,2),(5,2),(5,3)\).
The new certificate checks every quotient class, every directed boundary
arc, both complete cycles, all \(81\) seam endpoint pairs and all
\(54\) mixed-corner counts. The producer uses literal disjoint pairs
and the two tracks just described. The auditor uses union-find, base-three
typed-port enumeration and undirected degree-two boundary walks. The
ordinary two-track argument, rather than a count alone, is the geometry
bridge to the physical annuli.

## 6. Proof of Theorem B

Assume disconnected incidence. The parent facts give two three-face
annuli. If two quadrilateral faces belong to the same component, they
share one of its seams \(AB\). By Section 5 that seam has one endpoint
on the boundary bordering the disk cap; call it \(A\). Its entire star
is exactly those two quadrilaterals and one cap triangle. At the other
endpoint \(B\), the same two faces are its only nontriangles: there is
no triple point intersection, no contact with the other component, and
all remaining faces of the physical map are triangles. Thus Lemma A
applies and excludes that seam.

Each three-face annular component would contain at most one quadrilateral.
The two components could then contain at most two quadrilaterals, in
contradiction to Q3. This proves connectedness for the entire cohort.
The point-coverage assertion is the corresponding parent premise.

In particular **both** prior disconnected residuals QQQ+PPP and QQP+QPP
are excluded, including the earlier possible degree profiles
\((n_3,n_4,n_5)=(6,3,6)\) and \((7,1,7)\). We do not need to find a
G22 motif inside their complementary triangle annuli: those residuals
cannot occur under the given hypotheses. The connected-incidence case
and optimizer coverage remain to be addressed.

## 7. Calibration, reproducibility and limitations

The local prohibition must not be extended to all positive \(c\). A
classical triangular prism at \(c=1/7\) has six points
\[
 U_i=\left(\frac2{\sqrt7}\cos\frac{2\pi i}3,
           \frac2{\sqrt7}\sin\frac{2\pi i}3,\sqrt{\frac37}\right),
 \qquad
 V_i=\left(\frac2{\sqrt7}\cos\frac{2\pi i}3,
           \frac2{\sqrt7}\sin\frac{2\pi i}3,-\sqrt{\frac37}\right).
\]
Their complete contact graph has the two three-cycles and the three
matched vertical edges: nine contacts with dot product \(1/7\), and
six strict noncontacts with dot product \(-5/7\). Radial projection of
the convex triangular prism (which contains the origin in its interior)
gives the two actual triangular faces and three convex hemispheric
quadrilateral faces. The supporting face planes have positive distance
from the origin, so their radial projections lie in open hemispheres.
Every vertical edge has TQQ at both endpoints. The \(t=1\) discriminant
in Section 3 is exactly zero at \(c=1/7\), as it should be. This
calibration is not a new construction or an application of Lemma A.

See [README.md](README.md) for exact replay commands,
[DEPENDENCIES.md](DEPENDENCIES.md) for source/graph dependencies,
[LITERATURE.md](LITERATURE.md) for primary prior work, and
[VALIDATION.json](VALIDATION.json) for complete normal/optimized results
and actual costs. [controls.py](controls.py) rejects twenty-three altered
certificates and accepts five valid representation changes. The latter
prevent interpreting canonical-byte matching as semantic verification.

All ordinary spherical, embedding, annulus, cap and code-to-statement
bridges remain unformalized. The code certifies the algebraic and finite
gluing statements under their stated predicates. It does not enumerate
all fifteen-point contact graphs, prove that an optimizer satisfies this
cohort, or provide the actual nine-triangle/simple-pentagon occurrence
predicate of the earlier
[G22 facial-injectivity interface](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-1/g22-facial-injectivity/PROOF.md).
The next precise frontier is a connected-map occurrence argument, or a
rigorous extension proving enough optimizer coverage to use Theorem B.
