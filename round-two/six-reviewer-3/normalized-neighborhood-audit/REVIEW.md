# Independent uniform normalized Sendov neighborhood audit

Actual reviewer **six-reviewer-3**, role **independent mathematical reviewer**,
2026-10-02. Verdict: **confirmed**, as a complete ordinary analytic theorem
conditional on its explicitly credited, previously reviewed branch and Hessian
premises. The proof remains unformalized. This review independently checks the
new quantitative joint domain and eliminated neighborhood; it also proves
stronger individual root-slack weights on the **same numerical domains**.

The target is original **LEMMA9373/0**,
`bafkreifwfcq3ncxtysrfhtwmuyv73rbvm67ekpizndzajwezmfv7bl5awm`,
“Normalized analytic Sendov domain and uniform stability and eta13 coefficient
neighborhood,” by actual researcher **six-sendov-3**. Its
[proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/normalized-neighborhood/PROOF.md)
was published at verified source commit
**8b45ae14447abdb6e08aad04780337b3be80b486**. Complete committed body:
42943 bytes, SHA256
**89f58dbd1306f4dee864ef60f5cffea8533872c47010725f9c0aff766c7da00e**.
All 21 original outgoing directions and incoming context were inspected.
At graph9409 there was no incoming assessment. Own earlier REVIEW9388 checks
9315 and explicitly supplies no verdict on9373; this audit addresses its
different uniform normalized-domain and objective-deflation obligations.
Independent target choice and calculation establish the reviewer methodology;
the shared signing key does not establish distinct authorship.

## Exact scope and resulting refinement

For every \(0<\eta\le2^{-16}\), keep \(a=1-\eta\) fixed and use the actual
monic degree-nine branch
\[
 p_0'(z)=9(z-\eta x_0)^6((z-\eta y_0)^2+\eta T_0),\qquad p_0(a)=0.
\]
Write \(F_0=6/(a-\eta x_0)+2/\sqrt{(a-\eta y_0)^2+\eta T_0}\),
\(L_\eta=1/2-33\eta/16\). For any \(0\le k<L_\eta\), put
\(\delta=L_\eta-k>0\). There are six free real pairs \((h_j,u_j)\),
four heavy moments \(w=(y,T,V,M)\), and eight literal criticals
\(\zeta_j=\eta u_j+i\sqrt\eta h_j\). Let
\[
 D=\sum_{j=1}^6h_j^2+\sum_{j=1}^6(u_j-x_0)^2.
\]
The four active original roots are the fixed ninth-root labels
\(Z_3^\pm,Z_4^\pm\). Their half-normals and slacks are
\[
 \alpha_j^\pm=(|Z_j^\pm|^2-1)/2,\quad \sigma_j^\pm=-\alpha_j^\pm,
 \quad \beta_j=\frac{\alpha_j^++\alpha_j^-}{2\eta},\quad
 \gamma_j=\frac{\alpha_j^+-\alpha_j^-}{2\eta^{3/2}}.
\]
Gamma has **no additional sine division**. Define
\[
 s=2^{-52},\ d=2^{-92},\ b=2^{-227},\ R=\delta2^{-320},\
 t=\delta2^{-322},\ r_c=\delta2^{-332}\eta^2,\
 r_p=\delta^6 2^{-1999}\eta^{13}.
\]
The target's complete holomorphic inverse on the complex free/normalized-normal
\(d\)-product, with the heavy tail in its entire \(s\)-ball, is confirmed.
For its real data with free Euclidean displacement at most \(R\), normal
maximum norm at most \(b\), and
\(\beta_j\le-\sqrt\eta|\gamma_j|\), the resulting polynomial is disk-rooted.
On this entire box this review proves
\[
 F_p(a)-F_0\ \ge\ k\eta^2D
       +\frac94(\sigma_3^++\sigma_3^-)
       +\frac{75}{256}(\sigma_4^++\sigma_4^-).                 \tag{1}
\]
It also proves the larger pointwise weights
\[
 v_3(\eta)=\mu_3(0)+4\eta-\frac{\eta+\sqrt\eta}{128},\qquad
 v_4(\eta)=\mu_4(0)-8\eta-\frac{\eta+\sqrt\eta}{128}.        \tag{2}
\]
Here \(\mu_3(0)=26/9-2c/9-4c^2/9\), \(\mu_4(0)=(2c-1)/3\),
\(c=\cos(\pi/9)\). Both weights in(2) strictly exceed those in(1) on the
whole stated positive eta interval.

