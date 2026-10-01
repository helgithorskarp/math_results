# The fourth degree-nine first-power boundary coefficient

Actual author **six-sendov-3**, role **researcher**, 2026-10-01.
Complete ordinary author proof with exact finite algebra. Independent
review of this extension is pending. Collars and remainder constants
are existential; no claim of formal verification or historical priority.

## 1. Statements and inherited hypotheses

Let p be a degree-nine complex polynomial with all original roots in the
closed unit disk. For a marked root a, with the eight critical points
counted with multiplicity, put

\[
 F_p(a)=\sum_{j=1}^8 |a-\zeta_j|^{-1},\qquad \eta=1-|a|.
\]

A zero denominator means infinity. Multiplying p by a nonzero constant
and rotating the plane preserve F. When 0<eta is sufficiently small,
take p monic and a=1-eta positive. Define

\[
\begin{gathered}
c=\cos(\pi/9),\quad d=2c^2-1,\quad v=2d^2-1,\quad
y=[3(1+c)]^{-1},\quad x=2/3-y,\quad H=14y,\quad U_0=-8x,\\
C=8/3+y,\quad
B_*=2311/108+(4934/27)c-(1976/9)c^2,\\
C_3=-60800959/17496-(307083769/17496)c+(10980067/486)c^2,\\
\rho=(c-5)/3,\quad L=-7(2c+1)/18,\quad b=\sqrt{H/2},\\
u_z=(U_0+\rho H)/8,\qquad u_p=u_z-\rho H/2.
\end{gathered}                                                    \tag{1}
\]

These constants and the selected profile
\(h^*=(b,-b,0^6),\ u^*=(u_p,u_p,u_z^6)\) are credited prior results.
The new fourth coefficient is

\[
 C_4=\frac{340367352475}{839808}
     +\frac{808137564635}{419904}c
     -\frac{1052841914857}{419904}c^2,
 \qquad -233.920855886<C_4<-233.920855885.                    \tag{2}
\]

Write base3(eta)=8+C eta+Bstar eta2+C3 eta3 and
base4(eta)=base3(eta)+C4 eta4. There exist K,eta0>0 such that
every p,a as above with 0<eta<eta0 obeys

\[
 F_p(a)\ge\operatorname{base4}(\eta)-K\eta^5.                 \tag{3}
\]

At every sufficiently small positive eta an explicit all-disk family
below has F=base4(eta)+O(eta5). Consequently

\[
 \inf_{p,a:\ |a|=r} F_p(a)
 =8+C(1-r)+B_*(1-r)^2+C_3(1-r)^3+C_4(1-r)^4
       +O((1-r)^5).                                        \tag{4}
\]

The error constants in (3)-(4) are uniform over competitors. No
existence of a minimizing polynomial is assumed. In particular the
exact cubic line base3 is not a universal lower bound in any boundary
collar, because C4<0 and the family exists at every small radius.

The proof also gives a quantitative finite first-jet gap on every fixed
fourth upper-budget class F<=base3+U eta4; see (24). A fixed fifth upper
budget F<=base4+T eta5 forces, after a simultaneous permutation,

\[
\begin{aligned}
h&=h^*+\eta\gamma h^*+O(\eta^{3/2}),\\
u&=u^*+\eta(\beta,\beta,\alpha^6)+O(\eta^{3/2}),
\qquad
h_j=\Im\zeta_j/\sqrt\eta,quad u_j=\Re\zeta_j/\eta.          \tag{5}
\end{aligned}
\]

Here gamma,alpha,beta are specified below. This selects the full
next critical profile for arbitrary complex competitors, not just a
symmetric family. The joint O(eta3/2) normalized-coordinate error in (5)
is optimal across fixed fifth upper-budget classes: the explicit split
family in Section7 has a nonzero limiting error at that scale. This also
proves sharpness of the O(eta5/2) real-coordinate error for the six small
critical points. Other individual coordinate exponents are not asserted
optimal.

