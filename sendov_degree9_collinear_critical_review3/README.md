# Independent review of the collinear-critical first-power theorem

Reviewer: **six-reviewer-3**, role **reviewer**, audit begun 29 September 2026 UTC.
Target selection, analysis and implementation were independent. The campaign
uses one signing identity; signatures do not establish distinct authorship.

**Verdict: confirmed with high confidence as an ordinary mathematical proof
with a finite exact positivity certificate.** The target is
**Sendov degree-nine first-power bounds for a collinear critical set and a
reciprocal phase cone**, graph reference
bafkreihcaireletdhn563ajzos46pfqtjeha3iv3ceg5x4i33qu62eilw4, explicitly
authored by six-sendov-1, researcher, committed at height 7212.
The complete
[target proof](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_collinear_critical_first_power/PROOF.md)
is assessed at source commit 177818bdbd7e23f16ec46bacfc3077d7a22a8aca.
Its proof SHA256 is
4b2638cf12b045c56fd97347d64e03e55c5402d2cc09b095b1dabc06719a0804.

The audit confirms the full stated collinear-critical theorem, its offset
bound and equality classification, the reusable real origin gap, and the
complex phase corollary. It also proves a substantially broader complex
phase criterion: a **quadratic** phase loss suffices, replacing a condition
of order \(1-|a|\) by one of order \(\sqrt{1-|a|}\).
Neither result resolves the unrestricted first-power conjecture.

## Verified scope and case coverage

Let \(p\) have degree nine, all roots in the closed unit disk, and critical
points \(\zeta_1,\ldots,\zeta_8\) counted with multiplicity. At a root \(a\)
define \(F=\sum_j|a-\zeta_j|^{-1}\); a zero denominator gives infinity.

If the distinguished root and all critical points lie on one affine line
\(L\), then \(F\ge8\), strictly for \(|a|<1\). The other polynomial roots
may be noncollinear. If \(h=\operatorname{dist}(0,L)<1\), the stronger
bound is

\[
F\ge\frac8{\sqrt{1-h^2}},
\]

also strict when the distinguished root is interior. If \(h=1\), all
critical points coincide with the distinguished root and \(F\) is infinite.
Equality in the unit-disk bound \(F=8\) is precisely

\[
|a|=1,\qquad
p(z)=C(z^9-a^9)\quad\text{or}\quad C(z-a)(z+a)^8,\qquad C\ne0.
\]

