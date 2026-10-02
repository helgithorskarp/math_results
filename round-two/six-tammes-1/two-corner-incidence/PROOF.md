# Two adjacent free corners and nontriangle incidence

Actual author: **six-tammes-1**, researcher, 2026-10-02.

Status: an author-checked computer-assisted local lemma and ordinary
physical-map reduction. The new finite claims have twelve complete closure
cases and twenty-seven complete oriented gluing cases. Two different exact
algorithms check the whole certificate. These new claims have not received
independent researcher review or proof-assistant verification.

## Statements

Let \(X\subset S^2\) contain at least four distinct points and suppose
\[
 x\cdot y\le c\quad(x\ne y),\qquad c\in[1/2,3/5].
\]
The complete contact graph includes every point, including isolated points,
and every edge \(xy\) with \(x\cdot y=c\). Draw its edges as the minor
great-circle arcs of length \(\arccos c\). All faces and vertex sectors
below belong to this physical drawing.

A corner of an actual simple disk face is **sealed** if its own face angle
is at most \(\pi\) and every other cyclic sector there is an actual
triangular disk face with three distinct boundary vertices. This condition
tests the whole complementary star, not just the two neighboring edges.

**Lemma A: two adjacent free corners.** Let an actual face have disk
closure and a simple boundary of length four or five. If all its corners
outside some pair of adjacent boundary vertices are sealed, it is
impossible. No angle or star condition is required at the two free
vertices. No connected-map, global degree profile, convexity, hemisphere,
irreducibility or fifteen-point hypothesis is needed for this local lemma.

For the following statements impose these additional **map hypotheses**:

1. The complete graph is connected and has minimum contact degree at least
   three.
2. Every face has disk closure with a simple boundary, and its length is
   three, four or five.
3. Each nontriangular face closure is geodesically convex and is contained
   in an open hemisphere. Each face may have a different containing
   hemisphere. In particular, its own angles are at most \(\pi\).

Let \(\mathcal N\) be the graph whose nodes are the nontriangular faces,
with adjacency when two faces share a physical boundary vertex.

**Lemma B: components of at least three faces.** Every physical point lies
on a nontriangle. No nontriangle's set of shared corners is contained in
the endpoints of one of its boundary edges. Every component of
\(\mathcal N\) has at least three nodes; if there are \(k\) nontriangles,
there are at most \(\lfloor k/3\rfloor\) components. This remains an
\(|X|\ge4\) statement. It imports no hexagon or polar-cap result.

**Lemma C: the disconnected T11/Q3/P3 residual.** Under the map
hypotheses, assume exactly fifteen points and exactly eleven triangular,
three quadrilateral and three pentagonal faces. If \(\mathcal N\) is
disconnected, it has exactly two components of three faces. Each is an
annulus assembled from three disks sharing three full contact edges with
disjoint endpoints. Each annulus has two boundary cycles, with exactly
three mixed vertices on each cycle. The complementary regions are two
triangulated disks and a triangulated annulus, with no interior point
vertices. The two disk caps force at least six degree-three vertices.
Consequently the only possible disconnected degree profiles are
\[
 (n_3,n_4,n_5)=(6,3,6)\quad\hbox{or}\quad(7,1,7).
\]
In particular, a map in this cohort with at most five degree-three vertices
has connected \(\mathcal N\).

The only unordered component face partitions are QQQ+PPP or QQP+QPP.
The disk caps have lengths three or six; a six-cap consists of three
alternating ears and their central triangle. These are precise necessary
residual patterns, not asserted realizations or optimizer coverage.

## 1. Physical angle and reflection reduction

Equal contact arcs cannot cross or overlap without producing a pair at
distance less than \(d=\arccos c<\pi/2\). At a transverse crossing,
choose from each arc an endpoint at distance at most \(d/2\) from the
crossing; the strict triangle inequality gives the shorter pair.
Collinear overlap gives the same contradiction directly. Nor can an edge
interior contain another point vertex. Thus the contact drawing is an
embedding.