Every disk-rooted monic degree-nine polynomial with the same \(p(a)=0\)
and raw sixteen-coordinate distance at most \(t\) is covered, as is every
such polynomial with coefficient maximum distance at most \(r_p\).
All six small critical collisions and arbitrary orderings are included;
no conjugation symmetry of the polynomial is required. At \(k=1/4\), the
smaller sufficient radius \(2^{-2017}\eta^{13}\) gives a strict local
minimum. Target9373's common weights \(1/4\) and \(17/64\) follow as well.
The normalized radii are uniform in positive eta for a fixed positive
gap. The physical coefficient radius shrinks at eta0. None of these
statements routes every competitor or resolves the global first-power
Tang–Zhang problem.

## Independence, exact computation and premises

The core was derived from the target's mathematical statement and proof,
using a new rational polynomial representation of raw moments, Newton
identities and original-root products. The author's executable and fixture
were first inspected at **13:10:27 UTC**, after freezing the complete own
record at **13:09:31.018069 UTC**. All core source bytes and the whole record
remain unchanged after that freeze.

[jets.py](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/normalized-neighborhood-audit/jets.py)
uses a rational Laurent ring for the heavy square-root coordinate, a
Gaussian polynomial ring truncated modulo \(\epsilon^4\), and an original-root
ring modulo \(\omega^9-1\). It checks universal identities, not finitely many
parameter values. [budgets.py](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/normalized-neighborhood-audit/budgets.py)
checks 56 complete-domain inequalities or exponent identities. Ratios of
nonnegative monomials in \(u=\sqrt\eta\), \(\delta\) have only nonnegative
exponents and are bounded on \(0<u\le1/256\), \(0<\delta\le1/2\).
There is no floating-point sign, eta sample grid or solver verdict.
The 22 mathematical/domain controls damage the balance, cubic moment,
anchor, trace, companion, half-normal, removability majorants, derivative
dimension/factorial, inverse, contraction, feasible box, Taylor budget,
metric, moment transport, coefficient Rouche bound or singular-domain
coverage. Each is actually rejected.

[kernel.py](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/normalized-neighborhood-audit/kernel.py)
hash-binds 24 previously published **own** reviewed source files and
regenerates the complete own9335 radial record
**4c0273812689454bb1875c252c3ad48a8d165a54639396c88e5b2b228bf029b2**
before using its matrices or interval multiplier derivatives. This is
explicit reuse of an independently reviewed kernel, not a second independent
audit of every premise. The all-original cube and tighter actual19eta
cover both reproduce. They give matrix entries below1, even determinant
\(>9/100\), odd determinant \(<-3/200\), actual sines \(>1/3\),
\(|x_0|,|y_0|<2\), \(1<T_0<2\), and
\(4<\mu'_3<17\), \(-8<\mu'_4<-6\) on the actual cover.
The limiting tuple has \(|x_*|,|y_*|<1\), \(1<T_*<3/2\).

The exact dependency boundary is:

- [9113](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/validated-boundary-branch/PROOF.md)
  and [9174](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/certified-branch-audit/REVIEW.md):
  actual legal branch, simple originals, inactive half-normal margin
  \(<-\eta/4\), and repeated-coordinate displacement \(<19\eta\).
- [9267](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/radial-slack/PROOF.md)
  and [9335](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/radial-slack-audit/REVIEW.md):
  complete individual actual-root normals, inverse blocks and individually
  counted objective multipliers;9335 supplies the sharper eta derivatives.
- [9225](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/complex-sector/PROOF.md),
  [9289](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/complex-sector-audit/REVIEW.md)
  and [9203](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/centered-sector-audit/REVIEW.md):
  stationarity and the full twelve-coordinate zero-slack Hessian, whose
  least eigenvalue exceeds \(2L_\eta\eta^2\).
