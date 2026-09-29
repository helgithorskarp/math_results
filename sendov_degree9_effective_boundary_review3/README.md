# Independent review of the effective degree-nine first-power annulus

Reviewer: **six-reviewer-3**, role **reviewer**, 29 September 2026.
Selection, analysis and implementation were independent. All campaign
signatures share an identity; signatures do not establish distinct authorship.

**Verdict: confirmed with high confidence as an ordinary mathematical proof.**
The target, authored explicitly by six-sendov-2, researcher, is
**Sendov degree-nine effective first-power boundary stability and explicit
annulus**, graph reference
bafkreigenk4drh3ixa54mwshdukdnv3xs2f7khffkpc7u2t4rfcmcq34ey.
The complete
[target proof](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_effective_boundary_first_power/PROOF.md)
was checked at source commit 4ef7996638ffee0f42d7780e477c2745aeac233e.
Its proof SHA256 is
9fffca3e956d09353dc4dddbb98cc62eaf12edf0afaae47b395a64cc349b1dde.
The graph target and its full neighborhood were inspected before selection.
Earlier reviews concern the preceding local lemma, concentration argument,
quadratic boundary stability and a distinct existential linear margin.
They do not audit the effective claim assessed here.

This review confirms both the quantitative critical-energy reduction and
the original numerical annulus. A proved refinement below widens the annulus
by a factor of **121**, keeping the same strict slope. This does not settle
the first-power endpoint on the remaining range of root moduli.

## Scope, hypotheses and case coverage

Let \(p\) have degree nine and all its roots in the closed unit disk.
Count its eight critical points \(\zeta_j\) with multiplicity, and define

\[
F(a)=\sum_{j=1}^8|a-\zeta_j|^{-1},\qquad
Q=\sum_{j=1}^8|\zeta_j|^2,\qquad T=\max_j|\zeta_j|.
\]

A zero denominator gives infinity. Multiplication by a nonzero scalar and
rotation permit monic normalization and a distinguished root
\(a=|a|\in[0,1]\). Set \(\eta=1-a\).

The verified statements are:

1. If \(0<\eta\le10^{-6}\) and \(F(a)\le8+\eta/20\), then
   \(Q\le1.6\times10^9\eta\).
2. For every interior distinguished root with
   \(1-10^{-18}\le|a|<1\), one has \(F(a)>8+(1-|a|)/20\).
3. **Refinement proved here:** the second statement holds on the larger
   closed-inner-endpoint annulus
   \[
   1-121\times10^{-18}\le|a|<1.
   \]

The first assertion is a necessary condition under a hypothetical small
first-power sum. It does not assert existence of polynomials realizing
that hypothesis. Repeated distinguished roots give infinity and cannot
satisfy it. Repeated other roots and critical points are allowed throughout.
Boundary roots \(|a|=1\) are excluded from the strict annulus assertion;
both the binomial and collapsed families attain the boundary sum eight.
The small-root branch in the local argument is covered explicitly below.

## The finite reduction passes the audit

Put \(q_j=(a-\zeta_j)^{-1}\), \(r_j=|q_j|\),
\(\mu=\frac18\sum r_j\), and \(u_j=(a-z_j)^{-1}\), where the \(z_j\)
are the eight other roots. A finite \(F\) makes the distinguished root
simple. Differentiating the normalized root factorization gives

\[
e_k(q)=(k+1)e_k(u),\qquad \mu\le1+\eta/160.
\]

Maclaurin followed by the root equation for the polynomial with roots
\(u_j\) gives the strict Cauchy bound \(|u_j|<7\mu<8\), because

\[
\sum_{k=1}^8\frac{\binom8k}{(k+1)7^k}
=\frac{41980912}{51883209}<1.
\]

Gauss--Lucas and the sum hypothesis give
\(1/(1+a)\le r_j<5\). The disk condition on \(z_j=a-1/u_j\) is exactly

\[
(1-a^2)|u_j|^2+2a\Re u_j-1\ge0.
\]

It yields, with \(\alpha_j=\Re u_j-1/2\),

\[
\sum|\alpha_j|<1100\eta,\quad|\alpha_j|<456\eta,\quad
8-\Re\sum q_j<1030\eta.
\]

In particular the angular defect and mean drift satisfy

\[
D=\tfrac18\sum(r_j-\Re q_j)\le140\eta,\qquad
|\mu-1|\le130\eta.
\]

These estimates use disk-root containment, rather than an assumption that
each critical distance is at least one. The individual reciprocal bounds
also prevent any omitted collision or division by zero.

### Finite variance exclusion

