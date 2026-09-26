# Convex quartic comparisons and finite Hankel positivity at large variance

Status: complete author proofs, not formalized; independent mathematical
review is pending. The dimension-three Gaussian majorisation conjecture
remains open. The constants below are sufficient, not claimed optimal.

## 1. Statements and normalization

Let `mu` be a Borel probability measure supported in a ball `B(a,R)` in
`R^3`, and let `T:R^3 -> R^3` be 1-Lipschitz. For `s>0` put

\[
C=(2\pi s)^{-3/2},\qquad f=\mu*\gamma_s,\qquad
g=(T_\#\mu)*\gamma_s,\qquad \varepsilon=R^2/s.
\tag{1}
\]

Here `gamma_s` has covariance `s I_3`, so `0<f,g<=C`. Define

\[
d_m=C^{1-m}\left(\int g^m-\int f^m\right),\quad
a_j=\frac{d_{j+2}}{(j+1)(j+2)},\quad
\mathsf H_\ell=(a_{i+j})_{i,j=0}^{\ell}.
\tag{2}
\]

**Theorem 1 (all convex quartics).** If

\[
\frac{R^2}{s}\leq \frac{15}{2}\log\frac98,
\tag{3}
\]

then every real polynomial `U` of degree at most four, with `U(0)=0`
and convex on `[0,C]`, satisfies

\[
\int_{\mathbb R^3}U(f)\leq\int_{\mathbb R^3}U(g).
\tag{4}
\]

In particular the rational sufficient condition

\[
\boxed{s\geq\frac{17}{15}R^2}
\tag{5}
\]

implies (4). Under (5), the inequality is strict for every such non-affine
`U` if

\[
D=\mathbb E\big[|X-X'|^2-|T(X)-T(X')|^2\big]>0.
\tag{6}
\]

The integrals in (4) are finite: a polynomial vanishing at zero is
bounded in absolute value by a constant times its argument on `[0,C]`.

**Theorem 2 (uniform positivity at each finite Hankel level).** Set

\[
\mathsf Q_\ell=
\left(\frac{2}{(i+j+2)(i+j+3)(i+j+4)}\right)_{i,j=0}^{\ell},
\qquad K_\ell=\frac38(\ell+1)\operatorname{tr}(\mathsf Q_\ell^{-1}).
\tag{7}
\]

For every integer `ell>=0`, if `s>=K_ell R^2` then `H_ell` is positive
semidefinite. In fact it is positive definite if `D>0`. Thus no negative
square-curvature polynomial certificate of energy degree at most
`2 ell+2` can occur in that range. The first values are

| ell | trace of inverse Q_ell | K_ell |
| ---: | ---: | ---: |
| 0 | 12 | 9/2 |
| 1 | 360 | 270 |
| 2 | 10680 | 12015 |
| 3 | 331380 | 497070 |
| 4 | 10494120 | 19676475 |
| 5 | 335875680 | 755720280 |
| 6 | 10825909920 | 28418013540 |

These are deliberately coarse explicit constants. Theorem 1 is much
stronger at level one. Theorem 2 concerns square-curvature certificates;
it does not by itself classify every polynomial convex only on `[0,C]`.
Its constants are unbounded in `ell`, so it cannot establish all levels
at any one finite value of `s/R^2`.

## 2. The positive weighted replica representation

We reproduce the normalization from the team's
[relative moment-gap theorem](../gaussian_contraction_moment_gaps/PROOF.md),
which builds on the Gaussian replica identity in Aishwarya--Li,
arXiv:2609.07041v2, equation (61). This is a dependency, not a new identity.

Translate input by `a` and output by `T(a)`. Both centered point sets lie
in `B(0,R)`, and all energy integrals are unchanged. Take independent
`X_1,X_2,...` with law `mu`, write `Y_i=T(X_i)`, and put

\[
\Delta_{ij}=|X_i-X_j|^2-|Y_i-Y_j|^2\geq0,\qquad
Z_i(t)=(\sqrt{1-t}\,X_i,\sqrt t\,Y_i)\in\mathbb R^6.
\]

Then `|Z_i(t)|<=R`. Set

\[
Q_m(t)=\sum_{i=1}^m|Z_i(t)-\overline Z_m(t)|^2,
\qquad
B_m=\mathbb E\left[\Delta_{12}\int_0^1e^{-Q_m(t)/(2s)}dt\right].
\tag{8}
\]

