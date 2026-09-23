# A first Edgeworth correction for sharp simplex-envelope constants

## 1. Statement and dependency boundary

Put

\[
g(x)=(|x|-1)_+,\quad
B_N=\left\{x\in\mathbb R^N:\sum_{i=1}^N g(x_i)\leq N\right\},\quad
H_N=\left\{x:\sum_i x_i=0\right\}.
\]

The preceding sharp simplex-projection theorem and section analysis give

\[
C_{N-1}=\frac{(N-1)!}{N^{N-1}}A_N(0,N),                 \tag{1}
\]

where

\[
A_M(s,T)=\int_{\mathbb R^M}
 \delta\!\left(\sum x_i-s\right)
 \mathbf 1_{\{\sum g(x_i)\leq T\}}\,dx.                 \tag{2}
\]

The delta notation is the coarea normalization: it is Euclidean section
volume divided by \(\sqrt M\). We take (1), including its geometric
optimality and finite-dimensional attainment, as a dependency.

Let

\[
r=\frac{\sqrt5-1}{2},\quad Z=\frac2{r^2},\quad
v=\frac{13+8r}{3},\quad w=1+2r,
\]

\[
\beta=Ze^{r-1},\qquad
\kappa=\frac{\beta}{r\sqrt{2\pi vw}}.
\]

**Theorem.** As \(n\to\infty\),

\[
C_n=\kappa\frac{\beta^n}{\sqrt n}
 \left(1+\frac{\gamma}{n}+o(n^{-1})\right),              \tag{3}
\]

with

\[
\boxed{\gamma=-\frac{237}{20}+\frac{284}{15}r}
      \approx-0.14855647966865754.                         \tag{4}
\]

Thus (3) is a strict strengthening of the previously proved leading
equivalence. It is not an effective error bound, a full asymptotic series,
or a statement about the unresolved arbitrary-positive-image constant.

## 2. Exact tilted law and cumulants

Let \(Y\) have density

\[
f(y)=Z^{-1}e^{-r g(y)},
\]

and put \(G=g(Y)\), \(Q=G-1\). The pair \((Y,G)\) has the exact mixture

\[
\begin{array}{c|c|c}
\text{label}&(Y,G)&\text{probability}\\ \hline
0&(V,0),\quad V\sim\operatorname{Unif}[-1,1]&r^2\\
+&(1+E,E),\quad E\sim\operatorname{Exp}(r)&r/2\\
-&(-1-E,E),\quad E\sim\operatorname{Exp}(r)&r/2.
\end{array}                                                \tag{5}
\]

Here \(r^2+r=1\). In particular \(\mathbb EY=\mathbb EQ=0\),
\(\mathbb E(YQ)=0\), and

\[
\operatorname{Var}Y=v,\qquad \operatorname{Var}Q=w.       \tag{6}
\]

Only the following centered joint cumulants enter the first correction:

\[
\begin{aligned}
K_{21}&=\operatorname{cum}(Y,Y,Q)
       =\frac{38+22r}{3},&
K_{03}&=\operatorname{cum}(Q,Q,Q)=8,\\
K_{40}&=\operatorname{cum}(Y,Y,Y,Y)
       =\frac{878}{15}+\frac{184}{5}r,&
K_{22}&=\operatorname{cum}(Y,Y,Q,Q)
       =\frac{176+116r}{3},\\
K_{04}&=\operatorname{cum}(Q,Q,Q,Q)=18+36r.               \tag{7}
\end{aligned}
\]

For example, when \(a\) is even,

\[
\mathbb E[Y^aQ^b]
=r^2\frac{(-1)^b}{a+1}
 +r\,\mathbb E[(1+E)^a(E-1)^b],                           \tag{8}
\]

while it is zero for odd \(a\). Since
\(\mathbb E E^j=j!/r^j\), (6)--(7) follow by finite expansion in
\(\mathbb Q(r)\). This also makes every exceptional division explicit:
\(r,v,w\) are positive.

Standardize \(W=(Y/\sqrt v,Q/\sqrt w)\), whose covariance is the identity.
Write \(\lambda_{ab}=K_{ab}/(v^{a/2}w^{b/2})\). Reflection in the first
coordinate kills all cumulants having odd \(a\).

