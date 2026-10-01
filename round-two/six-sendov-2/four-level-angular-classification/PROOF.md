# Sharp angular ratio for all profiles with at most four original levels

Actual author **six-sendov-2**, role **researcher**, 2026-10-01.
Complete ordinary author proof with finite exact rational certificates;
unformalized, independent review of this extension pending. The inherited
sign-count lemma8851 and fourfold-family lemma8897 also have independent
review pending at the initial indexed8934 refresh. The three-level and
asymmetric-family inputs have scoped independent confirmations8806/8859.

## 1. Definition, exact theorem and inherited inputs

For a balanced norm-one real eight-vector theta set
\[
 e=\mathbf1/\sqrt8,\qquad P=I-ee^T,\qquad
 H=P\operatorname{diag}(\theta)P|_{e^\perp},\qquad
 w=\operatorname{diag}(\theta)e,
\]
\[
 \rho_\lambda=8\|\Pi_\lambda w\|^2,\qquad
 \eta=\sum_{\lambda\text{ distinct}}\rho_\lambda^2,
 \qquad X=\sum\theta_j^4,
 \qquad C=\frac{1-\eta}{X-1/8}.
\tag{1}
\]
Use full eigenspaces, including at collisions. At the uniform4+4 orbit
use the continuous value16 from
[lemma8753](../angular-three-level-transition/PROOF.md), confirmed in
[review8806](../../six-reviewer-1/three-level-angular-audit/REVIEW.md).
Let F4 be the closed subset with at most four distinct original coordinate
values. Normalization throughout this note is the Euclidean norm.

Let alpha be the unique root near -0.853410556973737 of
\[
4575t^4+11695t^3+11175t^2+4737t+746=0,
\]
and inherit
\[
 c_3=\frac{8(\alpha-1)^2(5\alpha+3)^2}
 {(15\alpha^2+24\alpha+10)(35\alpha^2+38\alpha+11)},
 \qquad 24.53389668<c_3<24.53389670.
\tag{2}
\]
Write O3 for permutations and sign changes of the normalization of
\[
                 (\alpha^4,1^3,-4\alpha-3).
\tag{3}
\]
Exponents on values indicate repeated entries.

**Theorem 1.** On all of F4,
\[
                    \boxed{C\le c_3,}
\tag{4}
\]
with equality exactly on O3. In particular every genuinely four-level
profile is strictly below c3. There is no positive uniform gap on that
open stratum: four-level profiles can approach (3).

**Theorem 2, useful paired strengthening.** If theta can be partitioned
into four equal pairs, including every collision, then
\[
       \boxed{C\le 28-96X=16-96(X-1/8)\le16.}
\tag{5}
\]
Equality in the first inequality is exactly the centrally symmetric
four-label multiset or the triple-label collision. The latter has
original multiplicities6+2, X=7/24 and C=0. Equality C=16 consists only
of the extended uniform4+4 orbit. Thus96 is the sharp coefficient of
the fourth-moment excess in (5); every nonuniform centrally symmetric
paired profile attains it. Section5 derives (5) from the credited paired
spectral invariant mechanism, independently regenerated here.

**Corollary 3, global restricted stability.** There exists b4>0 such that
\[
 c_3-C(\theta)\ge b_4\operatorname{dist}(\theta,O_3)^2
                    \quad(\theta\in F_4).
\tag{6}
\]
The coefficient and collar in this global bound are existential. The
sharp asymptotic local coefficient in F4 is the already audited
fourfold-splitting value Lambda4, with
340.462200<Lambda4<340.462201; no larger asymptotic coefficient works.
No effective neighborhood or optimum global b4 is supplied.

**Corollary 4, exact restricted uniform transition.** For
J_R=R X-eta, the uniform orbit is globally maximizing on F4 exactly
when R<=-c3. For R<-c3 it is the complete equality set. At R=-c3
the equality set is the union of the uniform orbit and O3. For
R>-c3 the O3 value is strictly larger than the uniform value. This
is the complete four-level variational transition, without assigning
the unrestricted all-sphere threshold.

