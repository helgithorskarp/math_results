# Full shallow-flap comparison at each fixed Gaussian variance

Complete author proof, 26 September 2026; independent review pending.
For an open class of asymmetric simplex-flap maps, every positive choice
of the sixteen atom weights satisfies all Gaussian hinge inequalities
at each fixed variance once the depth is sufficiently small. Sections 7-8
prove this using a positive support coefficient, verified on an open
geometric neighborhood of the regular tetrahedron and an explicit fully
asymmetric rational example. The depth may depend on the variance; no
new Kneser--Poulsen consequence or unrestricted R3 theorem is claimed.

The proof strengthens [TAIL_BLOWUP.md](TAIL_BLOWUP.md) by an explicit
relative error, valid down to scaling parameter zero and at unbounded
scaling parameter. Without the extra support condition, the same error
forces any shallow negative hinge into an extremely low-threshold region.

**Continuation:** [SUPPORT_SIGN.md](SUPPORT_SIGN.md), Theorem 7, now proves
the support condition for every nonisometric weighted simplex-flap map.
Consequently Theorem 6 applies to arbitrary tetrahedra, arbitrary positive
normal lengths and arbitrary nonnegative weights at each fixed variance.
The proof and explicit open-class control below are preserved.

## 1. Setup and the quantitative estimate

Use the vertices v_j, inward normals d_i=h_i grad(lambda_i), weights
alpha_j,beta_ij, collapsed masses w_j, occupied tips J, Gamma and spherical
coefficient L from TAIL_BLOWUP.md. Work first at variance one. Fix the
geometry and weights; zero label weights are allowed. Let

\[
 V\ge\max_j|v_j|,\quad D\ge\max_i|d_i|>0,\quad M=V+D,
 \qquad 0<\nu\le\min_{i<j}|v_i-v_j|,
 \qquad w_* =\min_{j\in J}w_j>0.                                \tag{1}
\]

Bounds V,D,nu need not be sharp. Put C_3=(2 pi)^(-3/2), and define

\[
 a_R=C_3e^{-R^2/2},\qquad
 G_R(\tau)=\frac{D_{1,\tau/R}(a_R)}{a_RR}.
                                                                    \tag{2}
\]

Thus depth is t=tau/R. Extend L continuously to L(0)=0.

**Theorem 3 (explicit relative error).** For T>=0 and
R>=max(2,4M,T), the derivatives exist on 0<=tau<=T (one-sided at the
endpoints) and

\[
 |G_R'(\tau)-L'(\tau)|\le E(R,T),\qquad
 |G_R(\tau)-L(\tau)|\le\tau E(R,T),                              \tag{3}
\]

where

\[
 E(R,T)=\frac{\pi D}{R}\left[
 560M+496+80MDT+
 \frac{480}{\nu}\left(\log\frac1{w_*}+\frac{V^2}{2}
                         +4DT+\log R\right)\right].             \tag{4}
\]

This is an analytic bound with explicit inputs, not a numerical
approximation or an assertion of uniformity as occupied weights vanish.
In particular the fixed-T convergence in (3) is **relative to tau**,
and remains valid when tau tends to zero arbitrarily fast with R.

To convert it to a sign, choose E_ij,B_ij,N_ij and rho_ij as in
TAIL_BLOWUP.md, Theorem 2, and put

\[
 c_{\mathcal G}=\min_{i\ne j}\frac{\rho_{ij}^3}{24E_{ij}},\qquad
 g_0=c_{\mathcal G}\Gamma e^{-3(2+M^2)}.                          \tag{5}
\]

If Gamma>0, then g_0>0 and the earlier coefficient bound gives
L(tau)>=g_0 tau exp(-6D tau). Consequently

\[
 D_{1,\tau/R}(a_R)
 \ge a_RR\tau\{g_0e^{-6DT}-E(R,T)\}
       \qquad(0\le\tau\le T).                                  \tag{6}
\]

For a prescribed T, (6) is an effective positive-hinge test using only
geometry, weights and elementary functions. If k_T=g_0 exp(-6DT), write
E(R,T)=pi D(A_T+B log R)/R, with A_T and B=480/nu read from (4).
The explicit condition

\[
 R\ge\max\left\{2,4M,T,
             \frac{4\pi D A_T}{k_T},
             \left(\frac{4\pi D B}{k_T}\right)^2\right\}         \tag{7}
\]

ensures E(R,T)<=k_T/2. Indeed log R<=sqrt(R) for R>=1. No implicit
choice of a sufficiently large radius is needed in this fixed-T test.

