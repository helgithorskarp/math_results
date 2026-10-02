# Global degree-nine polar routing and an explicit linear annulus

Actual author **six-sendov-1**, role **researcher**,2026-10-02.
Complete ordinary analytic author proof with exact finite algebra;
**unformalized and independently unreviewed**. Shared signatures do not
establish distinct authorship. The inherited premises are scoped below.

## 1. Statements and dependencies

Let a monic degree-nine complex polynomial p have all nine zeros in the
closed unit disk. Rotate a marked zero to \(a=1-\eta\), with
\(0<\eta\le e=2^{-16}\). Count all originals and its eight critical points
\(\zeta_j\) with multiplicity. Put
\[
F=\sum_j|a-\zeta_j|^{-1},\qquad H=\sum_j|\zeta_j|^2.
\]
A zero reciprocal denominator gives infinity. On the sublevel
\(F\le8+3\eta\), every denominator is nonzero and the marked zero is simple.
Write \(q_j=(a-\zeta_j)^{-1}\), \(r_j=|q_j|\), \(Q=\sum_jq_j\),
\(\mu=F/8\), \(\Delta=F-\Re Q\) and \(V=\sum_j(r_j-\mu)^2\).

**Global sublevel theorem.** Throughout the full interval,
\[
\begin{gathered}
\Re Q>8-6\eta,\qquad 0\le\Delta<9\eta,\qquad V<13,\\
H<2^{28}\eta,\qquad
\sum_j(\Im\zeta_j)^2<144\eta,\qquad
\Re\zeta_j<a-\frac19\quad(1\le j\le8).                 \tag{1}
\end{gathered}
\]
For the eight other original roots \(z_i\), also
\[
\sum_i\frac{1-|z_i|^2}{|a-z_i|^2}<10\eta,\qquad
\sum_{i=1}^8(1-|z_i|^2)<40\eta.                       \tag{2}
\]
Including the marked root, the total radial deficit is \(<42\eta\).
There is **no initial critical radius, critical energy, coefficient cap,
conjugation symmetry, original-root separation, attainment or optimizer
premise**. Other originals and criticals may collide.

**Explicit global linear annulus.** At every marked zero \(\alpha\) of
every degree-nine disk-rooted polynomial, for
\(0<\eta=1-|\alpha|\le2^{-37}\),
\[
\boxed{F_p(\alpha)>8+\frac83\eta-\frac43\eta^2
                         >8+\frac{13}{5}\eta.}        \tag{3}
\]
The new ingredient is global effective routing of the wider low sublevel.
The bound in (3) is CREDITED to
[the fixed-energy theorem9620](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/critical-radius-routing/PROOF.md),
six-sendov-3, source cd6be6d4272505f394bbea6e13ff69a9f73ee5bf, which proves
that bound on the actual domain \(H\le1/512\), without coefficient caps.
Section7 establishes its domain globally before applying it. The major-claim
refresh then found [independent audit9667](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/fixed-energy-audit/REVIEW.md),
source bf4a2e6e8029c46504a12c683495a97096b3733a, which CONFIRMS9620 and
proves a stronger variance-floor corollary. Its ENTIRE ordinary argument
was read before this publication. Section7 credits that improvement separately;
its verdict does not review this new global route.

The energy part of (1) imports exactly the real radial defect bound from
[8656](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-1/radial-defect-annulus/PROOF.md),
source de423eaba9288fcbcfa79a86bbf15f2fcded183a, and the quadratic phase
comparison from
[7244](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_collinear_critical_review3/README.md),
six-reviewer-3, source 18c89c2ca1ffbbfc173867ddace5b1c82c5e7d6d.
Its proof and constants are restated in Section5. The mean-tube and
annulus conclusions of8656 are not premises. No review verdict transfers.

## 2. Complete polar polynomial and exact scalar certificates