The established inputs are precisely:8753/8806 for three-level bounds,
extension and local stability;8800, confirmed8859, for3+3+1+1;
8851 for sign-count/heavy-block exclusions;8897 for4+2+1+1.
The new remaining family is3+2+2+1. The earlier
[four-level displacement theorem7940](../../../sendov_degree9_four_level_displacement/PROOF.md)
optimizes a different, max-normalized objective J. Its conclusion does
not imply (4). The original degree-nine first-power endpoint and the
all-sphere Cstar=c3 assertion remain open.

## 2. Full-eigenspace original-moment bridge

For a nonzero balanced unnormalized u write N=sum u_j^2,
S3=sum u_j^3, S4=sum u_j^4, and m2=S4-N^2/8. The compression of
diag(u) has characteristic polynomial f'/8, where f=prod(z-u_j).
At each actual equal-level block of multiplicity m, the m-1 difference
vectors have zero coupling; the block-constant complement supplies one
simple root in each gap. The weighted secular function
sum m_i/(z-r_i) has strictly negative derivative between actual levels.
These facts, with collision conventions, are credited to
[7432](../../../sendov_collapsed_angular_quartic/PROOF.md) and
[review7496](../../../sendov_collapsed_angular_review3/PROOF.md).

If a labeled active cubic h has three distinct real roots lambda_i, it
is permissible to keep an additional inactive original-level root with
weight zero. For raw masses r_i=8||Pi_i diag(u)e||^2 the three identities
are
\[
 \sum r_i=N,\qquad \sum r_i\lambda_i=S_3,
 \qquad \sum r_i\lambda_i^2=m_2.
\tag{7}
\]
They follow from v=diag(u)e, Hv=Pdiag(u)v, and direct inner products.
Let p_k=sum lambda_i^k, G_ij=p_{i+j} for i,j=0,1,2,
mu=(N,S3,m2)^T, D=det G. The Vandermonde is invertible and hence
\[
 \sum r_i^2=\mu^TG^{-1}\mu,
 \qquad C(u/\sqrt N)=\frac{N^2D-\mu^T\operatorname{adj}(G)\mu}{m_2D}.
\tag{8}
\]
This also explains why normalized full eigenspaces, rather than splitting
a degenerate positive mass artificially, are essential. In the charts
below the cubic is simple wherever this expression is used. A labeled
zero mass introduces no extra positive mass.

The source reconstructs the original f'/8, raw moments in two routes,
Newton sums, G, adjugate and both ratio polynomials with Fraction
arithmetic. Seven additional full eight-coordinate controls compute
Frobenius projection of uu^T onto symmetric matrices commuting with
Pdiag(u)P. They use no active cubic or residue. This projection has
norm square sum||Pi_lambda u||^4, which is the raw mass-square sum in
(8), including all full eigenspaces and the orthogonal zero e mode.
Controls include a positive-label collision, negative-pair merger,
asymmetric paired collision, singular6+2 and uniform4+4. These controls
support implementation accuracy; the written spectral argument supplies
the universal identification.

## 3. Complete3+2+2+1 coverage and boundary

From [8851](../sign-count-angular-reduction/PROOF.md), any at-most-four-level
profile with C>=c3 has exactly four positive and four negative coordinates,
no zeros and no block of size at least5. All other sign sectors have
C<112/5, and all heavy-block profiles have C<20. These sufficient
constants are not asserted sharp.

In3+2+2+1 the triple and singleton must have one sign; the two pairs
have the opposite sign. Reflect to make the former positive. Their
positive total can be scaled to4, leaving negative-pair mean-1. Thus
every competitive profile, after permutation, is the normalization of
\[
 u=(a^3,(-1+x)^2,(-1-x)^2,4-3a),\quad
 0<a<4/3,\quad V=x^2\in[0,1),
\]
\[
                       N=8+12(a-1)^2+4V\ge8.
\tag{9}
\]
The closed rectangle is compact after normalization. On a=0,a=4/3
or V=1 there is a zero coordinate, so the sign exclusion gives
C<112/5. The V=0 boundary is4+3+1 and is bounded by c3 from8753.
Equality there is exactly a=-1/alpha, yielding (3). The collision
a=1 is4+2+2 and has C<=16 from the same three-level theorem. The
uniform point is(a,V)=(1,0), with its inherited continuous value16.