Let \(v=\frac18\sum(r_j-\mu)^2\), \(b=1-a^2\). The polar identity follows
by integrating \(p'\) from \(a\) to \(1/a\) and comparing root products:

\[
\prod_j\frac{1-az_j}{a-z_j}
=\int_0^1\prod_j(a+btq_j)\,dt.
\]

The left factors have modulus at least one. The second derivative of
\(\log(a+btr)\) on \(0\le r\le5\) is at most
\(-(bt)^2/(a+5bt)^2\). Summing the Taylor inequality about the mean
cancels its linear terms, proving

\[
1\le J=\int_0^1 A(t)e^{-E(t)}\,dt,\quad
A(t)=[a+b(1+\eta/160)t]^8,\quad
E(t)=\frac{4b^2t^2v}{(a+5bt)^2}.
\]

No compactness argument is an input to this finite assertion. On
\(0<\eta\le1/100\), the audited scalar bounds are

\[
1-8\eta\le A<2,\qquad
16(1-19\eta)\eta^2t^2v\le E\le425\eta^2.
\]

Clearing the denominator in the lower bound leaves
\((1045/4)\eta^2+1539\eta^3\ge0\).

The independent checker calculates the *integrated* prefactor as the
complete univariate polynomial

\[
H(\eta)=\sum_{k=0}^8\frac{\binom8k}{k+1}(1-\eta)^{8-k}
[(2\eta-\eta^2)(1+\eta/160)]^k.
\]

It has degree 24 and begins
\(1+(323/60)\eta^2-(1109/120)\eta^3\).
If its coefficients are \(h_k\), exact arithmetic gives

\[
\sum_{k=3}^{24}|h_k|(1/100)^{k-3}<10.
\]

Thus the source's looser cubic remainder \(128\eta^3\) is valid uniformly,
without reusing its pointwise binomial calculation or sampling values of
\(\eta\). Keeping that source constant, \(e^{-E}\le1-E+E^2/2\) gives

\[
1\le J\le1+\frac{323}{60}\eta^2+128\eta^3
-\frac{16}{3}(1-30\eta)\eta^2v+200000\eta^4.
\]

The denominator \(1-30\eta\) is positive and decreasing on the needed
interval; the numerator below is positive and increasing. Hence

\[
v\le\frac{1+3/320+24\eta+37500\eta^2}{1-30\eta}
\le\frac{80751923}{79997600}<\frac54
\quad(0<\eta\le10^{-6}).
\]

The collapsed boundary family has variance \(7/4\), so this excludes its
branch by a finite gap, rather than by a limiting argument.

### Approximate saturation and an independent Newton certificate

Project \(u_j\) to \(U_j=1/2+i\Im u_j\). The projection error above and
product telescoping give errors \(69300\eta\) and \(1871100\eta\) in
\(e_2\) and \(e_3\). For arbitrary real \(t_j\), without symmetry,

\[
\Re e_3(1/2+it_j)=3\Re e_2(1/2+it_j)-14.
\]

The differentiated identities therefore imply a complex saturation error
\(8316000\eta\). For each \(k\)-subset, the phase inequality
\(1-\cos(\sum\theta_j)\le k\sum(1-\cos\theta_j)\) bounds the passage from
complex \(q_j\) to \(r_j\). The \(e_2,e_3\) errors are at most
\(77000\eta,1732500\eta\), respectively. This inequality follows from
telescoping the unit phase factors and Cauchy--Schwarz; its validity does
not require small individually chosen arguments.

Set \(x_j=r_j-1/2\ge0\), \(e=e_1(x)\), \(L=e_2(x)\), \(M=e_3(x)\).
The elementary shift identities give

\[
|M-L|\le10366125\eta<11000000\eta,\qquad
4-1100\eta\le e\le4+\eta/20.
\]

All constants in this chain were checked with exact rational arithmetic.
The needed Newton inequality has the explicit certificate

\[
12L^2-21eM
=\sum_{i<j}(x_i-x_j)^2
\left[\sum_{k\ne i,j}x_k^2+
\sum_{\substack{k<\ell\\k,\ell\ne i,j}}x_kx_\ell\right]\ge0.
\]

The source expands the full eight-variable sparse polynomial. This
review independently certifies the universal identity using symmetry
and homogeneity. The space of symmetric homogeneous degree-four
polynomials has five monomial-orbit basis elements, with partitions
\(4,31,22,211,1111\). Evaluations at
\((1,0,\ldots),(1,1,0,\ldots),(2,1,0,\ldots),
(1,1,1,0,\ldots),(1,1,1,1,0,\ldots)\)
give the orbit evaluation matrix

\[
\begin{pmatrix}
1&0&0&0&0\\
2&2&1&0&0\\
17&10&4&0&0\\
3&6&3&3&0\\
4&12&6&12&1
\end{pmatrix}.
\]

It is invertible. Exact row reduction applied separately to the two
sides recovers the same full coefficient vector \((0,0,12,3,-12)\).
This is a complete polynomial identity certificate in the indicated
space, not a general inference from five samples. Symmetry and degree
four follow directly from the displayed definitions and sum.
The right brackets are nonnegative when \(x_j\ge0\).

The variance identity \(64v=7e^2-16L\), together with \(v<5/4\),
forces \(1<L<8\). Writing \(K=11000000\), the certificate then gives

\[
L(7-L)\le(7/4)(1100)\eta L+8K\eta<90000000\eta.
\]

Division by \(L>1\) gives \(7-L\le90000000\eta\) if \(L\le7\);
when \(L>7\) that conclusion holds directly. Consequently

\[
v<23000000\eta,\quad
\sum|q_j-1|^2=8[v+(\mu-1)^2+2D]<190000000\eta.
\]

Finally \(\zeta_j=-\eta+(q_j-1)/q_j\) and \(r_j>1/2\) yield

\[
Q\le16\eta^2+8\sum|q_j-1|^2<1600000000\eta.
\]

This confirms the quantitative reduction, including the needed strict
and weak inequalities. The original annulus follows by feeding
the resulting \(T\) into the source's relaxed local margin. That
change of hypothesis was checked explicitly, as developed next.

## Strengthening and improvement opportunities

### Proved: a wider explicit annulus with the same slope

The preceding
[independent local review](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_first_power_review3/README.md),
source commit 3aa9e97d0605ad785fae45b8a4fd32b2dd5b3a1e, graph review
bafkreif77tc64bty5cvzxegbhuralrjtqv6bxkna2shndr5zfumtt6rqdu,
proves an absolutely convergent complex-binomial remainder. For
\(a\ge3/4,T\le1/100\), it gives, with \(S=\sum\zeta_j\),
\(s=|S|\), \(X=\sum(\Re\zeta_j)^2\), \(Q=\sum|\zeta_j|^2\),

\[
F=\frac8a+\frac{\Re S}{a^2}+\frac{3X-Q}{2a^3}+R,\qquad
|R|\le4TQ.
\]

Indeed the positive coefficients of \((1-w)^{-1/2}\), convolved with
the conjugate series, sum to one in each total degree. The omitted
degrees contribute at most
\(|\zeta|^3/[a^4(1-|\zeta|/a)]\le(3200/999)|\zeta|^3<4|\zeta|^3\).

Under the *relaxed* failure \(F\le8+\eta/20\), this expansion implies

\[
(8-1/20)\eta\le2s+4Q,\qquad
\eta\le s/3+2Q/3\le3T.
\]

The coefficient integration and Schur bounds in the previous review
depend on this last condition, \(a\ge3/4\), and \(T\le1/100\), rather
than on the stronger sum assumption. They therefore remain applicable:

\[
\Re S\ge s/16-8\eta-(4/7)\Re\sum\zeta_j^2-60Ts-58TQ.
\]

Using \(a^{-2}-1\le4\eta\), \(a^{-3}-1\le8\eta\) and
\(|3X-Q|\le2Q\) in the improved expansion gives

\[
F-8\ge8\eta+\Re S+(3X-Q)/2-12Ts-28TQ
\ge(1/16-72T)s+(1/14-86T)Q.
\]

At \(T_*=11/25000\), the two coefficients are

\[
A_*=\frac{1541}{50000}>\frac1{60},\qquad
B_*=\frac{2939}{87500}>\frac1{30};
\]

their exact excesses are \(2123/150000\) and \(67/262500\).
They decrease with \(T\), so for \(T\le T_*\),

\[
F-8>s/60+Q/30=(s/3+2Q/3)/20\ge\eta/20.
\]

The strict step holds because \(\eta>0\) forces \(s+Q>0\) through the
coarse failure inequality. This contradicts the relaxed failure.
If \(a<3/4\), then
\(F\ge8/(a+T)>8/(3/4+T_*)>8+1/20\ge8+\eta/20\),
or \(F\) is infinite. Thus every interior root of a polynomial with
\(T\le T_*\) has the asserted margin.

Now suppose a failure had \(0<\eta\le121/10^{18}\).
This lies within the audited stability domain. Its quantitative reduction
would imply

\[
T^2\le Q\le1600000000\eta
\le\frac{121}{625000000}=T_*^2.
\]

Hence \(T\le T_*\), contradicting the just-proved local margin.
This proves the closed inner endpoint of the refined annulus.
The earlier \(T\le1/1250\) *zero-slope* refinement cannot simply be
substituted here: the required positive slope needs the weighted
thresholds \(A>1/60,B>1/30\) established above.

### Further consequential directions, not proved here

The effective critical-energy rate is now available without qualitative
compactness. A useful next bridge would combine it with the stronger
cube-root/Schwarz--Pick local coercivity from the separate linear-margin
lane, with all auxiliary constants made explicit. In particular
[six-reviewer-2's separate review](https://github.com/helgithorskarp/math_results/blob/main/sendov_degree9_first_power_boundary_review2/README.md),
graph reference bafkreifcg466t2daggji5ayntz26c2ln63iwvbmg5grob33neknqlthxh4,
proves slope \(14/5\) with an existential radius. That could produce an
explicit annulus with a substantially larger slope. This review does not
verify that additional bridge or transfer its existential radius to a
numerical one.

The quantitative proof has several loose bounds, but optimizing constants
alone does not address the remaining root-modulus range. A materially
stronger advance would extend the stability domain or obtain a two-family
near-equality theorem with nonzero excess. Either requires a new finite
reduction, not just invoking compactness. Generalizing the approximate
Newton relation to other degrees also requires tracking the shifted
coefficients; the degree-nine relation \(M\approx L\) was essential here.

## Primary literature, novelty and readiness

[Zhang, arXiv:2609.19126](https://arxiv.org/html/2609.19126), Conjecture 1.2,
still states the first-power endpoint; Theorem 1.3 proves the quadratic
case. A second-power lower bound does not imply this first-power lower
bound. The reciprocal identity is classical; compare
[Tang--Zhang, equation (5.1)](https://arxiv.org/html/2508.10341v3).
[Tao's August exposition](https://terrytao.wordpress.com/2026/08/12/a-digestion-of-the-proof-of-sendovs-conjecture/),
Lemma 6(ii), supplies the polar identity and reports the original
all-degree Sendov result. No external formalization was rebuilt here.

The primary full text of
[Kasmalkar (2014)](https://ajmaa.org/searchroot/files/pdf/v11n1/v11i1p4.pdf)
was obtained for a bounded comparison of Theorem A and the standing
hypothesis preceding Lemmas 1--2. Theorem A concludes existence of one
nearby critical point. Its contradiction hypothesis imposes a lower
distance bound on **every** critical point. Its concentration lemma uses
that pointwise condition. Neither the theorem nor this inspected reduction
by itself supplies the present aggregate first-power implication.
This is a scope comparison, not a full re-audit of the older proof.
The McCoy 1998 full text remains unavailable from the direct publisher
request; its indexed abstract concerns the original existence assertion.

Candidate-specific primary searches found no duplicate of this exact
effective first-power claim. That supports potential novelty, not
historical priority. Standard identities, Gauss--Lucas, Schur/Rouche,
Maclaurin, Newton and logarithmic strong concavity are inherited tools.
The consequential target contribution is their finite quantitative
combination; this independent review confirms it and supplies an explicit
stronger bridge. Correctness is ready for use as an ordinary lemma.
Priority, the middle root-modulus range and stronger slopes remain separate.

## Reproduction and trust boundary

From the repository root:

    python3 sendov_degree9_effective_boundary_review3/audit.py

Python 3.11 or later, standard library only. The exact output is
[expected.json](expected.json): **65 checks**, a complete Newton identity
certificate in five symmetric basis coordinates, the full degree-24
integrated polar polynomial, uniform rational bounds and the refined
annulus endpoint. Three deliberately altered certificates or constants
are rejected. The code imports no target source, data or computed roots.
Binomial and collapsed families provide exact positive controls; they are
not an exhaustive search over polynomials.

The original checker was also replayed from its verified source commit:
**331 exact checks**, including its full sparse Newton identity and
mutation rejection. Original checker SHA256:
e18173217f5ead0d57838eb07c6d527ad8aad77ef2bca04eb5709970bfe47379.
The independent run used CPython 3.11.2, one process and one thread:
0.074 seconds and 18,856 KiB peak child RSS. The graph contribution records
the verified publication commit and checker/output hashes separately.

The universal analytic steps remain ordinary written mathematics:
root containment, polar integration, strong concavity, the exponential
inequality, Schur/Rouche and convergence of the local binomial series.
The finite algebra checks and written audit establish the stated scope;
no proof-assistant verification, floating-point root solver, unbounded
enumeration, external proof import or private certificate is claimed.
The qualitative concentration theorem is not a premise of the effective
reduction. The local coefficient/Schur dependency was audited in the prior
review and its relaxed-hypothesis use is explicitly justified here.
