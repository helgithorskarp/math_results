# Axial cone rotations and full Gaussian majorisation

Complete author proof, 26 September 2026. Independent mathematical review and
formalization are pending. The unrestricted dimension-three conjecture remains
open. The new input here is a contracting motion for a geometric class; the
implications from such a motion are established results.

The [consolidated scope statement](SCOPE.md) records the exact quantifiers,
comparison with later Team B work, and the claimed Kneser--Poulsen advance.
This revision retains Theorem 1 and the original exact checker unchanged;
it adds the class comparisons in Sections 4.1 and 5.1.

Write a point of Euclidean three-space as $(u,z)\in\mathbb C\times\mathbb R$,
with the usual real inner product on $\mathbb C$. For a centrally symmetric
compact convex planar body $P$ with $0$ in its interior, put

$$
C(P)=\{(zu,z):z\ge0,\ u\in P\}.
$$

Given two such bodies $P,Q$, define

$$
W(P,Q)=\operatorname{conv}\{\overline u v:u\in P,\ v\in Q\}\subset\mathbb C.
\tag{1}
$$

This is a centrally symmetric convex body. Here $\operatorname{per}$ means
ordinary Euclidean perimeter, and the cone sections have the fixed height
normalization $z=1$.

**Theorem 1 (a perimeter criterion).** If

$$
\operatorname{per}W(P,Q)\le4,
\tag{2}
$$

then the map on $D=C(P)\cup(-C(Q))$ given by

$$
T(a)=a\quad(a\in C(P)),\qquad T(-b)=b\quad(b\in C(Q))
\tag{3}
$$

has a continuous contracting motion in $\mathbb R^4$, with the first cone
fixed and the second cone moving rigidly. The pieces meet only at zero, where
the definitions agree. Consequently:

