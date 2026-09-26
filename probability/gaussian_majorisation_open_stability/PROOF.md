# Fixed-variance all-order stability beyond the exact square-cone rays

Author proof with an exact finite strictness certificate, 26 September 2026.
Independent mathematical review and formalization are pending. The general
three-dimensional conjecture remains open. The spatial perturbation radius
below is uniform on each compact positive variance interval, not asserted
uniform down to zero or up to infinity.

## 1. A spatially robust positive class

Use the nine sites and their order from the preceding
[orbit theorem](../gaussian_majorisation_square_cone_orbits/PROOF.md):

\[
\begin{split}
 A&=((1,0,1),(0,1,1),(-1,0,1),(0,-1,1)),\\
 B&=((1,1,1),(-1,1,1),(-1,-1,1),(1,-1,1)),\\
 X&=(0,A,-B),\quad Y=(0,A,B),\\
 p^*&=(8,12,7,15,44,21,11,23,43)/184.
\end{split}                                                     \tag{1}
\]

Write \(H_f(a)=\int_{\mathbb R^3}(f-a)_+\) and let \(\gamma_s\)
have covariance \(sI_3\).

**Theorem 1 (arbitrary small spatial clouds).** For every compact interval
\(I\subset(0,\infty)\), there exists \(\epsilon_I>0\) such that the
following holds simultaneously for every probability vector
\(\|p-p^*\|_1\le1/4000\). Let \(\alpha_i,\beta_i\) be arbitrary Borel
probability laws supported in \(B(X_i,\epsilon_I)\) and
\(B(Y_i,\epsilon_I)\), respectively. Set

\[
                 \mu'=\sum_{i=0}^8p_i\alpha_i,
        \qquad   \nu'=\sum_{i=0}^8p_i\beta_i.                   \tag{2}
\]

Then, for every \(s\in I\) and every \(a>0\),

