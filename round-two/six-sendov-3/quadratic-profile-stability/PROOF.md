# Effective quadratic boundary error and physical stability

Actual **six-sendov-3**, role **researcher**, 2026-10-02.
Complete ordinary author proof, **UNFORMALIZED and independently UNREVIEWED**.
Finite exact evidence corroborates the coefficient identities and numerical
budgets; the analytic and imported proof boundaries are explicit below.
This is a quantitative refinement of prior9620/9671 after the separately
credited9731 global entry. The sharp slope, dual angles, leading profiles,
qualitative higher-order rates and exact-minimizer stability are prior work.

## 1. Actual domain and conclusions

Let p be complex monic of degree nine, with all nine original zeros in the
CLOSED unit disk and marked zero a=1-eta, where 0<eta<=e=2^-16.
Count ALL eight critical points zeta_j with algebraic multiplicity. Set

\[
 F=\sum_j|a-\zeta_j|^{-1},\qquad H=\sum_j|\zeta_j|^2.
\]

A zero reciprocal denominator gives infinity. No initial critical radius,
energy, coefficient cap, conjugation, original/critical separation, critical
template, optimizer, attainment, branch matching or smooth-family premise is
imposed. With the CREDITED8530/8608 constants

\[
 c=\cos(\pi/9),\quad d=2c^2-1,\quad y=\frac1{3(1+c)},
 \quad x=\frac23-y,\quad h_0=14y,\quad C=\frac83+y,
\]

the unrestricted actual-domain estimate on this numerical window is

\[
 \boxed{F>8+C\eta-390\eta^2>8+\frac{14}{5}\eta.}       \tag{1}
\]

For the following physical stability statements retain F<=8+3eta.
Write

\[
 m=\tfrac18\sum\zeta_j=M+iD,\quad \nu_j=\zeta_j-m,
 \quad V=\sum|\nu_j|^2,\quad T=\sum\nu_j^2,
\]
\[
 u=a-m,\quad r=|u|,\quad \xi_j=\nu_j\bar u/r=X_j+iY_j,
 \quad Q+iJ=T\bar u/u,\quad E=\sum X_j^2=(V+Q)/2.
\]

Let omega_k=exp(2 pi i k/9), and Z_k be the ACTUAL original labeled near
m+u omega_k by the counted-circle theorem of9620, with Z_0=a. Opposite
labels are not declared conjugate. For k=3,4 use the actual paired slacks

\[
 s_k=-\tfrac12\left\{\frac{|Z_k|^2-1}{2}
                  +\frac{|Z_{9-k}|^2-1}{2}\right\}\ge0,
\]
\[
 w_4=\frac1{c+d},\qquad
 w_3=\frac23\left(7-\frac{1-d}{c+d}\right),\qquad
 \Psi=w_3s_3+w_4s_4+E/4\ge0.
\]

The stronger physical inequality is

\[
 \boxed{F-8>C\eta+\Psi-390\eta^2.}                    \tag{2}
\]

For arbitrary epsilon>=0 retain ALSO F<=8+Ceta+epsilon eta, and put
Delta=epsilon eta+390eta^2>0. Then

\[
 \Psi<\Delta,\quad E<4\Delta,\quad
 |M+x\eta|<\tfrac85\Delta,\quad |Q+h_0\eta|<26\Delta,
\]
\[
 |V-h_0\eta|<34\Delta,\quad |H-h_0\eta|<35\Delta,
 \quad \sum(\Re\zeta_j)^2<13\Delta,                 \tag{3}
\]
\[
 |D|<\sqrt{\eta\Delta}+\Delta+44\eta^2,              \tag{4}
\]
and EVERY one of the nine actual originals satisfies

\[
 \boxed{\left|Z_k-\left[\omega_k+
       \eta(-\omega_k/3-x-y\omega_k^{-1})\right]\right|
       <10\Delta+4\sqrt{\eta\Delta}.}                \tag{5}
\]

These are all-profile critical moment and actual-original estimates. There
is no assertion of a unique selected critical multiset or a global optimizer.
Both the low sublevel and the added near-slope inequality remain necessary
premises for (3)-(5), including when epsilon is large. Inequality (2)
requires the low sublevel only.

## 2. Credited actual entry before local estimates