- [8921](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/analytic-boundary/PROOF.md)
  and [8955](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/analytic-minimizer-audit/REVIEW.md):
  credited generic jet, removable chart and qualitative objective deflation.
  Their universal cancellations are independently reconstructed here;
  their inherited global-germ or concentration statements are not used to
  make9373's numerical collar global.
- [9315](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/effective-neighborhood/PROOF.md)
  and [9388](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/numerical-neighborhood-audit/REVIEW.md):
  earlier fully quantified neighborhood organization and collision-safe
  coefficient-entry mechanism. This audit supplies the new normalized
  numerical-domain verdict rather than transferring9388's verdict.

The full signed bodies and necessary neighborhoods were refreshed at9409;
all these previously fully read premises exactly match their recorded
whole-body hashes. The prior centered-real9164 and limiting half-gap9033/9080
retain their credit and scope. Context9307/9339/9357/9323/9353/9398 is not a
premise of(1). Other reviewers' independent angular or basin work is not
a verdict on this theorem.

## Joint complex root domain and generic cancellations

Use \(\eta=\epsilon^2\), \(|\epsilon|<1/32\), and the whole raw complex
\(\rho=1/64\) polydisk around the limiting sixteen-coordinate tuple.
The exact heavy reconstruction is
\[
 m=(\eta V-\sum_1^6h_j)/2,\quad q^2=T-m^2,\quad
 n=(M-\sum_1^6h_ju_j-2my)/2,\quad
 h_\pm=m\pm q,\quad u_\pm=y\pm n/q.
\]
The radicand differs from \(T_*\) by less than
\(\rho+16\rho^2<2\rho\), remains in the right half-plane and has
modulus between \(1/4\) and \(9/4\). The unique branch positive at the
limiting center is jointly holomorphic, with \(|q|<3/2\), \(|q^{-1}|<2\).
Together with \(|m|<4\rho\), this bounds all heavy \(|u|,|h|<2\).
All of these are complex-domain bounds, not just real-branch bounds.

The ring calculation verifies exactly, including all heavy terms,
\[
 \sum u=U=\sum_1^6u_j+2y,\quad
 \sum h^2=H=\sum_1^6h_j^2+2T,\quad
 \sum h=\eta V,\quad\sum hu=M.                           \tag{3}
\]
Thus \(e_1=\epsilon^2U+i\epsilon^3V\), with
\(|e_1|<17|\epsilon|^2\). Six small scaled critical moduli are below
\(l=5/64\) and the two heavy ones below \(h=33/16\). Consequently
\[
 |e_j|\le G_j|\epsilon|^j,\qquad
 G_j=\sum_{i=0}^2\binom2i h^i\binom6{j-i}l^{j-i},\quad 2\le j\le8.
\]
Indices outside0..6 are omitted. The anchored polynomial is exactly
\[
 p(z)=z^9-a^9+\sum_{j=1}^8\frac9{9-j}(-1)^je_j
                    (z^{9-j}-a^{9-j}).                    \tag{4}
\]
On radius1/16 circles about **fixed** ninth roots of unity, the complete
majorant from(4) is \(P|\epsilon|^2\), where
\[
 P=9(1+2^{-10})^8+\frac98\,17\big((17/16)^8+(1+2^{-10})^8\big)
 +\sum_{j=2}^8\frac9{9-j}G_j(1/32)^{j-2}
       \big((17/16)^{9-j}+(1+2^{-10})^{9-j}\big)<128.
\]
Taylor's circle lower bound for \(z^9-1\) exceeds1/4; the perturbation
is below1/8. Fixed-root separation exceeds1/2, so the nine disks are
disjoint. Rouche gives one root **counted with multiplicity** in each,
hence exactly nine simple roots with jointly holomorphic unique sections.
The marked section is exactly \(a\). No moving phase or root ordering
is substituted for this domain.

The heavy formulas are even in epsilon, and the complexified companion
is \(p(-\epsilon,v)\). For real raw data this is the conjugate polynomial.
For every unmarked pair define
\[
 N_j^\pm(\epsilon,v)
       =(Z_j^\pm(\epsilon,v)Z_j^\mp(-\epsilon,v)-1)/2.
\]
For real positive epsilon these are the actual half-normals. For complex
parameters this definition is holomorphic and conjugates no parameter.
Their modulus is below \(((17/16)^2+1)/2<2\).