Three pairwise contacting points \(V_i\) have Gram matrix
\(H=(1-c)I+cJ\), with positive eigenvalues \(1-c,1-c,1+2c\).
They bound a small equilateral triangle. No other packing point lies there:
for \(s=\sum\lambda_iV_i\), \(\lambda_i\ge0\),
\(\sum\lambda_i=1\),
\[
 \|s\|^2=c+(1-c)\sum\lambda_i^2\ge(1+2c)/3>c^2,
 \qquad\sum\lambda_i\bigl((s/\|s\|)\cdot V_i\bigr)=\|s\|>c.
\]
Since \(|X|\ge4\), the complementary large disk contains another point
and cannot be an actual triangular face. Every actual triangular sector
therefore has angle
\[
 \alpha=\arccos\frac{c}{1+c}\in(\pi/3,2\pi/5).
\]
The endpoint comparisons are strict: \(c/(1+c)\le3/8<1/2\), and
\(c/(1+c)\ge1/3>(\sqrt5-1)/4=\cos(2\pi/5)\).

At a contact vertex the smaller tangent-angle separation of any two
neighbors is at least \(\alpha\), by the packing inequality. Each cyclic
gap is at least \(\alpha\), so degree is at most five. At a sealed face
corner, if \(m\) is the number of other triangular sectors, then
\[
 \beta+m\alpha=2\pi,\qquad \beta\le\pi,
 \qquad m\in\{3,4\}.
\]
Simple boundaries ensure exactly one sector of this face at its corner.

The third vertices \(B,E\) of two successive actual triangles sharing a
contact edge \(CA\) are the two distinct intersections of the sphere with
the two contact planes. Reflection in \(\operatorname{span}(C,A)\)
therefore gives
\[
 B+E=r(C+A),\qquad r=\frac{2c}{1+c}\in[2/3,3/4],
 \qquad c=\frac r{2-r}.
\]
All denominators are positive. A sealed fan at current vertex \(C\),
starting with previous boundary vertex \(a_0\) and outside third vertex
\(a_1\), forces
\[
 a_{j+1}=r(C+a_j)-a_{j-1}.
\]
After \(m\) triangular sectors the next boundary vertex is \(a_m\),
and its outside third vertex is \(a_{m-1}\). The state
\((\text{previous},\text{current},\text{outside})\) becomes
\((C,a_m,a_{m-1})\). Actual neighboring triangles force this reflection;
no independent chirality choices at later steps are omitted. Either initial
anchor orientation is permitted.

## 2. Twelve strict closing-contact exclusions

Label the free adjacent corners \(P_0,P_1\). The actual outside triangle
on \(P_1P_2\) exists because \(P_2\) is sealed. Its anchor
\((P_1,P_2,A_1)\) has Gram matrix \(H\); represent it by
\(e_0,e_1,e_2\). Apply the fans only at
\(P_2,\ldots,P_{q-1}\). There are \(q-2\) updates, and the final
current vector \(v\) represents \(P_0\). Its required contact with
\(P_1=e_0\) implies
\[
 g(r):=(2-r)(v\cdot e_0-c)
       =(2-r)v_0+r(v_1+v_2)-r=0.                 \tag{1}
\]
We need only this one necessary closing-contact equation; no state closure
or free-corner equation is assumed.

The literal fan matrices acting on state rows are
\[
 T_3=\begin{pmatrix}0&1&0\\-r&r+r^2&r^2-1\\-1&r&r\end{pmatrix},
 \quad
 T_4=\begin{pmatrix}0&1&0\\1-r^2&r^2+r^3&r^3-2r\\
                         -r&r+r^2&r^2-1\end{pmatrix}.
\]
Enumerate **all** words in \(\{3,4\}^{q-2}\): four quadrilateral
words and eight pentagonal words. There is no quotient. The certificate
contains each final vector, every coefficient of (1), and its complete
Bernstein expansion on the closed interval \([2/3,3/4]\). With
\(u=(r-2/3)/(3/4-2/3)\),
\[
 g(r)=\sum_{j=0}^n b_j\binom nj u^j(1-u)^{n-j}.
\]
For every word all \(b_j\) have the same strict sign, including the two
endpoint coefficients. The nonnegative basis sums to one; hence \(g\)
never vanishes, proving Lemma A. Compact signs and degrees are:

