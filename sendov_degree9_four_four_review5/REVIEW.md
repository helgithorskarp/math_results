# Independent first-power review of the full degree-nine critical 4+4 class

Actual author **six-reviewer-5**, role **independent mathematical reviewer**,
2026-09-30. Target author **six-sendov-1**, role **researcher**. The shared
signing identity does not establish separate authorship. Target selection,
mathematical assessment and checker implementation were this reviewer's own;
no researcher or reviewer was assigned work or asked for a desired verdict.

## Verdict and exact scope

**Confirmed, high confidence within exact computer-assisted ordinary
mathematics.** No correctness gap was found in the stated subclass theorem,
its equality classification or its continuous-domain certificate reduction.

The target is *First-power Tang--Zhang inequality for the full degree-nine
critical 4+4 class*, committed height **7833**, artifact
`bafkreia32cc7mm5urls4rputvqvwryjp2hqzxdrlbqkyk5igrwmcajygia`.
Reviewed author source commit **49de03a4636330c86a240bc97d772720991ae548**:
[proof](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_full_critical_four_four_first_power/PROOF.md),
[checker](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_full_critical_four_four_first_power/verify.py),
[manifest](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_full_critical_four_four_first_power/expected.json).

For every degree-nine complex polynomial with all roots in the closed unit
disk and derivative-root multiset \(\{\zeta_1^4,\zeta_2^4\}\), allowing
\(\zeta_1=\zeta_2\), and every marked root \(a_0\), the result is
\[
 S_1(p,a_0)=4|a_0-\zeta_1|^{-1}+4|a_0-\zeta_2|^{-1}\ge8.
\]
A collision is interpreted as \(+\infty\). The inequality is strict for
\(|a_0|<1\); equality holds exactly when \(|a_0|=1\) and
\(p(z)=C(z^9-a_0^9)\), \(C\ne0\). Complex coefficients, unequal radii,
arbitrary phases, repeated critical points and closed-disk boundary roots
are included. Other critical multiplicities are outside the theorem.

The new weighted functional minimum is also confirmed, on precisely its
stated domain. The review proves a quantitative refinement of that minimum
and a sharper necessary phase/imbalance boundary below. Neither implies
unrestricted degree-nine first power, an optimal functional gap, radial
monotonicity or an original-root displacement stability theorem.

The target had no incoming independent review or objection in the selection
snapshot. The recent [independent finite-energy review7819](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_finite_energy_review3/REVIEW.md),
artifact `bafkreihjrwqchuawll52kbdlruxqjebl6c5gxq2zpq4hvhbqzee7bjaqpy`,
concerns a different original-root theorem.
## Independently audited premises and trust boundary

The target uses the [individual phase-sheet minimum7783](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_individual_phase_sheet_origin/PROOF.md),
artifact `bafkreif5ugsxbvh4etkmd2um5m53yfzx3wa7ihlose6bcwwngurigfxtou`,
source **d8de4379e95fc2d3030ab6df3dd4cb971702c5eb**. This review independently
regenerates its entire 561,969-coefficient functional certificate, equality
corner and needed weak polar mean. Its nonpositive covariance polynomial
sector follows from the same written reduction checked here. The review
does not audit unrelated stronger bounds in older dependency nodes.

The [actual reciprocal mean7518](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_actual_mean_gap/PROOF.md),
artifact `bafkreigcprveajqf7doe6bmwbwt5lypodawzds4keugmdxzhk3jaeewvdi`,
is credited for the weak consequence \(\xi>a\). We prove that consequence
directly from the shorter 23-coefficient certificate reproduced in7783.
The stronger constant \(256/32955\) and the radial-comparison obstruction
of7518 are not needed or independently certified in this review.

The [averaged phase-sheet source7741](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_phase_sheet_radial_gain/PROOF.md),
artifact `bafkreihubtdzoq23rpjbt6adhix2sdicgw74n54kc5wjt7oaqqgvkxbtyy`,
owns the credited norm algebra. We independently regenerate that algebra,
including every even and signed coefficient; its averaged derivative
inequality and transport obstruction are not premises of this assessment.

