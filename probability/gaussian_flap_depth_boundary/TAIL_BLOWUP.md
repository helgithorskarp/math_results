# A strictly positive tail coefficient for asymmetric simplex flaps

Author proof, 26 September 2026; independent review pending. This supplies
sign information for the indecomposable flap maps in [PROOF.md](PROOF.md),
including arbitrary tetrahedra and asymmetric weights. It excludes a
specific joint depth/threshold regime. It does not prove full comparison
at positive depth, or the unrestricted dimension-three conjecture.

## 1. Statement and normalizations

Let v_0,...,v_3 be the vertices of a nondegenerate tetrahedron. Choose
positive h_i and set d_i=h_i grad(lambda_i), where lambda_i are its affine
barycentric coordinates. Thus

\[
 d_i\cdot(v_k-v_j)=h_i(\mathbf1_{k=i}-\mathbf1_{j=i}).                 \tag{1}
\]

Fix nonnegative weights alpha_j and beta_ij (i!=j), of total mass one.
The source and target laws at depth t>0 are

\[
 \mu_t^- =\sum_j\alpha_j\delta_{v_j}
       +\sum_{i\ne j}\beta_{ij}\delta_{v_j-td_i},\qquad
 \mu_t^+ =\sum_j\alpha_j\delta_{v_j}
       +\sum_{i\ne j}\beta_{ij}\delta_{v_j+td_i}.                    \tag{2}
\]

Write f_(s,t)=mu_t^-*gamma_s, g_(s,t)=mu_t^+*gamma_s, with covariance
s I_3, and D_(s,t)(a)=H_g(a)-H_f(a), where H_f(a)=integral (f-a)_+.
Set

\[
 w_j=\alpha_j+\sum_{i\ne j}\beta_{ij},\quad
 J=\{j:w_j>0\},\quad
 \Gamma_j=\sum_{i\ne j}h_i\beta_{ij}w_i,\quad
 \Gamma=\sum_j\Gamma_j.                                           \tag{3}
\]

As proved by the pair-distance identity in PROOF.md, Gamma=0 exactly
when the positive-weight endpoint configurations are congruent. This
includes zero label weights. The full sixteen-label map is indecomposable
even among intermediate configurations in R5; that geometric obstruction
does not itself decide the Gaussian sign.

For j in J, let C_j consist of directions theta in S^2 for which
v_j.theta is maximal among the occupied v_k. Any choice on ties is
equivalent for integration: ties lie in finitely many great circles.
Use **unnormalized spherical area** d sigma, of total mass 4 pi. Define

\[
 W_j^\pm(\theta,\tau)
    =\alpha_j+\sum_{i\ne j}\beta_{ij}e^{\pm\tau d_i\cdot\theta},\qquad
 L_j(\tau)=\int_{C_j}\log\frac{W_j^-(\theta,\tau)}
                              {W_j^+(\theta,\tau)}\,d\sigma,
 \qquad L(\tau)=\sum_{j\in J}L_j(\tau).                            \tag{4}
\]

Every logarithm has a positive argument. Empty-tip terms are omitted.

**Theorem 1 (tail limit).** Fix the geometry, weights and s>0. For tau>0,
put

\[
 R_{\rm phys}=s\tau/t,\qquad
 a(t,\tau)=(2\pi s)^{-3/2}e^{-s\tau^2/(2t^2)}.
\]

Then, as t decreases to zero,

\[
 \frac{D_{s,t}(a(t,\tau))}{a(t,\tau)sR_{\rm phys}}
       \longrightarrow L(\tau).                                  \tag{5}
\]

Convergence is uniform for tau in every compact subinterval of (0,infinity).
The coefficient L is independent of s.

**Theorem 2 (quantitative strict sign).** L_j(tau)>=0 for every j in J
and tau>0, with equality if and only if Gamma_j=0. In particular

\[
                 L(\tau)>0\quad\Longleftrightarrow\quad\Gamma>0.   \tag{6}
\]

Here is an explicit lower bound. Choose V>=max_k |v_k| and
D>=max_k |d_k|, and put M=V+D. For each ordered pair i!=j, let k,l be
the remaining two indices and choose positive bounds

\[
 E_{ij}\ge |v_i-v_j|,\quad
 B_{ij}\ge\max\{|v_i-v_k|,|v_i-v_l|\},\quad
 N_{ij}\ge|d_k+d_l|.
\]