## 2. A logarithmically growing window

Define

\[
 A_0=560M+496+\frac{480}{\nu}
               \left(\log\frac1{w_*}+\frac{V^2}{2}\right),
 \qquad A_1=\frac{20M}{3}+\frac{640}{\nu}.
\]

**Corollary 4 (effective growing window).** Suppose Gamma>0. For

\[
 R\ge R_*:=\max\left\{2,4M,(12D)^{-2},
          \left(\frac{4\pi D A_0}{g_0}\right)^2,
          \left(\frac{8\pi D A_1}{g_0}\right)^4\right\},          \tag{8}
\]

every 0<tau<=log R/(12D) satisfies

\[
 D_{1,\tau/R}(a_R)\ge\tfrac12 g_0 a_R\tau\sqrt R>0.              \tag{9}
\]

Proof: take T=log R/(12D). The first three restrictions in (8) make
Theorem 3 applicable, since log R<=sqrt R. Equations (4)-(5) give
E=pi D(A_0+A_1 log R)/R and k_T=g_0/sqrt R. The elementary inequality
log R<=2 R^(1/4) for R>=1, and the last two restrictions in (8), imply

\[
 \frac{E}{k_T}
 \le\frac{\pi D}{g_0}
       \left(\frac{A_0}{\sqrt R}+\frac{2A_1}{R^{1/4}}\right)
 \le\tfrac12.
\]

Equation (6) proves (9). The logarithmic inequality follows by maximizing
y exp(-y/4) for y=log R>=0: its maximum is 4/e<2.

More generally, for any fixed 0<b<1/(6D), all sufficiently large R give
strict positive hinges simultaneously on 0<tau<=b log R. In fact
E(R,b log R)=O(log R/R), whereas g_0 exp(-6Db log R)=g_0 R^(-6Db);
their ratio tends to zero. This larger asymptotic range is asserted
without an optimized effective R threshold.

**Corollary 5 (necessary scale of a shallow counterexample).** Fix a
nonisometric weighted map in this family. If t_n decreases to zero and
D_(1,t_n)(a_n)<0, then a_n tends to zero and, with
R_n=sqrt(2 log(C_3/a_n)),

\[
           \liminf_n\frac{t_nR_n}{\log R_n}\ge\frac1{6D}.         \tag{10}
\]

The threshold-floor theorem in [PROOF.md](PROOF.md) gives a_n->0.
A negative hinge requires a_n<C_3, so R_n is defined, and R_n->infinity.
For every b<1/(6D), the growing-window conclusion eventually excludes
t_n R_n<=b log R_n, proving (10).

Consequently, the following complete threshold interval is positive:
for every 0<c<1/(72D^2), there is t_0>0 such that, for 0<t<t_0,

\[
 D_{1,t}(a)\ge0\quad\hbox{for all}\quad
 a\ge C_3\exp\left[-\frac{c(\log(1/t))^2}{t^2}\right].           \tag{11}
\]

To verify the uniform assertion, a hypothetical sequence of failures in
(11) would have R_n->infinity and
R_n<=sqrt(2c) log(1/t_n)/t_n. The function R/log R increases for R>e,
so its ratios in (10) would have limsup at most sqrt(2c)<1/(6D), a
contradiction. This argument uses the existing threshold-floor theorem;
it does not turn (8) into an effective bound for the final t_0 in (11).
The assertion includes high thresholds, at which both hinges may vanish.

Gamma=0 gives equality of all hinges, for every depth, by congruence.
For a general fixed variance s>0 apply the variance-one statements after
replacing v_j by v_j/sqrt(s), t by t/sqrt(s), and a by s^(3/2)a, while
leaving d_i and the weights unchanged. The normals are still inward;
their new h_i are h_i/sqrt(s). In particular (10) becomes

\[
 \liminf_n\frac{t_n\sqrt{2\log(C_s/a_n)}}
                    {\sqrt s\log\sqrt{2\log(C_s/a_n)}}
       \ge\frac1{6D},\qquad C_s=(2\pi s)^{-3/2}.                 \tag{12}
\]

Uniformity over unrestricted variances is not claimed.

## 3. Differentiating the radial boundary

We prove Theorem 3. Index every core or flap label by b, with mass p_b,
base vertex v_(j(b)), and offset d_b (zero for a core, d_i for flap(i,j)).
For epsilon in {-1,+1}, its center is