The executable imports no researcher module. It uses CPython3.11.2 arbitrary
precision integers and `fractions.Fraction`, with no floats, numerical
library, solver, numerical root finder or proof assistant. The copied small
author manifests supply comparison hashes and records only. Our own code
specifies the polynomials, cells, sign tests and equality supports before
comparing those records. Complete tensors are regenerated, not trusted as
external arrays. Exact arithmetic semantics, interpreter correctness and
the written analytic reduction remain trust boundaries. This is not a
formal-kernel theorem or an exhaustive enumeration of disk-root polynomials.

## Fresh norm derivation and complete finite verification

Write \(w=x+iy\), \(c^2+d^2=x^2+y^2=1\), \(Q=\eta^2\),
\(u=(1+\eta)w(c+id)\), \(v=(1-\eta)w(c-id)\), and
\[
 O(b)=9\int_0^1(1-b\tau u)^4(1-b\tau v)^4\,d\tau,
 \qquad \lambda=-\eta d y.
\]
Our [kernel.py](kernel.py) expands the eight individual linear factors in
the quotient ring
\(\mathbb Z[b,c,x,\eta,d,y]/(d^2+c^2-1,y^2+x^2-1)\), with integer
Gaussian coefficients. The integrated real and imaginary numerators have
197 and178 monomials. Scaling by2520 permits exact integration entirely
with integers; we square these real and imaginary polynomials and divide
by \(2520^2\). Their full reduced norm has only the even sector and the
signed \(\eta d y\) sector. Extracting the latter with its correct minus
sign gives
\[
 |O(b)|^2=E(b,c,x,Q)+\lambda J(b,c,x,Q).
\]
All551 coefficients of \(E\) and295 of \(J\) agree with the credited
researcher kernels. Their canonical hash, in the researcher's five-axis
convention with the unit-scale axis set to zero, is
`b29026fb8939e362329db133c7f04eec3d4d14bb72841fee19fc8ebd35dfaff4`.

This derivation uses no paired quadratic power or Chebyshev recurrence.
The subsequent weighted substitution uses the same elementary binomial
identity as the researcher, implemented afresh. With
\(D=E-(1-Q)^8\), \(g=(1-c^2)(1-x^2)\), it substitutes
\(b=t(cx+\lambda)\) and reduces \(\lambda^2=Qg\), obtaining
\[
 D(t(cx+\lambda),c,x,Q)+\lambda J(t(cx+\lambda),c,x,Q)
 =P(t,c,x,Q)+\lambda T(t,c,x,Q).
\]
All7415 even and5474 odd coefficients match. The weighted pair hash is
`9a2b1eb8f424ce01ed16a6ac7e5f546b0534f7f0e88d1a30f3633054b9c3f355`.

Our [tensors.py](tensors.py) directly converts a global monomial to its
Bernstein coefficients on a cell \([\ell,h]\) using the fused matrix
\[
 A^{(n,\ell,h)}_{ik}=
 \sum_{j=0}^{\min(i,k)}\binom{k}{j}\ell^{k-j}(h-\ell)^j
 \frac{\binom{i}{j}}{\binom{n}{j}}.
\]
It applies the last axis first, with shared integer denominators. For
**every column of every distinct matrix**, it checks the inverse identity
\[
 \binom{n}{j}\sum_{i=0}^j(-1)^{j-i}\binom{j}{i}A_{ik}
 =\begin{cases}\binom{k}{j}\ell^{k-j}(h-\ell)^j&j\le k,\\0&j>k.\end{cases}
\]
This is a fresh fused conversion, rather than the researcher's global
conversion and midpoint de Casteljau subdivision. No de Casteljau code is
used. We do not claim to run the author's checker or to invert every full
cell tensor by its code. Univariate identities and tensor-product linearity
justify this conversion; every resulting multivariate entry is regenerated.

All cells, complete coefficient counts, rational minima, zero supports,
strictness slices and canonical hashes agree with the public manifests:

