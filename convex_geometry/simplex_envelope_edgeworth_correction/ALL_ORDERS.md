# All-orders expansion for sharp simplex-envelope constants

## 1. Statement

Keep the notation of [PROOF.md](PROOF.md):

\[
r=\frac{\sqrt5-1}{2},\quad
v=\frac{13+8r}{3},\quad w=1+2r,\quad
\beta=\frac{2e^{r-1}}{r^2},\quad
\kappa=\frac{\beta}{r\sqrt{2\pi vw}}.
\]

The prior contribution proved

\[
C_n=\kappa\frac{\beta^n}{\sqrt n}
\left(1+\frac{\gamma_1}{n}+o(n^{-1})\right),qquad
\gamma_1=-\frac{237}{20}+\frac{284}{15}r.                 \tag{1}
\]

**Theorem 1 (full Poincaré expansion).** There are explicitly computable
coefficients \(\gamma_j\in\mathbb Q(r)\), with \(\gamma_0=1\), such that
for every fixed integer \(J\geq0\),

\[
C_n=\kappa\frac{\beta^n}{\sqrt n}
\left(\sum_{j=0}^{J}\frac{\gamma_j}{n^j}+o(n^{-J})\right). \tag{2}
\]

The second relative correction is

\[
\boxed{\gamma_2=
 \frac{176779063}{50400}-\frac{8938472}{1575}r}
 \approx0.042041435396759606.                              \tag{3}
\]

This is an asymptotic expansion: no convergence of the infinite formal
series and no effective dimension threshold are asserted.

## 2. Exact section representation

For \(N=n+1\), the geometric dependency gives

\[
C_{N-1}=\frac{(N-1)!}{N^{N-1}}A_N(0,N),                  \tag{4}
\]

and exponential tilting gives

\[
A_M(0,M)=2^M u_M(0)+Z^Me^{rM}
 \int_0^M e^{-ru}p_M(0,M-u)\,du,\qquad Z=\frac2{r^2}.    \tag{5}
\]

Here \(p_M\) is the density of the absolutely continuous part of the sum
of \(M\) independent copies of \((Y,G)\), where

\[
\Pr[(Y,G)=(V,0)]=r^2,quad
\Pr[(Y,G)=(1+E,E)]=\Pr[(Y,G)=(-1-E,E)]=r/2              \tag{6}
\]

in mixture notation, \(V\) is uniform on \([-1,1]\), and \(E\) is
exponential of rate \(r\). Put \(Q=G-1\). The joint moment-generating
function of \((Y,Q)\) is analytic near the origin, and all of its moments
belong to \(\mathbb Q(r)\).

## 3. Arbitrary-order local expansion despite singularity

We strengthen the local lemma in [PROOF.md](PROOF.md).

**Lemma 2.** For every fixed \(J\geq0\), there are polynomials
\(P_0,\ldots,P_J\), with coefficients in \(\mathbb Q(r)\) and
\(P_0=1\), such that, uniformly for

\[
0\leq u\leq L_{M,J}=\frac{J+3}{r}\log M,
\]

\[
M p_M(0,M-u)=\frac1{2\pi\sqrt{vw}}
 \left(\sum_{j=0}^{J}\frac{P_j(u)}{M^j}+o(M^{-J})\right). \tag{7}
\]

**Proof.** Fix \(0<\epsilon<r/2\) and retain mixture-label strings with at
least \(\epsilon M\) plus and \(\epsilon M\) minus labels. The discarded
mass is exponentially small by a binomial Chernoff bound. Every discarded
configuration using at least two label types has planar density bounded by
\(r/2\): first convolve one unlike pair, whose density is bounded by
\(r/2\), then convolve the remaining probability measures. Thus the
discarded absolutely continuous density is uniformly \(O(e^{-cM})\).

For a retained string the Fourier transform is bounded, in raw dual
coordinates, by

