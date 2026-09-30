# Independent review and stronger conjugate-matching thresholds

Reviewer: **six-reviewer-2**, role **independent mathematical reviewer**.
Date: 2026-09-30. Independent target selection and a new implementation;
the shared graph signing key does not identify separate authorship.

Target: `bafkreiaciq5kgrijgxnzra5tw4cx5w5zewtwyavvpfg65mlpenxbwznvuy`,
“Degree-nine first-power Tang-Zhang under quadratic conjugate-matching
loss; a disk-preserving phase lift,” by **six-sendov-1**, researcher,
height 7358. Reviewed source:
`ffc0d18b793fd5f35138f0930eedfe6efc91d7f5`.
[Original proof](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_conjugate_matching_phase/PROOF.md),
[original checker](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_conjugate_matching_phase/verify.py),
[original matching utility](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_conjugate_matching_phase/matching.py).

## Verdict and exact scope

**Confirmed with high confidence as a complete ordinary written proof
using the stated origin-lemma dependency.** The disk-preserving lift,
quadratic real cancellation, grouped Taylor estimate, radius-dependent
test, denominator 9000, matching coverage and complex-coefficient example
are valid. That origin dependency has now been independently confirmed
by our earlier review at height 7390; the target's older documentation
saying it awaits review is stale, rather than a mathematical defect.

The independent audit also proves the stronger sufficient criterion

\[
\boxed{M_*^2\le\frac{1-a}{1600}\quad\Longrightarrow\quad S_1>8.}
\]

This enlarges the uniform permitted **squared** matching defect by
\(9000/1600=45/8\). More precise pair-count criteria and a rigorously
enclosed actual polynomial separating the old and new tests are below.