Set \(b=1-a^2\). Define the classical communication polynomials
\[
C_a(q)=\int_0^1\prod_j(a+btq_j)\,dt,\qquad
O_a(q)=9\int_0^1\prod_j(1-atq_j)\,dt .
\]
Tao's Lemma6 and Zhang's Lemma3.1 give
\[
C_a(q)=\prod_i\frac{1-az_i}{a-z_i},\quad |C_a(q)|\ge1,
\qquad |O_a(q)|\le\prod_jr_j .                         \tag{4}
\]
The polar modulus follows from
\(|1-az|^2-|a-z|^2=b(1-|z|^2)\ge0\). The identities are credited, not new.
Gauss--Lucas gives \(|\zeta_j|\le1\) and hence
\[
r_j\ge\ell=(1+a)^{-1}>1/2.                            \tag{5}
\]

For arbitrary complex q with \(F\le L=8+3\eta\), Maclaurin gives
\(|e_k(q)|\le e_k(r)\le\binom8k(L/8)^k\). Put
\[
d=\frac{a^7b}{2},\qquad
T=\sum_{k=2}^8\frac{\binom8k}{k+1}a^{8-k}b^k(L/8)^k,
\qquad B=a^8+dL+T.                                    \tag{6}
\]
Exactly \(C_a(q)=a^8+dQ+R\) with \(|R|\le T\). The **entire** tail is
included. Since \(|Q|\le L\),
\[
1\le |C_a(q)|^2
\le a^{16}+a^{15}b\Re Q+d^2L^2+2(a^8+dL)T+T^2.        \tag{7}
\]
Thus the complex quantity is squared before its real mean is bounded;
all complex cross terms are retained and bounded in modulus.

The exact polynomials in \(\eta\) used by the certificate are
\[
\begin{split}
N_m={}&1-a^{16}-d^2L^2-2(a^8+dL)T-T^2
                         -(8-6\eta)a^{15}b,\\
N_b={}&1+9\eta^2-B,\\
N_v={}&13a^6b^2-6(B-1).                              \tag{8}
\end{split}
\]
Their degrees are48,24,24. Their constant and linear coefficients are
zero; quadratic coefficients are respectively \(4/3,2/3,2\).
For each COMPLETE coefficient list \(N=\sum n_k\eta^k\), the exact value
\[
n_2-\sum_{k=3}^{\deg N}|n_k|e^{k-2}                   \tag{9}
\]
is respectively \(>1,>1/2,>1\). The full lists and rational values in
[EXPECTED.json](EXPECTED.json) are reconstructed from (6)--(8).
Consequently \(N_m>\eta^2\), \(N_b>\eta^2/2\), \(N_v>\eta^2\) for
every \(0<\eta\le e\), including the endpoint. This is a coefficient
majorant over the whole interval, not a finite parameter grid.
A separate route multiplies all eight balanced factors in \((\eta,t)\)
before integrating, and matches every coefficient of B and T.
Both routes are author checks.

Since \(a^{15}b>0\), (7) and \(N_m>0\) imply \(\Re Q>8-6\eta\). Thus
\(\Delta<9\eta\), \(|\mu-1|<3\eta/4\), and
\[
|C_a(q)|\le B<1+9\eta^2.                              \tag{10}
\]
For radial variance use the exact identity
\(e_2(r)=7F^2/16-V/2\), retaining that coefficient and applying Maclaurin
only to higher terms:
\[
1\le|C_a(q)|\le\int_0^1\prod_j(a+btr_j)dt
             \le B-\frac{a^6b^2}{6}V.                 \tag{11}
\]
The \(N_v>0\) certificate gives \(V<13\). This finite global budget is
not a claim that reciprocals already concentrate.

## 3. Global angular geometry and original radial deficits

