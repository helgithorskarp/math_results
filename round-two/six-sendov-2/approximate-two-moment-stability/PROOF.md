# Approximate stationarity and two original odd moments

Actual **six-sendov-2**, role **researcher**, 2026-10-03. Complete ordinary
author proof relative to the explicitly credited lemmas below;
**UNFORMALIZED and independently UNREVIEWED**. The exact source checks
corroborate finite identities and sufficient constants. They do not
formalize the analytic implications or confer an independent verdict.

## 1. Every actual profile: statement and inputs

Let eight DISTINCT REAL originals satisfy
\[
 a_1<\cdots<a_8,\qquad \sum_i a_i=0,\qquad \sum_i a_i^2=1,
 \qquad a_{i+1}-a_i\ge\delta,\quad 0<\delta\le1.
\]
Use the actual angular functional of
[7432](https://github.com/helgithorskarp/math_results/blob/main/sendov_collapsed_angular_quartic/PROOF.md)
and the coefficient framework of
[9496](../mass-stationary-chart/PROOF.md):
\[
 f=\prod_i(z-a_i),\quad h=f'/8,\quad
 m_j=-8f(\lambda_j)/h'(\lambda_j)>0,\quad\sum_jm_j=1,
\]
where \(\lambda_1,\ldots,\lambda_7\) are the seven ACTUAL simple real
criticals. Put
\[
 \eta=\sum_jm_j^2,\qquad D=\sum_i a_i^4-1/8>0,
 \qquad C=(1-\eta)/D.
\]
The actual mass interpolant \(p\), characterized by
\(p(\lambda_j)=m_j\), has degree at most SIX. In the local feasible
coefficient chart with the coefficients of \(z^8,z^7,z^6\) fixed to
\(1,0,-1/2\), define ALL SIX derivatives
\[
 g_k=DC[z^k]\quad(0\le k\le5),\qquad
 \epsilon=\max_{0\le k\le5}|g_k|,
 \qquad \mu_k=\sum_i a_i^k.                             \tag{1}
\]
Distinct originals make this chart locally feasible; this definition does
not assume stationarity. Define
\[
 b_\delta=10^{-3940}\delta^{10412},\qquad
 L_\delta=2\,10^{3940}\delta^{-10418},\qquad
 q_\delta=10^{-136}L_\delta^{-190}.                     \tag{2}
\]

**Theorem. EVERY profile above satisfies**
\[
 \boxed{\epsilon+\mu_3^2+\mu_5^2\ge q_\delta
          >10^{-748794}\delta^{1979420}.}              \tag{3}
\]
Moreover, whenever \(\epsilon\le b_\delta/2\),
\[
 \boxed{L_\delta^{50}\epsilon+
      \frac{13}{48}|\mu_3|+\frac3{40}|\mu_5|
       \ge10^{-68}L_\delta^{-95}.}                     \tag{4}
\]
There is NO STATIONARITY assumption. These are deliberately coarse
sufficient constants. This is an original-real-root angular result,
not a physical-H estimate or a complex first-power theorem.

The substantive new bridge is the quantified comparison of a RAW quintic
tuple with the reconstructed9550 chart. This comparison retains every one
of9952's FIVE residuals. It does not apply9952's exactly stationary
original-root corollary to a nonstationary tuple.

The direct quantitative inputs are:

* [10064 approximate mass floor](../approximate-stationary-mass-coercivity/PROOF.md),
  source5d4952bfedbd3de4de590e35fc7fcb25ce0775c6: EVERY actual profile
  satisfies \(\epsilon+|p_5|\ge b_\delta\). The ACTUAL degree-six
  coefficient is retained first, with
  \(p_6=Dg_0/16\) and
  \(\|K-4Cz^2+4\|_{\rm coef}\le1835008\epsilon\).
  On cropping only p6, ALL coefficient residuals are bounded by
  \(M^{10}\epsilon\), where \(M=100\delta^{-6}\).
  This ordinary input includes its own heat/asymmetry/geometry premises;
  it remains independently unreviewed at the present refresh.
* [9550 complete triangular chart](../degree-five-triangular/PROOF.md),
  sourcecb4cf7d9d83f3d376d3763b65cbe2fddd50637f4: the exact reconstructed
  h,p and ALL FIVE remaining equations. Its fixed pivots and formulas
  are credited prior art; their whole polynomials are regenerated here.
* [9952 Theorem A](../joint-moment-coercivity/PROOF.md),
  source2565659ede2258987d64f379de80b9a7b5913e7e: for EVERY finite
  COMPLEX parameter tuple with
  \(|B|,|E|,|r|,|s|,|t|,|t^{-1}|\le L\), \(L\ge1\),
  \[
    |B|+|F_*|+\|\mathcal R_*\|_\infty
                \ge10^{-68}L^{-95}.                  \tag{5}
  \]
  This theorem ALREADY allows a nonzero full residual. Its ordinary proof
  and its named inputs were independently confirmed in9994, actual
  six-reviewer-5. That verdict is not a review of this new leaf.

For exact stationarity, the already published10040 and the independent
[10072 refinement](../../six-reviewer-5/stationary-mass-floor-audit/PROOF.md)
have sharper same-domain rates. In particular10072 proves
\(|p_5|\ge10^{-2176}\delta^{6528}\) and
\(\mu_3^2+\mu_5^2\ge(57600/4549)10^{-413576}\delta^{1241460}\),
relative to its explicit input boundary. Those exact-stationary results
are credited and are not transported to the present approximate domain.
This theorem does not improve their stationary rates.

## 2. Universal raw-quintic error norm

For the algebraic bridge, allow complex coefficients and put
\[
 h=z^7-\tfrac38z^5+Bz^4+Ez^3+Fz^2+Gz+J,
 \quad p=p_0+p_1z+p_2z^2+rtz^3+stz^4+tz^5,\quad t\ne0. \tag{6}
\]
F denotes the actual coefficient of h in this section, not a function.
The coefficient vector is
\[
 x=(B,E,F,G,J,p_0,p_1,p_2,rt,st,t).                    \tag{7}
\]
Define Q,O,K by the credited normal-representative algebra9496/9550.
With remainder \(\operatorname{rem}_h\) and
\(\tau_j=\sum_{\ell=1}^7\lambda_\ell^j\) interpreted algebraically
through Newton identities,
\[
 T(1)=0,\qquad T(z^k)=\sum_{j=0}^{k-1}\tau_jz^{k-1-j}-kz^{k-1}.
\]
T acts on the UNIQUE normal representative; products are reduced before
T is applied. Q is the ordinary quotient of \(8f+ph'\) by monic h,
where \(f'=8h\); its value is independent of f's arbitrary constant.
Then
\[
 O=ph''+(p'-Q)h'+(64-Q')h,
 \quad K=-16p-\tfrac14T^2\operatorname{rem}_h(p^2)
                +\tfrac14T\operatorname{rem}_h(p(Q-p')).            \tag{8}
\]
In this section measure the eleven rows
\[
 \Phi(x)=(O_0,\ldots,O_5,K_0+4,K_1,K_3,K_4,K_5),
 \qquad \rho=\|\Phi(x)\|_\infty.                      \tag{9}
\]
The K2 row determines the reconstructed value of C and is not needed
for9952A. It is not among the FIVE remaining equations being compared.
All higher O rows and K6 vanish identically in the quintic map. No
equation among \(tO_2,tO_1,tO_0,K_1,K_0+4\) is dropped.

Assume
\[
 L\ge100,\quad \|x\|_\infty\le L,\quad
 |B|,|E|,|r|,|s|,|t|,|t^{-1}|\le L.                   \tag{10}
\]
The coordinates rt and st in x and the separate ratios r,s both have
the displayed bounds. This explicit condition is automatic for the
actual application below.

Every row of Phi is an ordinary polynomial of total degree at most4 in
the ELEVEN coefficient variables (7). The exact maximum over rows of
the sum of coefficient one-norms of ALL eleven partial derivatives is
\[
 N_\Phi=1611571/4096.                                 \tag{11}
\]
This known degree-four bound is credited10040/10072 and regenerated
here on the entire eleven-row map. Therefore complex straight segments
inside the coefficient box \(\|x\|_\infty\le2L\) obey
\[
 \|\Phi(x)-\Phi(y)\|_\infty
 \le8N_\Phi L^3\|x-y\|_\infty
 \le L^5\|x-y\|_\infty.                              \tag{12}
\]
Indeed all partial derivatives have degree at most3, and
\(8N_\Phi<100^2\le L^2\). Integration along the complex segment
proves (12); no real-root, mass-positivity or actual-profile premise is
assigned to any projected tuple.

## 3. Quantified triangular reconstruction

Keep B,E,r,s,t fixed throughout. The following known exact identities
determine the chart, and the new estimates control their errors.
First set
\[
 p_{2,*}=8+t(5B/7-27s/56-rs).
\]
The entire raw high kernel row is
\[
 K_5=(7/4)t(p_2-p_{2,*}).                             \tag{13}
\]
After p2 is replaced, define
\[
\begin{split}
 X_0(F)&=-5/7+t(3Br/7+75B/392+4Es/7+5F/7+3rs/28+9s/784),\\
 X_1(F,G)&=128B/5+t(-8B^2/7-4Brs+4Bs/7+16Er/3+3E
                         +20Fs/3+8G-3r/8-9/64).
\end{split}                                                        \tag{14}
\]
The full equations are
\[
 O_5=42(p_0-X_0(F)),\qquad O_4=(15/4)(p_1-X_1(F,G)).   \tag{15}
\]
X0 is independent of p1,G,J; X1 is independent of p0,J. Once these two
mass coefficients are replaced simultaneously, O5,O4,K5 are identically
zero. In this COMPOSED map the next high equations are
\[
 K_4=24t^2(G-G_0(F)),\qquad
 K_3|_{G=G_0(F)}=-(15/14)t^2(F-F_*),                  \tag{16}
\]
where the entire affine polynomial G0 satisfies
\[
 G_0'(F)=-5s/6.                                      \tag{17}
\]
Here G0 is obtained by setting G=0 in K4 and multiplying by
\(-1/(24t^2)\); Fstar is obtained by setting F=0 in the next K3 row
and multiplying by \(14/(15t^2)\). These are exactly9550's formulas.
At Fstar,Gstar=G0(Fstar), the entire next equation is
\[
 O_3=-28t(J-J_*).                                    \tag{18}
\]
All divisions are by fixed nonzero constants and the stipulated t or t2.
They are valid for complex t, including negative real t.

For clarity, each change of F or G also recomputes X0,X1. Holding an old
p1 while moving G would invalidate (16). The exact mass changes are
\[
 \Delta_G X_1=8t\,\Delta G,\quad\Delta_G X_0=0,
 \quad \Delta_F X_0=(5/7)t\,\Delta F.
\]
If F and G0(F) move together, their p1 change is EXACTLY zero:
\[
 \Delta X_1=((20/3)ts+8t(-5s/6))\Delta F=0.           \tag{19}
\]
This cancellation is the useful part of the coupled correction.

Suppose first that \(\rho\le L^{-40}\). Use (12) after each correction.
The following powers are conservative simultaneous infinity-norm bounds:

| Stage | Complete coefficient displacement bound | New eleven-row residual bound |
| --- | ---: | ---: |
| Replace only p2 using (13) | \(L\rho\) | \(L^7\rho\) |
| Replace p0,p1 by X0,X1 using (15) | \(L^7\rho\) | \(L^{13}\rho\) |
| Replace G by G0(F), recompute p1 | \(L^{16}\rho\) | \(L^{22}\rho\) |
| Replace F by Fstar and G by G0(Fstar), recompute mass coefficients | \(L^{25}\rho\) | \(L^{31}\rho\) |
| Replace J by Jstar | \(L^{32}\rho\) | \(L^{38}\rho\) |

Here is the full accounting. The first displacement is at most
\((4/7)L\rho\). The next mass displacement is at most
\((4/15)L^7\rho\). The G-only displacement of h is at most
\(L^{15}\rho/24\), and its p1 change at most \(L^{16}\rho/3\).
The F displacement is at most \((14/15)L^{24}\rho\); its G change is
at most \((5/6)L^{25}\rho\), its p0 change at most
\((5/7)L^{25}\rho\), and its p1 change is zero by (19). Finally the J
change is at most \(L^{32}\rho/28\) and leaves all mass coefficients
unchanged. The residual estimates follow, in order, from
\[
\begin{split}
 1+L^6&\le L^7,& L^7+L^{12}&\le L^{13},\\
 L^{13}+L^{21}&\le L^{22},& L^{22}+L^{30}&\le L^{31},\\
 L^{31}+L^{37}&\le L^{38}.&&
\end{split}                                                        \tag{20}
\]
Every inequality is on the CLOSED domain L>=100.

There is no circular box assumption in this use of (12). Inductively,
each next correction is first bounded from the CURRENT residual and
its exact pivot; this calculation uses no next segment. Every prefix
sum of the displayed displacements is bounded by
\[
 (L+L^7+L^{16}+L^{25}+L^{32})\rho
    \le L^{33}\rho\le L^{-7}<1.                      \tag{21}
\]
Thus the next endpoint and its entire segment remain inside the
coefficient box L+1<2L, so (12) applies and closes the induction.
This works over complex coefficients as well.

The final coefficients are EXACTLY9550's reconstructed hstar,pstar;
all six high rows vanish and the remaining full residual is
\[
 \mathcal R_*=(tO_2,tO_1,tO_0,K_1,K_0+4).
\]
The complete raw-to-chart comparison is consequently
\[
 |F-F_*|\le L^{24}\rho,\qquad
 \|\mathcal R_*\|_\infty\le L^{39}\rho,\qquad
 |F-F_*|+\|\mathcal R_*\|_\infty\le L^{40}\rho.        \tag{22}
\]
The factor L for the three tO rows is retained. All FIVE entire
polynomials are checked against the credited chart; a selected matrix
pivot, projective surrogate or four-equation subsystem is insufficient.

Apply9952A (5) at the unchanged parameters B,E,r,s,t to (22). This gives
\[
 \boxed{|B|+|F|+L^{40}\rho\ge10^{-68}L^{-95}.}         \tag{23}
\]
If instead \(\rho>L^{-40}\), then \(L^{40}\rho>1\), which directly
implies (23). Thus (23) holds throughout (10), with no small-residual,
root-feasibility or stationarity assumption. The stronger displacement
estimates (22) have the stated small-rho premise.

## 4. Returning to the actual degree-six profile

Set \(b=b_\delta\), \(\tau=b/2\),
\(L=L_\delta=(\tau\delta^6)^{-1}\). Suppose
\(\epsilon\le b/2\). The DIRECT10064 input gives
\[
 |t|=|p_5|\ge\tau>0.                                  \tag{24}
\]
Do not remove p6 by an exactly stationary assumption. Its actual identity
\(p_6=Dg_0/16\) is used before cropping;10064's full degree-six map and
its entire monic residue-pair inverse give for the CROPPED quintic
\[
 \rho\le M^{10}\epsilon,\qquad M=100\delta^{-6}.       \tag{25}
\]
For specificity, the initial entire kernel error is at most
1835008epsilon and the crop contributes at most
\(M^{10}\epsilon/16\); their sum is at most M10epsilon since M>=100.
The initial actual O rows vanish and the same crop bound controls them.
All eleven rows (9) are subsets of that controlled full map, so (25)
retains their full error. The cropped interpolant is not asserted to
equal the actual masses or to be positive at criticals.

The actual mesh/interpolation estimates of10064 give
\[
 |p_k|\le5/(9\delta^6)<\delta^{-6}\quad(0\le k\le6),
 \quad |B|,|E|,|F|,|G|,|J|\le35.
\]
All originals/criticals lie in[-1,1]. In particular the raw coefficient
vector of the cropped map has norm at most M. Its ratios
\(r=p_3/t\), \(s=p_4/t\) satisfy
\[
 |r|,|s|\le\tau^{-1}\delta^{-6}=L,
 \quad |t^{-1}|\le\tau^{-1}\le L.
\]
Also M<=L and L>=100, so every assumption (10) holds. Negative t needs
no orientation or reflection: the universal argument already includes it.
Combining (23) and (25) gives
\[
 |B|+|F|+L^{50}\epsilon\ge10^{-68}L^{-95}.             \tag{26}
\]
Here \(L^{40}M^{10}\le L^{50}\). Only this step imports actual geometry
and the full-p6 input; none is imported into intermediate projections.

Balanced norm-one Newton identities for the ACTUAL f yield
\[
 B=-5\mu_3/24,\qquad F=\mu_3/16-3\mu_5/40.
\]
Hence
\[
 |B|+|F|\le(13/48)|\mu_3|+(3/40)|\mu_5|,
 \quad (13/48)^2+(3/40)^2=4549/57600=:\kappa^2.        \tag{27}
\]
Equations (26)--(27) prove (4) without treating Fstar as the actual F.

## 5. The joint gradient and TWO-moment-square floor

Write \(a=10^{-68}L^{-95}\) and \(q=a^2=q_\delta\).
If \(\epsilon\ge\tau\), then \(\epsilon\ge q\), since
\(q=10^{-136}\tau^{190}\delta^{1140}\le\tau\).
For \(\epsilon<\tau\), equation (4) applies. If
\(\epsilon\ge a/(2L^{50})\), it again suffices: indeed
\[
 \frac{q}{a/(2L^{50})}=2\,10^{-68}L^{-45}\le1.
\]
Otherwise (4) and Cauchy--Schwarz give
\[
 \kappa\sqrt{\mu_3^2+\mu_5^2}\ge a/2,
 \quad\mu_3^2+\mu_5^2\ge a^2/(4\kappa^2)>a^2=q,
\]
because \(4\cdot4549/57600<1\). These cases exhaust every epsilon,
including both splitting equalities, and prove the first inequality (3).
Finally
\[
 q=2^{-190}10^{-748736}\delta^{1979420}
       >10^{-748794}\delta^{1979420},
\]
since \(2^{190}<10^{58}\). No finite sampling of delta or L establishes
any of these comparisons.

## 6. Exact evidence and remaining scope

[verify.py](verify.py) is a self-contained stdlib Fraction checker. It
reconstructs all raw coefficient, parameter-composed, p2-corrected,
fully composed and final maps, including the normal-representative
adjoint and EVERY high zero row. It checks89 whole identities; all121
coefficient gradient polynomials; the exact gradient norm; all seven
solved9550 polynomials, FIVE residuals and five matrix rows; and18
closed monomial budgets. Every budget is proved by dividing by its
upper power of L and checking all nonnegative terms are nonincreasing
for L>=100. The endpoint100 is an exact sufficient comparison, not an
experimental inference. The ordinary segment/bootstrap reasoning is
the written proof above.

The [compact whole record](expected.json) is regenerated before comparison,
and nine intentional mathematical damages must reject without using it.
Normal and optimized Python execution must match the ENTIRE typed record;
externally damaging the LAST high-kernel coefficient of its full Phi
also rejects. [compare_cas.py](compare_cas.py) optionally compares the
entire maps and gradients with alternate SymPy polynomial division and
logarithmic-series traces. This is same-author corroboration, not an
independent review. Reproduction and actual evidence are in
[README.md](README.md); exact input and primary-literature credit is in
[LITERATURE.md](LITERATURE.md).

This theorem supplies a separation-only approximate TWO-original-odd-moment
floor and a reusable raw-quintic stability bridge. Stationary existence,
original-collision continuation, global angular optimizer classification,
physical-H bounds and the global complex first-power endpoint remain
outside its conclusion. There is no numerical search, solver timeout,
incomplete enumeration or resource failure in the proof. The constants
are too small for practical numerical certification and carry no
optimality or historical-priority claim.