Define delta_ij=min(h_k,h_l)/N_ij and
rho_ij=min(1/4,delta_ij/(8 B_ij)). Then

\[
 L_j(\tau)\ \ge
 \tau e^{-3(2+M^2)-6D\tau}
       \sum_{i\ne j}\frac{h_i w_i\beta_{ij}\rho_{ij}^3}{24 E_{ij}}.
                                                                    \tag{7}
\]

Thus L(tau)>=c_G Gamma tau exp(-3(2+M^2)-6D tau), where
c_G=min_(i!=j) rho_ij^3/(24 E_ij)>0 depends only on the geometry and
the chosen bounds. This coefficient bound holds for all weights, although
the limiting approximation (5) is only asserted for fixed weights.

**Corollary (excluded scaling windows).** If Gamma>0, fix s>0 and
0<tau_0<=tau_1<infinity. There is t_*>0 such that

\[
 D_{s,t}(a(t,\tau))>0
       \quad(0<t<t_*,\ \tau_0\le\tau\le\tau_1).                   \tag{8}
\]

The assertion is strict for these very small positive levels. No effective
t_* is claimed. This extends the positive-threshold-floor exclusion in
PROOF.md, but does not join it uniformly to all thresholds.

## 2. Outer level radii and proof of the limit

First take covariance one, write t=tau/R, and let
a=(2 pi)^(-3/2) exp(-R^2/2). All centers lie in a fixed ball of radius M
for R sufficiently large, uniformly on a compact tau interval. On each
ray theta, either density is at least a for r<=R-M and is less than a
for r>R+M. For r>M its radial logarithmic derivative is

\[
       -r+\theta\cdot\sum_b\pi_b(r\theta)c_b,                     \tag{9}
\]

where pi_b are posterior label probabilities and c_b the centers.
Its value is between -r-M and -r+M. For R>2M the positive superlevel
set therefore has a unique outer radius r_-(theta) or r_+(theta), and
is precisely the radial interval from zero to that radius. Both radii
belong to [R-M,R+M]. In particular these far-tail levels are regular.

Away from fan walls, let j be the uniquely dominant occupied tip, and
write h=v_j.theta (only in this paragraph; h_i still denotes (1)).
The other tips' contributions are exponentially small in R. At r=R+O(1),
the factors from the offsets within tip j converge, uniformly on compact
tau intervals, to W_j^pm(theta,tau). The exact exponent from an offset
epsilon tau d_i/R, epsilon in {-1,+1}, is

\[
 \epsilon(r\tau/R)d_i\cdot\theta
 -\epsilon(\tau/R)v_j\cdot d_i
 -\tau^2|d_i|^2/(2R^2).
\]

Consequently the level equation gives

\[
 r_\pm=R+h+
   \frac{h^2-|v_j|^2+2\log W_j^\pm(\theta,\tau)}{2R}
   +o(R^{-1}),\qquad
 R(r_--r_+)\longrightarrow\log(W_j^-/W_j^+).                      \tag{10}
\]

To justify integration through fan walls, compare matching source and
target labels at the same x=r theta. Their Gaussian logarithmic density
ratio has absolute value at most 2 tau D(r+V)/R. The same bounds hold
for the ratio of the mixtures because their weights agree. Applying (9)
between the two outer radii proves

\[
             |r_--r_+|\le C\tau/R,                              \tag{11}
\]

for a constant independent of theta and large R, uniformly on compact
tau intervals. Since radial volume is (1/3)integral r^3 d sigma,
dominated convergence applied to (10)-(11) yields

\[
       \frac{V_f(a)-V_g(a)}R\longrightarrow L(\tau).              \tag{12}
\]

This convergence is uniform in tau: discard a small angular neighborhood
of the finitely many walls, use uniform tip dominance on its complement,
and then use the uniform bound (11) on the discarded neighborhood.
The weights are fixed, so the positive w_j have a positive minimum.

It remains to control the exterior mass, which is of the same order as
the desired normalization. For either density P and its outer radius r,
write Q_theta=integral_r^infinity P(ell theta) ell^2 d ell. Substitute
u=(ell^2-r^2)/2 and use the posterior weights at r theta to obtain exactly

\[
 \frac{Q_\theta}a
  =r\int_0^\infty e^{-u}\sqrt{1+2u/r^2}\,J(u)\,du,\qquad
 e^{-Mu/r}\le J(u)\le e^{Mu/r}.                                  \tag{13}
\]

