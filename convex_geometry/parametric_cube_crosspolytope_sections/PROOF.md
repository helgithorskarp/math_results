# All-order asymptotics for a parametric family of diagonal sections

## 1. Statement

Let

\[
g(x)=(|x|-1)_+,
\qquad H_N=\{x\in\mathbb R^N:\textstyle\sum_i x_i=0\}.
\]

For \(\rho>0\), define

\[
\begin{aligned}
A_N(\rho)
&=\int_{\mathbb R^N}\delta\!\left(\sum_i x_i\right)
  \mathbf1_{\{\sum_i g(x_i)\leq \rho N\}}\,dx\\
&=\frac1{\sqrt N}
  \left|\left([-1,1]^N+\rho N B_1^N\right)\cap H_N\right|_{N-1},
\end{aligned}                                                   \tag{1}
\]

and, for \(N=n+1\),

\[
D_n(\rho)=\frac{n!}{N^n}A_N(\rho).                            \tag{2}
\]

Let \(r=r(\rho)>0\) be determined by

\[
\rho=\frac1{r(r+1)},\qquad
r=\frac{\sqrt{1+4/\rho}-1}{2},                               \tag{3}
\]

and set

\[
P=r^3+3r^2+6r+6,quad
v=\frac{P}{3r^2(r+1)},quad
w=\frac{2r+1}{r^2(r+1)^2},                                  \tag{4}
\]

\[
\beta(r)=\frac{2(r+1)}r\exp\!\left(-\frac r{r+1}\right),
\qquad
\kappa(r)=\frac{\beta(r)}{r\sqrt{2\pi v w}}.               \tag{5}
\]

**Theorem 1.** There are rational functions \(\gamma_j(r)\in\mathbb Q(r)\),
with \(\gamma_0=1\), such that for every fixed integer \(J\geq0\),

\[
D_n(\rho)=\kappa(r)\frac{\beta(r)^n}{\sqrt n}
 \left(\sum_{j=0}^J\frac{\gamma_j(r)}{n^j}+o(n^{-J})\right). \tag{6}
\]

The expansion is locally uniform in \(\rho\): for every compact
\(I\subset(0,\infty)\), the remainder after division by the leading
factor is \(o(n^{-J})\) uniformly for \(\rho\in I\).

The first relative correction is

\[
\boxed{
\gamma_1(r)=\frac{
30r^{10}+28r^9+150r^8+918r^7-873r^6-9504r^5
-18045r^4-16740r^3-8370r^2-2160r-270}
{60(2r+1)^3(r^3+3r^2+6r+6)^2}.}                             \tag{7}
\]

No uniformity as \(\rho\downarrow0\) or \(\rho\to\infty\), convergence
of the infinite formal series, or effective threshold is claimed.

## 2. The general saddle and its nonsingular covariance

For \(r>0\), put

\[
Z(r)=\int_{\mathbb R}e^{-r g(x)}\,dx=\frac{2(r+1)}r,
\qquad f_r(x)=Z(r)^{-1}e^{-r g(x)}.                          \tag{8}
\]

If \(Y\) has density \(f_r\), and \(G=g(Y)\), its exact mixture law is

\[
\begin{array}{c|c|c}
\text{label}&(Y,G)&\text{probability}\\ \hline
0&(V,0),\quad V\sim\mathrm{Unif}[-1,1]&r/(r+1)\\
+&(1+E,E),\quad E\sim\mathrm{Exp}(r)&1/[2(r+1)]\\
-&(-1-E,E),\quad E\sim\mathrm{Exp}(r)&1/[2(r+1)].
\end{array}                                                  \tag{9}
\]

Consequently

\[
\mathbb EY=0,\qquad \mathbb EG=\frac1{r(r+1)}=\rho,
\qquad \operatorname{Cov}(Y,G)=0,                           \tag{10}
\]

and direct integration gives the positive variances (4). Thus (3) is
exactly the saddle equation. Both variances are bounded above and away from
zero when \(\rho\) ranges over a compact subset of \((0,\infty)\).

Let \(Q=G-\rho\). All joint moments of \((Y,Q)\) are rational functions
of \(r\), and its moment-generating function is analytic on a neighborhood
whose size can be chosen uniformly for \(r\) in a compact positive
interval.

## 3. A parameter-uniform local expansion

Let \(p_{M,r}(s,t)\) denote the convolution version of the density of the
absolutely continuous part of the sum of \(M\) independent copies of
\((Y,G)\). We claim that for every fixed \(J\),

\[
M p_{M,r}(0,\rho M-u)=\frac1{2\pi\sqrt{vw}}
 \left(\sum_{j=0}^J\frac{P_j(r,u)}{M^j}+o(M^{-J})\right),   \tag{11}
\]

where \(P_0=1\), every \(P_j\) is a polynomial in \(u\) with coefficients
in \(\mathbb Q(r)\), and the expansion is uniform for \(\rho\) in a fixed
compact subset of \((0,\infty)\) and \(0\leq u\leq C_J\log M\).

Here is the density argument, including the singular one-step law. On a
compact parameter interval, all three label probabilities in (9) are
bounded away from zero. Fix \(\epsilon>0\) below the minimum positive-tail
probability, and retain label strings having at least \(\epsilon M\) plus
and \(\epsilon M\) minus labels. A Chernoff bound, uniform on the parameter
interval, makes the omitted probability \(O(e^{-cM})\). Every non-pure
omitted convolution has a planar density bounded by a parameter-uniform
constant: first convolve two different line types and then convolve the
remaining probability measures. Hence the omitted absolutely continuous
density is uniformly \(O(e^{-cM})\).

The conditional Fourier transform of every retained string satisfies

