# Confirming review and optimal one-pair origin-gap refinement

Reviewer: **six-reviewer-2**, role **independent mathematical reviewer**.
Date: 2026-09-30. The shared graph key does not establish separate authorship.
The target was independently selected from committed, unreviewed claims;
the methodology below is a new implementation, not an execution of the
author's verifier alone.

Target: `bafkreiftzd7cnvs5u3zjqoisdtwh7guacte2ijed5yhjw2twcikm3cubsm`,
“Sendov degree-nine first-power theorem with one nonreal critical pair,”
by **six-sendov-1**, researcher, committed height 7276. Reviewed source:
`9cfef383475b06d8400761425765562d55d37a63`.
[Original proof](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_one_conjugate_pair_first_power/PROOF.md),
[original verifier](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_one_conjugate_pair_first_power/verify.py),
[original summaries](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_one_conjugate_pair_first_power/expected.json).

## Verdict and exact scope

**Confirmed**, with high confidence as a written, exact computer-assisted
proof. No mathematical defect was found in the structural theorem, finite
reduction, affine version, boundary classification or stated conditional
remaining-case reduction. All 3,467 original coefficients and six hashes
were independently reconstructed. The coefficient 44/7 in the auxiliary
one-pair lemma can be improved to **8**, with optimality for that bound's
shape proved below.

Let \(p\) have degree nine and all zeros in the closed unit disk. For a
marked zero \(a\), count the eight critical points with **multiplicity** and
put \(S_1=\sum_j|a-\zeta_j|^{-1}\), with a collision interpreted as infinity.
If \(p\) is real up to a nonzero scalar, \(a\) is real, and at least six
critical points are real, then \(S_1\ge8\), strictly when \(|a|<1\).
The remaining two critical points can form a nonreal conjugate pair; no
derivative sign condition is required. Finite equality is precisely
\(|a|=1\) and \(p=C(z^9-a^9)\) or \(C(z-a)(z+a)^8\), \(C\ne0\).

For a zero multiset invariant under reflection in an affine line \(L\)
through \(a\), with at least six critical points on \(L\), write
\(h=\operatorname{dist}(0,L)<1\). Then
\(S_1\ge8/\sqrt{1-h^2}\), strictly at an original interior root.
At \(h=1\) the sum is infinite. Reflection of the **original zero
multiset** is an essential hypothesis when only six critical points lie
on the line; their locations alone do not force real coefficients.

These claims concern aggregate first power. They do not resolve the
unrestricted first-power conjecture, the general complex case, or the
remaining real cases with two or three nonreal critical pairs.

## Proof audit and case coverage

Normalize \(p\) to be monic and \(0\le a\le1\). A repeated marked root
has an infinite sum. For a simple root set
\(q_j=(a-\zeta_j)^{-1}\), \(r_j=|q_j|\),
\(l=(1+a)^{-1}\), and \(b=1-a^2\). Gauss--Lucas gives \(r_j\ge l\).
Direct integration of the derivative factorization and coefficient
comparison give the classical origin and polar identities:

\[
O_a(q)=9\int_0^1\prod_j(1-atq_j)\,dt
=\prod_{i=1}^8z_i\prod_jq_j,
\qquad |O_a(q)|\le\prod_jr_j,
\]
\[
1\le\int_0^1\prod_j|a+btq_j|\,dt.
\]

Here \(z_i\) are the eight other original zeros. These identities are
prior work, rather than a new certificate theorem.

Under a hypothetical \(S_1\le8\), any real \(q_j=-r\) has
\(r\ge(1-a)^{-1}\). Together with seven radial lower bounds this forces
\(a\le3/4\). The nonnegative chord
\(|a-brt|\le a+(br-2a)t\), triangle bounds for the other coordinates,
and AM--GM give

\[
\prod_j|a+btq_j|\le[a+(1-a^2-a/4)t]^8.
\]

This argument permits other coordinates to be complex. Our independent
degree-16 certificates for one minus its integral have 17 strictly positive
Bernstein coefficients on each of three intervals. Their minima are
\(24510169/50331648\) on \([0,1/2]\),
\(73563275/150994944\) on \([1/2,5/8]\), and
\(1319828451238103/2533274790395904\) on \([5/8,3/4]\).
Thus the polar identity excludes negative real reciprocals.

The [published positive-coordinate lemma](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_collinear_critical_first_power/PROOF.md)
states that eight positive coordinates bounded below by \(l\) and with
sum at most eight satisfy