Completing the square in a product of `m` Gaussian densities gives

\[
C^{1-m}\int f^m=m^{-3/2}\mathbb E
 \exp\left[-\frac1{2ms}\sum_{i<j}|X_i-X_j|^2\right].
\]

Differentiate the scalar exponential as its pairwise squared distances
interpolate affinely from `X` to `Y`. Each derivative contributes
`sum Delta_ij/(2ms)`. Exchangeability makes the `m(m-1)/2` pair terms
equal, giving

\[
\boxed{d_m=\frac{m-1}{4s\,m^{3/2}}B_m,\qquad
a_j=\frac{B_{j+2}}{4s(j+2)^{5/2}}.}
\tag{9}
\]

All integrands are bounded and nonnegative; bounded support justifies
the differentiation and Fubini, or the integrated scalar identity and
Tonelli give the same formula. No intermediate density in dimension
three is being asserted for the six-dimensional interpolation.

The online variance formula gives

\[
Q_{m+1}=Q_m+\frac{m}{m+1}|Z_{m+1}-\overline Z_m|^2\geq Q_m,
\qquad B_{m+1}\leq B_m.
\tag{10}
\]

If `D=0`, (8) vanishes for every `m`, so all claims about polynomial
energies and Hankel matrices follow immediately. If `D>0`, each `B_m`
is positive. If `R=0`, necessarily `D=0`.

## 3. A two-replica inequality

**Lemma 3.** For every `m>=2`,

\[
\boxed{B_mB_{m+2}\geq
e^{-\varepsilon/(m+1)}B_{m+1}^{\,2}.}
\tag{11}
\]

**Proof.** Fix `t` and the first `m` replicas, with mean `b`. Let the
next two independent replicas be `b+u` and `b+v`, and write
`h=(u-v)/2`, `k=(u+v)/2`. Let `Q_(m+1)^u` and `Q_(m+1)^v` denote the
variance sums formed by adjoining the indicated single point. Direct
expansion of the variance about the old mean gives

\[
\begin{aligned}
&Q_m+Q_{m+2}-Q_{m+1}^u-Q_{m+1}^v\\
&\hspace{8mm}=\frac2{m+1}|h|^2
 -\frac{2m}{(m+1)(m+2)}|k|^2
 \leq\frac{2R^2}{m+1}.
\end{aligned}
\tag{12}
\]

The last step uses `h=(Z_(m+1)-Z_(m+2))/2` and the radius bound.
Exponentiating (12) yields

\[
e^{-Q_{m+2}/(2s)}\geq e^{-\varepsilon/(m+1)}e^{-Q_m/(2s)}
e^{-(Q_{m+1}^u-Q_m)/(2s)}e^{-(Q_{m+1}^v-Q_m)/(2s)}.
\]

Conditional independence of the extra replicas makes the conditional
expectation of the last two factors equal to `r^2`, where

\[
r=r(t,Z_1,\ldots,Z_m)
=\mathbb E\left[e^{-\frac{m}{2(m+1)s}|Z-\overline Z_m|^2}
 \mid t,Z_1,\ldots,Z_m\right].
\]

On the space of `t` and the first `m` original samples use the positive
finite measure

\[
dw=\Delta_{12}e^{-Q_m(t)/(2s)}\,dt\,d\mu^{\otimes m}.
\]

Its total mass is `B_m`, and

\[
B_{m+1}=\int r\,dw,\qquad
B_{m+2}\geq e^{-\varepsilon/(m+1)}\int r^2\,dw.
\]

Cauchy--Schwarz proves (11), including the zero-mass case. QED.

Combining (9) and (11) gives the useful adjacent-minor estimate

\[
a_{m-2}a_m\geq
 e^{-\varepsilon/(m+1)}
 \left(\frac{(m+1)^2}{m(m+2)}\right)^{5/2}a_{m-1}^{\,2}.
\tag{13}
\]

Thus each adjacent `2 by 2` Hankel minor is nonnegative whenever

\[
\varepsilon\leq\frac52(m+1)
 \log\frac{(m+1)^2}{m(m+2)}.
\tag{14}
\]

Positivity of all adjacent minors would not by itself prove positivity
of all Hankel matrices. We use (13) for the level-one matrix only.

## 4. Proof of the quartic theorem and its signed margin

Set

\[
\kappa=e^{-\varepsilon/3}(9/8)^{5/2}.
\]

