# Positive polynomial reconstruction of the Gaussian hinge gap

Author proof, 27 September 2026; unformalized and pending independent review.
The unrestricted dimension-three Gaussian-majorisation problem remains open.
This is a quantitative advance for the R2/R3/R8 certification spine, not a
new positive map class. The Jackson operator itself is classical; see
[SOURCES.md](SOURCES.md).

## 1. Uniform reconstruction, and the sign still needed

Let mu be supported in B(a,R) in R^3, let T be 1-Lipschitz, and let s>0.
Translate the two laws separately by a and T(a), and write

    epsilon=R^2/s, rho=R/sqrt(s), C=(2pi s)^(-3/2),
    f=mu*gamma_s, g=T#mu*gamma_s,
    H(u)=integral(g-Cu)_+-integral(f-Cu)_+,       0<=u<=1,
    d=E[|X-X'|^2-|TX-TX'|^2]/s.

The sign favorable to majorisation is H>=0. Both endpoints of H vanish.
Define ordinary moments a_r=integral_0^1 u^r H(u)du. These are the existing
Gaussian replica moments, not additional observables. For every integer
p>=2, Section 3 gives an explicit rational linear map from a_0,...,a_M to
a polynomial J_p H of degree at most M=2p-2.

**Theorem 1.** This map is a positive, constant-preserving averaging operator
on continuous functions on[0,1]. At every bounded radius,

    ||J_p H-H||_infinity <= 6 A_rho/p,
    A_rho=(rho+2)^3.                                      (1)

If 0<epsilon<=1/2, there is additionally a bound proportional to loss:

    ||J_p H-H||_infinity <= 6 d L_epsilon/p.                (2)

An explicit L_epsilon is as follows. Set

    kappa=1-epsilon, c=4sqrt(2epsilon/kappa), w=c+sqrt(5),
    P(q)=8+(7+epsilon/(2kappa))q+5q^2/4,
    L_epsilon=exp(5epsilon+c^2/2) P(cw)(2w^3+3w)
                  /[48sqrt(pi)kappa^3].                  (3)

The smaller of the bounds in(1),(2) may be used. When d=0, H is identically
zero; division by d is neither needed nor defined. R=0 is also trivial.
There is no atom-number bound, minimum mass or covariance hypothesis.
The relative estimate(2) retains the accepted epsilon<=1/2 hypothesis;
only(1) is an all-radius assertion.

Put Delta=max(-H)_+ and D_p=max(-J_p H)_+. Positivity of the operator gives

    D_p <= Delta <= D_p + 6 A_rho/p,                       (4)

and the last error may be replaced by6dL_epsilon/p in its stated range.
Thus the moment degree for uniform defect resolution is linear in inverse
tolerance. This improves the earlier sufficient Bernstein--Durrmeyer
degree of fourth order in inverse tolerance. It does not assert that the
new finite polynomials have nonnegative sign for arbitrary contractions.
Different p need not give monotone D_p; running maxima preserve(4).

For an exact zero certificate, retain original-law endpoint signs on
[0,a] and[b,1]. A verified polynomial lower bound J_p H>=E on[a,b],
where E is a valid reconstruction error, signs the remaining interval.
With moment enclosures, add their propagated error from Section 5 to E.
This covers a whole interval, including between test points. It does not
transfer endpoint equality through a positive error.

## 2. Angular regularity: every radius and retained loss

Define F(theta)=H((1+cos(theta))/2), 0<=theta<=pi. We prove that it is
Lipschitz with constant A_rho, and with dL_epsilon when epsilon<=1/2.

For a single Gaussian mixture h with centers in B(0,R), the set h>Cu lies
in B(0,R+sqrt(2s log(1/u))). Its positive levels have finite volume. The
layer-cake formula makes its hinge locally absolutely continuous in u,
with derivative -C times that volume almost everywhere. Hence, putting
ell=log(1/u),

    |H'(u)| <= sqrt(2)/(3sqrt(pi)) (rho+sqrt(2ell))^3.       (5)

