# Three four-triangle fives are impossible in the nine-Q branch

Actual author **six-tammes-1**, role **researcher**, 2026-10-01.
Status: complete author-checked ordinary geometric/contact-structure proof,
with exact finite fan and original-alias checks. Independent mathematical
review and formalization are pending.

## 1. Statement and scope

Let fifteen distinct unit vectors have minimum geodesic separation `d`,
and put `c=cos(d)`, where

    1/2 < c < 3/5.

Assume their **complete** contact graph is connected, has degrees3,4,5,
and its minor-geodesic edges form a cellular sphere embedding whose faces
are simple strictly convex hemispherical triangles T and quadrilaterals Q.
Assume there are exactly nine Qs and exactly three degree-five vertices.

**Theorem.** At least one of the three fives has at most three incident Ts.
Equivalently, the subfamily in which all three fives have four Ts is empty.

The theorem treats all contacts and original fifteen points. It assumes no
coordinate template, spatial symmetry, closeness to an incumbent, congruence
between different Qs, or prescribed relationship among the three fives.
It holds on the full interval above, without the narrower beta premise used
in earlier count catalogues. It is conditional on the stated T/Q embedding;
pentagonal/hexagonal faces, other degree counts and unrestricted optimizer
coverage are not settled. Known fifteen-point incumbents have larger faces
and are not excluded by this theorem. No global numerical bound is changed.

Euler gives `E=30,T=8`, and the degree sum gives `n3=n5=3,n4=9`.
Call a two-T four **ordinary**, a one-T or zero-T four **deficient**, and a
four-T five **ordinary**. These terms specify triangle incidences, not shape.

Suppose all three fives are ordinary. Write `a,b,O` for the numbers of
one-T, zero-T and ordinary fours. Counting the twenty-four T corners gives

    a+2b=6,       O=9-a-b=3+b<=6.                       (1)

An edge with Q on both sides will be called a QQ edge. Its incidence at a
deficient four is a QQ end. The total QQ-end supply of deficient fours is

    2a+4b=12.                                         (2)

Every three has three QQ contacts, all to deficient fours, as proved below.
They consume nine distinct QQ ends. Thus **at most three QQ ends remain
for deficient-four contacts with points other than the threes**. In each
possible arrangement of the fives we force at least five such ends.

## 2. Credited spherical facts, with their local arguments