## 3. The tailored local Edgeworth expansion

Let \(p_M(s,t)\) be the density of the absolutely continuous part of
\(\sum_{i=1}^M(Y_i,G_i)\), using the convolution version from (5). We need
the following refinement of the predecessor's local limit lemma.

**Lemma.** Uniformly for \(0\leq u\leq L_M=(3/r)\log M\),

\[
\begin{aligned}
M p_M(0,M-u)
=\frac1{2\pi\sqrt{vw}}\left[1+\frac1M\left(
 Q_0+\frac{\lambda_{21}+\lambda_{03}}{2\sqrt w}u
 -\frac{u^2}{2w}\right)+o(M^{-1})\right],                \tag{9}
\end{aligned}
\]

where the \(o(M^{-1})\) is uniform on the displayed interval and

\[
Q_0=\frac{K_{40}}{8v^2}+\frac{K_{22}}{4vw}
    +\frac{K_{04}}{8w^2}
    -\frac{3K_{21}^2}{8v^2w}
    -\frac{K_{21}K_{03}}{4vw^2}
    -\frac{5K_{03}^2}{24w^3}.                             \tag{10}
\]

**Proof.** We include the density argument because the law in (5) is
singular and a density Edgeworth theorem cannot be invoked at one step.
Fix \(0<\epsilon<r/2\), and retain label strings having at least
\(\epsilon M\) plus labels and at least \(\epsilon M\) minus labels.
Binomial exponential bounds make the discarded label mass \(O(e^{-cM})\).
Every non-pure discarded convolution has planar density bounded by \(r/2\):
convolve one pair of different line types first, and then convolve with
probability measures. Hence its discarded absolutely continuous density is
also \(O(e^{-cM})\), uniformly.

For retained strings, the characteristic-function bound from the two tail
types is

\[
\left(1+\frac{(\xi+\eta)^2}{r^2}\right)^{-\epsilon M/2}
\left(1+\frac{(\eta-\xi)^2}{r^2}\right)^{-\epsilon M/2}.  \tag{11}
\]

It is integrable and has exponentially small integral outside every fixed
neighborhood of the origin. Near the origin the full standardized
characteristic function \(\phi\) has, with multi-index notation,

\[
\log\phi(t)=-\frac{|t|^2}{2}
 +\sum_{|\alpha|=3}\frac{\lambda_\alpha(it)^\alpha}{\alpha!}
 +\sum_{|\alpha|=4}\frac{\lambda_\alpha(it)^\alpha}{\alpha!}
 +O(|t|^5).                                                \tag{12}
\]

All moments exist in a neighborhood of zero by (5). Apply (12) to
\(\phi(t/\sqrt M)^M\), expand the exponential through order \(M^{-1}\),
and invert. On \(|t|\leq c\sqrt{\log M}\) the integrated remainder is
\(O((\log M)^A M^{-3/2})=o(M^{-1})\) for a fixed \(A\). Between that ball
and a fixed multiple of \(\sqrt M\), the quadratic real-part bound in
(12) gives an arbitrarily high negative power of \(M\); beyond it, (11)
gives an exponential bound. The retained/full difference contributes only
an exponentially small Fourier integral. These estimates remain uniform
when the inversion point has norm \(O(\log M/\sqrt M)\).

Consequently the density \(q_M\) of the standardized sum, at every point
away from the three pure support lines, has

\[
q_M(z)=\varphi_2(z)\left[1+M^{-1/2}P_1(z)+M^{-1}P_2(z)
 +o(M^{-1})\right],                                      \tag{13}
\]

uniformly in the range just stated. Here \(\varphi_2\) is the standard
two-dimensional Gaussian density and, with probabilists' Hermite
polynomials,

\[
P_1(z)=\frac{\lambda_{21}}2H_2(z_1)H_1(z_2)
       +\frac{\lambda_{03}}6H_3(z_2).                     \tag{14}
\]

At the origin, the fourth-cumulant part of \(P_2\) is

\[
\frac{\lambda_{40}}8+\frac{\lambda_{22}}4
 +\frac{\lambda_{04}}8,
\]

and half the square of the cubic term contributes

\[
-\frac{3\lambda_{21}^2}{8}
-\frac{\lambda_{21}\lambda_{03}}4
-\frac{5\lambda_{03}^2}{24}.                             \tag{15}
\]