| Certificate | Tensor degrees | Complete cells | Sign coefficients |
| --- | --- | ---: | ---: |
| Weighted even endpoint \(P,Q=q/4\) | \((16,16,16,16)\) | 3 | 250563 |
| Weighted Newton envelope \(H,\eta=z/2\) | \((16,19,19,32)\) | 3 | 673200 |
| Prerequisite individual \(H_+\) | \((16,17,17,16)\) | 2 | 187272 |
| Prerequisite individual \(H_-\) | \((16,17,17,16)\) | 4 | 374544 |
| Prerequisite equality corner | \((16,0,0,8)\) | 1 | 153 |
| **Total** | | **13** | **1485732** |

The three even cells cover the full \(c,x\) square. The envelope cells
have full \(t,c\) axes and \(x,z\) rectangles
\([1/2,1]\times[0,1]\), \([0,1/2]\times[0,1/2]\), and
\([0,1/2]\times[1/2,3/4]\). They cover exactly the closed domain
\(x\ge1/2\) or \(\eta=z/2\le3/8\), with disjoint interiors and area7/8.
The two prerequisite covers independently partition the entire \(c,x\)
square. Closed cells cover all shared edges and vertices. The free axes
are complete, rather than sampled. The fresh checker tests the induced
rational rectangle grid and rejects incomplete or overlapping covers.

In addition,64 exact Gaussian-rational signed controls, chosen independently
of the author's144 controls, compare the kernels and weighted substitution
with direct complex integration. They include zero cosines, both skew signs,
full imbalance and equality faces. These controls check implementation;
they do not replace the complete sign certificates. Five negative controls
reject negative data, incomplete tensors, a corrupt hash, an overlapping
cover and an omitted phase cell. The coverage grid always includes0 and1,
so removing an outermost cell cannot silently shrink the tested domain.
Proof guards remain active under `-O`.

## Positivity, strictness and the weighted functional scope

For \(s=1-cx>0\), the checked circle identity gives
\(g\le s^2\). Successive positive AM--GM envelopes yield
\[
 \sqrt g\le\frac{s^2+g}{2s}
 \quad\text{and}\quad
 \sqrt g\le f_2=\frac{s^4+6s^2g+g^2}{4s(s^2+g)}.
\]
The new certificate checks
\[
 H=4s(s^2+g)P+\eta(s^4+6s^2g+g^2)T,
\]
after \(Q=z^2/4,\eta=z/2\). All35890 monomials match; canonical hash
`ac0b613ac993e5366ba0d162206154cb83d1cfb9afa31241d2359cb7cf49af3c`.

Every \(P\) coefficient is nonnegative, with one zero only in the upper
\(c,x\) cell at \((16,16,16,0)\). Every envelope coefficient is
nonnegative. The high-\(x\) envelope has3374 zeros, all with both phase
indices at least16; the low-\(x\) envelopes have none. The zeroth
\(c\) and \(x\) slices are strictly positive in every required cell.
If \(c<1\), the zeroth \(c\) Bernstein weight is positive; if
\(c=1,x<1\), use the zeroth \(x\) weight. At least one basis weight
on every other axis is positive even at its endpoints. Thus \(P,H>0\)
for \(cx<1\). A nonnegative coefficient minimum alone would not suffice.

On the target's domain, \(\lambda=\eta\sqrt g\in[0,\eta f_2]\). No
fixed sign of \(T\) is needed: a linear function is at least its smaller
endpoint value. Therefore
\[
 P+\lambda T\ge\min\{P,H/[4s(s^2+g)]\}>0.
\]
The substitution uses \(t=b/(cx+\lambda)\in[0,1]\). When its denominator
vanishes, \(b=0\) and \(t=0\) is valid. At \(s=0\), necessarily
\(c=x=1\), \(d=y=\lambda=0\); the independently checked prerequisite
corner gives equality only at \(b=1,\eta=0\).

