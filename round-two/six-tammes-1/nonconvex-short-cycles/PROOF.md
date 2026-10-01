# Nonconvex short spherical cycles: sharp coverage and empty pentagons

Actual author **six-tammes-1**, role **researcher**, 2026-10-01.
Status: author-checked written proof; exact auxiliary checks are provided.
The geometric/topological proof is not formalized. Independent review is
pending. No global numerical Tammes-15 bound or optimality is claimed.

## 1. Statements

Let v_0,...,v_(m-1) be distinct unit vectors, m=3,4,5,6. Suppose their
successive minor-geodesic arcs form a simple closed curve and every boundary
inner product is at least k<1. Set b_m=cos(2*pi/m). Assume k>b_m; explicitly,

    m=3: -1/2<k<1,       m=4: 0<k<1,
    m=5: a<k<1,          m=6: 1/2<k<1,
    a=(sqrt(5)-1)/4.

These inequalities automatically put the entire boundary in an open
hemisphere. Let P be the closed bounded polygonal region in that hemisphere,
defined by gnomonic projection. It is the smaller of the two spherical
regions bounded by the curve. It may be concave and may have straight
angles. For every x in P,

    max_i x dot v_i >= sqrt((k-b_m)/(1-b_m)).        (1)

All four bounds are sharp, attained at the axis point of a regular
spherical m-gon with adjacent dot product k. No convexity, equal-side,
diagonal-packing, contact-graph, irreducibility, or degree premise is used.

A spherical c-code is a finite set of distinct unit vectors with all
pairwise dot products at most c. Put

    K5(c)=a+(1-a)*c^2.

**Unconditional pentagon exclusion.** Let 0<c<1. If five distinct points
of any c-code have their five prescribed cycle-edge dots at least
k>K5(c), then their minor arcs automatically form a simple hemispherical
cycle and its smaller closed region contains no further code point.
This includes concave cycles, without any facial-embedding assumption.
The strict threshold is sharp among arbitrary finite c-codes when
1/sqrt(5)<=c<1: at k=K5(c), a regular pentagon at height c plus its axis
point is a six-point c-code with a point inside the pentagon.

For the interval used in the Tammes-15 reductions, 1/2<=c<=3/5, the
explicit uniform band

    c-1/60 <= v_i dot v_(i+1) <= c

forces all the same conclusions with covering cosine **strictly greater
than c+1/500**. This removes the convexity premise from the earlier
pentagon exclusion and allows five times its uniform edge tolerance.
It trades its earlier larger margin for the larger tolerance; the exact
function K5 gives the complete threshold tradeoff.

On the narrower parameter interval 14/25<=c<=3/5, matching the nearby
contact-algebra exclusions, the wider band **[c-1/32,c]** gives covering
cosine **>c+1/400**, with the same unconditional emptiness conclusion.
This is an exact parameter theorem; it does not import an external
global upper bound to supply its parameter premise.

The supremum of all uniform edge tolerances ensuring pentagon emptiness
throughout [1/2,3/5], across arbitrary finite c-codes, is exactly

    E0=(7-3*sqrt(5))/16.

Every tolerance e<E0 works. At e=E0 emptiness fails in the regular example
with c=1/2. This sharpness concerns arbitrary code sizes, not a claim
about the sharp fifteen-point-specific tolerance.

## 2. The hemisphere is automatic

Put S=sum_i v_i and L=acos(k). At graph distance r along the cycle,
the spherical triangle inequality gives distance at most r*L. For the
distances used below, r*L<pi, so their dot product is at least cos(r*L).
For every vertex v_i the resulting lower bounds are

    m=3: v_i dot S >= 1+2*k,
    m=4: v_i dot S >= 1+2*k+(2*k^2-1)
                          = 2*k*(1+k),
    m=5: v_i dot S >= 1+2*k+2*(2*k^2-1)
                          = 4*k^2+2*k-1,
    m=6: v_i dot S >= 1+2*k+2*(2*k^2-1)+(4*k^3-3*k)
                          = (1+k)*(4*k^2-1).

Each is positive on its stated domain. For m=5, a is the positive root
of 4*k^2+2*k-1; for m=6 the bound is positive at k>1/2. Hence S!=0
and H={x:(S/||S||) dot x>0} contains all vertices and their minor arcs.
For m=3 the bound directly uses all three pairs, so no two-edge distance
estimate is needed even when k is negative.

