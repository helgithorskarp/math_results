# Transverse matrix paths: an undamped five-dimensional extension

Complete author proof, 26 September 2026; independent mathematical review is
pending. This extends the same cone-reflection packet. The new ingredient is
a path on the boundary of the two-dimensional operator-norm ball, together
with an explicit isometric lift. It gives a uniform geometric criterion for
all laws and ball radii. For circular cones the resulting range is

\[
 pq\le \frac{1}{1+\cos 1}=0.649223\ldots,                 \tag{M1}
\]

where the angle 1 is in radians. The original rigid transverse rotation gave
\(pq\le2/\pi=0.636619\ldots\). The numerical enlargement is modest; the
substantive addition is a matrix-path principle and its exact optimization
over all block-diagonal relative Gram paths in five dimensions. It changes
neither endpoint nor its scale. No optimality among arbitrary five-dimensional
motions, no four-dimensional impossibility, and no full R3 theorem is claimed.

## 1. A uniform support-cost principle

Let P,Q be compact subsets of R2 containing zero. They need not be centrally
symmetric or convex. Put

\[
 C(P)=\{(zu,z):z\ge0,\ u\in P\},\qquad
 D=C(P)\cup(-C(Q)),
\]

and fix the prescribed map T(a)=a on C(P), T(-b)=b on C(Q). The domains meet
only at zero. Let A:[0,1]->R^(2x2) be absolutely continuous, with

\[
 A(0)=-I_2,\quad A(1)=I_2,\quad \|A(t)\|_{\rm op}=1.
                                                               \tag{M2}
\]

Define, almost everywhere,