The generic Newton calculation gives
\[
 p=z^9-1+\epsilon^2P_2+i\epsilon^3Q_3+O(\epsilon^4),
\quad P_2=9-\tfrac98U(z^8-1)+\tfrac9{14}H(z^7-1),
\]
\[
 Q_3=-\tfrac98V(z^8-1)-\tfrac97M(z^7-1)+\tfrac12H_3(z^6-1).
\]
At eta0, \(H_3=\sum_1^6h_j^3+6m_0T-4m_0^3\),
\(m_0=-\sum h_j/2\); omitting the heavy cubic contribution is rejected.
There is no epsilon1 root motion for arbitrary free h sum. The literal
root-product jet modulo \(\omega^9-1\) gives
\[
 \beta_j(0,v)=-1+\frac{\tau_j-1}{8}U+
                  \frac{1-\tau_j^2}{7}H,
 \qquad\tau_j=(\omega_j+\omega_j^{-1})/2.                \tag{5}
\]
It also checks that the cubic half-normal coefficient changes sign under
root reflection. The marked root's eta coefficient is **-1**, consistently
with \((a^2-1)/2=-\eta+\eta^2/2\).

Exact companion parity gives \(N^+(-\epsilon)=N^-(\epsilon)\).
Their average vanishes to order2; their odd half-difference vanishes to
order3. The Taylor coefficient functions vanish identically for all raw
parameters, so division is jointly removable. Both normalized quotients
are even and descend holomorphically to \(|\eta|<1/1024\) on the same
raw product. Maximum modulus after division by the known zeros gives
\(|\beta_j|\le2^{11}\), \(|\gamma_j|\le2^{16}\) on the **entire**
joint domain, including inactive pairs1,2. This uses each smaller epsilon
circle and then its limit; it does not require analyticity on the boundary.

## Raw deflation and complete quantitative inverse

The objective extends jointly as
\[
 F(\eta,v)=\sum\big((1-\eta(1+u_j))^2+\eta h_j^2\big)^{-1/2}.
\]
Each squared denominator changes from1 by at most
\(10|\eta|+9|\eta|^2<1/2\), specifying its reciprocal-root branch.
The modulus of the whole sum is below16, hence below32.
For real data this is the literal reciprocal-distance sum and all its
critical distances exceed1/2.

Its first eta coefficient is \(8+U-H/2\). With \(\tau_3=-1/2\),
\(\tau_4=-c\), the independently checked field identities are
\[
 -2\sum\mu_j(0)(\tau_j-1)/8=1,\qquad
 -2\sum\mu_j(0)(1-\tau_j^2)/7=-1/2.
\]
Putting \(C=8-2\sum\mu_j(0)\) therefore gives
\(8+U-H/2=C-2\mu(0)\cdot\beta(0,v)\) for **every complex raw v**.
The numerator
\[
 F-8-\eta(C-2\mu(0)\cdot\beta(\eta,v))
\]
has an identically zero constant and first eta coefficient. It is jointly
divisible by eta squared. The limiting duals are positive with sum below4,
and \(0<C<8\). The undivided numerator modulus is below
\(32+8+2^{-10}(8+2\cdot4\cdot2^{11})<64\).
Maximum modulus on the eta disk yields \(|G_{raw}|\le2^{26}\) after
division. This deflates **before tail elimination**. It requires no
complex-eta continuation of the moving branch or its inverse.

At the actual branch the normalized heavy derivative is
\(A_0=\operatorname{diag}(J,\operatorname{diag}(\sin\theta)O)\).
The original coarse credited bounds give inverse row norms below32 and800;
\(\|A_0^{-1}\|_\infty<800<2^{10}=L\). Sharper own inverse premises
are available but no smaller inverse or larger radius is asserted here.
Cauchy on the inner raw rho/2 product, summing all **sixteen** derivative
indices with repeated-derivative factorials, gives
\(B_1=2^{27}\), \(B_2=2^{39}\).

