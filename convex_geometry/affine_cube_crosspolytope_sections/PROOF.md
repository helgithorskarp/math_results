# Full asymptotics for every interior affine section

## 1. The theorem

Put

\[
g(x)=(|x|-1)_+,
\qquad H_{N,\theta}=\{x\in\mathbb R^N:\textstyle\sum_i x_i=\theta N\},
\]

and define the delta-normalized section

\[
\begin{aligned}
A_N(\theta,\rho)
 &=\int_{\mathbb R^N}\delta\!\left(\sum_i x_i-\theta N\right)
   \mathbf1_{\{\sum_i g(x_i)\leq\rho N\}}\,dx\\
 &=\frac1{\sqrt N}
   \left|\left([-1,1]^N+\rho N B_1^N\right)
   \cap H_{N,\theta}\right|_{N-1}.
\end{aligned}                                                   \tag{1}
\]

For (N=n+1), let

\[
D_n(\theta,\rho)=\frac{n!}{N^n}A_N(\theta,\rho).             \tag{2}
\]

The natural open parameter region is

\[
\mathcal C=\{(\theta,\rho):\rho>(|\theta|-1)_+\}.           \tag{3}
\]

For (r>|a|), set

\[
Z(a,r)=\int_{\mathbb R}e^{ax-rg(x)}\,dx
=\frac{2\sinh a}{a}+\frac{e^a}{r-a}+\frac{e^{-a}}{r+a},     \tag{4}
\]

where the first quotient is (2) at (a=0).  Section 2 proves that
for each ((\theta,\rho)\in\mathcal C) there is a unique ((a,r)),
(r>|a|), satisfying

\[
\partial_a\log Z(a,r)=\theta,
\qquad -\partial_r\log Z(a,r)=\rho.                         \tag{5}
\]

Let (Y) have density (Z^{-1}e^{ay-rg(y)}), put (G=g(Y)), and let

\[
\Sigma=\operatorname{Cov}(Y,G),\qquad
F=Z(a,r)e^{-a\theta+r\rho},\qquad
\beta=F/e,qquad
\kappa=\frac{\beta}{r\sqrt{2\pi\det\Sigma}}.              \tag{6}
\]

**Theorem.**  For every integer (J\geq0), there are real-analytic
functions (\gamma_j:\mathcal C\to\mathbb R), with (\gamma_0=1), such
that

\[
D_n(\theta,\rho)=\kappa\frac{\beta^n}{\sqrt n}
 \left(\sum_{j=0}^J\frac{\gamma_j(\theta,\rho)}{n^j}
       +o(n^{-J})\right).                                   \tag{7}
\]

The remainder after division by the leading factor is uniform on every
compact subset of (\mathcal C).  In particular, this classifies the
full interior affine phase: there is one analytic saddle and an all-orders
integer-power expansion throughout (3).  No assertion is made on the
boundary (\rho=(|\theta|-1)_+), or uniformly as that boundary is
approached.

The first correction has the invariant formula in Section 6.  Reflection
gives (\gamma_j(-\theta,\rho)=\gamma_j(\theta,\rho)).  At (\theta=0),
the theorem and all its constants specialize to the previously proved
central-section family.

## 2. The saddle map is an analytic diffeomorphism

The support of ((Y,G)) before tilting is

\[
\{(x,0):-1\leq x\leq1\}
\cup\{(1+t,t):t\geq0\}
\cup\{(-1-t,t):t\geq0\}.                                  \tag{8}
\]

Its closed convex hull is the epigraph

\[
\{(\theta,\rho):\rho\geq(|\theta|-1)_+\},                 \tag{9}
\]

whose interior is exactly (\mathcal C).  In natural coordinates
((a,b)=(a,-r)), the log-Laplace transform is (\Lambda(a,b)=\log
Z(a,-b)) and its domain is the open cone (b<-|a|).

The Hessian of (\Lambda) is the covariance of ((Y,G)).  It is positive
definite: if a linear combination of (Y) and (G) were constant, its
restriction to the interval part of (8) would first force the coefficient
of (Y) to vanish, and either ray would then force the other coefficient
to vanish.  Thus the gradient is locally one-to-one and analytic.

For completeness, the standard mean-parameter argument is short here.
Fix (m=(\theta,\rho)) in the interior (9).  The strictly convex function

\[
(a,b)\longmapsto \Lambda(a,b)-a\theta-b\rho               \tag{10}
\]

is coercive on the natural cone.  Indeed, finitely many small intervals
in (8) have a convex hull containing a neighborhood of (m); lower
bounding the Laplace integral on those intervals gives linear growth in
every escaping parameter direction.  At either finite boundary
(r-a=0) or (r+a=0), the corresponding tail integral in (4) diverges.
Hence (10) has a unique critical point.  Conversely, every gradient value
is a strict barycenter of (8) and so lies in (3).  The positive Hessian and
the analytic inverse theorem now show that