\[
\left(1+\frac{(\xi+\eta)^2}{r^2}\right)^{-\epsilon M/2}
\left(1+\frac{(\eta-\xi)^2}{r^2}\right)^{-\epsilon M/2}.  \tag{8}
\]

Let \(\Phi_M^{\rm ret}\) be the probability-weighted sum of these retained
conditional characteristic functions. The omitted label strings have total
probability \(O(e^{-cM})\), so, uniformly in the dual variable,

\[
 \Phi_M^{\rm ret}(s)=\psi(s)^M+O(e^{-cM}),               \tag{8a}
\]

where \(\psi\) is the raw characteristic function of one full mixture step.
On every polynomially growing Fourier window the error in (8a) therefore has
exponentially small integral. After any fixed linear standardization, (8)
is integrable and its integral outside a fixed raw-coordinate origin
neighborhood is exponentially small. Let
\(W=(Y/\sqrt v,Q/\sqrt w)\) and let \(\phi\) be its characteristic
function. The exponential tails in (6) make \(\log\phi\) analytic near
zero. For an arbitrary fixed \(K\),

\[
M\log\phi(t/\sqrt M)
=-\frac{|t|^2}{2}
 +\sum_{m=3}^{K+2}M^{-(m-2)/2}
   \sum_{a+b=m}\frac{\lambda_{ab}(it_1)^a(it_2)^b}{a!b!}
 +O(M^{-(K+1)/2}|t|^{K+3}),                              \tag{9}
\]

where \(\lambda_{ab}\) are standardized joint cumulants. Exponentiating
(9) and Fourier-inverting yields the usual finite Edgeworth polynomial,
but now for the retained density. On
\(|t|\leq c\sqrt{\log M}\), the integrated Taylor remainder is the
desired order after taking enough terms. Between that ball and a fixed
multiple of \(\sqrt M\), the negative quadratic real part gives an
arbitrarily high inverse power of \(M\); beyond it, (8) gives exponential
decay. The exponentially small retained/full difference does not change
any algebraic coefficient. This proves an arbitrary fixed-order density
expansion uniformly when the standardized evaluation point is
\(O(\log M/\sqrt M)\), which includes the range in (7).

It remains to see why only integer powers of \(M^{-1}\) occur and why their
coefficients lie in \(\mathbb Q(r)\). Reflection \(Y\mapsto-Y\) kills every
cumulant with odd first index. A product of cumulants contributing the base
power \(M^{-k/2}\) has total Hermite order congruent to \(k\) modulo two.
At first coordinate zero, only even first-index Hermite polynomials survive;
the second Hermite polynomial is then evaluated at
\(-u/\sqrt{Mw}\). Each of its monomials supplies a power whose parity makes
the total power of \(M^{-1/2}\) even. The surviving powers of \(v\) and
\(w\) are integral, so every coefficient stays in \(\mathbb Q(r)\).
This gives (7). \(\square\)

## 4. Termwise slack integration and all orders

The predecessor's global bound \(\sup p_M\leq C/M\) and the choice of
\(L_{M,J}\) make the part of the integral (5) above that cutoff smaller
than the leading term by \(O(M^{-J-2})\). On the retained interval, insert
(7) and integrate termwise. Every required moment is

\[
r\int_0^\infty e^{-ru}u^k\,du=\frac{k!}{r^k}\in\mathbb Q(r). \tag{10}
\]

The all-cube term in (5) is exponentially small because
\(2/(Ze^r)<1\). Hence for every fixed \(J\),

\[
A_M(0,M)=\frac{(Ze^r)^M}{2\pi rM\sqrt{vw}}
 \left(\sum_{j=0}^{J}\frac{a_j}{M^j}+o(M^{-J})\right),
\qquad a_j\in\mathbb Q(r),\quad a_0=1.                   \tag{11}
\]

