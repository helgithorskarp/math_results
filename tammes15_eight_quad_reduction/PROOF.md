# Short-corner triangles and four-cycles in the Tammes-15 contact branch

Author: **six-tammes-1**, role: **researcher**. Date: 2026-09-29.
Status: complete unformalized hand proof with exact arithmetic and finite
cover checks. Independent review is pending.

## Statement

Let `X` consist of fifteen distinct unit vectors, with minimum geodesic
separation `d` and `c=cos(d)`. Join **every** pair at distance `d` by its
shorter great-circle arc. Suppose the resulting complete contact graph is
connected, has degrees 3, 4, or 5, and decomposes the sphere into simple
strictly convex triangles and quadrilaterals, each contained in an open
hemisphere. Suppose it has exactly eight quadrilateral faces.

Assume first `1/2<c<=119/200`. All conclusions also hold for
`1/2<c<beta`, where `beta` is the unique root in `(119/200,3/5)` of

\[
1+4c+2c^2-4c^3-11c^4-24c^5=0,
\qquad 0.598431478994<\beta<0.598431478995.
\tag{1}
\]

The wider interval uses the independently verified rhombus inequalities
of [4]; its endpoint is excluded. No optimality or numerical upper-bound
improvement is claimed.

Set `alpha=acos(c/(1+c))` and `x=2pi-4alpha`. At a degree-four vertex let
the **triangle deficit** be `2-t`, and at a degree-five vertex let it be
`4-t`, where `t` is the number of incident triangular faces. Let `D` be
the vertices with positive deficit. Construct `H` on `D` by adding one
edge for each pair of opposite quadrilateral corners whose common angle
is strictly below `x`.

**Lemma.** `H` is a simple embedded triangle-free graph. Every deficient
degree-five vertex has deficit one and degree two in `H`. A four-cycle
of `H` cannot contain two or more degree-five vertices.

Consequently at most two degree-five vertices have positive deficit. The
necessary degree/deficit cover has 35 profiles, and the necessary colored
auxiliary cover has 18 types across six deficit distributions. If there
are two deficient degree-five vertices, `H` is a four-vertex path with
these two vertices internal. Counts are proved in Section 7.

These assertions concern the stated branch. They neither enumerate all
contact graphs nor declare a survivor geometrically realizable. In
particular they do not exclude `q=8` itself. No two different
quadrilaterals are required to be congruent.

## 1. Local geometry and the deficit cover

We use the rhombus identities and inequalities proved in [3,4]:

\[
\begin{split}
\rho(t)&=2\arctan\frac1{c\tan(t/2)},&
b&=2\arctan\frac1{\sqrt c},\\
y&=\rho(x),&z&=2\pi-2\alpha-y.
\end{split}
\tag{2}
\]

Triangle corners equal `alpha`. A quadrilateral is a spherical rhombus;
opposite corners agree, adjacent corners are `t,rho(t)`, and its
diagonals bisect their endpoint corners. Every quadrilateral corner
satisfies `alpha<t<2alpha`. In the indicated interval,

\[
\frac{3\pi}8<\alpha<\frac{2\pi}5,
\quad x<z<b<y<2\alpha,
\quad y>\frac{2\pi}3,
\quad x<\frac\pi2.
\tag{3}
\]

The upper bound on `alpha` is `5alpha<2pi` from [3,4]. For its lower
bound, `c<3/5` gives `c/(1+c)<3/8`, and
`cos(3pi/8)>3/8`: squaring reduces the latter to `sqrt(2)<23/16`,
whose square is `512<529`.

Two vertices can be opposite in at most one quadrilateral face. Indeed,
the other two vertices solve `P dot Q=R dot Q=c`, `||Q||=1`. The two
contact planes meet in a line and have at most two sphere intersections.
`P,R` are independent: equality is excluded by distinctness and
antipodality by `c>0`. The existing simple face supplies both intersections,
so its four vertices and minor boundary arcs are fixed; only one
strictly convex region in an open hemisphere can be that face. A
contacting pair cannot be opposite in a quadrilateral, because its
contact diagonal would split the face. We call these the **uniqueness**
and **contact** rules.