For 0<a<4/3 and0<V<1 the positive and negative labels are separated.
Four distinct labels give exactly three simple active roots. At a=1
the triple and singleton merge, producing one simple zero-mass root
at the positive label, and two gap roots. These three roots remain
distinct. On V=0 the analogous zero-mass root is at the negative label;
even at the uniform corner the cubic has three distinct roots. Thus
D>0 in every competitive interior and every root strip used below,
and m2>0 except at that uniform corner by the equality condition in
Cauchy--Schwarz for sum u_j^4 >=N^2/8.

Put A=z-a, B=(z+1)^2-V and d0=4-3a. For f=A^3B^2(z-d0),
\[
 f'/8=A^2Bh,
\]
\[
 h=z^3+(2a-2)z^2+
    (-V/2-3a^2/2+5a-9/2)z
    -Va+3V/2-3a^2/2+3a-3/2.
\tag{10}
\]
Use (8) to define positive-scaled integer polynomials n(a,V),d(a,V),
with C=n/d and d>0 in the strict interior. The complete coefficients
and normalization scalar are regenerated and recorded by
[verify.py](verify.py) and [expected.json](expected.json); there is no
external symbolic input. Each polynomial has a-degree10 and V-degree5.

For orientation the boundary ratio simplifies to
\[
 C(a,0)=\frac{72a^4-96a^3-208a^2+160a+200}
 {110a^4-644a^3+1427a^2-1410a+525}.
\tag{11}
\]
This expression at a=1 means the continuous extension. No monotonicity
in V is assumed: it is false. At a=1/10,V=1/4, the literal profiles
(1^3,-5^2,-15^2,37) and(1^3,-10^4,37) have respectively
\[
\frac{345593988944}{434411238715},\qquad
\frac{1069156}{1988185},
\]
whose difference287292132347164/1114438591799461 is positive.
Both lie far below c3; this only excludes the proposed fixed-a boundary
majorization. The exact values are regenerated by the ratio checker;
the first also has a separate full-coordinate pinching control.

## 4. Exhaustive necessary stationary certificate

At an interior stationary point both primitive positive-content derivative
numerators vanish:
\[
 p=\operatorname{prim}(n_a d-nd_a),\qquad
 q=\operatorname{prim}(n_V d-nd_V).
\tag{12}
\]
They have V-degrees9 and8. Give a weight1 and V weight2. All p terms
have weight<=19, and all q terms weight<=18, checked exactly. The formal
17 by17 Sylvester determinant in V therefore has a-degree at most170:
\[
8\cdot19+9\cdot18
-2\left(\sum_{j=0}^{16}j-\sum_{j=0}^{7}j-\sum_{j=0}^{8}j\right)=170.
\tag{13}
\]
Indeed an entry from a shifted row of p has a-degree bounded by
19-2 times its V exponent, and similarly for q. In each determinant
permutation the selected column degrees sum to0+...+16, while row
shifts sum to(0+...+7)+(0+...+8). A specialization that lowers a V
degree still uses this same formal matrix.

The complete universal identity is
\[
\operatorname{Res}_V(p,q)=k(a-3)(a-2)(a+1)^{14}(3a-5)^{14}
 (a-1)^{41}F_3^5F_6F_7F_{12}F_{17}F_{34},
\tag{14}
\]
with k=-38548364790109088594101492776960000000000. Every integer
coefficient of the named factors is printed in verify.py. Their product
has degree162, hence also satisfies the bound170. The checker evaluates
the original17 by17 matrix at every integer0,...,170 using exact integer
Bareiss determinants and verifies equality with the factored right side.
The degree bound makes171 agreements a polynomial identity, with no
numerical reconstruction or generic-specialization inference.

Sturm variation counts exhaust the real roots of each non-linear factor
in the whole interval(0,4/3). The only in-chart linear factor is a=1,
already bounded by16 as an original-label collision.

| Factor degree | Multiplicity in(14) | Roots in(0,4/3) | Certified isolating interval when present |
|---:|---:|---:|---|
|3|5|0|none|
|6|1|0|none|
|7|1|1|(17738947/44086634,17746771/44106079)|
|12|1|1|(879863/1222944,790092/1098169)|
|17|1|1|(2054307/1605941,3053246/2386855)|
|34|1|1|(2818709/2607070,429694/397431)|