The direct analytic premise is the published
[cubic theorem8751](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/cubic-boundary/PROOF.md),
source52a408f210846d246b5c8dfd890cc142d480d2c4,
artifact bafkreia7q6o6yd6eqb7ok7mtbohko4rz27els2xg5wimfqbkmh4ndhrfkq.
It is independently confirmed, subject to its inherited premises, by
[review8781](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/cubic-boundary-audit/REVIEW.md),
source94cbfb364599e5cfa0cf866723c5f9717f38bc39,
artifact bafkreic2em367vlwtsjqarqmkzusqlb3d52fsnn3kzyroli32e2t2be5gu.
That review's sharper cubic penalty and smaller repair of the *old fixed
family* are prior work; neither determines C4. Its full source and
graph body were read and its independent171-check/five-damage baseline
reproduced. The author8751 baseline was also exactly replayed,90 checks
and six damages. Their reproduction is input validation, not new research.
The earlier concentration7190, second optimum8619/review8684, and
profile8668/review8718 remain inherited. [LITERATURE.md](LITERATURE.md)
records their scope and provenance.

## 2. Fourth-budget contact and the imaginary improvement

Fix finite real U and impose F<=base3+U eta4. All O estimates in Sections
2-6 are uniform on this class in a U-dependent existential collar.
The parent cubic theorem gives dist((h,u),M)=O(eta), where M is the
simultaneous-permutation orbit of (hstar,ustar). Choose a nearest
permutation at each eta. No label is assumed analytic or continuous.
The critical points may have arbitrary multiplicities.

Use the parent's exact moments

\[
\begin{gathered}
\Re\sum\zeta_j=U_0\eta+\eta^2W,\quad
\Re\sum\zeta_j^2=-H\eta+\eta^2D,\quad U_2=\sum u_j^2,\\
V=\Im\sum\zeta_j/\eta^{3/2},\quad B=2h\cdot u,
\quad J_k=\sum h_j^k,quad J_{ab}=\sum h_j^a u_j^b.           \tag{6}
\end{gathered}
\]

W,D,h,u are bounded, W-Wstar,D-Dstar=O(eta), and exactly
sum h=eta V, sum h2=H+eta(U2-D), sum u=U0+eta W. The selected profile
makes J3,h dot u,J5,J31,J12 and all higher opposed-pair odd moments
zero. Their actual values are O(eta). The parent sine estimate gives
V=4B/7+O(eta3/2), so sum h=O(eta2).

All imaginary coefficients of p=Rpoly+iI are O(eta5/2). Specifically
Im P1,Im P2,Im P3 are O(eta5/2); Im P4,Im P5 are O(eta7/2).
For example Im P3=-eta3/2 J3+3eta5/2 J12 and
Im P4=-4eta5/2 J31+4eta7/2 sum(hu3).
Im P6,Im P7 are O(eta9/2), and Im P8 is later. Newton identities,
products with bounded real moments and real anchoring preserve these
orders. The *whole* vector I is controlled, not just a few coefficients.

Let omega_k=exp(2pi i k/9), k=3,4. For each actual active conjugate
pair let Aavg_k be the average of half squared-modulus minus one;
both individual quantities are nonpositive. Put

\[
\begin{gathered}
(A_3,B_3)=(3/2,3/2),\quad (A_4,B_4)=(1+c,1-d),\\
w_4=(c+d)^{-1},\quad w_3=\tfrac23[7-(1-d)/(c+d)],\\
\sigma=\frac38-\frac{(3/2)w_3+(1-v)w_4}{20},\quad
\mathcal B(h,u)=K_0+\|u\|^2/2+\rho J_{21}+\sigma J_4,\\
K_0=-2609/405-(2000/81)c+(12964/405)c^2,\quad
k=\rho u_p+\sigma H.                                     \tag{7}
\end{gathered}
\]

The weights are positive and sum wA/8=1, sum wB/7=1.
At the profile grad_u Bcost=uz times1 and grad_h Bcost=2k hstar.
The exact mean/norm identities and Taylor's formula give

\[
\mathcal B(h,u)=B_*+\eta\Theta_*+O(\eta^2),\quad
\Theta_*=u_zW_*+k(U_2^*-D_*).                              \tag{8}
\]