For example J(u)=sum_b pi_b(r theta)
exp((sqrt(r^2+2u)-r) theta.c_b); its bound follows from
sqrt(r^2+2u)-r<=u/r. Dominated convergence gives
Q_theta/(aR)->1 uniformly in theta and compact tau intervals. Hence
both complete exterior masses divided by aR converge to 4 pi, and their
difference divided by aR converges to zero. Since

\[
 H_P(a)=1-Q_P(a)-aV_P(a),\qquad
 D(a)=Q_f(a)-Q_g(a)+a(V_f(a)-V_g(a)),                              \tag{14}
\]

equations (12)-(14) prove (5) for s=1.

For general s use x=sqrt(s) y. The standardized centers are
v_j/sqrt(s) +/- tau d_i/R, where R=sqrt(s) tau/t. Scaling all base
vertices by the same positive factor leaves their normal fan unchanged.
The standardized level is a_std=s^(3/2) a, and
a_std R=a s R_phys. The argument above applies verbatim, including
uniform convergence on compact tau intervals, and gives (5).

## 3. Isolating a tip gives an established five-dimensional motion

For each j in J form an **isolated packet**: keep the masses alpha_j
at v_j and beta_ij at v_j +/- t d_i, but replace all mass at every other
tip k by a single core atom of weight w_k at v_k. The base law and its
occupied tips stay unchanged. Its only nonzero term in (4) is L_j.
This is a device for identifying the leading coefficient. It is not a
decomposition of the original positive-depth hinge into packet hinges.

Translate v_j to the origin and let K_j be the simplicial cone generated
by d_i, i!=j. Any three of the normals are independent. Equation (1)
shows that every fixed vector v_k-v_j belongs to the positive dual K_j^*.
The isolated packet therefore lies in the **simplicial-cone reflection**
class: fix the dual cone and send -b to b for b in K_j. We use the explicit
motion from the shared
[simplicial-cone proof](../gaussian_simplicial_cone_reflections/PROOF.md),
Theorem A and Sections 2-3 (graph 6042).

Precisely, it supplies a piecewise smooth family of linear isometries
F_u:R3 -> R5, with F_0=-I and F_1=I, for which

\[
 P_{\mathbb R^3}F_u d_i=c_i(u)d_i,\quad
 c_i'(u)\ge0,\quad c_i(0)=-1,\quad c_i(1)=1.                     \tag{15}
\]

For clarity, this input is an explicit smooth motion, not an assumed
rectifiable lift of an arbitrary Gram path. On a basis b_1,b_2,b_3,
put H=span(b_2,b_3), let P project onto H, choose an isometry J:H->R2,
and set eta=|(I-P)b_1|/|b_1|. If 0<eta<1, with -1<=lambda<=1,

\[
\begin{split}
 F_\lambda b_1&=\left(\frac{\lambda+\eta}{1+\eta\lambda}b_1,
       \frac{\sqrt{1-\lambda^2}}{1+\eta\lambda}JPb_1\right),\\
 F_\lambda b_r&=(\lambda b_r,\sqrt{1-\lambda^2}Jb_r),\quad r=2,3.
\end{split}                                                       \tag{16}
\]

The first coefficient's derivative is (1-eta^2)/(1+eta lambda)^2>0.
The two polynomial Gram identities are
(lambda+eta)^2+(1-eta^2)(1-lambda^2)=(1+eta lambda)^2 and
lambda(lambda+eta)+(1-lambda^2)=1+eta lambda.
Take lambda=-cos(pi u) for smooth endpoints. If eta=1, first rotate
b_1 from its negative to its positive using one auxiliary coordinate,
with b_2,b_3 fixed negative; then rotate their plane using both auxiliary
coordinates, with b_1 fixed positive. Orthogonality makes both stages
isometric and all three physical coefficients nondecreasing. This proves
(15), including the exceptional case, and integral c_i'(u) du=2.

The known full Gaussian comparison for each isolated packet already
implies L_j>=0 via (5). A limit of strict inequalities, however, need not
be strict. The following argument proves the quantitative assertion (7).

## 4. A positive contribution from a thin angular band

Work at covariance one. Put t=tau/R and a=C_3 exp(-R^2/2), where
C_n=(2 pi)^(-n/2). Use (15) on the isolated packet. At time u its moving
centers are v_j+tF_u d_i with weights beta_ij; its fixed centers are v_j
with weight alpha_j and v_k with weights w_k, k!=j. Let P_u be its R5
Gaussian density, and let U_u be the posterior average of the center
velocities. Direct differentiation gives the continuity equation and
divergence identity