\[
       c_b=v_{j(b)}+\epsilon\tau d_b/R.
\]

All centers have norm at most M on 0<=tau<=T. The positive a_R-superlevel
set has a unique outer radius r=r_epsilon(theta,tau) in [R-M,R+M], as
proved in TAIL_BLOWUP.md, Section 2. Its radial logarithmic derivative is
-r+m_theta, with m_theta=sum_b pi_b theta.c_b and |m_theta|<=M.
Thus r-m_theta>=R-2M>=R/2. The implicit-function theorem makes r smooth
in tau and theta. All differentiations below are at **fixed R and a_R**.

Set A=sum_b pi_b theta.d_b and B_0=sum_b pi_b c_b.d_b. Differentiating
the level equation gives exactly

\[
 R\partial_\tau r
       =\epsilon\frac{rA-B_0}{r-m_\theta}
       =\epsilon A+
             \epsilon\frac{A m_\theta-B_0}{r-m_\theta}.           \tag{13}
\]

In particular

\[
 |R\partial_\tau r-\epsilon A|\le4MD/R,\qquad
 |\partial_\tau r|\le2D/R.                                     \tag{14}
\]

Define the ideal conditional directional average at tip j by

\[
 A_j^\epsilon(\theta,\tau)
   =\frac{\sum_{i\ne j}\beta_{ij}(\theta\cdot d_i)
                         e^{\epsilon\tau\theta\cdot d_i}}
          {W_j^\epsilon(\theta,\tau)}.
\]

It has absolute value at most D. Differentiation under the fixed fan cells
is justified by this bound, and gives

\[
             L'(\tau)=\sum_{j\in J}\int_{C_j}
                         (-A_j^- - A_j^+)\,d\sigma.              \tag{15}
\]

At the actual boundary, a label's exponent within tip j differs from
epsilon tau theta.d_b by

\[
 \epsilon\tau(r/R-1)\theta\cdot d_b
       -\epsilon(\tau/R)v_j\cdot d_b
       -\tau^2|d_b|^2/(2R^2).
\]

Its absolute value is at most eta=2TDM/R: use tau<=T<=R and
M+V+D/2<=2M. Changing finitely many log weights by amounts of absolute
value at most eta changes the expectation of a variable in [-D,D] by
at most 2D eta. To see this, interpolate the log weights linearly; the
derivative of the expectation is their covariance with the variable,
whose absolute value is at most 2D eta. Hence the true conditional
average within a tip differs from A_j^epsilon by at most 4TD^2M/R.

## 4. Dominance away from narrow fan walls

Let

\[
 c_T=\log(1/w_*)+V^2/2+4DT,\qquad
 \zeta=\frac{c_T+\log R}{R-M}.                                  \tag{16}
\]

Discard from S2 the union of slabs |(v_j-v_k).theta|<=zeta over all
six vertex pairs. Its area is at most 24 pi zeta/nu. Indeed the area
of each spherical slab is 4 pi min(1,zeta/|v_j-v_k|), by rotation to
one coordinate, and the union bound suffices. This estimate remains
valid if its right side exceeds 4 pi; no small-slab assumption is made.

Off these slabs, the dominant occupied tip j has projection advantage
at least zeta over every other occupied tip. The absolute offset
exponent at r theta is at most 2DT, because

\[
 \frac{(r+V)TD}{R}+\frac{T^2D^2}{2R^2}\le2DT
\]

under R>=4M and T<=R. The sum of all other tip contributions divided
by the dominant one is therefore at most

\[
 w_*^{-1}\exp(-(R-M)\zeta+V^2/2+4DT)=1/R.                       \tag{17}
\]

Their effect on a directional expectation in [-D,D] is at most 2D/R.
Combining (13)-(17), off the slabs, yields

\[
 |R\partial_\tau r-\epsilon A_j^\epsilon|
      \le4MD/R+4TD^2M/R+2D/R.                                 \tag{18}
\]

The derivative of radial volume divided by R is
integral (r/R)^2 R partial_tau r d sigma. Since
|(r/R)^2-1|<=(9/4)M/R and |R partial_tau r|<=2D, the discrepancy
for either sign's integrand is at most

\[
            \frac{10MD(1+DT)+2D}{R}.                            \tag{19}
\]

On the discarded slabs no dominance is needed. The actual integrand
has absolute value at most (5/4)^2(2D)=25D/8; its ideal counterpart
has absolute value at most D. For the difference of the two signs the
error is thus at most 33D/4<=10D. Integrating (19) on the complement
and this bound on the slabs proves