The complete ordinary proof of six-sendov-1's
[9731 whole-origin entry](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-1/weighted-origin-routing/PROOF.md),
source45ce3d1c8eafadc7cfc4f0f3a207b25a456c744d, was read with its actual
9687/8656 inputs and its unchanged exact baseline reproduced. It states,
with EXACTLY the actual domain and low sublevel of Section1,

\[
 H<64\eta\le1/1024<1/512.                             \tag{6}
\]

Its canonical signed committed statement and complete defining-proof bytes
were checked. Fresh
[REVIEW9764](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/whole-origin-entry-audit/REVIEW.md),
source746b284c87d7ec736873e8d46c4ed9ae45653d05, independently CONFIRMS
its full actual H64 entry domain. Its whole review, independent core proof
and late transport were read and aligned with the complete signed body;
whole pinned/current readers match. Its directH60 and credited9756 global14
refinements are prior results, not numerical premises here. That verdict
does not review this new390 theorem. There is no circular use of the local
estimates before entry. The earlier9687 global carrier and the alternate
H<=1/16 reflection entry are not premises here.

Only AFTER (6), apply the imported
[9620 fixed-energy proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/critical-radius-routing/PROOF.md),
sourcecd6be6d4272505f394bbea6e13ff69a9f73ee5bf, and the complete all-phase
normal/motion proof of
[9671](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/effective-profile-stability/PROOF.md),
source48241d95ef16ffb51e183c89101762a321152dc0. Their scoped consequences are

\[
 V<6\eta,\quad |M|<4\eta/5,\quad |D|<\eta/3,
 \quad |m|<13\eta/15,\quad 1-\eta<r<1+\eta.           \tag{7}
\]

All actual originals are simple and labeled by disjoint counted circles
AFTER entry; critical collisions remain included. For V=0 the centered
polynomial is exactly w^9-u^9 and its displacement errors vanish.
The complete original-motion estimate, for every phase, is

\[
 \left|Z_k-m-u\omega_k-
       \frac{T}{14u}(\omega_k^{-1}-\omega_k)\right|
 \le\frac{\mu_3}{9a_*^2}+V^2,
 \qquad a_*=1-e,\quad \mu_3=\sum|\nu_j|^3.            \tag{8}
\]

It is strict for V>0; the non-strict zero form suffices below. Full Newton
identities give the centered integrated coefficients d_7=-9T/14 and
d_6=-U_3/2, where U_3=sum nu_j^3. All remaining lower coefficients and
nonlinear displacements are retained in the imported9671 budgets. In
particular its nonzero phase-four d_3 is not discarded.

For A_k=1-cos(2pi k/9), B_k=1-cos(4pi k/9), set
L_k=-A_k M-B_k Q/14. Re-extracting the signed cubic from the COMPLETE
actual normals of9671, Section3, gives

\[
 -s_3=-\eta+L_3+R_3,\quad |R_3|<40\eta^2,
\]
\[
 -s_4=-\eta+L_4-\frac{\Re(U_3\bar u/u^2)}{12}
                +\widetilde R_4,
 \qquad |\widetilde R_4|<46\eta^2.                   \tag{9}
\]

No zero-third-moment or conjugation premise is introduced. The phase-three
cubic cancels exactly, while the phase-four cubic is retained. These full
normal bounds, not jets alone, include all original half-normal quadratic
terms, the bar(m) displacement term and the entire nonlinear root error.

The two actual unaveraged cube normals additionally give the imported bound

\[
 |aD-J/14|\le(2/\sqrt3)(s_3+E_3),\qquad E_3<37\eta^2. \tag{10}
\]

Independent audits9667/9669 assess9620, not9671/9731 or this new theorem.
The complete pinned
[REVIEW9756](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/effective-stability-audit/REVIEW.md),
source345e13e266c576620644bbbc47812b3707623dda, independently CONFIRMS9671
in its exact domain and proves a14eta^(3/2) refinement using the stronger
credited9669 constants. Its whole ordinary proof was read and its complete
reader-expanded source matches the signed defining body. Neither those
stronger constants nor the new14 budgets are premises here; the weaker
explicit bounds (7)-(10) suffice.9756 does not review9731 or this390 theorem.
Review9719 assesses9687's seeds, not the later entry or local refinement.
None of those verdicts transfers here.

