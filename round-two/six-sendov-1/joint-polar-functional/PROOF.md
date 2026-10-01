# A fixed origin-polar certificate for the coalesced critical-coordinate relaxation

Author **six-sendov-1**, role **researcher**, 2026-10-01. Complete ordinary
analytic proof with exact rational algebra; independent review of this joint
certificate is pending. The deliverable is a functional reduction, a single
explicit dual weight and quantitative phase/slack coefficients. The actual
polynomial baseline and its cutoff `5/8` were already proved in
[7290](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_collapsed_radius_threshold/PROOF.md).
They are credited, not presented as newly solved cases.

## 1. The relaxed domain and theorem

Put `a0=5/8`, `ell=1/(1+a)`, and `q0(a)=(9ell,ell,...,ell)` with seven
small coordinates. For complex nonzero `q_j=r_j exp(i theta_j)` close to
this positive vector, choose the small continuous arguments. Define

    O_a(q)=9 int_0^1 prod_j(1-atq_j) dt,
    C_a(q)=int_0^1 prod_j(a+(1-a^2)tq_j) dt,
    Q_a(q)=(|C_a(q)|-1)/(1-a^2),             a<1,
    Q_1(q)=(Re sum_j q_j-8)/2.

The normalized polar function has the stated real analytic extension at
`a=1`, proved below. The relaxed necessary constraints are

    |a-1/q_j|<=1  (j=1,...,8),
    |O_a(q)|<=prod_j r_j,
    Q_a(q)>=0.                                             (1)

No assertion that every tuple satisfying (1) comes from a disk-rooted
polynomial is made. The tuple theorem uses only these explicit conditions.

Set

    mu0=22096964222976/21378414915091,
    J_a(q)=|O_a(q)|-prod_j r_j-mu0 Q_a(q),
    h(a,theta)=1/[sqrt(1-a^2 sin(theta)^2)+a cos(theta)],
    s_j=r_j-h(a,theta_j), j=2,...,8.

**Functional reduction.** For every `a0<A<=1`, there is a common `delta_A>0`
such that `A<=a<=1`, `max_j|q_j-q0_j(a)|<delta_A` and (1) imply

    sum_j r_j >= 16/(1+a)
        +(a-5/8)[(1/8)sum_{j=2}^8 s_j
                        +(1/22500)sum_{j=1}^8 theta_j^2]. (2)

All seven slacks are nonnegative. Equality in the baseline in this
neighborhood holds exactly at `q=q0`. The coefficients in (2) are explicit
and sufficient; the common reciprocal width is existential, not effective.
The proof also establishes the following stronger reference-budget gap.
For small nonnegative `s` and small `theta`, put

    r_j^ref=h(a,theta_j)+s_j  (j>=2),
    r_1^ref=16ell-sum_{j=2}^8 r_j^ref,
    q_j^ref=r_j^ref exp(i theta_j),
    G(a,s,theta)=J_a(q^ref).

Uniformly on every compact interval `[A,1]` as above, a common product
neighborhood satisfies

    G(a,s,theta) >= (a-5/8)[(3/8)sum s_j
                                     +||theta||^2/7500].  (3)

**Sharp onset of the quadratic dual method.** For an arbitrary real weight
`mu`, write `G_mu` for the same reference function with `mu` in place of
`mu0`. For `0<a<5/8`, no real `mu` makes both its slack derivatives and
its six transverse phase eigenvalues nonnegative at the reference. At
`a=5/8` the only such weight is exactly `mu0`, and both quantities vanish.
For every `5/8<a<=1`, the fixed weight `mu0` makes the slack derivative
strictly positive and the full eight-dimensional phase matrix positive
definite. This is a sharp functional dual onset, not a new polynomial cutoff.
The degenerate endpoint is excluded from (2) and (3).

## 2. Analyticity and actual-polynomial applicability

The critical-disk inequality for a reciprocal is exactly

    (1-a^2)r^2+2ar cos(theta)>=1.

Its local positive radial threshold is `h`; the rationalized formula is
real analytic near `theta=0`, including `h(1,theta)=1/(2cos(theta))`.
The reference heavy critical point is `(8a-1)/9`, strictly interior for
`a0<=a<=1`; a small common neighborhood preserves that constraint.

At the model, the origin integrand is the derivative of `t(1-atell)^8`,
and the polar integrand is the derivative of `t(a+(1-a)t)^8`. Therefore

    O_a(q0)=P=9ell^8>0, C_a(q0)=1, G(a,0,0)=0.             (4)