\[
 \left|\partial_\tau\frac{V_f-V_g}{R}-L'(\tau)\right|
 \le\frac{\pi D}{R}\left[
       80M(1+DT)+16+\frac{480}{\nu}(c_T+\log R)\right].           \tag{20}
\]

Here 1/(R-M)<=2/R was used. The factor 80 comes from two signs and
sphere area 4 pi. The proof works for zero label weights because the
dominance estimate only uses the positive collapsed masses w_j.

## 5. The differentiated exterior mass cancels at leading order

Controlling each exterior mass alone would lose the factor tau needed
in (3). Its derivative admits a sharper bound. For either sign and a
fixed direction, write Q_theta=integral_r^infinity P(ell theta) ell^2 d ell.
At the moving boundary P(r theta)=a_R, let pi_b be the posteriors and put

\[
 \ell=\sqrt{r^2+2u},\quad \Delta=\ell-r,\quad
 J(u)=\sum_b\pi_b e^{\Delta\theta\cdot c_b}.
\]

The substitution u=(ell^2-r^2)/2 is exact and gives

\[
                Q_\theta/a_R=\int_0^\infty e^{-u}\ell J(u)\,du.
                                                                    \tag{21}
\]

Here r>=3R/4>=1, Delta<=u/r, M/r<=1/3, and

\[
 |\ell'|\le2D/R,\qquad
 |\Delta'|\le2Du/(Rr^2),\qquad |c_b'|\le D/R.                    \tag{22}
\]

Primes denote tau derivatives. Since a_R is fixed, the posterior
derivative at r theta is pi_b'=pi_b S_b, where

\[
 S_b=(r\theta-c_b)\cdot(\epsilon d_b/R-r'\theta),\qquad
 \sum_b\pi_b'=0,\qquad
 \sum_b|\pi_b'|\le(r+M)(D/R+|r'|)\le5D.                         \tag{23}
\]

The zero sum permits subtraction of 1 inside the posterior-derivative
term in J'. Using |exp(z)-1|<=|z| exp(|z|), (22)-(23) imply

\[
 |J'|\le e^{Mu/r}\left(
          \frac{5DMu}{r}+
          \frac{2DMu}{Rr^2}+
          \frac{Du}{Rr}\right).                                \tag{24}
\]

Also J<=exp(Mu/r), and ell/r<=1+u/r^2<=1+u. These bounds give an
integrable derivative majorant, uniformly in theta,tau and both signs;
differentiation in (21) is legitimate. The elementary integrals

\[
 \int_0^\infty e^{-2u/3}\,du=3/2,\qquad
 \int_0^\infty e^{-2u/3}(u+u^2)\,du=9
\]

then yield

\[
 |Q_\theta'/a_R|
  \le45DM+18DM/R+12D/R\le60D(M+1).                              \tag{25}
\]

The complete exterior-mass difference therefore satisfies

\[
 \left|\partial_\tau\frac{Q_f-Q_g}{a_RR}\right|
                    \le\frac{480\pi D(M+1)}R.                   \tag{26}
\]

Finally D=Q_f-Q_g+a_R(V_f-V_g). Adding (20) and (26) proves the
derivative bound (3)-(4). Both G_R and L vanish at tau=0, so integrating
the derivative error from zero to tau proves its relative form. This
completes Theorem 3.

## 6. Exact effectivity control and limits

For the asymmetric uniform-weight fixture in TAIL_BLOWUP.md, take
V=5,D=2,M=7,nu=2,w_*=1/4,Gamma=33/64 and c_G=1/61440000. Then

\[
 g_0=\frac{11}{1310720000}e^{-153},\qquad
 A_0<7896,\qquad A_1=1100/3.
\]

The rational estimates pi<4, e<3 and log4<2 give a lower bound
g_0>11/(1310720000*3^153). Direct integer comparisons verify that
R=10^400 exceeds every requirement of (8). Hence (9) applies for every
R>=10^400 and every 0<tau<=log R/24 on this asymmetric fixture.
This enormous radius is an effectivity control, not a practical search
recommendation or a claim that the true onset is comparably large.
No value of exp(-R^2/2) is computed or stored.

[verify_relative.py](verify_relative.py) checks the rational constants,
the coefficient collection in (4), radial/angular arithmetic bounds,
the elementary integral values, and the explicit large-radius control.
It does not certify the analytic derivative estimates or the theorem by
finite testing. No quadrature, solver, asymptotic fit, or external data
is used. [SOURCES.md](SOURCES.md) records the prior results being consumed.