| q | word | degree | sign |
|---|---|---:|:---:|
| 4 | 33 | 5 | - |
| 4 | 34 | 6 | - |
| 4 | 43 | 6 | - |
| 4 | 44 | 7 | + |
| 5 | 333 | 7 | - |
| 5 | 334 | 8 | - |
| 5 | 343 | 8 | + |
| 5 | 344 | 9 | + |
| 5 | 433 | 8 | - |
| 5 | 434 | 9 | + |
| 5 | 443 | 9 | + |
| 5 | 444 | 10 | + |

[check.py](check.py) uses the reflected-neighbor recurrence and dense exact
polynomials. [audit.py](audit.py) imports neither it nor its polynomial
helper: it uses the displayed matrices, sparse polynomials, the alternative
Gram formula \(g=(2-2r)v_0+r\sum v_i-r\), and literal Bernstein basis
expansion. It checks all 264 final-vector coefficient positions, all twelve
obstructions and full word coverage. Both use integers/Fraction, with no
floating-point or solver premise.

This does **not** establish the analogous two-free-corner hexagon claim.
That sixteen-word domain has surviving necessary equations and is outside
the statement and certificate.

## 3. Convex intersection and component size

In the stated map cohort every physical point lies on a nontriangle. If
all its sectors were triangular, their sum would be at most
\(5\alpha<2\pi\), impossible. A corner not incident to another
nontriangle is sealed. Consequently Lemma A says that the shared-corner
set of any Q or P cannot fit inside any boundary-edge endpoint pair. This
implies at least two distinct shared corners; if there are exactly two,
they must be nonadjacent. It does not imply two different neighboring faces.

Two distinct convex nontriangle closures can meet in at most a single
vertex or a single full contact edge and its endpoints. Here is where the
extra geometric hypotheses enter. Any two common points have a unique
minor arc because each closure lies in an open hemisphere, and that arc
lies in both closures by geodesic convexity. An intersection with
noncollinear points would have two-dimensional interior, contradicting the
disjoint interiors of different physical faces. Thus a nontrivial
intersection is a boundary arc along one great circle. Embedded graph
edges cannot partly overlap, so it is a common edge chain. At an internal
vertex of a chain both face sectors would have angle \(\pi\), exhausting
the entire cyclic star and giving degree two. Minimum degree three excludes
this. The intersection is therefore at most one whole edge. In particular
three distinct faces cannot share two vertices: all would have to occupy
the two sides of that same edge.

A one-node component would have no shared corners and is excluded by
Lemma A. In a two-node component the only shared corners come from the
pair intersection just described. They fit inside one boundary edge's
endpoints (choose either incident edge for a single shared vertex), again
contradicting Lemma A. This proves Lemma B directly from the twelve new
closure cases. It requires neither the previously published one-free-corner
result nor its hexagonal capacity argument.

## 4. Equality counting forces two three-face annuli

For the T11/Q3/P3 fifteen-point cohort there are six nontriangles. If their
incidence graph is disconnected, Lemma B gives exactly two components of
three faces. Their physical vertex sets are disjoint. The total number of
nontriangle corner occurrences is \(3\cdot4+3\cdot5=27\), and their
union covers all fifteen points.

Write the three closures in component \(a\) as \(F_{a,0},F_{a,1},F_{a,2}\).
Their pair intersections contain at most two point vertices. Inclusion-
exclusion on these finite boundary-vertex sets gives
\[
 15=27-\sum_{a=1}^2\sum_{i<j}|F_{a,i}\cap F_{a,j}\cap X|
           +\sum_{a=1}^2|F_{a,0}\cap F_{a,1}\cap F_{a,2}\cap X|
       \ge27-12=15.
\]
Equality forces each of the six pair intersections to contain exactly two
vertices, and both triple intersections to be empty. Each pair therefore
shares one full contact edge, and no two shared edges in a component have
a common endpoint.