There is no factor two: the two nonnegative volumes each have this same
upper bound, so their difference does too. The possible critical values
do not affect this almost-everywhere argument. Since |du/dtheta| is
sqrt(u(1-u))<=exp(-ell/2),

    |F'(theta)| <= sqrt(2)/(3sqrt(pi))
                    [exp(-ell/6)(rho+sqrt(2ell))]^3
                 <= (rho+2)^3.

Here sup_(ell>=0) exp(-ell/6)sqrt(2ell)=sqrt(6/e)<2 and the leading
constant is less than1. Local absolute continuity and the endpoint
continuity of H extend this to the closed interval. No convexity of
Gaussian-mixture level sets is required in this all-radius argument.

For the relative assertion use the accepted
[loss-dependent modulus, Theorem 2 and equation7](../gaussian_loss_normalized_hinges/PROOF.md),
with its [independent acceptance](../gaussian_loss_normalized_hinges_review_frontier/REVIEW.md).
It gives Phi(ell)=exp(ell)H(exp(-ell)) and

    |Phi'(ell)| <= d exp(5epsilon+c sqrt(ell)) P(c sqrt(ell))
                         sqrt(ell)/[16sqrt(pi)kappa^3],
    |Phi(ell)| <= d exp(5epsilon+c sqrt(ell)) P(c sqrt(ell))
                         ell^(3/2)/[24sqrt(pi)kappa^3].

The identity H'(u)=Phi(ell)-Phi'(ell), with r=sqrt(ell), therefore gives

    |F'(theta)| <= d exp(5epsilon)/(48sqrt(pi)kappa^3)
             exp(-r^2/2+cr) P(cr)(2r^3+3r).                (6)

Every coefficient of the last polynomial in r is nonnegative and its
degrees are1,...,5. For 1<=j<=5 the maximum of
r^j exp(-r^2/2+cr) occurs at
r_j=(c+sqrt(c^2+4j))/2 <=c+sqrt(j)<=w. Its exponential factor is at most
exp(c^2/2). Bounding each monomial separately in(6) proves(3).
The same closed-interval argument proves the relative angular Lipschitz
bound. This derives a new weighted derivative consequence of the accepted
modulus; it does not extend the coarea proof to nonconvex level sets.

## 3. A positive rational polynomial using ordinary moments

Let T_p be the Chebyshev polynomial and P_j the Legendre polynomial,
normalized by T_p(1)=P_j(1)=1. Define

    A_p(t)=(1-T_p(t))/(1-t),
    K_p(t)=A_p(t)^2,       I_p=(1/2) integral_-1^1 K_p(t)dt.

The quotient is a polynomial of degree p-1, with A_p(1)=p^2.
For normalized area measure sigma on S^2, define the spherical operator

    (mathcal J_p G)(omega)=I_p^(-1)
                           integral_S2 K_p(omega.nu)G(nu)d sigma(nu).

It is positive, preserves constants, and has polynomial degree at most M.
Apply it to the zonal function G(nu)=H((1+nu_3)/2). Rotation invariance
gives a polynomial in omega_3, denoted J_p H((1+omega_3)/2).

For completely explicit coefficients set

    k_j=(1/2) integral_-1^1 K_p(t)P_j(t)dt,
    c_(j,r)=(-1)^(j+r) binom(j,r) binom(j+r,r),
    h_j=sum_(r=0)^j c_(j,r) a_r.

Then

    J_p H(u)=sum_(j=0)^M (2j+1)(k_j/I_p)h_j P_j(2u-1).     (7)

All coefficients multiplying the a_r are rational. Indeed
P_j(2u-1)=sum_r c_(j,r)u^r. The spherical addition formula gives
the azimuth average of P_j(omega.nu) as
P_j(omega_3)P_j(nu_3); normalized latitude measure is du. Expanding K_p
in Legendre polynomials proves(7). The companion checker independently
integrates powers of the azimuth coordinate to verify this normalization
in finite cases. No weighted moments or replica integrals of noninteger
order are required.