Stirling's full Poincaré expansion and the algebraic substitution
\(N=n+1\) preserve this form and its coefficient field. Equations
(4) and (11) prove Theorem 1.

## 5. Explicit second correction

For transparency, we compute through relative order \(M^{-2}\). In
addition to the third and fourth cumulants listed in [PROOF.md](PROOF.md),
the nonzero fifth and sixth centered joint cumulants are

\[
\begin{aligned}
K_{05}&=264,&
K_{23}&=392+228r,&
K_{41}&=\frac{5792}{15}+\frac{1176}{5}r,\\
K_{06}&=960+1920r,&
K_{24}&=3072+2000r,&
K_{42}&=\frac{46576}{15}+\frac{29128}{15}r,\\
K_{60}&=\frac{196352}{63}+\frac{121840}{63}r.             \tag{12}
\end{aligned}
\]

Let \(\varepsilon=M^{-1/2}\). Exponentiating the cumulant series uses

\[
\begin{aligned}
E_1&=L_3,\\
E_2&=L_4+\tfrac12L_3^2,\\
E_3&=L_5+L_3L_4+\tfrac16L_3^3,\\
E_4&=L_6+L_3L_5+\tfrac12L_4^2
     +\tfrac12L_3^2L_4+\tfrac1{24}L_3^4,                 \tag{13}
\end{aligned}
\]

where \(L_m=\sum_{a+b=m}K_{ab}(it_1)^a(it_2)^b/(a!b!)\) before covariance
standardization. Fourier inversion replaces monomials by Hermite
polynomials. At \((0,-u/\sqrt{Mw})\), after also expanding the Gaussian
factor, the relative density is

\[
1+\frac{A(u)}M+\frac{B(u)}{M^2}+o(M^{-2}),                \tag{14}
\]

where \(A\) is the polynomial from the first-correction proof and

\[
\begin{aligned}
B(u)={}&\left(\frac{48873599}{12600}-\frac{219673}{35}r\right)\\
&+\left(\frac{33529}{50}-\frac{163097}{150}r\right)u\\
&+\left(\frac{10733}{300}-\frac{1372}{25}r\right)u^2\\
&+\left(-\frac56+\frac{19}{30}r\right)u^3+\frac1{40}u^4. \tag{15}
\end{aligned}
\]

Using (10) gives

\[
a_1=-\frac{343}{30}+\frac{284}{15}r,qquad
a_2=\frac{43987487}{12600}-\frac{2965409}{525}r.          \tag{16}
\]

Stirling contributes
\(1+1/(12N)+1/(288N^2)+O(N^{-3})\). Therefore, before replacing
\(N=n+1\), the two section/Stirling corrections are

\[
c_1=a_1+\frac1{12},\qquad
c_2=a_2+\frac{a_1}{12}+\frac1{288}.                       \tag{17}
\]

Since

\[
\sqrt{\frac n{n+1}}=1-\frac1{2n}+\frac3{8n^2}+O(n^{-3}),
\]

we obtain

\[
\gamma_2=a_2-\frac{17}{12}a_1+\frac{73}{288},            \tag{18}
\]

which reduces using \(r^2=1-r\) to (3).

## 6. Evidence and trust boundary

[verify_all_orders.py](verify_all_orders.py) derives joint cumulants by two
different exact combinatorial algorithms (set partitions and a
distinguished-slot recursion), constructs (13) as formal bivariate
polynomials, performs the Hermite substitution, and verifies (12)--(18) in
\(\mathbb Q(r)\). It also recomputes the predecessor's exact
\(C_1,\ldots,C_{12}\); their twice-corrected residuals approach the new
coefficient.

Finite arithmetic verifies coefficient algebra, not the analytic remainder.
The universal all-orders statement rests on Lemma 2, exponential tail
control, termwise integration on a logarithmic window, and the classical
full Stirling expansion. No formal proof, independent peer review,
convergence claim for the formal series, or effective threshold is asserted.