Indeed the u linear term is uz eta W, while
2 hstar dot(h-hstar)=eta(U2-D)-||h-hstar||2.
Replacing bounded moments by their limits costs O(eta2).
The parent's retained-slack cubic equality, with its cubic coefficient
identity Theta*+f3*+sum wR3*=C3, now reads

\[
F-\operatorname{base3}
=\eta^2[\mathcal B(h,u)-B_*-\eta\Theta_*]
   -\sum_k w_k Aavg_k+O(\eta^4).                           \tag{9}
\]

The budget and (8) force -Aavg_k=O(eta4). Each individual active radial
quantity lies between twice its average and zero, hence is O(eta4).

The root map at omega satisfies conjugation parity:
Phi_baromega(R,I)=conjugate(Phi_omega(R,-I)). Its radial pair average
is even in I and differs from its value for Rpoly by O(||I||2)=O(eta5).
The radial half-difference is odd in I; uniform derivatives on a fixed
coefficient neighborhood give its linearization at z9-1 with error
O(eta||I||+||I||3)=O(eta7/2). The omitted imaginary Newton terms also
have order at least eta7/2. The two active sine rows therefore give

\[
V=4B/7+O(\eta^2),\qquad B=2LJ_3+O(\eta^2),\qquad
h\cdot u-LJ_3=O(\eta^2).                                 \tag{10}
\]

For clarity, the leading rows are
(Im P1/8)sin theta_k+(Im P2/14)sin2theta_k
-(Im P3/18)sin6theta_k. Divide by eta3/2 and solve. The sine ratios
are -1 and -2c, so their determinant is nonzero. The original-root
half-differences are O(eta4); the larger O(eta7/2) linearization error
still yields the O(eta2) residual in (10). This argument uses actual
disk roots; it imposes no disk hypothesis on Rpoly.

## 3. Complete first and second moving corrections

Set

\[
\begin{gathered}
W_* =2512/27+(5840/9)c-(21392/27)c^2,\\
D_* =-4270/27-(29492/27)c+(4012/3)c^2,\qquad
\gamma=(6u_z^2+2u_p^2-D_*)/(2H).                           \tag{11}
\end{gathered}
\]

Initially write h=hstar+eta xi_actual and u=ustar+eta nu_actual;
both first jets are bounded. The exact moments and (10) imply, each
with defect O(eta), the four affine conditions

\[
\sum\xi=0,\quad h^*\cdot\xi=H\gamma,\quad
\sum\nu=W_*,\quad h^*\cdot\nu-(\rho+3L)\sum(h_j^*)^2\xi_j=0. \tag{12}
\]

The last relation follows by expanding h dot u-LJ3 and using
ustar dot xi=uz sum xi-rho sum(hstar2 xi). Correct only the large-pair
coordinates of xi and nu by O(eta) to make (12) exact. The constant
four-row system is invertible. All six small imaginary and six small
real coordinates remain free: the full affine chart is

\[
\begin{gathered}
S=\sum_{i=1}^6 t_i,\quad R=\sum_{i=1}^6 r_i,\\
\xi/b=(\gamma-S/2,-\gamma-S/2,t_1,\ldots,t_6),\\
\nu_{i+2}=W_*/8+r_i,\quad
(\nu_1+\nu_2)/2=W_*/8-R/2,\\
\nu_1-\nu_2=-(\rho+3L)b^2S.                               \tag{13}
\end{gathered}
\]

Thus the actual coordinates admit an *exact* moving decomposition
h=hstar+eta xi+eta2 chi, u=ustar+eta nu+eta2 v2, with bounded chi,v2.
The improved mean in (10) gives

\[
\sum\chi=(24L/7)\sum(h_j^*)^2\xi_j+O(\eta)
          =8b\kappa_1+O(\eta),\quad \kappa_1=-3Lb^2S/7.     \tag{14}
\]

Define m(t,r),theta(t,r) by the two third active radial equations of
the canonical real polynomial constructed from

\[
h_c=h^*+\eta\xi+\eta^2(\theta h^*+b\kappa_1\mathbf1),\qquad
u_c=u^*+\eta\nu+\eta^2m\mathbf1.                           \tag{15}
\]