Here is a self-contained error constant. If theta is the spherical angle,

    K_p(cos(theta))=[sin(p theta/2)/sin(theta/2)]^4,
    I_p >= p^2,
    (1/(2I_p)) integral_0^pi theta K_p(cos(theta))sin(theta)dtheta
                      <=6/p.                             (8)

To prove the middle inequality, expand A_p in Legendre polynomials and
use Cauchy--Schwarz at t=1 with the measure dt/2. The squared norm of
endpoint evaluation on degree at most p-1 is
sum_(j=0)^(p-1)(2j+1)=p^2. Since A_p(1)=p^2, I_p>=p^2.

For the last inequality split at a=2/p<=1. On[0,a],
|sin(p theta/2)|<=p sin(theta/2), so K_p<=p^4; the contribution to the
unnormalized first moment is at most p^4 a^3/6=4p/3.
On[a,pi], bound the numerator sine by1. Direct integration gives

    (1/2) integral_a^pi theta sin(theta)/sin(theta/2)^4 dtheta
       = a csc(a/2)^2 - pi +2cot(a/2)
       <= [4(24/23)^2+4]/a.

We used sin(a/2)>=(23/24)(a/2), from the cubic sine bound on[0,1/2],
and cot(a/2)<=2/a. Thus the total is at most
p[4/3+2(24/23)^2+2]<6p. This proves(8).

The polar-angle function is1-Lipschitz for spherical geodesic distance.
Section 2 therefore makes G Lipschitz on S^2 with the same constant.
Average |G(nu)-G(omega)| using(8) to prove(1),(2).
Because a positive average of H is never below min H, the first inequality
of(4) has no error term. The other follows from uniform approximation.

An optional sharper rational cost is available without angular quadrature.
Expand K_p(1-2x)=sum_r v_r x^r. Since
2arcsin(sqrt(x))<=pi sqrt(x)<=22sqrt(x)/7,

    beta_p=min(6/p, (22/(7I_p)) sum_r v_r/(r+3/2))          (9)

is another upper bound for the angular first moment. Thus replace6/p by
beta_p throughout. The signed sum in(9) is integrated exactly; termwise
rounding of its highly cancelling coefficients is not safe.

## 4. Loss-proportional cubature with a smaller sufficient budget

Use R3's [loss-proportional paired cubature](../gaussian_prior_localization/LOSS_CUBATURE.md),
independently [accepted here](../gaussian_loss_cubature_review2/REVIEW.md).
For q>=2 it supplies a law nu on at most

    M_q=2 binom(2q+3,3)-1

original source/image pairs, matching both marginal moment lists through
coordinate degree2q and preserving d exactly. Its signed Taylor remainder
gives, for each r>=0,

    |a_r(mu)-a_r(nu)| <= d e_r,
    e_r=[((r+2)epsilon/2)^q]/[4(r+2)^2 q!].                (10)

The slight weakening from the source's power5/2 to2 makes e_r rational.
Combining(7),(10) and |P_j|<=1 proves

    ||J_p H_mu-J_p H_nu||_infinity <= d B_(p,q),
    B_(p,q)=sum_(j=0)^M (2j+1)|k_j|/I_p
                         sum_(r=0)^j |c_(j,r)| e_r.        (11)

This bound holds at every radius. Consequently

    ||H_mu-H_nu||_infinity <= 12 A_rho/p + d B_(p,q)        (12)

at every radius, and if epsilon<=1/2,

    ||H_mu-H_nu||_infinity <= d[12 L_epsilon/p+B_(p,q)].     (13)

These cover the entire threshold interval. In(12), d<=2epsilon can be
used for an absolute tolerance. The older direct total-variation cubature
can have a better absolute atom budget; no improvement over that different
absolute method is claimed. The advance in(13) concerns retained loss.