## 3. All-degree reciprocal expansion and signed cubic feedback

For real t in [-1,1], the classical Laplace integral is

\[
 P_n(t)=\frac1\pi\int_0^\pi
       (t+i\sqrt{1-t^2}\cos\phi)^n\,d\phi.             \tag{11}
\]

One can derive its generating function directly: for |z|<1 the summands
are uniformly absolutely bounded by |z|^n, so sum inside the integral.
The resulting integral of 1/(1-zt-iz sqrt(1-t^2) cos(phi)), evaluated by
v=tan(phi/2), is (1-2tz+z^2)^(-1/2), with branch equal to1 at z=0.
The elementary scalar integral can first be evaluated near z=0 and then
extended analytically on the unit disk, where its denominators and the
quadratic under the square root do not vanish. Thus (11) gives precisely
the Legendre generating coefficients for ALL n. Its integrand has modulus
at most1, since t^2+(1-t^2)cos^2(phi)<=1. Hence |P_n(t)|<=1 for ALL n.
Finite recurrence/binomial/Laplace comparisons in the checker corroborate
low coefficients only; the all-degree statement is this ordinary proof.

Centering eliminates the linear term. The complete expansion is therefore

\[
 F=\frac8r+\frac{V+3Q}{4r^3}
      +\frac1{r^4}\sum(X_j^3-\tfrac32X_jY_j^2)
      +\mathcal R_{\ge4}.                            \tag{12}
\]

The zero nu_j terms are treated directly, without defining their angle.
From (7), max|nu_j|<=sqrt(V)<tau=1/96, because 6e<tau^2; also r>a_*.
Absolute convergence justifies every exchange. The ENTIRE tail satisfies

\[
 |\mathcal R_{\ge4}|
 \le\sum_j\frac{|\nu_j|^4}{r^5}\sum_{l\ge0}(\tau/r)^l
 \le\frac{V^2}{(r-\tau)r^4}\le G V^2,
 \qquad G=\frac1{(a_*-1/96)a_*^4}.                   \tag{13}
\]

Here sum|nu_j|^4<=V^2 by the complete nonnegative cross-product identity.
No tail is omitted and no finite degree cutoff proves (13).

The complete signed cubics obey

\[
 \left|\sum(X_j^3-\tfrac32X_jY_j^2)\right|
 \le\tfrac32\sum|X_j||\xi_j|^2\le\tfrac32 V\sqrt E,
\]
\[
 |\Re\sum\xi_j^3|
 \le3\sum|X_j||\xi_j|^2\le3V\sqrt E.                \tag{14}
\]

The first bounds use the full pointwise polynomials. Squaring the two
majorants leaves respectively (5/4)X^6+(15/2)X^4Y^2 and
8X^6+24X^4Y^2, which are nonnegative. Cauchy and sum|xi_j|^4<=V^2
give the second bounds. Crucially, the real critical energy E is retained.
Exactly Re(U_3 bar(u)/u^2)=Re(sum xi_j^3)/r, with all complex phases.

Convexity of 8t^(-1/2) at t=a^2 and the full mean/range bounds (7) give,
as in9671 but keeping (12)'s cubic and fourth-order tail separately,

\[
 F-8\ge8\eta+8M+(V+3Q)/4-40\eta^2
             -\frac{3}{2a_*^4}V\sqrt E-GV^2.        \tag{15}
\]

For clarity the complete noncubic conversion cost is
[8(4/5)(2-e)/a_*^2+4(169/225)/a_*^3+24]eta^2<40eta^2.
The 24 term bounds the r^-3 quadratic-moment adjustment. The positive
8/a-(8+8eta) is discarded. No old eta^(3/2) remainder is substituted.

## 4. Positive physical defect and a uniform quadratic error

The PRIOR8530/8608 dual identities are

\[
 w_3A_3+w_4A_4=8,\quad w_3B_3+w_4B_4=7,
 \quad 8-w_3-w_4=C.                                  \tag{16}
\]

The selected cosine root has 15/16<c<47/50. These strict bounds follow
from 8c^3-6c-1=0, monotonicity on its selected interval, and the rational
endpoint signs. They give 4<w_3<23/5 and 1/2<w_4<3/5.
Using (9), (14)-(16), and E=(V+Q)/2, yields

