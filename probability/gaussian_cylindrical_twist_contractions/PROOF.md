# Sharp endpoint-budget lifting for cylindrical twists

Complete author proof, 27 September 2026. Independent review and historical
priority are pending. The unrestricted three-dimensional Gaussian-majorisation
problem remains open.

## 1. The whole class and the exact endpoint condition

Let R>0, 0<a<1, let I be a nondegenerate interval in R, and let theta,h
be real Lipschitz functions on I. Write Q_phi for planar rotation through
angle phi, J(x,y)=(-y,x), and

\[
\mathcal C=\{(u,z):u\in\mathbb R^2,\ |u|\le R,\ z\in I\},\qquad
T(u,z)=(aQ_{\theta(z)}u,h(z)),\qquad k=a^{-2}-1>0.
\tag{1}
\]

The twist and the axial profile may be nonlinear and may reverse direction.
The total angle need not be small. The scale a is constant throughout the
cylinder. The exact condition for T to be 1-Lipschitz on the **whole solid
cylinder** is

\[
h'(z)^2+\frac{R^2}{k}\theta'(z)^2\le1
\quad\text{for almost every }z\in I.                  \tag{2}
\]

**Theorem.** Every map (1) satisfying (2) has a simultaneous continuous
contracting motion in R4, starting with the inclusion of C in R3 and
ending at T(C) in that same R3. Consequently, for every bounded Borel
probability law mu on C, every variance s>0 and every threshold b>=0,

