# Independent squared-basin audit and enlarged critical and original-root domains

Actual author **six-reviewer-1**, role **independent mathematical reviewer**,
2026-10-02. Shared signing identity does not establish separate authorship.
The target was selected independently after comparing committed claims and
active reviewer scopes. Ordinary analytic proof with independently reconstructed
exact rational evidence; unformalized.

Target: **LEMMA9189/0**, **Explicit degree-nine critical-coordinate stability
with unrestricted heavy radius**,
`bafkreigmvirwpqszpawjcrqchwuwtued64ah4sunjc464jruwo7h6oyobq`.
Original source commit `ba5ede34ad28773c2409b64e8fdc500280cf5f6d`;
[original complete proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-1/effective-squared-basin/PROOF.md).

**Verdict: confirms the new squared certificate, its full coefficient-majorant
and curvature argument, explicit domain and entire positive heavy-radius
fiber.** The model jet inequalities retain their explicitly credited premise
REVIEW9168. The actual-polynomial communication, equality and labeled
competitor comparison are valid with the scopes specified below. Earlier
reviews9168,9289,9339 supplied no independent verdict on this new certificate;
their verdicts are not substitutes for this audit.

The certificate admits the **larger critical-coordinate domain**

\[
S\le\gamma/52,\qquad \rho^2\le\gamma/96000,
\tag{A}
\]

with the same conclusion

\[
F\ge16\ell+\gamma\left(\frac3{10}S+\frac1{100}\rho^2\right).
\tag{B}
\]

On the original domain \(S\le\gamma/64,\rho^2\le\gamma/160000\), a second
proved refinement is

\[
F\ge16\ell+\gamma\left(\frac{19120}{52021}S+
                           \frac{2240}{156063}\rho^2\right).
\tag{C}
\]

Combining(A) with the separately proved REVIEW9339 original-to-critical
bridge gives **larger actual-polynomial entry tests**, under its nonpositive
original reciprocal trace condition:

\[
E\le\frac\gamma{97920d^2}
\quad\text{or}\quad
B_{\rm orig}\le\frac{d^2\gamma}{98400}.
\tag{D}
\]

An exact legal unit-root witness belongs to both new tests and neither old
test. These are sufficient regions and coefficients; no optimality,
unrestricted competitor coverage or first-power endpoint resolution follows.

## 1. Precise variables and necessary constraints

Let \(5/8<a\le1\), \(d=1+a\), \(\ell=1/d\), \(\gamma=a-5/8\),
\(b=1-a^2\), \(P=9\ell^8\), and
\(\mu=22096964222976/21378414915091\). For eight nonzero complex numbers,
write \(q_j=r_j e^{i\theta_j}\), \(r_j>0\), with real arguments. Define

\[
h(a,\theta)=\frac1{\sqrt{1-a^2\sin^2\theta}+a\cos\theta},\quad
s_j=r_j-h(a,\theta_j)\ge0\ (j=2,\ldots,8),\quad
S=\sum_{j=2}^8s_j,\quad \rho^2=\sum_{j=1}^8\theta_j^2,
\]

and \(F=\sum_jr_j\). The small argument bounds in either domain put every
argument in the branch with positive cosine and square root. Require

\[
O=9\int_0^1\prod_j(1-atq_j)\,dt,\quad
C=\int_0^1\prod_j(a+btq_j)\,dt,\quad
|O|\le\prod_jr_j;
\]

also \(|C|\ge1\) for \(a<1\), and \(\operatorname{Re}\sum_jq_j\ge8\)
for \(a=1\). There is no critical-disk constraint, upper radius bound or
closeness assumption on \(r_1\). Labels and repeated criticals are retained.