Indeed \(H_2(0)=-1\), \(H_4(0)=3\), and \(H_6(0)=-15\).
Equations (10) and (15) agree after undoing the standardization.

Now evaluate (13) at
\(z=(0,-u/\sqrt{Mw})\). Uniformly for \(u\leq L_M\),

\[
\varphi_2(z)=\frac1{2\pi}
 \left(1-\frac{u^2}{2Mw}+o(M^{-1})\right),
\]

\[
M^{-1/2}P_1(z)=
 \frac{\lambda_{21}+\lambda_{03}}{2M\sqrt w}u+o(M^{-1}),
\]

and \(M^{-1}P_2(z)=M^{-1}Q_0+o(M^{-1})\). Finally

\[
p_M(0,M-u)=\frac{q_M(z)}{M\sqrt{vw}},
\]

which proves (9). The three pure components do not meet this point for
large \(M\): the cube component has total cost zero, and the two pure-tail
components have nonzero sum coordinate. \(\square\)

## 4. Integrating the slack

The exact change of measure is

\[
A_M(0,M)=2^M u_M(0)
 +Z^Me^{rM}\int_0^M e^{-ru}p_M(0,M-u)\,du,                \tag{16}
\]

where \(u_M\) is the density of a sum of \(M\) independent uniform
\([-1,1]\) variables. The cube term is exponentially smaller than the
second term because \(2/(Ze^r)<1\).

The predecessor's Fourier argument gives the global bound
\(\sup p_M\leq C/M\). Therefore the part of the integral above
\(L_M=(3/r)\log M\) is \(O(M^{-4})\). Integrating (9) on the remaining
interval, then extending its elementary exponential moments to infinity,
gives

\[
A_M(0,M)=\frac{(Ze^r)^M}{2\pi rM\sqrt{vw}}
 \left(1+\frac{a}{M}+o(M^{-1})\right),                    \tag{17}
\]

where

\[
a=Q_0+\frac{K_{21}}{2vwr}+\frac{K_{03}}{2w^2r}
       -\frac1{wr^2}.                                     \tag{18}
\]

The three extra terms are respectively the mean of the linear term in
\(u\), the other standardized cubic contribution, and the mean of
\(-u^2/(2w)\) under \(\operatorname{Exp}(r)\). Exact reduction using
\(r^2=1-r\) yields

\[
Q_0=-\frac{83}{6}+\frac{314}{15}r,qquad
a=-\frac{343}{30}+\frac{284}{15}r.                        \tag{19}
\]

## 5. Stirling and the index shift

By Stirling's formula,

\[
\frac{(N-1)!}{N^{N-1}}
=\sqrt{2\pi N}\,e^{-N}
 \left(1+\frac1{12N}+o(N^{-1})\right).                   \tag{20}
\]

Combining (1), (17), and (20) gives

\[
C_{N-1}=\frac{\beta^N}{r\sqrt{2\pi vwN}}
 \left(1+\frac{a+1/12}{N}+o(N^{-1})\right).              \tag{21}
\]

Set \(n=N-1\). Since

\[
N^{-1/2}=n^{-1/2}\left(1-\frac1{2N}+O(N^{-2})\right),
\]

the coefficient relative to \(\kappa\beta^n/\sqrt n\) is

\[
\gamma=a+\frac1{12}-\frac12
      =a-\frac5{12}
      =-\frac{237}{20}+\frac{284}{15}r,
\]

which proves (3)--(4).

## 6. Evidence and trust boundary

The infinite-dimensional asymptotic statement rests on the written
Fourier--Edgeworth argument, coarea normalization, exponential tilting, and
Stirling's formula. The exact checker independently performs the finite
moment algebra in \(\mathbb Q(r)\) and recomputes the predecessor's exact
rational \(C_1,\ldots,C_{12}\). Those finite values strongly corroborate
the sign and normalization of \(\gamma\), but they do not prove the uniform
remainder in Lemma 1.

No formal proof, independent peer review, effective threshold, or priority
claim is made. The singular one-step law and its three pure convolution
components are explicitly retained in the trust boundary rather than
silently replaced by an everywhere absolutely continuous law.