The classical T/Q corner facts are those in
[Musin--Tarasov, Proposition4.1](https://arxiv.org/html/1312.5450#S4.SS1)
and [their N14 paper](https://arxiv.org/abs/1410.2536). The preceding campaign
[odd-degree proof](https://github.com/helgithorskarp/math_results/blob/main/tammes15_nine_quad_odd_degree_reduction/PROOF.md)
already proves the three-neighbor restriction used here. The necessary local
arguments are included; that prior result or its review is not imported as
an unchecked geometric oracle. Historical priority is not claimed for these
elementary sphere and face-link mechanisms.

Put

    alpha=acos(c/(1+c)), phi=2pi-4alpha,
    A=2pi-2alpha, b0=2atan(1/sqrt(c)),
    rho(u)=2atan(1/(c*tan(u/2))).

Every T has angle `alpha`. A convex equilateral Q has equal opposite
angles, and adjacent angles `u,v` satisfy

    cot(u/2)cot(v/2)=c,      v=rho(u).

One elementary derivation puts its vertices in the form
`(x,0,z),(0,y,w),(-x,0,z),(0,-y,w)`, with `x,y,z,w>0`,
`x^2+z^2=y^2+w^2=1` and `zw=c`. Opposite contact solutions and convex
hemispherical diagonals justify this normalization. At the first two
vertices the tangent-vector sums/differences give half-angle cotangents
`wx/y` and `zy/x`, respectively. Their product is `c`.
The diagonal opposite a corner `u` has dot
`c^2+(1-c^2)cos(u)`. Contact completeness makes both Q diagonals strict
noncontacts. Therefore

    alpha < u < 2alpha,                               (3)

using the decreasing involution `rho` and `rho(alpha)=2alpha`.

On the stated interval,

    3pi/8 < alpha < 2pi/5,       alpha < phi < pi/2.    (4)

For the upper angle bound, `c/(1+c)>1/3>cos(2pi/5)`; the last comparison
squares to `49>45`. For the lower bound, `c/(1+c)<3/8<cos(3pi/8)`;
the last comparison squares to `529>512`. These are exact comparisons.
The bounds `(3)` and `5alpha<2pi` show that a three has no T, a four
has at most two Ts, and a five at most four Ts, by its full angle sum.
An ordinary four's two Q corners sum to `A`, and each is greater than
`phi`. A three's three Q corners are also each greater than `phi`.
An ordinary five's sole Q corner equals `phi`.

For `u in(0,pi)`, the positive half-tangents of `u,rho(u)` have product
`1/c>1`. Their arctangent sum is maximal when the half-tangents agree:
this follows by differentiating `atan(t)+atan((1/c)/t)`. Thus

    u+rho(u)<=2b0<A.                                  (5)

Indeed `cos(b0)=(c-1)/(c+1)>-c/(c+1)=cos(pi-alpha)` since `2c-1>0`.

If a three U contacts V, the two faces at UV are Qs. If their U corners
are `u,v`, the third corner is less than `2alpha`, hence `u+v>A`.
The corresponding corners at V satisfy

    rho(u)+rho(v) <=4b0-u-v <4b0-A <A.

V cannot be another three, whose corresponding sum would exceed A, or
an ordinary four, whose corresponding sum equals A. V cannot be an
ordinary five with only one Q. All its possible neighbors are therefore
deficient fours. This proves the nine-end demand following `(2)`.

Two distinct actual unit points have at most two common positive-c contact
neighbors: their two affine dot-product planes intersect the sphere in
at most two points. The only dependent distinct case is antipodality,
which has no common positive-c contact neighbor. This bound is repeatedly
used to control identifications of **original** points.

## 3. Fans force a path or triangle among the fives

Write the three fives as F,G,H. An ordinary five has four consecutive T
faces and one Q in its degree-five cyclic link. Its five distinct contact
neighbors form a linear word of five points; consecutive pairs make its
four Ts. The two ends meet its sole Q. The three middle points are its
fan internals.

An edge between two ordinary fives cannot belong to a Q: their Q corners
would both equal `phi<pi/2`, whereas `rho(phi)>pi/2`. Thus every five-five
contact is T-T and the other five occurs internally in each fan.
Every other internal is an ordinary four. A three or zero-T four has no
T, and a one-T four cannot meet the two different Ts at an internal.

No ordinary four can be internal in two five fans. It would belong to
four T incidences; at most one actual T can belong to both distinct
five fans, giving at least three different Ts at a two-T four. The same
point may still be internal in one fan and an endpoint in another; this
possibility is retained throughout.

If `e55` is the number of five-five contacts, there are exactly
`9-2e55` distinct ordinary-four internals. By `(1)`, `e55>=2`.
The complete graph among the three fives is consequently either a path
or a triangle. All other graphs on the three originals are excluded by
this count, rather than assumed away.

The Q opposite of every ordinary five is a deficient four. Opposite
angles rule out an ordinary four or three. If two fives were opposite
in a shared Q, its two other vertices would be ordinary fours: they
are endpoints of both noncontacting five fans, giving two distinct Ts;
and no five can be adjacent to a five in a Q. Each of the two fans has
three internals. The third five can be internal in at most one of them,
since otherwise the opposite pair would have a third common contact,
in addition to the two Q endpoints. The remaining at least five internals
are distinct ordinary fours and distinct from the two shared endpoints.
This requires at least seven ordinary fours, contrary to `(1)`.
Hence **all three Q opposites below are deficient fours**, including when
different Qs have equal opposites or share an edge.

## 4. Triangle case: original links and QQ debt

Suppose F,G,H are mutual contacts. Their equilateral minor triangle is
an actual T face. To see that its smaller region has no other code point,
write such a point as a normalized nonnegative combination of its three
vertices, with coefficient sum1. If all its vertex dots are at most c,
the combination has norm at most c. Its dot with F is at least c, whereas
the alleged point's dot with F is at most c; hence `c<=c^2`, impossible.
The triangle is convex hemispherical, and a cellular complete graph cannot
subdivide its empty interior without an additional original vertex.

At each five the other two fives are therefore adjacent internals, and
the remaining internal is an ordinary four I. Direct an arrow from this
five to whichever other five adjoins I in its fan. A mutual arrow would
make their second common T use the same I internal in both fans, forbidden
by Section3. There are three arrows on three possible pairs, each with
at most one arrow. They give a directed three-cycle.

Relabel the actual fives F0,F1,F2 along that directed cycle. This is role
renaming, not an assumption of geometric symmetry. Let Ii be internal at
Fi and an endpoint at F(i+1), indices modulo3. The full fan words are

    Fi: I(i-1), F(i-1), F(i+1), Ii, Ai.

The Ii are three distinct ordinary fours. Every extra endpoint Ai is a
one-T or ordinary four outside the Ii set. It cannot be another five
(the other two are already internal), a three or zero-T point. It cannot
be an Ii: either it repeats a neighbor in its own fan or adds a new third
T at a full ordinary Ii in the other fan. The Ai are pairwise distinct:
two fives already have the third five and their common Ii as their two
common contacts, so an additional common endpoint is forbidden.

Write each sole Q as

    Qi=(Fi,I(i-1),Hi,Ai),       Hi deficient.

The Hi may coincide with one another or with some other Aj. No global
fresh-point assumption is made. At Ii its two known Ts give link path

    F(i+1) -- Fi -- Ai.

The Q from F(i+1) contributes the corner F(i+1)--H(i+1). If H(i+1)=Ai,
these three distinct faces seal a three-cycle in the degree-four link,
which cannot include a fourth distinct neighbor. Its deficient role
also excludes either five alias. Thus H(i+1) is the fourth neighbor,
and the remaining corner Ai--H(i+1) is Q. Consequently each edge
`Ii-H(i+1)` is QQ, accounting for **three distinct non-three QQ ends**
at deficient fours. All original opposite aliases are covered by this
role/link argument; in particular the sealed-link alias is rejected
before counting the edge as new.

If some Ai is one-T, its only T is `(Fi,Ii,Ai)`, which does not contain
Hi. Hence `Ai-Hi` is QQ at both deficient ends. It is distinct from the
three ordinary-to-deficient edges just counted, and adds two ends. This
forces at least five non-three QQ ends, contradicting `(2)` and the
nine three-neighbor ends. Coincident Hi or reciprocal Ai/Hi edges cannot
erase these five distinct incidences.

If no Ai is one-T, all three are further distinct ordinary fours, so
`O>=6`. Equation `(1)` forces `O=6,a=0,b=3`; every Hi is zero-T. At Ai
the known T `(Fi,Ii,Ai)` and Q `Qi` give neighbor pairs Fi--Ii and Fi--Hi.
Its fourth neighbor J is distinct from these three local neighbors;
J denotes any remaining actual original, not a newly introduced point.
The second T at Ai must use either Ii,J or Hi,J. The first alternative
is a new third T at Ii: its existing other T `(Fi,F(i+1),Ii)` excludes
Ai, and J cannot equal Fi. The second alternative puts a T at zero-T Hi.
Both are impossible, closing the remaining triangle case.

## 5. Path case: both endpoint/internal orientations retained

Now the five graph is F-G-H, with F,H noncontacts. At the middle five
the two other fives must be nonadjacent internals, since an adjacent pair
would make T(F,G,H) and a forbidden FH contact. Up to reversing its local
fan word, write

    G: X,F,I,H,Y.

I is ordinary and internal at G. The two T faces at FG force F's two
neighbors around its internal G to be I,X. Since I cannot be internal
in F as well, it is F's endpoint, and X is internal at F. Similarly I
is H's endpoint and Y internal at H. Thus the outer words, with both
local reversals included, are

    F: I,G,X,R,A,        H: I,G,Y,S,B.

The five internals I,X,Y,R,S are distinct ordinary fours. A,B are outside
these five: reuse either repeats a neighbor in its own fan or adds a new
third T at an internal in another fan. A and B are distinct; otherwise
F,H would share three contacts G,I,A. They are one-T or ordinary fours.
Since `O<=6`, at least one of A,B is one-T.

Write F's Q opposite as J. At I, the two Ts have link path F--G--H, and
the F-Q corner adds F--J. J is deficient, hence is the fourth neighbor.
The remaining H--J sector is Q. H's sole Q therefore has the **same**
opposite J. The edge I-J is QQ. Write the middle five's Q opposite as K;
its Q is `(G,X,K,Y)`. At X its two full Ts `(F,G,X),(F,X,R)` exclude K,
so X-K is QQ; likewise Y-K is QQ. These three edges have different
ordinary endpoints I,X,Y and supply three non-three deficient QQ ends.
All J/K coincidences are allowed at this stage.

If, for example, A is one-T, its unique T `(F,R,A)` excludes J, so A-J
is QQ at both deficient ends. This adds two distinct ends, again giving
at least five where `(2)` allows three. The alternative B one-T is the
same counted argument with the endpoint names reversed. This closes the path.

For the exact small terminal audit one can sharpen the count without a
new geometric premise. The path fans contain eight distinct Ts (twelve
five incidences minus the four shared T faces at FG and GH). These are
all Ts in the graph. Thus A,B cannot gain a second T elsewhere; both
are one-T, `O=5,a=2,b=2`. J differs from A,B by Q simplicity, so J is
one of the two zero-T originals. K is any deficient original. The eight
J/K assignments give seven non-three QQ ends. Six violate an individual
QQ supply; the remaining two violate the total nine-end demand. This
finite refinement is not needed for the ordinary five-end contradiction.

## 6. Exact finite checks and their trust boundaries

[check.py](check.py) exhausts all placements of the other fives in the three
internal fan positions:54 path words and216 triangle words. Both matchings
of the two actual T thirds at every five-five edge are retained, giving
216/1728 interface words. Union/find identifies forced originals; every
remaining alias is retained by restricted-growth partitions. It checks
63,144/13,392 original-alias partitions, rejecting repeated neighbors,
excess T incidence, excess known degree, extra five contacts and third
common contacts. Exactly8 path and16 triangle local charts remain.
These are **necessary local fan entries**, not realized sphere embeddings
or a catalogue of all fifteen-vertex maps. The direct hand arguments in
Sections3--5 establish why every actual case is covered.

The opposite/endpoint cover uses all original role aliases, including
reciprocal deficient-deficient edges and common opposites. The triangle
case has35,118 raw assignments across `(a,b)=(6,0),(4,1),(2,2),(0,3)`.
Repeated Q vertices and sealed links are removed before QQ counting. The
last zero-T case is closed by its second-T forcing; all others have more
QQ debt than the available three ends. The path case retains all eight
opposite assignments described above.

[audit.py](audit.py) imports no primary code. It uses triangle-incidence
patches and Hamiltonian neighbor paths to reconstruct every surviving local
chart, four-neighbor cyclic link completion, and binary QQ adjacency rows.
It compares the complete chart sets and every terminal classification by
exact hashes. This is complementary same-author validation; it does not
independently formalize the geometric completeness argument or constitute
independent researcher review. Normal and optimized Python runs agree.

A path with its two extra endpoints identified is rejected by the two-common-
contact bound and becomes a nonempty surrogate when that bound is released
to three. Loosening the three-neighbor demand9 to3 also leaves nonempty QQ
prefixes. Releasing the zero-T prohibition in the last local link supplies
a nonempty local completion. These controls are not spherical packings or
counterexamples to the theorem. No floating point, solver, external data,
large proof corpus or incomplete enumeration is proof evidence.

The remaining mathematical trust boundaries are the ordinary written sphere,
complete-contact, original-face, link and coverage arguments. Exact code
validates finite obligations, not those continuous bridges by itself.

## 7. What this removes and what remains

The public source catalogue
[two-ordinary-fives exclusion](https://github.com/helgithorskarp/math_results/blob/main/tammes15_two_ordinary_fives_exclusion/README.md)
at source `6dffbb940c10f415b71e275a45010a7141d1ee4e` leaves18 necessary beta profiles, not maps. This theorem
removes its three all-ordinary-five r=3 rows:

    (a,b,f0,f1,f2)=(2,2,3,0,0),(4,1,3,0,0),(6,0,3,0,0).

Under that source catalogue's inherited hypotheses, fifteen source profiles
remain, split0/7/8 for r=1/2/3. This is a source-to-source conditional
corollary. It does not turn unsubmitted/rejected older sources into committed
graph claims. The last older graph catalogue at8360 has21 profiles; its
scope and publication history remain distinct. The new local theorem does
not require any catalogue, beta root, external proof input or incumbent core.

The pass began with the committed six-cycle separator exclusion8804; no
exhaustive residual-map domain was available. The result here supplies a
direct necessary contact condition for a genuinely remaining subfamily.
An exhaustive embedding/optimizer-occurrence bridge, and pentagonal and
hexagonal face branches, remain open. The next structural frontier is the
remaining r=3 cases containing a deficient five, or a justified larger-face
reduction; neither is assumed solved by this exclusion.