Gnomonic projection in H takes each minor arc to a line segment. The
simple boundary becomes a simple planar polygon. Its bounded region
lies in the convex hull of its vertices, even if the polygon is concave.
The inverse image P is compact, lies in H, and has area less than 2*pi.
It is therefore the smaller spherical region. This also makes the
definition independent of which containing hemisphere is selected.

## 3. The minimum and the winding number

Write F(x)=max_i x dot v_i. Every x in P belongs to the hemispherical
geodesic convex hull of the vertices, because of the preceding planar
convex-hull containment. Thus x=w/||w|| for a nonzero nonnegative
combination w=sum_i lambda_i*v_i with sum_i lambda_i=1, and

    F(x)>=x dot w=||w||>0.                         (2)

On a boundary edge of length at most L, an endpoint is within distance
L/2, giving

    F(x)>=sqrt((1+k)/2).                           (3)

This is strictly greater than each bound in (1). The squared differences
for m=3,4,5,6 are respectively (1-k)/6, (1-k)/2,
(1-k)*(1+a)/(2*(1-a)), and 3*(1-k)/2.

If (1) fails, minimize F on compact P. Equations (2),(3) give an interior
minimum q with t=F(q)>0. A vertex is active when q dot v_i=t. Their
tangent directions at q are not contained in a closed semicircle. To
prove this, such a semicircle would supply a unit tangent vector e with
e dot v_i<=0 for every active vertex. Along q(s)=cos(s)q+sin(s)e their
inner products are at most t*cos(s)<t for small positive s. The inactive
vertices retain their strict slack, and q(s) stays in P. This contradicts
minimality. There are therefore at least three active vertices; all of
them have positive projection t onto q.

For every vertex define p_i=q dot v_i and its unit tangent direction
w_i=(v_i-p_i*q)/sqrt(1-p_i^2). No vertex is q, and no vertex is -q
because P and its vertices lie in H. Hence all w_i are defined.

Crucially, the w_i need not be in the same cyclic angular order as the
boundary vertices. Use signed principal angular increments instead:

    delta_i = the signed increment from w_i to w_(i+1) in (-pi,pi),
    theta_i = abs(delta_i).

These increments are well-defined, including delta_i=0. Opposite tangent
directions would force their minor edge through q or -q; the first is
excluded because q is interior, the second because the edge lies in H.
The direction along an edge traces exactly its principal angular arc:
the edge is a normalized positive combination of its endpoints, so its
tangent projection is a positive combination of the two tangent vectors.

Stereographic projection from -q takes P to a compact planar Jordan
region containing the origin. Its boundary has winding number +1 or -1
about the origin. Its radial direction is w, since the stereographic
image of v is (v-(q dot v)q)/(1+q dot v). Consequently

    sum_i delta_i = +2*pi or -2*pi,
    sum_i theta_i >= 2*pi.                         (4)

This replaces the convex-boundary-order step in the earlier proof. The
continuous Jordan/winding statement is part of the written argument,
not a numerical assertion from plotted coordinates.

## 4. The angle budget, including negative increments

For m=3 the direct convex-combination argument suffices, even for
-1/2<k<0:

    ||sum_i lambda_i*v_i||^2
        >= k+(1-k)*sum_i lambda_i^2 >= (1+2*k)/3.

Together with (2), this proves (1).

For m=4,5,6 the putative violating t satisfies t^2<k. At least three
projections are active and positive, leaving at most m-3 nonpositive
projections. If an edge has endpoint projections p,r, then

    v_i dot v_(i+1)
        = p*r+sqrt(1-p^2)*sqrt(1-r^2)*cos(theta_i). (5)

When both projections are positive, p,r<=t. An angle >=pi/2 would give
edge dot<=t^2<k. For b=cos(theta_i)>0, the two elementary inequalities
p*r<=(p^2+r^2)/2 and
sqrt(1-p^2)*sqrt(1-r^2)<=1-(p^2+r^2)/2 yield

    theta_i <= B=acos((k-t^2)/(1-t^2)) < pi/2.     (6)

For a mixed positive/nonpositive pair, an angle >=pi/2 gives nonpositive
edge dot. Otherwise (5)<=cos(theta_i), so theta_i<=acos(k)<=B as well.
Only an edge with two nonpositive projections can escape (6).

