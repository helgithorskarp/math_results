# A ten-triangle component cannot contain the full G20 motif

Actual author **six-tammes-1**, role **researcher**, 2026-10-02, pass22.
An ordinary geometric reduction followed by an exact polynomial certificate.
The separate programs are by the same author; independent researcher review
and formalization of this new result are pending.

Let X be a finite set of at least twelve distinct unit vectors in R^3,
with every distinct pair having inner product at most c, where

\[
                 c\in I=[14/25,593/1000].                 \tag{1}
\]

Use the **complete** contact drawing: every pair with product c is an edge,
drawn by its minor geodesic arc. An actual triangular face is a component
of the complement whose closure is the smaller hemispheric triangular
disk with its stated three distinct corners. The triangle adjacency graph
has these actual faces as vertices, joined when they share an edge. No
contact edge may be deleted to manufacture a face or adjacency.

The twelve labels below denote twelve **distinct** points. Prescribe the
eighteen contacts in the edges of

\[
\begin{split}
\mathcal A&=\{(0,5,11),(0,6,11),(0,5,7),(5,9,11)\},\\
\mathcal B&=\{(1,2,4),(2,4,8),(1,2,10),(1,10,12)\},
\end{split}                                               \tag{2}
\]

and also the two cross contacts **7-12 and 9-10**. These are exactly the
twenty prescribed contacts of the credited
[twelve-point frame](../../six-tammes-2/twelve-core-frame/PROOF.md).
Additional contacts are allowed. The eight displayed contact triples
are actual triangular faces: the embedding and empty-contact-triangle
argument in [LEMMA9813, Section2](../connected-map-filters/PROOF.md)
applies to this complete drawing. Alternatively their actual-face status
can be retained as an explicit local hypothesis throughout the proof.

**Local theorem.** If a component of the triangle adjacency graph is a
tree and contains all eight faces in(2), it has at least eleven faces.
In particular, there is no ten-face tree component containing the full
G20 motif on the closed interval(1).

**Fifteen-point corollary.** Retain **all** the physical hypotheses of
[LEMMA9813 CorollaryC](../connected-map-filters/PROOF.md), now with c in I:
fifteen distinct unit points; complete contact graph connected and minimum
degree at least3; every actual face closure a simple disk with3..5 distinct
boundary points; every nontriangle closure geodesically convex and in its
own open hemisphere; and counts T11/Q3/P3. For the full G20 motif, the
necessary profile list in that corollary loses **1+10**. The ten remaining
necessary profiles are

\[
\begin{gathered}
11;\quad4+7,\ 5+6;\\
1+4+6,\ 1+5+5,\ 2+4+5,\ 3+4+4;\\
1+1+4+5,\ 1+2+4+4;\quad1+1+1+4+4.
\end{gathered}                                            \tag{3}
\]

The weaker eighteen-contact motif still has the original eleven-profile
screen. Neither missing cross contact is proved by this theorem. No motif
occurrence, profile realizability, general packing exclusion, new global
separation bound or optimizer-cohort coverage is asserted.

## 1. Complete geometric reduction to144 placements

For completeness, contact arcs embed: a transverse crossing gives two
chosen endpoints whose distances to the crossing have sum at most
acos(c), and their strict triangle inequality contradicts the packing
condition. Collinear overlap or a vertex inside an arc also violates
separation. For a contact triple x_i and nonnegative lambda_i summing
to1, put q=sum lambda_i x_i. Then
||q||^2>=(1+2c)/3>c^2. If another packing point z=q/||q|| were in
the smaller triangle, z.x_i<=c would imply ||q||=z.q<=c, a contradiction.
Thus that smaller triangular disk has no other point; embedding prevents
an edge without an interior endpoint from entering it. It is an actual
face of the complete drawing. The three corners are in an open hemisphere
since each has positive product1+2c with their sum. This also justifies
the actual-face assertion for all eight triples in(2), without relying on
an external enumeration or irreducibility theorem.

A tree of f triangular faces contains at most f+2 distinct point vertices.
Root the tree at one triangle and order every child after its parent.
The first face has three vertices; each later face shares its parent edge
and adds at most one. Vertex pinches or extra identifications only decrease
the count. This argument does not require the component closure to be a
disk. Since(2) already uses twelve distinct point vertices, f>=10.

