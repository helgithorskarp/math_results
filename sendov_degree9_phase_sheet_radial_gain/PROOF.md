# A global radial gain averaged over the two common-phase sheets

Actual author **six-sendov-1**, role **researcher**, 2026-09-30.
Complete ordinary written author proof with exact finite evidence;
independent review pending. The balanced origin bound is a credited
premise. This result does not prove unrestricted first power, or even
the whole unequal-radius critical 4+4 case.

## 1. Exact claim

Let \(0\le b\le cx\le1\), \(0\le c,x\le1\), and let real \(d,y\)
satisfy \(c^2+d^2=x^2+y^2=1\). Put \(w=x+iy\). For

\[
0\le\eta\le\tfrac12,\qquad Q=\eta^2,\qquad
U_\pm=(1\pm\eta)w(c+id),\quad
V_\pm=(1\mp\eta)w(c-id),
\]

define

\[
O_\pm=9\int_0^1(1-btU_\pm)^4(1-btV_\pm)^4\,dt,
\quad N_\pm={|O_\pm|^2\over(1-Q)^8},\quad
\mathcal A(Q)={N_++N_-\over2}.
\]

The signs exchange the two radii while keeping the two phases fixed;
they do not conjugate the entire configuration. At \(Q=0\) the two
norms coincide, and their value is denoted \(N_0\).

**Averaged radial theorem.** Throughout this full common-phase domain,

\[
{d\mathcal A\over dQ}>{7\over(1-Q)^9},\qquad
\mathcal A(Q)\ge N_0+{7\over8}\big[(1-Q)^{-8}-1\big]
\ge3-2b+{7\over8}\big[(1-Q)^{-8}-1\big].                 \tag{1}
\]

The first integrated inequality is strict when \(Q>0\). In particular

\[
\mathcal A(Q)\ge3-2b+7Q.                                  \tag{2}
\]

No optimal constant is asserted. This theorem retains arbitrary common
phase and full relative imbalance, but averages the two signed sheets.
It is stronger than an unsigned perturbation estimate and weaker than
an individual-sheet origin bound.

## 2. Polynomial kernel and a complete finite certificate

Writing \(\beta=\eta d\), the paired factor in the integral is

\[
1-2btw(c+i\beta)+b^2t^2(1-Q)w^2.
\]

Its fourth power has nine integrated coefficients. Squaring the resulting
integral and reducing \(d^2=1-c^2\), \(y^2=1-x^2\) gives exact rational
polynomials

\[
|O_+|^2=E(b,c,x,Q)+\lambda J(b,c,x,Q),\qquad
\lambda=-\eta d y,\quad
|O_-|^2=E-\lambda J.                                      \tag{3}
\]

Here \(E\) has 551 nonzero monomials and \(J\) has 295. The checker
derives every coefficient by two routes: a multinomial paired expansion
with Chebyshev cross terms, and four direct quadratic convolutions followed
by squaring the full real and imaginary parts. It also compares 20 pairs
of exact Gaussian-rational norms against eight direct linear convolutions.
These are author cross-checks, not independent peer review.

Equation (3) implies

\[
\mathcal A={E\over(1-Q)^8},\qquad
\mathcal A_Q={K\over(1-Q)^9},\quad
K=(1-Q)E_Q+8E.                                             \tag{4}
\]

The new finite inequality is **\(K>7\) whenever \(0\le b\le cx\le1\)
and \(0\le Q\le1/4\)**. To prove it, substitute

\[
b=tcx,\qquad Q=q/4,\qquad t,c,x,q\in[0,1].
\]

This parametrizes the entire stated domain: if \(cx=0\), then \(b=0\);
otherwise choose \(t=b/(cx)\). The polynomial \(K-7\) has tensor degree
at most \((15,16,16,7)\) in these new coordinates. Its tensor Bernstein
basis is nonnegative and sums to one. The full \(t,q\) intervals and the
following five rectangles in \(c,x\) cover the unit cube.

| \(c\) interval | \(x\) interval | Minimum coefficient of \(K-7\) |
| --- | --- | --- |
| \([0,1]\) | \([0,1/2]\) | \(2963365694921/131533373440\) |
| \([0,1/2]\) | \([1/2,1]\) | \(125740982300897/1315333734400\) |
| \([1/2,3/4]\) | \([1/2,1]\) | \(393292274316073277/86201711617638400\) |
| \([3/4,1]\) | \([1/2,3/4]\) | \(8646616828491364672619/5020387684611260416000\) |
| \([3/4,1]\) | \([3/4,1]\) | \(207381757/642252800\) |

Every cell has **36,992 coefficients**; all **184,960 coefficients**
are strictly positive. The checker checks coverage and disjoint interiors,
regenerates every entry, and compares midpoint de Casteljau subdivision
against direct affine power substitution and conversion. It inverts the
entire tensor basis on every cell back to its power polynomial, and also
inverts the original full-box tensor. No large coefficient file is needed.

The forward formula for a power coefficient \(a_{k}\), with multi-indices,
is

\[
\gamma_i=\sum_{k\le i}a_k\prod_{j=1}^4
 {\binom{i_j}{k_j}\over\binom{n_j}{k_j}}.
\]

The inverse uses, along each axis,

\[
a_k=\binom nk\sum_{j=0}^k(-1)^{k-j}\binom kj\gamma_j.
\]

Shared denominators reduce these computations to integer arithmetic.
The checked degree, exact minima and canonical coefficient hashes are
in [expected.json]\(expected.json). Positivity proves (K>7\), including
all parameter boundaries. Equation (4), integration from zero, and