\[
(a,r)\in\{r>|a|\}\longleftrightarrow(\theta,\rho)\in\mathcal C          \tag{11}
\]

is an analytic diffeomorphism.  Consequently the inverse image of a
compact subset of (\mathcal C) stays a positive distance from
(r=|a|) and in a bounded parameter set.

## 3. The singular one-step law and its smooth convolution

Write

\[
I_0=\frac{2\sinh a}{a},\qquad
I_+=\frac{e^a}{r-a},\qquad I_-=\frac{e^{-a}}{r+a}.          \tag{12}
\]

The tilted law is the following three-component mixture:

\[
\begin{array}{c|c|c}
\text{label}&(Y,G)&\text{probability}\\ \hline
0&(V,0),\quad f_V(x)=e^{ax}/I_0,\ -1<x<1&I_0/Z\\
+&(1+E_+,E_+),\quad E_+\sim\operatorname{Exp}(r-a)&I_+/Z\\
-&(-1-E_-,E_-),\quad E_-\sim\operatorname{Exp}(r+a)&I_-/Z.
\end{array}                                                 \tag{13}
\]

All three probabilities and both exponential rates are bounded away from
zero on a compact saddle set.  Although (13) is singular in the plane,
its convolution has a uniformly controlled absolutely continuous part.

Let (p_M(s,t)) be the planar density of that absolutely continuous part
for a sum of (M) independent copies.  Choose (\epsilon>0) below the
minimum of the two tail-label probabilities and retain label strings with
at least (\epsilon M) plus labels and (\epsilon M) minus labels.  A
uniform Chernoff bound makes the probability of the other strings
(O(e^{-cM})).  Every omitted non-pure string already has a bounded planar
density after two different line types are convolved, and further
convolution cannot increase its (L^\infty) norm.  The only pure strings
are handled separately in Section 5.

For a retained string, the modulus of its Fourier transform is bounded by

\[
\left(1+\frac{(\xi+\eta)^2}{(r-a)^2}\right)^{-\epsilon M/2}
\left(1+\frac{(\eta-\xi)^2}{(r+a)^2}\right)^{-\epsilon M/2}.             \tag{14}
\]

This gives a parameter-uniform integrable majorant and exponential decay
outside a fixed raw-frequency neighborhood.  In that neighborhood, the
logarithm of the full characteristic function has a Taylor expansion of
arbitrary fixed order, uniformly on the compact saddle set.  Covariance
standardization, expansion on (O(\sqrt{\log M})), and Fourier inversion
therefore give, for every fixed (J),

\[
M p_M(\theta M,\rho M-u)
=\frac1{2\pi\sqrt{\det\Sigma}}
 \left(\sum_{j=0}^J\frac{P_j(a,r,u)}{M^j}+o(M^{-J})\right),              \tag{15}
\]

uniformly for (0\leq u\leq C_J\log M).  Each (P_j) is a polynomial in
(u) with real-analytic coefficients, and (P_0=1).

There are no half-integer powers in (15), even away from the symmetric
saddle.  The Edgeworth polynomial multiplying (M^{-k/2}) has Hermite
parity (k).  Evaluating it at ((0,-u)/\sqrt M) contributes a monomial
of degree (d\equiv k\pmod2); hence the resulting power
(M^{-(k+d)/2}) is integral.  The Gaussian factor also has only integral
powers.  The same estimates give the global bound

\[
\sup_{s,t}p_M(s,t)\leq C/M.                                \tag{16}
\]

## 4. Change of measure and slack integration

Apart from the pure strings isolated below, product change of measure gives

\[
A_M^{\mathrm{ac}}(\theta,\rho)
=F^M\int_0^{\rho M}e^{-ru}p_M(\theta M,\rho M-u)\,du.       \tag{17}
\]

By (16), the part with (u>C_J\log M) is smaller than the leading term by
an arbitrary prescribed inverse power when (C_J) is chosen large enough.
Insert (15) below that cutoff and integrate termwise, using

\[
r\int_0^\infty e^{-ru}u^k\,du=\frac{k!}{r^k}.              \tag{18}
\]

It follows that

\[
A_M^{\mathrm{ac}}(\theta,\rho)
=\frac{F^M}{2\pi rM\sqrt{\det\Sigma}}
 \left(\sum_{j=0}^J\frac{a_j(a,r)}{M^j}+o(M^{-J})\right),                 \tag{19}
\]

locally uniformly, with (a_0=1) and analytic (a_j).

## 5. The three pure strata are exponentially smaller

The decomposition (13) has three singular strings.  In the original
Lebesgue integral their contributions are