Here the real polynomial is obtained by the complete real Newton
construction and anchoring at1-eta. These equations have constant
responses -Ak m+(H Bk/7)theta; their determinant is
H(A4 B3-A3 B4)/7=3H(c+d)/14>0. Consequently m,theta are bounded
polynomials on every bounded first-jet box. Their full exact coefficients
are generated in candidate.py and recorded in expected.json.

The actual p1,p2 jets are fixed by (12). At third order, chi,v2 enter
the real polynomial only through sum v2 and hstar dot chi. All imaginary
products start at eta5, and the radial pair-average error is O(eta5).
The O(eta4) active averages therefore force

\[
\sum v_2=8m(t,r)+O(\eta),\qquad
h^*\cdot\chi=H\theta(t,r)+O(\eta).                         \tag{16}
\]

Project these two defects and (14) to exact canonical values, on the
independent vectors1 and hstar. The corrections are O(eta). We obtain

\[
\begin{aligned}
h&=h_c+\eta^2\tau+\eta^3\psi,&\quad \sum\tau=0,\quad h^*\cdot\tau=0,\\
u&=u_c+\eta^2\varsigma+\eta^3\upsilon,&\quad \sum\varsigma=0. \tag{17}
\end{aligned}
\]

All t,r,tau,varsigma,psi,upsilon are bounded moving parameters. Nothing
has been assumed to converge or to possess a Taylor series. The second
tangent space has dimension6+7=13, and the third corrections have all
8+8=16 coordinates. This is the completeness step absent from a
calculation on one symmetric path.

## 4. Uniform fourth dual expansion and higher trace

For bounded h,u,W,D with the exact mean/norm definitions, the real
critical powers through eta4 are

\[
\begin{aligned}
\Re P_1&=U_0\eta+W\eta^2,&
\Re P_2&=-H\eta+D\eta^2,\\
\Re P_3&=-3J_{21}\eta^2+U_3\eta^3,&
\Re P_4&=J_4\eta^2-6J_{22}\eta^3+U_4\eta^4,\\
\Re P_5&=5J_{41}\eta^3-10J_{23}\eta^4+O(\eta^5),&
\Re P_6&=-J_6\eta^3+15J_{42}\eta^4+O(\eta^5),\\
\Re P_7&=-7J_{61}\eta^4+O(\eta^5),&
\Re P_8&=J_8\eta^4+O(\eta^5).                             \tag{18}
\end{aligned}
\]

U3=sum u3,U4=sum u4. No moment in (18) is discarded. Imaginary products
in real elementary coefficients have order at least eta5. Real anchoring
preserves the uniform error. The complete fourth anchored coefficient
has106 rational monomials in fifteen independent real moment symbols;
it is reproduced coefficient by coefficient in generic_eta4.py. Both
Newton recurrence and the independent product of truncated exponentials
exp(sum (-1)^(j-1) P_j t^j/j) agree on the full complex jet. All five
low imaginary symbols are independent and retained before truncation.

The scalar fourth coefficient of one exact distance is

\[
a_4(h,u)=(1+u)^4-5h^2(1+u)^3+(45/8)h^4(1+u)^2
 -(35/16)h^6(1+u)+(35/128)h^8.                            \tag{19}
\]

Together with the lower scalar coefficients and the exact mean/norm
substitution, (18)-(19) and the uniform simple original-root maps give

\[
\Phi(h,u):=F+\sum_k w_k Aavg_k
=8+C\eta+\eta^2\mathcal B(h,u)
    +\eta^3\Gamma_3(h,u,W,D)+\eta^4\Gamma_4(h,u,W,D)
    +O(\eta^5).                                           \tag{20}
\]

Gamma3,Gamma4 denote the complete scalar-plus-radial coefficients,
including every moment in (18). They are polynomials in the bounded
moments, with constant root denominators, hence uniformly Lipschitz
on the boxes in question. Formula (20) holds for the actual competitors
and for (15). It follows by expanding the real polynomial first and
then applying the uniform root Taylor map. The even imaginary pair
correction O(||I||2)=O(eta5) is included in the error. Its eta2 coefficient
is precisely the credited Bcost in (7), because the W,D terms cancel
by the two positive dual identities. No active slack is dropped.

