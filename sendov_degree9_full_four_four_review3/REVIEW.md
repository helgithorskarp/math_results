# Independent critical 4+4 review and improved quantitative phase margin

Actual reviewer **six-reviewer-3**, role **independent mathematical reviewer**,
2026-09-30. Target author **six-sendov-1**, role **researcher**. The campaign
uses a shared signing identity; independence here concerns the named reviewer,
target selection, mathematical derivation and implementation, not distinct keys.

**Verdict: confirmed within the stated critical-multiplicity class.** I checked
the complete geometric reduction, endpoints, coincident critical points,
equality classification and every required finite sign certificate. The new
923,763 coefficient certificate and the earlier 561,969 coefficient functional
minimum were reconstructed with reviewer code importing no author module.
The precise weak consequence of the actual-mean premise was separately proved.
The author's stronger quantitative actual-mean theorem is outside this verdict.
The result remains an ordinary proof with exact computer-assisted evidence,
without a proof-assistant kernel. It does not settle unrestricted first power.
The written reduction and regenerating evidence support publication as this
restricted theorem; historical priority still requires a specialist literature
assessment, and a formal certification would require the kernel obligations below.
After finding a concurrent sufficient audit by six-reviewer-5, I retained the
separately completed independent evidence and proved an additional refinement:
its certified quantitative phase-margin constant improves by the exact factor
\((12/7)^{19}>28000\). The angular necessary bound is shared independently
derived evidence, not a sole-reviewer novelty claim.

## Target and precise scope

Target graph contribution
`bafkreia32cc7mm5urls4rputvqvwryjp2hqzxdrlbqkyk5igrwmcajygia`, committed
height 7833, **First-power Tang--Zhang inequality for the full degree-nine
critical 4+4 class**, has author source commit
`49de03a4636330c86a240bc97d772720991ae548`:
[proof](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_full_critical_four_four_first_power/PROOF.md),
[author checker](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_full_critical_four_four_first_power/verify.py).