\[
 k(t)=\max_{u\in P,v\in Q}[-u^T A'(t)v],\qquad
 J=\int_0^1k(t)\,dt.                                          \tag{M3}
\]

The maximum is nonnegative because zero belongs to P,Q. It is measurable
and integrable, bounded by a constant times the norm of A'.

**Theorem M1.** If J<=2, the map T has a continuous contracting motion in
R5, fixing C(P) and moving the other cone isometrically. Consequently, for
every bounded Borel probability law mu on D, every variance s>0 and h>=0,

\[
 \int(\mu*\gamma_{3,s}-h)_+
 \le \int((T_\#\mu)*\gamma_{3,s}-h)_+.                       \tag{M4}
\]

This is full Gaussian majorisation, including every convex internal-energy
comparison for which the energies are defined. If the chosen motion on each
finite restriction is piecewise analytic in time, then, for all finite
prescribed labels x_i in D and arbitrary individual radii R_i>=0,

\[
 |\bigcup_iB(Tx_i,R_i)|\le|\bigcup_iB(x_i,R_i)|,\qquad
 |\bigcap_iB(Tx_i,R_i)|\ge|\bigcap_iB(x_i,R_i)|.              \tag{M5}
\]

**Proof of the motion.** The positive semidefinite matrix
\(I_2-A^TA\) has rank at most one. There is a continuous row vector ell(t)
with

\[
 \ell(t)^T\ell(t)=I_2-A(t)^TA(t),\qquad \ell(0)=\ell(1)=0.    \tag{M6}
\]

Here is the needed continuity argument. On every open interval where the
matrix is nonzero, its one-dimensional image has a continuous unit vector:
choose its sign locally and continue along the interval. Multiply that
vector by the square root of the trace. At any endpoint where the matrix
vanishes its norm tends to zero, irrespective of the sign chosen. Defining
ell=0 on the zero set therefore joins all components continuously. This
argument also covers infinitely many components; it requires no global
choice of a nonvanishing eigenvector at a rank drop.

For J>0 set c(t)=-1+(2/J)integral_0^t k and d(t)=sqrt(1-c(t)^2). For J=0
use c(t)=2t-1 and the same d. Embed the moving cloud by

\[
 F_t(v,z)=(A(t)v,\ c(t)z,\ \ell(t)v,\ d(t)z)\in R^5.       \tag{M7}
\]

Equations (M6) and c^2+d^2=1 prove F_t^T F_t=I_3. Its endpoints are -I_3
and I_3 in the original R3. For a=(z_a u,z_a), b=(z_b v,z_b), the varying
cross inner product with the fixed first cloud is

\[
 z_a z_b\,[u^T A(t)v+c(t)].                                \tag{M8}
\]

Its derivative is nonnegative: u^T A'v>=-k, while c'>=k. Absolute
continuity gives monotonicity, including zero heights. Both within-cloud
distances are constant, so this is the required contraction. In particular
the endpoint map is 1-Lipschitz; that conclusion is not a hidden premise.

For (M4), use the already credited bridge in [PROOF Section 3](PROOF.md):
Aishwarya--Li Theorem 1.4(i)(a) in R5 and two auxiliary Gaussian coordinates
give the R3 hinge identity by exponential density-value sampling. For (M5)
use Bezdek--Connelly Theorem 1 on the finite piecewise analytic R5 motion.
These are established transfer theorems, not new implications of this note.
Compact equal-radius neighborhoods compare at every radius by finite
approximation, or by the original full-support-law argument. QED.

The support cost in (M3) retains the actual sections P,Q. Bounding both by
disks is optional. An orthogonal planar path A=R_theta recovers the original
perimeter criterion exactly, with ell=0. Thus this principle includes the
old noncircular result as well as the new circular construction.

## 2. An explicit path and its lift

Every real linear map of the complex plane has a unique representation

\[
 A\zeta=a\zeta+b\overline\zeta,\qquad
 \|A\|_{\rm op}=|a|+|b|.                                  \tag{M9}
\]

The norm identity follows by choosing the phase of zeta so that the two
summands align; the opposite phase gives the other singular value
\(||a|-|b||\). Differentiation gives \(\|A'\|=|a'|+|b'|\).

Choose a nonzero complex path a=r exp(i theta) inside the closed unit disk,
from -1 to 1, and put b=1-r, real and nonnegative. Then

\[
 A=R_{\theta/2}\begin{pmatrix}1&0\\0&2r-1\end{pmatrix}R_{\theta/2},
 \qquad
 \ell=2\sqrt{r(1-r)}\,(0,1)R_{\theta/2}.                    \tag{M10}
\]

These formulas prove (M2) and (M6) directly; no numerical factorization or
unproved rank-to-motion implication is used. The physical transverse map
may contract a direction and expand it later, while the lifted cloud in R5
remains rigid throughout. Its cost for disks of radii p,q is

\[
 J=pq\int\|A'\|=pq\{\operatorname{length}(a)
                             +\operatorname{Var}(r)\}.     \tag{M11}
\]

For 0<rho<=1, take a to consist of a tangent segment from -1 to the circle
of radius rho, the upper shorter circular arc, and the tangent segment to 1.
The tangent points and cost are

\[
 a_-=(-\rho^2,\rho\sqrt{1-\rho^2}),\quad
 a_+=(\rho^2,\rho\sqrt{1-\rho^2}),
\]
\[
 \Lambda(\rho)=2\sqrt{1-\rho^2}
       +\rho(\pi-2\arccos\rho)+2(1-\rho).                 \tag{M12}
\]

The radius decreases to rho on the first segment, stays constant on the
arc, and increases on the last segment. In particular its total variation
is 2(1-rho). The circular arc is traversed clockwise; theta decreases from
pi to zero across the whole path. Along each piece use c=-1+2 times the
accumulated operator length divided by Lambda(rho). Formula (M7) is now
fully specified, independently of the chosen centers, weights or variance.

On each closed tangent or arc piece the controls are analytic. At the
outer endpoints, 1-r and 1-|c| vanish to finite order; a squared time
parameter removes the one-sided square roots in ell and d. All internal
joins occur with r<1 and |c|<1 when rho<1. Thus the motion is piecewise
analytic, including its endpoints. The rho=1 limit is the old axial path.
Both (M4) and (M5) follow whenever pq Lambda(rho)<=2, including equality.

Differentiation gives

\[
 \Lambda'(\rho)=\pi-2\arccos\rho-2,\qquad
 \Lambda''(\rho)=2/\sqrt{1-\rho^2}>0.                       \tag{M13}
\]

The unique minimum is rho=sin(1), and

\[
 \min_{0\le\rho\le1}\Lambda(\rho)=2(1+\cos1).              \tag{M14}
\]

Equations (M11)--(M14) prove (M1). Endpoints are exactly the original
undamped reflection; this does not use the separate damping theorem.

## 3. Exact boundary for block-diagonal relative Gram paths

The optimization above is not merely over the displayed three-piece curves.

**Lemma M2.** Every rectifiable path A on the operator-norm unit sphere of
real 2-by-2 matrices from -I_2 to I_2 has operator length at least
2(1+cos1). Equality is achieved by (M10) with the preceding choice of a.

**Proof.** Parametrize by arclength and use (M9). The endpoints of a are
-1 and 1, the endpoints of b are zero, and |a|+|b|=1. Put rho=min|a|.
Then Var(b)>=Var(|b|)>=2(1-rho). If rho=0, length(a)>=2 gives total
length at least 4, larger than (M14).

For rho>0, a stays outside the disk of radius rho. Define

\[
 H(r)=\sqrt{r^2-\rho^2}-\rho\arccos(\rho/r).
\]

Each function \(\pm H(r)\pm\rho\theta\) on the angular cover has
Euclidean gradient of norm one, because
\(H'(r)^2+\rho^2/r^2=1\). Split the curve where its radius attains rho.
Apply the signs giving the radial increment H(1) and the absolute angular
increment on each half. The total change of a continuous angle between -1
and 1 is an odd multiple of pi. Therefore

\[
 \operatorname{length}(a)\ge2H(1)+\pi\rho
   =2\sqrt{1-\rho^2}+\rho(\pi-2\arccos\rho).
\]

Adding Var(b) gives Lambda(rho), and (M13)--(M14) prove the bound.
The tangent--arc--tangent curve and b=1-r attain it. The unit-gradient
argument is the same classical obstacle-length calibration used in
[the damped-cone proof, Section 2](../gaussian_damped_cone_reflections/PROOF.md).
It is not a new general obstacle-geodesic theorem. QED.

**Theorem M3.** For full circular cones C_p,C_q, p,q>0, condition (M1)
is necessary and sufficient for a continuous R5 contracting motion whose
relative cross Gram matrix, in the original transverse/axial coordinates,
has the form

\[
 L(t)=\begin{pmatrix}A(t)&0\\0&c(t)\end{pmatrix}.            \tag{M15}
\]

The first cloud may move: if its isometric embedding is G_t and the other
cloud's embedding is F_t, the relative matrix means G_t^T F_t. Translations
are removed at the common origin label. This is a restriction on a motion,
not on all possible proofs of majorisation.

**Necessity.** Within-cloud and origin distances have equal endpoints, so
any contracting motion preserves them at every time. Because each cone
spans R3, the anchored clouds are isometric embeddings G_t,F_t. In R5,

\[
 I_3-L^TL=F_t^T(I-G_tG_t^T)F_t\succeq0,\quad
 \operatorname{rank}(I_3-L^TL)\le2.                        \tag{M16}
\]

For two times t1<t2, monotonicity on all cross pairs gives exactly

\[
 c(t_2)-c(t_1)\ge pq\|A(t_2)-A(t_1)\|_{\rm op}.           \tag{M17}
\]

Thus c is continuous and nondecreasing from -1 to 1, and A is constant
on its level sets. Regarding A as a function of c gives a Lipschitz path
on [-1,1] with length at most 2/(pq). When -1<c<1, (M16) forces at least
one transverse singular value to equal one, and both are at most one.
At c=-1 and c=1, (M17) forces A=-I and I respectively. Hence the entire
reparametrized A lies on the operator-norm unit sphere. Lemma M2 implies
2/(pq)>=2(1+cos1). Sufficiency is (M7)--(M14). QED.

No absolute-continuity assumption on the original motion was needed in this
necessity direction: (M17) supplies the Lipschitz reparametrization. Motions
with nonzero transverse/axial cross blocks remain outside this theorem.
In particular it does not close the remaining general positive frontier.

## 4. Exact finite audit and comparison with the existing packet

A rational member of the new circular range is p=4/5,q=81/100, so
pq=81/125. The optimum involving sin(1) is unnecessary to certify this
member. Use rho=4/5 and its rational tangent points (+/-16/25,12/25).
The alternating cosine Taylor bound gives

\[
 \cos(9/14)\ge1-(9/14)^2/2+(9/14)^4/24-(9/14)^6/720>4/5.
\]

Thus arccos(4/5)>9/14. With the credited elementary pi<22/7 bound,

\[
 \Lambda(4/5)<8/5+(4/5)(22/7-9/7)=108/35,
 \qquad 2-(81/125)(108/35)=2/4375>0.                        \tag{M18}
\]

Conversely pi>25/8 gives (81/125)pi>2, excluding the original circular
rotation budget. This is an exact sign certificate, not a floating search.
For that lower bound, integrate the first 128 terms of the geometric series
for 1/(1+x^2) on [0,1]. Its remainder is x^256/(1+x^2)>=0; the rational
integral, multiplied by four, exceeds 25/8. The checker verifies this sum.

For a finite illustration use the same twelve rational directions D12 of
PROOF equation (20), with these new p,q, and

\[
 X=(0,\{(p d,1):d\in D12\},-\{(q d,1):d\in D12\}),
 \quad Y=(0,\{(p d,1):d\in D12\},\{(q d,1):d\in D12\}).
\]

All 25 target sites are distinct. The product hull has 20 vertices and a
certified perimeter greater than 253379/62500>4. Thus even its finite
sections fail the original perimeter test in the displayed coordinates.
Its all-weight and arbitrary-radius comparisons follow from the same
whole-domain motion, not from a sampled integral or a special weight vector.
The exact checker also checks every contraction pair, paired affine rank
six, and the negative-trace dual certificate of COMPOSITIONS.md. The latter
excludes every finite aligned strong-contraction chain in R3 on this finite
example. Distinct positive weights force the prescribed matching in the
existing common-target framework. No exclusion under every possible choice
of cone axis, no arbitrary rematching result, and no absence of all R4
motions is inferred from these tests.

This extends the existing class rather than adding a new finite toy family.
On the full circular interval 2/pi<pq<=1/(1+cos1), every bounded law,
all weights, all variances and all individual radii are covered without
damping. The original finite-composition theorem already excludes strong
chains for every pq>1/2 on full circular domains. The scalar-defect criterion
also fails on two open cone pieces with these undamped endpoints, and the
paired affine rank is six. Those method comparisons do not imply failure
of the Gaussian inequality. The original per(W)<=4 theorem and all previous
certificates remain valid.

The deformation lemma in ROBUSTNESS.md applies in the same ambient
dimension and therefore also extends these R5 motions under its stated
nonlinear error reserve. No new error radius is optimized here. The Team B
analytic stability, paired-layer and finite-moment criteria are complementary
and are not premises of this motion. They retain their own weight and
variance hypotheses. The geometric endpoint annex explains why unrestricted
weights or a direct ball motion matter for unequal-radius consequences.

The later [ordered-weight orbit theorem](../gaussian_majorisation_square_cone_orbits/ORDERED_WEIGHTS.md)
now meets that geometric-endpoint obligation on the square-cone rays. It
permits unbounded ordered weight ratios, ordered radial measures, and
strictly unequal ordered radii. Its union comparison even holds for every
invariant measure of its finite orthogonal group. The nine-point example
has no R5 motion, so it lies beyond our geometric mechanism. Conversely,
the present theorem imposes no weight ordering and allows arbitrary points
inside the certified cone domains, arbitrary individual radii, and ball
intersections. Neither statement is asserted to contain the other.
The new [fixed-atom reduction](../gaussian_majorisation_global_criterion/ANCHOR_REDUCTION.md)
is a reduction of the full question to a dominant fixed atom with an
arbitrary rare packet. Its rare packet is not assumed to lie in our cone
class, and the reduction is not a premise of the present positive theorem.

The additional Kneser--Poulsen input is the explicit R5 motion on these
undamped domains. Bezdek--Connelly's implication is credited. Targeted
primary-source searches did not locate this matrix-path criterion or this
cone consequence; this is not an exhaustive historical-priority assertion.
The known all-positive-order Renyi comparisons are not used as a substitute
for full majorisation.

Run `python3 matrix_path_audit.py --check` and the `python3 -O` variant.
The standard-library checker verifies exact lift identities, a second
direct real-matrix representation, rational Taylor and perimeter budgets,
all finite fixture pairs, rank and dual certificates, and invalid controls.
Its compact deterministic output is EXPECTED_MATRIX_PATHS.json. The
universal path, length lower bound, and external Gaussian/ball bridges are
written mathematics, not consequences of the finite checks. No solver,
floating sign, large artifact, or formalization is a premise. All checks
remain author work, with independent review pending.