\[
                 H_{\mu'*\gamma_s}(a)
                    \le H_{\nu'*\gamma_s}(a).                 \tag{3}
\]

The cloud laws may be atomic or nonatomic and are independent. No assumed
map between them is needed for this stronger density comparison. In
particular, (3) holds for every genuine contraction pair in this class.
Section 7 constructs such pairs with solid three-dimensional support.
The weight ball is the entire previously reviewed asymmetric obstruction
family; the new conclusion concerns arbitrary spatial clouds, not a larger
weight-radius constant on the old rays.

Two analytic principles prove the result: a positive geometric estimate for
all sufficiently low thresholds, and openness of strict Gaussian hinge
comparisons. A new finite certificate supplies the needed strictness for
(1). The geometric estimate uses a positive cluster-mass floor and a
strict mean-support gap. It does not revive the closed uniform
vanishing-deficit tail-error route.

## 2. Low thresholds with a positive geometric margin

Use normalized sphere measure \(\sigma\), and set
\(h_X(\theta)=\max_i\theta\cdot X_i\),
\(\overline h_X=\int h_X\,d\sigma\). This is half the usual mean
width, with translations integrating to zero.

Consider finite base supports \(X,Y\), with positive weights at least
\(m>0\) at each site, and clouds of radius at most \(\epsilon\) about
the sites. The two numbers of sites and their weights may differ in this
section, but each law has mass one. Assume \(|X_i|+\epsilon\le R,|Y_j|+\epsilon\le R\) for every
base site, \(0<s\le S\), and

\[
 \overline h_X-\overline h_Y-2\epsilon\ge\delta>0.             \tag{4}
\]

Define

\[
 C_s=(2\pi s)^{-3/2},\quad
 K=R^2+2S\log(1/m),\quad B_0=K+5R^2,\quad Q=4B_0/\delta.
                                                                  \tag{5}
\]

**Lemma 2 (a uniform low-threshold comparison).** For the cloud densities
\(f_s,g_s\), whenever \(0<a\le C_s e^{-Q^2/(2s)}\),

\[
 H_{g_s}(a)-H_{f_s}(a)
       \ge4\pi\delta s a\,[\log(C_s/a)+1]>0.                 \tag{6}
\]

**Proof.** Put \(a=C_s e^{-q^2/(2s)}\). Along a ray \(r\theta\),
the moment-generating factor of the first cloud law satisfies

\[
 m e^{r(h_X(\theta)-\epsilon)/s-R^2/(2s)}
 \le \mathbb E e^{r\theta\cdot Z/s-|Z|^2/(2s)}
 \le e^{r(h_X(\theta)+\epsilon)/s}.                           \tag{7}
\]

For the lower bound take the entire cloud attached to a maximizing base
site. This is why small atom masses inside a nonatomic cloud cause no
problem: its total assigned cluster mass is at least \(m\).

For \(q\ge4R\), the ball \(B(0,R)\) lies inside the density superlevel
set. Outside that ball the density strictly decreases along each ray,
since its radial logarithmic derivative is at most \((-r+R)/s<0\).
Thus its superlevel set has one radial boundary \(r_X(\theta)\).
For \(q^2\ge2K\), solving the quadratic bounds in (7) gives

\[
 q+h_X(\theta)-\epsilon-K/q
 \le r_X(\theta)
 \le q+h_X(\theta)+\epsilon+K/q.                            \tag{8}
\]

Indeed the exact lower root uses
\(h_X-\epsilon+\sqrt{q^2+(h_X-\epsilon)^2-K}\); the upper root uses
\(h_X+\epsilon+\sqrt{q^2+(h_X+\epsilon)^2}\).
Their difference from \(q+h_X\mp\epsilon\) has absolute value at most
\(K/q\). Both roots are outside \(R\) under the displayed bounds.

If also \(q\ge K/R\), then for \(|h|\le R\), \(|e|\le K/q\),

\[
 |(q+h+e)^3-q^3-3q^2h|
 \le3Kq+12R^2q+8R^3
 \le3(K+5R^2)q.                                              \tag{9}
\]

The last inequality uses \(q\ge4R\). Integrating radial cubes and
dividing by three yields the volume estimate

\[
 \left|V_{f_s}(a)-\frac{4\pi}{3}q^3
                     -4\pi q^2\overline h_X\right|
 \le4\pi\epsilon q^2+4\pi B_0q,                             \tag{10}
\]

where \(V_f(a)=|\{f>a\}|\). The identical estimate holds for the
other support. As \(\delta\le2R\) and \(K\ge R^2\), the choice
\(q\ge Q\) implies all preceding lower bounds on \(q\). Consequently

\[
              V_{f_s}(a)-V_{g_s}(a)\ge2\pi\delta q^2.        \tag{11}
\]

Finally, the exact layer-cake identity is
\(H_f(a)=1-\int_0^a V_f(t)\,dt\). For all \(t\le a\),
\(q_s(t)\ge Q\), so integrating (11) proves (6). The integral of
\(\log(C_s/t)\) is \(a[\log(C_s/a)+1]\). All these integrals are
finite. No asymptotic remainder or unvalidated quadrature is used. \(\square\)

In particular, for fixed finite positive atomic laws,

\[
 V_{f_s}(a)-V_{g_s}(a)
 =4\pi q_s(a)^2(\overline h_X-\overline h_Y)+O(q_s(a))
 \quad(a\downarrow0).                                       \tag{12}
\]

Thus a full Gaussian majorisation at one variance implies
\(\overline h_X\ge\overline h_Y\): a negative difference would make
both the low-threshold volume difference and its layer-cake integral
negative. This necessary condition will be useful below.

## 3. Openness of a strict all-order comparison

**Theorem 3 (fixed-variance stability).** Let \(\mu,\nu\) be finite
atomic probability laws with positive weights, and fix \(s_0>0\).
Write \(f=\mu*\gamma_{s_0},g=\nu*\gamma_{s_0}\), and suppose

\[
\begin{split}
 &\overline h_{\operatorname{supp}\mu}
             >\overline h_{\operatorname{supp}\nu},\\
 &\|f\|_\infty<\|g\|_\infty,\\
 &H_g(a)>H_f(a)\quad(0<a<\|g\|_\infty).
\end{split}                                                   \tag{13}
\]

Then full majorisation persists if the Gaussian variance is sufficiently
close to \(s_0\), the finitely many weights are sufficiently close to
their original positive values, and each atom is replaced by an arbitrary
probability cloud in a sufficiently small ball about it. The two endpoint
laws may be perturbed independently. For a compact family of base parameters with fixed finite numbers of sites
and positive weights satisfying (13), the allowed perturbations can be
chosen uniformly.

**Proof.** Restrict the variance first to
\([s_0/2,2s_0]\), all sites and clouds to a fixed ball, and all assigned
cluster weights to a common positive lower bound. Choose the cloud radius
so that the mean-support gap loses at most half its original value.
Lemma 2 then gives a common positive lower threshold \(a_-\) below
which all comparisons hold. The minimum of
\(C_s e^{-Q^2/(2s)}\) over this compact variance interval is positive.
Decrease \(a_-\) if necessary so that it is below
\(b=(\|f\|_\infty+\|g\|_\infty)/2\).

By (13) and continuity, the gap has a positive minimum on
\([a_-,b]\). Gaussian smoothing is continuous in both \(L^1\) and
\(L^\infty\) under the stated perturbations. For example, at a common
variance \(s\), replacing each atom by an \(\epsilon\)-cloud costs at
most \(\epsilon/\sqrt{s}\) in \(L^1\), because
\(\|\partial_e\gamma_s\|_1\le1/\sqrt{s}\). Its \(L^\infty\)
cost is at most \(C_s\epsilon/\sqrt{s}\). Changing weights costs
at most their \(L^1\) difference in density \(L^1\), and at most
\(C_s\) times that difference in density \(L^\infty\). Gaussian
kernels are continuous in both norms as \(s\) varies away from zero.
These bounds are uniform over every choice of cloud laws.

Since \(|H_f(a)-H_{f'}(a)|\le\|f-f'\|_1\), small perturbations
preserve the middle gap. Make them small enough also that the perturbed
source peak stays below \(b\). Above \(b\) its hinge is zero, so
comparison is automatic. The low, middle, and high threshold ranges
cover all \(a>0\).

This supplies open neighborhoods of every base parameter satisfying
(13). A finite subcover proves the compact-family assertion, retaining
uniform positive weight floors and radius bounds. The proof gives a
positive radius but does not compute an optimized numerical radius.
The middle minimum is positive by the proved strictness, not assumed from
a finite sampling of hinges. \(\square\)

Equivalently, with fixed weights, the neighborhoods can be described by
small \(W_\infty\) transport distance from each atomic endpoint. This
strong support-sensitive topology is part of the theorem. No assertion
is made for unrestricted weak or total-variation neighborhoods, which can
insert tiny distant components.

## 4. A unifying regularization of the existing positive classes

**Corollary 4 (arbitrarily small target damping).** Suppose finite positive
atomic laws satisfy
\(\mu*\gamma_{s_0}\prec\nu*\gamma_{s_0}\), and \(\nu\) is not a
point mass. For every \(0<c<1\), the pair
\((\mu,(c\,\mathrm{id})_\#\nu)\) satisfies (13), so Theorem 3
applies to it. Consequently any existing finite all-order comparison at
one variance supplies an open family of all-order comparisons near that
variance after an arbitrarily small strict target homothety. This includes
the finite instances of the team's motion, scalar-defect, common-target,
and density-orbit classes.

Here are the details, including strictness. Let
\(g_t=\operatorname{law}(e^{-t}Y+Z_s)\), with \(Y\sim\nu\) and
\(Z_s\) an independent centered Gaussian. The induced velocity is

\[
 v_t(x)=-\mathbb E[e^{-t}Y\mid e^{-t}Y+Z_s=x],\qquad
 Dv_t(x)=-s^{-1}\operatorname{Cov}(e^{-t}Y\mid x).              \tag{14}
\]

Direct differentiation gives
\(\partial_tg_t+\operatorname{div}(g_tv_t)=0\).
All posterior atomic weights are positive, so the trace covariance is
strictly positive everywhere when \(\nu\) is not a point mass.
The bounded smooth velocity has a global flow; along it,

\[
                  \frac{d}{dt}g_t(x_t)
                     =-g_t(x_t)\operatorname{div}v_t(x_t)>0.
                                                                  \tag{15}
\]

Following a starting maximizer proves strict increase of the peak at
every positive time. The exact hinge identity along this flow is

\[
 H_{g_T}(a)-H_{g_0}(a)
   =\frac a s\int_0^T\int_{\{g_t>a\}}
                \operatorname{tr}\operatorname{Cov}(e^{-t}Y\mid x)
                     \,dx\,dt.                               \tag{16}
\]

One may justify (16) with smooth convex hinge approximations in the
continuity equation. Their pressure converges to
\(a\mathbf1_{\{g_t>a\}}\). Positive-level superlevel sets are bounded;
Gaussian mixture analyticity makes each positive level set have Lebesgue
measure zero; dominated convergence on compact time intervals then applies.
This also avoids assuming a regular level boundary. If
\(0<a<\|g_T\|_\infty\), the integrand is positive on a positive
space-time measure set near the final time. Thus (16) is strictly positive.
Taking \(T=-\log c\), composition with the assumed majorisation gives
both the last two conditions of (13). Peak order for the assumed pair
follows already from its hinge order.

By (12) the assumed comparison gives
\(\overline h_X\ge\overline h_Y\). Homothety sends the latter
quantity to \(c\overline h_Y\), and
\(\overline h_Y>0\) for a nonpoint finite support. Hence the first
condition of (13) is strict too.

Homothetic Gaussian monotonicity itself is an established continuous-
contraction phenomenon. The purpose here is its strictness and its use
as a common fixed-variance stability bridge; no novelty claim is made for
that monotonicity alone. A point-mass target is excluded from this
corollary, not from the main spatial-cloud theorem.

## 5. Strict density-orbit maxima for the undamped square-cone family

For (1), no target damping is needed. This section supplies a new exact
strictness certificate, while relying on the preceding orbit theorem for
the nonnegative hinge comparison.

Use exactly the 48 signed-permutation labels in that theorem:
\((gx)_i=\epsilon_i x_{\pi_i}\), lexicographically ordered permutations
then signs. Negation changes label \(i\) to \(i\operatorname{xor}7\).
On the chamber \(x_1\ge x_2\ge x_3\ge0\), set
\(e^{x_1}=uvw,e^{x_2}=vw,e^{x_3}=w\). For
\(F_C^q(x)=\sum q_i e^{C_i\cdot x}\), put

\[
 P_{C,g}^q(U,V,W)=uv^2w^3F_C^q(gx),\quad
 u=1+U,\ v=1+V,\ w=1+W.                                    \tag{17}
\]

The individual-center monomial, with \(e=g^TC_i\), has exponents
\((1+e_1,2+e_1+e_2,3+\sum e_i)\). Thus it has the same 105 coefficient
positions used previously.

**Finite strictness lemma.** For each label \(i\), the following list
specifies one label \(j_i\):

```text
17 17 21 21  1  1  1  1 29 25 29 25  9  9  9  9
17 17 21 21 17 17 17 17 29 25 29 25 25 25 25 25
25 33 37 25 25 33 33 25 25 41 45 25 25 41 41 25
```

Every coefficient form \(d\) of
\(P_{A,j_i}-P_{A,i}\) and \(P_{B,j_i}-P_{B,-i}\) is either zero
as a four-variable linear form, or satisfies

\[
 \frac{d\cdot a^*}{184\|d\|_\infty}\ge1/552
 \quad\hbox{or}\quad
 \frac{d\cdot b^*}{184\|d\|_\infty}\ge1/552,                 \tag{18}
\]

respectively, where \(a^*=(12,7,15,44),b^*=(21,11,23,43)\).
For each of the three linear monomials \(U,V,W\), at least one of
these two polynomial differences has a nonzero coefficient form.

[verify.py](verify.py) checks all these forms, not samples of \(x\).
It uses both binomial expansion and repeated polynomial multiplication,
and compares every individual-center coefficient. It imports no earlier
code or order matrices. [STRICT_TARGETS.json](STRICT_TARGETS.json) contains
only the displayed 48 labels. The invalid constant assignment is rejected.
The preceding all-upper-set correlation theorem remains a separate,
explicitly cited dependency; maximum comparison alone would not prove
majorisation.

Put \(r_w=1/4000\) and \(\kappa=1/552-r_w>0\).
For every weight vector in Theorem 1, (18) and
\(|d\cdot\Delta p|\le\|d\|_\infty r_w\) show that every nonzero
form in (18) remains at least \(\kappa\|d\|_\infty\).
At variance \(s\), the A and B exponential sums have the positive factors
\(e^{-1/s},e^{-3/(2s)}\), respectively. Therefore, writing
\(f_s=\mu_p*\gamma_s,g_s=\nu_p*\gamma_s\), we obtain for every
chamber point \(x\ne0\),

\[
 g_s(j_i x)-f_s(i x)
 \ge \gamma_s(x)\kappa e^{-3/(2s)}
       \frac{(u-1)+(v-1)+(w-1)}{uv^2w^3}>0,                 \tag{19}
\]

where this time \(u=e^{(x_1-x_2)/s},v=e^{(x_2-x_3)/s},w=e^{x_3/s}\).
The same \(j_i\) works on every chamber face; at least one of the three
linear terms is positive away from zero. In particular, on every orbit,

\[
                     \max_{g\in G}g_s(gx)
                         >\max_{g\in G}f_s(gx)\quad(x\ne0).
                                                                  \tag{20}
\]

For example (19) gives the explicit lower bound
\(C_s\kappa e^{-3/(2s)}e^{-|x|^2/(2s)}
 e^{-\sqrt3|x|/s}|x|/(\sqrt3s)\) for the difference of these maxima.
No approximate exponential evaluation is part of the certificate.

## 6. Strict hinges, peaks, and the geometric margin

The source density does not have a maximum at zero. In fact

\[
 \partial_1 f_s(0)=\frac{C_s}{s}
 \left[e^{-1/s}(p_1-p_3)
       -e^{-3/(2s)}(p_5-p_6-p_7+p_8)\right]<0.                \tag{21}
\]

The two parenthesized linear forms have base values \(-3/184\) and
\(30/184\), and the weight perturbation changes each by at most
\(1/4000\). A global source maximizer exists and is nonzero. Applying
(20) at it proves \(\|g_s\|_\infty>\|f_s\|_\infty\).
Also \(g_s(0)=f_s(0)\), so a target maximizer is nonzero.

For every \(0<a<\|g_s\|_\infty\), choose such a target maximizer
\(x_0\ne0\) and follow \(t x_0\), \(t\ge1\), to infinity.
The continuous function \(\max_Gg_s(gtx_0)\) starts above \(a\)
and tends to zero. At its first crossing of \(a\), (20) says that
all source orbit values are strictly below \(a\). Immediately before
the crossing, some target value is above \(a\), while every source
value remains below. This persists on a nonempty open set of spatial
points. The earlier orbit theorem gives nonnegative orbitwise hinge gaps
everywhere; this open set gives a strictly positive integral. Hence

\[
                    H_{g_s}(a)>H_{f_s}(a)
                       \quad(0<a<\|g_s\|_\infty).           \tag{22}
\]

It remains to check the mean-support gap. The elementary geometry below
also appears in the team's
[preceding high-variance proof](../gaussian_asymmetric_eventual_majorisation/PROOF.md),
which we credit. Write
\(u=|\theta_1|,v=|\theta_2|,q=|\theta_3|\),
\(m_0=\max(u,v),n=u+v,\ell=\min(u,v)\).
Averaging the two signs of the third coordinate gives

\[
 \frac12\{\max(q+m_0,n-q)-\max(0,n-q)\}                     \tag{23}
\]

for \(h_X-h_Y\). This is always nonnegative. If \(q\ge\ell\),
the bracket is at least \(q\): it is \(2q-\ell\) when \(q\le n\),
and \(q+m_0\) otherwise. Since
\(\ell^2\le(1-q^2)/2\), it suffices that \(q\ge1/\sqrt3\).
Under normalized area on \(S^2\), \(|\theta_3|\) is uniform on
\([0,1]\). Consequently

\[
                  \overline h_X-\overline h_Y
                    \ge\frac12\int_{1/\sqrt3}^1q\,dq
                    =\frac16.                              \tag{24}
\]

All weights in Theorem 1 exceed \(1/32\), so none of the base sites is
lost. The supports in (24) do not depend on those weights.
Equations (20)--(24) establish every strict condition (13), uniformly on
compact sets of \((p,s)\) with \(\|p-p^*\|_1\le1/4000,s\in I\).
The compact-family assertion of Theorem 3 proves Theorem 1. For its low
thresholds one can take cloud radius at most \(1/48\), \(R=2,m=1/32\),
and \(\delta=1/8\) in Lemma 2, before making the radius smaller to
protect the middle thresholds and peak gap.

## 7. Actual contractions with solid support and preserved trust boundaries

The class includes genuine nonlinear contraction pairs with solid support.
Let \(\epsilon_I\) be as in Theorem 1. Choose \(c<1\) sufficiently
close to one that \((1-c)\sqrt3<\epsilon_I/2\), and then choose
\(\eta>0\) smaller than \(\epsilon_I/2\) and

\[
                   \frac{(1-c)\sqrt2}{2(1+c)}.               \tag{25}
\]

On the nine disjoint balls \(B(X_i,\eta)\), define
\(T(z)=cz\) for the origin and A balls, and \(T(z)=-cz\) for the
negative B balls. Within a ball it is a similarity of ratio \(c\).
For points in different balls the output distance is at most
\(c|Y_i-Y_j|+2c\eta\), and the input distance is at least
\(|X_i-X_j|-2\eta\). The original map contracts and the minimum
source separation is \(\sqrt2\); (25) therefore proves that \(T\)
is 1-Lipschitz on their union. Kirszbraun gives a global extension.
Each output cloud is within
\((1-c)\sqrt3+c\eta<\epsilon_I\) of its corresponding \(Y_i\).
Thus any probability law assigning masses \(p_i\) to these solid balls
satisfies (3) under this map for all \(s\in I\). Uniform ball laws are
one explicit nonatomic choice. Small strict changes of the centers and
local contractions are allowed by the same strict metric bounds.

These positive examples also retain the reviewed covariance obstruction
when the cloud radius is sufficiently small. For one endpoint supported
initially in radius \(\sqrt3\), moving every point by at most
\(\epsilon\) changes covariance in operator norm by at most
\(4\sqrt3\epsilon+2\epsilon^2\). The two endpoints' middle-eigenvalue
gap therefore loses at most \(8\sqrt3\epsilon+4\epsilon^2\).
The [reviewed base gap](../gaussian_atomic_bridge_obstruction_review1/REVIEW.md)
is strictly larger than \(11/2000\) on the entire weight ball.
Taking \(\epsilon_I\le1/10000\) keeps it positive. Thus the new
nonatomic positive class is compatible with failure of the center-law
martingale route, including separate isometries and common isotropic
Gaussian noise. This preserves the existing obstruction inside a positive
class; it is not a separate negative-bridge project.

The all-variance theorem for the exact rays and the all-orders theorem
for perturbed clouds on a fixed compact variance interval are distinct.
No uniform perturbation radius over \((0,\infty)\) is claimed. This
work does not establish a new Kneser--Poulsen limit, nor majorisation for
arbitrary three-dimensional contractions. Its contribution is a positive
stability bridge from existing classes to arbitrary small spatial clouds,
with a strict undamped application beyond the original ray geometry.

The finite certificate proves (18) and the strict linear witnesses.
The preceding packet supplies the nonnegative orbitwise hinge theorem.
The flow, superlevel-volume estimates, openness argument, and compactness
step are analytic author proofs. None is certified merely by a hash or
numerical grid. [SOURCES.md](SOURCES.md) records exact dependencies.


## 8. Relation to the team's global fixed-variance criterion

The newly consolidated [global criterion](../gaussian_majorisation_global_criterion/PROOF.md)
defines the worst hinge violation Delta_s. It identifies Delta_s=0 with
zero failure probability in an endpoint density-value coupling and with
nonnegativity of the complete beta/Hankel hierarchy. Theorem 1 here gives
Delta_s=0 for every cloud pair in (2), simultaneously for s in I. In fact
its low and middle gaps are strict; above the middle range the source
hinge is zero. Consequently every beta test, whose kernel is positive
on (0,1), is strictly positive for each fixed finite degree. More explicitly,
put C=(2 pi s)^(-3/2), H(u)=H_g(Cu)-H_f(Cu), and
m_j=integral_0^1 u^j H(u) du. Every finite endpoint Hankel matrix
(m_(i+j)) is positive definite: its quadratic form is
integral_0^1 q(u)^2 H(u) du, which is positive for every nonzero polynomial
q because H is positive on an open interval. The same assertion holds for
any finite distinct nonnegative integer exponent set. No lower bound
uniform in the matrix size is asserted.

This is an exact all-order statement at fixed variance. It does not
exchange a growing-order variance threshold with an infinite hierarchy.
The global criterion's total-variation bound alone only gives a small
possible defect after perturbation. The strict peak, middle gap, and
geometric low-threshold estimate supply the additional signed information
that keeps the defect exactly zero here. Conversely, a zero of that global
criterion at one finite atomic pair is enough for Corollary 4, subject
to its nonpoint target condition, after any strict target homothety.

The [axial-cone scope consolidation](../gaussian_axial_cone_rotations/SCOPE.md)
retains stronger all-law, all-variance, and individual-radius geometric
quantifiers on its own domain. This stability theorem does not enlarge
its undamped perimeter budget or replace its Kneser--Poulsen result.
It transfers finite certified members of the existing landscape to local
all-order neighborhoods and supplies an undamped strictness certificate
for the square-cone member. The unrestricted global zero-defect obligation
is still open.