\[
 \partial_u P_u=-\operatorname{div}(P_uU_u),\qquad
 \operatorname{div}U_u
  =-t\sum_{i\ne j}h_i c_i'(u)\pi_{\mathrm{core},i}
                                      \pi_{\mathrm{move},i}.      \tag{17}
\]

Indeed the general divergence is the sum over unordered label pairs
of pi_b pi_c (dot c_b-dot c_c).(c_b-c_c). Rigid/rigid pairs contribute
zero. A moving i and a fixed k contribute
-t h_i c_i'(u) 1_(k=i), by (1) and (15).

For a fixed density level q define K_u(q)=integral_{P_u>q} P_u.
At the far-tail regular levels used below, differentiation of the moving
domain, followed by the divergence theorem, gives

\[
 \frac{d}{du}K_u(q)
 =-q^2\int_{P_u=q}\frac{\operatorname{div}U_u}{|\nabla P_u|}\,dS
 =qt\sum_{i\ne j}h_i c_i'(u)
    \int_{P_u=q}\frac{\pi_{\mathrm{core},i}\pi_{\mathrm{move},i}}
                       {|\nabla\log P_u|}\,dS.                  \tag{18}
\]

For completeness, the integral of partial_u P_u over the domain is
-q integral U_u.n. The moving-boundary term is
q integral partial_u P_u/|grad P_u|. Substitution of (17) cancels the
U_u.n terms and leaves (18). Each smooth motion stage is sufficient;
integrate over the stages and telescope at their common endpoints.

At the endpoints P_u factors as f or g times gamma_1^(2). If Z has
that two-dimensional Gaussian law, gamma_1^(2)(Z)/C_2 is uniform on (0,1).
It follows directly that

\[
 K_0(C_2a)=H_f(a),\qquad K_1(C_2a)=H_g(a).                         \tag{19}
\]

This two-coordinate cancellation is prior work, also used in the shared
cone proof. We apply (18) at q=C_2 a=C_5 exp(-R^2/2).

Fix i!=j and let k,l be the other indices. Use the bounds in Theorem 2,
and temporarily suppress their ij subscripts. In physical R3 set

\[
 e=\frac{v_i-v_j}{|v_i-v_j|},\qquad
 \theta_0=-\frac{d_k+d_l}{|d_k+d_l|}.
\]

The denominator in theta_0 is nonzero, e.theta_0=0, and
(v_i-v_k).theta_0=h_k/|d_k+d_l|>=delta,
with the analogous inequality for l. Regard e,theta_0 as vectors in R5.
On the three-sphere S3 in e-perp, take the patch

\[
 A=\{\sqrt{1-|y|^2}\,\theta_0+y:
            y\perp e,\ y\perp\theta_0,\ |y|\le\rho\}.
\]

Its area is at least the Euclidean three-ball volume
A_0=4 pi rho^3/3. Points z of this patch satisfy |z-theta_0|<=2 rho,
so both gaps (v_i-v_k).z and (v_i-v_l).z are at least 3 delta/4.
Extend it to a band on S4:

\[
       \theta=z\cos b+e\sin b,\qquad |b|\le1/(R E).              \tag{20}
\]

For R E>=4 and R>=8 B/(delta E), the band has area at least
A_0/(R E), because its area element is cos^3(b) db d sigma_3(z)
and cos^3(b)>=1/2. Throughout it

\[
 |(v_i-v_j)\cdot\theta|\le1/R,\qquad
 (v_i-v_k)\cdot\theta,\ (v_i-v_l)\cdot\theta\ge\delta/2.           \tag{21}
\]

For the second assertion use cos b>=7/8 and
B |sin b|<=delta/8. These estimates also cover zero weights on either
of the other vertices; the same band still works.

Every center of P_u has norm at most M once t<=1. Its q-level surface
is a radial graph with r in [R-M,R+M], by the argument of Section 2
in dimension five. For R>=2M, |grad log P_u|<=r+M<=2R. Put C_0=2+M^2.
On the band, every individual Gaussian component divided by the
component centered at v_i is at most exp(C_0+2D tau): (21) bounds its
base projection by 1/R, each moving displacement has length at most tD,
and the difference of squared center norms contributes at most M^2/2.
The selected component at v_j+tF_u d_i has the lower bound
exp(-C_0-2D tau) on the same ratio. Therefore