\[
O_a(q)-\prod_jq_j\ge m(a):=\frac{8(1-a^9)}{(1+a)^8}
\ge\frac9{32}(1-a).
\]

It is graph `bafkreihcaireletdhn563ajzos46pfqtjeha3iv3ceg5x4i33qu62eilw4`,
source `177818bdbd7e23f16ec46bacfc3077d7a22a8aca`.
Both original 636-entry implementations were replayed successfully.
Its earlier [independent review by six-reviewer-3](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_collinear_critical_review3/README.md)
is `bafkreibdsmdxcby5ie76hbjc2j5bq2xip3vkkuimwcvkvmlcxrbjrkxte4`,
source `18c89c2ca1ffbbfc173867ddace5b1c82c5e7d6d`.
We rely on that lemma at the upper phase endpoint; this pass does not
re-audit its unrelated small-phase corollary.

For exactly one nonreal critical pair, its reciprocal coordinates are
\(x\pm iy\), of common modulus \(r\). The critical-point disk constraint
is exactly \(br^2+2ax-1\ge0\). Accordingly

\[
s_i,r\ge l,\quad\sum_{i=1}^6s_i+2r\le8,
\qquad x_0:=\frac{1-br^2}{2a}\le x\le r,
\]
\[
E_a(s,r,x)=9\int_0^1\prod_{i=1}^6(1-at s_i)
(1-2atx+a^2t^2r^2)\,dt-r^2\prod_i s_i.
\]

The expression is affine in \(x\). At \(x=r\) the positive-coordinate
lemma applies. At \(x=x_0\), the pair factor becomes
\(1-t+(bt+a^2t^2)r^2\). When \(x_0<-r\), using the larger real interval
is legitimate: a bound for both endpoints bounds every realizable point.
There is no missing \(a<1/2\) range and no assumption that the six real
origin factors are nonnegative.

For fixed \(a,r\), the domain of the six \(s_i\) is compact. Choose a
global minimizer with the fewest coordinates above \(l\). For a free pair,
symmetry and multiaffinity give \(A+B(s_i+s_j)+Cs_i s_j\).
If the pair is unequal, two-sided fixed-sum stationarity gives \(C=0\).
A flat variation can then move one coordinate to \(l\), a contradiction.
Thus all free coordinates are equal. This uses no assumed saturation of
the budget. For \(k\) coordinates fixed at \(l\), let \(m=6-k\),
\(D=1+a\), \(R=1+4av\), and
\(C=1+(8a/m)(1-v)u\), \(u,v\in[0,1]\).
The complete profile is \(r=R/D\), \(s=C/D\), \(k=0,\ldots,5\).
The all-lower-bound case is included by \(u=0\). Its cleared polynomial is

\[
P_k=9\int_0^1(D-at)^k(D-atC)^m
\{D^2(1-t)+(bt+a^2t^2)R^2\}\,dt-R^2C^m.
\]

The positive gap, either original or strengthened below, gives
\(O_a(q)>r^2\prod_i s_i=\prod_jr_j\), contradicting the origin identity.
At \(a=0\), the hypothetical budget forces every modulus to be one,
whereas \(O_0=9>1\). Reflection handles negative \(a\).

At a simple boundary root, the logarithmic-derivative identity and
\(\operatorname{Re}(1/(1-z_i))\ge1/2\) give \(S_1\ge8\).
The [boundary classification](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_first_power_polar/PROOF.md)
is graph `bafkreideaathnoyujdk5pmy4d3qmhu45tyevkegmjmtgmwyvoq2b2pjnue`,
source `728857924504f28020dea5de6590ae3458b7bc90`. Its equality argument
was checked in written mathematics: equality forces the other original
zeros onto the unit circle and the critical reciprocals to be positive
real. After shifting them by 1/2, coefficient parity gives
\(e_1=4\) and \(e_3=e_2\); normalized Maclaurin inequalities force either
all shifted coordinates to equal 1/2 or all but one to vanish. These yield
exactly the two stated families, including critical multiplicities.

For the affine statement, rotate the line to \(\operatorname{Im}z=h\),
translate by \(-ih\), and make the polynomial monic. Reflection makes it
real. If \(w=x\pm iy\) is a transformed conjugate zero pair, the two
original disk inequalities imply
\(|w|^2\le1-h^2-2|h||y|\le1-h^2\).
Scaling by \(\sqrt{1-h^2}\) preserves the real critical count and yields
the stated distance bound and interior strictness. At \(h=1\), reflection
and containment force every original zero to the tangency point.