Euler and incidence, with `q=8`, give

\[
e=31,\quad f_3=10,\quad n_5=n_3+2,\quad n_4=13-2n_3.
\tag{4}
\]

A degree-three vertex has no triangles: one triangle and two strict
quadrilateral corners sum to less than `5alpha<2pi`. Similarly a
degree-four vertex has at most two triangles, and a degree-five vertex
has at most four. The total deficit is

\[
2n_4+4n_5-3f_3=4.
\tag{5}
\]

An ordinary degree-five vertex has one rhombus corner `x`. At an
ordinary degree-four vertex both rhombus corners exceed `x`, since they
sum to `2pi-2alpha` and each is below `2alpha`. At degree three all
corners exceed `x`, for the same reason applied to the other two corners.
Thus every corner below `x` is in `D`.

At a deficient degree-five vertex of deficit `delta`, all `delta+1`
rhombus corners are below `x`: the other four corners are at least
`alpha`, with one strict inequality. Equal opposite corners give
`delta+1` different neighbors in `D` by uniqueness. Hence

\[
|D|\ge\delta+2,\qquad 4\ge\delta+(|D|-1)\ge2\delta+1.
\tag{6}
\]

Therefore every deficient degree five has deficit one, three triangles,
and two rhombi. At a degree-four deficit-one vertex, three corners below
`x` are impossible because `3x+alpha<2pi`; this uses
`alpha>3pi/8>4pi/11`. At a degree-four deficit-two vertex, four such
corners are impossible because `4x<2pi`.

Each rhombus has at most one below-`x` opposite pair: its adjacent
corners exceed `y>x`. Thus `H` has one interior diagonal per contributing
face, no crossings, and no loops or multiple edges. Its degree bounds
for colors `4/1,4/2,5/1` (degree/deficit) are respectively

\[
\deg_H\le2,\quad\deg_H\le3,\quad\deg_H=2.
\tag{7}
\]

Since the total deficit is four, it has at most four vertices. If it has
four, all have deficit one; if it has fewer, the simple-graph bound also
gives maximum degree two. These facts precede any cycle exclusions.

## 2. Diagonal lengths, triangle angles, and common neighbors

For an edge of `H`, let its rhombus small corner be `u<x` and adjacent
large corner `v=rho(u)>y>2pi/3`. The diagonal between the small corners
has cosine

\[
r=c^2+(1-c^2)\cos v,
\qquad
-\frac13<\frac{4c^2}{1+c}-1<r<\frac{3c^2-1}{2}<\frac1{25}<\frac1{16}.
\tag{8}
\]

The lower expression follows from `v<2alpha`; it is increasing in `c`
and equals `-1/3` at `c=1/2`. The upper expression follows from
`v>2pi/3`, and `c<3/5`. For any two edge cosines `r,s` in this interval,

\[
-1/48<rs<1/9,\qquad
K:=\sqrt{(1-r^2)(1-s^2)}>8/9.
\tag{9}
\]

For a spherical triangle whose three sides are edges of `H`, the cosine
law gives, for every smaller angle `theta`,

\[
\cos\theta=\frac{r-st}{\sqrt{(1-s^2)(1-t^2)}},
\qquad -\frac12<\cos\theta<\frac3{32}.
\tag{10}
\]

Indeed the numerator is between `-4/9` and `1/12` and the denominator
exceeds `8/9`. In particular `theta<2pi/3`. The formula also excludes
a degenerate triangle.

No three vertices of an `H` triangle have a common unit contact
neighbor `Z`: by (8),

\[
\|P+Q+R\|^2=3+2(r+s+t)<9c^2,
\quad Z\cdot(P+Q+R)=3c,
\tag{11}
\]

contrary to Cauchy--Schwarz. Consequently the two rhombi for incident
edges of such a triangle cannot be adjacent at any of its vertices:
their shared boundary neighbor would contact all three vertices.

Two independent vertices have at most two common contact neighbors by
the contact-plane intersection argument. If their inner product is
`p<-5/9`, they have none, since such a neighbor would imply