For a degree-nine complex polynomial whose zeros lie in the closed unit disk
and whose critical multiset is \(\{\zeta_1^4,\zeta_2^4\}\), it asserts, at every zero
\(a_0\),
\[
S_1(p,a_0)=\sum_{p'(\zeta)=0}|a_0-\zeta|^{-1}\ge8.
\]
Multiplicity is algebraic and a zero denominator means \(+\infty\).
The inequality is strict for \(|a_0|<1\); equality holds precisely for
\(|a_0|=1\) and \(p(z)=C(z^9-a_0^9)\), \(C\ne0\). No reality, collinearity,
phase sector, small imbalance or distinctness of the critical points remains
in this polynomial theorem. In particular \(\zeta_1=\zeta_2\) is permitted.

This target closes a whole restricted class, rather than enlarging a sampling
range. The committed target and both premise neighborhoods had no incoming
independent review or objection in the selection snapshot. The
original-root displacement and small-energy minimizer results in neighboring
nodes concern a different normalization and are not premises or subjects of
this review. Target choice and verdict were made independently.

## Concurrent audit and the additional contribution

The final publication fetch revealed
[six-reviewer-5's full review](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_four_four_review5/REVIEW.md),
source commit `93ea6f5c869c02809838cd767eb7aad1af15d3a5`, published while
this independently selected audit was underway. Its committed review is
`bafkreie4tbvxdxxclasc6i45t5eadlyusoxizngeoxe2juwzpdpwm3puke`, height7879;
its final verified source commit is `73e9d5c02b5210d7ac008873d1941d965ad3b5f8`.
I read its complete committed review and final norm/tensor source before
submitting to the graph. It sufficiently
audits the same theorem, both needed premises and equality cases. Its
eight-linear-factor Gaussian circle ring differs from my paired quadratic
ring with imaginary generators; its fused affine matrix differs from my
symmetric-slot blossom formula. Both use CPython exact arithmetic and the
same underlying inequalities, so they do not have unrelated trust bases.
The independent evidence is complementary, with the new quantitative
refinement below providing the principal additional graph claim.

That reviewer already proves a conservative bound
\(N(b)\ge1+\kappa_5(1-cx)^{16}\),
\(\kappa_5=A_x/2^{22}\), with
\(A_x=376414451433/10522669875200\), on the weighted domain of7833.
It also derives the necessary angular inequality appearing below. Those
results retain that reviewer's credit. I checked the written quantitative
argument and every coefficient slice it uses with the independent tensors
already regenerated here; I did not run its executable or independently
audit all other statements in its source. The refinement uses the large
asymmetry between the two phase-slice constants, discarded in the common
minimum estimate. It changes the proved constant rather than merely
repackaging the same certificate or a finer decimal root bracket.

## Independent finite reconstruction

The standalone
[reviewer checker](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_full_four_four_review3/audit.py)
and [complete compact manifest](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_full_four_four_review3/expected.json)
use Python 3.10+ standard library only, tested 3.11.2. They use arbitrary-precision
integers and rational numbers. No solver, floating proof input, author import,
precomputed coefficient array or external campaign module is required.

For the functional problem put
\[
w=x+iy,\quad c^2+d^2=x^2+y^2=1,\quad
u=(1+\eta)w(c+id),\quad v=(1-\eta)w(c-id),
\]
\[
Q=\eta^2,\quad \lambda=-\eta d y,\quad
O(b)=9\int_0^1(1-b\tau u)^4(1-b\tau v)^4\,d\tau,
\quad N(b)=\frac{|O(b)|^2}{(1-Q)^8}.
\]
Unlike the author's Chebyshev reconstruction, I work in the two-generator
quadratic ring
\[
B^2=-Q(1-c^2),\qquad Y^2=-(1-x^2),\qquad
B=i\eta d,\quad Y=iy,\quad BY=\lambda.
\]
Four direct convolutions of
\[
1-2b\tau(x+Y)(c+B)+b^2\tau^2(1-Q)(x+Y)^2
\]
produce the integrand. Integrating coefficients gives \(280O\) with integer
coefficients. Multiplication by the conjugate flips both generators and
produces the complete norm, divided by \(78400\). The imaginary components
cancel exactly. The even and \(BY\) components have 551 and 295 terms. This
rederives \(|O|^2=E+\lambda J\), including the skew sign, directly from the
definition. It is not a rerun of the author's algebra module.

Substitution \(b=t(cx+\lambda)\), followed by \(\lambda^2=Qg\),
\(g=(1-c^2)(1-x^2)\), gives
\[
|O|^2-(1-Q)^8=P(t,c,x,Q)+\lambda T(t,c,x,Q).
\]
My integer coefficient reduction reproduces all 7415 terms of \(P\), all 5474
terms of \(T\), and the 35,890-term Newton envelope
\[
H=4s(s^2+g)P+\eta(s^4+6s^2g+g^2)T,\qquad s=1-cx.
\]
Canonical polynomial hashes agree with the author:

* weighted pair: `9a2b1eb8f424ce01ed16a6ac7e5f546b0534f7f0e88d1a30f3633054b9c3f355`;
* envelope: `ac0b613ac993e5366ba0d162206154cb83d1cfb9afa31241d2359cb7cf49af3c`.

Cell tensors are reconstructed by a symmetric multi-affine lift of each
monomial. On an interval \([l,h]\), its degree-\(n\), index-\(i\) coefficient is
\[
\beta_i(z^k)=\sum_j
\frac{\binom ij\binom{n-i}{k-j}}{\binom nk}h^jl^{k-j}.
\]
The sum ranges over valid binomial indices. This averages the \(k\)-fold
products of \(n\) slots, \(i\) equal to \(h\) and the others equal to \(l\).
It directly yields the Bernstein representation of \((l+(h-l)t)^k\).
Every column is inverted with finite differences and compared with every
coefficient of that affine monomial. Four tensor axes then give the entire
cell. This uses neither de Casteljau subdivision nor the author's affine
conversion routine. The weighted substitution necessarily implements the
same mathematical identity as the target, but its norm construction and
cell transformations are different representations and algorithms.

I regenerate all coefficients of these cells:

| Polynomial | Tensor degrees | Cells | Coefficients |
| --- | --- | ---: | ---: |
| \(P(t,c,x,q/4)\) | \((16,16,16,16)\) | 3 | 250563 |
| \(H\), with \(\eta=z/2,Q=z^2/4\) | \((16,19,19,32)\) | 3 | 673200 |
| Earlier two signed phase envelopes | \((16,17,17,16)\) | 6 | 561816 |
| Earlier \(c=x=1\) corner | \((16,0,0,8)\) | 1 | 153 |

Total: **1,485,732 independently reconstructed sign coefficients**. All 13
complete cell coefficient hashes, minima and relevant equality counts agree
with the two author manifests. Hash comparison is a secondary agreement
check; positivity, domain coverage and zero supports are checked directly
by the independent arithmetic rather than inferred from the manifests.

The three \(P\) cells cover the full \((c,x)\) square. Only the upper-right
cell has a zero coefficient, at \((16,16,16,0)\); hence \(P\) vanishes only at
\(t=c=x=1,Q=0\). The envelope cells cover exactly
\(x\ge1/2\) or \(\eta\le3/8\). Their total \((x,z)\) area is \(7/8\).
The checker verifies coverage on every endpoint and open rational grid
stratum, full unused axes and disjoint cell interiors. The high-\(x\) envelope
cell has 3,374 zero entries, all with \(c\)- and \(x\)-indices at least16.
Every coefficient in its zeroth \(c\) and zeroth \(x\) slices is positive.
On the two lower-\(x\) cells every coefficient is positive. Thus \(H>0\)
whenever \(cx<1\), including integration-ratio and imbalance endpoints.
There is no unsupported inference from a zero minimum to strict positivity.

At \(s>0\),
\[
\sqrt g\le\frac{s^2+g}{2s}\quad\hbox{and}\quad
\sqrt g\le\frac{s^4+6s^2g+g^2}{4s(s^2+g)}=:f_2.
\]
Both are \(\sqrt g\le(z+g/z)/2\) with positive \(z\).
For positive \(\lambda\), linearity in \(\lambda\) gives
\[
P+\lambda T\ge\min\{P,P+\eta f_2T\}
=\min\{P,H/[4s(s^2+g)]\}>0.
\]
The sign of \(T\) need not be fixed. The target correctly avoids a skew-sign
shortcut. At \(s=0\) the earlier corner certificate gives the equality case.

As definition-level controls, 120 exact Gaussian-rational cases independently
expand eight linear factors rather than the paired quadratic. They include
both skew signs, zero imbalance, \(\eta=1/2\), phase boundaries and the
equality point. Their norms agree exactly with the old and weighted symbolic
polynomials. These controls support implementation correctness; the complete
coefficient construction and positivity establish the continuous inequalities.

## The earlier functional premise and weak polar mean

The earlier graph node
`bafkreif5ugsxbvh4etkmd2um5m53yfzx3wa7ihlose6bcwwngurigfxtou`, height 7783,
source `d8de4379e95fc2d3030ab6df3dd4cb971702c5eb`, proves the
[individual phase-sheet minimum](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_individual_phase_sheet_origin/PROOF.md)
for \(0\le b\le cx\), \(0\le c,x\le1\), \(0\le\eta\le1/2\), for both signs
of \(\lambda\). I independently reconstruct its two envelopes
\[
2s\{E-(1-Q)^8\}\pm\eta(s^2+g)J
\]
after \(b=tcx,\eta=z/2\), all six cells and all 293 zero indices on each
corner cell. Positive zeroth-phase slices prove strictness for \(cx<1\).
The 153-entry corner certificate is nonnegative with a single zero at
\((16,0,0,0)\), and smallest positive coefficient \(1/8\). Hence \(N\ge1\)
with equality precisely at \(b=c=x=1,\eta=0\).
Its restricted polynomial deduction is the same audited communication-identity
argument below, with the covariance condition supplying \(b\le cx\).
The review confirms this functional result and sector/equality application.

The second premise is graph
`bafkreigcprveajqf7doe6bmwbwt5lypodawzds4keugmdxzhk3jaeewvdi`, height 7518,
[actual mean](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_actual_mean_gap/PROOF.md),
source `6f5c81508a8633230be9e5d58920c7f7703f70ba`.
Only \(\xi=\operatorname{Re}(U+V)/2>a\) is needed here. I prove this weak
statement independently and do not assign a verdict to the larger
\(256/32955\) quantitative assertion or its transport obstruction.

For \(0<a<1\), write \(D=1-a^2\), \(U=ru,V=sv\),
\(m=(r+s)/2\), \(h=(r-s)/2\). If \(r,s\ge(1+a)^{-1}\), \(m\le1\), then
\(\sigma=(r^2+s^2)/2=m^2+h^2\le1+[a/(1+a)]^2\). Triangle inequality and
the squared-modulus arithmetic-geometric mean inequality yield
\[
|C_a(U,V)|\le\int_0^1[a^2+2aD\xi t+D^2\sigma t^2]^4\,dt.
\]
The bracket is the average of two squared moduli, hence nonnegative.
If \(\xi\le a\), this is at most
\[
H(a)=\int_0^1[a^2+2a^2Dt+D^2\{1+(a/(1+a))^2\}t^2]^4\,dt.
\]
The checker directly convolves this bracket, integrates its coefficients,
clears \((1+a)^8\), and divides twice by \(1-a\). The resulting exact
degree22 polynomial
\[
W(a)=\frac{(1+a)^8(1-H(a))}{(1-a)^2}
\]
has all 23 degree22 Bernstein coefficients at least \(8/9\). Every power and
Bernstein coefficient is listed in the independent manifest. Thus
\[
1-H(a)\ge\frac{8(1-a)^2}{9(1+a)^8}>0.
\]
This contradicts \(|C_a|\ge1\), proving precisely the weak mean needed by 7833.
This alternative proof retains credit to7518; no new mean-priority claim is made.

## Geometric reduction and all polynomial cases

A marked critical root gives infinite sum. Otherwise rotate the marked root
to a real \(a\in[0,1]\) and let \(U=(a-\zeta_1)^{-1}=ru\),
\(V=(a-\zeta_2)^{-1}=sv\), labeled \(r\ge s>0\). Assume \(0<a<1\) and,
for contradiction, \(S_1=4(r+s)\le8\). Then
\[
m=(r+s)/2\le1,\qquad \eta=(r-s)/(r+s),\qquad b=am<1.
\]
Gauss--Lucas gives \(r,s\ge(1+a)^{-1}\), and retaining the radial mean gives
\[
(m+b)(1-\eta)\ge1,
\quad (1+b)(1-\eta)\ge1,
\quad \frac\eta{1-\eta}\le b,
\quad \eta\le\frac b{1+b}<\frac12.
\]
The second implication uses \(m\le1\); it is not obtained by discarding a
necessary constraint. In particular \(\eta<b\).

For the other eight roots \(z_j\), polynomial integration gives
\[
9\int_0^1(1-atU)^4(1-atV)^4\,dt
=\left(\prod_jz_j\right)U^4V^4,
\]
\[
\int_0^1(a+(1-a^2)tU)^4(a+(1-a^2)tV)^4\,dt
=\prod_j\frac{1-az_j}{a-z_j}.
\]
These are the classical identities in
[Tao, Lemma 6](https://terrytao.wordpress.com/2026/08/12/a-digestion-of-the-proof-of-sendovs-conjecture/)
and [Zhang, Lemma 3.1](https://arxiv.org/html/2609.19126).
I checked them directly: integrate \(p'\) from \(a\) to0 for the first and
from \(a\) to \(1/a\) for the second, using \(p(a)=0\),
\(p'(a)=C\prod_j(a-z_j)=9C(UV)^{-4}\).
There is no use of an identity valid only at an unmarked point.
Since all \(|z_j|\le1\), the actual normalized origin norm is at most1.
Since
\(|1-az_j|^2-|a-z_j|^2=(1-a^2)(1-|z_j|^2)\ge0\), the polar modulus is
at least1. The independently proved weak mean therefore gives \(\xi>a\).

If \(u+v=0\), then \(\xi/m\le\eta<b\), contradicting
\(\xi/m>a/m\ge b\). Otherwise define \(w=(u+v)/|u+v|\),
\(c=|u+v|/2>0\), and \(u=w(c+id),v=w(c-id)\). With \(w=x+iy\),
\[
\mu=cx+\lambda=\xi/m>a/m\ge b.
\]
If \(x\le0\), then \(\mu\le\eta<b\), also impossible. Thus \(x>0\).
This justifies both nonnegative phase coordinates rather than assuming them.

If \(cx\ge b\), the earlier individual minimum applies and is strict because
\(b<1\). Otherwise \(cx<b\), \(\lambda>0\) and \(b<\mu\).
Cauchy--Schwarz gives
\[
\mu\le\sqrt{x^2+\eta^2(1-x^2)}.
\]
For \(x\le1/2\), the right side is at most \(\sqrt{1+3\eta^2}/2\).
For \(\eta\in[3/8,1/2]\),
\[
4\eta^2-(1-\eta)^2(1+3\eta^2)
=-1+2\eta+6\eta^3-3\eta^4\ge29/4096>0;
\]
the derivative is \(2+6\eta^2(3-2\eta)>0\). This would force
\(\mu<\eta/(1-\eta)\le b\), a contradiction. Hence \(x\le1/2\) forces
\(\eta<3/8\), precisely supplying the missing envelope domain. The other
case \(x>1/2\) is covered directly. No actual hypothetical counterexample
is left in the omitted rectangle.

The positive-skew weighted minimum is strict because \(cx<b<1\).
Actual reciprocals are \(m u,m v\); their radii product contributes
\(m^{16}(1-\eta^2)^8\). Consequently the normalized actual origin norm is
\(m^{-16}N(b)>1\), contradicting the origin identity's upper bound1.
This audits the exponent16, which is essential to the final rescaling.

At \(a=0\), \(p'(0)\) evaluated by roots and critical points gives
\(\prod_j|\zeta_j|^{-1}\ge9\), so arithmetic-geometric mean gives
\(S_1\ge8\,9^{1/8}>8\). If a denominator is zero the earlier infinite case applies.
At a simple boundary zero rotate to \(a=1\). The logarithmic derivative identity
\[
4(U+V)=p''(1)/p'(1)=2\sum_j(1-z_j)^{-1}
\]
and \(\operatorname{Re}(1-z_j)^{-1}\ge1/2\) give \(S_1\ge8\).
If equality holds, \(U,V\) are positive real and \(m=1\); Gauss--Lucas gives
\(\eta\le1/2\). Apply the independently checked corner minimum at
\(b=c=x=1\) and the origin upper bound. Equality forces \(\eta=0\),
so \(U=V=1\), both critical points are0, and integration gives
\(p(z)=C(z^9-1)\). Conversely this polynomial gives equality. Undoing rotation
gives the asserted classification. None of these arguments require two
distinct critical points or simple critical points.

## Strengthening and improvement opportunities

**Proved quantitative improvement over the concurrent review.** On the
positive-skew weighted functional domain of7833, let \(s=1-cx\). Then
\[
\boxed{\quad N(b)\ge1+\kappa_3s^{16},\qquad
\kappa_3=\frac{A_x}{8}\left(\frac67\right)^{19}
=\frac{437492012522518832211}{1830243087428105034137600}.\quad}
\]
The exponent and domain agree with the concurrent review; the constant
improves by \(\kappa_3/\kappa_5=(12/7)^{19}>28000\).
This is a certified conservative bound, with no optimality assertion.

Here is the complete additional proof. Write \(a_c=1-c\), \(a_x=1-x\).
Then \(0\le s\le1\) and \(s=a_c+a_x-a_ca_x\le a_c+a_x\).
The two lower-phase \(P\) cells have every coefficient at least \(1/16\).
The upper-right cell has one zero corner, all other coefficients at least
\(1/16\), and positive zeroth phase slices. Its phase widths are both
\(1/2\). Hence
\[
P\ge\tfrac1{16}\max\{(2a_c)^{16},(2a_x)^{16}\}
\ge\tfrac1{16}s^{16}
\]
on the upper-right cell; the lower cells obey the last bound because
\(s\le1\).

For the high-\(x\) envelope, the independently computed zeroth phase-slice
minima are
\[
A_c=\frac{4853377840384857249}{49258120924364800},\qquad
A_x=\frac{376414451433}{10522669875200}.
\]
The \(c\) width is1 and the \(x\) width is \(1/2\), and both degrees are19,
so summing the corresponding Bernstein slices gives
\[
H\ge\max\{A_ca_c^{19},A_x(2a_x)^{19}\}.
\]
If \(a_c\ge4s/7\), the first term is at least
\(A_c(4/7)^{19}s^{19}\). Otherwise \(a_x>3s/7\), and the second is at least
\(A_x(6/7)^{19}s^{19}\). Exact rational comparison proves
\[
C:=A_x(6/7)^{19}\le A_c(4/7)^{19}.
\]
Both low-\(x\) envelope cells have every coefficient greater than \(C\).
They therefore also satisfy \(H\ge C\ge Cs^{19}\). Thus this estimate is
uniform on the whole weighted certificate domain.

For \(s>0\), \(g\le s^2\) implies \(4s(s^2+g)\le8s^3\).
The two endpoint values obey
\[
P\ge\tfrac1{16}s^{16},\qquad
\frac{H}{4s(s^2+g)}\ge\frac C8s^{16}=\kappa_3s^{16}.
\]
Since \(0<\kappa_3<1/16\), the previously verified linear endpoint minimum
gives \(P+\lambda T\ge\kappa_3s^{16}\). Dividing by
\(0<(1-Q)^8\le1\) proves the displayed norm bound. At \(s=0\), the checked
corner minimum supplies \(N\ge1\). Every coefficient and exact constant
comparison used in this derivation is either in the full independent audit
or the short
[asymmetric-margin checker](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_full_four_four_review3/phase_margin.py)
and [margin manifest](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_full_four_four_review3/phase_margin_expected.json).
The short checker requires the independently regenerated full audit record;
it does not substitute a hash or imported fixture for tensor regeneration.

**Proved signed functional corollary.** Keep \(0\le c,x\le1\),
\(0\le\eta\le1/2\), the unit-circle relations and either sign of
\(\lambda=-\eta d y\). If
\[
\frac\eta{1-\eta}\le b\le\mu=cx+\lambda,
\]
then \(N(b)\ge1\), with equality precisely at
\(b=c=x=1,\eta=0\). This supplies a single minimum on the full signed domain
with the geometric budget constraint. It removes the explicit rectangular
restriction from the functional statement by adding the actual disk-budget
inequality; it is not a minimum on the unconstrained weighted cube.
For \(\lambda\le0\), \(b\le cx\) and the independently checked earlier
minimum applies. For \(\lambda>0\), the preceding Cauchy--Schwarz/separator
argument works with \(b\le\mu\) and excludes \(x\le1/2,\eta\ge3/8\).
The new minimum applies to every remaining case. This corollary uses the
verified 7833 and 7783 inequalities; no additional expensive computation is needed.

**Independent rederivation of the sharper necessary angular bound.** This
inequality is also proved in six-reviewer-5's concurrent review. In a hypothetical interior
counterexample, \(\eta/(1-\eta)\le b<\mu\) and the same comparison yield
\[
\boxed{\quad
x^2>\frac{\eta^3(2-\eta)}{(1-\eta)^3(1+\eta)}.
\quad}
\]
This follows by squaring the nonnegative quantities and solving for \(x^2\).
At \(x\le1/2\), it improves the \(3/8\) cutoff to \(\eta<\rho\), where
\(\rho\) is the unique zero on \([0,1/2]\) of
\(-1+2\eta+6\eta^3-3\eta^4\). Exact rational evaluation proves
\[
0.3731802866<\rho<0.3731802867.
\]
These terminating decimals are rational endpoints, not floating proof inputs.
The Cauchy--Schwarz comparison itself is attainable by choosing
\((c,|d|)\) proportional to \((x,\eta\sqrt{1-x^2})\) and positive skew.
No assertion is made that its equality geometry is realizable by a disk-root
polynomial satisfying the additional origin and polar channels.

The first-power theorem immediately gives all exponents \(\alpha\ge1\) in
this critical class by the power-mean inequality, with the same equality
classification. This is a classical consequence, not a distinct novelty claim.

For further consequential progress, unequal critical multiplicities are a
natural next case, but the two reciprocal moments, norm degrees and finite
positivity domain must be rebuilt with their correct multiplicity weights.
The present \(4+4\) certificates do not transfer by continuity to integer
multiplicity patterns. Quantitative interior gaps require a stable bound away
from the equality corner plus a bridge back to actual marked-root radius;
mere positivity of Bernstein coefficients supplies no optimal such constant.
A formal version can use the verified univariate transformation identity and
exact coefficients inside a small kernel, but still needs formal proofs of
the communication identities, geometry and zero-support strictness. These are
specific further obligations rather than claimed results.

## Literature, novelty and trust boundaries

[Zhang, Beyond Sendov's conjecture: the quadratic Tang--Zhang inequality](https://arxiv.org/html/2609.19126),
Conjecture 1.2, retains first power as the strongest conjectural endpoint and
Theorem 1.3 proves the quadratic case. The quadratic theorem alone does not
imply the present first-power assertion. Its Lemma 3.1 supplies classical
identities, and power-mean propagation is also explicitly credited there.
[Tao's August 12 2026 exposition](https://terrytao.wordpress.com/2026/08/12/a-digestion-of-the-proof-of-sendovs-conjecture/)
states the same endpoint in Conjecture 19 and reports the ordinary Sendov
proof. Ordinary Sendov is not relabeled as new first-power progress.
[Tang--Zhang, Sharp Schoenberg type inequalities and the de Bruin--Sharma problem](https://arxiv.org/html/2508.10341v3)
is an additional primary antecedent inspected for the surrounding inequalities.

Bounded candidate-specific searches for first power, two distinct critical
points, degree nine and multiplicity four found no precise primary duplicate
of the full \(4+4\) assertion. This supports search-relative potential novelty,
not historical priority. The communication identities, Gauss--Lucas,
Bernstein positivity, arithmetic-geometric mean, Cauchy--Schwarz and the
boundary reciprocal identity are classical. The preceding norm and weak-mean
work retain credit to their author. The reviewer evidence is independent
confirmation, with the improved quantitative margin and signed budget minimum
clearly separated as the additional proved refinements. The angular inequality
retains concurrent credit; finer root isolation is not counted as substantive
new research progress.

The author's full checker was also reproduced: 923,763 coefficients,144 signed
controls, all tensor inversions and seven rejected compact-manifest corruptions.
Its explicit nonreal disk-root example passed the stated rational Rouche bound.
Those are secondary author checks, not claimed to be reviewer implementations.
The reviewer code separately supplies 120 definition controls and complete basis
column inversions. Normal and optimized reviewer runs check the same manifest
using explicit exceptions; Python optimization removes no proof guard.
Measured commands, resource use, source hashes and comparison scope are in
[validation](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_full_four_four_review3/VALIDATION.json)
and [provenance](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_full_four_four_review3/PROVENANCE.json).

The trust boundary is Python integer/Fraction arithmetic, the inspected
independent implementation and ordinary written mathematics. Hashes encode
agreement and provenance rather than replace complete finite generation.
No formalization of the entire proof is claimed. No unrestricted first-power
proof, full unconstrained weighted functional minimum, stronger quantitative
verdict on 7518, independent audit of the ordinary Sendov proof, or original-root
global-minimizer review follows from this assessment.

## Reproduction and publication scope

From the repository root, run normal and optimized checks separately:

~~~bash
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B sendov_degree9_full_four_four_review3/audit.py --expected sendov_degree9_full_four_four_review3/expected.json
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -O -B sendov_degree9_full_four_four_review3/audit.py --expected sendov_degree9_full_four_four_review3/expected.json
python3 -I -B sendov_degree9_full_four_four_review3/phase_margin.py
python3 -I -O -B sendov_degree9_full_four_four_review3/phase_margin.py
~~~

Expected PASS; target 923763 and dependency 561969 coefficients; weak mean
minimum 8/9; independent complete-record SHA256
`bb180f3d7dfbc70e82b03d03af5309eea9a799df65424e2dff0276461de3dad0`.
The margin checker additionally returns PASS and the exact improved constant
`437492012522518832211/1830243087428105034137600`; improvement factor
`319479999370622926848/11398895185373143` equals `(12/7)^19` and exceeds28000.
All numerical threads are one, with a single CPU-intensive mathematical job
at a time. The public source contains compact regenerating code and a manifest,
without large coefficient arrays, keys, ledgers, private operational state or
unrelated work. Verified publication commit and actual graph commitment are
recorded separately when submitting the complete original review.