For m=4 there is at most one nonpositive vertex. All four increments
have absolute value <pi/2, contrary to (4).

For m=5, an exceptional edge would mean exactly two consecutive
nonpositive vertices, with the other three vertices all active. Those
three occur on the complementary two-edge path, whose total angular
variation is at most 2*B<pi. A continuous angular lift of that path has
range at most its variation, so its three active directions lie in an
open semicircle. This contradicts Section 3. Thus all five edges obey
(6), and (4) implies 5*B>=2*pi, hence

    (k-t^2)/(1-t^2)<=a,
    t^2>=(k-a)/(1-a),

a contradiction. Signed increments cause no problem.

For m=6 a violating t^2<2*k-1 gives B<pi/3. If there is no exceptional
edge, (4) is impossible because 6*B<2*pi. Otherwise, with at most three
nonpositive vertices, there is exactly one maximal consecutive run of
length r>=2, where r=2 or 3. A second run with an exceptional edge is
impossible. The complementary path, between the positive vertices just
after and before the run, contains every active vertex and has 5-r edges.
All these edges obey (6); its total angular variation is <(5-r)*pi/3<=pi.
Its active directions again lie in an open semicircle, a contradiction.
This proves (1) for hexagons as well, without a convexity premise.

Sharpness follows from vertices at height
h=sqrt((k-b_m)/(1-b_m)) with equally spaced horizontal directions. Their
adjacent dot products are k, their smaller region contains the axis point,
and F equals h there. These regular examples are valid on every stated
domain and prove equality in the bound.

## 5. A packing cycle is automatically simple

The unconditional pentagon hypothesis has k>K5(c)>c^2, since
K5(c)-c^2=a*(1-c^2)>0. The elementary short-edge planarity lemma from
the parent package applies. For completeness, if minor edges AB and CD
crossed at an interior point, positive combinations give

    W=alpha*A+beta*B=gamma*C+delta*D,
    ||W||^2 >= (1+k)*(alpha+beta)^2/2,
    ||W||^2 >= (1+k)*(gamma+delta)^2/2,
    ||W||^2 <= c*(alpha+beta)*(gamma+delta).

Therefore (1+k)/2<=c, contrary to k>c^2>=2*c-1. This rules out disjoint
edge crossings, including collinear overlap. An edge cannot pass through
a third code vertex: its length is <=acos(k)<acos(c^2)<2*acos(c),
while passage through a third point would require length >=2*acos(c).
Adjacent edges also cannot overlap without one containing the other
endpoint. Thus the prescribed five-cycle is a simple closed curve.
Section 2 supplies its hemisphere, since k>K5(c)>a.

Its covering cosine in (1) is strictly greater than c exactly when
k>K5(c). A further code point in the closed region would have dot
product >c with some boundary vertex, contradicting the code inequality.
This proves the unconditional pentagon exclusion.

There is a useful graph consequence. Join every pair of code points whose
dot product is at least a fixed k>K5(c), using minor arcs. This graph is
planar by the preceding crossing argument. Every cycle of length three,
four or five has an empty smaller region: (1) gives T5(k)>c, and T3,T4
are stronger. Thus this embedding has **no separating cycle of length
at most five**, where separation means code vertices on both sides.
Every chordless three-, four-, or five-cycle bounds an actual face; no
other edge can lie in its empty region without a boundary chord or a
forbidden crossing. This does not assert graph connectedness or exclude
isolated vertices in larger regions.

In particular, for an exact complete contact graph with actual maximum
dot product 1/sqrt(5)<c<1, take k=c>K5(c). Every chordless five-cycle is
an empty face even if it is concave. The statement extends the parent
four-cycle face bridge rather than claiming that pentagons are convex.

At k=K5(c), the regular pentagon at height c has these boundary dots,
with strictly smaller nonadjacent dots. Its axis-to-vertex dots are c.
The union is a c-code exactly when K5(c)<=c, equivalent to

    c-K5(c)=(1-c)*((1-a)*c-a)>=0,
    c>=a/(1-a)=1/sqrt(5).

Its axis point is interior, so the strict universal threshold is sharp.
The analogous hexagon covering bound still permits insertion when its
edge dots are c: sqrt(2*c-1)<c for c<1. No new hexagon capacity claim
follows from this extension.

## 6. Exact uniform tolerances

