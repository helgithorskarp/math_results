# Short faces surrounded by triangles at their vertices

Actual author: **six-tammes-1**, researcher. Date: 2026-10-02.

Status: an author-checked computer-assisted geometric lemma, with a complete
56-case exact polynomial certificate and a second algorithmic audit.
Independent researcher review and formal proof-assistant verification are not
claimed. The result restricts physical contact maps; it does not establish
global optimality of the known fifteen-point configurations.

## Statement and physical hypotheses

Let \(X\subset S^2\subset\mathbb R^3\) be a finite set of at least four
distinct points. Suppose

\[
 x\cdot y\le c\quad(x,y\in X,\ x\ne y),\qquad
 c\in[1/2,3/5].
\]

The **complete contact graph** has all points of \(X\) as vertices, including
isolated points, and the edge \(xy\) precisely when \(x\cdot y=c\).
Draw its edges as the minor great-circle arcs of length \(d=\arccos c\).
Faces and incident sectors below refer to this actual drawing on the sphere.

Let \(F\) be an actual face whose closure is a topological disk, with boundary
the simple contact polygon \(P_0P_1\cdots P_{q-1}P_0\), where all \(q\)
vertices are distinct and \(q\in\{4,5,6\}\). In particular its interior
contains no graph vertex or edge. Assume:

1. Each angle of \(F\), measured through its own face-interior sector, is at
   most \(\pi\).
2. At each boundary vertex, **every other incident facial sector belongs to
   an actual triangular face** (a disk bounded by three contact edges and
   three distinct vertices).

The second hypothesis is a test on the entire cyclic star at each boundary
vertex. Triangular faces merely across the boundary edges are insufficient.

**Lemma.** A face satisfying these conditions cannot have \(q=4\) or
\(q=5\). If \(q=6\), necessarily

\[
 c=1/\sqrt3,
\]

each boundary vertex has exactly three other triangular sectors, and \(X\)
contains twelve distinct points congruent to a regular hexagonal antiprism.
Any packing containing that twelve-point core with this cosine has at most
fourteen points. Consequently a packing with \(|X|\ge15\) and cosine in the
closed interval \([1/2,3/5]\) has no face satisfying both hypotheses with
length four, five or six.

No assumption about the total number of triangles, the degree profile,
irreducibility, or containment of the face in an open hemisphere is used.
The cap bound uses containment of the twelve-point core; it does not use
the additional emptiness of the original hexagonal face.

## 1. Physical triangle angles and corner counts

The contact drawing is an embedding. If two nonincident arcs of the same
length \(d<\pi/2\) crossed, choose on each the endpoint closest to an
intersection. Its distance to the intersection is at most \(d/2\). The two
chosen endpoints have distance less than \(d\), by the strict triangle
inequality for a transverse crossing. Overlapping collinear arcs likewise
give two distinct endpoints at distance less than \(d\). Both contradict
the packing condition. A third graph vertex cannot lie in an edge interior,
since its distance to an endpoint would be less than \(d\).

Three pairwise contacting points have positive-definite Gram matrix

\[
 H=(1-c)I_3+cJ_3,
\]

and bound a small convex spherical equilateral triangle in an open
hemisphere. No other point of \(X\) lies in that small closed triangle.
Indeed a point there can be written \(z=s/\|s\|\) with
\(s=\sum_{i=1}^3\lambda_i V_i\), \(\lambda_i\ge0\),
\(\sum_i\lambda_i=1\). Then

\[
 \|s\|^2=c+(1-c)\sum_i\lambda_i^2\ge(1+2c)/3>c^2,
 \qquad \sum_i\lambda_i(z\cdot V_i)=\|s\|>c.
\]

For \(z\) distinct from the three vertices, this contradicts all three
packing inequalities. Since \(|X|\ge4\), the complementary region of
the equilateral triangle contains another graph vertex and cannot be the
triangular face. Thus every actual triangular face used in the argument
has the small interior angle