1. For every bounded Borel probability measure $\mu$ on $D$, every $s>0$, and
   every $h>0$, with $\gamma_{3,s}$ the Gaussian of covariance $sI_3$,

   $$
   \int(\mu*\gamma_{3,s}-h)_+\,dx
   \le \int(T_\#\mu*\gamma_{3,s}-h)_+\,dx.
   \tag{4}
   $$

   Thus full majorisation holds, equivalently every convex internal-energy
   comparison for which the energies are defined. Atom counts, weights,
   mass at zero, and the distribution inside each cone are unrestricted.
2. For any finite labeled centers $x_i\in D$, $y_i=T(x_i)$, and arbitrary
   radii $r_i\ge0$,

   $$
   \left|\bigcup_i B(y_i,r_i)\right|
   \le\left|\bigcup_i B(x_i,r_i)\right|,
   \qquad
   \left|\bigcap_i B(y_i,r_i)\right|
   \ge\left|\bigcap_i B(x_i,r_i)\right|.
   \tag{5}
   $$

   These are three-dimensional volumes. In particular, for every compact
   $K\subset D$ and every $r>0$,
   $|T(K)+rB_3|\le|K+rB_3|$.

The same statements hold after a common Euclidean similarity. No affine
change of the metric is allowed. A global 1-Lipschitz extension of (3) exists
by Kirszbraun's theorem, though the comparisons only use the specified domain.

**Corollary 2 (circular cones).** Set

$$
C_p=\{(u,z):z\ge0,\ |u|\le pz\},\qquad p,q>0.
$$

All conclusions hold for the central reflection
$C_p\cup(-C_q)\longrightarrow C_p\cup C_q$ whenever

$$
pq\le\frac2\pi.
\tag{6}
$$

For comparison, a simplicial cone $K$ with
$C_q\subseteq K\subseteq C_p^*$ exists **if and only if** $pq\le1/2$.
Hence the interval $1/2<pq\le2/\pi$ supplies cone domains outside every such
separator. The superscript $*$ always denotes the positive dual.

## 1. The motion and its exact geometric criterion

Let $J$ be rotation through $\pi/2$ on $\mathbb R^2$, and $R_\theta$ rotation
through $\theta$. Define

$$
k(\theta)=\max_{u\in P,v\in Q}u\mathbin{\cdot}J R_\theta v,
\qquad L=\int_0^\pi k(\theta)\,d\theta.
\tag{7}
$$

The body in (1) is centrally symmetric and contains a disk of positive radius.
Thus $k$ is positive, continuous, and $\pi$-periodic. Since
$u\cdot JR_\theta v=\operatorname{Re}(i e^{i\theta}\overline u v)$, $k$ is
the support function of $W$ along a rotating unit direction. Cauchy's planar
perimeter formula gives

$$
L=\tfrac12\operatorname{per}W.
\tag{8}
$$

For completeness, for a convex polygon the total variation of its boundary
projection in direction $e$ is twice its width in that direction. Integrating
over a half-circle of directions, each edge of length $\ell$ contributes
$2\ell$. Hence perimeter is the integral of width over that half-circle.
For a centrally symmetric body the width is twice its support function.
Approximation by inscribed convex polygons gives (8) for general convex
bodies. Rotation or reversal of the half-circle does not change this integral.

Use the parameter $\theta$ decreasing from $\pi$ to $0$, and set

$$
c(\theta)=-1+\frac2L\int_\theta^\pi k(\alpha)\,d\alpha,
\qquad d(\theta)=\sqrt{1-c(\theta)^2}.
\tag{9}
$$

For $b=(v_b,z_b)\in\mathbb R^3$ define the linear embedding

$$
F_\theta(b)=(R_\theta v_b,c(\theta)z_b,d(\theta)z_b)\in\mathbb R^4.
\tag{10}
$$

It preserves every inner product, because $R_\theta$ is orthogonal and
$c^2+d^2=1$. Its endpoints are $F_\pi(b)=(-b,0)$ and
$F_0(b)=(b,0)$. Keep every $a\in C(P)$ at $(a,0)$ and send $-b$ along (10).
Within either cluster all distances are constant.

For a cross-pair write $a=(z_a u,z_a)$ and $b=(z_b v,z_b)$, with $u\in P$,
$v\in Q$. The only changing part of its squared distance is

$$
-2z_a z_b\,[u\cdot R_\theta v+c(\theta)].
\tag{11}
$$

If $\theta=\pi(1-t)$, differentiation of the bracket gives

$$
\pi\left[\frac2L k(\theta)-u\cdot JR_\theta v\right]\ge0
\tag{12}
$$

when $L\le2$. Thus every cross-distance decreases. Trajectories are continuous
including at zero and at both endpoints. This proves the motion assertion and,
in particular, verifies directly that (3) is a contraction.

The criterion is exact **within this axial rotation form**. More precisely,
consider any absolutely continuous scalar functions $c(t),\theta(t)$ and a
continuous $d(t)$ with $c^2+d^2=1$, giving a contracting motion of the full two
cones by (10), with endpoints $-I$ and $I$. Then, for almost every $t$,

$$
c'(t)\ge |\theta'(t)|k(\theta(t)).
\tag{13}
$$

Indeed, central symmetry lets $u\cdot JR_\theta v$ attain both $k(\theta)$
and $-k(\theta)$. The cross-pair derivative must be nonnegative for every
$u,v$. To use a common set of full measure in this assertion, first take a
countable dense subset of $P\times Q$, intersect its derivative sets, and
then use continuity in $u,v$. Integrating (13) and using the endpoints and
periodicity gives

$$
2\ge\int_0^1 |\theta'|k(\theta)\,dt\ge L.
\tag{14}
$$

The last inequality follows also by taking an antiderivative of $k$: the
endpoint angles differ by an odd multiple of $\pi$. Thus (2) is necessary and
sufficient for this specified form, with the stated regularity in the
necessity direction. It is **not** asserted necessary for an arbitrary motion
in four or five dimensions, for majorisation, or for (5).

## 2. Circular cones and a fully explicit analytic path

If $P$ and $Q$ are disks of radii $p$ and $q$, then $W$ is the disk of radius
$pq$, so $L=\pi pq$. Formula (9) becomes $c=1-2\theta/\pi$.
An analytic parametrization, including its endpoints, is

$$
\theta(t)=\frac\pi2(1+\cos\pi t),\quad
c(t)=-\cos\pi t,\quad d(t)=\sin\pi t,\qquad 0\le t\le1.
\tag{15}
$$

This gives $F_t(v,z)=(R_{\theta(t)}v,c(t)z,d(t)z)$. For any cross-pair,

$$
\frac d{dt}\langle(a,0),F_t(b)\rangle
\ge\pi\sin(\pi t)z_a z_b\left(1-\frac\pi2 pq\right)\ge0.
\tag{16}
$$

This proves Corollary 2 without computing a support function. Equivalently,
with the continuous parameter $\tau=(1-\cos\pi t)/2$, the axial coefficient
increases at speed $2$, while the planar rotation has speed $\pi$. Condition
(6) is sharp among the axial paths covered by (13).

Zero slopes can be included separately by the same path (15): the relevant
transverse vectors are then zero and (16) still holds. Their degenerate
sections are not part of the body hypothesis of Theorem 1.

The perimeter criterion also improves on enclosing noncircular sections by
disks. For example, let
$P=Q=[-9/10,9/10]\times[-1/20,1/20]$. The product body is the hexagon with
vertices $(\pm13/16,0)$ and $(\pm323/400,\pm9/100)$. Its perimeter is

$$
\operatorname{per}W=\frac{323}{100}+\frac{\sqrt{13}}{10}
<\frac{18}{5}<4.
$$

Yet the smallest centered circular sections containing these rectangles
have slope product $13/16>2/\pi$ (already $3(13/16)>2$ and $\pi>3$).
Thus (2) uses more of the transverse geometry than the disk bound (6).

## 3. Gaussian and ball-volume consequences

We apply [Aishwarya--Li, Theorem 1.4(i)(a)](https://arxiv.org/html/2609.07041v2):
under a continuous contraction, a Gaussian-convolved density sampled from
itself increases in stochastic order. Pad (10) with one zero coordinate to
work in $\mathbb R^5$. At the endpoints the convolved densities are
$f(x)\gamma_{2,s}(y)$ and $g(x)\gamma_{2,s}(y)$, where
$f=\mu*\gamma_{3,s}$ and $g=T_\#\mu*\gamma_{3,s}$.

Let $C=(2\pi s)^{-1}$. If $Y$ has density $\gamma_{2,s}$, then
$\gamma_{2,s}(Y)=C e^{-E}$ with $E$ exponential of mean one. For an independent
$X$ with density $f$,

$$
\mathbb P\{f(X)\gamma_{2,s}(Y)>Ch\}
=\int f(x)(1-h/f(x))_+\,dx=\int(f-h)_+\,dx.
\tag{17}
$$

The analogous identity for $g$ turns stochastic order into (4). This is the
same two-coordinate cancellation proved in the team's
[paired-rank source](../gaussian_majorisation_rank_abel/PROOF.md), reproduced
here to make the bridge explicit. It does not cancel an arbitrary product
majorisation inequality; it uses the stronger density-value order supplied by
the continuous-motion theorem.

The unpadded four-dimensional motion also retains the stronger comparison

$$
\int f(x)F_{1/2}(\log(f(x)/h))\,dx
\le\int g(x)F_{1/2}(\log(g(x)/h))\,dx,
\tag{18}
$$

where $F_{1/2}$ is the Gamma$(1/2,1)$ distribution function, zero on negative
arguments. This follows by the same sampling calculation with one auxiliary
Gaussian coordinate. Equation (4), not a cancellation assumption about (18),
is the claimed majorisation conclusion.

For circular cones the path is analytic by (15). For finitely many centers
in the general theorem, choose centrally symmetric convex polygons
$P'\subset P$ and $Q'\subset Q$ with zero in their interiors containing all
the normalized transverse coordinates used by those centers. This is possible
by adjoining a sufficiently small square about zero before taking the finite
convex hull. Then $W(P',Q')\subseteq W(P,Q)$, and perimeter is monotone under
inclusion by the width formula above. The function $k$ for $P',Q'$ is the
maximum of finitely many sinusoidal functions. It has finitely many analytic
pieces and is strictly positive. Equations (9)--(10), with the cosine
reparametrization of $\tau$ used after (16), are therefore piecewise analytic,
including the square-root endpoints. Padding to dimension five and reversing
the motion permits [Bezdek--Connelly, Theorem 1](https://arxiv.org/pdf/math/0108098)
to be applied with $n=3$. It gives both inequalities (5), with the original
individual radii. Coincident centers and zero radii follow by continuity.

For the compact equal-radius consequence one may use (4) and
Aishwarya--Li, Theorem 1.8(i), with any full-support probability law on $K$.
Alternatively, take dense finite restrictions in (5). Thus the comparison
holds at every radius, not only at large radius or high Gaussian variance.

## 4. Separation from the simplicial class

We first record an elementary planar fact. If a triangle contains a centered
disk of radius $r>0$ and lies inside the centered disk of radius $R$, then

$$
r\le R/2.
\tag{19}
$$

To see this, list its three vertex directions in circular order. Some
consecutive angular gap is at least $2\pi/3$. Every gap is less than $\pi$,
since zero is in the interior. In the direction of the midpoint of the large
empty angular gap, each vertex has projection at most $R/2$: its angular
distance is at least $\pi/3$, and a negative projection already suffices.
The triangle's support value is therefore at most $R/2$, whereas containment
of the inner disk makes that value at least $r$. Equality is realized by the
equilateral triangle of circumradius $R$.

Now $C_p^*=C_{1/p}$. Slicing an intermediate simplicial cone $K$ at $z=1$
would give a triangle containing the disk of radius $q$ and contained in the
disk of radius $1/p$. Formula (19) proves necessity of $pq\le1/2$. The
equilateral triangle proves sufficiency. The theorem of
[researcher 7 on simplicial cone reflections](../gaussian_simplicial_cone_reflections/PROOF.md)
applies under exactly such an enclosure. Thus the circular range in Corollary
2 beyond $1/2$ is not covered by that criterion.

### 4.1. The converse containment also fails

The positive orthant $O=\operatorname{pos}\{e_1,e_2,e_3\}$ is simplicial
and self-dual. Therefore its central reflection, fixing $O$ and sending
$-O$ to $O$, is covered by the simplicial theorem (and by successive
one-sided coordinate folds). It does not satisfy our perimeter criterion,
even after choosing another common axis and larger centrally symmetric
sections.

Indeed, let $e$ be any unit axis for which both full positive clusters could
be contained in cones with compact height-one sections. Necessarily
$a_j=e\cdot e_j>0$ for $j=1,2,3$: a nonzero ray with nonpositive height
cannot belong to such a cone. Since $\sum_j a_j^2=1$, choose $j$ with
$a_j^2\le1/3$. The transverse coordinate of this ray at height one is

$$
u_j=\frac{e_j-a_j e}{a_j}\in e^\perp,
\qquad |u_j|^2=\frac1{a_j^2}-1\ge2.
$$

Both centrally symmetric sections $P,Q$ must contain $\pm u_j$. Identifying
$e^\perp$ isometrically with $\mathbb C$, their product body contains
$\pm\overline{u_j}u_j=\pm|u_j|^2$. A convex body's perimeter is at least
twice its diameter, so

$$
\operatorname{per}W(P,Q)\ge4|u_j|^2\ge8>4.
$$

This proves noncontainment in both directions between the two stated
geometric criteria. It is not an obstruction to other four-dimensional
motions: the coordinate folds give such motions for this orthant map.
Nor does it compare closures under arbitrary compositions of the criteria.

## 5. A rational 25-point witness to the additional scope

Let $\mathcal D$ be these twelve rational unit vectors, in circular order:

$$
\begin{split}
&(1,0),(4/5,3/5),(3/5,4/5),(0,1),\\
&(-3/5,4/5),(-4/5,3/5),(-1,0),\\
&(-4/5,-3/5),(-3/5,-4/5),(0,-1),\\
&(3/5,-4/5),(4/5,-3/5).
\end{split}
\tag{20}
$$

Take $p=3/4$, $q=4/5$,

$$
A=\{(pu,1):u\in\mathcal D\},\quad
B=\{(qu,1):u\in\mathcal D\},\quad
(0,A,-B)\longmapsto(0,A,B).
\tag{21}
$$

The circular theorem applies with $pq=3/5$: the classical bound $\pi<22/7$
gives $2-\pi pq>4/35$. This is a uniform analytic margin, not a sampled
trajectory sign. All 144 cross-pairs strictly contract, with squared-distance
loss between $8/5$ and $32/5$; the other 156 pairs preserve their distances.
All 25 centers in each configuration are distinct.

The numerical constant can be checked without a floating approximation:
$22/7-\pi=\int_0^1 x^4(1-x)^4/(1+x^2)\,dx>0$.
The checker verifies the polynomial division and rational integration in
this identity.

Even this finite example has no intermediate simplicial cone

$$
\operatorname{pos}(B)\subseteq K\subseteq\{w:a\cdot w\ge0\ (a\in A)\}.
\tag{22}
$$

Indeed the largest adjacent gap in (20) has cosine $4/5$. The polygon with
vertices $q\mathcal D$ contains a centered disk of radius
$r=3q/\sqrt{10}$. The section at $z=1$ of the cone on the right of (22) is
the polygon $d\cdot u\le1/p$ for all $d\in\mathcal D$, since $\mathcal D$ is
centrally symmetric. It lies in the centered disk of radius
$R=\sqrt{10}/(3p)$. These bounds follow by bisecting each adjacent angular
gap. Also every nonzero point in this dual cone has $z>0$, so a simplicial
intermediate cone would indeed have a triangular section. But

$$
\frac rR=\frac9{10}pq=\frac{27}{50}>\frac12,
\tag{23}
$$

contradicting (19).

Both $A$ and $B$ span $\mathbb R^3$. Using the directions east, north, west,
the determinants of the corresponding three rows are $2p^2=9/8$ and
$2q^2=32/25$. The six paired rows $(a,a)$ and $(-b,b)$ have determinant
$8(9/8)(32/25)=288/25$. Consequently the paired affine rank of (21), with
the origin included, is six and the displacement span has dimension three.
Paired affine rank is invariant under independent rigid alignments of the
two endpoints. Thus the at-most-six-points, rank-five, and two-dimensional
displacement criteria do not establish this example. Omitting the origin
would lose this rank distinction, since all targets would have $z=1$.

Nor is (21) a strong coordinatewise contraction in any orthonormal coordinates.
Such a contraction would require $a_jb_j\ge0$ for all $a\in A,b\in B$ and
every coordinate $j$. Since each cloud spans three-space, each coordinate
takes a nonzero value on each cloud. Hence after coordinate sign changes both
clouds lie in one orthant $O$. That would give the forbidden simplicial
separator $\operatorname{pos}(B)\subseteq O\subseteq A^*$.

Allowing independent rigid alignments does not repair this strong-contraction
criterion. After removing translations, distances within the anchored cloud
and zero are preserved. Coordinatewise inequalities must therefore all be
equalities on that cloud. In each scalar coordinate a distance-preserving map
of a finite subset of the real line is a common sign and a translation;
the translation is zero at the origin. Spanning by $A$ then forces the
relative orthogonal alignment to be a diagonal sign map in those coordinates.
Removing those signs returns to the preceding orthant contradiction.

Finally (21) admits no continuous contracting motion in $\mathbb R^3$ itself.
In any purported motion all within-cloud distances and all distances to the
origin remain constant, since their endpoint values are equal. Subtract the
moving origin and normalize by the uniquely determined continuous orthogonal
motion of three independent anchored vectors. The anchored cloud is fixed.
The moving cloud would then be a continuous orthogonal embedding of
$\mathbb R^3$ into itself running from $-I$ to $I$, which is impossible since
the determinants are $-1$ and $1$. The explicit motion therefore has minimal
ambient dimension four for this fixture. This is a motion obstruction only;
the Gaussian and ball comparisons are positive results.

### 5.1. Scalar-defect and common-target comparisons

The later [scalar-defect criterion](../gaussian_majorisation_scalar_defect/PROOF.md)
asks for fixed unit vectors $e,f\in\mathbb R^3$ satisfying, for all pairs,

$$
|x-x'|^2-|T(x)-T(x')|^2
\ge |e\cdot(x-x')-f\cdot(T(x)-T(x'))|^2.
$$

It cannot establish (21). Every distance to the origin is preserved, so
the pairs $(0,a)$ and $(0,-b)$ would force
$(e-f)\cdot a=0$ and $(e+f)\cdot b=0$. Spanning by $A$ and $B$ gives
$e=f$ and $e=-f$, impossible for unit vectors. This is precisely the
norm-preserving spanning obstruction already proved in that source,
specialized here and accompanied by an exact six-column matrix certificate.
Independent rigid alignments are included in the freedom to choose $e,f$.
The obstruction is to this sufficient inequality, not to a five-dimensional
motion; our four-dimensional motion exists.

For a measure-level comparison, give the displayed 25 labels distinct
positive weights $w_i=2^i/(2^{25}-1)$, $0\le i\le24$. The
[common-target theorem B](../gaussian_majorisation_common_target/PROOF.md)
then says that every positive finite mixture of source laws, each mapped
deterministically to this same 25-atom output law, has every component
source equal to the original law. Each component map is a bijection on
the support. Distinct weights force it to use the prescribed labels.
Thus such a mixture cannot rescue any criterion already excluded for this
prescribed map, including the scalar-defect and paired-rank-five criteria.
With repeated weights a component may instead permute equal-weight labels;
the injective-target theorem alone does not exclude those rematchings.
This argument does not exclude stochastic couplings or decompositions after
smoothing. The axial theorem itself needs neither distinct weights nor a
mixture, and applies to all probability weights.

## 6. Scope and verification

The criterion (2) is a geometric sufficient condition for the full shared
question, with an additional Kneser--Poulsen class at arbitrary radii. The
finite certificate demonstrates that this class adds cases beyond the
specific existing criteria checked above. It does not establish historical
priority or exclude every possible composition or reformulation of known
methods. See [SOURCES.md](SOURCES.md) for the bounded literature and team audit.

[verify.py](verify.py) checks the rational fixture, all pair distances, rank
minors, disk-sandwich constants, and universal polynomial identities for the
isometric motion and its Cauchy--Schwarz bound. It also checks a noncircular
product polygon and invalid controls. No finite sample proves an
all-time, all-angle, Gaussian, or volume inequality: those depend on the
written argument and the cited primary theorems. Computation uses exact
integers and fractions, without a solver, floating sign test, external data,
or missing large certificate.

[scope_audit.py](scope_audit.py) supplements the unchanged original checker:
it checks the scalar-obstruction matrix, a positive identity-map control,
and the distinct normalized weights in Section 5.1. The all-axis orthant
argument in Section 4.1 is a written proof, not an axis search. These are
author checks; no independent review is implied.