To compare (17) with (15), their h,u differ by O(eta2). Their W differ
by O(eta2), because sum varsigma=0. Their D differ by O(eta2), since
hstar dot tau=0 and
D=||u||2-(||h||2-H)/eta: the norm-square difference starts at eta3.
Thus the eta3 and eta4 terms of (20) change by O(eta5) or less.
Taylor's formula for Bcost gives

\[
\mathcal B(h,u)-\mathcal B(h_c,u_c)
=\eta^2[2k h^*\cdot\tau+u_z\sum\varsigma]+O(\eta^3)
=O(\eta^3).                                               \tag{21}
\]

The gradient variation is O(eta) times an O(eta2) displacement; the
third correction is O(eta3); the quadratic remainder is O(eta4).
Consequently **Phi(actual)-Phi(canonical)=O(eta5)** uniformly.
This proves that every higher tangent and normal parameter in (17)
is harmless for the fourth coefficient. In particular replacing W,D
by their limits without tracking their changes would not justify it.

The exact higher_trace.py checks this trace on the complete13-dimensional
second tangent space and16-dimensional third correction space. On the
second space, every real polynomial/objective jet below fourth is
unchanged and the full fourth dual response equals the zero differential
in (21). On the third space the full primitive response is

\[
-\frac98\Big(\sum\upsilon\Big)(z^8-1)
+\frac97(h^*\cdot\psi)(z^7-1),
\]

and the scalar response is sum upsilon-hstar dot psi; their positive
dual sum is identically zero. These full polynomial identities support
the trace; uniform errors and the moving-parameter comparison remain
the written analytic proof (20)-(21), not a numerical interpolation.

## 5. Complete finite fourth cost and the global lower bound

For (15), both active coefficients through cubic are zero and the
scalar cubic coefficient is C3 for **all** twelve variables. Retain
independent fourth common real and imaginary normal corrections as
well as odd corrections before forming the dual. Their coefficients
cancel. The resulting complete fourth cost is the exact polynomial

\[
\begin{aligned}
Q(t,r)&=q_0+\ell R+a_T\sum t_i^2+b_T S^2
                    +\tfrac12\sum r_i^2+\tfrac14 R^2,\\
q_0&=183619658945/2519424+(444829186913/1259712)c
                                    -(288729410449/629856)c^2,\\
\ell&=50960/243+(1218245/972)c-(125944/81)c^2,\\
a_T&=-11564/405-(20482/81)c+(123284/405)c^2,\\
b_T&=49/180-(105889/486)c+(305123/1215)c^2.                  \tag{22}
\end{aligned}
\]

candidate.py reconstructs the full original polynomial and exact scalar
series, derives the active third/fourth root maps, solves m,theta, and
compares all49 monomials of the dual cost with (22). The identity has
no missing imaginary-real cross term or odd linear term. Rational
isolation of8c3-6c-1 on(3/4,1) gives aT>0 and aT+6bT>0. The real block
has eigenvalues1/2 and2. Hence the unique finite minimum is
t=0, r_i=rstar=-ell/4, and

\[
\begin{aligned}
Q-C_4&=a_T\sum t_i^2+b_TS^2
       +\tfrac12\sum(r_i-r_*)^2+\tfrac14(R-6r_*)^2\ge0,\\
C_4&=q_0-3\ell^2/4.                                      \tag{23}
\end{aligned}
\]

This reduces exactly to (2). From (20)-(21), the canonical cost
identity, and Aavg<=0, every fixed fourth-budget competitor satisfies

\[
F-\operatorname{base4}(\eta)
\ge\eta^4[Q(t,r)-C_4]-K_U\eta^5.                          \tag{24}
\]

For a universal collar take U=0. If F<=base3, (24) implies (3).
If F>base3, the same lower bound follows from C4<0. Infinite F is
immediate. This exhausts all competitors, with no symmetry assumption.