The endpoints are rational nonroots, have independent count1, and
exhaust each factor's total chart count. For every one of these four
intervals I the whole polynomial
\[
                 (49/2)d(a,V)-n(a,V)
\tag{15}
\]
has **all six degree5 Bernstein coefficient polynomials in V strictly
positive throughout I**, using exact rational interval Horner evaluation
of each coefficient. Thus(15)>0 on I times[0,1], not just at a sampled
V or an approximate lift. The full positive bounds are in expected.json.
Since d>0 on these strips, every corresponding necessary stationary
candidate has C<49/2<c3. No converse assertion that a resultant root
is an actual stationary point is used, and no algebraic lift inversion
is required.

If a profile of this family had C>c3, compactness of the competitive
rectangle and the boundary analysis would give an interior maximizer,
away from a=1. Fermat's condition(12) would force one of the four
strips and contradict(15). Therefore C<=c3. Equality in the interior
would also be a stationary global maximum and yield the same
contradiction. The only equality is the inherited V=0 orbit(3).
This proves the complete3+2+2+1 family, including every sign sector
and collision by section3 and8851.

## 5. Paired invariant deficit on the full class

Write u=(t1,t1,t2,t2,t3,t3,t4,t4), sum ti=0, and form
\[
 g(z)=\prod_{i=1}^4(z-t_i)=z^4-Az^2-Tz+B,
 \quad f=g^2,\quad f'/8=gh,\quad
 h=g'/4=z^3-Az/2-T/4.
\tag{16}
\]
Here A>0 for nonzero u. Use capitals only in this section for the
quartic invariants; they are not the chart factors in(10). Define
\[
 K=A^2-4B,\quad I=A^2+12B,\quad
 \Delta=128A^3-432T^2.
\]
The Newton identities give N=4A,S3=6T,S4=4A^2-8B, so
\[
 X-1/8=K/(8A^2),\qquad m2=2K.
\tag{17}
\]
The credited [paired formula7883](../../../sendov_degree9_four_double_displacement/PROOF.md)
for the same full compression yields the raw pinching invariant
Psi=sum over distinct lambda of ||Pi_lambda diag(u)e||^4:
\[
 \Psi=A^2/8-B+6B^2/A^2
             +18T^2I^2/(A^2\Delta).
\tag{18}
\]
Its displacement objective and maximizer are retained as prior art.
This proof independently reconstructs f'/8, moments, Gram and adjugate
using (8), and verifies the complete denominator-cleared identity
\[
 \boxed{C=16-12K/A^2-576T^2I^2/(A^2\Delta K)}
\tag{19}
\]
wherever Delta,K are positive. Identity(19) is a consequence of the
credited spectral formula, not a claim that its mechanism is new.

For real labels g has four real roots. Its derivative has three simple
real roots unless at least three labels coincide: strict interlacing
handles four distinct roots, a single double root or two doubles.
Thus Delta>0 everywhere except that triple-label case. K>=0 follows
from(17) and Cauchy--Schwarz; K=0 is precisely the uniform4+4 orbit.
Consequently the last term in(19) is nonnegative throughout the
nonsingular nonuniform class, proving(5) there.

The invariant has the useful exact sum of squares
\[
 I=\frac{(t_1-t_2)^2(t_3-t_4)^2
        +(t_1-t_3)^2(t_2-t_4)^2
        +(t_1-t_4)^2(t_2-t_3)^2}{2}.
\tag{20}
\]
All three products vanish simultaneously exactly when at least three
labels coincide. To see this, partition the four labels into their
actual equal-value classes: if there is no class of size3, either all
labels are distinct, one class has size2, or two classes have size2;
in each case one displayed matching pairs unequal labels on both edges.
Balance excludes a quadruple coincidence for nonzero u. Thus I>0 in
the nonsingular class. Equality in the first inequality of(5) there
is exactly T=0, equivalent to even g and a centrally symmetric root
multiset, with multiplicities.

At the excluded triple-label profile(t,t,t,-3t), t!=0, the original
six-plus-two compression has a single positive mass, hence eta=1,
C=0 and X=7/24. Formula(5) is an equality directly; no Delta is divided.
At uniform, the inherited extension gives C=16, also an equality.
This exhausts all cases and proves Theorem2 and its equality statements.

## 6. Assembly, stability and remaining frontier

The five positive four-part partitions of8 are exactly the following.
Profiles with fewer levels are already bounded by8753; collision cases
in the listed families are consistent with those bounds.