\[
\int(\mu*\gamma_{3,s}-b)_+
\le\int((T_\#\mu)*\gamma_{3,s}-b)_+ .                 \tag{3}
\]

For every finite list x_i in C and arbitrary individual radii r_i>=0,

\[
\left|\bigcup_i B(Tx_i,r_i)\right|
\le\left|\bigcup_i B(x_i,r_i)\right|,\qquad
\left|\bigcap_i B(Tx_i,r_i)\right|
\ge\left|\bigcap_i B(x_i,r_i)\right|.                 \tag{4}
\]

Neither the law, its weights nor its support needs rotational symmetry.
Centers need not fill circles or the cylinder. It is the map that must
admit the extension (1)--(2); contractivity on a few selected sites alone
does not replace that hypothesis.

Here gamma_(3,s) is the centered Gaussian with covariance s I3. The
construction is a tangential input beyond azimuth-preserving meridian
maps. It is not an assertion that all endpoint-contractive screw matchings
lift: the [two-rigid-group obstruction](../gaussian_two_body_screw_obstruction/PROOF.md)
rules out that broader statement.

## 2. Why the endpoint condition is exact

At a height where theta and h are differentiable, undoing the output
rotation gives

\[
DT(\xi,\eta)=(a\xi+a\theta'Ju\eta,\ h'\eta).
\]

Put S=1-a^2. Completing a square gives the exact identity

\[
\begin{split}
|(\xi,\eta)|^2-|DT(\xi,\eta)|^2
={}&S\left|\xi-\frac{a^2\theta'}S Ju\eta\right|^2\\
&+\left(1-h'^2-\frac{a^2\theta'^2}{S}|u|^2\right)\eta^2.
\end{split}                                                    \tag{5}
\]

Since a^2/S=1/k, this is nonnegative for all |u|<=R exactly when (2)
holds. Necessity follows by taking interior radii tending to R and the
minimizing xi in (5). Sufficiency follows by integrating the derivative
bound on segments in the convex cylinder. One can justify the latter
without an exceptional-line issue by smoothing the Lipschitz curve
z->(R theta(z)/sqrt(k),h(z)) on interior subintervals: convolution preserves
its unit derivative-ball constraint. The resulting smooth maps are
1-Lipschitz by (5), and their locally uniform limit is T. Endpoint heights
of I follow by continuity. Thus no differentiability beyond Lipschitz
regularity is being hidden in the characterization.

## 3. Unfold the axial profile while adding the twist

Choose any reference height z0 in I. For 0<=t<=1 set

\[
\lambda_t=(1+kt)^{-1/2},\qquad
q_t(z)=\sqrt{1-t+t h'(z)^2},
\tag{6}
\]

and define signed integrals from z0 when z<z0:

\[
H_t(z)=(1-t)z_0+t h(z_0)+\int_{z_0}^z q_t(v)\,dv,
\qquad F_t(u,z)=(\lambda_t Q_{t\theta(z)}u,H_t(z)).
\tag{7}
\]

The derivatives in (6) are defined almost everywhere; their values on the
null exceptional set do not affect the integrals. All maps are continuous
in their inputs and in t. On any bounded input set their images remain
uniformly bounded. At t=0, F_0 is the identity. At t=1,

\[
F_1(u,z)=(aQ_{\theta(z)}u,A(z)),\qquad
A(z)=h(z_0)+\int_{z_0}^z|h'(v)|\,dv.                 \tag{8}
\]

The function A is nondecreasing; it is the unfolded axial coordinate.
The important schedule is reciprocal-square transverse scale and
square-root axial speed, rather than linear interpolation of those two
parameters.

### Direct all-pair proof

Fix heights z>w and transverse inputs u,v in the radius-R disk. For t<1
write

\[
\begin{split}
L_t&=\int_w^z q_t(x)\,dx,\qquad
B_t=\int_w^z\frac{1-h'(x)^2}{q_t(x)}\,dx,\\
\delta&=\theta(z)-\theta(w),\qquad
C_t=|Q_{t\theta(z)}u-Q_{t\theta(w)}v|.
\end{split}
\tag{9}
\]

These quantities are finite, with L_t>0 and B_t>=0. Cauchy--Schwarz and
(2) imply

\[
R|\delta|\le\sqrt{k}\int_w^z\sqrt{1-h'^2}
\le\sqrt{k L_tB_t}.                                  \tag{10}
\]

The squared distance is D_t=lambda_t^2 C_t^2+L_t^2. We have
L_t'=-B_t/2 and (lambda_t^2)'=-k lambda_t^4. The skew symmetry of J gives

\[
\left|\frac d{dt}C_t^2\right|\le2R|\delta|C_t.
\tag{11}
\]

For example rotate both vectors by -t theta(w); the derivative becomes
2 delta times a scalar product of JQ_(t delta)u with the difference of
the two vectors. Its absolute value is at most 2|delta|R C_t. Combining
(9)--(11),

\[
D_t'\le-k\lambda_t^4 C_t^2
       +2\sqrt{k}\lambda_t^2 C_t\sqrt{L_tB_t}-L_tB_t
     =-\bigl(\sqrt{k}\lambda_t^2C_t-\sqrt{L_tB_t}\bigr)^2\le0.
\tag{12}
\]

There is no sign assumption on theta' or h'. At equal heights the angle
difference and axial distance vanish, and the transverse scale decreases.
Continuity extends all pair comparisons to t=1, including possible
collisions and flat intervals of A. Thus F_t is one simultaneous
contracting motion in R3 on the entire cylinder.

### A second way to see the choice of schedule

For 0<=s<t<1, F_s maps C bijectively onto the convex cylinder of radius
lambda_s R over H_s(I). The relative map F_t F_s^(-1) is again of the
form (1). Its transverse scale squared is (1+ks)/(1+kt), its angle
derivative is (t-s)theta'/q_s, and its axial derivative is q_t/q_s.
Its endpoint condition reduces to

\[
q_t^2+\frac{R^2(t-s)}k\theta'^2\le q_s^2,
\tag{13}
\]

which is exactly (t-s) times (2). This is a consistency check of the
whole motion, not an independent theorem assumed in (12).

## 4. Fold the axis using just one extra coordinate

For z>=w,

\[
|h(z)-h(w)|\le\int_w^z|h'|=A(z)-A(w).                \tag{14}
\]

Hence there is a well-defined 1-Lipschitz function f on A(I) with
f(A(z))=h(z). If A has a plateau, h is constant on it, so this assertion
still holds. No inverse of A is required at t=1.

For the second phase keep the transverse vector v unchanged and use

\[
G_s(v,x)=\left(v,(1-s)x+sf(x),
                 \sqrt{s(1-s)}[x-f(x)]\right),\quad0\le s\le1.
\tag{15}
\]

The last two coordinates have squared pair distance

\[
(1-s)(x-y)^2+s[f(x)-f(y)]^2,                          \tag{16}
\]

which is nonincreasing by (14). Formula (15) is the classical
one-dimensional leapfrog. Concatenate (7), with a zero fourth coordinate,
and (15). The resulting R4 motion ends at T. This completes the
construction for arbitrary axial order reversals. No rematching of
labels, mass splitting, or symmetry of the input law is used.

The degenerate scales have elementary limits of the same conclusion:
at a=0 first collapse the transverse disk and then use the axial leapfrog;
the only endpoint requirement is Lip(h)<=1 and theta is irrelevant. At
a=1, nonexpansiveness on a solid cylinder forces theta'=0 almost
everywhere by the off-diagonal block of the derivative Gram matrix, so
theta is constant and a global rotation followed by the axial leapfrog
suffices. These cases are separate from the formula k>0.

## 5. Gaussian and ball-volume transfers

Pad the R4 motion by a zero coordinate to obtain an R5 motion.
[Aishwarya--Li, Theorem 1.4(i)(a)](https://arxiv.org/html/2609.07041v2)
compares sampled density values along continuous contractions. At the
endpoints the five-dimensional convolution is f(x)gamma_(2,s)(y).
For Y with density gamma_(2,s), gamma_(2,s)(Y) is uniform on [0,c],
c=(2 pi s)^(-1). Its sampled tail at cb is therefore exactly
integral(f-b)_+. This gives (3). This transfer, including the sufficiency
of two auxiliary coordinates, is explicitly prior work. If the closure
of a bounded support meets excluded endpoints of I, extend theta and h
continuously there; all inequalities and motion formulas pass to the
closure. The cited theorem then applies on that compact support.

For finite labels, (7) is analytic in t on every compact subinterval of
[0,1): the integrands in (6) admit locally uniformly convergent analytic
expansions there. Apply
[Bezdek--Connelly, Theorem 1](https://arxiv.org/pdf/math/0108098v1)
to each truncated first phase, padded to R5, and take t up to one.
Volumes of finite unions and intersections of fixed-radius balls are
continuous in the centers: their indicators converge almost everywhere
outside the finitely many limiting sphere boundaries and are uniformly
supported in a bounded set. The second phase is analytic after
s=sin^2(phi), and the same theorem applies. To arrange distinct finite
endpoints in that phase, first merge identical input centers, keeping
the largest radius for the union and the smallest for the intersection.
Replace f by f_epsilon=epsilon Id+(1-epsilon)f, still 1-Lipschitz.
Each distinct input pair can collide at the new endpoint for at most one
epsilon unless its transverse vectors differ, in which case it never
collides. Choose epsilon tending to zero off this finite exceptional set.
The axial leapfrog for each f_epsilon has distinct centers throughout
and endpoints in R3. Center continuity passes its conclusions to f.
This proves both inequalities (4); zero radii follow by continuity too.
No smoothness of theta,h as spatial functions is needed for this argument.

## 6. A full-dimensional tangential benchmark

Take R=1, a=c=3/5, omega=16/15, and

\[
\theta(z)=\omega z,\qquad h(z)=c|z|,
\qquad |z|\le3H,\quad H=15\pi/32.
\tag{17}
\]

Here k=16/9 and c^2+omega^2/k=1. The condition is saturated almost
everywhere, while the angle changes with height and the axial order
reverses. The theorem signs every bounded law on this cylinder at every
variance and permits arbitrary finite centers and individual ball radii.

This is a control for the class, not its definition. The seven source sites

\[
0,e_1,e_2,He_3,e_1+He_3,e_2+He_3,-He_3
\tag{18}
\]

have targets

\[
0,ae_1,ae_2,cHe_3,ae_2+cHe_3,-ae_1+cHe_3,cHe_3.
\tag{19}
\]

Their paired affine rank is six: the determinant of the six paired
differences, in source-then-target coordinate order, is
4ca^2H^2=108H^2/125. Thus the paired-rank-five sufficient condition does
not cover this finite restriction. All 21 endpoint inequalities are
strict; the checker checks them using exact rational bounds on H^2.

The **whole map**, not necessarily the seven-site restriction, also fails
the [scalar-defect criterion](../gaussian_majorisation_scalar_defect/PROOF.md)
in every pair of endpoint frames. Suppose unit e,f satisfy that criterion
for all pairs in the cylinder. At positive heights z and boundary |u|=1,
the tangent vector

\[
(\xi,\eta)=(aJu,1)
\]

is a zero-loss differential direction in (5). It is realized by a curve
on the cylinder boundary. Its image derivative is (Q_(omega z)Ju,c).
Dividing the scalar-defect inequality by the squared curve increment and
taking a limit yields

\[
e_3=c f_3,\qquad a e_\perp=Q_{\omega z}^T f_\perp.
\tag{20}
\]

Two positive heights H and 2H give rotations J and -I, forcing both
transverse parts to vanish. Unit lengths would then require |c|=1,
contradicting c=3/5. The checker verifies this finite linear-algebra
consequence of the differential constraints. Their realization by actual
nearby pairs is part of the written proof.

It is also genuinely non-normal in the displayed frame. On z>0 the
displacement W=T-Id has

\[
W\cdot\operatorname{curl}W
=a\omega(\cos(\omega z)-a)|u|^2
 +2a\sin(\omega z)(c-1)z.
\tag{21}
\]

At (u,z)=(0,H) this is -12H/25, nonzero. Locally W cannot be a scalar
multiple of a gradient. In particular it cannot directly follow the
normals of a fixed convex core, including signed nonlinear normal
profiles; the smooth-field argument is the one recorded in the
[earlier tangential dependency](../gaussian_tangential_screw_lift/PROOF.md).
No exclusion of arbitrary compositions or independent-frame normal
representations is claimed.

## 7. The sharp endpoint budget versus the concurrent twisted-meridian motion

The prepublication refresh found R6's concurrent
[twisted-meridian theorem](../gaussian_twisted_meridian_contractions/PROOF.md).
It permits general radial-to-axial coupling and variable transverse factors,
with a sufficient phase budget. The present theorem completes the endpoint
budget for the constant-scale, height-only class. The distinction is not
merely that the twist is nonconstant: that is already allowed by R6.

Here is an exact comparison, using the positive-height part of
theta(z)=omega z, h(z)=c z with 0<a,c<1. Put b_t=1-(1-a)t.
In R6's linear-meridian interpolation with any continuously differentiable
phase clock ell(0)=0, ell(1)=1, consider two radius-R inputs at heights
separated by epsilon. The squared pair distance is

\[
(1-t+t c^2)\epsilon^2
 +2b_t^2R^2[1-\cos(\alpha+\ell(t)\omega\epsilon)],
\tag{22}
\]

where alpha is their freely chosen initial azimuth difference. At any
fixed time choose the current azimuth difference to be v epsilon and
differentiate with the source pair held fixed. Dividing by epsilon^2
and taking epsilon to zero, nonexpansion requires, for every real v,

\[
-(1-c^2)-2(1-a)b_tR^2 v^2
       +2b_t^2R^2\ell'(t)\omega v\le0.
\]

Maximizing this quadratic in v gives

\[
R^2\omega^2\ell'(t)^2
\le\frac{2(1-a)(1-c^2)}{b_t^3}.
\]

Integration, using 1<=integral_0^1 |ell'| and
integral_0^1 b_t^(-3/2)dt=2(a^(-1/2)-1)/(1-a), forces

\[
R^2\omega^2\le B
:=\frac{8(1-c^2)(1-\sqrt a)}{a(1+\sqrt a)}.          \tag{23}
\]

In contrast, the exact endpoint bound proved and attained here is

\[
R^2\omega^2\le E:=\frac{(1-c^2)(1-a^2)}{a^2}.
\tag{24}
\]

For every 0<a<1,

\[
\frac BE=\frac{8a}{(1+\sqrt a)^2(1+a)}<1,
\]

since, for x=sqrt(a),

\[
(1+x)^2(1+x^2)-8x^2=(1-x)^2(x^2+4x+1)>0.            \tag{25}
\]

Thus a nonempty interval of endpoint-contractive twist slopes is outside
every C1 phase clock of that specific meridian interpolation. The saturated
benchmark (17) lies at E, so it is included by our theorem and excluded
from that interpolation. Equations (23)--(25) do not exclude other
motions, compositions, or all certificates in transformed endpoint frames.
They explain why changing the radial and axial schedules is useful.
R6's broader radial/axial dependence is not subsumed by our theorem.

## 8. What this changes, and what it leaves open

The construction signs a whole class with arbitrary height-dependent
twisting and axial folding at the **exact** endpoint Lipschitz budget.
It supplies a sharp-budget dependency for the R6 geometric chain; it does
not add a variant of the closed cap, flap, or rigid-screw constructions. The
[meridian theorem](../gaussian_meridian_contractions/PROOF.md) preserves
azimuth and allows different radial dependence. Neither theorem is claimed
to contain the other in full. Their constant-twist overlap and R6's
concurrent nonconstant-twist class are credited. Section 7 identifies the
additional endpoint range proved here.

The scale a must be constant, the transverse sections must be full disks
of the same radius, and theta,h depend only on height. General radial
dependence, disconnected screw domains, or arbitrary finite endpoint
contractions are not covered. The 24-site obstruction to a universal R5
screw theorem remains intact. The small-scale fixture is not a proof of
historical novelty or of optimal lifting dimension.

The new assertion is this simultaneous motion and class characterization.
The general motion-to-Gaussian and motion-to-ball transfers are classical.
[SOURCES.md](SOURCES.md) records the primary comparison and the current team
boundary. The exact checker audits algebra and controls; the universal
quantifiers, Lipschitz extension/approximation steps and analytic transfers
remain written mathematics, not formalization or independent review.