\[
 F-8\ge C\eta+w_3s_3+w_4s_4+E/2
              -252\eta^2-GV^2-KV\sqrt E,
\]
\[
 K=\frac3{2a_*^4}+\frac3{20a_*}.                     \tag{17}
\]

All signs in the substitution are fixed by L_k=eta-s_k-R_k; in
particular the signed fourth cubic is weighted by w_4 after substitution.
The full quadratic-normal cost40+40w_3+46w_4 is below252.
No uncontrolled imaginary third moment appears in (17).

The exact nonnegative-square identity is

\[
 E/4-KV\sqrt E=(\sqrt E/2-KV)^2-K^2V^2.
\]

Since V<6eta and the STRICT rational endpoint comparison is

\[
 252+36(G+K^2)<390,                                   \tag{18}
\]

(17) proves (2) and the first part of (1) on the low sublevel. All zero
variance/zero E cases are included; no division by these quantities occurs.
For F>8+3eta, including infinity, (1) follows from C<3. Finally
C>17/6, and 17/6-390e>14/5, prove the second inequality in (1) on the
ENTIRE closed numerical window. This proves unrestricted objective
coverage, using9731 only on the low arm.

## 5. Fresh moment and physical critical stability

The added near-slope bound and (2) give Psi<Delta. Positivity yields
s_3<Delta/4, s_4<2Delta and E<4Delta. From (9), (14), V<6eta,
Delta>=390eta^2 and sqrt390>19, the FULL error budgets are

\[
 |R_3|<40\eta^2,\qquad
 |R_4|<46\eta^2+\frac{V\sqrt E}{4a_*}
          <\left(\frac{46}{390}+\frac3{19a_*}\right)\Delta
          <\Delta/2.                                \tag{19}
\]

Thus |L_3-eta|<(1/4+40/390)Delta<3Delta/8, and
|L_4-eta|<5Delta/2. The old9671 bounds R_3<Delta/100 and
R_4<Delta/12 are NOT reused with the new Delta; their attempted
substitution fails exact counterchecks.

The optimal pair has A_k x+B_k y=1. Its Cramer determinant magnitude is
3(c+d)/2>651/256, while B_4<31/128 and A_4<97/50. Hence

\[
 |M+x\eta|<\left[\frac{62}{651}\frac38
                      +\frac{128}{217}\frac52\right]\Delta
               <\frac85\Delta,
\]
\[
 |-Q/14-y\eta|<\left[\frac{24832}{32550}\frac38
                      +\frac{128}{217}\frac52\right]\Delta
               <\frac95\Delta.                      \tag{20}
\]

This gives |Q+h_0eta|<26Delta. Since V=2E-Q,
|V-h_0eta|<34Delta; H=V+8|m|^2 gives |H-h_0eta|<35Delta using
8(169/225)eta^2 and Delta>=390eta^2.

From |Q+iJ|<=V, J^2<=4EV<96eta Delta. The unaveraged actual cube
constraints (10), s_3<Delta/4 and 2/sqrt3<7/6 imply

\[
 |D|<\frac{\sqrt{96}}{14a_*}\sqrt{\eta\Delta}
         +\frac7{24a_*}\Delta+\frac{259}{6a_*}\eta^2.
\]

The coefficients are respectively below1,1,44, proving (4).
The first strict inequality uses 96<196a_*^2; it is not a floating sign.

For unrotated real critical energy, Re(u)>0 and
|u/r-1|^2<=2D^2/r^2. Apply the three-term squared-norm inequality
to Re(zeta_j)=M+X_j+Re[xi_j(u/r-1)], using the UNCONDITIONAL local
bounds |M|<4eta/5 and |D|<eta/3 from (7). This gives

\[
 \sum(\Re\zeta_j)^2
 <12\Delta+\frac{384}{25}\eta^2+\frac{4\eta^3}{a_*^2}
 <13\Delta.                                         \tag{21}
\]

All estimates are pointwise in the actual polynomial. No near-slope
smooth path or nondegenerate critical matching is needed.

## 6. Fresh all-nine-original motion bound

Exactly T/u=(Q+iJ)/bar(u), while |u-1|<28eta/15. Equations (20) and
J^2<96eta Delta, with sqrt96<10, give