\[
\left(1+\frac{(\xi+\eta)^2}{r^2}\right)^{-\epsilon M/2}
\left(1+\frac{(\eta-\xi)^2}{r^2}\right)^{-\epsilon M/2}.    \tag{12}
\]

This bound is integrable and has an exponentially small integral outside
a fixed raw-frequency neighborhood, uniformly for the allowed \(r\).
The retained characteristic function differs uniformly from the full
i.i.d. characteristic function by \(O(e^{-cM})\), so this difference also
has exponentially small integral on every polynomially growing window.

After covariance standardization, the logarithm of the full characteristic
function has a Taylor expansion of arbitrary fixed order, uniformly in the
parameter. On \(|t|\leq c\sqrt{\log M}\), expand
\(M\log\phi_r(t/\sqrt M)\) and its exponential far enough to make the
integrated remainder \(o(M^{-J})\). Between that ball and a fixed multiple
of \(\sqrt M\), the uniform negative quadratic real part gives an arbitrary
inverse power of \(M\); beyond it, (12) gives exponential decay. Fourier
inversion proves the arbitrary-order local density expansion.

At first standardized coordinate zero, reflection \(Y\mapsto-Y\) kills all
cumulants with odd first index. The total Hermite parity then forces every
surviving power of \(M^{-1/2}\) to be even. The corresponding powers of
\(v\) and \(w\) are integral, so the coefficients are rational functions
of \(r\). Taylor expansion at the second standardized coordinate
\(-u/\sqrt{Mw}\) proves (11).

## 4. Slack integration and normalization

The product change of measure gives the exact identity

\[
A_M(\rho)=2^M u_M(0)+Z(r)^M e^{r\rho M}
 \int_0^{\rho M}e^{-ru}p_{M,r}(0,\rho M-u)\,du,             \tag{13}
\]

where \(u_M\) is the density of a sum of \(M\) independent uniform
\([-1,1]\) variables. The same retained-label Fourier estimate gives the
global bound \(\sup p_{M,r}\leq C/M\), uniformly on compact parameter
intervals.

Choose \(C_J\) in (11) large enough that the part of (13) above
\(C_J\log M\) is smaller than the leading term by \(o(M^{-J})\). Insert
(11) below the cutoff and integrate termwise. Every coefficient remains in
\(\mathbb Q(r)\) because

\[
r\int_0^\infty e^{-ru}u^k\,du=\frac{k!}{r^k}.              \tag{14}
\]

The cube term is exponentially smaller: using \(r\rho=1/(r+1)\),

\[
\frac{Z(r)e^{r\rho}}2=\frac{r+1}{r}e^{1/(r+1)}>1,          \tag{15}
\]

uniformly away from the parameter endpoints. Therefore

\[
A_M(\rho)=\frac{[Z(r)e^{1/(r+1)}]^M}{2\pi rM\sqrt{vw}}
 \left(\sum_{j=0}^J\frac{a_j(r)}{M^j}+o(M^{-J})\right),    \tag{16}
\]

with \(a_0=1\) and \(a_j\in\mathbb Q(r)\), locally uniformly in \(\rho\).
Stirling's full expansion and \(M=N=n+1\) convert (16) into (6), with
(5).

## 5. The first correction

Write \(K_{ab}=\operatorname{cum}(Y^a,Q^b)\). Through relative order
\(M^{-1}\), all inputs can be obtained without integration. For odd \(a\),
reflection gives \(\mathbb E[Y^aQ^b]=0\); for even \(a\), (9) gives

\[
\mathbb E[Y^aQ^b]
=\frac{r(-\rho)^b}{(r+1)(a+1)}
 +\frac1{r+1}\sum_{i=0}^a\sum_{j=0}^b
 \binom ai\binom bj(-\rho)^{b-j}\frac{(i+j)!}{r^{i+j}}.    \tag{17}
\]

The moment--cumulant relation gives the required \(K_{ab}\) as rational
functions. The constant part of the two-dimensional Edgeworth polynomial is

\[
Q_0=\frac{K_{40}}{8v^2}+\frac{K_{22}}{4vw}+\frac{K_{04}}{8w^2}
-\frac{3K_{21}^2}{8v^2w}-\frac{K_{21}K_{03}}{4vw^2}
-\frac{5K_{03}^2}{24w^3}.                                 \tag{18}
\]

Evaluation at \((0,-u/\sqrt{Mw})\), including the Gaussian factor, gives
the relative density correction

\[
Q_0+\left(\frac{K_{21}}{2vw}+\frac{K_{03}}{2w^2}\right)u
-\frac{u^2}{2w}.                                           \tag{19}
\]

Consequently

\[
a_1=Q_0+\frac{K_{21}}{2vwr}+\frac{K_{03}}{2w^2r}
-\frac1{wr^2},\qquad \gamma_1=a_1-\frac5{12}.             \tag{20}
\]

The exact rational-function computation in [verify.py](verify.py) derives
each required cumulant both from set partitions and from a distinguished-slot
recursion. Reduction of (20) gives (7).

When \(\rho=1\), equation (3) becomes \(r^2+r=1\). Equations (4)--(7)
reduce to the earlier sharp simplex constants

\[
v=\frac{13+8r}{3},\quad w=1+2r,\quad
\gamma_1=-\frac{237}{20}+\frac{284}{15}r.                  \tag{21}
\]

Thus Theorem 1 genuinely extends the preceding single-radius theorem.

## 6. Trust boundary

The exact checker verifies the mixture algebra, cumulants, rational
simplification, specialization (21), and selected exact finite sections.
Those computations do not prove the asymptotic remainder. The universal
statement rests on the parameter-uniform retained-label Fourier estimates,
arbitrary-order Taylor expansion, slack-tail bound, and Stirling expansion
above. There is no formal proof, independent peer review, effective
threshold, or claim about the singular limits \(\rho=0,\infty\).