\[
4c^2\le\|P+Q\|^2=2(1+p)<8/9,
\quad\text{whereas }4c^2>1.
\tag{12}
\]

We will repeatedly use these exact neighbor counts.

For later use, every triple of pairwise contacting vertices bounds an
empty equilateral minor triangle, hence a triangular face. To see
emptiness, a nonvertex point in its spherical convex hull is a normalized
positive combination `V=(sum a_i P_i)/||sum a_i P_i||`, with at least two
positive coefficients. For each triangle vertex,
`P_j dot sum a_i P_i >= c sum a_i`, while
`||sum a_i P_i||<sum a_i`. Thus `P_j dot V>c`, contradicting minimum
separation if `V` were a further point of `X`. The triangle is in an
open hemisphere since `c>0`; its minor contact arcs bound that empty face.

## 3. The auxiliary graph is triangle-free

Put

\[
C=2\pi-3\alpha,\quad\phi=C/2=\pi-3\alpha/2,
\quad\psi=\phi+\alpha=\pi-\alpha/2>2\pi/3.
\tag{13}
\]

At a deficient degree-five vertex the two rhombus angles sum to `C`.
If the rhombi are adjacent, the smaller angle between their bisecting
`H` directions is `phi`; if separated by one and two triangles, it is
`psi`. The adjacent case is impossible in an `H` triangle by (11), and
the separated case contradicts (10).

At a degree-four deficit-one vertex, two `H` corners `u,v` and the
third rhombus corner `h` satisfy

\[
u+v=2\pi-\alpha-h>C,\qquad\alpha<h<2\alpha.
\tag{14}
\]

Again adjacency contradicts (11). Otherwise the two separating corners
are `alpha,h`, and the smaller bisector angle is
`(u+v)/2+alpha>psi>2pi/3`, contrary to (10). It is the smaller angle
because `u,v<x`, so this expression is below `x+alpha=C<pi`.

An `H` triangle without a deficit-one vertex would need three deficit-two
vertices and total deficit at least six. By (5) this is impossible.
Therefore `H` is triangle-free.

## 4. Mixed four-cycles and the basic Gram identities

On a four-cycle, associate to every edge its common small rhombus angle.
At a degree-five vertex the sum of its two edge angles is `C`. At a
degree-four deficit-one vertex that sum is strictly larger than `C`
by (14). The sum of the two-angle totals over either bipartition of an
even cycle is the sum of all edge angles. Thus a part of two degree-five
vertices cannot face a part containing any degree-four vertex. This
excludes cycles with three degree fives and one degree four, and with
two opposite degree fives and two degree fours.

For the remaining cases write

\[
k=\frac{c}{1+c},\quad B=\cos(\alpha/2)=\sqrt{\frac{1+k}{2}},
\quad a=\cos\phi=(1-2k)B,\quad b=\cos\psi=-B.
\tag{15}
\]

Then

\[
1/3<k<3/8,\quad 3/4<B<5/6,\quad 3/16<a<1/3.
\tag{16}
\]

For four unit vertices in cycle order, if the side cosines are `r,s,r,s`
and opposite cosines are `p,q`, their Gram matrix separates, under the
simultaneous exchange of opposite vertices, into the two blocks

\[
\begin{pmatrix}1+p&r+s\\r+s&1+q\end{pmatrix},
\quad
\begin{pmatrix}1-p&r-s\\r-s&1-q\end{pmatrix}.
\tag{17}
\]

Rank at most three requires a zero determinant of at least one block.
The cosine law gives `p,q=rs+Ka` or `rs+Kb` when the corresponding
stars have smaller direction angle `phi` or `psi`.

A second useful identity concerns sides `r,s,t,s`. If the two stars at
the ends of the `r` side have direction cosines `a0,b0`, put
`p=rs+K b0`, `q=rs+K a0`. Resolving both remaining points along and
normal to the plane of that side gives the two possibilities

\[
t=rs^2+sK(a_0+b_0)-r(1-s^2)a_0b_0
 \ \pm\ (1-s^2)\sqrt{(1-a_0^2)(1-b_0^2)}.
\tag{18}
\]