\[
 \left|\frac{T}{14u}+y\eta\right|
 <\frac{26\Delta+10\sqrt{\eta\Delta}}{14a_*}
       +\frac{28y}{15a_*}\eta^2.                     \tag{22}
\]

Also |m+xeta|<13Delta/5+sqrt(eta Delta)+44eta^2 by (3)-(4).
Use x+y=2/3 and compare
m+(a-m)omega_k+[T/(14u)](omega_k^-1-omega_k)
with the target in (5). Each of its two phase-difference factors has
modulus at most2. The imported full remainder (8) has

\[
 \mu_3\le\sqrt{7V/8}\,V<\frac{55}{4}\eta^{3/2},
 \qquad V^2<36\eta^2,                                \tag{23}
\]

where centering gives 8|nu_j|^2<=7V. Including EVERY remainder yields

\[
 \left(\frac{26}{5}+\frac{26}{7a_*}\right)\Delta
 +\left(2+\frac{10}{7a_*}\right)\sqrt{\eta\Delta}
 +125\eta^2+\frac{55}{36a_*^2}\eta^{3/2}.             \tag{24}
\]

The125 coefficient is valid because
88+36+896/(1395a_*)<125, using y<16/93.
Now eta^2<=Delta/390 and eta^(3/2)<sqrt(eta Delta)/19. The two strict
rational budgets

\[
 \frac{26}{5}+\frac{26}{7a_*}+\frac{125}{390}<10,
 \qquad 2+\frac{10}{7a_*}+\frac{55}{684a_*^2}<4
\]

prove (5), for ALL nine labels including the marked original and V=0.
The entire complex U_3 displacement is bounded here by mu_3; no inference
that its imaginary part is controlled by E is made.

## 7. Exact evidence, coverage and prior-art boundary

The self-contained standard-library checker reconstructs complete rational
and Gaussian polynomial maps for the eight critical coordinates, rotated
energy/P3/ReU3 and centered integrated cubic. Every identity compares its
WHOLE coefficient map before hashing. It also regenerates complete ninth-root
phase coefficients, the credited dual relations, and all strict rational
endpoint budgets. Three coefficient constructions of each Legendre polynomial
through degree12 agree fully; complete finite telescoping controls retain
every term. Those finite degrees are corroboration, not an all-degree proof.

Literal arbitrary-critical controls test whole centered/rotated moments,
including total collision, pure imaginary real-energy zero and genuinely
complex phases. They assert NEITHER actual original-disk feasibility NOR
the low sublevel. Finite samples or timeout/UNKNOWN are no universal premise.
The default checker compares the entire typed fixture after reconstruction;
explicit --emit is author regeneration, not a tamper check. Arithmetic reuse,
own baseline reproduction and two construction routes are not independent review.

Imported actual entry, Rouché labeling, complete nonlinear normal/motion
bounds, the ALL-degree integral/convergence proof, Cauchy/Maclaurin,
square completion and all-parameter case coverage remain ordinary mathematics
outside a formal kernel. The local9671 theorem is independently CONFIRMED
by9756 in its stated domain, and9731's full entry is independently CONFIRMED
by9764. This new quadratic theorem remains independently unreviewed;
those verdicts and audits of their parents do not review this new leaf.
No optimal effective390
constant or uniformly improved stability constant for every epsilon is
claimed; Psi retains E/4, and its fresh Delta/error budgets are explicit.

Prior8530/8608 give the sharp C, exact dual and limiting moment/motion
profile.8619/8668/8684 already supply qualitative higher-order budget rates;
8921/8955 give an exact analytic minimizer and stronger selected-profile
slack estimates on existential collars. This result supplies an EFFECTIVE
quadratic error and physical moment/all-original constants on the prescribed
whole numerical window. It does not add a sharp second coefficient, template
uniqueness, optimizer classification or historical-priority assertion.

Extending this quadratic theorem beyond eta2^-16 requires wider actual
entry AND complete local budgets. No largereta sharp/stability extension
is proved here; optimal widths and the unrestricted strongest first-power
endpoint remain open here.
The separate9707 radius1/25 energy extension to2^-14 alone does not extend
the local hypotheses used in this proof. The current primary first-power
Conjecture1.2 is distinct from the proved quadratic Theorem1.3.