\[
{7\over8}\big[(1-Q)^{-8}-1\big]\ge7Q
\]

give the first assertion and (2). The last elementary inequality follows
from the binomial expansion, or integration of \((1-Q)^{-9}\ge1\).

The remaining input in \(1), **(N_0\ge3-2b\)**, is the already published
[balanced unit-origin lemma, Section 3](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_balanced_radius_origin_gap/PROOF.md).
It applies since the two unit directions have average real part \(cx\ge b\).
Its stronger rectangular certificate on \(c,x\in[b,1]\) was independently
audited in the [near-balanced review](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_balanced_radius_review2/REVIEW.md).
That finite input is cited, not newly claimed or silently reproduced here.

## 3. A necessary signed-skew barrier for hypothetical first-power failure

For a degree-nine disk-root polynomial with critical multiplicities 4+4,
rotate a finite simple marked zero to \(a\in(0,1)\), and write its two
critical reciprocals as

\[
U=m(1+\eta)w(c+id),\quad V=m(1-\eta)w(c-id),\quad b=am.
\]

Suppose the first-power budget \(4(|U|+|V|)\le8\) holds. Then \(m\le1\).
Gauss--Lucas gives both radii at least \(1/(1+a)\), hence

\[
0\le\eta\le{a\over1+a}\le\tfrac12.
\]

The classical origin identity gives

\[
N_{\rm actual}=m^{-16}{E+\lambda J\over(1-Q)^8}\le1.       \tag{5}
\]

On the additional domain \(0\le c,x\le1\), **\(cx\ge am\)**, (1) forces

\[
-\lambda J\ge(1-Q)^8(3-2am-m^{16})
              +{7\over8}\big[1-(1-Q)^8\big]>0.            \tag{6}
\]

Thus an individual sheet with \(\lambda J\ge0\) cannot satisfy the
first-power budget. This is an explicit signed-kernel criterion, not a
claim that the sign follows from all polynomial hypotheses.

The credited [actual mean lemma](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_actual_mean_gap/PROOF.md)
gives \(m(cx+\lambda)>a\) under that budget and the polar identity.
Consequently the domain \(cx\ge am\) is automatic when \(\lambda\le0\)
and the canonical \(c,x\) are positive. When \(\lambda>0\), a configuration
can have \(cx<am\); (6) is not asserted there. Origin (5), the stronger
actual mean filter, and the skew relation must still be coupled to close
the remaining interior problem. A reflected abstract sheet need not come
from another disk-root polynomial.

## 4. Even the mean-decreasing sheet need not be radially monotone

The averaging in (1) cannot be removed by asserting radial monotonicity
on \(\lambda\le0\). Here is an exact obstruction that retains the polar,
critical-disk and quantitative actual-mean filters.

Take

\[
a=4/5,\quad m=1,\quad\eta=1/10^6,\quad
c+id={399+40i\over401},\quad w={99+20i\over101}.
\]

Use the plus sheet \(U,V\) above, so \(\lambda=-\eta d y<0\), and let

\[
U_0=w(c+id),\quad V_0=w(c-id),\quad
C=\int_0^1(a+(1-a^2)tU)^4(a+(1-a^2)tV)^4dt.
\]

Define \(C_0\) using \(U_0,V_0\), and \(N,N_0\) as the normalized origin
norms at \(eta,0\). Exact rational arithmetic proves

\[
-{1\over5\cdot10^9}<N-N_0<-{1\over10^{10}},\qquad
3/2<N<N_0<8/5,\qquad 9/8<|C|^2,|C_0|^2<5/4.             \tag{7}
\]

For all four reciprocal coordinates \(Z=U,V,U_0,V_0\),

\[
2a\Re Z+(1-a^2)|Z|^2-1>0,
\]

which is equivalent to the critical point \(a-1/Z\) being strictly inside
the disk. Both lower-radius bounds hold, and for the imbalanced data

\[
\Re(U+V)/2>a+{256\over32955}{1-a^2\over a}.
\]

These are abstract necessary-channel data with **\(N>1\)**. They are
neither a disk-root polynomial witness nor a counterexample to first
power or to the averaged theorem. They disprove the stated one-sheet
transport shortcut. The earlier [radial obstruction](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_actual_mean_gap/PROOF.md)
has \(\lambda>0\); the sign restriction alone therefore cannot repair
monotonicity on either sheet.

## 5. Reproduction and proof boundary

Python 3.10+ standard library only, one process and all numerical threads one:

~~~bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B verify.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B -O verify.py
~~~

Both regenerate the required complete expected manifest and reject seven
corruptions using explicit exceptions. The checker validates the full
finite certificate, both exact norm constructions, Gaussian controls,
all assertions in (7), disk slacks and the actual mean threshold.
The analytic use of Bernstein positivity, integration in (4), the cited
balanced lemma and communication identities, and the interpretation of
(6) remain ordinary written mathematics. There is no proof-assistant
formalization, exhaustive polynomial enumeration, floating proof input,
solver, externally imported campaign module, or independent-review verdict.

The original unrestricted first-power endpoint remains conjectural in
[Zhang, Conjecture 1.2](https://arxiv.org/html/2609.19126) and
[Tao, Conjecture 19](https://terrytao.wordpress.com/2026/08/12/a-digestion-of-the-proof-of-sendovs-conjecture/).
The known quadratic inequality and ordinary Sendov proof report are
distinguished from this averaged degree-nine functional estimate.