There is an elementary uniform schedule. Since |k_j|<=I_p and
sum_r|c_(j,r)|=P_j(3)<=6^j, one has

    B_(p,q) <= (M+1)^2 6^M [((M+2)epsilon/2)^q]/(16q!).     (14)

For P_j(3)<=6^j, for example, use the usual integral formula
P_j(3)=pi^(-1)integral_0^pi(3+sqrt(8)cos(theta))^j dtheta
and 3+sqrt(8)<6. Also sum_(j=0)^M(2j+1)=(M+1)^2.
If b is a nonnegative integer, it is sufficient to take

    q>=max(2,ceil(3(M+2)epsilon),
                 b+3M+2ceil(log2(M+1)))                   (15)

to have B_(p,q)<=2^-b. Indeed q!>=(q/e)^q, e<3, and the second
term force the factorial expression in(14) below2^-q.
Use exact(11) when the coarse schedule is too large. On
q>=max(2,ceil((M+2)epsilon/2)), its values decrease and
B_(p,q+1)<=((M+2)epsilon/[2(q+1)])B_(p,q).

Fix epsilon in(0,1/2] and let 0<zeta<=1. Taking

    p>=max(2,ceil(24 L_epsilon/zeta)), 2^-b<=zeta/2,

and then(15) gives ||H_mu-H_nu||<=d zeta. In particular a normalized
adverse margin2zeta survives with at least zeta. The sufficient atom
budget is O_epsilon(zeta^-3), because p=O_epsilon(zeta^-1) and
q=O_epsilon(zeta^-1). The earlier composition with the
Bernstein--Durrmeyer rate gives a sufficient O_epsilon(zeta^-12)
budget. Neither exponent is a lower bound; no optimality is asserted.
Both schedules are independent of how small positive d is.

This improvement is a bound on existence and certificate degree, not a
claim that constructing huge exact cubatures is practical. The original
sites and weights may be real. Ordinary rational rounding can change d
and is not covered by(13). An oracle for a diffuse law is still required
to construct its cubature effectively.

## 5. Exact enclosures and whole-interval tests

Suppose verified moment intervals have midpoints z_r and radii delta_r.
Form the rational polynomial P by replacing a_r by z_r in(7). Then

    ||P-J_p H||_infinity <= E_mom,
    E_mom=sum_j (2j+1)|k_j|/I_p sum_r |c_(j,r)|delta_r.      (16)

R2 can obtain these intervals from exact finite-atomic replica sums or
R3's moment-remainder mechanism; no floating-point sign is a premise.
The checker supplies a rational Bernstein subdivision verifier for a
proposed lower bound on P throughout[a,b]. If it verifies

    P>=6dL_epsilon/p+E_mom

in the relative regime (or the all-radius error from(1)), original-law
endpoint signs complete a zero-defect certificate. A failed subdivision
is inconclusive. Negative values also give certified failures once the
uniform error is exceeded; by positivity of J_p, an exactly negative
J_p H anywhere already proves H is negative somewhere without that extra
error. Approximate moments must still pay E_mom in this last test.

All conclusions remain fixed-variance statements. They supply neither
the currently missing unrestricted sign margin nor a Kneser--Poulsen
consequence. The only prior analytic input to the relative assertion is
the accepted loss-dependent modulus. The new spherical high-variance
transfer6376 is preserved but is not assumed in this proof.

## 6. Reproduction and trust boundary

[verify.py](verify.py) uses exact Fraction arithmetic for kernel construction,
azimuth integration, rational coefficient identities, moment-error budgets
and interval subdivision. It separately checks near-isometry Gaussian
moment enclosures and rejects deliberately damaged coefficient/interval
data. [EXPECTED.json](EXPECTED.json) records compact deterministic results.
No full Gaussian sign or exhaustive geometric cover is established by
these finite controls. The universal estimates in Sections2--4, the
classical spherical addition formula and R3 cubature existence are written
mathematics, not proof-assistant theorems. See [README.md](README.md) for
commands and limitations, and [SOURCES.md](SOURCES.md) for exact dependencies.
