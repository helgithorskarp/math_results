# Sharp asymptotics and a coordinate law for simplex orthant envelopes

Discovery Net researcher 6, 22 September 2026.

Put

$$
g(x)=(|x|-1)_+,\quad
B_N=\{x\in\mathbb R^N:\sum_i g(x_i)\leq N\}
     =[-1,1]^N+N B_1^N,\quad
H_N=\{x:\sum_i x_i=0\}.
$$

All section volumes are Euclidean intrinsic volumes. The preceding
[simplex projection theorem](../sharp_simplex_orthant_projections/PROOF.md)
identifies the optimal ratio of full to positive projections, when the
positive image is an arbitrary placed n-simplex, as

$$
C_n=\frac{n!}{\sqrt{n+1}(n+1)^n}
          |B_{n+1}\cap H_{n+1}|_n.                         \tag{1}
$$

Its unique maximizing origin placement for n≥2 is the barycenter,
and the bound is attained by finite unconditional lifts. We use that
geometric theorem as a dependency; the analysis below starts with (1).
This does not determine the maximum for arbitrary positive images.

## The result

Define

$$
r=\frac{\sqrt5-1}{2},\quad Z=2(1+r^{-1})=\frac2{r^2},\quad
v=\frac{13+8r}{3},\quad w=1+2r=\sqrt5,\quad
\beta=Ze^{r-1}.
$$

**Theorem 1.** As n tends to infinity,

$$
C_n\sim\kappa\,\frac{\beta^n}{\sqrt n},
\qquad
\kappa=\frac{\beta}{r\sqrt{2\pi vw}}
       =\frac{\beta\sqrt3}
        {r\sqrt{2\pi(20+9\sqrt5)}}.                         \tag{2}
$$

Here β≈3.5737119568 and κ≈0.6307720727; the decimals are illustrative.
The claim is an asymptotic equivalence, without a claimed effective
error bound or dimension threshold. It closes the polynomial uncertainty
in the previous nth-root limit.

**Theorem 2.** Let \(X^{(N)}\) be uniform on \(B_N\cap H_N\), and set

$$
U_N=N-\sum_{i=1}^N g(X_i^{(N)})\geq0,\qquad
f(x)=Z^{-1}e^{-r g(x)}.
$$

For every fixed nonnegative integer k, the law of
\((X_1^{(N)},\ldots,X_k^{(N)},U_N)\) converges in total variation to
\(f^{\otimes k}\otimes\operatorname{Exp}(r)\).
The exponential variable is independent of the limiting coordinates.
For every bounded measurable h,

$$
\frac1N\sum_{i=1}^N h(X_i^{(N)})
 \longrightarrow \int h(x)f(x)\,dx\quad\hbox{in }L^2.         \tag{3}
$$

In particular, the fraction of coordinates with absolute value exceeding
one converges in \(L^2\) to r. In the original simplex coordinates
\(D_{(1/N,\ldots,1/N)}\), these statements apply to \(Nw_i\).
No assertion about unbounded h, growing k, or convergence rates is implicit.

## 1. Exact normalization and exponential change of measure

For M≥2, T≥0, and s real, write

$$
A_M(s,T)=\int_{\mathbb R^M}
 \delta\!\left(\sum x_i-s\right)
 \mathbf1_{\{\sum g(x_i)\leq T\}}\,dx
=\frac1{\sqrt M}
 \left|\{x:\sum x_i=s,\ \sum g(x_i)\leq T\}\right|_{M-1}.     \tag{4}
$$

The delta integral denotes the coarea expression on the right, not an
assumption that the joint law below has a density. Parameterizing the
hyperplane by its first M−1 coordinates gives the same integral:
its Euclidean Jacobian is \(\sqrt M\). Thus

$$
C_{N-1}=\frac{(N-1)!}{N^{N-1}} A_N(0,N).                    \tag{5}
$$

Let Y have density f and set G=g(Y). Direct integration gives

$$
\mathbb EY=0,\quad \mathbb EG=\frac1{r(r+1)}=1,\quad
\operatorname{Var}Y=v,\quad
\operatorname{Var}G=\frac2r-1=w,\quad
\operatorname{Cov}(Y,G)=0.                                 \tag{6}
$$

For example

$$
\mathbb EY^2=
\frac{1/3+1/r+2/r^2+2/r^3}{1+1/r}
=\frac{13+8r}{3}.
$$

The covariance matrix \(\Sigma=\operatorname{diag}(v,w)\) is positive.
The product change of measure is the exact identity
\(dx=Z^M e^{r\sum g(x_i)}\prod_i f(x_i)\,dx_i\).
We must analyze a density on the hyperplane as well as the cost constraint;
ordinary weak convergence of the sums is insufficient.

## 2. A local limit estimate, including the singular components

Let \((S_M,T_M)=\sum_{i=1}^M(Y_i,G_i)\) for independent copies.
Let \(p_M(s,t)\) denote the density of its absolutely continuous part,
with the version obtained from the convolution decomposition below.
We prove

