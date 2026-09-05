# A field and midpoint reduction for dense506 three-point repairs

**Theorem (structural reduction with an exact finite exclusion).** Fix either
of the two pinned dense506 hosts H and its published proper four-colouring c.
Put C=C3(H), the nonhost points with at least three unit neighbours in H,
and U=H union C. Use coordinates (X,Y) representing X+i*sqrt(3)*Y, with
metric N(X,Y)=X^2+3Y^2, and put

\[
 F=\mathbb Q(z,r),\qquad z=\sqrt{33},\quad
 r=\sqrt{-408+72z}>0.
\]

Suppose c does not extend after three arbitrary plane points are added.
Then the additions are distinct points outside U, form a unit equilateral
triangle, and each has exactly two differently coloured H neighbours.
All three available colour lists are the same two-colour set. Moreover,
exactly one of these two possibilities holds:

1. All three added points belong to F^2 in the stated coordinates.
2. All three lie outside F^2, in one common real quadratic extension of F.
   Their three host-pair midpoints form a nondegenerate equilateral triangle
   of side strictly between zero and one. The three lines through the
   respective host pairs are concurrent at a point of F^2.

The mixed field/non-field case, the translated-conjugate case, and the
coincident-midpoint case are excluded. The last exclusion is specific to
these hosts and c: an exact compatibility graph on their 96,003 differently
coloured host pairs consists of isolated vertices and **686 P2, 160 P3,
34 P4, and 11 P5 components**, where Pn is a path on n vertices.

This is a necessary-condition theorem for failure to extend a particular
host colouring. It does not assert that either remaining case occurs, or
that such a failure would make the enlarged graph non-four-colourable.
Neither remaining case is enumerated here. No <=508 five-chromatic graph
is established. A non-four-colourable one-deletion/three-point repair
would in particular have to satisfy this reduction.

## Imported hosts and prior extension results

Let A and V be the pinned Parts tables of orders 159 and 214. With
alpha=i*sqrt(3), beta=alpha*z/3, define

\[
 t=(5+z+5\alpha-\beta)/12,\quad B=A\cup(\overline A+t),
\]
\[
 u_\pm=[-18-6z-30\alpha+6\alpha z
          \pm r(3+6\alpha+\alpha z)]/72,
 \qquad H_\pm=B\cup u_\pm(V-V[10]).
\]

Here V[10]=alpha/6. Both hosts have 506 vertices and 2,389 unit edges.
Coordinates, labels and c are imported from the
[arbitrary-two-point/C3 theorem](../hadwiger_nelson_dense506_two_point_extension/PROOF.md).
The fixed colour row has SHA-256
`010e6190aa14b6eadc285a6131d7b455bd5434f79ed9b4f69cdfb2848acddcb4`.

The [preceding three-addition theorem](../hadwiger_nelson_dense506_two_low_repair/PROOF.md),
source `1cd7e59a87ff10ba462f9f0dc8e43d4fa94b0fa2`, closes all additions using
at least one point of C. Points already in H and repeated additions reduce
to earlier cases. Thus a new failure uses three distinct points outside U.
Each has at most two H neighbours and an available list of size at least
two. A graph on three vertices with such lists is list-colourable unless
it is a triangle and the union of its lists has size two: for a forest,
colour outward from a root; for a triangle, apply the three-set matching
condition. Hence all lists equal one two-colour set. Each added point has
exactly two H neighbours, of the two complementary colours. This argument
does not require a criticality assumption or a SAT decision.

## Circle intersections and quadratic fields

Write J(X,Y)=(-3Y,X), multiplication by alpha, and
R=(I+J)/2, rotation through 60 degrees. Both maps have coefficients in F.
Let a,b be distinct H points, d=b-a, s=N(d)>0 and m=(a+b)/2.
Their unit-circle intersection points are