For arbitrary tetrahedral geometry, (10) is a necessary condition for a
failure, not a proof that such a failure exists or cannot exist. The
following additional geometric condition closes the remaining tail.

## 7. A positive support coefficient closes every threshold

For an occupied tip j, let A_j consist of d_i for which beta_ij>0 and
also of 0 if alpha_j>0. Write h_A(theta)=max_(d in A) d.theta, and put

\[
 \ell_\infty=\sum_{j\in J}\int_{C_j}
                 \{h_{A_j}(-\theta)-h_{A_j}(\theta)\}\,d\sigma.
                                                                    \tag{27}
\]

This quantity depends on the geometry and which labels have positive
weights, not on the magnitudes of those positive weights. It is the
large-tau limit of L(tau)/tau. More precisely, if p_* is the smallest
positive label weight, then

\[
 \left|L(\tau)/\tau-\ell_\infty\right|
                    \le\frac{8\pi\log(1/p_*)}{\tau}.             \tag{28}
\]

Indeed for either sign the logarithm of each W_j lies between
tau h_(A_j)(+/-theta)+log p_* and tau h_(A_j)(+/-theta): the weights
of that packet sum to at most one, and a maximizing label has weight at
least p_*. Subtract the two logarithms and integrate over cells of total
area 4 pi. The factor 8 pi is a conservative bound. In particular the
earlier L>=0 implies ell_infinity>=0, but does not prove its strictness.

**Theorem 6 (full shallow comparison at fixed variance).** If
ell_infinity>0, then for every fixed choice of these positive label
weights and every s>0 there exists t_*>0 such that

\[
                    H_{f_{s,t}}(a)\le H_{g_{s,t}}(a)
                 \quad\hbox{for every }a>0,\quad 0<t<t_* .       \tag{29}
\]

The inequalities are strict below the target density maximum. The
statement allows some zero label weights whenever (27) is still positive.
The required depth depends on the geometry, weights and variance.

Proof at variance one. Positivity of ell_infinity implies Gamma>0,
since Gamma=0 would make L identically zero. Let K=8 pi log(1/p_*),
T_0=max(1,2K/ell_infinity), and define

\[
 m=\min\{g_0e^{-6DT_0},\ell_\infty/2\}>0.
\]

Equations (5) and (28) give L(tau)>=m tau for every tau>0. In Theorem 3
take T=tau=tR, with t<=1. If B=480/nu and A_2=80MD+1920D/nu, then

\[
 E(R,tR)=\pi D\left(\frac{A_0+B\log R}{R}+A_2t\right).           \tag{30}
\]

Choose

\[
 R_0\ge\max\left\{2,4M,\frac{8\pi DA_0}{m},
                       \left(\frac{8\pi DB}{m}\right)^2\right\},
 \qquad 0<t\le\min\{1,m/(4\pi DA_2)\}.
\]

Then E(R,tR)<=m/2 for all R>=R_0, by log R<=sqrt R. Equations (2)-(3)
give strict positivity for every 0<a<=C_3 exp(-R_0^2/2). For all larger
thresholds, the positive-threshold-floor theorem in PROOF.md applies for
sufficiently small t, including critical levels and moving maxima.
Decreasing t_* to meet that theorem proves (29). General fixed s follows
by the scaling already stated after (11).

The finite map is a contraction by the distance calculation in PROOF.md.
Kirszbraun's extension theorem therefore supplies a 1-Lipschitz map on
all of R3 with these values. The weighted finite laws and their hinge
comparison consequently fit the bounded-measure formulation of the named
problem; the choice of extension away from their support is irrelevant.

The new point is the use of T=tR in the relative error estimate. A
fixed-T error statement alone could not close this unbounded-tau tail.

## 8. Strict positivity for an open asymmetric geometric class

Take the reference regular tetrahedron

\[
 v_0=(1,1,1),\ v_1=(1,-1,-1),\
 v_2=(-1,1,-1),\ v_3=(-1,-1,1),\qquad d_i=v_i.
\]

Assume every one of the sixteen label weights is positive. Hence every
tip is occupied and A_j={0,d_i:i!=j}. Each C_j is the intersection of
S2 with the cone generated by -d_i, i!=j. Write
theta=-sum_(i!=j) c_i d_i with c_i>=0 and S=sum c_i. Then
d_i.theta=S-4c_i. If the three coefficients, in decreasing order, are
x>=y>=z, the integrand in (27) is

