# Explicit joint-moment and full-residual coercivity

Actual **six-sendov-2**, role **researcher**, 2026-10-03. Complete ordinary
author lemma with an exact rational certificate; **unformalized and
independently unreviewed**. Polynomial Bezout identities, coefficient norms,
complex segment estimates, Newton identities, interlacing, derivative mesh
and Lagrange interpolation retain their classical credit.

## 1. Full definitions and the claims

Use the entire reconstructed maps of
[9550](../degree-five-triangular/PROOF.md), source
**cb4cf7d9d83f3d376d3763b65cbe2fddd50637f4**. All expressions lie in
QQ[B,E,r,s,t,t^-1], with the sole localization **t!=0**. The heptic and
mass interpolant have the form

\[
 h=z^7-\tfrac38z^5+Bz^4+Ez^3+F^*z^2+G^*z+J^*,\quad
 p=p_0+p_1z+p_2z^2+rtz^3+stz^4+tz^5.
\]

The recursive fixed-pivot definitions of ALL starred coefficients, p0,p1,p2,
Q, the normal-representative operators T,rho and the full ODE/kernel are
exactly Sections2--3 of9550. In particular

\[
 O=ph''+(p'-Q)h'+(64-Q')h,\quad
 \mathcal K=-16p-\tfrac14T^2\rho(p^2)+\tfrac14T\rho(p(Q-p')),
\]

and the **complete five-vector** is

\[
 R=(tO_2,tO_1,tO_0,\mathcal K_1,\mathcal K_0+4).          \tag{1}
\]

All five R entries are ordinary polynomials, degree at most10. Fstar has
absolute Laurent degree4. There is no sampled, truncated or unspecified
residual. The source regenerates the whole9550 input through
[9902](../cubic-quintic-exclusion/PROOF.md), source
**fadd074a5339772bb937e7e77c5a0292c80b256a**.

**Theorem A.** Let B,E,r,s,t be any finite **complex** parameters, t!=0.
For every real L>=1 such that

\[
 |B|,|E|,|r|,|s|,|t|,|t^{-1}|\le L,
\]

the entire reconstructed maps satisfy

\[
 |B|+|F^*|+\|R\|_\infty\ \ge\ \frac1{10^{68}L^{95}}.      \tag{2}
\]

No R=0 premise, s!=0 assumption, unknown pivot or reality/positivity
assumption is used in Theorem A. This is joint coercivity of the two
coefficients and **all five** residuals. It is not a lower bound for R alone,
a full coupled-Jacobian statement or an original-root existence test.

**Theorem B.** Let a1<...<a8 be distinct real originals, sum ai=0,
sum ai^2=1, at first-order stationarity of the angular quotient defined in
[7432](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_quartic/PROOF.md).
Write f=product(z-ai), h=f'/8 and
mj=-8f(lambda_j)/h'(lambda_j)>0 at its seven simple real criticals.
Let p be their unique mass interpolant; [9496](../mass-stationary-chart/PROOF.md)
proves p has exactly degree5 at this stationarity. Suppose specified
delta,tau in(0,1] satisfy

\[
 a_{i+1}-a_i\ge\delta\quad(1\le i\le7),\qquad
 |p_5|\ge\tau.
\]

Then, with mu_k=sum ai^k,

\[
 \mu_3^2+\mu_5^2\ \ge\
 \frac{57600}{4549\,10^{136}}(\tau\delta^6)^{190}.         \tag{3}
\]

These are sufficient coarse constants, not optimized exponents. Theorem B
has an explicit **leading mass coefficient lower bound**. No numerical
tau(delta), nonempty stationary set, collision continuation, physical H,
reciprocal-distance inequality or full first-power endpoint is asserted.

## 2. Lift the old B=s=0 obstruction to a whole row unit

Let Rbar_i=R_i(0,E,r,0,t), and put

\[
 E_0(r)=-(10976r^2+7344r+1143)/2112,\qquad
 A_i=\bar R_i(E_0,r,t).
\]

The entire old slice identities are

\[
 \bar R_3=-88t(E-E_0)/7,\quad
 A_1=-tP(r)/9504,\quad
 A_0=a_2(r)t^2+b_2(r),\quad A_2=a_0(r)t^2+b_0(r),
\]

where P=4934272r^3+4606896r^2+1459368r+157599 and the entire coefficients
a2,b2,a0,b0 mean the t^2/t^0 coefficients of the indicated FULL rows.
They are generated without elimination choices by the preceding definitions.
The undivided cross identity is

\[
 a_2b_0-a_0b_2=(5/1254528)S(r),
\]

with S the complete degree-six polynomial of Section5 of9550.
Its rational Bezout polynomials U,V are already published there, with
**UP+VS=1**. No old exclusion is claimed new. Define

\[
 W_0=-(1254528/5)Va_0,\quad W_1=-9504U/t,\quad
 W_2=(1254528/5)Va_2,\quad W_3=W_4=0.
\]

Then sum Wi Ai=1 as an **entire** polynomial/Laurent identity. In particular
the cross uses no a0/a2 slope division or generic-degree assumption.
Let Di be the complete polynomial difference quotient defined by

\[
 \bar R_i-A_i=(E-E_0)D_i.
\]

It is evaluated exactly by E^k-E0^k=(E-E0)sum_(j=0)^(k-1)E^(k-1-j)E0^j.
The entire first displayed pivot gives E-E0=-7Rbar3/(88t). Therefore

\[
 Z_i=W_i\ (i=0,1,2,4),\quad
 Z_3=\frac7{88t}\sum_iW_iD_i,\qquad
                   \sum_{i=0}^4 Z_i\bar R_i=1.             \tag{4}
\]

Every Z is an explicit QQ[E,r,t,t^-1] polynomial. Their term counts are
8/6/7/24/0, total45 coefficients, and absolute Laurent degrees are
7/6/6/9/0. All coefficients and difference quotients are included in
[expected.json](expected.json), derived and fully multiplied by
[verify.py](verify.py). Only the known t inverse is used. The lift (4),
its norms and its quantitative use are new here; the underlying cubic/S
obstruction remains credited to9550.

## 3. Whole coefficient bounds

For a Laurent polynomial g=sum c_alpha v^alpha, define
|g|_coef=sum|c_alpha| and deg_abs g=max sum|alpha_j|.
If all |v_j| and the only needed inverse |t^-1| are bounded by L>=1,
then |g(v)|<=|g|_coef L^(deg_abs g). All full polynomials are used.

The entire exact computations give:

| Quantity | Exact coefficient norm | Integer bound | Degree bound |
|---|---:|---:|---:|
| Sum of coefficient norms of Z_i | 108740454076928799436912812725247921959/536971633427366372750524416000 | N_Z=202506888 | 9 |
| Maximum coefficient norm of partial_j R_i, j=B,E,s | 599063571511/36126720 | N_R=16583 | 9 |
| Coefficient norm of partial_B Fstar | 321/140 | N_F=3 | **2** |

The source computes every coefficient and actual degree. The full Fstar
degree is4, but its **B derivative has degree2**; retaining this gives the
final exponent95. The norm of the five-vector uses a maximum, while the
unit uses the sum of all five Z norms, as (4) requires.

From9902, retain the whole rational x-unit directly multiplied in that
author proof. Its raw multiplier coefficient norms sum to S_raw, and
the regenerated entire input gives 0<S_raw<10^-13. The independent
[review9928](../../six-reviewer-1/joint-moment-audit/REVIEW.md), actual
six-reviewer-1, source **1f38478ea1fd984c26c58e528178b817c0532b52**,
confirms9902 relative to9550/9496/7432 and proves this sharper same-domain
margin. Credit for retaining the sharper margin belongs to that review;
it supplies no verdict on this new lemma. Put C_U=10^-13. The complete
five primitive rows P_i, 5x3 matrix M(r,x), all10 minors and the ordinary
Cauchy--Binet/singular-value bridge then give

\[
 \|P(r,x,u)\|_2\ge
 2|x|\sqrt{1+|u|^2+|u|^4}/(C_U Q A^{14}),                \tag{5}
\]

for arbitrary finite complex r,x,u with x*u!=0, |r|,|x|<=A, A>=1.
Here Q=14913669297722925580854623. The five rows are the full B=Fstar=0
residuals multiplied by s^2,s,s^2,s,s^2 and divided by their positive
rational contents. **All five** content inverses are bounded by
C_p=1814727936. Nothing about small physical energy or actual original
realization is imported from (5).

## 4. The small-s boundary is quantitatively controlled

Set b=|B|, f=|Fstar|, rho=||R||_infty and m=b+f+rho. Along the complex
straight segments changing B to0 and then s to0, all parameter moduli and
the t inverse remain bounded by L. Ordinary differentiation of polynomials
and Section3 give

\[
 |R_i-\bar R_i|\le N_R L^9(b+|s|).
\]

Using the ENTIRE unit (4),

\[
 1\le N_Z L^9[\rho+N_RL^9(b+|s|)]
   \le N_ZN_RL^{18}(\rho+b+|s|).                         \tag{6}
\]

Define the fixed rational a0 and the threshold sigma by

\[
 a_0=1/(2N_ZN_R)=1/6716343447408,\qquad
 \sigma=a_0L^{-18}.
\]

Consequently, if m<sigma, then rho+b<sigma and (6) forces |s|>sigma.
This covers the otherwise missing s=0/small-s branch without assuming
any quartic mass coefficient floor or selected-pivot nonvanishing.

## 5. Project to the complete zero-moment slice

Suppose also m<83sigma/(180L^2), and put D=3L^2>=1. By the full
Fstar B-derivative bound,

\[
 F_0=F^*(0,E,r,s,t),\qquad |F_0|\le f+Db\le Dm.
\]

The entire B=0 coefficient has E pivot **-83s/60**, as verified directly
in the original chart and in9902. Since |s|>sigma, the only new projection is

\[
 E'=E+\frac{60}{83s}F_0,\quad F^*(0,E',r,s,t)=0,\quad
 |E'-E|\le\frac{60D}{83\sigma}m<1.                       \tag{7}
\]

The s inverse here is justified by (6); it is not a generic assumption.
All moduli along the two segments from (B,E) to (0,E') are bounded by2L,
while r,s,t are fixed. Put J=N_R(2L)^9>=1. Then all five full residuals
at the projected point obey

\[
 |R_i(0,E',r,s,t)|\le\rho+J(b+|E'-E|)
  \le 2J\left(1+\frac{60D}{83\sigma}\right)m.             \tag{8}
\]

Set x=s^2,u=st. They are nonzero, and |r|<=L^2,|x|<=L^2. The projected
point lies on the entire B=Fstar=0 coefficient slice of9902, without an
actual-original interpretation. Multiplication by s^2,s,s^2,s,s^2 and
division by the full positive contents give its primitive vector P.
Since L>=1 and |s|<=L, (8) and sqrt(5)<3 give

\[
 \|P\|_2\le6C_pL^2J
           \left(1+\frac{60D}{83\sigma}\right)m.
\]

On the other hand (5), with A=L^2, gives
||P||_2 >=2|s|^2/(C_U Q L^28)>=2sigma^2/(C_U Q L^28).
Thus the small-m case forces

\[
 m\ge \frac{\sigma^2}
 {3C_U Q C_p N_R 2^9 L^{39}(1+60D/(83\sigma))}.          \tag{9}
\]

Every one of the five original residuals, the whole reconstructed Fstar,
both legal nonzero factors and every variable degree-loss branch remain.
There is no conic/rank shortcut or a single favorable residual replacing P.

## 6. Finish the universal complex bound, including closed endpoints

Substitute sigma=a0 L^-18 and D=3L^2 into (9). The powers are
36+39=75 and 2+18=20. Since L>=1,

\[
 1+\frac{180}{83a_0}L^{20}
 \le\left(1+\frac{180}{83a_0}\right)L^{20}.
\]

This holds for **every** L>=1; the ordinary reason is L^20>=1.
The source multiplies the whole factorization
L^20-1=(L-1)sum_(j=0)^19 L^j, not finitely sampled L values.
Therefore (9) implies m>=c0 L^-95, where

\[
 c_0=\frac{a_0^2}
 {3\,2^9 C_U Q C_p N_R(1+180/(83a_0))}.
\]

The following full rational comparisons are checked with integer/Fraction
arithmetic:

\[
 10^{-68}\le c_0,\qquad
 10^{-68}\le a_0,\qquad
 10^{-68}\le83a_0/180.                                    \tag{10}
\]

If m<10^-68 L^-95, (10) and L>=1 first imply m<sigma and then
m<83sigma/(180L^2). Sections4--5 apply, and (9) forces
m>=c0 L^-95>=10^-68 L^-95, a contradiction. This proves (2).
The proof uses strict inequalities only for the contrary assumption,
so the conclusion is valid on the **closed** budget L>=1, including L=1.
Negative or nonreal t is allowed in Theorem A; only t=0 is excluded.

## 7. Actual separated-original coefficient bounds

This section proves the ordinary geometric input used to pass to (3).
It is not original-root enumeration or a new derivative-mesh theorem.
Since sum ai^2=1, every |ai|<=1. Interlacing gives seven simple real
lambda_j in(a_j,a_(j+1)), all in[-1,1]. Their mesh exceeds delta:

For j=1,...,6, put x=lambda_j,y=x+delta. We have y<a_(j+2).
If y<=a_(j+1), then lambda_(j+1)>y already. Otherwise y is in the next
original interval. Let g(w)=sum_i1/(w-ai), strictly decreasing on each
such interval, with g(x)=0. For i=2,...,8,
y-ai<=x-a_(i-1). Both denominators are positive for i<=j+1 and negative
for i>=j+2. Since the reciprocal function decreases on each sign interval,

\[
 g(y)\ge\sum_{i=1}^7\frac1{x-a_i}+\frac1{y-a_1}
       =-\frac1{x-a_8}+\frac1{y-a_1}>0.
\]

The next zero of g is therefore lambda_(j+1)>y. This proves the needed
classical derivative mesh inequality directly, including every possible
position of x+delta relative to a_(j+1).

The proper partial fraction expansion of -8f/h has residues mj>0.
Balance and norm give f6=-1/2 and h5=-3/8; the coefficient of z^-1 in
-8f/h is -8(f6-h5)=1. Hence **sum mj=1**. All criticals are simple,
so no repeated-pole or collision convention is silently used here.

The Lagrange interpolant is

\[
 p(z)=\sum_{j=1}^7m_j
 \frac{\prod_{\ell\ne j}(z-\lambda_\ell)}
      {\prod_{\ell\ne j}(\lambda_j-\lambda_\ell)}.
\]

The mesh bound gives denominator modulus at least
delta^6(j-1)!(7-j)!>=36delta^6. Since all |lambda|<=1, the numerator
coefficient of z^k has modulus at most binom(6,k). Positivity and the
entire sum mj=1 therefore give, for **every** k=0,...,6,

\[
 |p_k|\le\frac{\binom6k}{36\delta^6}
        \le\frac5{9\delta^6}<\delta^{-6}.                \tag{11}
\]

The factor36 is the minimum of all seven factorial products, not a
one-sided critical-node estimate. At stationarity p6=0 and p5!=0 by9496;
reflection allows t=p5>0. From |p5|>=tau, equations r=p3/t,s=p4/t and
(11) give |r|,|s|<=delta^-6/tau, |t|<=delta^-6 and |t^-1|<=tau^-1.

The same original Newton identities give
B=-5mu3/24 and E=1/16-mu4/8. Since |mu3|<=1 and
1/8<=mu4<=1, |B|<=5/24<1 and -1/16<=E<=3/64.
Consequently **L=(tau delta^6)^-1** bounds every quantity in Theorem A.
This supplies the entire domain bridge, not just an upper mass coefficient
bound. The supplied tau lower bound remains necessary.

## 8. Original moment conversion and remaining frontier

For actual stationarity, the full feasibility theorem gives R=0 and the
starred coefficient is the actual critical coefficient.9902's whole Newton
identities give

\[
 B=-5\mu_3/24,\qquad F^*=\mu_3/16-3\mu_5/40.
\]

Thus
|B|+|Fstar| <=(13/48)|mu3|+(3/40)|mu5|.
The squared norm of these two weights is
(13/48)^2+(3/40)^2=4549/57600. Cauchy--Schwarz and Theorem A imply

\[
 \mu_3^2+\mu_5^2\ge\frac{57600}{4549}
             (10^{-68}L^{-95})^2,
\]

which is exactly (3). Both complete inverse moment identities are checked
as polynomials, not evaluated on a selected profile.

The bound is computable from a specified original separation and a
specified leading mass coefficient floor; for a single actual profile
one may take tau=min(1,|p5|). It gives an explicit rate at which a
near-zero odd-moment pair would force the leading mass coefficient to
degenerate on a fixed separated domain. It does NOT provide a numerical
delta-only tau(delta). Qualitative compactness from9902 already gives a
positive joint-moment gap on each NONEMPTY fixed-separated stationary set;
that old result is not claimed new. The unresolved numerical leading
coefficient floor is the next precise obligation for a separation-only
bound. No collisions, stationary classification, physical H, global
first-power inequality or full coupled-Jacobian rank is concluded.

## 9. Reproduction and trust boundary

Run CPython3.10+ standard library, with native thread variables set to1:

    python3 -I -B verify.py
    python3 -I -B -O verify.py

The checker regenerates and compares the ENTIRE pinned9902 input and its
ENTIRE9550 defining input. Same-author sparse Laurent arithmetic and old
9550 Bezout coefficients are openly reused, not independent implementations.
It constructs all45 Z coefficients and five complete E difference
quotients, multiplies all full identities, computes every coefficient norm
and degree, checks the full rational constants/power factorization/inverse
moments, and retains all seven interpolation constants. Mathematical damage
and boundary controls remain meaningful under optimization. Author-only
`--bootstrap` creates the fixture; it supplies no independent verdict.

The universal complex segment/norm argument, old Cauchy--Binet bridge,
real-root mesh/residues/interpolation and actual feasibility/moment bridges
are ordinary written mathematics. They are not proved by finite profile
samples, hashes or controls. Negative-t controls are algebraic charts, not
disk-feasible originals. Old x=0,r=-3/8,u=-224/9 really zeros all five
primitive polynomials, but cannot be a finite original chart with x=s^2,
u=st; it explains the boundary handled by (4). Every raw solving record,
exploratory log and old incomplete Groebner scout remains private. No
timeout, solver status, enumeration, prime or resource failure is a premise.
Input reviews9598/9781 are scoped to their own inputs. Review9928 confirms
9902 and its sharper coefficient margin relative to the cited framework;
the entire raw coefficient norm is also regenerated here. Its complete
two-point polynomial-extension boundary classification is credited to that
review, not claimed new or used as an original-root realization. None of
these reviews reviews this new lemma. No formalization or independent new
verdict is claimed.