\[
 x=m+\frac{Jd}{2}\sqrt{q},\qquad
 x'=m-\frac{Jd}{2}\sqrt{q},\qquad
 q=\frac{4-s}{3s}.
\]

This follows from perpendicularity to d and N(Jd)=3s. For real
intersections s<=4. A point outside F^2 has q>0 nonsquare in F, so its
coordinate field is the real quadratic field F(sqrt(q)), and its
nontrivial conjugate is exactly the other intersection. Its conjugate
midpoint is the midpoint of its two H neighbours.

If such a non-field point x had an additional unit neighbour p in F^2,
then p,a,b would all be common points of the distinct unit circles centred
at x and x'. Two distinct circles have at most two intersections. Thus
p belongs to {a,b}, and in particular to H. Consequently a triangle of
added points outside H cannot mix a field vertex with a non-field vertex.

If all three vertices are non-field, their quadratic extensions must be
the same. Orient their labels so that

\[
 x_2=(I-R)x_0+R x_1.
\]

Inside the real multiquadratic compositum of their coordinate fields,
distinct nonsquare classes give distinct nontrivial characters. The
non-field part of each vertex is a nonzero vector in its character space.
The maps I-R and R are invertible over F. A character occurring in only
one term cannot cancel in the displayed equation. With three non-field
terms, every character must therefore be the same. This also explains
why field membership is a conclusion of incidence geometry, not an
assumed coordinate restriction in the search.

Write x_i=m_i+v_i*sqrt(q), with all m_i,v_i in F^2 and q>0 nonsquare.
The common conjugation tau sends x_i to m_i-v_i*sqrt(q), giving another
unit equilateral triangle with the same orientation. Taking averages
gives m_2=(I-R)m_0+R*m_1. The midpoint triangle is equilateral or all
three midpoints coincide. Comparing an edge with its conjugate gives

\[
 \langle m_i-m_j,v_i-v_j\rangle=0,\qquad
 N(m_i-m_j)+qN(v_i-v_j)=1.
\]

Its common side length ell therefore lies in [0,1]. If ell=1, all v_i
are equal: the conjugate triangles differ by translation. The two host
neighbours of each x_i are then m_i plus or minus the same fixed nonzero
vector w. The three points m_i+w form a unit equilateral triangle in H,
but all their colours belong to the same complementary pair of colours.
This contradicts propriety of c. Hence ell<1.

If the host pair were repeated at two vertices, those vertices would be
the two different roots x,x'. Their unit separation forces s=3 and
q=1/9, making both roots elements of F^2. Thus the three host pairs are
distinct in the non-field case.

## Excluding ell=0 by a complete compatibility graph

For distinct host pairs with the same midpoint and the same two host
colours, let u,v denote their full chord vectors, and write

\[
 s=N(u),\quad t=N(v),\quad d=\langle u,v\rangle.
\]

Any unit-circle centres x,y associated with these pairs satisfy
N(x-m)=1-s/4 and N(y-m)=1-t/4. Their directions are perpendicular to u,v.
If N(x-y)=1, squaring the scalar-product identity necessarily gives

\[
 \boxed{(4-s-t)^2st=4(4-s)(4-t)d^2.} \tag{1}
\]

The derivation does not divide by d. In particular the zero-dot boundary
is retained. We impose no positivity, root-sign or square-class condition
in the finite check. Equation (1) is only a necessary condition; retaining
extra pairs makes the exclusion stronger to check, without losing any
possible geometric obstruction.

Make a graph whose vertices are the differently coloured H pairs.
Join two distinct pairs when they have the same midpoint and host-colour
pair and satisfy (1). A non-field equilateral triangle with ell=0 would
produce a triangle in this graph, since its three host pairs are distinct.

The exact census has:

| Quantity | Value |
|---|---:|
| Differently coloured host pairs | 96,003 |
| Nonempty midpoint/colour-pair groups | 62,696 |
| Within-group pairs tested by (1) | 144,650 |
| Compatibility edges | 1,152 |
| Vertices incident to those edges | 2,043 |
| Nontrivial components | 891 |
| Within-group triples | 581,432 |
| Compatibility triangles | 0 |