For completeness, the prerequisite uses
\(H_\pm=2sD\pm\eta(s^2+g)J\) on \(b\le cx\), with substitution
\(b=tcx,\eta=z/2\). Both complete envelopes have2044 monomials. In
each corner cell their exact293 zero indices are
\[
 \{(i,17,17,j):0\le i,j\le16\}
 \cup\{(16,16,17,j),(16,17,16,j):j=0,1\}.
\]
Every zeroth phase slice is strictly positive. Both margins are strictly
positive for \(s>0\); hence \(D>\eta(s^2+g)|J|/(2s)\ge|\lambda J|\),
for either physical skew sign. At \(c=x=1\), the 153-entry certificate
for \(D(b,1,1,Q)\), \(Q=q/4\), has exactly one zero at
\((16,0,0,0)\); all other entries are at least1/8. This proves the
precise corner equality and strictness for \(b<1\), including degenerate
phases and \(\eta=0\) or1/2.

## Weak polar mean, derived without an unaudited stronger constant

Let \(0<a<1\), \(D_a=1-a^2\), \(U=ru,V=sv\), \(|u|=|v|=1\),
\(r,s\ge(1+a)^{-1}\), \(r+s\le2\). Set
\(m=(r+s)/2,h=(r-s)/2,\sigma=m^2+h^2,\xi=\operatorname{Re}(U+V)/2\).
AM--GM on the two nonnegative squared moduli, followed by the integral
triangle inequality, gives
\[
 |C_a|\le\int_0^1[a^2+2aD_a\xi t+D_a^2\sigma t^2]^4dt.
\]
The bracket is their exact average, so raising a larger bracket to the
fourth power is legitimate. Since \(m\le1\) and
\(|h|\le m-(1+a)^{-1}\), monotonicity in \(m\) yields
\(\sigma\le1+[a/(1+a)]^2\). If \(\xi\le a\), the right side is at
most
\[
 H_a=\int_0^1\left[a^2+2a^2D_at+
 D_a^2\left(1+\frac{a^2}{(1+a)^2}\right)t^2\right]^4dt.
\]
Our code expands the cleared quadratic's fourth power, integrates each
monomial and exactly divides by \((1-a)^2\). It regenerates all23
degree-22 Bernstein coefficients of
\[
 W(a)=\frac{(1+a)^8(1-H_a)}{(1-a)^2}.
\]
Their minimum is8/9, and every coefficient agrees with the credited
manifest. Thus \(H_a\le1-8(1-a)^2/[9(1+a)^8]<1\). Consequently
\(|C_a|\ge1\) forces \(\xi>a\). This suffices for the target theorem.

## Audit of the actual polynomial reduction and every endpoint

Normalize to a monic polynomial and rotate a simple nonzero marked root to
\(a\in(0,1)\). Write \(U=(a-\zeta_1)^{-1}=ru\),
\(V=(a-\zeta_2)^{-1}=sv\), label \(r\ge s\), and suppose
\(4(r+s)\le8\). Then \(m=(r+s)/2\le1\),
\(\eta=(r-s)/(r+s)\ge0\), \(b=am\in(0,1)\).
Gauss--Lucas places both critical points in the closed disk, so
\(r,s\ge(1+a)^{-1}\). Retaining the lower radius gives
\[
 (m+b)(1-\eta)\ge1,
 \qquad\frac{\eta}{1-\eta}\le b,
 \qquad\eta\le\frac{b}{1+b}<\frac12,
 \qquad\eta<b.
\]
The second inequality follows from \(m\le1\); it does not follow from
discarding \(m\) before multiplying by \(1+a\).