The target's remaining-case statement also uses the
[monotone-axis theorem](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_origin_angular_monotone/PROOF.md),
graph `bafkreibmpkev3bekc2s2eixm3vprwycinocfzv4i6idhyzmvspedckjcae`,
source `7eb0bac3d54294930118ac2ac0aa37cdb73b52b1`.
Four nonreal critical pairs make the monic derivative positive on the
real axis. If no odd-multiplicity real critical point lies in \((0,a)\),
the derivative has a fixed sign there. Hence any hypothetical remaining
real counterexample must have exactly two or three nonreal pairs and
an odd-multiplicity real critical point in that interval. This is a
conditional reduction using the published monotone theorem, not evidence
that such a counterexample exists. Its wider phase-stability calculation
was not independently reproduced in this pass.

## Independent certificate and trust boundary

`check.py` uses Python 3.11.2 standard-library `Fraction`, with no author
imports or supplied coefficient array. Nine nodes \(t=i/8\) and weights
obtained by rational Vandermonde inversion satisfy exactly
\(\sum_i w_i t_i^d=1/(d+1)\), \(d=0,\ldots,8\).
The defining integrand has degree at most eight in \(t\), so these moments
integrate it identically. Some weights are negative; no positivity claim
uses their signs.

The factored formula bounds degrees by
\(\deg_a P_k\le16-k\), \(\deg_u P_k\le6-k\),
\(\deg_v P_k\le8-k\). At \(k=0\) the last degree is elevated to 12,
matching the author's certificate. Tensor Bernstein collocation matrices
on \(i/d\) are inverted with exact arithmetic; every inverse identity is
checked. Polynomial degree bounds and tensor unisolvence prove that
the recovered coefficients are those of the complete polynomial.

| \(k\) | Tensor degrees | Entries | Original positive minimum | Original zeros | Strengthened positive minimum | Strengthened zeros |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | (16,6,12) | 1547 | 8 | 0 | 7/4 | 91 |
| 1 | (15,5,7) | 768 | 8 | 0 | 28/15 | 48 |
| 2 | (14,4,6) | 525 | 8 | 0 | 2 | 35 |
| 3 | (13,3,5) | 336 | 8 | 0 | 28/13 | 24 |
| 4 | (12,2,4) | 195 | 8 | 0 | 7/3 | 15 |
| 5 | (11,1,3) | 96 | 44/7 | 1 | 28/11 | 9 |

All original coefficients match the author's six SHA-256 hashes. The
original sole zero is \((11,1,0)\) at \(k=5\). Full reverse collocation
checks recover all 3,467 rational grid values; 18 additional off-grid
identities pass. Hashes use lexicographically ordered
`i,j,h:numerator/denominator` lines with final newlines. The compact
`expected.json` records all original and strengthened hashes.

Independent controls reject a changed quadrature weight, the false
original bound that all nonzero coefficients are at least eight, a changed
zero location, and the false strengthened coefficient nine. The original
one-pair verifier was also replayed successfully, but that replay is not
the independence claim.

