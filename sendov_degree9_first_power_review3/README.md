# Independent review of the degree-nine first-power boundary annulus

Reviewer: **six-reviewer-3**, role **reviewer**, 29 September 2026. This
assessment and its implementation were selected and produced independently.
The campaign uses a shared signing identity; signatures do not demonstrate
distinct authorship.

**Verdict: confirmed with high confidence as an ordinary mathematical proof.**
The reviewed lemma is
`bafkreibmuqnxpbpmdbukl5vimg7vwjflce6gl5uqchegyvvxitvuddb7zu`,
“Sendov degree-nine first-power bound for clustered critical points and a
boundary annulus,” explicitly attributed to six-sendov-2, researcher.
Its source is
[the local proof](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_clustered_critical_first_power/PROOF.md)
at commit `4387d05063a12f670bfa83e6924bf0e4ba59dbd7`.
The annulus also uses sections 4–7 of
[the polar proof](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_first_power_polar/PROOF.md)
at commit `728857924504f28020dea5de6590ae3458b7bc90`, graph dependency
`bafkreideaathnoyujdk5pmy4d3qmhu45tyevkegmjmtgmwyvoq2b2pjnue`.
Those sections were audited here, including the equality classification,
uniform limit argument and the closed failure hypothesis. The dependency's
separate global numerical lower bound and central-radius certificate were
not audited in this review.

## Exact scope and independent evidence

Let \(p\) have degree nine and all its roots in the closed unit disk. Let

\[
T=\max_{1\le j\le8}|\zeta_j|,\qquad
F(a)=\sum_{j=1}^8|a-\zeta_j|^{-1},
\]

with critical points counted with multiplicity and a zero denominator
giving infinity. The target proves \(T\le1/10000\Rightarrow F(a)\ge8\)
at every root, with equality exactly for

\[
|a|=1,\qquad p(z)=C(z^9-a^9),\quad C\ne0.
\]

Its corollary gives some universal positive boundary-annulus width on which
every interior root has \(F(a)>8\), without an assumption on \(T\).
Neither statement resolves the full first-power conjecture or gives an
explicit annulus width.

The audit checked scalar and rotational normalization, repeated roots,
derivative multiplicities, coefficient integration, the Schur transform
including its closed-disk limit, all inequality directions and constants,
boundary saturation, root continuity and the compactness quantifiers.
It found no gap in this scope. The original local checker and the original
boundary-family checker were replayed from their stated commits.

The independent argument below replaces the local Taylor remainder by a
convergent complex-binomial series. It also obtains concentration directly
from the product of moduli, without the dependency's exponential angular
and variance envelope. Its accompanying checker imports no target code,
data or computed critical roots. It uses exact rational and Gaussian-rational
polynomials: 16 polar-identity controls, 80 direct product-expansion
controls, 30 boundary parity controls and rational bound propagation.
These controls validate algebra; they do not prove universality by sampling.

## A series remainder improves the local range

Make \(p\) monic and rotate \(a\) to \([0,1]\). A multiple distinguished
root already gives infinite \(F\). If \(a<3/4\) and \(T\le1/100\), every
critical distance is less than one, so \(F>8\). On the remaining branch
put

\[
\eta=1-a,\quad S=\sum\zeta_j,\quad s=|S|,\quad
Q=\sum|\zeta_j|^2=X+Y,\quad P_2=\sum\zeta_j^2,
\]

where \(X=\sum(\Re\zeta_j)^2\), \(Y=\sum(\Im\zeta_j)^2\).
Thus \(s\le8T\), \(Q\le8T^2\), and \(\Re P_2=X-Y\).

For \(w=\zeta/a\), the absolutely convergent binomial series gives

\[
\frac1{|a-\zeta|}
=\frac1a(1-w)^{-1/2}(1-\overline w)^{-1/2}.
\]

The coefficients \(h_k={2k\choose k}/4^k\) are positive. The convolution
identity \(\sum_{j=0}^kh_jh_{k-j}=1\) follows for every \(k\) by squaring
the generating function. The product equals the displayed real reciprocal
because the analytic branch takes value one at zero and conjugation
preserves it. After total degree two, the absolute tail is at most

\[
\frac{|\zeta|^3}{a^4(1-|\zeta|/a)}
\le\frac{3200}{999}|\zeta|^3<4|\zeta|^3
\quad(a\ge3/4,\ T\le1/100).
\]

The constant, linear and quadratic terms are respectively

\[
\frac1a,\qquad \frac{\Re\zeta}{a^2},\qquad
\frac{3(\Re\zeta)^2-|\zeta|^2}{2a^3}.
\]

Consequently the target's expansion holds with the stronger error bound

\[
F=\frac8a+\frac{\Re S}{a^2}+\frac{3X-Q}{2a^3}+E,
\qquad |E|\le4TQ. \tag{1}
\]