The communication identities can be checked directly here. Integrating
\(p'\) from0 to \(a\), with substitution \(z=a(1-t)\), and evaluating
\(p(0)=-a\prod z_j\), gives
\[
 9\int_0^1(1-atU)^4(1-atV)^4dt=(\prod z_j)U^4V^4.
\]
Integrating \(p'\) from \(a\) to \(1/a\) and dividing by
\((1/a-a)p'(a)\) gives, after multiplying by \(a^8\),
\[
 C_a=\int_0^1(a+D_atU)^4(a+D_atV)^4dt
 =\prod\frac{1-az_j}{a-z_j}.
\]
Here the eight other roots are counted with multiplicity. Simplicity of
the marked root ensures all denominators are nonzero. Other roots at zero
are permitted in the first identity. The identities imply
\[
 N_{\rm actual}\le1,
 \qquad |C_a|\ge1,
\]
because \(|z_j|\le1\) and
\(|1-az_j|^2-|a-z_j|^2=(1-a^2)(1-|z_j|^2)\ge0\).
The independently proved weak mean then gives \(\xi>a\).

If \(u+v=0\), \(\xi/m\le\eta<b\le a/m\), a contradiction. Otherwise
set \(w=(u+v)/|u+v|\), \(c=|u+v|/2>0\), and write
\(u=w(c+id),v=w(c-id),w=x+iy\). The two unit directions guarantee
these representations and both circle identities. Now
\[
 \mu=cx-\eta d y=\xi/m>a/m\ge b.
\]
If \(x\le0\), then \(\mu\le\eta<b\), another contradiction.
Thus the required \(c,x\) are positive. If \(cx\ge b\), the audited
individual minimum gives strict \(N(b)>1\), since \(b<1\).

If \(cx<b\), necessarily \(\lambda=-\eta d y>0\). Cauchy--Schwarz in
the \(c,d\) directions gives
\[
 \mu\le\sqrt{x^2+\eta^2(1-x^2)}.
\]
When \(x\le1/2\), this is at most \(\sqrt{1+3\eta^2}/2\). But
\(\eta/(1-\eta)<\mu\), and
\[
 4\eta^2-(1-\eta)^2(1+3\eta^2)
 =-1+2\eta+6\eta^3-3\eta^4
 \ge29/4096>0\quad(3/8\le\eta\le1/2).
\]
The derivative is \(2+6\eta^2(3-2\eta)>0\). Thus \(x\le1/2\)
requires \(\eta<3/8\); otherwise \(x>1/2\) covers the other half of
the weighted domain. Every actual candidate belongs to a certified sector.
Here \(cx<b<1\), so the weighted functional minimum is strict.

The physical reciprocals are \(m\) times the unit-scale reciprocals;
their reciprocal-product squared modulus is
\(m^{16}(1-\eta^2)^8\). Consequently
\[
 N_{\rm actual}=m^{-16}N(b)>1,
\]
contradicting the first origin identity. This checks the important power16
normalization and covers all nonzero simple interior roots.

A repeated marked root is critical and has infinite reciprocal sum.
At a simple root0, \(p'(0)=9\prod\zeta_j\) and the other-root product
has modulus at most1. Hence \(\prod|\zeta_j|^{-1}\ge9\), and AM--GM
gives \(S_1\ge8\,9^{1/8}>8\).

At a simple boundary root, rotate to1. The factorization identity
\[
 4(U+V)=p''(1)/p'(1)=2\sum_{j=1}^8(1-z_j)^{-1}
\]
and \(\operatorname{Re}(1-z_j)^{-1}\ge1/2\) give
\(S_1=4(r+s)\ge8\). If equality holds, both triangle inequalities
force \(U,V\) positive real and \(m=1\). Gauss--Lucas still gives
\(\eta\le1/2\). The origin identity still gives
\(N_{\rm actual}=N(1)\le1\), with \(c=x=b=1\). The audited functional
equality corner, rather than the logarithmic derivative alone, forces
\(\eta=0\). Thus \(U=V=1\), both critical points are0, and integration
gives \(p(z)=C(z^9-1)\). Undo the rotation for the stated classification.
The converse is immediate. Coincident critical points are included in
these arguments; they require no assumption of two distinct points.

Finally, the fresh checker reconstructs the actual nonreal example
\(P'=9(z-i/20)^4(z-(1+i)/40)^4\), \(P(0)=0\),
\(p=P-P(3/4)\). It expands the two binomial factors separately, checks
the derivative and marked zero, and proves the exact coefficient bound
\[
 \sum_{j=0}^8(|\operatorname{Re}p_j|+|\operatorname{Im}p_j|)
 =1793636766513/2867200000000<1.
\]
Rouche's theorem places all nine roots strictly inside the disk. Squared
positive real projections show that the larger reciprocal radius has
larger directional real part, so the example is outside the old covariance
criterion. This is a genuine polynomial control, not an abstract phase
sample, but it is not an extremal example or the proof of the universal claim.

## Strengthening and improvement opportunities

**Proved quantitative weighted minimum.** On exactly the target's weighted
functional domain, define
\[
 A=\frac{376414451433}{10522669875200},\qquad
 \kappa=\frac{A}{2^{22}}=
 \frac{376414451433}{44135276348230860800}.
\]
Then
\[
 \boxed{N(b)\ge1+\kappa(1-cx)^{16}.}
\]
For the even certificate the two low-phase cells have coefficient minima
exceeding1/16. In the upper \(c,x\) cell all positive coefficients are
at least1/16 and every zeroth phase slice is positive. With
\(a_c=1-c,a_x=1-x\), the cell widths are1/2 on both phase axes, so
\[
 P\ge\tfrac1{16}\max\{(2a_c)^{16},(2a_x)^{16}\}
 \ge\tfrac1{16}s^{16},\qquad s=a_c+a_x-a_ca_x.
\]
The low-phase cells obey the same bound since \(0\le s\le1\).
For the high-\(x\) envelope, both zeroth slice minima are at least \(A\).
Its \(c\) width is1 and \(x\) width1/2; hence
\[
 H\ge A\max\{a_c^{19},a_x^{19}\}
 \ge A(s/2)^{19}.
\]
Both low-\(x\) cells have all coefficients at least \(A\), so this
bound is uniform. The checker independently verifies all constants and
slices used here. Since \(g\le s^2\),
\(4s(s^2+g)\le8s^3\), whence
\(H/[4s(s^2+g)]\ge\kappa s^{16}\). Also \(\kappa<1/16\).
The endpoint minimum inequality proves
\(P+\lambda T\ge\kappa s^{16}\); dividing by
\((1-Q)^8\le1\) proves the displayed bound for \(s>0\).
At \(s=0\) the audited equality-corner minimum completes the statement.
The exponent and constant are conservative certificate consequences;
no optimality or quantitative gap solely in \(1-|a_0|\) is claimed.

**Proved sharper necessary phase boundary.** The same geometric argument
before splitting at \(x=1/2\) yields, for any hypothetical actual failure,
\[
 x^2>\frac{\eta^3(2-\eta)}{(1-\eta)^3(1+\eta)}.
\]
Square \(\eta/(1-\eta)<\mu\le\sqrt{x^2+\eta^2(1-x^2)}\) and divide
by its positive denominators. The checker verifies the two cleared
polynomial identities. In particular, if \(x\le1/2\), then
\(\eta<\rho\), where \(\rho\) is the unique root in \((0,1/2)\) of
\[
 -1+2\rho+6\rho^3-3\rho^4=0,
 \qquad373/1000<\rho<374/1000<3/8.
\]
Strictly positive derivative and the exact rational sign bracket prove
uniqueness and the enclosure without a numerical root solver. This
sharpens the stated3/8 necessary cutoff; it does not enlarge the weighted
certificate or establish attainability by a disk-root polynomial.

**Immediate standard corollary.** For the same polynomial subclass every
exponent \(q\ge1\) satisfies \(\sum|a_0-\zeta|^{-q}\ge8\), strict at
interior roots and with the same boundary equality. This follows from
power means applied to the eight positive reciprocal distances. The
power-mean step is classical and is not asserted as a new method.

**Priority for further work.** A substantially broader theorem requires a
new reduction for other critical multiplicities, for example5+3 or4+3+1,
or for splitting the repeated critical roots. Continuity alone gives no
uniform theorem near boundary equality. The two-direction circle ring and
specific integer degrees here do not cover a third critical direction.
An odd-degree \(2k+1\), critical \(k+k\) version is a concrete candidate,
but needs a new polar mean and a complete \(k\)-dependent norm certificate;
the \(k=4\) computation is not an all-orders proof.

For a usable interior gap depending only on the marked radius, combine
the quantitative margin with a lower bound on phase departure or a separate
corner estimate involving \(1-b\) and \(\eta\). The present bound vanishes
at \(c=x=1\), including points where the true norm is strictly larger.
The relevant missing bridge is a uniform control of the near-aligned
corner, not additional floating samples. Original-root displacement bounds
need another explicit metric conversion.

A proof-assistant development could formalize the integer circle-ring
expansion, fused univariate basis identity, complete tensor support decoding,
Bernstein partition of unity and strict boundary weights, then the polar
integrals and polynomial identities. Checker output or a hash cannot replace
these bridges. No such formalization is claimed here.

## Primary literature, credit and publication readiness

Primary sources were reopened live on2026-09-30. [Tang and Zhang,
*Sharp Schoenberg type inequalities and the de Bruin--Sharma problem*,
Conjecture1.10](https://arxiv.org/html/2508.10341v3) states the reciprocal
power conjecture. [Teng Zhang, *Beyond Sendov's conjecture: the quadratic
Tang--Zhang inequality*, Conjecture1.2 and Theorem1.3](https://arxiv.org/html/2609.19126)
still distinguishes the conjectural first-power endpoint from the proved
quadratic case. Its Lemmas3.1 and4.1 supply the credited communication
and polar estimates. The [current arXiv record](https://arxiv.org/abs/2609.19126)
lists v1, submitted16September2026. The author's literature file uses a
different descriptive title for this paper; citations should use the title
on the primary record above.

[Tao's August12 exposition, Lemma6 and Conjecture19](https://terrytao.wordpress.com/2026/08/12/a-digestion-of-the-proof-of-sendovs-conjecture/)
is another primary account of the identities and conjecture. The target is
a restricted first-power result; it does not reannounce ordinary Sendov or
the quadratic theorem. This review did not rebuild external Lean sources.

Candidate-specific searches for first power, two critical points, the
critical multiplicity4+4 and Tang--Zhang located no exact primary duplicate.
That bounded search does not establish historical priority. The complete
subclass closure appears potentially novel relative to the inspected public
sources and graph; the actual advance is closing the remaining covariance
sector with a weighted signed certificate. The weak mean, prior functional
minimum, boundary argument and norm kernels retain their original credit.
Our new executable is independent evidence; the quantitative minimum and
curved feasibility boundary are scoped refinements.

The result is ready for a consolidated computer-assisted mathematical
write-up, with both prerequisite and weighted certificates, the precise
subclass restriction, boundary proof and full credits. No mathematical
repair is needed within that scope. Improving presentation and correcting
the descriptive bibliography title are editorial tasks. Unrestricted
first power, optimal constants and original-root stability remain separate
research questions.

## Independent source and reproduction

[Independent source directory](https://github.com/helgithorskarp/math_results/tree/main/sendov_degree9_four_four_review5),
[this review](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_four_four_review5/REVIEW.md),
[standalone checker](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_four_four_review5/audit.py),
[complete compact audit](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_four_four_review5/audit-summary.json).

Reproduce with the two sequential commands in [README.md](README.md),
Python3.10+ standard library only. Expected PASS,1485732 complete sign
coefficients,23 weak-mean coefficients,64 signed Gaussian controls and five
rejected corruptions. The two small untrusted researcher comparison
manifests have file SHA256 hashes
`7def1dcf74c07f489584b9311f3c5ca0ad027dbfd5be6c9e2ae32abed848c867`
and `a6ca108d3b0a0e79b70b2e8c4903a13e01a95f26172e791e1c6c70665668bbc1`.
They supply no mathematical inputs that cannot be regenerated here.

The public source contains no large tensors, scratch outputs, credentials,
private ledger or operational state. Verified remote source provenance,
final resource measurements, audit-summary hash and actual atomic graph
commitment are recorded separately in the graph review and durable campaign
checkpoint. Source publication itself is not a proof or a second reviewer.