Every nontrivial component is a path. Their complete order histogram is
the [compact certificate](path_types.tsv): 686 P2, 160 P3, 34 P4, 11 P5.
The remaining 93,960 host-pair vertices are isolated. This proves ell!=0.

All host coordinates have denominator D=2592 in the basis
(1,z,r,zr) for each of X,Y. Midpoint equality is tested by equality of
the eight integer coordinate sums. Chord norms s,t and dot product d in
the code are numerator quantities; accordingly every literal 4 in (1)
is replaced by 4D^2. All products use arbitrary-precision integers in F.
The degree-four basis is faithful because r^2=-408+72z changes sign
under the two real embeddings of Q(sqrt33), and hence is not a square
in that field.

The exact edge stream, sorted rows [a,b,c,d] of the two sorted host pairs,
has SHA-256
`28aa4165d59c8903b11f61191a9e8dd2bc9c1c47503a3b046bbec68beaf6ba1f`.
The canonical path stream has SHA-256
`9f0c7ee878a48a5be4d2e99f031346cab90f3f217ec6c29a923534e2f9eef0ed`.
Streams use compact JSON without a trailing newline for hashing; generated
files add one newline. Each path starts at its smaller endpoint, and paths
are sorted lexicographically. Group entries consist of a sorted host-colour
pair and its lexicographically sorted host pairs; these entries are also
sorted, giving the group-stream SHA-256
`74dfd75341e61b74e21a8e8f1b588a1e372020e760007b4fd638c45598019d08`.

## Independent check and remaining geometry

The primary verifier builds H+ using its real four-coordinate arithmetic,
checks the fixed colouring on all 2,389 host edges, tests all 144,650
pair equalities, and checks the graph's path decomposition.

The [audit](audit.py) reconstructs H- from the pinned Parts tables using
the [independent reviewer's eight-basis quotient-ring code](../hadwiger_nelson_dense506_two_point_extension_review1/independent_check.py).
It obtains twice the dot product by polarization from the three norms
N(u), N(v), N(u-v), using no primary dot-product routine. It tests every
pair with exact arithmetic, and matches every group and edge entry to the
primary output. It then enumerates **all 581,432 within-group triples**
and checks that none has three compatibility edges, independently of the
primary path decomposition. There are no modular or floating-point
filters. The common labelled graph works for both hosts; alternatively,
its defining equalities are preserved by the automorphism r->-r.

Controls use 18 rational circle fixtures with all four root-sign choices
over 171 pair cases, including repeated pairs and a zero-dot case. They
recover exactly 12 compatible cases. They also check the repeated-pair
square boundary, accept P5 and reject a triangle and a branched tree as
invalid path decompositions.

Finally, the direct isometry taking the labelled triangle x_i to tau(x_i)
is a rotation or a translation. The translation case was excluded above.
Its rotation centre belongs to all three perpendicular bisectors of
x_i,tau(x_i), which are precisely the three host-pair lines. Two of these
lines are distinct and nonparallel: otherwise three noncollinear vertices
would have the same bisector line under a nontrivial rotation. Their
intersection therefore belongs to F^2. This proves the concurrency part
of the theorem.

The prior extension theorems and exact host data remain imported premises.
This new author-run audit is not an external review of the new reduction.
The ordinary trust boundary includes those premises, SHA-256 identity,
exact CPython arithmetic and unformalized geometric/code reasoning.

The all-F^2 case and the case of a nondegenerate midpoint triangle with
0<ell<1 are still open. No midpoint-pair enumeration for that second case,
no full two-neighbour completion set, and no subsequent construction phase
has been run here. The new finite certificate closes only ell=0; the
other exclusions and the concurrency conclusion are structural arguments.