Assume f=10. All component corners must be precisely those twelve labels,
because f+2=12 is already attained. Exactly two other triangular faces,
U,V, are left after the eight displayed faces. Each four-face cluster is
connected in the triangle adjacency graph. Their supports

\[
A_0=\{0,5,6,7,9,11\},\qquad B_0=\{1,2,4,8,10,12\}
\]

are disjoint. Within A, the face(0,5,11) is adjacent to each of its other
three faces; within B the order(2,4,8),(1,2,4),(1,2,10),(1,10,12) is a
path. These account for their internal adjacencies. Two distinct actual
triangles cannot share two different edges: that would give the same
three corners and the same smaller hemispheric disk.

Contract the connected A and B subtrees. Contraction in a tree leaves a
tree on the four nodes A,B,U,V, with no loops or parallel edges. A and B
are not adjacent because their supports are disjoint. No auxiliary
triangle can be adjacent to both A and B, since that would require two
distinct A corners and two distinct B corners in a three-corner face.
Consequently the contracted tree is necessarily

\[
                         A-U-V-B,                         \tag{4}
\]

after exchanging U,V. Indeed A and B have no common neighbor, so their
distance in a four-node tree must be3; this uses all four nodes.

The edges within each cluster have incidence one or two. Their six
boundary edges form the literal cycles

\[
             0-6-11-9-5-7-0,\qquad1-4-8-2-10-12-1.       \tag{5}
\]

Each patch is an abstract triangulated disk: start with its central/root
triangle and attach each remaining triangle along one boundary edge with
a fresh vertex. Actual faces have disjoint interiors in the embedded
complete contact drawing, so this disk and its simple boundary cycle are
also the actual patch. In particular a face outside a cluster cannot
attach along an internal cluster edge, which already has both incident
faces. The separate checker verifies all incidences, fresh vertices and
the cycles(5); no inference of disk structure is made from a count alone.

Let U share A boundary edge{a,a'} and V share B boundary edge{b,b'}.
Since all corners are in A_0 union B_0, U's third corner must lie in B_0:
otherwise U has three A corners, while V has at least two B corners,
preventing their common two-corner edge. Similarly V's third corner lies
in A_0. Thus their common edge is{a,b}, with a one of the chosen A-edge
endpoints and b one of the chosen B-edge endpoints. Exactly

\[
                   U=(a,a',b),\qquad V=(a,b,b')            \tag{6}
\]

result. There are six choices for each boundary edge and two choices for
each shared endpoint: **6*6*2*2=144 literal placements**. Every placement
is retained, with no symmetry quotient or assumption of realizability.
The certificate and two programs cover the complete labeled product set,
not just a count of cases. The glued patch has eighteen internal contacts
and the three cross edges a'b,ab,ab', hence21 edge contacts.

## 2. The contact-edge reflection covers all geometric branches

For adjacent contact triangles (x,y,z),(x,y,w), x.y=x.z=y.z=c and w
is a distinct unit vector with w.x=w.y=c. The two affine plane constraints
meet the unit sphere in exactly two points. Their midpoint is

\[
       q=\frac{c}{1+c}(x+y),\quad
       \|q\|^2=\frac{2c^2}{1+c}<1.
\]

The directions perpendicular to span{x,y} give the two choices; x,y are
independent since 0<c<1. One point is z, so the distinct other point is

\[
       w=2q-z=r(x+y)-z,\qquad r=\frac{2c}{1+c}.           \tag{7}
\]

This classical contact reflection is not claimed as a new identity.
Distinct point labels select the other branch at every actual shared
edge; no sign or orientation branch has been dropped. On I,

\[
 r\in J=[28/39,1186/1593],\quad c=\frac r{2-r},\quad2-r>0.\tag{8}
\]

Anchor the A contact triple (p0,p5,p11). Its Gram matrix
H=(1-c)Id+cJ_3 is positive definite, with eigenvalues1-c,1-c,1+2c.
It is a basis of R^3. The three other A corners are obtained by(7),
then the two corners b,b' in(6), then the other B corners by walking its
four-face tree. This determines every actual placement uniquely in that
basis. Every coefficient is an integer polynomial in r.

For coefficient vectors v,w, put

\[
 N(v,w)=(2-2r)\sum_i v_iw_i+r(\sum_i v_i)(\sum_i w_i).
\]

Then v^T H w=N(v,w)/(2-r). All twelve norms and all21 patch-contact
identities are checked as exact polynomial equalities in both programs.
The two extra prescribed G20 contacts require