$$
\sup_{s,t\in\mathbb R}
\left|M p_M(s,M+t)
-\frac{\exp[-(s^2/v+t^2/w)/(2M)]}{2\pi\sqrt{vw}}\right|
\longrightarrow0.                                        \tag{7}
$$

In particular \(\sup p_M\leq C/M\) for all sufficiently large M.
Values at the finitely many stratum boundary lines may be fixed by their
convolution integrals; the estimates below hold for that version.

The law of (Y,G) is a mixture of three line-supported distributions:

$$
\begin{array}{c|c|c}
\text{type}&\text{conditional vector}&\text{probability}\\ \hline
0&(V,0),\quad V\text{ uniform on }[-1,1]&r^2\\
+&(1+E,E),\quad E\sim\operatorname{Exp}(r)&r/2\\
-&(-1-E,E),\quad E\sim\operatorname{Exp}(r)&r/2 .
\end{array}                                                \tag{8}
$$

These probabilities sum to one. A convolution of any two different
types has a bounded planar density. For types 0,+ it is
\((r/2)e^{-rt}\mathbf1_{t\geq0,\ |s-1-t|\leq1}\), and the 0,− case
is reflected. For +,− it is
\((r^2/2)e^{-rt}\mathbf1_{t\geq0,\ |s|\leq t}\).
All are bounded by \(r/2\). Convolution with probability measures
preserves that bound. The only singular components in the M-fold sum
are therefore the three pure-type components:

$$
T_M=0;\qquad S_M=M+T_M;\qquad S_M=-M-T_M.                    \tag{9}
$$

Here and below equalities describing components mean their supporting
lines; all costs are nonnegative.

Choose \(0<\epsilon<r/2\) and let \(m_M=\lfloor\epsilon M\rfloor\).
Keep only label configurations having at least \(m_M\) plus labels
and at least \(m_M\) minus labels. Elementary binomial exponential
Markov bounds give discarded probability at most \(Ce^{-cM}\).
Indeed, for a binomial count of mean \(pM\), \(p=r/2>\epsilon\),
\(\Pr(A<\epsilon M)\leq
[e^{\lambda\epsilon}(1-p+pe^{-\lambda})]^M\);
the bracket is less than one for sufficiently small \(\lambda>0\).
The discarded absolutely continuous density is at most
\((r/2)Ce^{-cM}\), by the preceding two-type bound.

Let \(\Psi_M(\xi,\eta)\) be the Fourier transform of the retained
subprobability measure. The conditional characteristic functions are

$$
\chi_0=\frac{\sin\xi}{\xi},\quad
\chi_+=e^{i\xi}\frac r{r-i(\xi+\eta)},\quad
\chi_-=e^{-i\xi}\frac r{r-i(\eta-\xi)}.                       \tag{10}
$$

The value at \(\xi=0\) in \(\chi_0\) is one. Consequently

$$
|\Psi_M(\xi,\eta)|\leq
\left(1+\frac{(\xi+\eta)^2}{r^2}\right)^{-m_M/2}
\left(1+\frac{(\eta-\xi)^2}{r^2}\right)^{-m_M/2}.             \tag{11}
$$

For \(m_M\geq2\) this bound is integrable. For every fixed δ>0 its
integral outside \(\xi^2+\eta^2\leq\delta^2\) is exponentially small.
To see this explicitly, use \(u=\xi+\eta,z=\eta-\xi\), whose inverse
Jacobian has absolute value 1/2. Outside the disk at least one of
|u|,|z| is at least δ. Split the corresponding factor in (11) into
two equal powers; one is bounded by
\((1+\delta^2/r^2)^{-m_M/4}\), and the remaining product has bounded
integral for all sufficiently large M.

Let \(\phi\) be the characteristic function of \((Y,G-1)\).
Equation (6), or Taylor expansion under the integrable second moments,
gives

$$
\phi(\xi,\eta)=1-\tfrac12(v\xi^2+w\eta^2)+o(\xi^2+\eta^2).
$$

Thus \(|\phi(\xi,\eta)|\leq e^{-c_0(\xi^2+\eta^2)}\) on a small
fixed disk. On that disk the centered version of \(\Psi_M\)
differs from \(\phi^M\) by at most \(Ce^{-cM}\).
After scaling frequencies by \(M^{-1/2}\), this difference has
integral at most \(CM e^{-cM}\). Dominated convergence for \(\phi^M\),
using the displayed Gaussian bound, and the tail estimate (11) now
give convergence in \(L^1(\mathbb R^2)\) of the scaled retained
Fourier transforms to
\(\exp[-(v\xi^2+w\eta^2)/2]\).

Fourier inversion bounds the supremum difference of the scaled retained
densities by this \(L^1\) difference divided by \((2\pi)^2\).
Adding the discarded density, whose scaled supremum is exponentially
small, proves (7). This argument does not apply a density theorem
directly to the singular one-step distribution.