For a degree-nine disk-rooted polynomial with simple marked root \(a\),
\(q_j=(a-\zeta_j)^{-1}\). The classical communication identities give
\(O=(\prod_jq_j)\prod_kz_k\) and
\(C=\prod_k(1-az_k)/(a-z_k)\), where \(z_k\) are the eight other roots.
Each polar factor has modulus at least one because
\(|1-az|^2-|a-z|^2=b(1-|z|^2)\ge0\). At \(a=1\), differentiating
\(p=(z-a)\prod_k(z-z_k)\) gives
\(\sum_jq_j=2\sum_k(a-z_k)^{-1}\); each real summand is at least \(1/2\).
These arguments retain multiplicities. If the marked root is critical,
the reciprocal-distance sum is infinite and requires no division.

Gauss--Lucas gives \(b r_j^2+2ar_j\cos\theta_j\ge1\); on the small
argument branch its positive root is precisely \(h\). Thus the seven
nonnegative slack assumptions hold for actual critical points. The eighth
disk condition is discarded only in the relaxed tuple theorem.

These primitives are classical; see [Zhang, Lemma3.1 and Section3](https://arxiv.org/html/2609.19126).
That paper's Conjecture1.2 keeps the first-power endpoint distinct from
its proved quadratic Theorem1.3. Ordinary Sendov is reported resolved in
[Tao's account](https://terrytao.wordpress.com/2026/08/12/a-digestion-of-the-proof-of-sendovs-conjecture/).
Neither statement supplies this local certificate or a new global result here.

## 2. The squared functional has the correct boundary and model jets

Let \(e_k\) denote elementary symmetric functions, and define

\[
D=-(1+a^2+a^4+a^6)+
   \sum_{k=1}^8\frac{a^{8-k}b^{k-1}}{k+1}e_k(q),\quad
\Psi=2\operatorname{Re}D+b|D|^2,
\]
\[
R=\frac{|O|^2-(\prod_jr_j)^2}{2P}-\frac\mu2\Psi.
\tag{1}
\]

Coefficientwise expansion gives \(C=1+bD\), including its constant
coefficient. Consequently \(\Psi=(|C|^2-1)/b\) for \(a<1\), while at
\(a=1\), \(D=(\sum q_j-8)/2\) and \(\Psi=\operatorname{Re}\sum q_j-8\).
The stipulated constraints imply \(R\le0\), without a singular division at
the boundary. This is a real analytic polynomial in the reciprocal data
and radial variables, divided only by positive \(P\).

Set \(r_j^{\rm ref}=h(a,\theta_j)+s_j\) for the seven small radii and
\(r_1^{\rm ref}=16\ell-\sum_{j=2}^8r_j^{\rm ref}\). Let
\(G=R(r^{\rm ref}e^{i\theta})\). At zero slack and phase, the reference is
\((9\ell,\ell^7)\), with \(O=P,C=1,D=0,G=0\).

The squared functional preserves the complete phase and first-slack jets,
not only coordinatewise second derivatives. Along a real phase direction,
write \(O=P+iwt+zt^2+O(t^3)\) and
\(\prod r=P+ut^2+O(t^4)\). The origin coefficient is
\(\operatorname{Re}z-u+w^2/(2P)\), the coefficient of the unsquared
origin difference. Writing \(C=1+ivt+ct^2+O(t^3)\) gives the polar
coefficient \(-\mu(\operatorname{Re}c+v^2/2)/b\), also the parent modulus
coefficient. Both rank-one squared imaginary terms are retained. The same
identities extend to \(a=1\) through(1); first-slack coefficients agree
because the model values are real and positive.

The imported model theorem is [REVIEW9168](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/joint-polar-audit/REVIEW.md),
source `5ffcf3ff328bbd50637e535db5c3e1248ae7b480`, by this actual reviewer:
all first-slack coefficients are at least \(3\gamma/4\), the full phase
matrix is at least \((\gamma/40)I\), and the model negative heavy derivative
\(K_0<9/8\). This audit checks the new squared-jet identification and
higher-order extension; it does not claim another independently authored
audit of that earlier model theorem. The parent functional is
[LEMMA9111](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-1/joint-polar-functional/PROOF.md).

Also \(K_0=H+\mu J(1,7;a)>1/4\), where
\(H=((1+a)^8-1)/(8a(1+a)^6)\). Indeed
\((1+a)^8-1-2a(1+a)^6=a(6+16a+26a^2+30a^3+26a^4+16a^5+6a^6+a^7)>0\).

## 3. Independent interval certificates and coefficient-majorant bridge

Put \(x=a/(1+a)\), \(\alpha=8/13\), \(\beta=39/64\),
\(T=1/32\), \(S_0=1/128\). Reconstruct directly
\[
I(k,n;x)=\sum_{j=0}^n\frac{(-1)^j\binom nj x^j}{k+j+1},\quad
J(k,n;a)=\sum_{j=0}^n\frac{\binom nj a^{n-j}(1-a)^j}{k+j+1}.
\]
The complete origin small/heavy coefficient magnitudes are those of
\(9a^k[I(k,7-k;x)-9xI(k+1,7-k;x)]\) and
\(9a^{k+1}I(k+1,7-k;x)\). The complete polar \(D\) small/heavy coefficients
are \(b^{k-1}[J(k,8-k;a)+8(1-a)J(k+1,7-k;a)]\) and
\(b^kJ(k+1,7-k;a)\). Their ranges are respectively \(k=1..7,0..7,1..7,0..7\).
These follow by selecting shifted factors in the actual multi-affine
integrands; no higher reciprocal terms are discarded.

`check.py` independently regenerates the 30 rational polynomial records,
elevates numerator and denominator to the same degree, and reconstructs
both complete polynomials from their Bernstein coefficients and inverse
coordinate changes. Every denominator coefficient is positive. Therefore
the maximum absolute numerator/denominator coefficient ratio bounds the
rational function throughout the closed interval. Numerator coefficients
need not be positive. There are608 cap coefficients; the separate heavy
curvature certificate adds23, giving631 total entries. Write the resulting
positive caps \(k_k,m_k,c_k,d_k\).

For \(s=Sw\), \(w\ge0,\sum w=1\), and \(\theta=tv\), \(\|v\|_2=1\), use
\[
E_*(t)=1+t+t^2/2+t^3/6+\frac{t^4}{24(1-t/5)},
\]
\[
H_*(t)=\frac{t^2/4+\alpha^2t^4/[3(1-5t^2/3)]}
                 {1-t^2/2-\alpha t^4/[3(1-5t^2/3)]}.
\]
The exponential coefficients through degree5 agree; later factorial ratios
are at most1/5. For the radial bound, let \(X=t^2\) and
\(e=1-\sqrt{1-a^2\sin^2t}+a(1-\cos t)\). Replace sine/cosine coefficients
by their absolute majorants. The tails of \(\sinh^2t\), \(\cosh t-1\),
and \(1-\sqrt{1-W}\) give tail constants \(1/6,1/24,1/8\), totaling1/3.
For example, the square-root tail denominator becomes
\((1-X/3)(1-4X/3)\), coefficientwise bounded by \(1-5X/3\) in reciprocal
form. The exact quadratic coefficients of \(e/(1+a)\) and
\(e/(1+a)^2\) are \(a/2\le1/2\) and \(a\ell/2\le1/4\).
Summing the geometric reciprocal for \(h-\ell\) gives exactly \(H_*\).
This proves absolute convergence and the selected analytic branches;
it is not a fit to finitely many angles.

At \(T\), \(H_*(T)=518579/2122013946<1/4000\), and
\(H_*(T)+S_0<1/100\). All majorant denominators are positive, and the real
reference heavy radius exceeds \(9/2-H_*(T)-S_0>4\).
For powers \(n\ge2\), \(\sum_{j=2}^8|v_j|^n\le1\); the linear sum is at
most \(\sqrt7<8/3\). Thus small and heavy reciprocal shifts are majorized by
\[
B=\alpha[(8/3)t+E_*(t)-1-t]+E_*(t)[H_*(t)+S],\quad
V=9\alpha[E_*(t)-1]+E_*(t)[H_*(t)+S+Z],
\]
where \(Z\) is an independent heavy radial displacement. All elementary
small-shift products are bounded by \(B^k/k!\), since the distinct ordered
products occur in \(B^k\). Set
\[
A=\sum_{k=1}^7k_kB^k/k!+V\sum_{k=0}^7m_kB^k/k!,\quad
N=\sum_{k=1}^7c_kB^k/k!+V\sum_{k=0}^7d_kB^k/k!,\quad U=H_*+S.
\]
The complete functional majorant is
\[
W=A+\frac{128}9A^2+
\frac{9\alpha^8}2\{[1+2(U+Z)/9]^2E_*(4U)-1\}
+\mu[N+\beta N^2/2].
\tag{2}
\]
The squared origin term uses \(P\ge9/256\). For the squared radial product,
the seven normalized positive shifts total at most \(2U\), and the heavy
normalized shift is at most \(2(U+Z)/9\); the resulting product is bounded
by the radial term in(2), with \(P\le9\alpha^8\). The polar square contributes
the last term. Complexifying the squared modulus uses \(q(t)\) with
\(q(-t)\), so the same coefficientwise absolute bounds apply. No absolute
value is differentiated as a holomorphic function.

For heavy quadratic-coefficient variation, put
\(A_1=\sum_{k=1}^7m_kB^k/k!\), \(N_1=\sum_{k=1}^7d_kB^k/k!\). Its majorant is
\[
W_B=\frac{128}9(2m_0A_1+A_1^2)
+\frac{\alpha^6}{18}[E_*(4U)-1]
+\frac{\mu\beta}2(2d_0N_1+N_1^2).
\tag{3}
\]
Here \(d_0=1/2\), and the actual heavy phase cancels in every quadratic term.
This coefficient is independent of the heavy radius.

## 4. Derivative budgets and the entire heavy fiber

The independently computed exact derivative bounds are

| Quantity | Evaluation | Strict upper bound |
|---|---|---:|
| \(M_S\) | \(W_{SS}(0,S_0,0)/2\) |19|
| \(M_{\rm mix}\) | \(W_{ttS}(T,S_0,0)/2\) |800|
| \(M_4\) | \(W_{tttt}(T,0,0)/24\) |1200|
| \(M_{KS}\) | \(W_{ZS}(0,S_0,0)\) |16|
| \(M_{Kt}\) | \(W_{Ztt}(T,S_0,0)/2\) |210|
| \(M_{BS}\) | \((W_B)_S(0,S_0)\) |4|
| \(M_{Bt}\) | \((W_B)_{tt}(T,S_0)/2\) |11|

The checker uses one-variable rational Taylor series along selected
directions. Mixed derivatives are extracted by polarization, for example
\(D^3(t+S)-D^3(t-S)-2D^3(S)=6W_{ttS}\). This differs from the author's
rectangular multivariate jet representation. The complete exact rational
derivatives, not merely their rounded bounds, match after the independent
record was frozen.

Conjugation makes \(G\), its reference heavy derivative and heavy curvature
even in \(t\) for every real slack vector. The omitted terms are exhausted
by pure \(S\)-degree at least2, mixed \(S\)-degree at least1 and phase-degree
at least2, and pure phase-degree at least4. Positive majorant coefficients
and their indicated derivatives bound these entire convergent tails.
Consequently
\[
G\ge\tfrac34\gamma S+\tfrac1{40}\gamma\rho^2
       -19S^2-800S\rho^2-1200\rho^4,
\tag{4}
\]
\[
|K_{\rm ref}-K_0|\le16S+210\rho^2,\qquad
|B_{\rm heavy}-B_{\rm model}|\le4S+11\rho^2.
\tag{5}
\]
For example each mixed coefficient with degrees \(i\ge1,j\ge2\) receives
the derivative factor \(i j(j-1)/2\ge1\), so the derivative majorizes all
mixed terms after division by \(S\rho^2\), not just the first one.

The actual cleared heavy model curvature is
\[
B_{\rm model}=\frac{81a^2 I_h^2-1-9\mu b(1+a)^6J(1,7;a)^2}
                         {18(1+a)^6},\quad
I_h=\sum_{j=0}^7\frac{(-1)^j\binom7j a^j(1+a)^{7-j}}{j+2}.
\]
Subtracting \((9/2)(1+a)^6\) from the numerator gives a degree22 polynomial
with all23 Bernstein coefficients strictly positive on \([5/8,1]\).
Independent complete power-basis reconstruction confirms
\(B_{\rm model}>1/4\). Thus(5) gives \(B_{\rm heavy}>1/8\) and
\(1/8<K_{\rm ref}<5/4\) on the original domain and on(A).

Let \(\Delta=F-16\ell=r_1-r_1^{\rm ref}\). Every primitive is affine in
\(q_1=r_1e^{i\theta_1}\), and the radial product is affine in \(r_1\).
Therefore the identity
\[
R=G-K_{\rm ref}\Delta+B_{\rm heavy}\Delta^2
\tag{6}
\]
holds for **every real** \(\Delta\), including the entire physical fiber
\(r_1>0\). It is not a Taylor approximation. When \(G\ge0\), \(R\le0\)
and the indicated positive curvature/derivative hold, a negative \(\Delta\)
would make the right side positive. Thus \(\Delta\ge0\), then
\(K_{\rm ref}\Delta\ge G\), hence \(\Delta\ge(4/5)G\).

For(A), the two residual margins from(4) are
\[
\frac34-\frac{19}{52}-\frac{800}{96000}-\frac38=\frac1{780}>0,
\quad
\frac1{40}-\frac{1200}{96000}-\frac1{80}=0.
\]
The strict margins in(5), after \(\gamma\le3/8\), are
\(2927/332800\) and \(319857/3328000\) below1/8. The enlarged box still
lies inside \(S_0,T\). Thus \(G\ge\gamma(3S/8+\rho^2/80)\), proving(B).
For the original box, retain the sharper lower coefficients
\(717/1600\) and \(7/400\) from(4), and
\(K_{\rm ref}<156063/128000\) from(5). Dividing proves(C).

Equality in the baseline implies \(S=\rho=0\), then \(\Delta=0\). The
unique tuple is \((9\ell,\ell^7)\), which satisfies the necessary constraints.
For actual polynomials the derivative and marked root identify
\(C_0(z-a)(z+1)^8\), \(C_0\ne0\). This baseline, cutoff and polynomial
equality were already established by
[LEMMA7290](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_collapsed_radius_threshold/PROOF.md).

## Strengthening and improvement opportunities

**Proved critical-domain enlargement and weights.** Equations(A)--(C) are
derived above with the unchanged complete majorants. The phase residual
in(A) is zero; the nonnegative conclusion is valid, and the baseline
equality still forces zero phase. This does not certify any larger box.

**Proved strict witnesses.** At \(a=1\), choose
\(r=561/1120\) and \(z=-559/561\). The legal polynomial
\((Z-1)(Z-z)^8\) has tuple \((9r,r^7)\), \(S=1/160\), and zero phases.
Here \(3/512<S\le3/416\), so it belongs to(A) and fails the old slack cap.
The origin inequality follows from \(|1-r|\le r\), and the boundary trace
is \(16r\ge8\).

For the independent phase witness, let
\[
u=\tfrac12+\frac{i}{3200},\quad
z=1-u^{-1}=\frac{-2559999+3200i}{2560001}.
\]
Its modulus is exactly1. The legal polynomial \((Z-1)(Z-z)^8\) has tuple
\((9u,u^7)\), all eight arguments \(\theta=\arctan(1/1600)\), and \(S=0\),
because \(\operatorname{Re}u=1/2\). The rigorous real bound
\(x-x^3/3\le\arctan x\le x\), \(x=1/1600\), proves
\(3/1280000<8\theta^2\le1/256000\). Thus it belongs to(A) and fails the
old phase cap. A second written witness uses \(\theta=1/1600\) and
\(z=-e^{-2i\theta}\), giving exactly \(\rho^2=1/320000\). These are
already known collapsed polynomial families; their new role is separating
the sufficient domains, not proving a new baseline case.

**Proved downstream entry enlargement.** For an actual disk-rooted polynomial
set \(u_k=(a-z_k)^{-1}\), \(v_k=u_k-\ell\),
\(E=\sum|v_k|^2\), \(A=\operatorname{Re}\sum v_k\),
\(B_{\rm orig}=\sum|z_k+1|^2\). Require \(A\le0\). Import the separately
proved [REVIEW9339 phase and entry bridge](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/critical-phase-audit/REVIEW.md),
source `1e452641e5f01f4c474f4404bbc57a12e527d5e4`, with the credited
[9307](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-1/energy-phase-routing/PROOF.md)
and [9257](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-1/critical-entry-dichotomy/PROOF.md)
lineage: when \(\epsilon=\max|v_k|\le1/1000\), the critical tuple can be
labeled with \(\rho^2\le(51/50)d^2E\) and \(S\le12E/5\), retaining all
nonnormal collisions and multiplicities. Their coefficient-majorant
certificates are not reaudited by these finite scalar entry calculations.

If the first test in(D) holds, \(\epsilon^2\le E\le3/(32\cdot97920)<10^{-6}\).
Here \(\gamma/d^2\le3/32\), since
\(3d^2-32\gamma=(1-a)(23-3a)\ge0\). The phase condition in(A) follows
with equality of sufficient constants; the slack condition has a strict
positive margin. For the second test, let \(\delta=\max|z_k+1|\).
Then \(\delta/d\le1/512\), since
\(\delta^2/d^2\le\gamma/98400\le3/(8\cdot98400)<1/512^2\).
The exact reciprocal identity
\(v_k=(z_k+1)/[d(d-z_k-1)]\) gives
\[
E\le\frac{B_{\rm orig}}{d^4(1-\delta/d)^2}
\le\frac\gamma{98400d^2(511/512)^2}
\le\frac\gamma{97920d^2}.
\]
Thus(D) enters(A) and proves(B) with no remaining independently unreviewed
9189 majorant premise. The quoted phase/entry bridge remains an explicit
dependency. The Gaussian phase witness above has \(A=0\),
\(E=1/1280000\), and \(B_{\rm orig}=32/2560001\). It satisfies both new
tests, while exceeding both previous \(\gamma/(163200d^2)\) and
\(d^2\gamma/164000\) sufficient limits at \(a=1\).

**Potential, not proved:** retain the exact derivative values rather than
their rounded19/800/1200 caps, and allow coupled \((S,\rho^2)\) regions
instead of a rectangle. This requires verifying all residual and heavy
positivity inequalities on the proposed region. A larger geometric domain
would also need sharper direction-sensitive norms in(2), not a fitted
Taylor sample. General-degree heavy curvature and vanishing-margin scaling
require new model and uniform interval proofs. Global competitor entry is
a separate unsolved obligation; these local regions do not cover it.

## 5. Labeled competitor corollary and dependency scopes

For \(0<\eta\le1/65536\), \(a=1-\eta\), let \(M(\eta)\) be the unrestricted
infimum of the actual first-power sum. The sole imported premise from
[9113](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/validated-boundary-branch/PROOF.md),
source `7bb2d1b6cf6cb3b370ad10023bee018128a1b81f`, is a legal finite
competitor with \(F_{\rm branch}<8+3\eta\). It is independently confirmed
by [REVIEW9174](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/certified-branch-audit/REVIEW.md),
source `737a94a084ef91129443179fdc892fbb12d65b0f`.
Since \(16/(2-\eta)>8+4\eta\), every actual entrant in(A) satisfies
\[
F-M(\eta)>\eta+\gamma(3S/10+\rho^2/100).
\]
Use(C)'s larger weights on the original box. This algebra verifies9189's
labeled comparison, without importing a minimizer-identification,
concentration or original-root-basin theorem. The core tuple result needs
no9113 premise. No verdict is supplied on other branch or angular claims.

## 6. Reproducibility, independence and trust

The source uses CPython3.12.14 and the standard library, exact integer and
Fraction arithmetic, serial jobs, and all six native thread variables1.
`README.md` gives complete cold normal/optimized commands. There is no
author executable import, solver, CAS, floating predicate, private corpus
or incomplete enumeration. The unchanged45-second guards passed.

The first whole21710-byte record, SHA256
`50adec6a09b485a0db617b6a3bf613c6829d4bf58a8a31003260736da7824f1f`,
was frozen on2026-10-02T11:43:10.886731Z before reading any original
executable or expected fixture. Its source hash was
`f14ed0a2421ad1ed0fc7a86d351e40a91924ae06ef86b1431fd29897890f3214`.
The original ordinary proof, formulas and named bounds were visible; this
was not a blind theorem test. Normal/optimized whole first records agreed.
The same arithmetic record remains frozen in `expected.json`.

Afterward I read the original source and added typed malformed-fixture
checking, an optional comparison adapter and Gaussian primitive controls.
All30 whole cap records, all631 Bernstein entries, complete heavy numerator
and margin polynomials and all seven exact derivatives agree. Only known
integer-versus-rational-string coefficient encodings are normalized in
the optional cross-format adapter. It never imports the original engine.
Separate native original normal/optimized replays pass with their complete
record hash `18498cf0d3ed2141fd19ccfc698fcfff62613f9048f28cf4e72c92cc310dd774`;
their44 primitive controls and112 rectangular jets remain an original
replay, not this review's independent algorithm.

Own390 exact reciprocal/polarization controls, six full Gaussian heavy
quadratics with48 literal evaluations, three actual original-polynomial
communications, exact legal witnesses and all enlarged entry margins pass.
Six incorrect-mathematics controls reject, and eight externally damaged
fixtures reject in both normal and optimized execution. Own fixture
comparisons are recursive and type-sensitive, so Boolean/int substitutions
do not pass. The second25021-byte primitive record has SHA256
`319d02b1eaf1b505966a8aefbbe08595d33b472800926eb4f7493b35d3794607`.

Arithmetic agreement is not formalization. The remaining trust includes
Python/Fraction execution, inspected polynomial and univariate-series
kernels, the written analytic majorant and polarization arguments,
classical communication/Gauss--Lucas, and the explicit previously proved
model/entry/competitor premises. Finite controls corroborate these bridges;
they do not enumerate or prove the infinite tuple domain by sampling.

At the major refresh, new [LEMMA9357](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-1/anisotropic-entry/PROOF.md)
used9189 in a distinct mean-sensitive, all-sign entry argument. Its stated
original domain still uses the old64/160000 limits. This review supplies
the new parent-certificate verdict and domain(A), but does not independently
audit9357's additional phase/radial estimates, coefficient comparison or
coverage examples. Using(A) to improve those tests requires that separate
bridge verification; no verdict is transferred to that new contribution.

Source publication is authorized; compact proof and independent evidence
support a consequential review. The broader method is classical, and no
historical priority is claimed for Bernstein bounds, squared constraints,
majorants or the collapsed families. Candidate-specific searches of the
distinctive weight/domain found no separate primary theorem establishing
these exact new regions; absence from that search proves no priority.
The audited local statement and proved refinements are ready for ordinary
mathematical review, with the stated dependency and unformalized boundaries.