\[
 F(r)=N(p7,p12)-r=0,\qquad G(r)=N(p9,p10)-r=0.           \tag{9}
\]

The largest degree of either gap across all cases is9. Colliding or
otherwise unphysical formal placements are retained in this necessary
algebraic test; enlarging the tested class is safe for an exclusion.

## 3. Exact certificates exclude every placement on the closed band

For each of144 cases the programs compute rational polynomials h,u,v,
with h monic and nonzero, and verify coefficient by coefficient

\[
                         uF+vG=h.                        \tag{10}
\]

The highest witness degree is7. There are only23 distinct h polynomials.
The complete case-to-h table and every Bernstein coefficient are in the
8,029-byte [CERTIFICATE.json](CERTIFICATE.json). The programs reconstruct
and explicitly check(10); stored Bézout coefficient lists are unnecessary.
The auditor also verifies both divisions by h have zero remainder.
Verifying only that h divides both F and G would **not** justify the
argument: the constant1 always divides them. Identity(10) is the required
implication from a common root to a root of h. Both-zero gaps abort rather
than becoming a fictitious gcd1.

Write r=lo+(hi-lo)t, 0<=t<=1, with lo,hi from(8). In degree D=deg(h),

\[
 h(r)=\sum_{j=0}^{D} b_j\binom Dj t^j(1-t)^{D-j}.
\]

All listed b_j have one **strict** sign, checked using exact rational
arithmetic. Bernstein basis functions are nonnegative and sum to1,
including at both endpoints. Hence h has no root anywhere on J.
Equation(10) rules out(9) on J. All144 placements are therefore excluded.
The per-case degree histogram for h is

|degree|1|2|3|4|5|6|7|
|:---|---:|---:|---:|---:|---:|---:|---:|
|cases|20|35|20|42|9|11|7|

Together with the geometric completeness reduction, this proves the local
theorem. The corollary follows from9813's forest and necessary profile
screen: the only lost route is1+10, because two disjoint four-face clusters
cannot be placed in the singleton component. No other listed profile is
claimed feasible or excluded.

## 4. Verification and limits

[check.py](check.py) is a dense-polynomial A-anchored producer.
[audit.py](audit.py) anchors instead at the B triple(p1,p2,p4), builds the
B path first, propagates the bridge backward, then constructs the A star.
Its arithmetic uses sparse polynomial dictionaries; it computes Bernstein
coefficients by multiplication and degree elevation instead of affine
power expansion. Its row elimination produces Bézout witnesses and checks
the identities. It imports no producer arithmetic. Its main entrypoint
imports the producer's construction **only for comparison** of all
20,736 Gram polynomials and all288 cross-gap polynomials. It checks
1,728 norms and3,024 patch contacts in its own representation.

[controls.py](controls.py) checks literal coverage, input scope, cross
contacts, root-free coefficient/row bindings, closed-endpoint roots, the
both-zero gap trap and the merely-common-divisor trap. Reordered cases
and consistently permuted polynomial indices must still pass. All32
semantic damages reject and all3 valid controls pass.
[VALIDATION.json](VALIDATION.json) records the actual serial normal and
optimized Python executions and complete output/certificate equality.
There are no assert-dependent proof gates, solver calls, float signs,
sampled parameters or private external certificate inputs.

Two algorithms by one author do not constitute independent researcher
review. The actual-face, disk, tree-contraction and spherical-reflection
bridges above remain ordinary unformalized mathematics. The 142,814-byte
exploratory pilot stays private; it is neither a runtime input nor evidence
substituting for execution of these public programs.

The separately reviewed [variable G20 frame](../../six-tammes-2/twelve-core-frame/PROOF.md)
has a positive flexible family in
[REVIEW9809](../../six-reviewer-5/twelve-core-frame-audit/REVIEW.md).
The present theorem excludes a particular triangle-tree route, not all
G20 configurations. The new
[fixed-core three-addition theorem9828](../../six-tammes-2/twelve-core-completion/PROOF.md)
fixes twelve incumbent positions; those stronger hypotheses are not used
here. Remaining problems include the eleven-face route, the other profiles,
forcing either cross contact, literal occurrence, arbitrary three-addition
capacity over the entire flexible frame, the critical strip and coverage
of all global optimizers. No claim is made that(1) is a maximal exclusion
interval or that the necessary profile list is a global Tammes bound.
