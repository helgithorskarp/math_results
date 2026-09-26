# Bounded-law stability and finite certificates for every Gaussian hinge

Author proof, 26 September 2026; independent review and formalization
pending. This consolidates the finite-base stability theorem in
[PROOF.md](PROOF.md). It removes atomicity of the base laws and connects
the resulting open set to the team's
[global moment criterion](../gaussian_majorisation_global_criterion/PROOF.md).
The unrestricted three-dimensional contraction problem remains open.

The results concern arbitrary bounded probability laws in R3, without
assuming a map between the endpoints. In particular they apply to
contraction pairs when those pairs meet the stated hypotheses. All
Gaussian covariances are s I3. No radius uniform over every bounded law
or every positive variance is claimed.

## 1. Statement of the bounded-law bridge

For a bounded Borel probability law lambda, its support means its closed
support K, which is compact. Write

\[
 h_K(\theta)=\sup_{z\in K}\theta\cdot z,\qquad
 w(K)=\int_{S^2}h_K(\theta)\,d\sigma(\theta),\qquad
 H_f(a)=\int_{\mathbb R^3}(f-a)_+\,dx .                       \tag{B1}
\]

Here sigma is normalized area measure; w is half the usual mean width,
and is invariant under translation. Write W_infinity for the infimum,
over couplings, of the essential supremum of the distance. For two
compactly supported laws this infimum is attained: couplings are weakly
compact on the product of the two compact supports, and a weak limit of
couplings whose distances are at most r+1/n is concentrated on the
closed set of distances at most r.

**Theorem A (bounded base laws).** Let mu, nu have bounded support, fix
s0>0, and put f=mu*gamma_s0, g=nu*gamma_s0. Suppose

\[
 w(\operatorname{supp}\mu)>w(\operatorname{supp}\nu),\quad
 \|f\|_\infty<\|g\|_\infty,\quad
 H_g(a)>H_f(a)\quad(0<a<\|g\|_\infty).                       \tag{B2}
\]

There exist epsilon>0 and rho>0 such that every independent pair mu',nu'
with W_infinity(mu,mu')<epsilon and W_infinity(nu,nu')<epsilon satisfies

\[
 H_{\mu'*\gamma_s}(a)\le H_{\nu'*\gamma_s}(a)
 \quad\text{for every }a>0,\quad |s-s_0|<\rho .              \tag{B3}
\]

The perturbations themselves may have arbitrary atomic and nonatomic
parts. In fact they still satisfy all three strict conditions (B2).
A compact family of triples (mu,nu,s0) satisfying (B2), with the product
W_infinity topology on the laws and the usual topology on positive
variance, has one common positive neighborhood radius.

**Theorem B (regularization and the exact interior).** Let M be the set
of triples (mu,nu,s) of bounded laws and s>0 satisfying every Gaussian
hinge comparison. Then:

1. The interior of M consists exactly of the triples satisfying (B2).
   The same statement holds for the fixed-s section in the product
   W_infinity topology.