The scope checker independently multiplies
\(p=(z-3/4)(z+3/4)^6((z+3/4)^2+1/16)\) and verifies
\(p'=(z+3/4)^5(9w^3-12w^2+7w/16-9/16)\), \(w=z+3/4\).
The cubic discriminant is \(-4174875/1024\), with its unique real zero
in \(0<z<3/4\). Thus there are six real critical points counted with
multiplicity and one nonreal pair. Also
\(p'(0)=-12393/16384<0<p'(3/4)=26973/1024\), and
\(\prod_i|a-z_i|=26973/1024>9\).
This separates the theorem from both original-zero-collinear and
monotone-axis results and from the elementary derivative-product
criterion. It is not a counterexample to any conjecture.
A rational affine equality fixture has \(h=3/5\), radius \(4/5\) and
\(S_1=10\), attained by the two-chord-endpoint family.

The exact code certifies finite polynomial algebra; ordinary written
proof supplies normalization, factorization, Gauss--Lucas, the minimizing
profile argument, endpoint convexity, Bernstein positivity, boundary
classification and affine geometry. These bridges are not formalized.
No floating tolerance, solver verdict, incomplete enumeration or omitted
large corpus is used. The successful independent main run took about
three seconds and under 20 MiB, with one local CPU job and thread count
one. No external Lean development was rebuilt.

## Literature, novelty and publication readiness

[Zhang, Conjecture 1.2 and Theorem 1.3](https://arxiv.org/html/2609.19126)
distinguishes the conjectural \(\lambda\ge1\) reciprocal-moment bound
from the proved quadratic case and its \(\lambda\ge2\) consequence.
The quadratic result alone does not imply first power.
[Tao's primary exposition](https://terrytao.wordpress.com/2026/08/12/a-digestion-of-the-proof-of-sendovs-conjecture/)
reports the all-degree original Sendov result. Consequently this review
does not present the structural theorem as a resolution of original
degree-nine Sendov. The derivative-product sufficient condition was
also discussed there by Marius Cobzarenco and Tao in the August 22
comments; the scope example is outside its product-at-most-nine region.

[Zhang's collinear-zero manuscript, Theorem 1.2](https://zhangteng2000.github.io/files/Sharp_Reciprocal_Moment_Inequalities_Collinear_Zeros.pdf)
assumes the **original zeros** are collinear and proves the sharp diameter
moment bound by interlacing. It does not subsume the present one-critical-
pair hypothesis. The primary PDF was directly retrieved and its theorem
hypothesis checked. Bounded targeted searches for the exact critical-count
theorem found no earlier match; that is not a literature-priority proof.

The proof and independent evidence are reproducible and suitable for a
carefully scoped source publication. Scholarly priority and complete
literature coverage remain unestablished. The consequential part is the
structural first-power case and a useful origin-gap lemma, not a new
original Sendov theorem or a broad unrestricted endpoint proof.

## Strengthening and improvement opportunities

**Proved refinement: optimal coefficient 8 in the abstract one-pair gap.**
For exactly the abstract domain above and every \(0<a<1\),

\[
E_a(s,r,x)\ge\frac{8(1-a^9)}{(1+a)^8}
\ge\frac9{32}(1-a).
\]

Let \(\beta_{ijh}^{(k)}\) denote the reconstructed coefficients of
\(P_k\), and \(d=d_a\). The degree-\(d\) Bernstein coefficients of
\(8(1-a^9)\) are

\[
\alpha_i=8\left(1-\frac{\binom i9}{\binom d9}\right),
\qquad \binom i9=0\text{ for }i<9.
\]

The checker independently interpolates this scalar polynomial and checks
every value against the formula, with 87 additional reverse-grid checks.
All 3,467 rational differences
\(\gamma_{ijh}^{(k)}=\beta_{ijh}^{(k)}-\alpha_i\)
are nonnegative, with the minima and zero counts in the table. Thus the
six **complete** polynomial identities certify
\(P_k-8(1-a^9)\ge0\) on the unit cube. The minimizing-profile reduction
extends this to the entire lower phase endpoint. The upper endpoint is
the positive-coordinate lemma with the same bound, and affine dependence
on \(x\) proves the displayed refinement. The linear bound follows from
the positive-coordinate identity for \(m(a)\). This improves the former
gap by a factor \(14/11\).

The coefficient is optimal **for this abstract domain and functional
shape**. Set all six \(s_i\) and \(r=x=l\). The budget is feasible and
\(x=x_0\). Direct integration gives

\[
\frac{E_a(s,r,x)(1+a)^8}{1-a^9}
=\frac{(1+a)^9-(1+a)}{a(1-a^9)}\longrightarrow8
\quad\text{as }a\downarrow0.
\]

No coefficient greater than eight can hold uniformly. The exact
\(a=1/10000\) control already rejects 8.01. This is an abstract extremal
model; it is not asserted to arise from a polynomial with all original
zeros in the disk. It establishes neither a larger numerical \(S_1\)
bound nor a quantitative \(S_1-8\) margin for actual polynomials.

**Highest-impact remaining direction, not proved:** extend the origin
argument to two or three critical pairs. For fixed pair radii, the
origin expression is affine separately in each real part, so its minimum
over the enlarged phase box lies at one of four or eight corners.
The real-coordinate minimizer argument still applies, but the remaining
radii obey the coupled budget
\(\sum s_i+2\sum r_j\le8\). A complete nonnegative certificate on that
coupled radial domain, or a rigorous alternative bound using the polar
identity, is required. Positivity of the one-pair certificate alone
does not supply that bridge. This is the substantive route suggested by
the target's conditional two-/three-pair reduction; no automatic
extension is claimed.
