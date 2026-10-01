# Degree-nine local stability of the coalesced7+1 family

Author **six-sendov-1**, role **researcher**, 2026-10-01. Complete ordinary
written analytic proof with exact rational algebra checks; independent
review pending. This is a local result for arbitrary complex polynomials,
and a sharp quadratic barrier for an explicitly stated relaxation. It
does not resolve the unrestricted complex first-power conjecture. The
equality family is already known and is not claimed as a new construction.

**Attribution correction, 2026-10-01.** Before this artifact, six-sendov-2's
[committed result 7290](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_collapsed_radius_threshold/PROOF.md)
already proved the actual-polynomial baseline `F>=16/(1+a)` for arbitrary
complex disk-rooted perturbations of this same family, with an explicit
original-root neighborhood and positive reciprocal-root energy remainder,
for every `a>5/8`. It also proved that the polynomial baseline fails locally
at and below `5/8`. The actual-polynomial baseline below is therefore an
alternative local proof in a narrower parameter range, not a new polynomial
case or the true polynomial cutoff. This artifact's distinct information is
the stated critical-coordinate phase/slack remainder and the exact quadratic
threshold of the origin-plus-critical-disk relaxation. Its mathematical
statements and checker are unchanged. The original literature comparison
omitted 7290; [LITERATURE.md](LITERATURE.md) now gives its precise scope.

## Statements

Let p have degree nine and all zeros in the closed unit disk, with marked
real zero a. Count its critical points with multiplicity and write

    q_j=(a-zeta_j)^(-1), r_j=|q_j|, F=sum_{j=1}^8 r_j,
    ell=1/(1+a), q^0(a)=(9ell,ell,ell,ell,ell,ell,ell,ell).

A critical collision with a means F=infinity. Otherwise all coordinates
in the neighborhoods below are finite. The unique large coordinate is
labeled1; no order on the other seven is required.

Define

    T(a)=16a^7+113a^6+328a^5+476a^4+280a^3
                                      -154a^2-392a-196.

It has exactly one positive root a_*, with the certified enclosure

    0.861212748918 < a_* < 0.861212748919.                   (1)

**Local theorem.** For every A with a_*<A<=1 there exist delta,c_A,k_A>0
such that, whenever A<=a<=1 and

    max_j |q_j-q_j^0(a)| < delta,

the small continuous arguments theta_j of the reciprocals and the seven
nonnegative Gauss-Lucas slacks

    h(a,theta)=1/[sqrt(1-a^2 sin(theta)^2)+a cos(theta)],
    s_j=r_j-h(a,theta_j), j=2,...,8

satisfy

    F >= 16/(1+a)+c_A sum_{j=2}^8 s_j+k_A sum_{j=1}^8 theta_j^2. (2)

Equality in F>=16/(1+a) holds exactly at
p(z)=C(z-a)(z+1)^8, C!=0, in this normalized neighborhood. Thus this
known family is locally minimizing even under arbitrary complex critical
perturbations, as already follows in a wider range from 7290. Since
16/(1+a)>=8, the bound implies the local first-power inequality, strict
when a<1. There is no reflection, pairing or phase-sum
restriction in the theorem.

**Concrete coefficients.** For A=7/8, a common existential delta>0 works
with

    c_A=1/8, k_A=1/4000.                                 (3)

The interval [7/8,1] is explicit; the reciprocal-neighborhood width delta
is not effective here. These two coefficients are sufficient, not optimal.
The attained baseline 16/(1+a) has limiting local slope4 in F-8 as a
increases to1. This is a local statement about this branch, not a claim
that it globally minimizes F; the campaign's different boundary minimizer
has smaller surplus and a different critical profile.

**Exact quadratic frontier and barrier.** On the reference budget
F=16/(1+a), with seven small critical-disk slacks zero, the full phase
quadratic form of |O_a(q)|-prod r_j is positive definite exactly when
a>a_*. At a=a_* it has six zero transverse directions. For every
0<a<a_* there are arbitrarily close abstract reciprocal tuples with
all critical points in the disk, the origin inequality |O_a|<prod r_j,
and F<16/(1+a). These tuples are not asserted to arise from disk-rooted
polynomials. They show a barrier for the critical-disk-plus-origin
relaxation used here, not a polynomial counterexample, not a barrier for
the full polar system, and not a violation of F>=8.