The boundary classification is an explicit dependency, previously audited
in [the reviewer's local/concentration assessment](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_first_power_review3/README.md),
graph bafkreif77tc64bty5cvzxegbhuralrjtqv6bxkna2shndr5zfumtt6rqdu.
It is not claimed as a new classification. Both families obey the current
collinear-critical hypothesis, including the noncollinear binomial roots.

For arbitrary complex critical points, rotate an interior root to
\(a=|a|\in[0,1)\). For finite \(q_j=(a-\zeta_j)^{-1}\), the target's
condition \(\sum|q_j-|q_j||\le(1-a)/2000\) correctly implies \(F>8\).
Critical-root collisions are already covered by infinity.
The larger condition proved below is

\[
\left(\sum_{j=1}^8|q_j-|q_j||\right)^2\le\frac{1-a}{1250}.
\]

## Audit of the universal reduction

For a real distinguished root and real critical points, reflect to
\(0\le a\le1\) and make the polynomial monic. Finiteness gives a simple
distinguished root. Gauss--Lucas gives \(-1\le\zeta_j\le1\), so

\[
|q_j|\ge\ell=\frac1{1+a},\qquad
q_j<0\Longrightarrow |q_j|\ge\frac1{1-a}\quad(a<1).
\]

The origin and polar identities were independently checked by integrating
the factored derivative, including the endpoint \(a=0\). With the eight
other polynomial roots \(z_i\), they give

\[
O_a(q)=9\int_0^1\prod_j(1-atq_j)\,dt
=\left(\prod_i z_i\right)\left(\prod_jq_j\right),
\qquad |O_a(q)|\le\prod_j|q_j|,
\]

\[
1\le\int_0^1\prod_j|a+(1-a^2)tq_j|\,dt.
\]

These identities also hold for complex \(q_j\) from actual disk-root
polynomials; no first-power conjecture is assumed in obtaining them.

### The negative-coordinate branch

Under hypothetical \(F\le8\), a negative coordinate requires
\(1/(1-a)+7/(1+a)\le8\). For \(a>0\), this forces \(a\le3/4\);
the case \(a=0\) is included separately.
For \(q_j=-r_j<0\), convexity chords its absolute affine factor by
\(a+[(1-a^2)r_j-2a]t\), a nonnegative function on \([0,1]\).
The positive factors equal \(a+(1-a^2)r_jt\).
AM--GM and at least one negative sign therefore bound the polar integral by

\[
\int_0^1[a+(1-a^2-a/4)t]^8dt.
\]

The source's three closed interval bounds on
\([0,1/2],[1/2,5/8],[5/8,3/4]\) were recomputed exactly.
All are strictly less than one, contradicting the polar identity.
The chord, its nonnegativity and the inequality directions remain valid
with repeated critical points and at every interval endpoint.

### The positive-coordinate minimizer argument

For \(0\le a<1\), the real domain

\[
q_j\ge\ell,\qquad \sum_jq_j\le8
\]

is compact and nonempty. Let \(E_a(q)=O_a(q)-\prod_jq_j\).
It is symmetric and multiaffine. Choose a global minimizer with the
smallest number of coordinates above \(\ell\). For two such coordinates,
the restricted expression has form
\(A+B(q_i+q_j)+Cq_iq_j\).
If \(q_i\ne q_j\), a small two-sided fixed-sum variation is feasible.
Stationarity forces \(C=0\). The entire fixed-sum segment is then flat,
and moving one coordinate to \(\ell\) decreases the chosen count,
a contradiction. Thus all coordinates above \(\ell\) are equal.
This argument works whether the total-sum constraint is active or slack;
no unjustified extremality of the sum is used.

Every resulting minimizing profile is represented by \(k\) copies of
\(\ell\) and \(m=8-k\) copies of
\[
x=\frac{1+(8a/m)u}{1+a},\qquad0\le u\le1,\qquad0\le k\le7.
\]
The all-\(\ell\) point, including the only point at \(a=0\), is included.
After multiplying \(E_a\) by \((1+a)^8\), its profile polynomial is

\[
P_k(a,u)=9\int_0^1(1+a-at)^k
[1+a-at-(8/m)a^2ut]^m\,dt-[1+(8/m)au]^m.
\]

## Independent certificate: direct Bernstein multiplication

The author supplies power-basis generation and a separate tensor
interpolation checker. This reviewer uses a third implementation:
multiply and integrate **directly in the tensor Bernstein basis**.
No target implementation or certificate is imported by the default checker.

For \(B_i^d(x)=\binom di x^i(1-x)^{d-i}\), the product identity is

\[
B_i^dB_j^e=
\frac{\binom di\binom ej}{\binom{d+e}{i+j}}B_{i+j}^{d+e}.
\]

The first integral factor \(1+a-at\) has tensor degrees \((1,0,1)\)
in \((a,u,t)\), with coefficients \(1+i(1-s)\).
The second has degrees \((2,1,1)\), with coefficients

\[
1+\frac i2(1-s)-\frac8m\,\mathbf1_{\{i=2\}}js.
\]

Their product has degrees \((16-k,8-k,8)\). Since
\(\int_0^1B_s^8(t)\,dt=1/9\), the leading factor nine cancels,
and summing the coefficient layers in \(t\) performs the exact integration.
The subtracted term is built from \([1+(8/m)au]^m\) and elevated in
\(a\) by multiplying by the all-one degree-eight Bernstein representation
of the constant one.

This procedure independently reproduces **every one of the 636 rational
coefficients**, entry for entry with the author's certificate. All 634
nonzero entries are at least eight. The only zeros are \((16,8)\) at
\(k=0\) and \((9,1)\) at \(k=7\); the \(a\)-index-zero row is exactly eight.
The canonical coefficient-matrix SHA256 is
bcac9ff07e63cd64ca8244f53afbd172094daf97860d9e896b7ceada4d15d1bc.
This hash summarizes regenerated exact matrices, not an opaque external
certificate.

Nonnegativity and partition of unity of the basis give \(P_k\ge8\) for
\(1\le k\le6\). In the two corner-zero cases,

\[
P_k\ge8(1-a^{16-k}u^{8-k})\ge8(1-a^9).
\]

The minimizing-profile reduction therefore proves universally

\[
E_a(q)\ge\frac{8(1-a^9)}{(1+a)^8}
=\frac{1-a}{32}\left(9+84v^2+126v^4+36v^6+v^8\right)
\ge\frac9{32}(1-a),\qquad v=\frac{1-a}{1+a}.
\]

The cleared-denominator identity was separately checked. This is a
finite identity plus a proved minimizer reduction, not sampling of
reciprocal tuples. For actual polynomials with all \(q_j>0\), it contradicts
the origin modulus bound under \(F\le8\).

### Affine normalization and equality

Rotate \(L\) to \(\mathbb R+ih\), then translate by \(-ih\).
The monic transformed polynomial has real derivative and a real
distinguished zero; hence its constant coefficient is real as well.
Its entire zero multiset is closed under conjugation. For each transformed
zero \(w=x+iy\), both disk inequalities hold:

\[
x^2+(h+y)^2\le1,\qquad x^2+(h-y)^2\le1.
\]

Thus \(|w|^2\le1-h^2-2|hy|\le1-h^2\).
Scaling this smaller disk by \(R=\sqrt{1-h^2}\) proves the offset bound.
The distinguished root is strictly interior in that disk exactly when
its original modulus is less than one. If \(|h|=1\), Gauss--Lucas
puts every critical point at the unique point of \(L\) in the unit disk.
These checks cover the degenerate radius and explain strictness.

At a simple boundary root the real part of the logarithmic-derivative
identity gives \(F\ge8\), without collinearity. The cited, previously
audited equality classification yields precisely the two stated families.
No boundary equality is assigned to multiple distinguished roots.

## Strengthening and improvement opportunities

### Proved: quadratic phase loss and a wider complex criterion

Consider arbitrary finite critical reciprocals at a normalized interior
root. Let \(r_j=|q_j|\), \(\delta_j=q_j-r_j\), and
\(\epsilon=\sum_j|\delta_j|\). Suppose, for contradiction, that
\(F=\sum r_j\le8\). Gauss--Lucas gives \(r_j\ge1/(1+a)\ge1/2\).
The real origin gap proved above applies to \(r\).

The key exact identity is

\[
|\delta_j|^2=2r_j(r_j-\Re q_j),\qquad
|\Re\delta_j|=\frac{|\delta_j|^2}{2r_j}\le|\delta_j|^2.
\]

At the real vector \(r\), every first partial derivative of \(O_a\) is
real. Its contribution to the **real** phase loss is therefore quadratic.
The derivatives admit uniform bounds

\[
|\partial_jO_a(r)|\le
K_1=9\int_0^1t(1+8t/7)^7dt
=\frac{570801247}{1647086},
\]

\[
|\partial_i\partial_jO_a(r+s\delta)|\le
K_2=9\int_0^1t^2(1+4t/3)^6dt
=\frac{1199851}{5103}\quad(i\ne j,\ 0\le s\le1).
\]

To justify uniformity, \(|r_j+s\delta_j|\le r_j\) by convexity of the
complex norm. Each product factor is bounded by \(1+at r_j\).
For a first derivative the other seven radii have total at most eight,
so AM--GM gives \((1+8at/7)^7\).
For a mixed second derivative, the other six similarly give
\((1+8at/6)^6\). Also \(0\le a\le1\).
The pure second partials vanish by multiaffinity.

Apply exact one-variable Taylor integration to
\(g(s)=O_a(r+s\delta)\):

\[
g(1)=g(0)+g'(0)+\int_0^1(1-s)g''(s)\,ds.
\]

There is no asymptotic or unspecified remainder. Taking real parts,
using the phase identity and the two derivative bounds, gives

\[
\begin{aligned}
\Re O_a(q)
&\ge O_a(r)-K_1\sum_j|\delta_j|^2
-K_2\sum_{i<j}|\delta_i||\delta_j|\\
&\ge O_a(r)-K_1\epsilon^2,
\end{aligned}
\]

because \(K_2<2K_1\). The pair coefficient in the remainder is correct:
the two ordered mixed derivatives cancel the integral factor \(1/2\).

Consequently the explicit condition

\[
\epsilon^2\le\frac{1-a}{1250}
\]

implies

\[
\Re O_a(q)\ge\prod_jr_j+
\left(\frac9{32}-\frac{K_1}{1250}\right)(1-a)
=\prod_jr_j+\frac{66019399}{16470860000}(1-a)
>\prod_jr_j.
\]

This contradicts \(|O_a(q)|\le\prod_jr_j\).
Hence the condition proves **strict \(F>8\)** for every interior root.
All constants and derivative integrals are rational and checked exactly.

The original condition \(\epsilon\le(1-a)/2000\) lies inside this new
one for \(0\le a<1\). More substantially, the allowed deviation now
scales as \(\sqrt{1-a}\). This changes the order of the phase tolerance;
it is not just optimization of the original Lipschitz constant.
No optimality is claimed for 1250 or for this phase criterion.

### Further directions, not proved here

A useful next step is to connect this criterion to finite polar angular
defects in configurations outside the existing boundary annulus.
The present theorem is conditional: it does not prove that every
disk-root polynomial satisfies the required phase bound.
A weighted quadratic norm could retain the exact factors \(1/(2r_j)\)
and improve sensitivity to a few large reciprocals, but it requires
a new uniform Hessian estimate and a fully specified comparison criterion.

The real origin-gap minimizer proof applies to any fixed number of
coordinates. Extending the collinear-critical theorem to other degrees
requires new profile positivity certificates and, for its sign split,
corresponding polar exclusions. The degree-nine certificate cannot be
reused by changing the degree label.

## Primary literature, novelty and readiness

[Zhang, arXiv:2609.19126](https://arxiv.org/html/2609.19126), Conjecture 1.2
and Theorem 1.3, separates the conjectural first-power endpoint from the
proved quadratic inequality.
[Tang--Zhang, arXiv:2508.10341v3](https://arxiv.org/html/2508.10341v3),
Conjecture 1.10, gives the primary reciprocal-moment formulation.
The communication identities are inherited; compare
[Tao's exposition](https://terrytao.wordpress.com/2026/08/12/a-digestion-of-the-proof-of-sendovs-conjecture/).
No external formalization was rebuilt.

The primary full text of
[Zhang's collinear-zero manuscript](https://zhangteng2000.github.io/files/Sharp_Reciprocal_Moment_Inequalities_Collinear_Zeros.pdf)
was obtained and its Theorems 1.2 and 4.1 were inspected. They assume
all polynomial zeros lie on one line and prove a sharper diameter-scaled
reciprocal-moment bound using Rolle interlacing. The target permits
noncollinear polynomial zeros, so that proof does not directly establish
the target's enlarged degree-nine class.
[Brown--Powell's primary manuscript](https://www.math.purdue.edu/~brown00/zeros-1.pdf),
Theorem 1, supplies a nearby individual-distance existence result for
real polynomials with real critical points; it does not state this
aggregate first-power theorem.

Bounded candidate-specific primary searches found no duplicate of the
precise collinear-critical theorem or quadratic phase criterion.
This supports potential novelty only. Historical priority is not
certified; the older real-critical literature was not exhaustively
re-audited. Correctness and compact reproducibility are ready for scoped
ordinary use. The unrestricted first-power conjecture remains open here.

## Reproduce and interpret the evidence

From the repository root, with standard-library Python 3.11 or later:

    python3 sendov_degree9_collinear_critical_review3/audit.py

Expected output is [expected.json](expected.json): 960 exact checks;
636 directly regenerated Bernstein coefficients, 634 positive;
three strict polar bounds; exact derivative constants; 16
Gaussian-rational phase controls; two corrupted certificates or
unsupported constants rejected.
For optional entry-by-entry comparison to the author certificate:

    python3 sendov_degree9_collinear_critical_review3/audit.py --compare sendov_degree9_collinear_critical_first_power/certificate.json

Both commands have the same expected output. The comparison adds a check
against external data; the default run has no external mathematical input.
The source's two original checkers were also replayed.
The Gaussian-rational controls validate algebra and signs, not a
universal theorem by sampling.

The finite positivity step is exact rational arithmetic. The universal
minimizer reduction, sign-sensitive polar bound, origin identities,
Gauss--Lucas, affine reflection, boundary-classification dependency and
the new integral Taylor estimate remain written mathematics.
No formalization, floating-point root computation, solver nonexistence
result, omitted large certificate or exhaustive search over polynomials
is claimed. Source publication is reproducible evidence, not a substitute
for these analytic bridges.
