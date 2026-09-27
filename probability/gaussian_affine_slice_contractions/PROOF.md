# Contractions affine on parallel slices admit a five-dimensional motion

Complete author proof, 27 September 2026. Independent correctness review and
historical priority are pending. The unrestricted three-dimensional question
remains open.

## 1. Statement and an effective hypothesis

Let K be a closed convex subset of R2 with nonempty interior, and let I be a
nondegenerate interval of R. Let A:I->R^(2x2), b:I->R2 and h:I->R be Lipschitz.
Write

\[
 f_z(u)=A(z)u+b(z),\qquad T(u,z)=(f_z(u),h(z)),\qquad (u,z)\in K\times I.
 \tag{1}
\]

**Theorem.** If T is 1-Lipschitz on the entire prism K x I, then there is one
simultaneous continuous contracting motion of that prism in R5, from its
standard inclusion in R3 to T in the same R3. On any finite set of labels the
motion is piecewise smooth in the sense used by Bezdek--Connelly.
Consequently, for every bounded Borel probability law mu on K x I, every
variance s>0, and every threshold a>=0,

\[
 \int_{\mathbb R^3}(\mu*\gamma_{3,s}-a)_+
 \leq \int_{\mathbb R^3}((T_\#\mu)*\gamma_{3,s}-a)_+ .             \tag{2}
\]

Here gamma_(3,s) is the centered Gaussian density with covariance s I3.
Equivalently, all convex internal energies with U(0)=0 compare in the
majorisation direction whenever the integrals are defined. For every finite
list of centers x_i in the prism and arbitrary individual radii r_i>=0,

\[
 \left|\bigcup_i B(Tx_i,r_i)\right|\leq
 \left|\bigcup_i B(x_i,r_i)\right|,\qquad
 \left|\bigcap_i B(Tx_i,r_i)\right|\geq
 \left|\bigcap_i B(x_i,r_i)\right| .                              \tag{3}
\]

There is no symmetry assumption on K, the law, or the selected centers.
The matrices may be noncommuting, anisotropic, orientation reversing or
singular. Their singular values may change with z. The slice centers b(z)
may follow a curved path; h may fold or have plateaux. No extra contraction
margin, phase budget, number-of-atoms bound, covariance condition, or
restriction on s or a is imposed.

For checking the hypothesis, at a common differentiability height put
w=A'(z)u+b'(z). Nonexpansiveness of (1) is equivalent to

\[
 M(z,u)=\begin{pmatrix}
 I-A^TA&-A^Tw\\-w^TA&1-h'^2-|w|^2
 \end{pmatrix}\succeq0
 \quad\text{for every }u\in K,\text{ for a.e. }z\in I.           \tag{4}
\]

For necessity, first take interior u and a height where A,b,h are all
differentiable. Every direction of the derivative of T has norm at most
one. Continuity in u extends (4) to the boundary. These differentiability
heights form a single set of full measure independent of u. In particular,
||A(z)||<=1 and |h'(z)|<=1. Continuity gives the matrix bound at every
height. Conversely, integrate the derivative bound on a segment in the
convex prism. On a nonhorizontal segment the height is a nonconstant affine
function, so the exceptional heights have parameter measure zero. On a
horizontal segment use ||A(z)||<=1. This proves sufficiency without an
exceptional-line assumption. If K is a polytope, it suffices to check (4)
at its vertices: the derivative matrix is affine in u, and its operator
norm is convex in u. Formula (4), without inverses, includes all singular
cases.

The condition is on a whole prism extension, not merely on finitely many
selected endpoint pairs. A target height depending on u, or a general
nonlinear map on the transverse slice, is outside this theorem.

## 2. Horizontal completion of the slice maps

First suppose ||A(z)||<=c<1 uniformly. Set

\[
 D=I-A^TA,\qquad P=I-AA^T.
\]

Both matrices are positive definite. Completing a square in (4) gives

\[
\begin{split}
 |\xi|^2+\eta^2-|A\xi+w\eta|^2-h'^2\eta^2
 ={}&\left|D^{1/2}\bigl(\xi-D^{-1}A^Tw\eta\bigr)\right|^2\\
 &+\bigl(1-h'^2-w^TP^{-1}w\bigr)\eta^2.
\end{split}                                                     \tag{5}
\]

We used I+A D^(-1) A^T=P^(-1). Thus for every u in K, at almost every z,

\[
 w^TP^{-1}w\leq1-h'^2.                                          \tag{6}
\]

Fix an interior reference height z0. Starting with
B(z0)=D(z0)^(1/2), solve the matrix ordinary differential equation

\[
 B'=-B^{-T}A^TA'.                                                \tag{7}
\]

This is an ordinary finite-dimensional Caratheodory ODE on the invertible
matrices: its coefficients are measurable in z and locally integrably
bounded, and its right hand side is locally Lipschitz in B. The usual local
existence theorem applies on both sides of z0. Along any such solution,

\[
 (B^TB)'=-A'^TA-A^TA',\qquad B^TB=I-A^TA=D.                      \tag{8}
\]

Consequently the singular values of B lie between sqrt(1-c^2) and one.
The solution cannot leave the invertible matrices or escape to infinity
on a finite height interval; the right hand side is bounded there. Local
continuation therefore gives a solution throughout I. Define d(z0)=0 and

\[
 d'=-B^{-T}A^Tb',\qquad
 V(z)=\binom{A(z)}{B(z)},\quad e(z)=\binom{b(z)}{d(z)},\quad
 E_z(u)=V(z)u+e(z)\in\mathbb R^4.                               \tag{9}
\]

The following identities hold almost everywhere:

\[
 V^TV=I,\qquad V^TE_z'(u)=0,\qquad
 |E_z'(u)|^2=w^T\bigl(I+A D^{-1}A^T\bigr)w
             =w^TP^{-1}w\leq1-h'^2.                            \tag{10}
\]

Thus each E_z is an affine isometry of the entire transverse plane, and
the velocity of every point is perpendicular to its current slice plane.
This moving-frame completion is used only to prove a bound; the final
contracting motion does not require solving the ODE. In particular the
endpoints in (1) need not move on normal rays of a fixed convex set.

## 3. A uniform bound on transverse distance gain

Put omega(z)=sqrt(1-h'(z)^2). We claim that for all u,v in K and z>=w in I,

\[
 |f_z(u)-f_w(v)|^2-|u-v|^2
 \leq\left(\int_w^z\omega(s)\,ds\right)^2.                     \tag{11}
\]

First use the strict-matrix hypothesis of Section 2. For a running height
s in [w,z] let G(s)=|E_s(u)-E_w(v)|^2. The decomposition

\[
 E_s(u)-E_w(v)=V(s)(u-v)+E_s(v)-E_w(v)
\]

and the orthogonality in (10) give

\[
\begin{split}
 G'(s)&=2\langle E_s'(u),E_s(v)-E_w(v)\rangle\\
 &\leq2\omega(s)\int_w^s\omega(q)\,dq.
\end{split}                                                     \tag{12}
\]

All these curves are absolutely continuous on compact intervals. Integrate
(12), use G(w)=|u-v|^2, and drop the nonnegative squared distance in the last
two coordinates. This proves (11), including the translations b.

To remove strictness, replace (A,b) by ((1-epsilon)A,(1-epsilon)b), leaving
h unchanged. This is postcomposition of T by the linear contraction
diag(1-epsilon,1-epsilon,1), so all the hypotheses persist and the new
matrix norm is at most 1-epsilon. The right side of (11) is unchanged.
Let epsilon decrease to zero. This proves (11) in full generality, including
unit singular values and changing ranks. No inverse of a singular matrix
and no limit of the ODE solutions is used in this step.

## 4. An explicit contracting motion in R5

We use coordinates (x,H,y) in R2 x R x R2. For 0<=t<=1 define

\[
 q_t(z)=\sqrt{1-t+t h'(z)^2},\qquad
 H_t(z)=(1-t)z_0+t h(z_0)+\int_{z_0}^z q_t(s)\,ds,              \tag{13}
\]

with signed integrals below z0, and

\[
 \Phi_t(u,z)=\bigl(\sqrt{1-t}\,u,\ H_t(z),\ \sqrt t\,f_z(u)\bigr).
                                                                    \tag{14}
\]

This combines the distance-gain bound (11) with the unfolded axial speed
used in R4's [cylindrical-twist construction](../gaussian_cylindrical_twist_contractions/PROOF.md).
The new input is (11) for arbitrary affine slices, rather than the
constant conformal slice matrices of that construction.

Fix z>w. For t<1 write

\[
 L_t=\int_w^zq_t,\qquad C_t=\int_w^z\frac{\omega^2}{q_t},\qquad
 Q=|f_z(u)-f_w(v)|^2-|u-v|^2.
\]

The squared pair distance in (14) is
(1-t)|u-v|^2+t|f_z(u)-f_w(v)|^2+L_t^2. Differentiation is justified by
q_t>=sqrt(1-t) on every compact subinterval of t<1, and L_t'=-C_t/2.
Therefore its derivative is

\[
 Q-L_tC_t\leq\left(\int_w^z\omega\right)^2-L_tC_t\leq0.         \tag{15}
\]

The last inequality is Cauchy--Schwarz applied to sqrt(q_t) and
omega/sqrt(q_t). For equal heights, the pair square is
(1-t)|u-v|^2+t|A(z)(u-v)|^2, also nonincreasing. Continuity extends all
comparisons to t=1, even where h'=0. This is one simultaneous contraction
on the whole prism. Its endpoints are

\[
 \Phi_0(u,z)=(u,z,0),\qquad
 \Phi_1(u,z)=(0,H_1(z),f_z(u)).                                  \tag{16}
\]

Next apply the common ambient orthogonal rotation

\[
 (x,H,y)\longmapsto
 (\cos\alpha\,x+\sin\alpha\,y,\ H,
  -\sin\alpha\,x+\cos\alpha\,y),\qquad0\leq\alpha\leq\pi/2.
                                                                    \tag{17}
\]

All distances stay constant. Its endpoint is (f_z(u),H_1(z),0). Put

\[
 H_1(z)=h(z_0)+\int_{z_0}^z|h'(s)|\,ds.
\]

For z>=w, |h(z)-h(w)|<=H_1(z)-H_1(w). Thus there is a well-defined
1-Lipschitz function g on H_1(I) with g(H_1(z))=h(z). A plateau of H_1
forces h to be constant there. Finally, keeping the transverse vector v
fixed, use the one-dimensional leapfrog

\[
 (v,x,0,0)\longmapsto
 \bigl(v,(1-s)x+sg(x),\sqrt{s(1-s)}(x-g(x)),0\bigr),
 \qquad0\leq s\leq1.                                           \tag{18}
\]

Its axial and auxiliary squared pair distance is
(1-s)(x-y)^2+s(g(x)-g(y))^2, which decreases. The final point is
(f_z(u),h(z),0,0). Concatenating (14), (17), and (18) proves the
five-dimensional lifting assertion. Every phase is continuous jointly in
the source point and time, and bounded source sets have uniformly bounded
trajectories. No particle relabelling, splitting, or averaging is used.

For any fixed label the first phase is real analytic for 0<t<1. Indeed,
q_t is bounded away from zero on compact time subintervals and has a
locally uniformly convergent analytic expansion there; integration in
(13) preserves this property. The other two phases are analytic in their
interiors. The only possible nonsmooth times are the finitely many phase
endpoints. This is precisely the piecewise-smooth regularity in
Bezdek--Connelly, Section 3; no truncation with an endpoint outside R3 is
being used.

## 5. Gaussian internal energies and individual-radius ball volumes

Apply [Aishwarya--Li, Theorem 1.4(i)(a)](https://arxiv.org/html/2609.07041v2)
to the R5 continuous contraction. At either endpoint the convolved density
is F(x,y)=f(x) gamma_(2,s)(y), where f is the corresponding R3 density.
If Y has density gamma_(2,s), then gamma_(2,s)(Y) is uniform on [0,c],
c=(2 pi s)^(-1). Consequently the sampled-density tail is exactly

\[
 \mathbb P\{F(X,Y)>ca\}=\int_{\mathbb R^3}(f(x)-a)_+\,dx,
 \qquad X\sim f,\quad Y\sim\gamma_{2,s}\text{ independently}.
                                                                    \tag{19}
\]

The cited theorem couples the initial and final sampled density values in
increasing order, proving (2). This two-auxiliary-coordinate transfer is
prior work, also explained after Theorem 1.5 of that paper. If the closure
of a bounded support meets excluded finite endpoints of I, extend A,b,h
continuously there. The inequalities and motion extend too, so the theorem
applies on the compact support. The usual hinge representation gives the
stated convex-energy comparison; no new pressure hierarchy is asserted.

For finite configurations reverse our piecewise-smooth contraction and
apply [Bezdek--Connelly, Theorem 1](https://arxiv.org/pdf/math/0108098v1).
The endpoints are in the same R3 and the motion is in R(3+2), giving both
inequalities in (3), with individual fixed radii.

If distinct input labels have coincident outputs, use
T_epsilon=(1-epsilon)T+epsilon Id. It is still 1-Lipschitz and has the
slice form (1). For a given pair of distinct inputs its output difference
is affine in epsilon and nonzero at epsilon=1, hence vanishes for at most
one epsilon. Choose a sequence decreasing to zero avoiding the finitely
many forbidden values. Apply the theorem to these distinct endpoints and
pass to the limit. The resulting contracting trajectories have distinct
centers throughout because their final distances are positive. Volumes of
finite unions and intersections of fixed-radius balls are continuous in
their centers, by dominated convergence outside the finitely many limiting
sphere boundaries. Repeated input centers can first be merged, keeping the
largest radius for unions and the smallest for intersections. Zero radii
follow by continuity. These observations cover all degeneracies in (3).

## 6. A nonconformal prism example

On K=[-1,1]^2 and I=[-1,1] take

\[
 A(z)=\begin{pmatrix}1/4&z/8\\z/16&1/5\end{pmatrix},\qquad
 b(z)=(z^2/16,z/12),\qquad
 h(z)=\begin{cases}-3z/5&z\leq0,\\4z/5&z\geq0.\end{cases}       \tag{20}
\]

The derivative away from z=0 has rows
(1/4,z/8,(u_2+z)/8), (z/16,1/5,u_1/16+1/12), (0,0,h').
Its squared Frobenius norm is bounded on the entire prism by

\[
 \frac1{16}+\frac1{25}+\frac1{64}+\frac1{256}
       +\frac1{16}+\frac{49}{2304}+\frac{16}{25}
 =\frac{24359}{28800}<1.                                        \tag{21}
\]

Integrating across the two half-prisms proves endpoint contractivity.
A(0) has unequal singular values. Moreover
A(-1)A(1)-A(1)A(-1) has off-diagonal entries 1/80 and -1/160.
The translation curve bends and h folds with unequal one-sided speeds.
Thus (20) illustrates genuinely varying affine slices, beyond the constant
scalar-rotation cylindrical formula in these coordinates. The theorem is
the whole class (1), not this fixture or the coarse sufficient bound (21).
There is also a direct separation from the strong-coordinate class, even
after independent fixed orthogonal changes of source and target frames.
At the two interior points (0,0,-1/2) and (0,0,1/2), write the derivative
Gram matrices as G_- and G_+. Their commutator has entry
(G_-G_+-G_+G_-)_(1,2)=3913/36864000, which is nonzero. A map satisfying
coordinatewise contraction on an open set in fixed endpoint frames has
diagonal derivative in those frames: moving just one source coordinate
cannot change any other target coordinate. Hence all derivative Gram
matrices are simultaneously diagonalizable in one source frame and must
commute, a contradiction. This concerns the whole map on an open prism,
not merely the finite checker grid. No exclusion of compositions of
strong contractions or of every other known positive class is claimed.

## 7. Dependencies and verification boundary

The new geometric step is the horizontal affine completion (7)--(12), which
lets R4's unfolded-speed/Cauchy mechanism handle arbitrary slice matrices
and translations. The cylindrical class A(z)=a Q_(theta(z)), b=0 with
constant a is included in (1); its previously proved R4 ambient bound is
sharper than the R5 bound supplied here. The
[meridian](../gaussian_meridian_contractions/PROOF.md) and
[twisted-meridian](../gaussian_twisted_meridian_contractions/PROOF.md)
classes allow target height to depend on transverse radius and are
complementary; this theorem does not absorb their full scope. The reviewed
[directional normal-bundle theorem](../gaussian_angular_ray_contractions/NORMAL_BUNDLES.md)
is preserved. Its endpoint normal-ray assumption is not made here; the
normality in (10) concerns a constructed auxiliary frame only.

The proof uses standard finite-dimensional ODE existence and handwritten
continuum inequalities. [verify.py](verify.py) checks exact polynomial
identities, rational horizontal jets, a nonsymmetric prism fixture, and
deliberately wrong alternatives. It does not prove ODE existence, replace
the all-pair argument by a finite grid, numerically estimate Gaussian
hinges or ball volumes, or constitute independent review. See
[SOURCES.md](SOURCES.md) for provenance, comparisons with established
contraction classes, and the still-open historical-priority boundary.
