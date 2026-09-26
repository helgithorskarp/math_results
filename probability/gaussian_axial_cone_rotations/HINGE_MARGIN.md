# A quantitative hinge margin for the existing motion class

Complete author proof, 26 September 2026; independent review and
formalization are pending. This strengthens the effectiveness of the
existing axial, nonlinear-reserve and matrix-path package. It adds no
geometric subclass and no Kneser--Poulsen volume claim. The unrestricted
three-dimensional conjecture remains open.

The starting identity is **prior work**: the pressure representation in
[Aishwarya--Li, equation (66)](https://arxiv.org/html/2609.07041v2).
The contribution here is a uniform geometric lower bound for that
representation, followed by its explicit conversion to the actual
three-dimensional hinge gap. In particular, we use neither a regular-value
assumption nor differentiability or bounded variation of the trajectories.
No historical priority for quantitative strictness is asserted.

Section 7 completes the quantitative estimate through every threshold
below a certified **target** peak. It retains the same motion hypothesis
and uses a terminal part of its squared-distance loss. The earlier
source-peak bound remains valid and can be stronger when it applies.

## 1. Statement and usable inputs

Let mu be a probability measure with compact support K in R3, and suppose
there is a continuous contracting motion

    F_t : K -> R5,  0<=t<=1,
    F_0(x)=(x,0,0),  F_1(x)=(Tx,0,0).

Thus each trajectory is continuous and every pair distance is
nonincreasing. Motions in fewer dimensions may be padded with zeros.
Joint continuity follows from the common spatial Lipschitz bound and
compactness of K. Choose x_* in K and any

    R >= sup_{x in K} |x-x_*|.

An anchor outside K is also allowed when the same contracting motion is
defined on K together with the anchor. Translating by F_t(x_*) keeps all
centers in B_R and changes neither endpoint hinges nor pair-distance loss.
In particular R=diam(K) always works without inspecting the path.

For s>0 put

    C_3=(2 pi s)^(-3/2),
    f=mu*gamma_(3,s),  g=(T#mu)*gamma_(3,s),
    H(f,h)=integral (f-h)_+,
    D=E[|X-X'|^2-|TX-TX'|^2],  X,X' iid mu.

Let m be any certified lower bound on the source peak:

    0<m<=||f||_infinity.

One density evaluation m=f(z) suffices. The elementary bound
m=C_3 exp(-R^2/(2s)) also works, by evaluating at the source anchor.
For 0<h<m define the dimensionless positive number

$$
\kappa(R,s,m,h)=
\frac{e^{5/2}}{96\sqrt{2\pi}}
\left(\frac{m-h}{C_3}\right)^4
\exp\!\left[-\left(
\frac{2R}{\sqrt s}+\sqrt{2\log\frac{2C_3}{h}}
\right)^2\right].
\tag{1}
$$

The expression (1) is defined for all 0<h<m<=C_3; the source-peak
restriction is a hypothesis of the first bound (2).

**Theorem H.** Under these hypotheses,

$$
H(g,h)-H(f,h)\ \ge\ \kappa(R,s,m,h)\frac{D}{s}.
\tag{2}
$$

The estimate is uniform over atom counts, weights, nonatomic laws and
all eligible paths having these endpoint data and radius bound. Its
constant is deliberately conservative. It may be very small at small
variance, near h=0, or near the certified peak m; it is not an efficient
bound in every regime.

If D>0, the actual hinge gap is strictly positive at every
0<h<||f||_infinity: choose m between h and the source peak. It is
also strictly positive when ||f||_infinity<=h<||g||_infinity, because
then the source hinge is zero and the target hinge is positive. If D=0,
T preserves every distance on K and the endpoint laws are related by a
Euclidean isometry, so all their hinges agree. This gives a strictness
alternative **within the motion class**. The explicit formula (2) only
applies below the certified source peak; both hinges vanish at/above
the target peak, and they agree at h=0.

**Theorem H2 (target-peak completion).** Keep the same hypotheses on mu,
T, the motion, R and s. Let 0<M<=||g||_infinity and 0<h<M. Then

$$
\begin{split}
H(g,h)-H(f,h)\ \ge\ &
\kappa\!\left(R,s,\frac{M+h}{2},h\right)\\
&\times\min\left\{\frac D s,
       4e^{-R^2/s}\log\frac{2M}{M+h}\right\}.
\end{split}
\tag{14}
$$

Here kappa is exactly the function (1). In particular, (14) gives an
explicit strictly positive bound at every 0<h<||g||_infinity when D>0,
by choosing M between h and the target peak. A target density evaluation
also supplies a usable M. This removes the source-peak restriction of
(2), without asserting that (14) dominates (2) where both apply. The
proof is in Section 7; it does not apply Theorem H to an intermediate
configuration that might fail to lie in R3.

## 2. Extending the established pressure identity

Work temporarily in R5 after the moving translation. Write

    C_5=(2 pi s)^(-5/2),
    f_t(z)=E gamma_(5,s)(z-F_t(X)),
    nu_(x,y)=d[-|F_t(x)-F_t(y)|^2].

The last expression is a positive Lebesgue--Stieltjes measure on (0,1];
its total mass is the endpoint squared-distance loss. Translation of
the paths leaves these measures unchanged.

For Q in C1([0,C_5]), equation (66) gives

$$
\begin{split}
\int f_1Q(f_1)-\int f_0Q(f_0)
=\frac1{4s}\mathbb E_{X,X'}\int_{(0,1]}
\int_{\mathbb R^5}Q'(f_t(z))\,
\gamma_{5,s}(z-F_t(X))\gamma_{5,s}(z-F_t(X'))
\,dz\,d\nu_{X,X'}(t).
\end{split}
\tag{3}
$$

Here is the precise extension beyond the polynomial statement in that
source. Uniformly approximate Q' on [0,C_5] by polynomials p_j, and
integrate them from zero with the constant Q(0). This approximates Q
in C1. Apply the source identity to U_j(r)=r Q_j(r), whose pressure is
r^2 Q_j'(r). Endpoint integrals converge uniformly under the probability
densities. The absolute error on the right is at most

    ||Q_j'-Q'||_infinity D C_5 / (4s 2^(5/2)),

because the integral of a product of two Gaussian kernels is at most
C_5/2^(5/2). Hence (3) follows. Only finite D and continuity of the
contracting motion are used; a velocity field is unnecessary.

We also need a uniform peak bound. The Gaussian product formula, obtained
by completing the square, is

$$
\int f_t^k
=C_5^{k-1}k^{-5/2}
\mathbb E\exp\!\left[-\frac1{2ks}
\sum_{i<j}|F_t(X_i)-F_t(X_j)|^2\right]
\quad(k\ge2).
\tag{4}
$$

All its summands decrease under the motion, so these moments are
nondecreasing. Taking k-th roots and then k to infinity gives

    ||f_t||_infinity >= ||f_0||_infinity >= C_2 m,
    C_2=(2 pi s)^(-1).

This use of integer moments proves only a peak bound. The hinge estimate
will come from (3), not from cancellation of moment inequalities.

## 3. A radial shell estimate with no regular-level assumption

Set

    a=C_2 h,
    L=C_5/sqrt(e s),
    r_0=C_2(m-h)/(2L),
    q=sqrt(2s log(2C_5/a)),
    B=R+q.

The Gaussian gradient bound gives |grad f_t|<=L globally. Each f_t
attains its maximum at some z_t in B_R: at a stationary point its location
is a positive weighted barycenter of the kernel centers. Thus

    f_t(z)>=a+C_2(m-h)/2  if |z-z_t|<=r_0.                 (5)

On the sphere |z|=B, every center is at least q away, so f_t(z)<=a/2.
Consequently the inner ball in (5) lies strictly inside B_B(0).

Choose 0<epsilon<C_2(m-h)/2 and a smooth nondecreasing Q_epsilon
that is zero on [0,a], one on [a+epsilon,C_5], and whose derivative
is supported in (a,a+epsilon). Its derivative integrates to one.

For each omega in S4, follow the ray z_t+r omega from r=r_0 to its
unique exit r=b(omega) from B_B(0). The endpoint values of
Q_epsilon(f_t) are one and zero. The fundamental theorem of calculus
and the gradient bound imply

$$
1\le L\int_{r_0}^{b(\omega)}
Q_\epsilon'(f_t(z_t+r\omega))\,dr.
\tag{6}
$$

This remains valid when the ray crosses a level repeatedly. Radial
integration, r^4>=r_0^4 and |S4|=8 pi^2/3 give

$$
\int_{B_B(0)}Q_\epsilon'(f_t(z))\,dz
\ge\frac{|S^4|r_0^4}{L}.
\tag{7}
$$

For every two centers in B_R and every z in B_B(0), their kernel
product is at least

    C_5^2 exp(-(2R+q)^2/s).

Since Q_epsilon' is nonnegative, (7) supplies the following bound for
the inner integral in (3), uniformly in t, X and X':

$$
\int Q_\epsilon'(f_t)\gamma_{5,s}(z-F_t(X))
                 \gamma_{5,s}(z-F_t(X'))\,dz
\ge \frac{|S^4|r_0^4 C_5^2}{L}
       e^{-(2R+q)^2/s}.
\tag{8}
$$

No choice of z_t measurable in t is needed: (8) bounds the original
measurable integral by the same scalar for each t. No coarea formula,
regular threshold or smoothness of t -> F_t enters this argument.

## 4. Return to the actual three-dimensional hinge

Insert (8) into (3) and use E nu_(X,X')((0,1])=D. Let epsilon decrease
to zero. Dominated convergence applies to each endpoint probability
integral, and the one-sided step convention gives

$$
\int f_1\mathbf1_{f_1>a}-\int f_0\mathbf1_{f_0>a}
\ge\frac{|S^4|r_0^4 C_5^2}{4s L}
       e^{-(2R+q)^2/s}D.
\tag{9}
$$

This limit does not require any assertion about the measure of a critical
level set. At the endpoints, up to translations, f_i is the product
of its R3 density and gamma_(2,s). For Y with density gamma_(2,s),
gamma_(2,s)(Y)/C_2 is uniform on (0,1). Independence therefore gives

    integral (f tensor gamma_(2,s))
                 1_{f tensor gamma_(2,s)>C_2 h}
      = integral f(x)(1-h/f(x))_+ dx = H(f,h).             (10)

Apply this identity at both endpoints. Finally

    r_0=(sqrt(e s)/2)((m-h)/C_3),
    q=sqrt(2s log(2C_3/h)),
    |S4| e^(5/2)/(64(2 pi)^(5/2))=e^(5/2)/(96 sqrt(2 pi)).

Substitution in (9) proves (1)--(2).

For the stated equality alternative, the nonnegative continuous loss
function on K x K has integral zero exactly when it vanishes everywhere,
because K is the support of mu. Preservation of all distances identifies
a rigid map on the affine span: choose an affine basis in K, match its
Gram matrix, and use distances to that basis to identify every other
point. Extend this isometry to R3. Gaussian convolution and hinges are
invariant under the resulting rigid motion.

## 5. Internal energy and the original benchmark

The already known second-energy defect

    E_2=integral g^2-integral f^2

satisfies

$$
0\le E_2\le (4\pi s)^{-3/2}\frac{D}{4s}.
\tag{11}
$$

Indeed the two-kernel formula expresses E_2 as (4 pi s)^(-3/2)
times the expectation of exp(-d_1^2/(4s))-exp(-d_0^2/(4s));
use 1-exp(-u)<=u and d_1<=d_0. Combining (11) with (2) gives

$$
H(g,h)-H(f,h)\ge
4\kappa(R,s,m,h)(4\pi s)^{3/2}E_2.
\tag{12}
$$

Thus the motion hypothesis converts an elementary positive energy
defect into a margin for the actual hinge. A positive E_2 alone does
not establish (12) for an arbitrary contraction. For any compact
threshold interval [h_-,h_+] contained in (0,m), the minimum of
kappa on that interval is positive, giving a uniform margin there.

For the original 25-point fixture in [PROOF.md](PROOF.md), assign every
point weight 1/25 and keep the original undamped target. Its twelve
directions sum to zero, and its two nonzero height-one clouds have
p=3/4 and q=4/5. The origin is a fixed anchor, and exact inputs are

$$
R=\frac{\sqrt{41}}5,\qquad D=\frac{1152}{625},\qquad
m_s=C_3\frac{1+12e^{-25/(32s)}+12e^{-41/(50s)}}{25}.
\tag{13}
$$

The within-cloud and anchor losses vanish. The ordered cross-cloud
contributions give D=8(12/25)^2, and m_s is exactly the density at
the origin. Equations (1)--(2) now give a positive analytic certificate
for every s>0 and 0<h<m_s, with no hinge quadrature or high-degree
polynomial certificate. The general theorem applies to all weights;
equal weights are used only to make this benchmark substitution short.

## 6. Dependency and ownership boundary

- [A](PROOF.md), [R](ROBUSTNESS.md) and [M](MATRIX_PATHS.md)
  supply eligible motions. Apply H directly, with the actual perturbed
  endpoints in R. G's finite smoothing theorem, C's composition
  obstruction and the cap comparison are not premises of this estimate.
- The pressure identity and the two-coordinate conversion are credited
  to Aishwarya--Li. The additional ingredient is the uniform radial
  estimate (8), with the explicit constant and threshold limit above.
- The team's [common-set stability theorem](../gaussian_common_set_stability/PROOF.md)
  bounds a reference-test gap and retains a source-test error when
  comparing actual profiles. Here (2) bounds the actual hinge directly,
  under the additional low-dimensional-motion hypothesis. Neither result
  removes the other's hypothesis or proves the unrestricted sign.
- R4 retains ownership of new extremal maps and deformation constructions.
  This estimate consumes their possible R5 motion certificates; it does
  not construct or classify them. R2 may use (13) as a positive benchmark
  independent of its general finite-atomic certificate recipe. R8 may
  compare (12) with reference-margin estimates while retaining this
  geometric premise.
- No strict ball-volume inequality, new Kneser--Poulsen class, improved
  axial/matrix threshold, or extension beyond R5 motions follows here.

Verification is the written proof, including the C1 approximation,
radial estimate, endpoint sampling identity and exact substitution (13).
No new computational theorem or unreported numerical certificate is
used. The original core proof and checker files are unchanged.

## 7. Control the peak by the remaining pair loss

The [earlier entropy-rigidity source, Theorems B/C and Section 5](../gaussian_contraction_rigidity/PROOF.md)
already proves the posterior **lower** peak estimate, including the sharp
posterior coefficient 1/(4s) and a bounded-support lower bound in terms
of D. These are not new claims here. We use the following elementary
upper companion, with the posterior taken at a target mode.

### 7.1 Upper peak increment

Let U,V be bounded vectors on the same probability space, in R^n, with
|V-V'|<=|U-U'| for independent copies. Suppose V lies in a ball of radius
R. Let F and G be the respective Gaussian density maxima at variance s,
and put Delta=|U-U'|^2-|V-V'|^2 and d=E Delta. Then

$$
\log(G/F)\le \frac{e^{R^2/s}}{4s}\,d.
\tag{15}
$$

To prove it, write C_n=(2 pi s)^(-n/2), choose a target mode y, and
put d nu=gamma_(n,s)(y-V)dP/G on the common label space. The mode
equation gives E_nu V=y. Set x=E_nu U. The kernel ratio and Jensen give

$$
\frac{f_U(x)}{G}
=\mathbb E_\nu\exp\!\left[
       \frac{|y-V|^2-|x-U|^2}{2s}\right]
\ge \exp\!\left[-\frac{\mathbb E_{\nu\otimes\nu}\Delta}{4s}\right].
\tag{16}
$$

The variances in (16) are traces. Since F>=f_U(x), this bounds
log(G/F) by the posterior pair loss divided by 4s. Evaluation at the
center of the radius-R ball gives G>=C_n exp(-R^2/(2s)); hence
d nu/dP<=C_n/G<=exp(R^2/(2s)). Nonnegativity of Delta now proves
(15). The proof works on labels even when some intermediate centers
coincide. It requires no inverse of U or V and no velocity field.

### 7.2 Select a terminal interval

Return to the R5 motion, translated by the anchor, and write P_t=max f_t
for its lifted density peak. Define its remaining average pair loss

$$
d(t)=\mathbb E\big[
 |F_t(X)-F_t(X')|^2-|F_1(X)-F_1(X')|^2\big].
\tag{17}
$$

This is continuous and nonincreasing, with d(0)=D and d(1)=0.
Boundedness and continuity of the pair distances justify the expectation
and its continuity. Set

$$
\ell=\min\left\{D,
4s e^{-R^2/s}\log\frac{2M}{M+h}\right\}.
\tag{18}
$$

If D=0, (14) is the already proved equality case. Otherwise ell>0;
choose t_* with d(t_*)=ell, taking t_*=0 if ell=D. Apply (15) to
the coupled configurations at t and 1. For every t>=t_*,

$$
P_t\ge P_1\exp[-e^{R^2/s}d(t)/(4s)]
\ge C_2\frac{M+h}{2},\qquad C_2=(2\pi s)^{-1}.
\tag{19}
$$

The last inequality uses P_1=C_2||g||_infinity>=C_2 M and
(18). Thus the radial estimate (8), with m=(M+h)/2, holds throughout
this terminal interval.

For every smooth increasing step Q_epsilon used in Sections 3--4,
the integrand of (3) is nonnegative over the **entire** motion. Retain
only times in (t_*,1]. Their expected Stieltjes mass is d(t_*)=ell.
Consequently the right side of (9) has D replaced by ell and
m replaced by (M+h)/2. Take the same one-sided threshold limit and
use the product identity (10) at the two original endpoints. This proves
(14). No product decomposition at t_* is assumed: the intermediate
configuration may span all five dimensions. Continuity of pair distances
also excludes a time atom at t_*, so the interval convention causes no loss.

### 7.3 Concrete meaning and scope

For the original equally weighted 25-point benchmark, one additional
target density evaluation is

$$
M_s=g(0,0,1)
=\frac{C_3}{25}\left[
 e^{-1/(2s)}+12e^{-9/(32s)}+12e^{-8/(25s)}\right].
\tag{20}
$$

Together with R and D from (13), this supplies all inputs to (14).
It is a lower bound on the target peak, not a claimed exact mode or an
upper bound on the source peak. One may take the maximum of this value
and the target density at zero, which equals the earlier m_s.

The additional threshold range is real, rather than a change of
notation. For the already known two-point control with equal atoms at
+/-a e_1, 0<a<=sqrt(s), collapsed to zero, the source peak is
C_3 exp(-a^2/(2s)) and the target peak is C_3. Taking M=C_3 in (14)
covers thresholds between these peaks, where (2) has no admissible m.
The mode computation is the same cosh/tanh calculation in the earlier
entropy-rigidity source. This is a sanity control, not a new map family.

The improvement is confined to quantitative effectiveness of the existing
motion theorem. An arbitrary contraction obeys the peak estimate (15),
but that does not supply a positive Stieltjes pressure representation in
R5. Such a representation is still the geometric premise of (14).
Critical levels, zero weights and diffuse laws are included. No new
Kneser--Poulsen statement, endpoint deformation or optimal constant is
claimed. The original source-peak theorem and its proof are unchanged.