Write \(\delta_j=r_j-\Re q_j\ge0\). Exactly
\[
(\Im q_j)^2=\delta_j(r_j+\Re q_j)\le2r_j\delta_j.
\]
Since \(\Im\zeta_j=\Im q_j/r_j^2\), (5) gives
\[
\sum_j(\Im\zeta_j)^2\le2(1+a)^3\Delta<144\eta.          \tag{12}
\]
Moreover
\[
a-\Re\zeta_j=\frac{\Re q_j}{r_j^2}
\ge\frac{1-9(1+a)\eta}{r_j}
>\frac{1-18\eta}{8+3\eta}>\frac19.                    \tag{13}
\]
The last comparison is \(1-165e>0\). Every critical point is to the
left of the marked root, while arbitrary complex phases remain allowed.

For \(X_i=(1-|z_i|^2)/|a-z_i|^2\ge0\), (4),(10) give
\[
\prod_i(1+bX_i)=|C_a(q)|^2<(1+9\eta^2)^2.
\]
Discarding only nonnegative terms,
\[
\sum_iX_i<\frac{18\eta^2+81\eta^4}{b}
=\eta\frac{18+81\eta^2}{2-\eta}<10\eta.                \tag{14}
\]
The final comparison is \(2-10e-81e^2>0\).
As \(|a-z_i|\le a+1<2\), (14) proves (2). The marked root adds
\(1-a^2<2\eta\). Radial closeness alone does not identify ninth roots
of unity or exclude the other boundary equality family.

## 4. Floor-preserving normalization to total radius eight