Explicitly their projected inner product is
`[s(p+q)-r(pq+s^2)]/(1-r^2)`. Their perpendicular-product magnitude
is `K^2 sqrt((1-a0^2)(1-b0^2))/(1-r^2)`. Substitution gives (18),
covering both orientation choices. The denominators are positive by (8).

## 5. Four deficient degree-five vertices require sixteen points

If all four cycle vertices have degree five, their edge angles alternate
`u,C-u,u,C-u`, hence their side cosines alternate `r,s,r,s`.
Opposite direction types agree by the cosine law and equality of `p,q`
at opposite corners. There are three choices for the two types in (17).

If both are `phi`, then `p=q=rs+Ka`, with
`0<p<4/9`, `|r+s|<2/3`, and `|r-s|<19/48`. Therefore both determinants
in (17) are positive: `1+p>1` and `1-p>5/9>19/48`.

If one is `phi` and one `psi`, put

\[
U=1+ab=(1+k+2k^2)/2.
\]

The determinants are

\[
K\{KU-2kB(1+rs)\},\quad K\{KU+2kB(1-rs)\}.
\tag{19}
\]

The second is positive. The first is positive because

\[
\frac{1+rs}{K}<\frac54,
\quad\frac{U}{2kB}=\frac{1+k+2k^2}{4kB}
 >\frac{112}{27\sqrt{11}}>\frac54.
\tag{20}
\]

The numerator is larger than `14/9` and the denominator smaller than
`3sqrt(11)/8`. The last comparison squares to
`448^2>135^2*11`, namely `200704>200475`.

Only `psi` at all four vertices remains. Now

\[
p=q=rs-KB<1/9-(8/9)(3/4)=-5/9.
\tag{21}
\]

Opposite cycle pairs have no common contact neighbor by (12); adjacent
cycle pairs are noncontacts by the contact rule. Each adjacent pair has
exactly two common contact neighbors supplied by its rhombus. These eight
neighbors are distinct and outside the four cycle vertices: any two
different cycle edges together contain an opposite pair, which has no
common contact neighbor.

At each degree-five vertex the four neighbors in its two rhombi are
distinct, so its fifth contact is outside those eight and the four cycle
vertices. A neighbor of a nonincident cycle edge would contact the
opposite cycle vertex as well, which is forbidden by (12). These fifth
contacts are distinct from one another: an adjacent pair already has
its two possible common contact neighbors and an opposite pair has none.
Thus at least `4+8+4=16` points are required. This contradicts `|X|=15`.
This particular sixteen-point argument does not require other vertices
to be ordinary.

## 6. Two adjacent degree fives also require sixteen points

Name the cycle `A(5),B(5),C(4),D(4)` in order; every vertex has deficit
one, so these are all exceptional vertices. The small edge angles are
`u,v,w,v`, where `u+v=C` and `w>u` by (14). Their side cosines are
`r,s,t,s`, with `t>r`, because the diagonal cosine

\[
R(\theta)=\frac{4c^2}{1+c^2+(1-c^2)\cos\theta}-1
\tag{22}
\]

increases strictly on `(alpha,x)`. This formula follows by eliminating
the other diagonal from the rhombus Gram identities, or from (2),(8).

### 6.1 Both degree-five stars must have type psi

Apply (18). If both stars have type `phi`, the absolute value of its
first three terms is less than `8/27`, and the last term has magnitude
greater than `64/81`. Indeed `|r|,|s|<1/3`, `a<1/3`, `K<=1` give
`|r|[s^2+(1-s^2)a^2]+2|s|Ka<8/27`.
Thus the two possible `t` values are above `40/81` or below `-40/81`,
both outside (8).

If the stars have different types, define

\[
U=1+ab\le53/64,\quad J=-ab\le2/9,
\quad V=\sin\phi\sin\psi=(1+k-2k^2)/2\ge35/64.
\tag{23}
\]

For the plus choice in (18),

\[
t>35/72-25/243-5/128>1/16.
\tag{24}
\]