\[
 \alpha=\arccos\frac{c}{1+c},\qquad
 \pi/3<\alpha<2\pi/5.
\]

For the lower bound, \(c/(1+c)\le3/8<1/2\). For the upper bound,
\(c/(1+c)\ge1/3>\cos(2\pi/5)=(\sqrt5-1)/4\);
the last comparison follows from \(5<49/9\).

The tangent directions of two contact neighbors at a vertex have cosine
at most \(c/(1+c)\). Their smaller angular separation is therefore at
least \(\alpha\). Every consecutive gap in the cyclic neighbor order is
at least \(\alpha\), so a contact vertex has degree at most five.

At \(P_i\), let \(m_i\) be the number of sectors other than the single
sector of \(F\). Because the boundary of \(F\) is simple and all these
other sectors are triangular, the actual angle sum is

\[
 \beta_i+m_i\alpha=2\pi.
\]

The bound \(\beta_i\le\pi\) forces \(m_i\ge3\), while degree at most
five forces \(m_i\le4\). Hence

\[
 m_i\in\{3,4\}.
\]

These are physical sectors, not chosen abstract triangle incidences.

## 2. Forced reflection and the complete closure test

Suppose two distinct unit points \(B,E\) each contact the unit points
\(C,A\), which also contact each other. The intersection of the two
contact planes with the sphere has exactly two points. Reflection in
\(\operatorname{span}(C,A)\) exchanges them and gives

\[
 B+E=r(C+A),\qquad r=\frac{2c}{1+c}\in[2/3,3/4].
 \tag{1}
\]

The denominator is positive throughout the closed domain. Conversely
\(c=r/(2-r)\). The strict positive eigenvalues of the equilateral Gram
matrix ensure that the two triangle third points really are distinct.

Choose the actual orientation of the boundary and let \(A_{i-1}\) be
the third vertex of the triangular face on the other side of the edge
\(P_{i-1}P_i\). Traverse the complement of the \(F\) sector at \(P_i\).
Its triangle fan starts with
\(a_0=P_{i-1},a_1=A_{i-1}\), and successive actual triangles force

\[
 a_{j+1}=r(P_i+a_j)-a_{j-1}.
 \tag{2}
\]

After the \(m_i\) triangular sectors, \(a_{m_i}=P_{i+1}\) and
\(a_{m_i-1}=A_i\), the outside third point on the next boundary edge.
Thus the state \((\text{previous},\text{current},\text{outside})\) updates
to \((P_i,a_{m_i},a_{m_i-1})\). There is no independently selectable
chirality at a later step: actual consecutive triangular faces have
distinct third points on opposite sides of their common edge. Either
orientation of the initial physical anchor triple is allowed.

Use \((P_0,P_1,A_0)\) as a linear basis. Its Gram matrix is \(H\), so
it is nonsingular throughout the closed cosine interval. Set its
coefficient vectors to \(e_0,e_1,e_2\). Equation (2) has polynomial
coefficients in \(r\). In this state order the literal transfer matrices are

\[
 T_3=\begin{pmatrix}
 0&1&0\\-r&r+r^2&r^2-1\\-1&r&r
 \end{pmatrix},\qquad
 T_4=\begin{pmatrix}
 0&1&0\\1-r^2&r^2+r^3&r^3-2r\\-r&r+r^2&r^2-1
 \end{pmatrix}.
\]

For a \(q\)-gon, enumerate all words
\((m_1,\ldots,m_{q-1})\in\{3,4\}^{q-1}\), apply the corresponding
updates, and subtract \(e_0\) from the final current vector. All three
gap polynomials must vanish if \(P_q=P_0\). There are exactly
\(8+16+32=56\) words, without any symmetry quotient or selected subcase.
The count omits only the final corner \(P_0\), which is tested below in
the sole surviving case.

For every word the certificate supplies rational polynomials
\(u_0,u_1,u_2,g\) with the literal identity