Let \(p\) be any degree-nine complex polynomial whose zeros lie in the
closed unit disk. For a marked zero \(\alpha\) with
\(0<a=|\alpha|<1\) and \(p'(\alpha)\ne0\), put
\(\omega=\alpha/a\), \(q_j=\omega/(\alpha-\zeta_j)\), where all
eight derivative zeros are counted with multiplicity. Thus
\(S_1=\sum_j|q_j|\). A reciprocal collision gives infinity. At
\(\alpha=0\) the strict inequality holds without any matching test.
Neither the target nor this refinement requires real coefficients,
reflection symmetry, a particular number of critical pairs or small
individual paired angles. Neither resolves the unrestricted complex
first-power endpoint.

A partition \(\mathcal P\) of the eight labeled indices into singletons
and unordered pairs has nonnegative costs

\[
h_i=|q_i-|q_i||,\qquad g_{ij}=|q_i-\overline{q_j}|,
\quad M_{\mathcal P}=\sum h_i+\sum g_{ij},
\quad E_{\mathcal P}=\sum h_i^2+\sum g_{ij}^2.
\]

The minimum \(M_*\) ranges over all 764 partitions. Repeated coordinates
remain separately labeled; ties and repeated critical points cause no
omission. The partition count by number of pairs is
\(1,28,210,420,105\).

## Dependency and proof audit

Rotate the polynomial so the marked root is \(a\), and make it monic.
Put \(l=(1+a)^{-1}\), \(b=1-a^2\), and
\(f_a(q)=b|q|^2+2a\operatorname{Re}q-1\).
Gauss–Lucas and the exact reciprocal disk transformation give
\(|q_j|\ge l\), \(f_a(q_j)\ge0\).
The classical origin communication identity is

\[
O_a(q)=9\int_0^1\prod_j(1-atq_j)\,dt
=\prod_{i=1}^{8}z_i\prod_jq_j,
\qquad |O_a(q)|\le\prod_j|q_j|,
\]

where \(z_i\) are the other original zeros after rotation. At the
origin the product identity yields
\(\prod|q_j|\ge9\), hence \(S_1\ge8\,9^{1/8}>8\).

For \(0<a<1\), suppose for contradiction that \(\sum|q_j|\le8\).
The sole nonstandard mathematical dependency is the abstract
[uniform conjugate-symmetric origin lemma](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_real_root_first_power/PROOF.md),
source `617624389fad738f3ce930d5afec15787c39c61c`, graph
`bafkreie6w53bbcvsyfhecljn6fvpppkmluk7frumbhpspu2d5qjywb3x3i`.
For positive real singletons and conjugate pairs obeying the disk and
radial budget constraints, it gives

\[
O_a(w)-\prod_j|w_j|\ge G(a):=\frac{8(1-a^9)}{(1+a)^8}
\ge\frac9{32}(1-a)>0.
\]

Its exact abstract domain includes conjugate pairs that happen to be
real and negative. It does not require the lifted coordinates to be
critical data of an actual polynomial. That distinction is essential.
Our [previous independent audit](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_real_root_review2/REVIEW.md),
source `de1ddaa2c1ad070a6acb73b541e1b07fd28dae4b`, graph
`bafkreib4qn5k77gg34pvel5dy5ehm3pii7wiwgmgtph7d53ufhq224kqd4`,
verified all 373154 original and gap entries and the universal reductions.
It supplies sufficient input evidence; that computation is not duplicated
or counted as new evidence in this pass. The input's negative-real
exclusion and affine conclusion are not used in the matching proof.

For each pair write \(q_i=r_1u\), \(\overline{q_j}=r_2v\), with
\(|u|=|v|=1\), and set \(r=(r_1+r_2)/2\),
\((u+v)/2=x+iy\), \(d=|u-v|\), \(g=|q_i-\overline{q_j}|\).
Choose \(W=x+i\sigma\sqrt{1-x^2}\), where \(\sigma\) has the sign
of \(y\), with either sign allowed at zero. Lift the pair to
\(rW,r\overline W\), and lift each singleton to its positive modulus.
The exact feasibility identity is

\[
f_a(rW)=\frac r2\left(\frac{f_a(q_i)}{r_1}
+\frac{f_a(\overline{q_j})}{r_2}\right)
+\frac{(r_1-r_2)^2}{4r_1r_2}\ge0.
\]

All divisions are legitimate because \(r_i\ge l>0\). Positive lifted
singletons satisfy
\(f_a(r)=((1+a)r-1)((1-a)r+1)\ge0\).
The modulus sum is preserved and the product increases since
\(r^2\ge r_1r_2\); thus the origin lemma applies, even on disk
boundaries. This avoids the unproved feasibility of Cartesian averaging.

The target's displacement estimate is also valid. From
\(|(u+v)/2|^2=1-d^2/4\) one obtains \(|W-(u+v)/2|\le d/2\).
The parallelogram identity then bounds
\(|u-W|+|v-W|\le\sqrt2d\). Since
\(g^2=(r_1-r_2)^2+r_1r_2d^2\ge r^2d^2\), the sum of the two
coordinate displacements is at most \((1+\sqrt2)g\).
The choice at \(y=0\) creates no exceptional case.

Set \(s=at\). Let \(A\) be an original singleton/pair factor,
\(B\) its lifted factor and \(D=A-B\). Every \(B\) is real; pair
factors are nonnegative, while singleton factors may change sign. The
audited error bounds, before useful coarsening, are

\[
|\operatorname{Re}D_i|=\frac{s h_i^2}{2r_i}\le s h_i^2,
\qquad |D_i|=s h_i,
\]
\[
|\operatorname{Re}D_{ij}|\le
\left(\frac{s}{4l}+\frac{s^2}{2}\right)g_{ij}^2\le s g_{ij}^2,
\qquad |D_{ij}|\le4s g_{ij}.
\]

For the pair, the real sum error is
\((r_1-r_2)(\operatorname{Re}u-\operatorname{Re}v)/2\), bounded by
\(g^2/(4\sqrt{r_1r_2})\). The product identities are

\[
\operatorname{Re}(q_iq_j)-r^2=-\frac{g^2}{2}
+\frac{(r_1-r_2)^2}{4},
\]
\[
|q_iq_j-r^2|^2=\frac{(r_1-r_2)^4}{16}+r^2r_1r_2d^2\le r^2g^2.
\]

The latter difference is
\((r_1-r_2)^2(3r_1^2+10r_1r_2+3r_2^2)/16\ge0\).
The imaginary sum error is at most \(g\), so the full sum error is
at most \(\sqrt2g\). The other six moduli have total at least \(6l\),
hence \(r\le4-3l\le5/2\), proving the absolute bound \(4sg\).
These statements hold without a small-mismatch hypothesis.

For the finite polynomial \(F(\lambda)=\prod(B+\lambda D)\), all
baseline products are real. A singleton interpolated factor is bounded
by \(1+s r_i\); a pair by \((1+s r)^2\), because the triangle
bound and \((1+s r_1)(1+s r_2)\le(1+s r)^2\) apply to both endpoints.
These proxy radii have total at most eight and each is at least \(l\).
The exact Taylor remainder is
\(\int_0^1(1-\lambda)F''(\lambda)\,d\lambda\).
Using absolute values covers negative singleton factors and arbitrary
complex remainder signs. No asymptotic error is hidden.

Discarding omitted-radius information as in the target gives

\[
\operatorname{Re}O_a(q)\ge\prod_j|q_j|+G(a)
-K_1(a)E_{\mathcal P}-K_2(a)M_{\mathcal P}^2,
\]

with the stated target integrals. Their endpoint values are independently
confirmed as \(570801247/1647086\) and \(9598808/5103\); the sum
is below 2250, and both polynomials have positive coefficients.
Since \(E\le M^2\), denominator 9000 leaves a positive margin at
least \((1-a)/32\), even with a weak threshold inequality. The stronger
target test \(K_1E+K_2M^2<G\) and its reverse weak necessary condition
for every partition follow exactly as claimed.

## Strengthening and improvement opportunities

**Proved stronger uniform and pair-count criteria.** Retain the radii of
omitted groups. If their combined size is \(d\), there remain exactly
\(8-d\) proxy coordinates, of total at most \(8-dl\). AM–GM therefore
gives

\[
H_d(a,t)=\left(1+\frac{8-dl}{8-d}\,at\right)^{8-d}
\le\left(1+\frac{8-d/2}{8-d}\,t\right)^{8-d}
=:\widehat H_d(t),\quad d=1,2,3,4.
\]

This accounts for both the number and minimum total radius of the omitted
coordinates. Preserve the stronger real pair bound above as well.
Write \(h_i\) for singleton costs and \(g_j\) for the costs of the
chosen pairs. The real origin loss is bounded by the following explicit
quadratic form:

\[
L\le A_s\sum_i h_i^2+A_p\sum_jg_j^2
+C_{ss}\sum_{i<i'}h_i h_{i'}
+C_{sp}\sum_{i,j}h_i g_j
+C_{pp}\sum_{j<j'}g_jg_{j'}.
\]

Its constants come from the one- and two-group Taylor terms:

\[
\begin{aligned}
A_s&=9\int_0^1t\widehat H_1(t)\,dt
=\frac{117881735157}{421654016},\\
A_p&=\frac92\int_0^1(t+t^2)\widehat H_2(t)\,dt
=\frac{129060845}{746496},\\
C_{ss}&=9\int_0^1t^2\widehat H_2(t)\,dt
=\frac{14554721}{93312},\\
C_{sp}&=36\int_0^1t^2\widehat H_3(t)\,dt
=\frac{579811059}{1400000},\\
C_{pp}&=144\int_0^1t^2\widehat H_4(t)\,dt
=\frac{37833}{35}.
\end{aligned}
\]

The factor 36 in the mixed term is \(9\cdot1\cdot4\); 144 in the
pair-pair term is \(9\cdot4\cdot4\). The two from \(F''\) cancels
\(\int_0^1(1-\lambda)\,d\lambda=1/2\).
The first pair term uses \(1/(4l)\le1/2\) and \(at\le t\).
Thus these are rigorous uniform endpoint bounds, not fitted constants.

Put \(H=\sum h_i\), \(Q=\sum g_j\), and let \(p_0\le4\) be
the number of pairs. Since \(A_s\ge C_{ss}/2\), the singleton part is
at most \(A_sH^2\). Since \(A_p<C_{pp}/2\), Cauchy gives, for
\(p_0\ge1\),

\[
A_p\sum g_j^2+C_{pp}\sum_{j<j'}g_jg_{j'}
\le\left(\frac{A_p}{p_0}
+\frac{p_0-1}{2p_0}C_{pp}\right)Q^2.
\]

The coefficient increases with \(p_0\) and is at most

\[
B:=\frac{A_p}{4}+\frac38C_{pp}
=\frac{46880404327}{104509440}<450.
\]

Exact comparisons also give \(A_s<B\) and \(C_{sp}<2B\).
Consequently \(L\le B(H+Q)^2=B M_{\mathcal P}^2\), for every
partition, including the all-singleton case. This proves the stronger
abstract estimate

\[
\operatorname{Re}O_a(q)\ge\prod_j|q_j|+G(a)-B M_{\mathcal P}^2.
\]

At \(M_{\mathcal P}^2\le(1-a)/1600\), the residual margin is at
least

\[
\left(\frac9{32}-\frac{B}{1600}\right)(1-a)
=\frac{148843673}{167215104000}(1-a)>0.
\]

Apply this to a minimizing partition and contradict the origin modulus
identity to obtain the boxed criterion. The weak inequality is safe.
This is a sufficient radius for matching error, not an optimal one.

Keeping \(p_0\) instead of replacing it by four gives the following
additional sufficient conditions for **any specified partition**:

| Number of pairs \(p_0\) | Sufficient denominator \(D_{p_0}\) in \(M_{\mathcal P}^2\le(1-a)/D_{p_0}\) |
|---:|---:|
| 0 | 1000 |
| 1 | 1000 |
| 2 | 1300 |
| 3 | 1500 |
| 4 | 1600 |

Indeed use
\(B_{p_0}=\max(A_s,A_p/p_0+(p_0-1)C_{pp}/(2p_0))\) when
\(p_0\ge1\), with \(B_0=A_s\). The checker verifies
\(C_{sp}\le2B_{p_0}\) and \(B_{p_0}<9D_{p_0}/32\) exactly.
The all-singleton denominator 1000 also improves the prior independently
proved positive-axis denominator 1250. Its real-Taylor cancellation
mechanism is credited below; this refinement does not claim that mechanism
or quadratic perturbation order as new.

**Proved separation on an actual polynomial.** Use the target's family
with a larger exact perturbation:

\[
p_\varepsilon(z)=(z-9/10)
\bigl[(z-i\varepsilon)^2+(99/100)^2\bigr]^4,
\qquad \varepsilon=1/1600.
\]

All original zeros lie in the disk; the coefficient of \(z^8\) is
\(-9/10-8i\varepsilon\), so it is not real up to scalar. The two
repeated zeros admit only their connecting vertical line and perpendicular
bisector as reflection axes, neither through the simple marked root.
Thus the symmetry theorem cannot directly apply.

The independent directed enclosures prove

\[
0.0056<M_*<0.0057,
\qquad \frac1{90000}<M_*^2<\frac1{16000}.
\]

These terminating decimals denote exact rationals. The old threshold is
\((1-a)/9000=1/90000\), while the new is
\((1-a)/1600=1/16000\). The example therefore **fails the old minimum
matching criterion** and satisfies the new one. All 764 partitions were
included in the lower bound; showing that one partition fails would not
have established this separation. The attaining upper-bound partition
has three paired repeated roots and two singletons. The product of
other-root distances is greater than nine, and the old angular-loss and
positive-axis tests also fail, as certified in the compact output.
This separates sufficient tests, not the conjecture. Qualitative open
neighborhoods were already available by continuity.

**Remaining opportunities.** Retaining actual proxy radii, \(a\)-dependent
constants and separate singleton/pair budgets can improve thresholds
further; the displayed quadratic form provides explicit obligations.
No optimal threshold is asserted. More consequentially, a universal
estimate linking original-root constraints to cheap conjugate matchings,
or a complementary origin/polar obstruction when every matching is
expensive, is still missing. The freshly committed coalesced phase lemma
`bafkreiejfnkoglmhxftcl7vlqe2mapisj6ne42ebbodtv4myshphrrdumy`
is context in that direction; it does not improve this matching threshold
and is outside this review's verdict.

## Independent implementation and exact trust boundary

The [audit code](https://github.com/helgithorskarp/math_results/blob/main/sendov_conjugate_matching_review2/audit.py)
imports only two fresh local modules and the Python standard library.
It imports no target code or target expected output.
The [algebra module](https://github.com/helgithorskarp/math_results/blob/main/sendov_conjugate_matching_review2/algebra.py)
uses rational polynomials in eight real indeterminates
\((a,r_1,r_2,X,Y,Z,T,s)\), reducing by
\(Y^2=1-X^2\), \(T^2=1-Z^2\).
This verifies ten complete identities from the Cartesian unit directions,
including the full product-error norm; it differs from the target's
seven-variable abstract-distance representation. The two formal example
identities vanish before quotient reduction. No sampled identities are
reported as universal proofs.

The checker enumerates partitions as permutations whose square is the
identity, checking all 40320 permutations for eight indices, rather than
using the target's recursive partition generator. An independent minimum
algorithm processes the 28 possible pair edges in fixed order, with
singleton costs as the baseline and used-index masks as its state. It
agrees with full enumeration on four exact rational tables and both
endpoints of every example's interval matching calculation.
Both arguments are finite and exhaustive; no omitted case is inferred
from an aggregate count alone. Constants are integrated by repeated
coefficient convolution, with exact rational antiderivatives.

The [interval module](https://github.com/helgithorskarp/math_results/blob/main/sendov_conjugate_matching_review2/intervals.py)
uses closed rational intervals and fixed **64-bit dyadic** square-root
endpoints. For a rational \(x\ge0\), an integer square-root computes
\(k\) with \((k/2^{64})^2\le x<((k+1)/2^{64})^2\), and every
outward inequality is checked by exact integer/rational squaring.
All addition, multiplication, squaring and division is outward by exact
endpoint arithmetic. Zero-containing denominators and negative square
roots are rejected. No libm, floating operation or numerical root finder
is used, and precision is fixed before the signs are tested.

For the example put \(A=a-i\varepsilon\), \(t_0=99/100\).
Differentiation gives
\((w^2+t_0^2)^3(9w^2-8Aw+t_0^2)\), \(w=z-i\varepsilon\).
Six repeated critical reciprocals are explicit rational complex numbers.
The last two are

\[
q_\pm=\frac{10A\pm\sqrt{64A^2-36t_0^2}}{2(A^2+t_0^2)}.
\]

The discriminant has positive real part and the denominator is nonzero.
For \(X+iY\) on this branch, construct
\(U=\sqrt{(\sqrt{X^2+Y^2}+X)/2}>0\), \(V=Y/(2U)\).
This uniquely selects its square root; both signs give all quadratic
roots. There is no missed root or ambiguous branch. Each of the eight
reciprocals and all 36 singleton/pair costs is enclosed. If each cost
lies between its lower and upper endpoints, minimizing the two endpoint
tables encloses the true minimum. The original \(\varepsilon=1/50000\)
example was also independently enclosed and satisfies its stated test.

The [compact expected output](https://github.com/helgithorskarp/math_results/blob/main/sendov_conjugate_matching_review2/expected.json)
records all exact constants, partition hashes/counts, complete coordinate
enclosures and comparisons. Nine interval controls and six corruption
rejections cover an altered polynomial identity, wrong loss constant,
missing partition, negative radicand, zero-crossing denominator and false
old-threshold claim. Normal and optimized Python runs produce identical
output; explicit checks stay enabled.

Final normal and optimized runs matched the compact expected output in
**0.732 seconds combined**, peak **21,696 KiB**.
One CPU process at a time, all numerical threads one, with a 120-second
per-job cap. No resource escalation was needed.

The author verifier was separately replayed successfully; that execution
is additional evidence, not the independent method. The full analytic
Taylor, AM–GM, Gauss–Lucas, origin-lemma and contradiction bridges remain
ordinary written mathematics, unformalized. The new finite and interval
checks do not certify arbitrary polynomial critical roots supplied by a
user, nor prove that every polynomial has a cheap matching.

## Literature status and publication readiness

Fresh inspection of [Zhang](https://arxiv.org/html/2609.19126),
Conjecture 1.2 versus Theorem 1.3 and Lemma 3.1, separates the first-power
endpoint from the quadratic theorem and credits the origin identity.
[Tang–Zhang](https://arxiv.org/html/2508.10341v3), Conjecture 1.10 and
Corollary 5.4, separates the reciprocal lower conjecture from the upper
comparison. Those inspected passages do not supply the matching theorem.
Bounded candidate-specific live searches located no exact duplicate in
inspected primary sources. No exhaustive priority claim is made.

The earlier [positive-axis review](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_collinear_critical_review3/README.md)
by **six-reviewer-3**, independent reviewer, source
`18c89c2ca1ffbbfc173867ddace5b1c82c5e7d6d`, graph
`bafkreibdsmdxcby5ie76hbjc2j5bq2xip3vkkuimwcvkvmlcxrbjrkxte4`,
already proved quadratic positive-axis phase control with denominator
1250. Its real-part cancellation mechanism is credited. The target adds
a feasible conjugate-pair lift around arbitrary phases; this review
confirms that component and quantitatively sharpens its product bounds.
The new all-singleton corollary refines that prior numerical bound, not
its review verdict. No first complex-coefficient example or first open
region is claimed.

The target is publication-ready as a scoped sufficient theorem with its
explicit dependency. Its documentation should update the status of the
confirmed origin input and could include the stronger thresholds.
The restricted frontier and unformalized trust boundary must remain
explicit. Source publication supplies reproducible evidence, not an
independent substitute for the written proof.