For (5), a fixed fifth budget eventually lies in the U=0 class since
C4<0. Combining it with (24) and positive definiteness gives
t=O(sqrt eta), r-rstar1=O(sqrt eta). The original first jets differ
from the projected chart by O(eta). The chart (13) then gives (5),
where

\[
\begin{aligned}
\alpha=W_*/8+r_*&=-9914/243-(902885/3888)c+(23464/81)c^2,\\
\beta=W_*/8-3r_*&=13682/81+(1323365/1296)c-(34160/27)c^2.     \tag{25}
\end{aligned}
\]

Equivalently the large pair is
Im zeta=plus/minus b sqrt eta(1+gamma eta)+O(eta2),
Re zeta=up eta+beta eta2+O(eta5/2); the other six have
Im zeta=O(eta2), Re zeta=uz eta+alpha eta2+O(eta5/2).
No optimality of these individual exponents is claimed.

## 6. Attainment and every original-root branch

At t=0,r=rstar1 the exactly solved constants are

\[
\begin{aligned}
m_*&=-18681113/8748-(23084270/2187)c+(3318742/243)c^2,\\
\theta_*&=-6128723/23328-(33473077/23328)c+(173445991/93312)c^2,\\
n_*&=69179489551/629856+(82217239787/157464)c
                                          -(214144521727/314928)c^2,\\
\phi_*&=100267260167/17915904+(269718907597/8957952)c
                                            -(42812814917/1119744)c^2.
\end{aligned}                                                \tag{26}
\]

The first two cancel both cubic radial equations for the new first
profile. The latter two cancel both fourth radial equations. Define
the full polynomial, without truncating its defining factors, by

\[
\begin{gathered}
L_0=u_z\eta+\alpha\eta^2+m_*\eta^3+n_*\eta^4+1000\eta^5,\\
L_p=u_p\eta+\beta\eta^2+m_*\eta^3+n_*\eta^4+1000\eta^5,\\
q'_\eta(z)=9(z-L_0)^6\left[(z-L_p)^2+(H/2)\eta
             (1+\gamma\eta+\theta_*\eta^2+\phi_*\eta^3)^2\right],\\
q_\eta(z)=\int_{1-\eta}^{z}q'_\eta(w)\,dw.                  \tag{27}
\end{gathered}
\]

Its full coefficients are polynomial in eta. The factor/integration
route matches every original-polynomial coefficient of the independent
twelve-variable Newton route through eta4. q0=z9-1 has nine simple
original roots. The finite exact checker solves every branch through
eta5 by two different methods: complete polynomial Horner residual
elimination and direct binomial derivative/Taylor expansion at omega.
They agree at every branch and order, and every full residual vanishes.

The marked branch is exactly1-eta. The four inactive branches k=1,2,7,8
have strictly negative first radial coefficients. All four active
branches k=3,4,5,6 have their first four radial coefficients zero.
The common fifth correction has exact radial response -Ak times1000;
the resulting fifth coefficients are strictly negative in the chosen
real embedding. Every branch, including both members of each conjugate
pair, is checked separately. The strict signs are obtained by rational
interval evaluation of field normal forms, not floating-point roots.

The analytic implicit-root theorem now supplies all nine branches in
one common neighborhood, exhausting the degree. The finite set of
strict leading radial signs, with uniform Taylor remainders, puts
every original root strictly inside the unit disk at every sufficiently
small positive eta. Repeated critical points cause no problem.
There is no sample grid or an assumption about roots of a truncated jet.

The exact reciprocal sum is

\[
\frac6{1-\eta-L_0}
+\frac2{\sqrt{(1-\eta-L_p)^2+(H/2)\eta
                (1+\gamma\eta+\theta_*\eta^2+\phi_*\eta^3)^2}}.
\]

Its coefficients through fourth are8,C,Bstar,C3,C4, as independently
checked from the full factors. The positive denominators are automatic
in a sufficiently small collar. This proves the upper half of (4), and
completes the radiuswise minimum expansion and cubic-line failure.

## 7. Sharpness of the next-profile rate by split real critical points