Suppose \(F\le8\). Since \(a^{-2}<2\) and

\[
\frac1{2a^3}+4T\le\frac{32}{27}+\frac4{100}<4,
\]

equation \(1\) still gives

\[
8\eta\le2s+4Q,\qquad \eta\le s/4+Q/2\le3T. \tag{2}
\]

For completeness, the audited coefficient and Schur portion is recorded
here rather than assumed as a black box. Write

\[
p=z^9+cz^8+bz^7+\sum_{k=1}^6c_kz^k+c_0.
\]

Integration of \(p'=9\prod(z-\zeta_j)\) gives

\[
c=-9S/8,\quad b=9(S^2-P_2)/14,\quad |b|\le s^2+Q.
\]

For \(x_j=|\zeta_j|\le T\), pair counting and

\[
\sum_{i<j}x_ix_j\le7Q/2
\]

give \(e_k(x)\le {8\choose k}(Q/8)T^{k-2}\) for \(2\le k\le8\).
Thus

\[
\sum_{k=1}^6|c_k|
\le\frac{TQ}{8}(84+126T+126T^2+84T^3+36T^4+9T^5)
<13TQ,\qquad |c_1|\le(9/8)QT^6\le2TQ.
\]

Set \(Z=a^8c+a^7b+\sum_{k=1}^6c_ka^k\). Then \(c_0=-a^9-Z\).
Using \(1-a^k\le k\eta\), \(2\), and \(s^2\le8Ts\), one obtains

\[
|Z-(c+b)|\le29Ts+34TQ,\qquad
9\eta|Z|\le33Ts+31TQ.
\]

The respective first-moment coefficients are bounded by

\[
27+168/100<29,\qquad 243/8+216/100<33;
\]

the second bound's energy coefficient is \(27(1+13/100)<31\).
It follows that

\[
|a^9Z-(c+b)|\le62Ts+65TQ.
\]

Disk-root containment gives \(|c_0|\le1\); expanding its square and
discarding the nonpositive term \(-|Z|^2\) yields

\[
1-|c_0|^2\le18\eta+(9/4)\Re S+(9/7)\Re P_2+135Ts+130TQ. \tag{3}
\]

Here \(124+72/7<135\) bounds the contribution of \(S^2\).

The Schur coefficient inequality for a monic degree-\(n\) disk-root
polynomial \(h=z^n+d_{n-1}z^{n-1}+\cdots+d_1z+d_0\) is

\[
|d_{n-1}-d_0\overline{d_1}|\le(n-1)(1-|d_0|^2).
\]

For strictly interior roots, Rouché applies on the unit circle to

\[
h-d_0h^*,\qquad h^*(z)=z^n\overline{h(1/\overline z)}.
\]

The difference has a zero at zero. Divide by \(z\); its leading coefficient
is \(1-|d_0|^2\), its next coefficient is

\[
d_{n-1}-d_0\overline{d_1}.
\]

Vieta bounds the latter by \(n-1\) times the former. Scaling all roots
inward and taking a coefficient limit proves the closed-disk case,
including \(|d_0|=1\). Applying this to \(3\), with lower bound

\[
|c-c_0\overline{c_1}|\ge(9/8)s-2TQ,
\]

gives

\[
\Re S\ge s/16-8\eta-(4/7)\Re P_2-60Ts-58TQ. \tag{4}
\]

The energy rounding is safe since \((8\cdot130+2)/18=521/9<58\).
Finally \(a^{-2}-1\le4\eta\), \(a^{-3}-1\le8\eta\),

\[
|3X-Q|\le2Q
\]

and \(1\)–\(2\) imply

\[
F-8\ge8\eta+\Re S+(3X-Q)/2-12Ts-28TQ.
\]

Substitute \(4\). The \(\eta\) terms cancel, giving

\[
F-8\ge(1/16-72T)s+(3/7)X+(1/14)Y-86TQ
\ge(1/16-72T)s+(1/14-86T)Q. \tag{5}
\]

Both coefficients are positive for \(0\le T<1/1204\), a range contained
in the auxiliary domain \(T\le1/100\). Under \(F\le8\), equation \(5\)
forces \(Q=0\). Thus \(p=z^9-a^9\), \(F=8/a\), and \(a=1\). The converse
and undoing rotation give the same equality classification as the target.
In particular the theorem holds at the closed threshold \(T\le1/1250\),
with margins \(49/10000\) and \(23/8750\). No endpoint claim is made at

\[
T=1/1204.
\]

## Independent concentration check by direct products

Consider normalized monic disk-root polynomials with real simple roots

\[
0<a_k<1,\quad a_k\to1,\quad F_k(a_k)\le8.
\]

Suppress indices. Write \(\delta=1-a\), \(b=1-a^2\),

\[
q_j=(a-\zeta_j)^{-1}=x_j+iy_j,\quad r_j=|q_j|,\quad
\mu=\tfrac18\sum r_j\le1,\quad
D=\mu-\tfrac18\sum x_j\ge0,\quad
v=\tfrac18\sum(r_j-\mu)^2.
\]

Gauss–Lucas gives \(r_j\ge1/(1+a)\). The sum bound therefore gives

\[
r_j\le8-7/(1+a)\le9/2. \tag{6}
\]

The inherited polar identity follows by expressing \(p(1/a)/p'(a)\)
both from the root factorization and from integration of the derivative:

\[
\prod_{j=1}^8\frac{1-az_j}{a-z_j}
=\int_0^1\prod_{j=1}^8(a+btq_j)\,dt.
\]

The \(z_j\) here are the eight other roots, not critical points. Since

\[
|1-az|^2-|a-z|^2=(1-a^2)(1-|z|^2)\ge0,
\]

triangle inequality implies

\[
1\le\int_0^1\prod_j|a+btq_j|\,dt. \tag{7}
\]

Put \(U=\sum x_j\), \(V_x=\sum x_j^2\), \(V_y=\sum y_j^2\).
For fixed \(q\), expansion of each norm gives

\[
|a+btq_j|
=1+(2tx_j-1)\delta+(-tx_j+2t^2y_j^2)\delta^2+O(\delta^3).
\]

The remainder is uniform for \(|q_j|\le9/2\), \(0\le t\le1\),

\[
0\le\delta\le1/100,
\]

because \(|a+btq_j|\ge1-10\delta\ge9/10\) and the relevant third
derivatives are bounded on this compact set. Multiplying eight factors,

\[
\prod_j|a+btq_j|
=1+(2tU-8)\delta
+[2t^2(U^2-V_x+V_y)-15tU+28]\delta^2+O(\delta^3). \tag{8}
\]

Initially the second-order coefficients are just uniformly bounded.
Integrate \(8\) only to first order and use \(7\):

\[
1\le1-8(1-\mu+D)\delta+O(\delta^2).
\]

Both \(1-\mu\) and \(D\) are nonnegative. Thus they are \(O(\delta)\).
Set \(s=(1-\mu)/\delta\) and \(d=D/\delta\); these are bounded
nonnegative parameters, not assumptions on their limits.

Furthermore

\[
V_y=\sum(r_j-x_j)(r_j+x_j)\le2(9/2)\sum(r_j-x_j)=72D=O(\delta),
\]

and \(V_x=8(v+\mu^2)-V_y=8(v+1)+O(\delta)\).
Since \(U=8-8(s+d)\delta\), substituting these relations in \(8\) and
integrating gives

\[
1\le1+[16(1-v)/3-8(s+d)]\delta^2+O(\delta^3).
\]

All remainders remain uniform even though \(q_j,s,d,v\) vary with the
sequence. Dividing by \(\delta^2>0\) proves the same necessary budget as
the original argument:

\[
\limsup\bigl(s+d+2v/3\bigr)\le2/3,\qquad \limsup v\le1. \tag{9}
\]

This derivation does not use the exponential defect inequality or assume
that each critical distance is at least one.

The boundary classification was also checked, rather than inferred from
the already solved original Sendov statement. At a simple root \(a=1\),

\[
\sum q_j=2\sum(1-z_j)^{-1},\qquad
\Re(1-z)^{-1}\ge1/2.
\]

Equality \(F(1)=n-1\) forces other roots onto the unit circle and critical
points onto the real interval \([-1,1)\). Hence \(p\) is real. Put

\[
m=n-1\ge3,\quad u_j=(1-z_j)^{-1}=1/2+it_j,\quad x_j=q_j-1/2\ge0.
\]

The \(t_j\) multiset is symmetric. If

\[
T_0(X)=\prod(X-it_j)=X^m+A X^{m-2}+\cdots,
\]

its parity and the derivative identity

\[
\prod(1+q_jw)=\frac{d}{dw}\left[w\prod(1+u_jw)\right]
\]

give \(e_1(x)=m/2\), \(e_2(x)=3A\),

\[
e_3(x)=(m-2)e_2(x)/6.
\]

When \(e_2=0\), exactly one \(x_j=m/2\), giving

\[
p(z)=(z-1)(z+1)^{n-1}.
\]

Otherwise normalized symmetric means \(E_k=e_k/{m\choose k}\) obey

\[
E_3/E_2=1/2=E_1.
\]

Maclaurin gives \(E_3/E_2\le\sqrt{E_2}\le E_1\), so \(E_2=E_1^2\),
all \(x_j=1/2\), and \(p=z^n-1\). This checks the classification for

\[
n\ge4;
\]

it does not assert it for degree three.

For the degree-nine sequence, \(6\) gives

\[
|p'_k(a_k)|=9/\prod r_j\ge9/(9/2)^8>0.
\]

The compact coefficient limit consequently has a simple root at one.
Critical-root multiset continuity and \(6\) permit reciprocal limits. Since

\[
\mu\to1,
\]

the limit has boundary sum eight. The two classified families have
variance zero and \(7/4\), respectively. Equation \(9\) excludes the latter.
Every coefficient subsequential limit is therefore \(z^9-1\), and
compactness yields convergence of the full normalized sequence and

\[
T_k\to0.
\]

If no universal annulus existed, one could choose interior roots

\[
1-1/k<|a_k|<1,\qquad F_k(a_k)\le8.
\]

Normalization and this concentration force \(T_k\le1/1250\) eventually.
The local theorem then gives strict \(F_k(a_k)>8\), a contradiction.
This proves the claimed existence quantifier but supplies no numerical
annulus width.

## Strengthening and improvement opportunities

1. **Proved refinement:** the same local theorem and equality classification
   hold for every \(T<1/1204\), including the convenient closed range
   \(T\le1/1250\), eight times the original stated threshold. The series
   estimate and the full bound propagation above supply the required bridge.
   These conservative constants are not asserted to be optimal.
2. **Proved method simplification:** direct product expansion establishes
   the necessary concentration budget without exponential defect bounds.
   This reduces the analytic machinery and the number of coarse preliminary
   constants needed for this non-effective corollary.
3. **Consequential unresolved improvement:** an explicit annulus requires
   quantitative stability of the boundary equality classification and a
   numerical estimate relating a finite near-boundary failure to its critical
   radius. Compactness by itself cannot supply that estimate.
4. **Related follow-up, not verified here:** six-sendov-1 subsequently published
   a linear boundary margin in
   `bafkreiap2lza4etruvsviippvatvpi6kolhfpkupte3mimslxcxp5ruogu`, source
   [local boundary coercivity](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_first_power_boundary/PROOF.md)
   at commit `b2b065bea5cb6591ad27bf418efda2461a7f6053`. That stronger claim
   uses additional Schwarz–Pick and cube-root constraints. This review
   validates the earlier local lemma and its concentration dependency;
   it is not a verdict on that subsequent linear margin.

## Literature status and publication readiness

[Zhang, arXiv:2609.19126](https://arxiv.org/html/2609.19126), Conjecture 1.2,
still states the first-power endpoint; Theorem 1.3 and Corollary 1.4 cover
exponents at least two. A lower bound on the second-power sum does not imply
the first-power lower bound. [Tao's 12 August 2026 exposition](https://terrytao.wordpress.com/2026/08/12/a-digestion-of-the-proof-of-sendovs-conjecture/)
reports the all-degree original Sendov proof and supplies the inherited
polar identity in Lemma 6(ii). This review did not rebuild an external
formalization. The classical reciprocal identity is also explicit in
[Tang–Zhang, equation (5.1)](https://arxiv.org/html/2508.10341v3).

The indexed [McCoy 1998 publisher abstract](https://www.tandfonline.com/doi/abs/10.1080/17476939808815077)
concerns the original existence assertion near \(z^n-1\). The direct
publisher request returned HTTP 403, and the full older paper was not
independently obtained. Candidate-specific searches for
the first-power endpoint, near-boundary reciprocal sums and real-critical
unit-circle classifications did not locate a primary duplicate of the
combined lemma. This supports potential novelty only. It does not establish
priority or exclude a stronger older result. No rejection of Meng's older
degree-nine existence proof is inferred from later historical summaries.

Correctness is ready for use as a scoped ordinary lemma, with the exact
concentration dependency disclosed. Historical priority, an explicit annulus
and the intervening root-modulus range remain separate questions. The
subsequent linear-margin result does not replace the need to audit its
concentration foundation.

## Reproduction and trust boundary

From the repository root run:

```sh
python3 sendov_degree9_first_power_review3/audit.py
```

Python 3.11 or later, standard library only; no solver, numerical roots or
external certificate. Expected output is [expected.json](expected.json):
332 exact checks, 16 polar controls, 80 product controls, 30 parity controls,
and rejection of three altered bounds/signs. CPython 3.11.2 ran the checker
in 0.422 seconds with 11,324 KiB peak child RSS, one process and one thread.

The code validates finite algebra and rational estimates. The binomial-series
identity, Rouché, Gauss–Lucas, Maclaurin, uniform Taylor remainders and
compactness arguments are ordinary written mathematics, not formally checked
theorems. No private graph ledger, signing key, imported proof corpus,
floating-point tolerance or exhaustive polynomial sampling is part of the
public evidence. The reviewer reports both the precise verified scope and
these trust boundaries.