\[
 \pi_{\mathrm{core},i}\ge w_i e^{-C_0-2D\tau},\qquad
 \pi_{\mathrm{move},i}\ge\beta_{ij}e^{-2C_0-4D\tau},\qquad
 \pi_{\mathrm{core},i}\pi_{\mathrm{move},i}
       \ge w_i\beta_{ij}e^{-3C_0-6D\tau}.                         \tag{22}
\]

These estimates are uniform over the motion. The radial surface element
is at least r^4 times angular area. Restricting the nonnegative integral
in (18) to (20) gives

\[
 \int_{P_u=q}\frac{\pi_{\mathrm{core},i}\pi_{\mathrm{move},i}}
                       {|\nabla\log P_u|}\,dS
 \ge w_i\beta_{ij}e^{-3C_0-6D\tau}\frac{A_0 R^2}{32E}.             \tag{23}
\]

Here (R/2)^4/(2R) times A_0/(R E)=A_0 R^2/(32 E).
Each i-term has its own band. Their bands need not be disjoint, since
they bound distinct nonnegative summands of (18). Integrate (18), use
integral c_i'=2, then use (19) and divide by aR. The result for this
isolated packet is

\[
 \frac{H_g(a)-H_f(a)}{aR}
 \ge\tau e^{-3C_0-6D\tau}
       \sum_{i\ne j}\frac{h_i w_i\beta_{ij}\rho_{ij}^3}{24E_{ij}}.
                                                                    \tag{24}
\]

The numerical factor is C_2(4 pi/3)/16=1/24. The restrictions on R
are finite for each fixed tau (include R>=tau and R>2M), so taking
R to infinity in (24) and applying Theorem 1 proves (7).

If Gamma_j>0, at least one summand of (7) is positive. If Gamma_j=0,
every positive-weight moving/fixed pair in the isolated packet preserves
its distance; all its other pairs are rigid automatically. Its endpoint
weighted configurations are therefore congruent, and its hinges are
identical. Equation (5) gives L_j=0. This proves Theorem 2 in full.

Finally L is continuous in tau on (0,infinity), as follows directly from
(4) and positive weights on occupied tips. Its positive minimum on any
compact tau interval, together with the uniform limit (5), proves (8).

## 5. Exact controls and limitations

For the asymmetric fixture in PROOF.md, take
v=((0,0,0),(2,0,0),(1,3,0),(1,1,4)), h=(1,2,3,5), and put mass 1/16
on every label. Then w_i=1/4. For j=0,i=1 one may choose
V=5,D=2,M=7,E_10=2,B_10=5,N_10=2. These give delta=3/2 and rho=3/80.
The single indicated term in (7) is

\[
          L_0(\tau)\ge\frac9{262144000}\,
                           \tau e^{-153-12\tau}>0.               \tag{25}
\]

An independent analytic normalization control uses the right tetrahedron
v_0=0,v_1=e_1,v_2=e_2,v_3=e_3, h_i=1. Put beta_10=1/4 and
alpha_1=alpha_2=alpha_3=1/4, with all other label weights zero.
Only L_0 is nonzero; C_0 is the negative octant on S2 and
log(W_0^-/W_0^+)=-2 tau theta_1. Since the integral of theta_1 over
this octant is -pi/4 (orthogonal projection onto a quarter unit disk),

\[
                            L(\tau)=\pi\tau/2.                  \tag{26}
\]

This fixes the unnormalized area factor and sign without numerical
quadrature. A zero-Gamma control with alpha_0=beta_20=1/2 is mapped
by point reflection about v_0 and has L=0.

[verify_tail.py](verify_tail.py) checks rational geometric inequalities,
the universal polynomial identities behind (16), the coefficient (25),
the weights/linear integrand in (26), and the exact isometry control.
It does not verify analytic differentiation, integration, or limits.
Those remain written-proof obligations, not computer certificates.

The result is restricted to the classical flap family, even though its
full positive-label geometry has no R5 motion. The isolated packets have
R5 motions; their limiting coefficients add, but their actual hinges do
not. Uniform approximation as tau->0 or tau->infinity, as weights vanish,
or across unrestricted variances has not been proved. No all-threshold
positive-depth result, counterexample, or new Kneser--Poulsen consequence
is claimed. See [SOURCES.md](SOURCES.md) for the upstream dependencies.