Both moduli are real analytic near the compact reference curve. For every
fixed nearby `q`, `C_1(q)=1`. Hence `|C_a(q)|-1` has the analytic factor
`a-1`, and division by `1-a^2` is removable there. With `b=1-a^2`,
`a=sqrt(1-b)=1-b/2+O(b^2)`, expanding the primitive factors gives

    C_a(q)=1+b[(sum_j q_j)/2-4]+O(b^2).

This proves the displayed boundary value of `Q`, jointly with the local
variables. It also makes all derivative formulas below continuous at `a=1`.

For an actual monic degree-nine polynomial with marked simple zero `a`
and other disk roots `z_k`, its derivative factorization and integration
from zero to `a` give the classical origin identity

    O_a(q)=(prod_k z_k)(prod_j q_j), |O_a(q)|<=prod_j r_j.

For `0<a<1`, integration from `a` to `1/a` gives the classical complex
polar identity

    C_a(q)=prod_k (1-az_k)/(a-z_k).                       (5)

Indeed `p(1/a)=(1-a^2)a^(-9)prod_k(1-az_k)` and
`p'(a)=prod_k(a-z_k)=9/prod_j q_j`; changing variables in the integral
of `p'` gives (5). Since

    |1-az|^2-|a-z|^2=(1-a^2)(1-|z|^2)>=0,

every factor in (5) has modulus at least one, proving `Q>=0` for `a<1`.
These identities are credited to Zhang Lemma3.1 and its complex identity
(3.2); they are not new machinery.

At `a=1`, applicability is proved directly, rather than inferred merely
from analytic continuation. Writing `p(z)=(z-1)g(z)`, logarithmic
differentiation of `p'` and `g` gives

    sum_j q_j=p''(1)/p'(1)=2sum_k (1-z_k)^(-1).

Every disk root distinct from1 has `Re(1-z_k)^(-1)>=1/2`, so
`Re sum q_j>=8` and `Q_1>=0`. A critical collision at the marked root
has infinite reciprocal sum and is outside the finite neighborhood.
Otherwise the marked root is simple, including at the boundary.
Gauss-Lucas supplies the other constraints in (1). Thus actual polynomials
in this reciprocal neighborhood satisfy (2). That baseline was already known
from 7290 with an effective original-root neighborhood; the new statement
here is the explicit critical-coordinate functional reduction.

## 3. Full derivatives, retaining both complex modulus terms

Put `x=a/(1+a)`, `d=1-a`, `b=1-a^2`. Origin derivatives are obtained from

    I1=int_0^1 t(1-xt)^7 dt,
    I2=int_0^1 t^2(1-xt)^6 dt,
    I3=int_0^1 t^3(1-xt)^5 dt,
    Is=I1-8xI2, Iss=I2-8xI3.

For the real origin gap `Re O-prod r`, the heavy, heavy/small, small
diagonal and distinct-small entries of the reference quadratic matrix are

    hO=81x I1/2,       uO=-81x^2 I2/2,
    dO=9x Is/2+x cO/2, eO=-9x^2 Iss/2,
    cO=72x^2 I2/ell-8ell^7,
    H=-partial_{r_1}(|O|-prod r)=9x I1/ell+ell^7>0.

The imaginary linear coefficients of `O` are `w_h=-81xI1` and
`w_s=-9xIs`, seven identical small entries. Therefore its full modulus
quadratic matrix is

    A_O=A_Re+ww^T/(2P).                                 (6)

For the polar factors set

    J1=int_0^1 t(a+dt)^7 dt,
    J2=int_0^1 t^2(a+dt)^6 dt,
    J3=int_0^1 t^3(a+dt)^5 dt,
    Js=J1+8dJ2, Jss=J2+8dJ3.

Their exact positive-coefficient formula, valid for the indicated indices,
is

    int_0^1 t^k(a+(1-a)t)^n dt
      =sum_{j=0}^n [n!(k+n-j)!/((n-j)!(k+n+1)!)]a^j.      (7)

Differentiate the primitive affine-factor product in `C` at `q0`:
`C_h=bJ1`, `C_s=bJs`, `C_hs=b^2J2`, `C_ss=b^2Jss` for distinct small
coordinates. The normalized polar slack derivative is

    g(a)=partial_{s_j} Q_a(q^ref)=Js-J1=8dJ2.             (8)