Here `s^2+(1-s^2)J<=25/81`, and the negative contribution
`-2skBK` is bounded below by `-5/128` when `s>0`; it is positive
when `s<=0`. The positive final term is larger than `35/72`.
For the minus choice,

\[
t-r=-(1-s^2)\left[rU+V+2skB\sqrt{\frac{1-r^2}{1-s^2}}\right]<0.
\tag{25}
\]

The bracket exceeds `35/64-53/192-15/64=7/192`, using
`B<5/6` and `sqrt((1-r^2)/(1-s^2))<9/8`. This contradicts `t>r`.
Consequently both stars have type `psi`. Then

\[
p=A\cdot C=q=B\cdot D=rs-KB<-5/9.
\tag{26}
\]

Opposite pairs have no common contact neighbors. Exactly as in Section 5,
the four cycle vertices are noncontacts, the eight rhombus neighbors are
distinct and outside the cycle, and the fifth neighbors `T_A,T_B` are
distinct and outside those twelve points.

### 6.2 Alternating sides of the cycle

Under the simultaneous exchange `A<->B,C<->D`, the Gram blocks now have
determinants

\[
(1+r)(1+t)-(p+s)^2,\quad (1-r)(1-t)-(p-s)^2.
\tag{27}
\]

We have `p>-41/48`, from `rs>-1/48`, `K<=1`, and `B<5/6`, so
`-11/12<p-s<-2/9`. The second determinant is larger than
`(15/16)^2-(11/12)^2>0`. Rank at most three forces the first to vanish.
Because `p+s<0`, the sums satisfy

\[
A+B=-\lambda(C+D),\qquad\lambda>0.
\tag{28}
\]

The minus block has rank two and the plus block rank one; hence the four
points span `R^3` and every three are independent. With
`delta=det(A,B,C)!=0`, the determinants at consecutive turns are

\[
\det(D,A,B)=-\delta,\quad\det(A,B,C)=\delta,
\quad\det(B,C,D)=-\delta/\lambda,
\quad\det(C,D,A)=\delta/\lambda.
\tag{29}
\]

The interior-diagonal cycle is simple and embedded by Section 1. The
sign of a turn distinguishes which side of an oriented simple spherical
cycle contains its smaller-angle sector. Equation (29) therefore puts
the smaller sectors at `A,C` on one side and those at `B,D` on the
other. The nonzero determinants exclude straight or degenerate turns.

At `C,D`, the two cycle rhombi cannot be adjacent: adjacency would
identify two of their already distinct eight boundary neighbors. As
these vertices have degree four, their remaining corners are one
triangle and one third rhombus, whose angle is

\[
h=2\alpha-(w-u)>7\alpha-2\pi>x>\alpha.
\tag{30}
\]

The inequality uses `w<x`, `u>alpha`, and `11alpha>4pi`. Their
smaller bisector sector contains the triangle because `h>alpha`; its
angle is `(v+w)/2+alpha<C<pi`. The larger sector contains the third
rhombus. Similarly at `A,B` the smaller sector contains one triangle
and the larger contains the two triangles using `T_A,T_B`.

Let `R_C,R_D` be the opposite corners of `C,D` in their third rhombi.
It follows that `T_A,R_C` lie on the same side of the cycle, and
`T_B,R_D` on the other. These are strict sides: all other contact-graph
vertices are off the cycle, whose edges lie inside the original rhombi.
Contact edges and third faces cannot cross this cycle. Thus
`R_C!=R_D`, `R_C!=T_B`, and `R_D!=T_A`.

### 6.3 The third-rhombus opposite corners are new points

`R_C` is outside the four cycle vertices. Opposite `C` is `A`, and
they have no common contact neighbors; `B,D` are already opposite
`C` in the other two rhombi and uniqueness applies. It is also outside
the eight boundary neighbors. The four contacting `C` cannot be
opposite `C`. If `R_C` were an `AB` rhombus neighbor, it and the
`BC` neighbor of the third rhombus would form a contact triangle with
`B`. If it were a `DA` neighbor, it would form the analogous contact
triangle with `D` and the `CD` neighbor.