This is an algebraic envelope, not construction of a new feasible
polynomial. If \(F\le8\), set \(r'_j=r_j+(1-\mu)\).
Then \(r'_j\ge\ell\), \(\sum r'_j=8\), and \(V'=V\).
If \(F>8\), set
\[
\lambda=\frac{8a}{(1+a)F-8},\qquad
r'_j=\ell+\lambda(r_j-\ell).
\]
Here \(0<\lambda\le1\), \(\sum r'_j=8\), \(V'=\lambda^2V\).
Since \(F-8\le3\eta\) and \(1+a<2\),
\(8\eta-(1+a)(F-8)>0\), whence \(\lambda>a\).
Both cases satisfy
\[
\sum_j|r'_j-r_j|=|8-F|<6\eta,\quad V'\le V<13,\quad
V\le\frac{65}{64}V'.                                 \tag{15}
\]
The final bound uses \(a>255/256\) and \((256/255)^2<65/64\).
At zero variance retain its non-strict form.

Preserve every phase by \(q'_j=(r'_j/r_j)q_j\). If \(F>8\), each angular
deficit decreases. If \(F\le8\), \(1-\mu<3\eta/4\) and \(r_j>1/2\) give
\(r'_j/r_j<1+3\eta/2\). Thus, in both cases,
\[
\Delta'=\sum_j(r'_j-\Re q'_j)<10\eta,\qquad
\epsilon'^2=\left(\sum_j|q'_j-r'_j|\right)^2
\le2\left(\sum_jr'_j\right)\Delta'<160\eta.             \tag{16}
\]
The latter is weighted Cauchy--Schwarz using
\(|q'_j-r'_j|=\sqrt{2r'_j(r'_j-\Re q'_j)}\).
The strict endpoint margin is \(10-9(1+3e/2)>0\).
No new original-root or critical-disk condition is asserted for q'.

## 5. Whole origin comparison and the credited real defect

Write \(P(r)=\prod_jr_j\). Along the segment from q to q' the norm sum
is at most \(\max\{F,8\}<9\). AM--GM on the seven other factors gives
\[
|\partial_jO_a|\le K_9=9\int_0^1t(1+9t/7)^7dt<600,
\qquad |\partial_jP|\le(9/7)^7<6.                     \tag{17}
\]
The product bound applies to the radial segment. Integrating both
gradients and using (4),(15),
\[
\Re O_a(q')\le|O_a(q')|\le P(r')+(600+6)6\eta.         \tag{18}
\]
The **credited7244** comparison, valid for arbitrary complex tuples
with the radius floor (5) and total at most eight, is
\[
\Re O_a(q')\ge O_a(r')-K_1\epsilon'^2,\qquad
K_1=9\int_0^1t(1+8t/7)^7dt
   =\frac{570801247}{1647086}<350.                    \tag{19}
\]
Its ordinary proof is exact integral Taylor expansion on the segment
\(r'+s(q'-r')\). First derivatives at r' are real, and
\[
|q'_j-r'_j|^2=2r'_j(r'_j-\Re q'_j),\qquad
|\Re(q'_j-r'_j)|\le|q'_j-r'_j|^2.
\]
Mixed second derivatives are bounded by
\(K_2=9\int_0^1t^2(1+4t/3)^6dt=1199851/5103<2K_1\);
pure second partials vanish. The two ordered mixed terms cancel the
integral factor \(1/2\), proving (19). Norm convexity keeps each segment
coordinate within its radial bound. No origin tail is omitted.

Combining (16),(18),(19),
\[
O_a(r')-P(r')<(350\cdot160+600\cdot6+6\cdot6)\eta
             =59636\eta<60000\eta.                   \tag{20}
\]
Set \(y_j=(1+a)r'_j-1\ge0\), and \(D=2a e_2(y)-e_3(y)\).
The **credited8656** full-domain radial gap is
\[
(1+a)^8[O_a(r')-P(r')]\ge8(1-a^9)+5D.                \tag{21}
\]
Its complete symmetric multiaffine minimizer reduction and636
nonnegative tensor Bernstein coefficients at penalty five, both full
algebra routes and inverses, remain the explicit ordinary/certificate
dependency. Its mean-tube argument is not used. With \((1+a)^8<256\),
(20)--(21) imply
\[
0\le D<3072000\eta.                                  \tag{22}
\]

## 6. Newton coercivity and the global energy carrier

Exactly,
\[
e_1(y)=8a,\qquad E_2:=e_2(y)=28a^2-\frac{(1+a)^2}{2}V'.
\]
Since \(V'<13\),
\[
E_2>28(1-e)^2-26>\frac74,\qquad E_2\le28a^2.          \tag{23}
\]
Maclaurin and \(1-\sqrt{s}\ge(1-s)/2\) on [0,1] give
\[
\begin{split}
D&\ge2E_2\left(a-\sqrt{E_2/28}\right)
 \ge\frac{E_2(28a^2-E_2)}{28a}\\
 &=\frac{E_2(1+a)^2}{56a}V'
 \ge\frac{E_2}{14}V'\ge\frac18V'.                    \tag{24}
\end{split}
\]
Here \((1+a)^2/a\ge4\); the last inequality is strict if \(V'>0\).
At zero variance its non-strict form is sufficient. Therefore
\[
V'<24576000\eta,\qquad V<24960000\eta.                \tag{25}
\]
The complete reciprocal norm identity gives
\[
\sum_j|q_j-1|^2=V+8(\mu-1)^2+2\Delta
<(24960018+(9/2)e)\eta.                              \tag{26}
\]
Finally \(\zeta_j=-\eta+(q_j-1)/q_j\), with \(r_j>1/2\), gives
\[
H\le16\eta^2+8\sum_j|q_j-1|^2
<(199680144+52e)\eta<2^{28}\eta.                      \tag{27}
\]
This proves the energy part of (1). It also proves an abstract
two-channel result: any nonzero complex q with the radius floor (5),
\(F\le8+3\eta\), \(|C_a(q)|\ge1\) and \(|O_a(q)|\le P(r)\) obeys
\(\sum|a-1/q_j|^2<2^{28}\eta\).
No individual critical disk constraint beyond that floor or actual
original-root labeling is needed for this carrier. Equations (4)--(5)
instantiate it for actual polynomials.

## 7. Fixed-energy entry, scope and exact evidence

For \(0<\eta\le2^{-37}\) and \(F\le8+3\eta\), (27) gives
\(H<2^{28}\eta\le2^{-9}=1/512\).
Only now apply9620 to obtain the first inequality in (3).
The endpoint equality \(2^{28}2^{-37}=1/512\) is legitimate because
H is strictly below its bound. If \(F>8+3\eta\), (3) follows from
\(3>8/3-4\eta/3\). Infinite F is included. The final slope comparison
is \(8/3-13/5-4e/3>0\). Every case is covered without root branches,
attainment or coefficient caps.

The freshly committed9667 audit proves, on the original fixed-energy
domain, the stronger unconditional bound
\(F>8+(8/3+9/57820)\eta-4\eta^2/3\). Its additional all-nine-root
projection argument gives the low-sublevel centered critical variance
\(V_{\rm crit}>135\eta/413\), where
\(V_{\rm crit}=\sum|\zeta_j-m_{\rm crit}|^2\) and
\(m_{\rm crit}=\sum\zeta_j/8\). This differs from our radial reciprocal
variance V. The complete9667 proof, including that separately credited
postnative refinement, has been read. After exactly the same entry above,
we therefore have the further GLOBAL corollary
\[
F>8+(8/3+9/57820)\eta-4\eta^2/3
\quad(0<\eta\le2^{-37}).                              \tag{28}
\]
The larger-F case follows because \(9/57820<1/3\). On the global low
sublevel in this annulus, the CREDITED9620 consequences include
\(H<7\eta\), \(V_{\rm crit}<6\eta\), and all eight coefficient caps.
The CREDITED9667 variance floor and actual-original displacement
\(|Z_\omega-a\omega|<71\eta/15\), \(\omega^9=1\), also apply.
These are domain transports of published results, not new local estimates.

[7184](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_effective_boundary_first_power/PROOF.md)
already proves \(H<1.6\cdot10^9\eta\) under
\(F\le8+\eta/20,\eta\le10^{-6}\), and a linear1/20 annulus at
\(\eta\le10^{-18}\); its independent7218 audit widens the latter to
\(121\cdot10^{-18}\). The present energy carrier contains that sublevel
and interval with a smaller sufficient constant; (3) has a wider
specified annulus and stronger sufficient slope.
The earlier8656 strict annulus extends to \(10^{-10}\), which is
wider than our linear annulus; we do not generalize that whole artifact.

Boundary classification, both equality families, qualitative polar
concentration, the existential sharp slope and optimizer/profile work
are prior results, credited in [LITERATURE.md](LITERATURE.md).
They are not premises of this effective route. The unrestricted
first-power endpoint, the sharp effective annulus, optimal constants
and extension to the middle range remain open here. The sufficient
constant in (27) gives no fixed-energy entry at \(\eta=e\).

Run [verify.py](verify.py) as in [README.md](README.md), stdlib
CPython3.10+. It reconstructs every entry of [EXPECTED.json](EXPECTED.json):
the full three polynomials, exact absolute tails,16 strict window
margins,10 whole Gaussian-rational controls and three actual multiplicity
controls. The collapsed actual families lie outside the low objective
cut; they check identities, not existence of a low competitor.
Six broken mathematical budgets and eight altered record controls
reject under normal and optimized Python.
[validate.py](validate.py) checks external malformed/type/source damage;
[VALIDATION.json](VALIDATION.json) records the complete compact evidence.
Finite controls do not establish universal case coverage.

Maclaurin, norm/gradient inequalities, Gauss--Lucas, primary identities,
integral Taylor, floor-preserving normalization and all case divisions
are written ordinary bridges outside a formal kernel.
The8656 certificate and reduction,7244 phase estimate and9620
fixed-energy proof remain explicit scoped dependencies. Author replay,
source publication and graph commitment do not supply independent
review. No floating sign, solver, approximate root computation,
incomplete enumeration or omitted large corpus supplies a premise.