For c in [1/2,3/5], put e=1/60, d=1/500 and k=c-e. The bound

    a<3091/10000

follows from sqrt(5)<5591/2500, whose squared gap from 5 is exactly
9281/6250000>0. In particular k>=29/60>a and 0<c+d<1. Thus

    k-a-(1-a)*(c+d)^2
      > c-e-3091/10000-(6909/10000)*(c+d)^2 = g(c).

The polynomial g is concave and has exact positive endpoint values

    g(1/2)=928273/7500000000,
    g(3/5)=178863073/7500000000.

So T5(c-e)>c+d throughout the interval. This also gives k>K5(c)>c^2,
automatically satisfying the simplicity and hemisphere prerequisites.

For the narrower interval [14/25,3/5], take e=1/32 and d=1/400 instead.
The same rational upper bound on a and the same concavity argument give
positive endpoint lower bounds

    g(14/25)=107/102400,
    g(3/5)=14158371/1600000000.

Thus T5(c-1/32)>c+1/400 there. The proof needs only the explicit parameter
interval; no theorem about the global N15 optimum is imported.

To derive the optimal uniform threshold for emptiness, write

    E(c)=c-K5(c)=(1-c)*((1-a)*c-a).

E is strictly increasing on [1/2,3/5], since
E'(c)=1-2*(1-a)*c>0 there (already a>1/4 suffices). Its minimum is

    E(1/2)=1/4-3*a/4=(7-3*sqrt(5))/16=E0.

If e<E0 then c-e>K5(c) for every c in this interval. At e=E0, the
regular pentagon-plus-axis c-code with c=1/2 meets all five lower bounds
and has an interior code point. The same example remains allowed at
every e>E0. Thus E0 is the exact supremum of the universal tolerances.

## 7. Dependencies, prior art, and remaining scope

This is a strengthening of the
[parent sharp convex-polygon proof](https://github.com/helgithorskarp/math_results/blob/255d99ccd3ea40c4df2823f848b6154182f47bd7/round-two/six-tammes-1/short-polygon-cover/PROOF.md),
Discovery Net h8581,
`bafkreig6swikau7zwaf7adjvo3kgwqrvibjntzbhuijq7bak2na7tc5kym`.
The new ingredient is signed winding plus the short complementary
active-direction path. Convexity and a supplied hemisphere are removed
from the covering theorem, and from the pentagon packing exclusion.
The parent exact concave contact pentagon remains valid: concavity is
possible, but is now harmless for this covering/emptiness conclusion.

[Musin--Tarasov N14](https://arxiv.org/abs/1410.2536), Section 2.1 and
Section 3.2, credits the classical vertex-shift machinery and notes
convexity of irreducible contact faces. Proposition 3.2(7) gives the
classical qualitative isolated-point exclusion for convex contact faces
of at most five sides. Those facts are prior art. The present proof does
not assume irreducibility, does not certify a vertex shift, and does not
claim that arbitrary pentagons become convex. The broader nonconvex
unequal-side statement and sharp robust threshold are the output here.
A bounded fresh primary-literature and graph search found no identical
statement; this is not a historical priority claim.

The checker pins and reuses only the parent exact quadratic-field
implementation; its hash and immutable reader URL are in INPUTS.json.
It verifies the rational margin, threshold algebra, row-sum factorizations,
finite exceptional-role reductions, a genuine negative-increment example,
and a rank-three positive Gram certificate for the sharp six-point example.
The negative increment occurs inside the parent's actual concave contact
pentagon, at the normalized positive combination V+8*A+P; exact norms,
all ten pairs, noncrossing edges and winding one are checked again for
this new purpose. The four positive increment signs and the one negative
sign rule out reusing convex cyclic order without the new winding proof.
It does not certify the Jordan/winding, continuous minimum, or arc-crossing
proof. Those are the written trust boundary. No floating arithmetic,
optimizer, imported enumeration, or large proof input is used.

This theorem excludes points inside short pentagonal cycles regardless of
concavity and supplies the short-cycle face bridge just stated. It does
not eliminate pentagonal faces themselves, classify
hexagonal insertion regions, or establish occurrence of a forbidden motif
in every improving fifteen-point code. The next global geometric task is
to use this unrestricted short-cycle reduction with remaining pentagon/
hexagon face branches rather than repeat a qualitative convexity proof.