The three disk closures glued along these three edges form an orientable
subsurface of \(S^2\). At the disjoint edge endpoints their union is
locally a half-disk, with a nonempty complementary sector because degree
is at least three. The union is proper, connected and has
\(\chi=3-3=0\). Its genus is zero, as a subsurface of the sphere; thus
it is an annulus. Every point vertex in it is a boundary vertex. There are
six mixed vertices, each belonging to exactly two of the nontriangles,
and all other vertices belong to one.

## 5. Complete oriented port catalog

Label the faces cyclically by their three pairwise shared edges and choose
one common orientation from the sphere. On face \(i\) rotate labels so
that the incoming edge is \((0,1)\). Its outgoing edge is
\((k_i,k_i+1)\), where
\[
 q_i\in\{4,5\},\qquad 2\le k_i\le q_i-2.
\]
The endpoints are disjoint; this covers every possible position. The
oriented gluing to the next face necessarily reverses edge direction:
\[
 (i,k_i)\sim(i+1,1),\qquad(i,k_i+1)\sim(i+1,0),
 \quad i+1\pmod3.
\]
This rotation normalization discards no physical placement. Either global
orientation and every face-type ordering are covered; no permutation or
reflection quotient is used. The full domain has
\(\sum_{(q_0,q_1,q_2)\in\{4,5\}^3}\prod_i(q_i-3)=27\) cases.

The certificate lists every quotient class, every oriented boundary arc,
and both boundary cycles for all twenty-seven cases. The producer uses
union-find and directed successors. The auditor independently enumerates
typed ports by binary masks, uses literal disjoint identification pairs,
and walks the undirected degree-two boundary graph. Every cycle has
**exactly three mixed vertices**. The complete distribution is:

| pentagons in the component | boundary lengths | labeled port cases |
|---:|:---:|---:|
| 0 | 3 + 3 | 1 |
| 1 | 3 + 4 | 6 |
| 2 | 3 + 5 | 6 |
| 2 | 4 + 4 | 6 |
| 3 | 3 + 6 | 2 |
| 3 | 4 + 5 | 6 |

There are \(\sum q_i-6\) quotient vertices, all on the boundary.
For the two components the only unordered type/vertex splits are
QQQ+PPP with \(6+9\) vertices, or QQP+QPP with \(7+8\) vertices.
This is a finite catalog of necessary gluings, not a spherical realization
or global contact-graph enumeration.

## 6. Disk caps force six degree-three vertices

Two disjoint annuli embedded in the sphere leave two disk regions and one
annulus region. To see this, the first annulus has two complementary disks
by Jordan separation. The second, connected annulus lies in one of them
and splits it into a disk and an annulus. Each original annulus borders
one disk cap. All remaining physical faces are triangles. Every packing
point already belongs to the nontriangular annuli, so no complementary
region has an interior point vertex.

Let a disk cap have boundary length \(\ell\). A triangulated disk with
\(\ell\) boundary vertices and no interior vertices has \(\ell-2\)
triangles, by Euler and edge counting. Thus its total number of
boundary-vertex/triangle incidences is \(3\ell-6\). Exactly three of
its boundary vertices are mixed, by the complete port catalog. Each has
two nontriangle sectors and at least one cap-triangle sector. Each of the
remaining \(\ell-3\) vertices has one nontriangle sector and a sealed
complementary star, hence at least three cap-triangle sectors. Therefore
\[
 \sum_v t_v=3\ell-6\ge3+3(\ell-3)=3\ell-6.
\]
Equality forces each mixed vertex to have exactly one triangle sector and
each remaining vertex exactly three. At a mixed vertex the two
nontriangles meet across the shared edge; their union is locally one
sector, so every complementary triangle sector belongs to this same cap.
Thus each of the cap's three mixed vertices has total contact degree three.
The two caps have disjoint vertex sets and force at least six such vertices.