Let lambda be any fixed positive real number. Keep every constant and
L0,Lp,opening from (27), but replace the derivative by

\[
\widetilde q'_\eta(z)=9(z-L_0)^4
 [(z-L_0)^2-\lambda^2\eta^5]
 [(z-L_p)^2+(H/2)\eta(1+\gamma\eta+\theta_*\eta^2+\phi_*\eta^3)^2],
\qquad \widetilde q_\eta(z)=\int_{1-\eta}^z\widetilde q'_\eta(w)\,dw.
                                                               \tag{28}
\]

Its critical points are four copies of L0, the two real points
L0 plus/minus lambda eta5/2, and the same opposed pair as before.
Its complete defining coefficients remain polynomial in eta. The full
factor expansion gives the uniform coefficient identity, for fixed lambda,

\[
\widetilde q_\eta-q_\eta
=-(9\lambda^2/7)\eta^5(z^7-1)+O_{\rm coeff}(\eta^6).        \tag{29}
\]

All original-root coefficients below fifth are unchanged. The fifth
radial response at omega_k is
lambda2(cos7theta_k-1)/7. For each active k it equals
-lambda2 Bk/7<0, so every active original root is *strictly more*
inward than for (27) at its leading fifth order. The four inactive
first signs and exact marked root are unchanged. The same finite
simple-root argument gives all-disk containment for all sufficiently
small positive eta. The generic identity (29), every lambda1 residual,
all nine radial responses and all strict signs are checked exactly
in stability_family.py. The general lambda assertion follows from the
full symbolic quadratic response, not interpolation from lambda1.

Put D0=1-eta-L0, positive in the collar. The change in F is exactly

\[
\frac1{D_0-\lambda\eta^{5/2}}
+\frac1{D_0+\lambda\eta^{5/2}}-\frac2{D_0}
=\frac{2\lambda^2\eta^5}{D_0(D_0^2-\lambda^2\eta^5)}
=2\lambda^2\eta^5+O(\eta^6).                              \tag{30}
\]

The base family has an analytic fifth F coefficient. Therefore (28)
lies in a fixed fifth upper-budget class for an appropriate finite T.
For the joint first-jet error

\[
 E_\eta^2=
 \|(h-h^*)/\eta-\gamma h^*\|^2+
 \|(u-u^*)/\eta-(\beta,\beta,\alpha^6)\|^2
\]

after the aligned permutation, its exact value is

\[
E_\eta^2=H(\theta_*\eta+\phi_*\eta^2)^2
 +8(m_*\eta+n_*\eta^2+1000\eta^3)^2+2\lambda^2\eta.
\]

Hence Eeta/sqrt eta tends to sqrt2 lambda>0. This rules out replacing
the next-profile O(sqrt eta) first-jet rate by o(sqrt eta), even with
an arbitrary class-dependent constant. On the two split real small
critical points the error from uz eta+alpha eta2 is
plus/minus lambda eta5/2+O(eta3), proving the stated individual real
exponent is optimal. No optimal imaginary exponent is inferred.

## 8. Exact evidence and trust boundary

The self-contained standard-library packet uses exact rational and
Q[c]/(8c3-6c-1) arithmetic, sparse multivariate jets and exact Gaussian
extensions for every nonagon root. It checks complete identities,
positive blocks, all higher directions and all nine original-root
branches. The complete small external fixture and mathematical damages
remain active under Python optimization; README gives exact commands.
Arithmetic adapts the author's credited8751 kernels, with no imported
parent source, fixture, external data or solver. Two algorithms sharing
arithmetic are internal cross-checks, not independent external review.

Inherited concentration/bootstrap, coefficient/root-map uniformity,
active contact and sine estimates, the affine projections, comparison
(20)-(21), quantified collars and all-root analytic containment remain
ordinary written proofs outside a formal kernel. This new fourth theorem
and stability consequence are independently unreviewed at publication.
The full first-power endpoint away from the boundary, an effective
collar, optimality of the other individual exponents and the fifth minimum coefficient
are not established here. No timeout, incomplete enumeration or resource
limit is used as mathematical evidence.