| Four-level multiplicity | Bound and complete equality | Source |
|---|---|---|
|5+1+1+1|C<20|8851 heavy-block exclusion|
|4+2+1+1|C<=c3, equality only O3 collisions|8897|
|3+3+1+1|C<=c3, equality only O3 collisions|8800, confirmed8859|
|3+2+2+1|C<=c3, equality only O3 at V=0|sections3-4|
|2+2+2+2|C<=28-96X<=16|section5|

In particular no genuinely four-level row attains c3. This proves(4)
and the complete equality set, which does lie in F4 as a three-level
profile.

For Corollary4, away from uniform the exact difference from the uniform
value is J_R-(R/8-1)=(R+C)(X-1/8). Theorem1 and its equality set,
with X>1/8 away from uniform, immediately give all four assertions.

F4 is compact: it is the finite union, over partitions of the eight
coordinate indices into at most four nonempty blocks, of balanced unit
vectors constant on each block. The continuous extension of C is
inherited from8753/8806. Review8806 gives local full-sphere coercivity
with any fixed b<Lambda4; choose b340. Outside its neighborhoods of the
finite orbit O3, theorem1 and compactness give a positive minimum delta
of c3-C. Sphere chord distances are at most2. Thus
b4=min(340,delta/4)>0 proves(6); if that complementary set is empty,
take b340. This derives a global **restricted** existential coefficient.

For the sharp asymptotic local statement, the curve already used in
[review8859](../../six-reviewer-1/asymmetric-family-audit/REVIEW.md) is
\[
 u_\epsilon=((\alpha+\epsilon)^3,1^3,\alpha-3\epsilon,-4\alpha-3).
\]
After normalization it lies in F4. Its tangent is a pure fourfold
splitting, has zero sum and zero scalar product with u0, and has squared
norm12. The audited expansion in8806/8859 gives
(c3-C)/dist(theta,O3)^2 ->Lambda4. The full-sphere lower local bounds
with every fixed b<Lambda4 apply inside F4, while this curve excludes
a larger asymptotic coefficient. Endpoint validity on a whole collar
is not inferred.

Every potential violation of the all-sphere C<=c3 bound now has **at
least five distinct original levels**. Neither a universal support
reduction nor a certificate on that remaining stratum is given. A
gradient argument on compressed masses alone must still justify that
its variations come from actual original coordinates. The finite-energy
complex first-power inequality is also a separate obligation. Zhang's
[primary paper](https://arxiv.org/html/2609.19126), Conjecture1.2 and
Theorem1.3, keeps the first-power endpoint open while proving the
quadratic case. Ordinary Sendov is reported resolved there and in
[Tao's primary account](https://terrytao.wordpress.com/2026/08/12/a-digestion-of-the-proof-of-sendovs-conjecture/).

## 7. Reproduction and trust boundary

The standalone CPython3.11 standard-library source performs60 recorded
checks,171 integer17 by17 determinants, exhaustive rational Sturm
counts,24 whole-strip Bernstein coefficient bounds, the paired invariant
and sum-of-squares identities, and seven full-coordinate commutant
controls. Four damaged mathematical alternatives are rejected: wrong
resultant sign, omitted degree34 chart root, a false upper-bound constant,
and reversed active-cubic constant sign. Normal and optimized execution
must agree with the complete fixture; an altered external fixture is
separately rejected. See [README.md](README.md) for exact commands and
the canonical complete-record hash. The fixture is a regression record;
all decisive identities and signs are regenerated without importing it
as a mathematical premise.

The sparse Fraction kernel adapts the author's earlier8800/8897 work.
The171 specialization-safe determinant mechanism credits reviewer8859.
The paired spectral formula credits7883. Preliminary SymPy1.14.0
elimination and root isolation only selected factor coefficients and
rational endpoints: the source independently verifies the entire
identity, root exhaustion, interval signs and moment construction.
No floating-point input, generic algebraic lift, solver, incomplete
enumeration or external data certifies the theorem. Spectral
identification, compactness, Fermat necessity, the degree bound,
boundary/case coverage and inherited theorems are ordinary written
proof bridges; they are not checked by a proof-assistant kernel.
Finite author checks and graph/source publication are not independent
review. Detailed attribution and bounded current-status intake appear
in [LITERATURE.md](LITERATURE.md).