\[
 u_0(r)\,\mathrm{gap}_0(r)+u_1(r)\,\mathrm{gap}_1(r)
       +u_2(r)\,\mathrm{gap}_2(r)=g(r).
 \tag{3}
\]

For 55 words, \(g\) has Bernstein coefficients all strictly positive
or all strictly negative on the entire closed interval \([2/3,3/4]\).
The Bernstein basis functions are nonnegative and sum to one, including
at the endpoints. Hence \(g\ne0\) throughout that interval, and the
three necessary closure gaps cannot vanish simultaneously. The producer
constructs (3) by extended Euclidean polynomial arithmetic. The auditor
checks the polynomial identity and the literal Bernstein basis expansion;
it does not rely on a claim that a library has found the right gcd.

All eight quadrilateral words and all sixteen pentagonal words are among
the 55 exclusions. The only remaining word is the hexagon word
\((3,3,3,3,3)\), for which the exact combination is

\[
 g=r(r+1)(r+2)(r^2+2r-2).
\]

None of the first three factors vanishes on the closed band. The polynomial
\(h=r^2+2r-2\) is strictly increasing there and changes sign between the
endpoints. Its unique root is \(r=\sqrt3-1\). At that root

\[
 c=\frac r{2-r}=\frac{r+1}{3}>0,\qquad c^2=1/3.
\]

Reduction modulo \(h\) verifies that six \(T_3\) updates return the
entire anchor state. If the omitted corner had \(m_0=4\), its necessary
new-current-minus-\(P_1\) coefficient vector would instead be

\[
 (r,\ r-1,\ -1),
\]

which cannot vanish. Thus \(m_0=3\) also.

## 3. Identification and capacity of the exceptional core

The six boundary vectors and the six successive outside third points
give twelve coefficient vectors. The certificate lists all of them
modulo \(h\), and all 144 entries of their Gram matrix in the metric
\(H\). The auditor independently reconstructs every vector by matrix
products and checks every Gram entry. Diagonal entries are one. There
are 24 unordered contact pairs and 42 strictly separated unordered pairs;
in particular all twelve physical points are distinct.

Here is an ordinary coordinate description of the matching Gram matrix.
Put

\[
 b=\sqrt{2c-1},\qquad t=\sqrt{2(1-c)},\qquad c=1/\sqrt3.
\]

Take the six upper points
\((t\cos(i\pi/3),t\sin(i\pi/3),b)\), and the six lower points
\((t\cos(j\pi/3+\pi/6),t\sin(j\pi/3+\pi/6),-b)\),
for \(0\le i,j<6\). These are the usual regular hexagonal antiprism.
Within either ring, cyclic distances zero through three give Gram entries

\[
 1,\quad c,\quad 3c-2,\quad 4c-3.
\]

For an upper index minus a lower index, residues zero through five give

\[
 c,\quad c,\quad1-2c,\quad2-5c,\quad2-5c,\quad1-2c.
\]

These formulas follow by direct dot products, using \(\sqrt3=3c\).
They are precisely the audited Gram entries. Equality of these Gram
matrices, with the nonsingular anchor triple, supplies a single orthogonal
map between the reconstructed twelve physical points and this reference
antiprism. Neither a diagram nor an approximate alignment is used.

Consider another unit point and let \(q=|w|\) be the absolute value of
its coordinate along the antiprism axis. In the ring on the same side of
the equator there is a vertex within azimuthal distance \(\pi/6\).
Its dot product with the candidate is at least

\[
 a\sqrt{1-q^2}+bq,\qquad a=(\sqrt3/2)t.
\]

Exact rational comparisons give

\[
 a>3/4,\qquad b>3/8,\qquad c<3/5.
\]

Indeed \(a^2=(3/2)(1-c)>(3/2)(2/5)=3/5>9/16\).
Also \(c>73/128\), since
\(1/3-(73/128)^2=397/49152>0\); hence
\(b^2=2c-1>2(73/128)-1=9/64\).
The strict upper bound on \(c\) follows from \(1/3<9/25\).