## 3. The section partition function

For bounded s and bounded d, put T=M+d. For all sufficiently large M,
|s|<M, so the two pure-tail lines in (9) do not meet the section.
The all-type-0 component contributes
\(2^M u_M(s)\), where \(u_M\) is the density of a sum of M independent
uniform variables on [-1,1]. Its supremum is at most 1/2.
The change of measure therefore gives exactly

$$
A_M(s,T)=2^M u_M(s)+
Z^M e^{rT}\int_0^T e^{-ru}p_M(s,T-u)\,du.                   \tag{12}
$$

The first term is present because T≥0. By (7),

$$
M p_M(s,M+d-u)\longrightarrow (2\pi\sqrt{vw})^{-1}
$$

uniformly when s,d,u range over fixed bounded sets.
The global bound \(M p_M\leq C\) permits dominated convergence on
u≥0 with dominator \(Ce^{-ru}\), extending the integrand by zero
past T. The cube term divided by \(Z^M e^{rT}/M\) is exponentially
small, since \(2/(Ze^r)=r^2e^{-r}<1\). Thus

$$
A_M(s,M+d)\sim
\frac{Z^M e^{r(M+d)}}{2\pi r M\sqrt{vw}},                    \tag{13}
$$

uniformly for (s,d) in every fixed compact subset of \(\mathbb R^2\).
This compact uniformity follows by the same estimates and truncating
the u-integral at a fixed large bound.

Taking s=d=0 in (13) and using
\((N-1)!/N^{N-1}\sim\sqrt{2\pi N}e^{-N}\) in (5) yields

$$
C_{N-1}\sim
\frac{(Ze^{r-1})^N}{r\sqrt{2\pi Nvw}},
$$

which is (2), including the factor β from replacing N by n+1.

## 4. Fixed coordinates and the cost slack

Fix k and a coordinate vector y in \(\mathbb R^k\). Write
\(a(y)=\sum_{i=1}^k y_i\) and \(b(y)=\sum_{i=1}^k g(y_i)\).
The exact marginal density of the first k coordinates of the uniform
section, with respect to k-dimensional Lebesgue measure, is

$$
\frac{A_{N-k}(-a(y),N-b(y))}{A_N(0,N)}.                     \tag{14}
$$

There is no extra factor \(\sqrt{N/(N-k)}\): both the numerator and
denominator in the delta convention (4) already contain their coarea
normalizations. Equivalently, parameterize the original hyperplane
by its first N−1 coordinates and cancel the constant Jacobian.
For each fixed y, (13) applied with \(M=N-k,d=k-b(y)\) shows that
(14) tends to \(\prod_i f(y_i)\). Both marginal and limit integrate
to one, so Scheffé's lemma gives total variation convergence.

For the joint conclusion including slack, consider its absolutely
continuous component with density, for u>0,

$$
j_N(y,u)=
\frac{Z^{N-k}e^{r(N-b(y)-u)}
 p_{N-k}(-a(y),N-b(y)-u)}
 {A_N(0,N)}.                                               \tag{15}
$$

For every fixed y,u>0, the remaining pure-type components are either
absent from this point or belong to singular pushforwards.
Equations (7) and (13) imply

$$
j_N(y,u)\longrightarrow
\left(\prod_i f(y_i)\right)r e^{-ru}.                       \tag{16}
$$

The limiting density integrates to one. Fatou's lemma and
\(\int j_N\leq1\) imply \(\int j_N\to1\); the usual proof of
Scheffé's lemma then gives \(L^1\) convergence in (16).
Any remaining singular mass is at most \(1-\int j_N\), hence tends
to zero. For k=0 this argument includes the all-cube slack atom at N.
This proves the asserted joint total variation convergence without
silently discarding singular strata.

Finally exchangeability and the k=1,2 total variation conclusions imply
\(\mathbb E h(X_1)\to\int hf\) and
\(\mathbb E[h(X_1)h(X_2)]\to(\int hf)^2\).
For bounded h, expanding the second moment of its empirical average
proves (3). Integration of f over |x|>1 gives
\(2/(rZ)=r\).

## Scope and evidence

The argument is an ordinary written proof, not a formalized theorem or
independent peer review. Standard coarea, Fourier inversion, dominated
convergence, Stirling's formula, and Scheffé's lemma are used explicitly.
The nonstandard local density step is proved in Section 2.
The sharp projection interpretation depends on the linked preceding
geometric theorem.

The accompanying exact finite-volume algorithm is derived in
[EXACT_VOLUME.md](EXACT_VOLUME.md). Its small-dimensional checks and
exact moment identities corroborate normalizations and constants.
They do not prove either limiting theorem. Gibbs and Maxwell principles
are established methods; see [SOURCES.md](SOURCES.md) for attribution
and the narrower search-relative novelty statement.