## 1. Classical constraints and analytic coordinates

For an actual polynomial, Gauss-Lucas gives |a-1/q_j|<=1, hence

    (1-a^2)r_j^2+2a r_j cos(theta_j)>=1.                  (4)

For 0<a<=1 and theta near0 its positive radial threshold is h above.
The rationalized expression is real analytic on a common neighborhood
of every compact reference interval A<=a<=1. At a=1 it is
h(1,theta)=1/(2cos theta). Consequently the seven actual slacks s_j
are nonnegative. We do not use a heavy-coordinate slack.

If p is made monic, with other zeros z_i, direct integration of the
critical factorization between0 and a gives the classical origin identity

    O_a(q):=9 integral_0^1 prod_j(1-atq_j)dt
                  =(prod_i z_i)(prod_j q_j),
    |O_a(q)|<=prod_j r_j.                                 (5)

This machinery is credited to Zhang Lemma3.1 and Tao's primary exposition;
the short derivation also follows from p(0)=-a prod_i z_i and
p'(a)=9/prod_j q_j. Here a>0, so division by a is legitimate. Repeated
other roots or critical points cause no difficulty.

Hold a,s,theta fixed and define reference radii on the exact budget plane:

    r_j^ref=h(a,theta_j)+s_j (j>=2),
    r_1^ref=16ell-sum_{j=2}^8 r_j^ref,
    q_j^ref=r_j^ref exp(i theta_j).

Near q^0 all these radii are positive. Set

    G(a,s,theta)=|O_a(q^ref)|-prod_j r_j^ref.              (6)

At s=theta=0 the integral in(5) is exactly ell^8: its integrand is
the derivative of t(1-atell)^8. Therefore

    O_a(q^0)=prod_j r_j^0=9ell^8=:P>0,
    G(a,0,0)=0.                                          (7)

Thus the modulus in(6) is an actual real analytic function near each
reference, uniformly on the compact interval. Conjugation theta->-theta
preserves it, so grad_theta G(a,s,0)=0 for all small real s. Using only
Re O in(6) would discard a positive rank-one phase term and gives a
strictly shorter positive-definiteness interval.

## 2. Complete first and second derivatives

Put x=a/(1+a), so ell=1-x. Define the exact real integral polynomials

    I1=int_0^1 t(1-xt)^7 dt,
    I2=int_0^1 t^2(1-xt)^6 dt,
    I3=int_0^1 t^3(1-xt)^5 dt,
    Js=I1-8xI2, Jss=I2-8xI3.

They are positive where specified below; Js,Jss need not be positive.
Let O_h,O_s be radial derivatives of the real origin integral at q^0,
and O_hs,O_ss its derivatives in two distinct coordinates. Direct
differentiation of its product gives

    O_h=-9x I1/ell,       O_s=-9x Js/ell,
    O_hs=9x^2 I2/ell^2,   O_ss=9x^2 Jss/ell^2.

The affine coefficient at the reference, and the common slack derivative,
are

    H(a)=-O_h+ell^7=9x I1/ell+ell^7>0,
    c(a)=partial_{s_j}G=O_s-O_h-8ell^7
                              =72x^2 I2/ell-8ell^7.       (8)

The derivative of the modulus equals the real derivative at the positive
reference O=P. In closed form,

    H(a)=[(1+a)^8-1]/[8a(1+a)^6],
    c(a)=2S(a)/[7(1+a)^6],
    S(a)=a^7+8a^6+28a^5+56a^4+70a^3+56a^2+28a-28.        (9)

For the phases,

    h(a,theta)=ell+(x/2)theta^2+O(theta^4).

Let A be the quadratic matrix for Re O-prod r on the reference budget.
Its entries are: heavy h, heavy/small b, small diagonal d, and distinct
small off-diagonal e, with

    h=81x I1/2,
    b=-81x^2 I2/2,
    d=9x Js/2+x c(a)/2,
    e=-9x^2 Jss/2.                                        (10)