2. If (mu,nu,s) belongs to M and nu is not a point mass, then for every
   0<c<1, (mu,(c id)_#nu,s) is an interior point. These interior points
   converge to (mu,nu,s) as c increases to one.
3. M is closed and is the closure of its interior, both with variance
   variable and at each fixed variance.

For a known all-variance comparison and a fixed c<1, compactness gives
one spatial neighborhood valid simultaneously on every specified compact
variance interval. This transfers whole bounded-law members of the team's
geometric and density-orbit classes. The radius may depend on the laws,
the damping, and the interval; it is not a domain-wide all-law radius.
Finite changes of atom weights are additionally covered by the original
Theorem 3 in PROOF.md; they need not be small in W_infinity.

## 2. Finite support nets retain positive cluster masses

Fix a compact support K and eta>0. Choose finitely many points x_i in K,
separated by more than eta, that are maximal for this property. A greedy
construction terminates because a compact set has only finitely many
points separated by more than a fixed positive distance. Maximality
implies that every point of K is within eta of some x_i.

Partition K into nearest-site cells, breaking ties by the smallest index.
They are Borel sets. The cell of x_i contains K intersected with the
open ball B(x_i,eta/2); that ball has positive lambda mass because x_i
is a support point. Thus its cell has mass p_i>0. The associated atomic
net lambda_eta=sum_i p_i delta_x_i has

\[
 W_\infty(\lambda,\lambda_\eta)\le\eta,\qquad
 0\le h_K(\theta)-\max_i\theta\cdot x_i\le\eta.              \tag{B4}
\]

If W_infinity(lambda,lambda')<=epsilon, take an attaining coupling
(Z,Z'). Restrict that joint law to each event that Z lies in a given
cell. The conditional law of Z' has total assigned mass p_i and is
supported within eta+epsilon of x_i. This is a finite cloud
decomposition with a strictly positive mass floor min_i p_i. No lower
bound on individual atom masses of lambda or lambda' is required; no
disintegration beyond conditioning on finitely many positive-mass events
is used. A cloud support lies in the stated closed ball because the
coupling distance bound holds almost surely.

The mass floor depends on the law and the chosen net scale. We fix the
net first and never assume a positive mass floor uniform as eta tends to
zero or over all bounded laws. This distinction is essential to the
tail estimate and respects the previously closed tail-error route.

## 3. Low-threshold geometry for arbitrary bounded laws

Let f_s=lambda*gamma_s, C_s=(2 pi s)^(-3/2), and
a=C_s exp(-q^2/(2s)). Equation (10) of PROOF.md applies to the above
eta-cloud decomposition. For fixed eta and a compact positive variance
interval I, choose R bounding |x_i|+eta and S=max I. If m=min_i p_i,
put K_eta=R^2+2S log(1/m) and B_eta=K_eta+5R^2. For all sufficiently
large q, uniformly in s in I,

\[
 \left|\frac{V_{f_s}(a)-(4\pi/3)q^3}{4\pi q^2}
                 -w(\{x_i\})\right|
       \le\eta+B_\eta/q.                                  \tag{B5}
\]

The net support functions differ from h_K by at most eta. First let q
tend to infinity with eta fixed, and then let eta tend to zero. This
proves the uniform-in-s asymptotic

\[
 V_{f_s}(C_s e^{-q^2/(2s)})
     =\frac{4\pi}{3}q^3+4\pi q^2w(K)+o(q^2),
       \qquad q\longrightarrow\infty,\ s\in I.             \tag{B6}
\]

We claim no uniform remainder over all input laws. At any one fixed
variance, subtract (B6) for two laws and use the exact layer-cake identity

\[
 H_g(a)-H_f(a)=\int_0^a\{V_f(t)-V_g(t)\}\,dt.                \tag{B7}
\]

If w(supp mu)<w(supp nu), the integrand is strictly negative for every
sufficiently small positive t, contradicting hinge order. Consequently

\[
 \mu*\gamma_s\prec\nu*\gamma_s
       \quad\Longrightarrow\quad
       w(\operatorname{supp}\mu)\ge w(\operatorname{supp}\nu).
                                                                  \tag{B8}
\]

For stability we use an explicit signed estimate, not just this
asymptotic. Put delta0=w(supp mu)-w(supp nu)>0. Choose eta>0 with
eta<=delta0/16, and fix eta-nets of both supports. For endpoint
perturbations of W_infinity distance at most epsilon<=eta, each is an
(eta+epsilon)-cloud about its net, with the same assigned cell masses.
The net mean-support difference is at least delta0-2eta, so

\[
 w(\{x_i\})-w(\{y_j\})-2(\eta+\epsilon)
       \ge\delta_0-4\eta-2\epsilon\ge\delta_0/2.             \tag{B9}
\]

Use delta=delta0/2 in Lemma 2 of PROOF.md. Both finite mass floors are
fixed, and R can bound all |x_i|+2eta and |y_j|+2eta. That lemma now
gives a common strictly positive low-threshold bound for every perturbed
law and every variance in [s0/2,2s0]. The unknown internal distribution of
each cloud has no effect on its validity.

## 4. Middle thresholds, peaks, and openness

For any coupling with |Z-Z'|<=epsilon, integration of translated
Gaussian derivatives gives, at a common variance s,

\[
 \|\lambda*\gamma_s-\lambda'*\gamma_s\|_1
       \le\epsilon/\sqrt{s},\qquad
 \|\lambda*\gamma_s-\lambda'*\gamma_s\|_\infty
       \le C_s\epsilon/\sqrt{s}.                            \tag{B10}
\]

Indeed every unit directional derivative of gamma_s has L1 norm at most
1/sqrt(s) and supremum norm at most C_s/sqrt(s). Integrate the segment
between Z and Z', then average over the coupling. A change of variance
costs at most the corresponding L1 or supremum norm difference of the
two Gaussian kernels, which tends to zero uniformly away from s=0.
Also |H_f(a)-H_f'(a)|<=||f-f'||_1 uniformly in a.

Take b=(||f||_infinity+||g||_infinity)/2. Section 3 supplies a common
a_->0 for all low thresholds; decrease it so that a_-<b. On [a_-,b]
the base hinge gap has a strictly positive minimum. Its continuity in
a follows, for example, by dominated convergence in each hinge. The
bounds (B10) preserve that minimum for small perturbations. They also
keep the source peak below b and the target peak above b. For a>=b the
source hinge vanishes. Thus every hinge compares, and it is strict at
each a below the perturbed target peak.

For completeness, an attaining W_infinity coupling also shows that the
two closed supports are within Hausdorff distance epsilon: every
positive-mass ball about a support point must couple into its
epsilon-enlargement. Taking shrinking balls proves the assertion.
Hence their support functions differ by at most epsilon, and the
strict mean-support gap persists too. This proves Theorem A locally.

Equip triples with the maximum of the two W_infinity distances and
|s-s'|. An open neighborhood of a compact family contains a uniform
metric neighborhood of it: choose balls inside the open set, cover the
compact family by their half-radius balls, and take a finite subcover.
The minimum of the resulting finitely many positive half-radii suffices.
This proves the compact-family assertion without assuming a common mass
floor for an arbitrary unselected collection of input laws.

## 5. Strict homothety flow for arbitrary bounded posterior laws

Let Y have bounded law nu and set g_t=law(e^(-t)Y+Z_s), for t>=0.
Every differentiation below is justified by bounded Y and the smooth
Gaussian kernel. With conditional expectations taken under the Gaussian
posterior,

\[
 v_t(x)=-\mathbb E[e^{-t}Y\mid e^{-t}Y+Z_s=x],\qquad
 Dv_t(x)=-s^{-1}\operatorname{Cov}(e^{-t}Y\mid x),\qquad
 \partial_t g_t+\operatorname{div}(g_tv_t)=0.                 \tag{B11}
\]

The posterior has density proportional to gamma_s(x-e^(-t)y) relative
to nu. It is therefore equivalent to nu, including when nu is singular
or nonatomic. If nu is not a point mass, its posterior trace covariance
is strictly positive for every x and every finite t. The velocity is
bounded and globally Lipschitz, uniformly on compact time intervals,
because Y is bounded and its posterior covariance is uniformly bounded.
Its global flow satisfies

\[
 \frac{d}{dt}g_t(x_t)
      =\frac{g_t(x_t)}{s}
          \operatorname{tr}\operatorname{Cov}(e^{-t}Y\mid x_t)>0.
                                                                  \tag{B12}
\]

These densities tend to zero at spatial infinity and attain their
maxima. Follow a starting maximizer to conclude that their peaks
increase strictly between any two finite times.

The hinge identity is

\[
 H_{g_T}(a)-H_{g_0}(a)
  =\frac a s\int_0^T\int_{\{g_t>a\}}
       \operatorname{tr}\operatorname{Cov}(e^{-t}Y\mid x)
                         \,dx\,dt.                         \tag{B13}
\]

To justify it, approximate (r-a)_+ by smooth convex functions that
vanish for r<a/2 and whose pressures r U'(r)-U(r) converge to
a 1_(r>a), bounded by a constant depending on a. Integration by parts
in (B11) gives the pressure times trace-covariance formula. The relevant
superlevel sets lie in a common bounded spatial set over compact time
intervals. Each g_t is real analytic: integration against bounded Y
allows differentiation, or complex analytic extension, on compact
sets. It is nonconstant, so each positive level set has Lebesgue
measure zero; see the primary [zero-set proof](https://arxiv.org/abs/1512.07276).
Dominated convergence in space and time gives (B13),
without a regular-level assumption.

For 0<a<||g_T||_infinity, a positive space-time neighborhood near time T
lies above the threshold and has positive posterior trace covariance.
Thus (B13) is strictly positive. With T=-log c, any given full comparison
mu*gamma_s prec nu*gamma_s therefore becomes strictly ordered in every
hinge below the new target peak, and its peaks become strictly ordered.
By (B8) its old mean supports were ordered. A nonpoint compact support L
has w(L)>0: for two distinct points y,z in L, its mean support is at
least |y-z|/4. Since w(cL)=c w(L), damping makes this gap strict too.
Theorem A proves Theorem B(2).

This homothetic monotonicity is a special case of the known continuous-
contraction theory, including Aishwarya--Li Theorem 1.4. The strictness,
topology, and endpoint controls are its roles here.

## 6. The interior characterization and density

Suppose a triple belongs to M. Its means satisfy (B8), and its source
peak cannot exceed the target peak, by the hinge comparison at a
threshold between them.

If mu is a point mass, its Gaussian peak is C_s. A Gaussian convolution
of a nonpoint bounded law has maximum strictly below C_s: a maximum is
attained, and equality in the pointwise Gaussian upper bound would
force the law to be a point mass at that maximizer. Thus nu must also
be a point mass. Arbitrarily slightly replacing nu by two distinct
nearby equal-weight atoms makes its peak less than the source peak.
Such a pair is not interior.

Now suppose mu is not a point mass. Contract the source by c<1 as close
to one as desired, keeping the target and variance fixed. This is an
arbitrarily small W_infinity perturbation. If the mean supports were
equal, the source contraction makes their order fail, since
w(supp mu)>0. If the peaks were equal, (B12) makes their order fail.
If H_g(a)=H_f(a) for some 0<a<||g||_infinity, both hinges are positive,
so a<||f||_infinity. Equation (B13) strictly increases the source hinge
and again violates comparison. Therefore every interior point must
satisfy all of (B2). Theorem A proves sufficiency. This proves
Theorem B(1), including for a fixed variance.

The set M is closed in the specified space by (B10), kernel continuity,
and passage to the limit in each individual hinge. For density, the
nonpoint-target case is Theorem B(2). If nu is a point mass and mu is
nonpoint, this pair already satisfies (B2). Indeed its target peak and
mean-support inequalities are strict. Apply the homothety flow to mu.
Its densities converge in L1 to gamma_s as t tends to infinity. For
any 0<a<C_s, some finite-time peak exceeds a; comparison between that
time and a later finite time in (B13) is strict. Monotonicity at all
other times and the L1 limit show H_gamma_s(a)>H_f(a). A translation
of the point-mass target does not affect its hinges. Finally, if both
laws are point masses, replace the source by two equal-weight atoms
arbitrarily close to its original point. The preceding argument makes
each such pair an interior point. This proves Theorem B(3).

These topological conclusions do not continue an unknown contraction
through the whole zero-defect set: a proposed path still needs control
of its middle hinges. The next section gives a finite sufficient test
when the two endpoints of the threshold range are controlled.

## 7. A finite positive certificate at one fixed variance

The [global criterion](../gaussian_majorisation_global_criterion/PROOF.md)
supplies the exact normalized hinge moments and beta averages. Reuse
its notation at a fixed s>0:

\[
 C=(2\pi s)^{-3/2},\quad H(u)=H_g(Cu)-H_f(Cu),\quad
 a_j=\frac{C\int[(g/C)^{j+2}-(f/C)^{j+2}]}{(j+1)(j+2)},
 \quad
 b_{N,k}=(N+1){N\choose k}\sum_{\ell=0}^{N-k}
                   (-1)^\ell {N-k\choose\ell}a_{k+\ell}.
                                                                  \tag{B14}
\]

Thus b_(N,k)=E H(V) for V distributed as Beta(k+1,N-k+1).
If the two supports lie, after separate translations, in radius-R balls,
that source's explicit constant

\[
 L=2\sqrt{2/\pi}\left[r^3/3+\sqrt\pi r^2+4r+2\sqrt\pi\right],
 \qquad r=R/\sqrt{s},                                      \tag{B15}
\]

satisfies |H(u)-H(v)|<=L |u-v|^(1/2) on [0,1]. The proof only uses
bounded support, not a map: pointwise hinge differences are bounded by
sqrt(C f)|u-v|^(1/2), and similarly for g. Gaussian radial integration
bounds sqrt(C)(integral sqrt(f)+integral sqrt(g)) by (B15).

Assume that two rigorous endpoint certificates have been supplied:

\[
 H(u)\ge0\ (0\le u\le\tau),\qquad
 \|f\|_\infty/C\le b,\qquad 0<\tau<b<1.                    \tag{B16}
\]

For example, Lemma 2 of PROOF.md supplies the first with
tau=exp(-Q^2/(2s)) from its finite cloud decomposition, mass floor and
positive geometric margin. Section 2 supplies such a finite decomposition
for any bounded base pair with a positive mean-support gap. The second
certificate needs an actual upper bound on the source peak.

For N>=0 define

\[
 t_k=\frac{k+1}{N+2},\quad
 J_N=\left\{0\le k\le N:
        \operatorname{dist}(t_k,[\tau,b])\le\frac1{N+2}\right\},
 \qquad
 E_N=L\left[\frac1{4(N+3)}+\frac1{(N+2)^2}\right]^{1/4}.
                                                                  \tag{B17}
\]

**Theorem C (finite moments plus signed endpoint control).** If (B16)
holds and

\[
                  b_{N,k}>E_N\qquad(k\in J_N)               \tag{B18}
\]

for one finite N, then H(u)>=0 for every u in [0,1]. In particular
Delta_s=0 and every convex-energy comparison holds at this fixed s.
Only powers through N+2 enter (B18). The complete beta hierarchy and
every endpoint Hankel matrix are then nonnegative at the same variance;
each finite Hankel matrix on distinct nonnegative integer exponents is
in fact positive definite, since H is strictly positive on [tau,b].

**Proof.** Every u in [0,1] is within 1/(N+2) of at least one t_k;
this includes the two ends of the grid. For u in [tau,b], such an index
belongs to J_N. The beta law has mean t_k and variance at most
1/[4(N+3)]. Hence Jensen's inequality and (B15) give

\[
 |b_{N,k}-H(u)|
 \le L\,\mathbb E|V-u|^{1/2}
 \le L\{\mathbb E(V-u)^2\}^{1/4}
 \le E_N.                                                   \tag{B19}
\]

Condition (B18) proves strict positivity on the whole middle interval,
not merely at the grid points. The low interval is covered by (B16).
Above b the source hinge is zero, so the target hinge is nonnegative.
This proves the full comparison. A nonzero polynomial is nonzero on a
subset of positive measure of [tau,b], so integral q(u)^2 H(u) du>0.
This proves the Hankel assertion, also for arbitrary distinct exponent
sets. QED.

**Completeness on the interior.** Every pair satisfying (B2) admits
endpoint choices (B16) for which (B18) succeeds at a finite degree.
Take b strictly between the normalized peaks and take tau>0 sufficiently
small using Section 3. Let h_*=min_[tau,b] H>0. For each k in J_N,
choose u_k in [tau,b] within 1/(N+2) of t_k. Equation (B19) gives
b_(N,k)>=h_*-E_N. Since E_N tends to zero, every N with 2E_N<h_*
satisfies (B18). This is an existence statement; it does not assert a
practical degree or compute a numerical h_* for arbitrary input laws.

For finite rational atomic data the moments in (B14) are finite Gaussian
replica exponential sums, as in equation (10) of the global criterion.
They can in principle be enclosed with rigorous arithmetic. The test
requires certified strict lower bounds above a certified upper bound
for E_N; floating-point positivity is insufficient. The support geometry,
mass floor, and peak bound remain separate obligations. For general
bounded laws the theorem is an analytic finite-moment criterion; it does
not promise an algorithm for arbitrary unspecified measures.

Bare nonnegativity of finitely many beta tests is not this certificate.
The signed endpoint bounds and the strict localization margin (B18)
are what certify the unsampled thresholds. No new numerical certificate
degree is claimed for a configuration beyond the existing positive classes.

## 8. Durable relation to Team B's class landscape

| Input result | Consequence of this consolidation |
| --- | --- |
| Global coupling/moment criterion | Its zero-defect set has the exact interior (B2). Every interior pair has a finite positive certificate of the form (B16)--(B18), and a zero-failure endpoint density-value coupling. |
| Axial, simplicial, scalar-defect and damped-cone classes | Each bounded-law member with nonpoint target, including a nonatomic member, becomes an interior pair after any strict additional target homothety. On a specified compact variance interval one common spatial neighborhood works. |
| Common-target mixtures | The same transfer applies to its arbitrary solid background and bounded radial laws, retaining the original common-output and weight hypotheses. |
| Square-cone orbit comparison | Its bounded radial-law extension can enter the same damped bridge. The special nine-site family already has undamped strictness by PROOF.md, with a uniform original weight ball and arbitrary small clouds. |
| [Paired-layer completion](../gaussian_paired_layers_majorisation/ALL_VARIANCES.md) | This source has already combined our original compact-band stability theorem with its own small- and large-variance controls to obtain one constrained spatial neighborhood for all variances. Its geometric and weight restrictions are retained; it does not assert arbitrary nonatomic clouds down to zero variance. |
| Replica curvature and sparse Hankel results | Theorem C certifies every order at one fixed variance once its finite strict tests and signed endpoints are supplied. It does not interchange an order-dependent variance bound with an infinite hierarchy. |

The geometric source theorems retain their stronger domain-wide,
all-variance and individual-radius Kneser--Poulsen quantifiers. The
neighborhoods here depend on a chosen law and a positive variance band,
so they yield no new small-variance geometric limit. A new unrestricted
R3 theorem or counterexample still requires a global zero-defect or
negative-hinge argument outside these certified classes.

The latest [geometric-endpoint annex](../gaussian_majorisation_global_criterion/GEOMETRIC_LIMIT.md)
identifies the sharper pathwise scale Delta_s/a_s for exponentially varying
weights and classifies the old orbit cones' limiting radius profiles.
The neighborhoods and finite certificate here have no uniform estimate
on that scale as s tends to zero. They therefore do not change that
annex's radius-rematching boundary. The new
[axial composition comparison](../gaussian_axial_cone_rotations/COMPOSITIONS.md)
is also retained as a class distinction; its negative factorization
statement is not a premise of the positive bridge here.

The support-net, flow, topology and beta-localization proofs above are
analytic author proofs. The unchanged finite checker in this directory
checks only the square-cone strictness inputs listed in README.md; it
does not certify the measure-theoretic extension or Theorem C. Exact
dependencies and the initial source revision are in [SOURCES.md](SOURCES.md).