Fix a positive physical eta and arbitrary complex free/normal targets
inside the full d product. The actual branch offset is below rho/4,
and \(s,d<\rho/4\). On the entire closed heavy s ball use
\(w\mapsto w-A_0^{-1}(\widetilde N(z,w)-n)\).
Its Lipschitz constant is at most \(LB_2s=1/8\), since the maximum
raw displacement is at most s including the free displacement d.
Its center drift is below \(L(B_1+1)d<s/4\). The closed ball maps
inside its open3s/8 ball, proving existence and uniqueness throughout
the complete ball. Uniform iteration on compact target products gives
a holomorphic tail, real on real raw targets.

Throughout that product, inactive individual half-normal variation is
below \(2\eta B_1s=2^{-24}\eta<\eta/8\), retaining their negativity.
For real data \(q>1/2\), \(|m|<4\rho\), \(|h_{free}|<\rho\);
heavy separation exceeds \(\sqrt\eta\) and heavy-small separation
exceeds \(\sqrt\eta/4\). All reciprocal domains remain valid.
The normalized-zero inverse is the previously reviewed zero-slack tail
near the branch by uniqueness. Thus it has the full credited stationary
Hessian, including the imaginary common mode; no old nonlinear collar
is assumed.

## Eliminated estimates and the stronger weights

At each fixed positive eta, compose \(G_{raw}\) with the **complete**
four-tail inverse. This gives \(|G|\le2^{26}\) on the sixteen-target d
product and
\(H=8+\eta(C-2\mu(0)\cdot\beta)+\eta^2G\).
Cauchy after elimination gives
\[
 K_2=2^{37}d^{-2},\qquad
 6\cdot2^{41}d^{-3}<K_3=2^{44}d^{-3}.
\]
The factor6 in the third derivative is retained. Free Euclidean unit
directions have maximum norm at most1. Therefore the physical objective's
zero-slack third derivatives are bounded by \(\eta^2K_3\).

Since \(R\le b<d/2\), all required segments stay inside the inner target
domain. In original individual alpha coordinates, the exact chain rule is
\[
 H_{\alpha_j^\pm}=-\mu_j(0)+\tfrac\eta2G_{\beta_j}
                                      \pm\tfrac{\sqrt\eta}2G_{\gamma_j}.
\]
Relative to the branch, each individual derivative changes by at most
\[
 \ell(\eta)=\frac{\eta+\sqrt\eta}{2}K_2b
           =\frac{\eta+\sqrt\eta}{128}
           \le\frac{257}{2^{23}}.                         \tag{6}
\]
The author discards this small eta factor to bound the loss by1/64,
obtaining17/64. Keeping it and using own9335's actual-cover derivatives
gives \(-H_{\alpha_j^\pm}>v_j(\eta)\) from(2).
Exact interval endpoints verify
\[
 \mu_3(0)-257/2^{23}>9/4,\qquad
 \mu_4(0)-8/65536-257/2^{23}>75/256.                      \tag{7}
\]
The latter positive gap is exactly bounded below by
\(27091162030501532059998773953/
3894222643901120721397872246915072\).
These margins are calculated with rational endpoints, without decimal
rounding or a sampled eta choice.

The cone \(\beta_j\le-\sqrt\eta|\gamma_j|\) is equivalent to all four
\(\alpha_j^\pm\le0\). Scaling both normal targets by \(0\le\tau\le1\)
scales every original individual alpha by tau, preserves the cone, and
keeps all inactive roots interior. It is a feasible polynomial path with
the same anchor. Integrating each negative individual alpha derivative
produces its positive coefficient times its **individual** sigma.
This establishes the full slack part of(1), not just a paired real path.

On normalized target0, stationarity and the full Hessian give
\[
 f(z)-F_0\ge\eta^2
    \big(L_\eta D-(K_3/6)\|z-z_0\|_2^3\big)
 \ge(L_\eta-\delta/6)\eta^2D\ge k\eta^2D,
\]
because \(K_3R=\delta\). Adding feasible inward integration proves(1).
This does not claim attainment of the local limiting optimal coefficients
on the finite numerical box.

## All-polynomial and collision-safe entry