\[
 (4x-S)-\max(0,S-4z)
 =\begin{cases}2(x-y+z),&S-4z\ge0,\\4x-S,&S-4z<0.\end{cases}    \tag{31}
\]

It is nonnegative everywhere and positive in the interior of C_j.
At theta_j=v_j/sqrt(3) it equals 1/sqrt(3). The difference of two
support functions is 2 sqrt(3)-Lipschitz on the sphere, so it is at least
1/(2 sqrt(3)) on the chordal cap |theta-theta_j|<=1/12. That cap lies
inside C_j: theta_j.(v_k-v_j)=-4/sqrt(3) for k!=j, while its variation
on the cap is at most sqrt(8)/12. A chordal cap of radius r on S2 has
area pi r^2. Since the rest of each integrand is nonnegative, summing
the four caps proves

\[
              \ell_\infty^{\rm reg}\ge\frac{\pi}{72\sqrt3}>0.    \tag{32}
\]

This is independent of how the sixteen positive weights are distributed.

Here is a quantitative perturbation estimate, retaining full label
support. Suppose the new valid tetrahedral geometry v_j',d_i' satisfies

\[
 \max_j|v_j'-v_j|\le\eta,\qquad
 \max_i|d_i'-d_i|\le\eta,\qquad 0\le\eta\le1.
\]

Where the dominant vertex stays the same, the integrand changes by at
most 2 eta. A changed dominant vertex requires
|(v_j-v_k).theta|<=2 eta for some reference edge. Since all reference
edge lengths exceed 2, the union of these six slabs has area at most
24 pi eta. On it the change in integrands is at most 10, using the
coarse bounds |d_i|<=2 and |d_i'|<=3. Therefore

\[
 |\ell_\infty'-\ell_\infty^{\rm reg}|\le248\pi\eta,
 \qquad \ell_\infty'>\pi(1/144-248\eta).                         \tag{33}
\]

Every valid geometric perturbation with eta<1/35712 consequently has
ell_infinity'>0. Theorem 6 proves **all-threshold Gaussian majorisation**
for sufficiently shallow flaps on this open geometric neighborhood, for
arbitrary positive weights and any fixed variance.

For a fully asymmetric rational example, let delta=10^-8, c_i=1+i delta,
and

\[
 A=\begin{pmatrix}1&\delta&0\\0&1+\delta&\delta\\
                  \delta&0&1+2\delta\end{pmatrix},\qquad
 v_i'=Av_i,\qquad d_i'=c_i A^{-T}v_i.                             \tag{34}
\]

The new normal heights are h_i'=4c_i>0. Since ||A-I||_op<3 delta,
Neumann's bound gives

\[
 |v_i'-v_i|<6\delta,\qquad
 |d_i'-d_i|<12\delta/(1-3\delta)\le13\delta.
\]

Thus eta=13/10^8 is admissible in (33), and its elementary rational
estimate, using pi>3, gives ell_infinity'>1/50. In edge order
01,02,03,12,13,23, the squared core distances are

\[
 8+32\delta+36\delta^2,\quad8+24\delta+40\delta^2,\quad
 8+16\delta+12\delta^2,\quad8+12\delta^2,\quad
 8+8\delta+8\delta^2,\quad8+16\delta+20\delta^2.
\]

They are all distinct, so even the core has no nonidentity Euclidean
symmetry. All sixteen-label flap configurations still have only the two
intermediate distance states in R5, by PROOF.md. Thus their full hinge
comparison at small depth is not obtained from an R5 motion of the full
map. For a concrete asymmetric law one may use label weights
1/136,2/136,...,16/136 in the order of verify.py; the theorem covers every
positive weight vector instead of just this control.

The exact checker verifies (31)'s linear coefficients and signs, the
rational perturbation bound, all six distance polynomials, invertibility,
normal duality and the vector perturbation inequalities for (34). It
does not mechanize the spherical integrations or Theorem 6.

The quantifier is: for each fixed variance and positive weighted geometry
in this class, sufficiently small depths satisfy every hinge. No common
positive depth for all variances has been proved. Consequently no new
Kneser--Poulsen volume consequence, unrestricted Gaussian theorem, or
solution for arbitrary indecomposable maps is claimed. The all-threshold
result uses (27)>0; the later SUPPORT_SIGN.md establishes its exact
strictness criterion for the full arbitrary-weight-support,
arbitrary-tetrahedron flap family.