The four entry types of the *full modulus* phase matrix of `Q_a(q^ref)` are

    hP=-9ell J1/2+b(9ell J1)^2/2,
    uP=-9ell^2 bJ2/2+b(9ell J1)(ell Js)/2,
    dP=-ell Js/2+4x dJ2+b(ell Js)^2/2,
    eP=-ell^2 bJss/2+b(ell Js)^2/2.                       (9)

The terms with factor `b/2` are the polar modulus rank-one contribution;
it must be retained because it is subtracted in the joint function. Formula
(6) must likewise retain its origin modulus contribution. At `a=1`,
`hP=-9/8`, `dP=-1/8`, `uP=eP=0`, consistent with the boundary function.

For any weight `mu`, the slack derivative and phase matrix are exactly

    c_mu=cO-mu g, A_mu=A_O-mu A_P.                       (10)

The negative heavy derivative of the joint gap at the model is

    H_mu=H+mu J1.                                        (11)

Equations (6)-(11) describe every coordinate, with no phase-sum restriction.
The standalone checker verifies 64 full origin directional polynomials
and 64 full polar directional polynomials: eight basis directions and
both signs of every distinct pair. Its literal Gaussian factor products
are separate from the derivative-formula route. It verifies entire
univariate polynomials, not an interpolation grid. Nine further whole
identities check (7), (8), the mixed derivatives, and the closed origin
slack and heavy derivatives.

## 4. Exact fixed weight and whole-interval coercivity

Let `L=1+a`. Each polar entry in (9) has denominator `2L^2`; write its
four numerators as `p_h,p_u,p_d,p_e`. Explicitly,

    p_h=-9L J1+81b J1^2,
    p_u=-9bJ2+9b J1 Js,
    p_d=-L Js+8a dL J2+b Js^2,
    p_e=-bJss+b Js^2.                                    (12)

Write the origin entries over the common denominator `D=18L^7`, with
numerators `o_h,o_u,o_d,o_e` generated from (6). Then the joint entry
numerators are the exact polynomials

    n_i=o_i-9mu0 L^5 p_i, i=h,u,d,e.                     (13)

Also `cO=2S/(7L^6)`, where

    S=a^7+8a^6+28a^5+56a^4+70a^3+56a^2+28a-28.

The unique weight balancing the slack derivative at `a0` is

    cO(a0)/g(a0)=mu0.

With this same rational weight, both cleared polynomials vanish exactly
at `a0`. Define their full polynomial quotients

    U=L^6 c_mu0/(a-a0),
    V=(n_d-n_e)/(a-a0).

The division has zero remainder in both cases. The six small-coordinate
transverse directions have eigenvalue `(a-a0)V/D`. The complementary
orthonormal heavy/constant-small block is

    (1/D)[[n_h,sqrt(7)n_u],[sqrt(7)n_u,n_d+6n_e]] (14)

and covers the other two directions. To check that this entire block is
greater than `I/10000`, put `m=1/10000` and verify the two exact polynomials

    B_h=n_h-mD,
    B_det=(n_h-mD)(n_d+6n_e-mD)-7n_u^2.

The four whole Bernstein expansions on `[5/8,1]` have the following
strictly positive minimum coefficients. Every coefficient, not just these
minima, is regenerated and the complete inverse basis identity is checked.

| Polynomial | Degree | Coefficients | Minimum Bernstein coefficient |
|---|---:|---:|---:|
| U |12|13|185569622336413/3773450616832|
| V |13|14|11958395335884135/60375209869312|
| B_h |21|22|34218081333773727905117583/3043653656919408640000|
| B_det |35|36|9071857254690576581977710822146106450380553/17669348875577715442339492659200000000|

These 85 positive coefficients prove positivity on the entire interval,
because the Bernstein basis functions are nonnegative and sum to one.
All cleared denominators are positive. In particular `U>48`,
`V>2304/3750`, `L^6<=64` and `D<=2304`. Since `a-a0<=3/8`, (14) and
its transverse complement give the simple sufficient bounds

    c_mu0 >= (3/4)(a-a0),
    A_mu0 >= [(a-a0)/3750] I,       a0<=a<=1.             (15)

At `a0`, only the transverse complement and slack derivative vanish;
the two-dimensional block is still strictly positive. For `a>a0`, all
eight directions and all seven first-order slacks are positive.

For the heavy derivative, the closed formula

    H=(L^8-1)/(8aL^6)

obeys `0<H<=1` on `(0,1]`: its cleared excess is the full identity

    8aL^6-(L^8-1)
      =a^2(20+64a+90a^2+64a^3+20a^4-a^6)>0.