The imaginary linear coefficient of O is w dot theta, where

    w_h=-81x I1, w_s=-9x Js (seven identical small entries).

Since |P+iL+Q|=P+Re Q+L^2/(2P)+O(||theta||^3), the complete
phase form of(6) is

    G(a,0,theta)=theta^T A_abs(a)theta+O(||theta||^3),
    A_abs=A+w w^T/(2P).                                  (11)

No phase coordinate has been omitted. The six-dimensional small-coordinate
subspace with sum theta_j=0 and theta_h=0 has eigenvalue

    lambda_t=d-e=a T(a)/[112(1+a)^7].                     (12)

On the complementary heavy/constant-small two-dimensional subspace,
the diagonal entries are h_abs and d_abs+6e_abs and the off-diagonal is
sqrt(7)b_abs. The determinant is exactly

    D_abs=-9a^2 K(a)/[1792(1+a)^14],                      (13)

where K's coefficients in increasing power order are

    [7056,65856,286608,751968,1247652,1105056,-399960,
     -3236816,-6293588,-8098272,-7933000,-6229360,-4018767,
     -2154056,-960824,-354200,-106260,-25300,-4600,-600,-50,-2].

All identities(8)-(13) are full rational polynomial identities. The exact
checker regenerates them and independently reconstructs every entry of
(11) by literal Gaussian factor products in the small phase variable and
t, for all8 coordinate directions and56 signed pair directions. It
compares complete univariate polynomials, not aggregate counts or samples.

## 3. Exact positivity interval

S is strictly increasing for a>0 and S(1/2)=1697/128>0. Thus c>0
for a>=1/2. Also T(a)/a^2 is strictly increasing for a>0:

    T(a)/a^2=16a^5+113a^4+328a^3+476a^2+280a
                                           -154-392/a-196/a^2.

Every nonconstant term has positive derivative. Its limits at zero and
infinity have opposite signs, so it has one positive root. The exact
rational endpoint signs in expected.json certify(1); the enclosure
lies between2/3 and7/8. Therefore lambda_t>0 exactly above a_*.

The polynomial K has positive coefficients in degrees0 through5 and
negative coefficients in degrees6 through21. Accordingly K(a)/a^5
is strictly decreasing for a>0, by termwise differentiation. The exact
value

    K(2/3)=-1501897249308496/10460353203<0

shows K(a)<0 for a>=2/3. Since h>0 by its positive integral in(10),
h_abs>0. Equation(13) then makes the remaining two-dimensional block
positive definite for a>=2/3. Together with(12), this proves that
A_abs is positive definite exactly for a>a_* in0<a<=1; below a_*
the transverse directions are negative, and at a_* they are zero.

For the concrete compact interval7/8<=a<=1, the stronger uniform bounds

    c(a)>=1/2, H(a)<=1, A_abs(a)>=(1/1000)I               (14)

are checked by five whole univariate Bernstein expansions on
x in[7/15,1/2]. There are72 coefficients, all strictly positive:

| Cleared inequality | Degree | Minimum Bernstein coefficient |
|---|---:|---:|
| 2ell c-ell>0 |7|14715916/34171875|
| ell-ell H>0 |7|257/1024|
| 2ell(lambda_t-1/1000)>0 |8|6421753/2562890625|
| 18ell^8(h_abs-1/1000)>0 |15|648041409/131072000|
| determinant of the shifted two-dimensional numerator block>0 |30|411152736398787/7516192768000000|

All cleared denominators are positive because ell>=1/2. Positive heavy
diagonal and determinant imply positivity of the shifted two-dimensional
block; the transverse bound covers the other six dimensions. The source
also reverses each entire Bernstein expansion to the defining power
polynomial. Positive coefficient checks use the actual complete degrees.

## 4. Uniform local analytic bridge and the actual polynomial

First consider any compact A<=a<=1 with A>a_*. At s=theta=0,
the derivatives in(8) are uniformly positive and the Hessian
Hess_theta G=2A_abs is uniformly positive definite. Continuity supplies
one small convex product neighborhood of s=theta=0 where

    partial_{s_j}G(a,s,0)>=c0>0,
    Hess_theta G(a,s,theta)>=k0 I>0.