For \(0\le q\le9/10\), the right side of the following comparison is
positive and its squared gap is nonnegative:

\[
 \sqrt{1-q^2}\ge1-2q/3,
 \qquad
 (1-q^2)-(1-2q/3)^2=q(12-13q)/9\ge0.
\]

It follows that the indicated ring dot product is strictly greater than

\[
 (3/4)(1-2q/3)+(3/8)q
 =3/4-q/8\ge51/80>3/5>c.
\]

Thus every admissible additional point lies in one of the two open caps
\(w>9/10\) or \(w<-9/10\). Two unit points in the same cap have dot
product strictly greater than

\[
 2(9/10)^2-1=31/50>3/5>c.
\]

For example, write their axial coordinates as cosines of polar angles
less than \(\arccos(9/10)\); their separation is at most the sum of
those angles, which is strictly less than twice that cap radius.
Each cap holds at most one additional point. At most two points can be
added to the twelve-point core, proving the claimed fourteen-point bound.

## 4. Consequence for a physical face-incidence pilot

Suppose \(|X|\ge15\), the complete contact map is connected, and every
face has a disk closure and a simple boundary of length three through six.
Suppose every nontriangular face has all its own interior angles at most
\(\pi\). Then:

* Every point vertex is incident to at least one nontriangular face. If
  all its incident sectors were triangular, their angles would sum to
  \(\deg(v)\alpha\le5\alpha<2\pi\), an impossibility.
* Every nontriangular face shares a physical boundary vertex with another
  nontriangular face. Otherwise it would satisfy both hypotheses of the
  lemma and would have been excluded.

Form a graph whose nodes are the nontriangular faces and whose edges mean
that two distinct such faces share at least one physical point vertex.
It has no isolated node. If there are \(k\) nontriangular faces, there
are at most \(\lfloor k/2\rfloor\) components, and their combined
vertex incidence covers all points of \(X\).

In the physical incumbent profile with eleven triangles, three
quadrilaterals and three pentagons, this gives **at most three components
of mutually vertex-connected nontriangular faces, covering all fifteen
points**. The profile is a benchmark, independently established in the
[incumbent facial chart](../incumbent-facial-chart/PROOF.md). It is not
assumed for every optimizer. This is a necessary incidence filter, not
a proof that the particular G22 motif occurs in every optimizer and not
a global separation bound.

## 5. Exact evidence and trust boundary

[check.py](check.py) and [poly.py](poly.py) produce the complete word
certificate [CERTIFICATE.json](CERTIFICATE.json).
[audit.py](audit.py) imports neither producer nor polynomial helpers:
it uses dictionary polynomials, literal transfer matrices, coefficient
identities and literal Bernstein basis expansion. The producer instead
uses fan recurrences, dense polynomial lists and extended Euclidean
arithmetic. Full case identities and Gram entries, rather than only
aggregate counts, are compared.

[controls.py](controls.py) rejects twelve damaged inputs, accepts a valid
nonzero rescaling of a Bezout/sign witness, and checks the exact closed
all-three fan state for the square, pentagonal and hexagonal antiprisms.
The first two closures have quadratic roots outside the tested band.

All mathematical calculations use Python integers and
`fractions.Fraction`; no floating-point search, external coordinate file,
solver, imported peer certificate or external package is a proof premise.
The remaining trust boundary comprises the written physical-face and
cap arguments, the two small audited programs, and Python's exact
integer/rational implementation. This is algorithmic cross-checking by
the author, not independent researcher review. See
[VALIDATION.json](VALIDATION.json), [DEPENDENCIES.md](DEPENDENCIES.md)
and [LITERATURE.md](LITERATURE.md) for reproduction and scope.

The equilateral angle constraints, contact graph method, reflection
geometry and antiprism constructions are classical. No historical
priority is claimed for them or for the quadrilateral special case.
The contribution is the explicit complete closed-band mixed-fan
certificate, the physical hexagon reconstruction and capacity bridge,
and the resulting conditional incidence filter.