All boundary lengths are between three and six. A four-cap would have two
triangles but its sole sealed vertex would belong to three, impossible.
A five-cap would have three triangles and two sealed vertices, each in all
three triangles. Then their joining edge would belong to three triangular
faces, impossible in an embedded triangulated disk. A six-cap has three
mixed ears. Adjacent ears are impossible in a triangulated polygon of
length greater than three: deleting the triangles at two adjacent ears
would require crossing diagonals. Hence the ears alternate, and the other
three vertices form the central triangle. A three-cap is one triangle.

Consequently QQP+QPP must have two triangular caps and a middle annulus
with boundary lengths four and five, carrying **nine actual triangular
faces**. QQQ+PPP has one triangular cap and either another triangular cap
with a 3+6 middle annulus (nine triangles), or a six-cap with a 3+3 middle
annulus (six triangles). The 4+4 QPP and 4+5 PPP port choices cannot be the
component next to a disk cap and are excluded. These conclusions concern
actual regions of the map; they still do not identify the particular
nine-triangle G22 pattern or its simple-pentagon interface.

Finally \(2E=11\cdot3+3\cdot4+3\cdot5=60\), so \(E=30\).
With fifteen vertices and degrees in \(\{3,4,5\}\), the handshake
identity gives \(n_5=n_3\), \(n_4=15-2n_3\). At least six degree-three
vertices therefore leaves only the two profiles in Lemma C. This proves
the claimed connectedness for any cohort member with at most five.

## 7. Earlier results, reproducibility and remaining frontier

The one-free-corner refinement was independently published in
[REVIEW9663, six-reviewer-5](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-5/short-face-audit/REVIEW.md),
source commit **84b336a5009d8f3c9940e08dc56faeb7e22997ba**. Its sharp
thirteen-point actual-hexagonal-face bound and incidence consequence are
credited prior campaign results. The author had announced that direction
in message2233, but this packet makes no fresh novelty claim for it.

Optional [bridge.py](bridge.py) checks the parent
[short-face certificate](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-1/triangle-surrounded-faces/CERTIFICATE.json)
using only five constrained hexagon updates. It verifies all thirty-two
partial hexagon words, twelve distinct vectors, all 144 Gram entries and
the weaker core-containment capacity fourteen, without reading either
final-corner field. Parent source bytes are pinned in [PINS.json](PINS.json).
This is same-author corroboration of the now published omitted-corner
mechanism, not an independent review or a premise for Lemmas A--C. It does
not claim the sharper facial capacity thirteen.

The physical incumbent
[facial chart](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-1/incumbent-facial-chart/PROOF.md)
has the stated cohort and degree profile \(3^3 4^9 5^3\) in both known
completions. Our consequence for that profile is conditional map
connectedness. The chart is context and is not a proof input or a claim
about every optimizer.

All ordinary embedding, fan correspondence, convex intersection,
subsurface classification, triangulated-cap counts and code-to-statement
bridges remain unformalized. The two algorithms are written by the same
researcher. Whole normal/optimized outputs, complete regenerated bytes,
damage controls and actual costs are recorded in [VALIDATION.json](VALIDATION.json).
See [README.md](README.md), [DEPENDENCIES.md](DEPENDENCIES.md), and
[LITERATURE.md](LITERATURE.md) for reproduction and prior-art limits.

The concrete residual work is to exclude or route QQQ+PPP and QQP+QPP,
or classify connected nontriangle maps, into a **particular** actual
nine-triangle/simple-pentagon occurrence predicate, such as the earlier
[G22 facial-injectivity interface](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-tammes-1/g22-facial-injectivity/PROOF.md).
The nine triangles in
the identified middle annuli have not yet been shown to have that pattern.
Nor is the T11/Q3/P3 profile, connectedness, minimum degree, simple-disk
condition, or convex-hemispheric cohort established for every fifteen-point
optimizer. No global upper bound or optimality theorem follows here.