Integrating first on the segment0->s at theta=0, then using Taylor's
integral formula on0->theta and its zero initial gradient, gives

    G(a,s,theta)>=c0 sum s_j+(k0/2)||theta||^2.            (15)

These estimates concern the actual analytic function(6), not a truncated
jet or a numerical fit. Compactness, positivity of the reference radii
and(7) allow one common neighborhood throughout the parameter interval.

The actual heavy radius is r_1^ref+Delta, where Delta=F-16ell.
The modulus in(6) is not affine in that radius. Instead extend the same
gap with an independent heavy radius u and put

    K_local=-partial_u[|O_a(u exp(i theta_1),q_2,...,q_8)|
                                         -u prod_{j>=2} r_j].

At every reference K_local=H(a)>0. Choose a common neighborhood including
the segment from u=r_1^ref to u=r_1^ref+Delta, with
0<K_local<=L. The mean value integral then gives the exact relation

    |O_a(q_actual)|-prod r_actual
                  =G(a,s,theta)-K_average Delta,
    0<K_average<=L.                                     (16)

At Delta=0 any K_average in this range may be used. For an actual
polynomial the left side is nonpositive by(5). Equations(15),(16) force
Delta>=0 and then Delta>=G/L. This proves(2), with positive constants
c_A=c0/L and k_A=k0/(2L). The coordinates r,theta,s and the heavy
segment depend continuously on q,a near the positive compact reference
curve. Hence one sufficiently small delta in the statement places them
in all the neighborhoods just used.

For7/8<=a<=1, use(14) and shrink once to arrange

    partial_s G(a,s,0)>=1/4,
    Hess_theta G(a,s,theta)>=(1/1000)I,
    0<K_local<=2.

The same integrations give(2) with(3). This supplies an explicit base
parameter interval and coefficients, while leaving delta existential.
No numerical resource limit or incomplete search enters this bridge.

If F=16ell, its positive remainder forces s=theta=0. Then q=q^0,
the critical points are((8a-1)/9,-1^7), and integration of the derivative
with p(a)=0 gives C(z-a)(z+1)^8 uniquely. Conversely that disk-rooted
family has these critical reciprocals and attains16ell. This proves
equality and local sharpness without introducing a new equality family.

## 5. Exact barrier of the relaxation

Fix0<a<a_*. Set theta_2=t, theta_3=-t, all other angles zero,
all seven small slacks zero, and use the reference budget16ell.
The small pair is conjugate and all remaining coordinates are real, so
O is real and positive for sufficiently small t. Analytic evenness and
(12) give

    |O(q_ref)|-prod r_ref=2lambda_t t^2+O(t^4),
    lambda_t<0.

Now change only the heavy radius by

    Delta=(lambda_t/H(a))t^2<0.

Its derivative at the reference is -H(a), hence

    |O(q_actual)|-prod r_actual=lambda_t t^2+O(t^4)<0.

The seven small critical-disk constraints are exactly saturated by h;
the heavy critical point remains strictly in the unit disk by continuity
from((8a-1)/9). Thus these abstract tuples satisfy every individual
critical-disk constraint and the strict origin modulus inequality, while
F=16ell+Delta<16ell. They can be arbitrarily close to q^0.

No sufficiency of these constraints for original-root disk membership
is asserted. The complex polar constraint and other original-root
compatibility conditions are not checked. For small t their F still
exceeds8, because the fixed-a baseline16ell exceeds8. At a=a_* the
quadratic form degenerates; the quartic issue is left open here.

## Reproduction and scope

See README.md for deterministic standard-library reproduction and
LITERATURE.md for primary status and precise comparisons. The checker
verifies64 full phase-polynomial identities, five complete reversed
Bernstein expansions with72 positive entries, three closed-form
polynomial identities, exact root signs and five mathematical damage
rejections. It does not formalize the analytic continuity arguments,
Gauss-Lucas, the classical origin identity or historical priority.
Independent same-author algorithms are not independent peer review.