These remaining candidates are ordinary vertices. The triangle rules
out degree three. Degree five is impossible because its only rhombus
angle is `x<h`. At ordinary degree four the two rhombus angles sum to
`2pi-2alpha`, but the candidate already has a corner larger than `y`,
and its new corner `h` gives

\[
h+y-(2\pi-2\alpha)>9\alpha+y-4\pi>\pi/24>0.
\tag{31}
\]

This is impossible too. Hence `R_C` is outside these twelve points,
and the symmetric argument applies to `R_D`.

Finally `R_C!=T_A`. Such an identification would give five distinct
contact neighbors: `A`, the two `AB/DA` neighbors in `A`'s two
triangles, and the two `BC/CD` neighbors in `C`'s third rhombus.
It must have degree five, and is ordinary, but its corner `h>x`
contradicts its unique rhombus corner `x`. Similarly `R_D!=T_B`.
Together with Section 6.2 these give sixteen distinct points: the four
cycle vertices, eight boundary neighbors, and `T_A,T_B,R_C,R_D`.
The adjacent-two-five cycle is excluded.

Sections 4--6 exclude every four-cycle with at least two degree fives.

## 7. Complete necessary auxiliary cover

Write `a0=n3`, and let `d41,d42,d51` count deficient vertices of the
three colors. Equations (4)--(7) give all initial profiles:

\[
0\le a_0\le6,\quad n_4=13-2a_0,\quad n_5=a_0+2,
\quad d_{41}+2d_{42}+d_{51}=4,
\quad d_{41}+d_{42}\le n_4,\quad d_{51}\le n_5.
\tag{32}
\]

There are nine deficit distributions and 53 degree/deficit profiles.
The distribution `(d41,d42,d51)=(0,1,2)` forces a triangle of `H`
and removes seven profiles. The distributions `(1,0,3)` and `(0,0,4)`
force a four-cycle after triangles have been excluded, removing six
and five profiles. Thus 35 remain. The surviving distributions are:

| d41 | d42 | d51 | n3 | Degree profiles | Colored H types |
|---:|---:|---:|:---|---:|---:|
| 4 | 0 | 0 | 0..4 | 5 | 6 |
| 3 | 0 | 1 | 0..5 | 6 | 3 |
| 2 | 0 | 2 | 0..5 | 6 | 1 |
| 2 | 1 | 0 | 0..5 | 6 | 5 |
| 1 | 1 | 1 | 0..5 | 6 | 1 |
| 0 | 2 | 0 | 0..5 | 6 | 2 |
| Total | | | | 35 | 18 |

For four `4/1` vertices the six types are the empty graph, one edge,
two disjoint edges, a three-vertex path and isolate, the four-vertex
path, and the four-cycle. With three `4/1` and one `5/1` the types
are a three-vertex path centered at `5/1` plus an isolate, a
four-vertex path with `5/1` internal, and the four-cycle. With two
of each color only the four-vertex path with both `5/1` internal
remains. The three-vertex mixed `4/1,4/2,5/1` case is the path
centered at `5/1`. For `4/1,4/1,4/2`, there are the empty graph,
either color type of a single edge, and a path centered at either
color. Two `4/2` vertices give the empty graph or one edge.

`check.py` generates every edge mask on these at most four colored
vertices, applies the proved bounds and forbidden subgraphs, and
canonicalizes under color-preserving permutations. A second generator
partitions the vertices into path components and a possible four-cycle;
it compares the complete colored component signatures entry by entry.
It also regenerates all 53 initial profiles, all 35 survivors, and each
profile's allowed type codes. No geometric realization is asserted.

## 8. Exact checks, trust boundary, and context

The checker uses only integer and `Fraction` arithmetic. It checks the
rational margins in (8)--(10),(16),(20),(23)--(27), elementary polynomial
identities for the Gram determinants and (18), and the full finite cover.
`--selftest` rejects forbidden triangles and cycles, tests color
canonicalization and confirms that a single-five cycle and the allowed
two-five path are retained. Normal and optimized Python have identical
output. `EXPECTED.json` and `SHA256SUMS` are compact evidence.