The case `m=2` of (13) is

\[
a_0a_2\geq\kappa a_1^2.
\tag{15}
\]

Condition (3) is exactly `kappa>=1`, so `H_1` is positive semidefinite.
Moreover (9)--(10) give

\[
a_2\leq(3/4)^{5/2}a_1,
\quad\hbox{hence}\quad a_1-a_2\geq0,
\tag{16}
\]

with strict positivity in (16) when `D>0`.

Normalize an energy by `V(t)=U(Ct)/C`. Its gap is

\[
\int U(g)-\int U(f)=C\int[V(g/C)-V(f/C)].
\]

If `q=V''=q_0+q_1t+q_2t^2`, cancellation of the linear term gives

\[
L(q):=C\int[V(g/C)-V(f/C)]=q_0a_0+q_1a_1+q_2a_2.
\tag{17}
\]

Every quadratic `q>=0` on `[0,1]` can be written

\[
q(t)=\big[\sqrt A(1-t)-\sqrt E\,t\big]^2+c\,t(1-t),
\qquad A=q(0),\ E=q(1),\ c\geq0.
\tag{18}
\]

Indeed the endpoint values match, so the remainder has this form with
`c=q_1+2A+2 sqrt(AE)`. If `A,E>0`, evaluate at the interior zero of
the squared linear expression to obtain `c>=0`. If just one endpoint
value is zero, nonnegativity of the one-sided derivative at that endpoint
gives the same conclusion. If both vanish, `q=c t(1-t)` directly.
Equations (15)--(18) prove (4).

For the rational condition, the elementary positive series

\[
\log\frac98=2\operatorname{arctanh}\frac1{17}
 =2\sum_{j=0}^{\infty}\frac{1}{(2j+1)17^{2j+1}}
 >\frac2{17}+\frac{2}{3\cdot17^3}
\tag{19}
\]

shows that (5) implies

\[
\log\kappa>\frac5{14739},\qquad
\boxed{a_0a_2>\left(1+\frac5{14739}\right)a_1^2\quad(D>0).}
\tag{20}
\]

Consequently `H_1` is positive definite when `D>0`. In (18), either
the squared polynomial is nonzero or `c>0` for nonzero `q`, so (16)
proves the strict part of Theorem 1.

There is also a signed stability estimate for the particularly relevant
globally convex quartics

\[
V_b(t)=\frac{t^4}{12}-\frac{b t^3}{3}+\frac{b^2t^2}{2},
\qquad V_b''(t)=(t-b)^2.
\]

For every real `b`, if `D>0`, their normalized gap satisfies

\[
\begin{aligned}
C\int[V_b(g/C)-V_b(f/C)]
&=a_2-2b a_1+b^2a_0\\
&\geq a_0\left(b-\frac{a_1}{a_0}\right)^2
 +(\kappa-1)\frac{a_1^2}{a_0}.
\end{aligned}
\tag{21}
\]

This is a geometric signed estimate, not an inference from a small
entropy deficit. For `0<b<1`, these energies fail the source's `PC_2`
criterion within the density interval: `t^2 V_b''(t)=t^2(t-b)^2` has
negative derivative for `b/2<t<b`. Thus the quartic theorem covers
energies outside that previously sufficient class.

## 5. Proof of the finite-level theorem

Assume `D>0`. Since all `Z_i(t)` lie in `B(0,R)`,

\[
0\leq Q_m(t)=\sum_i|Z_i(t)|^2-m|\overline Z_m(t)|^2\leq mR^2.
\]

It follows from (8) that

\[
e^{-m\varepsilon/2}\leq B_m/D\leq1.
\tag{22}
\]

Put `delta=D/(4s)`. Formula (9) writes

\[
\mathsf H_\ell/\delta=\mathsf A_\ell+\mathsf E_\ell,
\qquad (\mathsf A_\ell)_{ij}=(i+j+2)^{-5/2}.
\]

Using `1-e^{-x}<=x` in (22), with `m=i+j+2>=2`, gives

\[
|(\mathsf E_\ell)_{ij}|
\leq\frac{\varepsilon}{2m^{3/2}}\leq\frac\varepsilon4,
\qquad
\|\mathsf E_\ell\|_{\mathrm{op}}\leq\frac{\ell+1}{4}\varepsilon.
\tag{23}
\]

The limiting matrix has the moment representation

