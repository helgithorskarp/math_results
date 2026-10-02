# Independent complex chamber audit, tighter remainder and wider sharp family

Actual reviewer **six-reviewer-1**, role **independent mathematical reviewer**,
2026-10-02. Target author: **six-sendov-1**, researcher. Shared campaign
signatures do not establish distinct authorship. I independently selected the
committed target after inspecting current claims and existing assessments;
neither the author nor a manager assigned the target or verdict.

**Verdict: confirmed with high confidence within the exact stated chamber
and the narrow written dependencies below.** The complete ordinary proof of
LEMMA9492 supports its universal complex-polynomial bound, actual original-root
feasibility of the sharp family, and both restricted infimum slopes. I find no
missing root-feasibility bridge or collision case. This review also proves
remainder constant **10**, a signed coefficient/critical-energy rigidity
estimate, and a **32-fold larger positive parameter interval for the particular
sharp family**. The universal chamber bound retains its original interval.
The argument is ordinary mathematics with independent exact corroboration,
not a proof-assistant formalization.

Target: *Whole complex coefficient-chamber exclusion and sharp restricted
boundary slope in degree nine*, LEMMA9492/0,
artifact **bafkreieuclmqmhkyubz7qmav6wybx5wyhd5eiiy2cdchakzgnflig3zxwy**.
I read its entire 19,585-byte defining body and all thirteen original directions.
The complete appended proof matches the pinned
[author proof](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-1/coefficient-chamber-sharp/PROOF.md)
at source commit **ceb9b1c6714c5fd1e6a841406bd90ea7a419ce21**.
At the substantive refresh through committed height9536, the only incoming
directions were contextual CITES from9506 and9533; neither supplies a verdict
on9492. Sufficient existing audits of different targets remain separate.

## Scope, quantifiers and dependencies

Let \(0<\eta\le e=2^{-16}\), \(a=1-\eta\), and
\[
 p(z)=z^9+\sum_{k=0}^8c_kz^k,\qquad |c_k|\le2\eta\quad(1\le k\le8).
\]
The coefficient \(c_0\) is unrestricted. Count all eight critical points
\(\zeta_j\) with algebraic multiplicity and put
\[
 F=\sum_{j=1}^8|a-\zeta_j|^{-1},\quad
 H=\sum_j|\zeta_j|^2,\quad T_m=\sum_j\zeta_j^m.
\]
The universal assertion imposes no anchor, original-root disk constraint,
real coefficients, conjugation symmetry, critical separation, or choice of
critical labels. Its conclusion is
\[
 F\ge8+\frac{14}{3}\eta-147\eta^{3/2}>8+4\eta.
\]
The actual disk-rooted subfamily additionally requires \(p(a)=0\) and all nine
original roots in the closed unit disk. The two restricted infima have slope
\(14/3\). Neither infimum is assumed attained.

The precise dependencies are:

- [9428](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-1/cyclotomic-exclusion/PROOF.md),
  artifact bafkreier566yyzlocgpxpumovbzjnryzr6tk6bdxotdicriwwog2j55sdq,
  supplies only all-critical localization and \(F>8+H/6-193\eta\).
  I separately inspected its ordinary contour/localization argument in that
  scope. This is not a verdict on its other quarter-power claims.
- [9113](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/validated-boundary-branch/PROOF.md),
  artifact bafkreie2x4vb54jbygq7gdf7vxntw3gpkvkcugilrw5yvumrdpnq32jrx4,
  supplies only the actual legal comparison \(M(\eta)<8+3\eta\), where \(M\)
  is the unrestricted marked disk-rooted infimum.
  [9174](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/certified-branch-audit/REVIEW.md),
  artifact bafkreibzh4ue3r4fqrfr7d5qi7vvdw4whoxy7vlzu6pbhecqkftsfqiji4,
  already independently confirms that comparison family and interval.
  I check scope compatibility and import this previously audited comparison;
  I do not independently rebuild its continuation certificate here.

Both precise source dependencies are byte-pinned, including full SHA256,
in [author-replay.json](author-replay.json). Newton's identities, binomial
convergence, contour integration, Rouché, holomorphic simple-root sections,
Cauchy estimates and the squeeze argument are ordinary written mathematics.
All finite checks use rational arithmetic and whole records.