\[
\begin{aligned}
C_M(\theta)&=\int_{[-1,1]^M}\delta(\textstyle\sum x_i-\theta M)\,dx,\\
R_M^+(\theta,\rho)&=\mathbf1_{\{\theta>1,\ \theta-1\leq\rho\}}
 \frac{((\theta-1)M)^{M-1}}{(M-1)!},\\
R_M^-(\theta,\rho)&=R_M^+(-\theta,\rho).
\end{aligned}                                                 \tag{20}
\]

The cube term is zero for (|\theta|>1).  When present, exponential
tilting by (a), together with the uniform local bound for a bounded
one-dimensional density, shows that its exponential ratio to (F^M) is

\[
\frac{I_0}{Z e^{r\rho}}<1.                                  \tag{21}
\]

For the plus ray, tilting its exponential coordinate gives the ratio

\[
\frac{I_+}{Z}\,e^{-r(\rho-\theta+1)}<1,                     \tag{22}
\]

and the minus ray has the reflected bound.  The omitted density factors
in these comparisons grow at most polynomially.  The inequalities are
strict and their maxima remain below one on every compact subset of
(\mathcal C).  Thus all three terms in (20) are exponentially smaller
than (19).  This point is essential when (|\theta|>1): the relevant
one-ray stratum is nonzero, but it does not alter the interior saddle
expansion.

Combining (19)--(22), taking (M=N=n+1), and applying Stirling's complete
expansion proves (7).  The leading constants are (6).  The universal
conversion from relative order (N^{-1}) in (19) to relative order
(n^{-1}) in (7) contributes (-5/12).

## 6. An invariant first correction

Let (X=(Y-\theta,G-\rho)), write (A=\Sigma^{-1}), use indices
(1=Y,2=G), and denote joint cumulant tensors by
(K_{i_1\ldots i_m}=\operatorname{cum}(X_{i_1},\ldots,X_{i_m})).
For the set (\mathcal P_2(q)) of pair partitions of
(\{1,\ldots,q\}), put

\[
\begin{aligned}
E_0={}&\frac1{24}\sum_{i_1,\ldots,i_4}K_{i_1\ldots i_4}
 \sum_{\pi\in\mathcal P_2(4)}
 \prod_{\{p,q\}\in\pi}A_{i_pi_q}\\
&-\frac1{72}\sum_{i_1,\ldots,i_6}
 K_{i_1i_2i_3}K_{i_4i_5i_6}
 \sum_{\pi\in\mathcal P_2(6)}
 \prod_{\{p,q\}\in\pi}A_{i_pi_q},                       \tag{23}\\
L={}&\frac12\sum_{i,j,k}K_{ijk}A_{ij}A_{k2}.              \tag{24}
\end{aligned}
\]

The order-(M^{-1}) relative density correction at slack (u) is

\[
E_0+Lu-\tfrac12A_{22}u^2.                                  \tag{25}
\]

Therefore the first section and normalized corrections are

\[
a_1=E_0+\frac Lr-\frac{A_{22}}{r^2},
\qquad
\boxed{\gamma_1=E_0+\frac Lr-\frac{A_{22}}{r^2}-\frac5{12}}.            \tag{26}
\]

All moments in (23)--(26) are obtained by differentiating the elementary
partition function (4), so (26) is an explicit analytic formula without
numerical integration.  The verifier instead computes the same raw
moments directly from the interval and two exponential tails, forms the
cumulants recursively, and contracts all (3) and (15) pair partitions
in (23).

At (\theta=0), (a=0), (\Sigma) is diagonal, and (26) reduces exactly
to the central formula.  For (\rho=1), with
(r=(\sqrt5-1)/2), it gives

\[
\gamma_1=-\frac{237}{20}+\frac{284}{15}r
=-0.1485564796686575406\ldots.                             \tag{27}
\]

For illustration, at ((\theta,\rho)=(1/2,1)), the unique saddle is

\[
(a,r)=(0.0890828094583270381\ldots,
       0.6466253569815012749\ldots)
\]

and (\gamma_1=-0.1387039848615766289\ldots).  At
((3/2,1)), beyond the cube range but still in the interior,

\[
(a,r)=(0.5718953080541680099\ldots,
       1.1491007999316258120\ldots),
\qquad
\gamma_1=-0.0533037262299038499\ldots.                     \tag{28}
\]

## 7. Exact finite sections and trust boundary

The companion [exact formula](EXACT_SECTION.md) partitions coordinates
into interval, plus-tail, and minus-tail labels and reduces every rational
finite section to polynomial integrals.  It includes the pure rays in
(20), specializes identically to the earlier central enumerator, and is
reflection invariant.  It is independent finite-dimensional evidence for
(26), not a proof of the limiting remainder.

The universal theorem rests on the diffeomorphism argument, uniform
retained-label Fourier estimates, slack-tail estimate, pure-stratum gaps,
and Stirling expansion above.  The computation is standard-library-only
and deterministic, but uses high-precision arithmetic for noncentral
saddles.  There is no formal proof, independent peer review, effective
onset bound, or assertion of uniformity at the boundary of (3).