These checks do not formalize spherical geometry, the cycle-side argument,
or the reduction to the contact equations. The complete hand proof above
is part of the claim's trust boundary. No floating-point conclusion,
solver verdict, incomplete enumeration, external certificate, large proof
corpus, or private ledger is used by the checker. The calculation involves
at most 64 graphs per distribution, not an exhaustive contact-graph search.

Musin--Tarasov [1,2] supply the classical contact-graph method and local
rhombus setting, not the present fifteen-point optimality claim. Yuan--Wang
[6] classify tilings when **all** rhombi are congruent; that hypothesis is
absent here. Current coordinate tables [7] still list the fifteen-point
incumbent without an optimality asterisk. The coordinate file was refreshed
unchanged (SHA-256
`1b77ee43d73613885d3fdcfb03dc8fad2e40302ff9c9ff639559cc9b326fb805`).
Targeted primary-literature searches did not locate these particular
auxiliary exclusions; this is bounded evidence and no priority claim.

Complementary six-tammes-2's prescribed-pattern results [8] classify the
two known thirty-contact patterns and force a missing edge in one
twenty-nine-contact pattern. Their integer/Fraction checker was read and
reproduced. These are citations, not logical premises of this proof.

### References

1. O. R. Musin and A. S. Tarasov, *The Tammes problem for N=14*,
   [arXiv:1410.2536](https://arxiv.org/abs/1410.2536), Experimental
   Mathematics **24** (2015), 460--468.
2. O. R. Musin and A. S. Tarasov, *Extreme problems of circle packings on
   a sphere and irreducible contact graphs*,
   [arXiv:1410.0744](https://arxiv.org/abs/1410.0744).
3. six-tammes-1, researcher, [triangle/quadrilateral dense-branch
   exclusion](https://github.com/helgithorskarp/math_results/blob/main/tammes_15_triangle_quad_exclusion/PROOF.md),
   source commit `49cc563183ceb804ba9c892cdaa3412dccc991be`, graph
   `bafkreia5jsqd4h2cd3laimpvt4rnvymvc2orhgaoazfaljionj6irfrvvq`, h7137.
4. six-reviewer-1, reviewer, [independent audit and interval/N
   refinements](https://github.com/helgithorskarp/math_results/blob/main/tammes_15_triangle_quad_exclusion_review1/README.md),
   source commit `f026ccec6854eb913e5c156f4ff0cf08ed5cb4a9`, graph
   `bafkreiflxdrel4fv4opchhucsisp7ylw2lsfgtrv4q7tya3o5vjh4ld53a`, h7182.
   This verifies [3]; it is not a review of the present result.
5. six-tammes-1, researcher, [seven-quadrilateral
   exclusion](https://github.com/helgithorskarp/math_results/blob/main/tammes15_seven_rhombus_exclusion/PROOF.md),
   source commit `cf2d8b5a7d860a666ab1115433d6a3e8fbe0e7e1`, graph
   `bafkreib7v7j2ex5iccpokhbiav53ufgjf6n5fm4x2dgb5fzgeobye7ykma`, h7192.
6. Q. Yuan and E. Wang, *Tilings of the sphere by congruent regular
   triangles and congruent rhombi*,
   [arXiv:2311.01183](https://arxiv.org/abs/2311.01183), Journal of Algebra
   (2025), [DOI](https://doi.org/10.1016/j.jalgebra.2025.03.033).
7. H. Cohn, [spherical code table](https://spherical-codes.org/),
   [author table](https://cohn.mit.edu/spherical-codes/),
   [fifteen-point coordinates](https://spherical-codes.org/data/3/15).
8. six-tammes-2, researcher, [specified contact-pattern
   classification](https://github.com/helgithorskarp/math_results/blob/main/tammes15_contact_pattern_obstruction/README.md)
   and [29-edge
   completion](https://github.com/helgithorskarp/math_results/blob/main/tammes15_contact_pattern_obstruction/DELETED_CONTACT.md),
   new completion source commit `59bfe4614d633dcb192149b81812f902f2802a84`,
   graph `bafkreidtdcxrljqkivui6vf64ocxre63md7mzm44sskvwjh6qfslqumhje`, h7204.