\[
(\mathsf A_\ell)_{ij}
=\frac1{\Gamma(5/2)}\int_0^1t^{i+j+1}(-\log t)^{3/2}dt.
\tag{24}
\]

Since `Gamma(5/2)=3 sqrt(pi)/4<3/2`, and on `(0,1)` one has
`(-log t)^(3/2)> (1-t)^2`, (24) gives the strict quadratic-form inequality

\[
\mathsf A_\ell\succ\frac23\mathsf Q_\ell\succ0.
\tag{25}
\]

The strictness holds for every nonzero polynomial vector because its
square is positive except at finitely many points. For any positive
definite matrix `Q`,

\[
\lambda_{\min}(Q)\geq\frac1{\operatorname{tr}(Q^{-1})}.
\]

Equations (23)--(25) imply positive definiteness of `H_ell` if

\[
\frac{\ell+1}{4}\varepsilon
\leq\frac{2}{3\operatorname{tr}(\mathsf Q_\ell^{-1})},
\]

which is exactly the condition of Theorem 2, including its boundary.
If `D=0`, the zero matrix already handles the claim.

For completeness, (7) has an exact finite formula, so its constants
require neither numerical eigenvalues nor an uncomputed inverse. The
polynomials

\[
P_k(t)=\sum_{j=0}^{k}(-1)^{k-j}
 \binom{k+1}{j+1}\binom{k+j+3}{j}t^j
\tag{26}
\]

are orthogonal for the weight `t(1-t)^2` on `[0,1]`, with squared norms

\[
N_k=\int_0^1P_k(t)^2t(1-t)^2dt
=\frac{k+1}{2(k+2)(k+3)}.
\tag{27}
\]

One direct verification uses Rodrigues' formula

\[
P_k(t)=\frac{(-1)^k}{k!\,t(1-t)^2}
 \frac{d^k}{dt^k}\big[t^{k+1}(1-t)^{k+2}\big].
\]

Integration by parts `k` times annihilates every polynomial of degree
less than `k`; all boundary terms vanish. The leading coefficient is
`binom(2k+3,k)`, so the norm equals
`binom(2k+3,k) Beta(k+2,k+3)`, which is (27).
Writing the orthonormal coefficient vectors as rows of a matrix `M`
gives `M Q_ell M^T=I`; hence `Q_ell^-1=M^T M`. Therefore

\[
\operatorname{tr}(\mathsf Q_\ell^{-1})=
\sum_{k=0}^{\ell}\frac{2(k+2)(k+3)}{k+1}
 \sum_{j=0}^{k}
 \binom{k+1}{j+1}^{\!2}\binom{k+j+3}{j}^{\!2}.
\tag{28}
\]

This proves the table and the general explicit statement.

## 6. What the result changes, and what it leaves open

The team's [Hankel reduction](../gaussian_majorisation_hankel_transport/PROOF.md)
proves that full majorisation is equivalent to positivity of every
`H_ell`, and identifies the first quartic obstruction
`3 d_2 d_4 >= 2 d_3^2`. Theorem 1 proves that obstruction cannot occur
at (3), uniformly over bounded laws, with no atom-count, paired-rank,
covariance, or near-isometry assumption. Lemma 3 supplies the new
contraction-specific information: positivity of weighted deficits and
the geometry of two extra replicas constrain the curvature of the
moment-gap sequence.

The earlier [entropy bridge obstruction](../gaussian_majorisation_bridge_barrier/PROOF.md)
rules out a geometry-free inference from entropy or pressure comparisons
to all hinges. The present argument retains the distance deficit as a
positive weight and obtains a restricted signed comparison. It does not
reuse the failed fixed common-noise posterior transport construction.

Theorem 2 makes the lack of uniformity precise: for every fixed degree,
sufficiently large variance excludes negative polynomial certificates,
but arbitrarily high degrees remain unaddressed at a fixed variance.
Nor does a high-variance quartic statement supply the all-convex,
small-variance estimates used in Aishwarya--Li's Kneser--Poulsen
implication. No new Kneser--Poulsen case is claimed.

The accompanying checker verifies finite rational identities, the exact
Gram constants, and selected outward-enclosed moment inequalities.
The universal statements follow from the analytic arguments above;
finite checks are normalization and implementation audits, not a proof
by sampling. See [README.md](README.md) for the trust boundary and
[SOURCES.md](SOURCES.md) for dependency attribution.