## Critical localization and the retained-energy inequality

For completeness, the scoped9428 localization follows from
\(h=p'/9=z^8+\sum_{k=1}^8(k/9)c_kz^{k-1}\).
On \(|z|=1/4\), the strict Rouché margin is
\[
 9(1/4)^8-\frac{2e}{(1-1/4)^2}=\frac{49}{589824}>0.
\]
Thus all eight criticals, including collisions, have modulus less than \(1/4\).
In particular \(F\) is finite on this entire chamber.

The coarse energy estimate has an analytic annulus argument, not an
unjustified logarithm through \(z=0\). On \(|z|=5/8\), set
\(q=(h-z^8)/z^8\), \(f(z)=G(z/a)\), \(G(t)=(1-t)^{-1/2}\), \(G(0)=1\).
Then
\[
 |q|<B\eta<1/900,\quad B=\frac{2147483648}{31640625}.
\]
The series for \(\log(1+q)\) is single valued on an annulus around that circle.
The argument principle counts all critical multiplicities, and integration
by parts on the closed circle gives
\[
 \Theta=\sum_jG(\zeta_j/a)-8
 =-\frac1{2\pi i}\int_{|z|=5/8}f'(z)\log(1+q(z))\,dz.
\]
Since \(a>255/256\), \((5/8)/a<32/51\) and
\(|G'(z/a)|<9/4\), the complete bound is
\[
 |\Theta|<\frac{24}{17}B\frac{900}{899}\eta<96\eta.
\]
For \(|\zeta/a|<64/255\), the square identity below gives
\(|G(\zeta/a)-1|^2\ge|\zeta/a|^2/6\): indeed the denominator is less than
\((9/8)^2(17/8)^2=23409/4096<6\).
Consequently \(F\ge8/a+(2/a)\Re\Theta+H/(6a^3)>8+H/6-193\eta\),
using \(2(256/255)96<193\).
This validates the exact imported hypotheses, constants and multiplicity
scope needed by9492.

Newton's identities give
\[
 T_1=-8c_8/9,\qquad T_2=T_1^2-14c_7/9,\qquad |T_2|\le H.
\]
For the analytic square root \(s(t)=\sqrt{1-t}\), \(s(0)=1\),
\[
 |G(t)|^2=2\Re G(t)-1+|G(t)-1|^2,\qquad
 G(t)-1=\frac{t}{s(t)(1+s(t))}.
\]
When \(|t|\le r\le1/6\),
\(|1+s|^2\le1+2\sqrt{1+r}+1+r\le4+2r\).
Therefore the squared denominator is at most
\((1+r)(4+2r)\le4+8r\), and
\[
 |G(t)-1|^2\ge(1/4-r/2)|t|^2.
\]
The last inequality uses
\(1/(4+8r)-(1/4-r/2)=r^2/(1+2r)\ge0\).

For every integer \(m\ge3\), the binomial coefficients
\(g_m=\binom{2m}{m}/4^m\) satisfy
\(g_{m+1}/g_m=(2m+1)/(2m+2)<1\), hence \(g_m\le5/16\).
Absolute convergence gives the infinite tail bound
\[
 |G(t)-1-t/2-3t^2/8|\le\frac5{16}\frac{|t|^3}{1-|t|}.
\]
Summing over all criticals costs at most
\((5/8)rH/[a^3(1-r)]\le(3/4)rH/a^3\). Since
\(|G(\zeta/a)|^2=a/|a-\zeta|\),
\[
 F\ge\frac8a+\frac{\Re T_1}{a^2}+\frac{3\Re T_2}{4a^3}
       +e_r\frac H{a^3},\qquad e_r=\frac14-\frac54r.       \tag{A}
\]
Here \(e_r\ge1/24>0\), and
\[
 F\ge8/a+\Re T_1/a^2-d_r|T_2|/a^3,\qquad
 d_r=\frac12+\frac54r.                                   \tag{B}
\]
Neither the infinite tail nor multiplicity coverage comes from finite
series enumeration.

If \(F>8+5\eta\), the advertised lower bound is immediate. Otherwise the
coarse estimate gives \(H<1188\eta\), so all critical ratios satisfy
\[
 |\zeta_j/a|<36\sqrt\eta\le9/64<1/6.
\]
Use \(|T_1|\le16\eta/9\),
\(|T_2|\le28\eta/9+256\eta^2/81\) in(B). The entire rational baseline
remainder after subtracting \(8+(14/3)\eta\) is
\[
 \frac{\eta^2}{a^3}
       \left(-\frac{146}{81}-6\eta+\frac{14}{3}\eta^2\right)
 \ge-2\eta^2.                                            \tag{C}
\]
This follows on the full interval from
\((33/32)(146/81+6e)<2\) and \(a^{-3}<33/32\).
The other term costs less than
\[
 \frac54\frac{33}{32}\frac{25}{8}36\,\eta^{3/2}
 =\frac{37125}{256}\eta^{3/2}<146\eta^{3/2}.
\]
Since \(2\eta^2\le\eta^{3/2}/128\), constant147 follows. Its strict comparison
with \(8+4\eta\) has margin
\(14/3-147/256-4=71/768>0\). These are whole-interval bounds.

## Actual original-root feasibility and the restricted slope

Integrating
\[
 p_\eta'(z)=9((z+b)^2+v)^4,\quad
 b=2\eta/9,\quad v=7\eta/18-28\eta^2/81
\]
and subtracting the entire primitive at \(a\) fixes the unique marked monic
polynomial. The full derivative and anchor are checked independently.
Its coefficients satisfy \(c_8=c_7=2\eta\). The critical values
\(-b\pm i\sqrt v\) each occur four times.

For complex \(|\eta|<\rho=1/128\), majorize the whole derivative by
\(9((z+(2/9)t)^2+Vt)^4\), \(t=|\eta|\),
\(V=7/18+28\rho/81\).
After integration, all six lower coefficients have order at least two in
\(t\), with positive endpoint bounds below4. Independently regenerated
bounds agree exactly with all six author fractions, so
\(|c_k|\le4|\eta|^2\), \(1\le k\le6\), on this whole complex disk.
The actual anchored polynomial, including its constant term, obeys
\[
 |p_\eta(z)-(z^9-1)|\le P|\eta|\quad(|z|\le17/16),
 \qquad P=\frac{1480778418455293707}{72057594037927936}<21.
\]
The constant-term estimate uses \(|(1-\eta)^9-1|
\le9|\eta|(1+\rho)^8\) as well as both evaluations of every lower coefficient;
there is no unanchored-polynomial substitution.

Draw circles of radius \(d=1/16\) around the nine ninth roots \(\omega\).
Their separation exceeds \(1/2\), so their disks are disjoint.
On every boundary, the complete Taylor remainder gives
\[
 |z^9-1|\ge9d-36(1+d)^7d^2>1/4,
 \qquad |p_\eta(z)-(z^9-1)|<21/128<1/4.
\]
Rouché gives exactly one multiplicity-counted root in each disk, hence nine
simple roots and uniquely holomorphic sections \(Z_\omega(\eta)\) on the
whole complex parameter disk. The section at \(\omega=1\) is exactly \(a\).
No critical labeling or differentiability assumption is needed.

For a root in its disk,
\[
 \left|\frac{Z_\omega^9-1}{Z_\omega-\omega}\right|
 \ge9-36d(1+d)^7>5,\qquad |Z_\omega-\omega|<5|\eta|.
\]
Use the limiting quotient when \(Z_\omega=\omega\).
The holomorphic companion
\[
 \alpha_\omega(\eta)=\frac{Z_\omega(\eta)Z_{\bar\omega}(\eta)-1}{2}
\]
equals the actual \((|Z_\omega|^2-1)/2\) for real \(\eta\), because this
particular polynomial has real coefficients. It satisfies
\(|\alpha_\omega|\le(5+25\rho/2)|\eta|<6|\eta|\).
The removable quotient \(\beta_\omega=\alpha_\omega/\eta\) has bound6.
Cauchy's coefficient estimate, first on smaller circles and then their
limit, gives
\[
 |\beta_\omega(\eta)-\beta_\omega(0)|
 \le6\frac{|\eta|/\rho}{1-|\eta|/\rho}\le6/511\quad(0<\eta\le e).
\]
The whole polynomial first jet is
\[
 p_\eta=z^9-1+\eta(2z^8+2z^7+5)+O(\eta^2),
\]
and implicit differentiation gives, for \(\omega=e^{i\theta}\),
\[
 \beta_\omega(0)
 =-\frac{5+2\cos\theta+2\cos2\theta}{9}
 =-\frac{4(\cos\theta+1/4)^2+11/4}{9}\le-11/36.
\]
Thus \(\beta_\omega(\eta)\le-5405/18396<0\).
All nine actual originals are strictly interior for every positive parameter
in the target interval. Small criticals alone would not prove this.

The exact objective is
\[
 F_\eta=\frac8{\sqrt{1-7\eta/6+7\eta^2/27}},
\]
with right derivative \(14/3\) at zero. Let \(I_{\rm ch}\) and \(I_{\rm disk}\)
be the unrestricted-complex and actual-disk-rooted chamber infima. For every
positive parameter,
\[
 8+(14/3)\eta-147\eta^{3/2}
 \le I_{\rm ch}(\eta)\le I_{\rm disk}(\eta)\le F_\eta.
\]
Dividing after subtracting8 and taking \(\eta\downarrow0\) proves both slopes
by a squeeze. The test family makes both sets nonempty. No optimizer or
compactness/attainment theorem is smuggled into this argument.

## Strengthening and improvement opportunities

### Proved: remainder10 on the entire original chamber interval

Retain(A) before discarding its energy. If \(F\le8+5\eta\), multiplication
by \(a^3\) and the two trace bounds gives
\[
 e_rH\le R(\eta),\quad
 R(\eta)=\frac{10}{9}\eta+\frac{43}{27}\eta^2+7\eta^3-5\eta^4
 <\frac98\eta.                                          \tag{D}
\]
The numerator is an independently checked whole polynomial identity.
The last estimate follows from
\(10/9+(43/27)e+7e^2<9/8\), dropping only a negative term.

At the first radius \(r_0=36\sqrt\eta\), \(e_{r_0}\ge19/256\).
Thus \(H<(288/19)\eta<16\eta\), and we may replace the radius by
\(r_1=(33/8)\sqrt\eta\), since \(4(256/255)<33/8\).
Now \(e_{r_1}\ge1883/8192\), whence
\[
 H<(9216/1883)\eta<5\eta.
\]
Since \(\sqrt5<9/4\) and \((9/4)(256/255)<23/10\), take
\(r_2=(23/10)\sqrt\eta\); its energy coefficient is at least489/2048.
Using this radius in(B), the full cost including(C) is
\[
 \frac54\frac{33}{32}\frac{25}{8}\frac{23}{10}+\frac1{128}
 =\frac{18991}{2048}<10.
\]
The \(F>8+5\eta\) case remains immediate, so for EVERY polynomial in the
original complex chamber and EVERY \(0<\eta\le2^{-16}\),
\[
 \boxed{F\ge8+(14/3)\eta-10\eta^{3/2}>8+4\eta.}            \tag{E}
\]
For actual disk-rooted chamber competitors the imported legal comparison
therefore gives the stronger full-window gap
\[
 \boxed{F-M(\eta)>\frac{625}{384}\eta,}
\]
because \(14/3-10/256-3=625/384\).
This gap is conditional only on the already stated comparison premise;
it is not an attainment or global minimizer claim.

### Proved: signed coefficient and real-critical-energy rigidity

On the same chamber and interval, assume additionally \(F\le8+5\eta\).
Put \(\Delta_8=2\eta-\Re c_8\ge0\), \(\Delta_7=2\eta-\Re c_7\ge0\).
Rewrite the last two terms of(A) as
\(d_r\Re T_2+e_r(H+\Re T_2)\).
The identity \(H+\Re T_2=2\sum_j(\Re\zeta_j)^2\) is exact.
Also
\(\Re T_2\ge-256\eta^2/81-(14/9)\Re c_7\).
With the final radius \(r_2\), \(a^{-2},a^{-3}\ge1\),
\(d_{r_2}\ge1/2\), and \(e_{r_2}\ge489/2048\), the whole signed
decomposition yields
\[
 \boxed{F\ge8+(14/3)\eta-10\eta^{3/2}
       +(8/9)\Delta_8+(7/9)\Delta_7
       +(489/1024)\sum_j(\Re\zeta_j)^2.}                 \tag{F}
\]
The residual term discarded in this decomposition is
\(d_r(\Re T_1^2+256\eta^2/81)/a^3\ge0\).
The full free-variable identity is checked, including this residual.

For any fixed \(K\ge0\), if
\(F\le8+(14/3)\eta+K\eta^{3/2}\) and
\((K+10)\sqrt\eta\le1/3\), the low-sublevel hypothesis follows.
Every nonnegative gap in(F) is then bounded by \((K+10)\eta^{3/2}\):
\[
 \Delta_8\le\frac98(K+10)\eta^{3/2},\quad
 \Delta_7\le\frac97(K+10)\eta^{3/2},\quad
 \sum_j(\Re\zeta_j)^2\le\frac{1024}{489}(K+10)\eta^{3/2}.
\]
Since \(|c_k-2\eta|^2\le4\eta\Delta_k\) for \(k=7,8\), both complex
coefficients are \(2\eta+O(\eta^{5/4})\), and
\(H=(28/9)\eta+O(\eta^{3/2})\).
These are necessary restrictions on near-sharp sequences. They do not
force a four-plus-four critical multiplicity or a unique leading profile.

### Proved: actual sharp-family feasibility through \(2^{-11}\)

The same complex-disk proof gives the sharper displacement
\(|Z_\omega-\omega|<(21/5)|\eta|\). Hence
\[
 |\beta_\omega|<
 \frac{21}{5}+\frac12(21/5)^2\rho
 =\frac{27321}{6400}<\frac92.
\]
For EVERY real \(0<\eta\le2^{-11}\), \(\eta/\rho\le1/16\), so
\[
 |\beta_\omega(\eta)-\beta_\omega(0)|\le3/10,\qquad
 \beta_\omega(\eta)\le-11/36+3/10=-1/180<0.
\]
Rouché still gives nine simple sections, and \(v>0\),
\(4\eta^2<2\eta\) and \(1-7\eta/6+7\eta^2/27>0\) throughout this larger
interval. Thus the identical anchored family has nine simple strictly
interior originals, remains in the coefficient chamber and has the
identical exact objective for all \(0<\eta\le2^{-11}\).
**This extends only the test family.** Neither(E), (F), universal sublevel
emptiness nor the comparison gap is extended beyond \(2^{-16}\).

### Remaining opportunities and limitations

The consequential next step is complementary coefficient coverage.
The known legal comparison is outside cap2; excluding this chamber
cannot exclude the comparison branch. To extend the method, one must
retain signed trace/energy information and prove actual original-root
constraints for the additional coefficient directions on an explicitly
stated interval. A critical-radius bound or a finite root grid supplies
neither that feasibility nor all-competitor entry. A complete classification
of near-sharp profiles would require a converse and a realization for every
admissible normalized critical profile, beyond(F)'s necessary moments.
Further improvement of constant10 requires a sharper certified radius/tail
budget; failure of our constant9 budget is not evidence that constant9 is
false. Formalizing the analytic branches and root-continuation argument
would strengthen the trust boundary without enlarging the mathematical scope.

## Independence, reproducibility and trust boundary

I saw the defining ordinary proof, but sealed the new independent executable
and entire fixture at **2026-10-02T15:40:33.483057+00:00**, before any target
executable/EXPECTED/VALIDATION materialization at
**2026-10-02T15:41:03.525790+00:00**.
The seal records exact frozen file hashes and methodology in
[independence.json](independence.json).

The unchanged rational polynomial kernel is credited to my own
[earlier kernel audit](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-1/uniform-support-audit/algebra.py),
source **448db1d41bc84a0e5bf2c6f6ce00a043b9a337dd**, REVIEW9455.
No earlier mathematical verdict transfers. All new target checks are freshly
implemented in [core.py](core.py), with no author import or fixture input.

Independent evidence includes the entire anchored bivariate original
polynomial, derivative, first jet, reciprocal-distance polynomial, retained
energy numerator and seven-variable signed slack; a fresh simultaneous
\(\mathbb Q[C_9]\) original-section recurrence through order6, with all
original residual coefficients checked at every stage; all companion
half-normal coefficients; five literal Gaussian-rational critical multisets
including total collision, repeated pairs, a genuinely nonconjugate case
and unequal imaginary amplitudes; and39 whole-window strict margins.
Literal controls build and anchor the full original polynomial and check
Newton identities, chamber constraints and real-part energy. They do not
assert original-root disk feasibility. Finite original sections corroborate
the written Rouché/Cauchy proof; they do not establish its all-parameter coverage.

The ten mathematical damages include a changed actual anchor, omitted
nonzero \(T_1^2\), wrong half-normal, missing critical multiplicity, invalid
interval/type, dropped actual positive real energy and two failed proof
budgets. The \(H<4\eta\) and constant9 damages show that those conclusions
do not follow from the displayed budgets; they are not counterexamples to
stronger possible theorems. Four external fixture damages (actual polynomial
coefficient, missing literal, extra field and changed numeric type) fail
under optimized Python as well.

The normal and optimized independent runs agree on the entire typed record:
canonical SHA256
**a4a697c3fed5dc8a4b0c90697381df52e30aad777b4586399a5a61a9b43112f8**,
five literal controls, ten mathematical damages, order6 original sections
and39 margins. Wall times0.491/0.636s; child peak20060KiB.
After sealing, I read the complete author executable and compact validation
files and reran its normal/optimized full fixture unchanged:
SHA256 **05732eacfe94a3e6583118d70cc8e315e936ec0890d067d518be9d4913500f7f**,
20 whole identity/control records,28 margins and11 mathematical damages,
0.111/0.280s, child peak21112KiB.
Every original-polynomial/derivative coefficient, all six complex-disk
majorants and all nine first root/half-normal coefficients agree with the
independent record. The author's18 external-fixture rejections are reported
in its validation file, not independently rerun here.

Tested CPython3.12.14, standard library only; all six native thread variables1,
serial children, fixed45/50-second guards and unchanged1CPU/2GiB scope.
No resource limit was hit or increased. No floating roots, solver, CAS,
finite parameter grid or incomplete enumeration establishes any assertion.
The complete records, not selected hashes or counts, are regenerated and
compared. Explicit exceptions preserve checks under optimized Python.
Reproduction commands and expected result are in [README.md](README.md);
the exact fixture is [expected.json](expected.json).

## Literature, novelty and publication readiness

The [current primary Zhang paper](https://arxiv.org/html/2609.19126)
states the strongest first-power sum as Conjecture1.2 and proves the quadratic
Theorem1.3. [Tao's primary exposition](https://terrytao.wordpress.com/2026/08/12/a-digestion-of-the-proof-of-sendovs-conjecture/)
addresses ordinary Sendov. This chamber review resolves neither the global
first-power endpoint nor global branch optimality.

The [earlier full critical4+4 theorem7833](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_full_critical_four_four_first_power/PROOF.md)
already treats that whole multiplicity class; the present family is a
restricted-chamber sharpness witness. Qualitative concentration, bootstrap,
leading original-root radial constraints and unrestricted asymptotic
boundary analysis already occur in
[8530](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/sharp-boundary-slope/PROOF.md)
and its sufficient scoped
[8608 audit](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/sendov-boundary-audit/REVIEW.md).
No classical method, Newton identity or square-root concentration scale
is claimed new.

Fresh
[9533](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-sendov-3/coefficient-chamber/PROOF.md)
states an effective actual-disk-rooted cap8 theorem, including the comparison
branch. I inspected its statement and relation to9492, not its complete proof
or executable; it receives no verdict here and is not a premise.
Likewise9506's sufficient audit of9438's fixed normalized collar is context,
not this chamber's assessment. No peer verdict or larger-domain constant
transfers. The distinct cap2 bound, cap8 statement and collar hypotheses
must remain distinct.

Candidate-specific primary searches for the coefficient chamber and slope
14/3 found no exact matching theorem; the bounded committed campaign intake
likewise found no duplicate assessment. These searches do not establish
historical priority. The publishable content here is a scoped independent
confirmation plus the explicit proved refinements(E), (F) and the enlarged
actual sharp-family interval. A standalone exposition should retain the
dependency declarations and ordinary complex-analysis trust boundary.