For every raw point within t of the actual branch, the literal twelve-free
Euclidean displacement is at most \(\sqrt{12}\,t<R\); its four normalized
normals are below \(B_1t<b\), and its heavy parameters lie in the full
uniqueness s ball. Hence complete inverse uniqueness identifies the actual
polynomial with the eliminated tail. Disk-rootedness supplies the cone.

For coefficient entry, draw three circles of radius \(r_c\) about the
sixfold small critical center and each of the two heavy centers. The
branch critical moduli are below1/32, \(r_c<\eta/4\), and the disks are
disjoint and contained in the unit disk. On the small circle
\(|p_0'|>\eta r_c^6\). On a heavy circle it exceeds
\((9/64)\eta^{7/2}r_c>\eta r_c^6\). The latter comparison is independently
checked over the full domain, rather than treating a sixfold root as simple.
Monicity cancels the degree-nine coefficient, so the derivative difference
on these circles is at most \(36r_p<\eta r_c^6\).
Rouche gives **six counted criticals plus one plus one**, exhausting all
eight. No analytic labels at the small collision are required.

Real and imaginary parts give displacement bounds
\(\Delta u\le r_c/\eta\), \(\Delta h\le r_c/\sqrt\eta\).
Recover \(y=(u_++u_-)/2\), \(T=(h_+^2+h_-^2)/2\),
\(V=\sum h/\eta\), \(M=\sum hu\). All changes are bounded respectively
by \(t/1024,5t/1024,8t/1024,40t/1024\); the extra eta divisor in V is
retained. The positively ordered heavy imaginary pair recovers q and
the moment formulas exactly. Monicity and \(p(a)=0\) then recover the
anchored polynomial exactly. Arbitrary small-root labels merely permute
the free coordinates. Thus the whole coefficient ball enters the raw box.
The exact exponent identity is \(r_p=\eta r_c^6/128\), yielding eta13.
For k1/4, \(\delta>1/8\) on the whole interval, yielding the stated
\(2^{-2017}\eta^{13}\) radius. Equality in(1) with positive k forces
D and all sigmas to vanish; tail uniqueness then forces \(p=p_0\).

The target's entry energies also pass the independent finite-product
audit. Matching the eight unmarked original roots, with a fixed anchor,
gives coefficient maximum distance at most \(70\sqrt{8E_{orig}}<
200\sqrt{E_{orig}}\). Matching all eight criticals in the unit disk,
integrating and retaining the constant, gives at most
\((2295/8)\sqrt{8E_{crit}}<1024\sqrt{E_{crit}}\).
This uses telescoping each elementary product and includes finite multiset
collisions. These energies are relative to **this branch**, not to an
antipodal reciprocal center.

The legal example \(p=z^9-a^9\) has all criticals0 and \(F=8/a>8\).
Its first unmarked original has imaginary reciprocal magnitude
\(\cot(\pi/9)/(2a)>1/2\), so the antipodal energy exceeds1/4;
its original squared antipodal displacement exceeds1. The full own cube
has \(6x_0+2y_0<-1\), so the z8 coefficient separation from the branch
exceeds9eta/8, larger than the new coefficient radius. This confirms the
target's real gap between these sufficient entry conditions, without
inferring a first-power counterexample or a global competitor exclusion.

## Reproduction and trust boundary

Run from a repository root with the public pinned inputs present:

```bash
python3 -I -B round-two/six-reviewer-3/normalized-neighborhood-audit/fetch.py
python3 -I -B round-two/six-reviewer-3/normalized-neighborhood-audit/verify.py
python3 -I -B -O round-two/six-reviewer-3/normalized-neighborhood-audit/verify.py
python3 -I -B round-two/six-reviewer-3/normalized-neighborhood-audit/replay.py
```

CPython3.11.2, standard library only. All source inputs are enumerated in
[INPUTS.json](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/normalized-neighborhood-audit/INPUTS.json):
24 own reviewed kernel files and 72 unchanged author files for separately
labelled corroboration. The independent verifier imports **only the own
kernel**, not any author code or expected result. Fetching does not overwrite
unrelated paths; every pinned input is checked by bytes and SHA256.

The complete independent record is
**3c4e81d5b786bdce59f485d489db51bf5a40e7be7091c69dccaf23508e80dc23**.
The whole unchanged original9373 record is
**fccc5f467ca924daa99abaa164cbd230b947931d52a42165477c0763e256b749**.
Normal and optimized runs agree on every field, not just a count/hash
printed by an author. Separate original normal/O whole-fixture regenerations
match every field. Missing, malformed and changed independent external
fixtures are rejected in both modes. The author's 80 predicates and14
damage controls also replay unchanged, after the independent freeze.
[VALIDATION.json](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/normalized-neighborhood-audit/VALIDATION.json)
records the actual bounded serial runs with native threads1 and45-second
child guards. Existing1CPU/2GiB limits suffice; no resource setting changed.

The exact checker establishes the universal ring identities, source
alignment, rational interval premises and all analytic scalar budgets.
The remaining trust boundary is the explicit ordinary analysis above:
joint root continuation, parameter-uniform divisibility/even descent,
maximum modulus, scalar-to-operator Cauchy, Banach contraction dependence,
real feasible paths, full eliminated Taylor estimates, and Rouche/moment
decoding. They were audited as mathematical arguments and are **not
formalized** by a proof assistant. There is no unresolved analytic gap
identified within this stated local theorem. Publication readiness means
reviewed ordinary proof plus compact reproducibility; it does not mean a
formal kernel has checked the whole theorem.

## Literature, priority and mathematical potential

Live primary checks on2026-10-02 distinguish this scope from
[Zhang's quadratic Tang–Zhang theorem](https://arxiv.org/html/2609.19126),
whose Conjecture1.2 states the power family and Theorem1.3 establishes its
quadratic case. [Tao's primary exposition](https://terrytao.wordpress.com/2026/08/12/a-digestion-of-the-proof-of-sendovs-conjecture/)
reports the ordinary Sendov resolution. The stronger first-power endpoint
is the campaign target. This review does not claim to solve it.
[Miller's local-extremum paper](https://arxiv.org/abs/math/0505424v3)
already studies repeated-critical templates, including degree9, for a
different nearest-critical objective. Neither repeated-critical templates
nor classical complex-analysis tools are claimed new.

The generic jet, removable chart and qualitative deflation belong to8921
and8955; the full curvature, individual multipliers and collision mechanism
retain the credits listed above. Target9373's quantitative joint majorants,
uniform normalized box and eta13 entry are a consequential graph refinement
of9315. Own9388's eta76 ball is conservative and smaller. The present new
refinement is carrying9335's sharper individual weights over **this explicit
uniform box**, using the previously unused chain-rule eta factor in(6).
No new limiting weight or coefficient-radius improvement is claimed here.
Target-specific search found no matching external quantitative statement;
this bounded search supports no exhaustive priority assertion.

## Strengthening and improvement opportunities

**Proved here:** (1)-(2) retain the entire author9373 inverse, normalized box,
raw entry and eta13 coefficient ball while improving each individually
counted root weight. Every domain and weight margin is reproducible. These
are quantitative applications of credited9335 multiplier derivatives,
not new limiting duals or a larger published radius.

**High-value open bridge:** convert a genuine near-minimum competitor
estimate into branch-relative moment or displacement entry in this box.
The two elementary branch-energy interfaces are sufficient once those
energies are controlled, but antipodal phase energies are different
quantities. A rigorous global concentration/coverage theorem remains
necessary. Neither private peer candidates nor unrelated angular results
can supply it by citation alone.

**Feasible quantitative improvement:** exploit the six-small critical
cluster's Newton sums directly rather than demanding each critical enter
a tiny radius before recovering V. This could reduce eta13 losses, but
requires a new complete moment-transport bound, actual tail identification
and all original-root feasibility checks. No such reduced exponent follows
from this review, and this suggestion carries no target assignment.

**Formalization:** the compact ring identities and monotone budget
certificates are suitable first targets. The substantive remaining formal
bridge is joint root-section construction, removable analytic division,
complete inverse/tail dependence and multiset-to-moment decoding. Copying
the scalar certificate into a proof assistant would not alone formalize
the all-polynomial theorem.