The final inequality follows from `a<=1`. Formula (7) gives
`0<J1<=J1(1)=1/2`; since `1<mu0<2`, (11) yields `0<H_mu0<2`.

## 5. Uniform nonlinear bridge

Fix `A>a0`. The reference quantities in (15) are continuous, with positive
uniform lower bounds on `[A,1]`. On one sufficiently small convex product
neighborhood, continuity therefore ensures

    partial_{s_j}G(a,s,0)>=(3/8)(a-a0),
    Hessian_theta G(a,s,theta)>=[(a-a0)/3750] I.           (16)

To retain the pointwise factor `a-a0`, choose absolute derivative errors
bounded by the respective half-margins at `A-a0`; these are no larger than
the half-margins at any `a>=A`. Thus compactness proves (16) uniformly;
it is not an extrapolation from finite Taylor samples.

Conjugation preserves both moduli and all radii, so
`G(a,s,-theta)=G(a,s,theta)` and `grad_theta G(a,s,0)=0` for all nearby
real slacks. Integrating the first inequality of (16) along `0->s`, then
integrating the Hessian along `0->theta` with weight `1-t`, proves (3).

For a nearby tuple satisfying (1), define its reference coordinates using
its seven slacks and eight phases. Its actual heavy radius is

    r_1=r_1^ref+Delta, Delta=sum_j r_j-16ell.

At the compact model, `-partial_{r_1}J=H_mu0` is strictly positive and
less than2. Shrink the common neighborhood so this derivative stays
positive and less than3 along the whole heavy-radius segment. The exact
mean-value integral then gives

    J_a(q)=G(a,s,theta)-K_av Delta, 0<K_av<3.             (17)

The constraints imply `J_a(q)<=0`. Since (3) is nonnegative, (17) first
forces `Delta>=0` and then gives `Delta>=G/3`. This proves exactly (2).
This is an integral of the actual modulus derivative, not an affine
approximation in the heavy radius. The inverse polar coordinates, their
slacks and the heavy-radius segment depend continuously on `q`, uniformly
on the compact curve, providing the stated common `delta_A`.

Equality in the baseline forces all slacks and all phases to vanish in
(2), and then `Delta=0`; hence `q=q0`. Conversely (4) supplies equality.
For actual polynomials, their critical factorization at this tuple has
critical points `((8a-1)/9,-1,...,-1)`; integration with `p(a)=0` gives
exactly the already known family `C(z-a)(z+1)^8`, `C!=0`.

## 6. The precise dual obstruction

Let `lambda_O=dO-eO` in (6), and `lambda_P=dP-eP` in (9). The two
modulus rank-one terms vanish on the six transverse directions. The
polar transverse numerator, with denominator `2L^2`, has coefficients
in increasing degree order

    [0,-17/72,-47/168,-43/504,-41/504,-13/168,
                                  -37/504,-5/72,-11/168,-2/63].

Consequently `lambda_P<0` for every `a>0`. For `0<a<1`, `g>0` by its
positive integral. Nonnegative slack and transverse coefficients require

    lambda_O/lambda_P <= mu <= cO/g.                    (18)

The exact compatibility identity, verified coefficient by coefficient, is

    L^8(g lambda_O-cO lambda_P)=a(8a-5)R(a),
    R(a)=1/2+(71/42)a+(115/42)a^2+(39/14)a^3
                             +(11/6)a^4+(31/42)a^5+a^6/7. (19)

Every coefficient of `R` is positive. The upper minus lower endpoint in
(18) has the sign of the left side of (19), since `g lambda_P<0`.
For `0<a<a0` the interval is empty. At `a0` its unique point is `mu0`;
the exact cutoff divisions already verify simultaneous vanishing.
For `a>a0`, the complete certificate above proves that this single fixed
weight also controls the remaining two-dimensional phase block.

This proves the claimed sharp quadratic-dual onset. At the endpoint,
nonnegative jets do not imply a nonlinear lower bound. The earlier actual
polynomials in 7290 already violate the baseline at `a0` by a negative
quartic term, so the endpoint is correctly excluded here. Its known
negative-side family is not relabeled as a new counterexample. Review9078's
different negative quartic path concerns the origin-only threshold near
0.8612, not the joint weight in this proof. Neither result refutes the full
first-power inequality `F>=8`.

The effective width, a larger geometric basin and the unrestricted complex
degree-nine first-power endpoint remain outside this functional reduction.
