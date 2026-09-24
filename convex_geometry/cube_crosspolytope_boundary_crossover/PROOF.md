# The Bessel boundary layer for affine cube--crosspolytope sections

## 1. Statement

Let

\[
g(x)=(|x|-1)_+,
\qquad
A_N(\theta,\rho)=\int_{\mathbb R^N}
 \delta\!\left(\sum_i x_i-\theta N\right)
 \mathbf1_{\{\sum_i g(x_i)\leq\rho N\}}\,dx.               \tag{1}
\]

Thus $A_N$ is $1/\sqrt N$ times the Euclidean volume of the affine
section of $[-1,1]^N+\rho N B_1^N$.  For $N=n+1$, put

\[
D_n(\theta,\rho)=\frac{n!}{N^n}A_N(\theta,\rho).            \tag{2}
\]

Fix $|\theta|<1$.  There is a unique $a\in\mathbb R$ satisfying

\[
\theta=\coth a-\frac1a,                                    \tag{3}
\]

with the continuous value $a=0$ when $\theta=0$.  Define

\[
I=I(a)=\int_{-1}^1e^{ax}\,dx=\frac{2\sinh a}{a},           \tag{4}
\]

and let $V$ have density $e^{ax}/I$ on $[-1,1]$.  Write

\[
v=\operatorname{Var}V,
\quad \kappa_3=\operatorname{cum}_3(V),
\quad \kappa_4=\operatorname{cum}_4(V),
\quad c=a\coth a=1+a\theta.                                \tag{5}
\]

All continuous values at $a=0$ are understood.  Let

\[
\mathcal F(z)=\mathrm I_0(2\sqrt z)
=\sum_{k=0}^{\infty}\frac{z^k}{(k!)^2},                    \tag{6}
\]

where $\mathrm I_0$ is the modified Bessel function.

**Theorem 1 (critical boundary crossover).**  For every integer $J\geq0$
there are real-analytic functions $\Psi_j(\theta,\lambda)$, even in
$\theta$, such that

\[
\frac{A_N(\theta,\lambda/N^2)}{A_N(\theta,0)}
=\sum_{j=0}^J\frac{\Psi_j(\theta,\lambda)}{N^j}
 +O(N^{-J-1}),                                               \tag{7}
\]

locally uniformly for $(\theta,\lambda)\in(-1,1)\times[0,\infty)$.  The
leading crossover is

\[
\boxed{\Psi_0(\theta,\lambda)
=\mathcal F(\lambda c)
=\mathrm I_0\!\left(2\sqrt{\lambda a\coth a}\right).}      \tag{8}
\]

In particular, $N^{-2}$ is the critical thickness scale: if
$N^2\rho_N\to0$, the ratio in (7) tends to $1$, while if
$N^2\rho_N\to\lambda\in(0,\infty)$, it tends to the nontrivial value
(8).

The first correction is explicit.  Put

\[
z=\lambda c,\qquad h=\lambda a,\qquad d=\theta z-h,
\qquad
\mathcal J(z)=\int_0^1t\mathcal F'(tz)\,dt.                 \tag{9}
\]

Then

\[
\boxed{\begin{aligned}
\Psi_1={}&\frac12\left(z\mathcal F'-z^2\mathcal F''\right)
-\frac{\kappa_3}{2v^2}d\mathcal F'\\
&-\frac1{2v}\left(
 ((1+\theta^2)z-2\theta h)\mathcal F'
 +d^2\mathcal F''\right)
+a\lambda h\mathcal J(z),
\end{aligned}}                                               \tag{10}
\]

where all derivatives are evaluated at $z$.

There is also an absolute normalized form.  Set

\[
\beta_0=I e^{-a\theta-1},
\qquad
Q_0=\frac{\kappa_4}{8v^2}-\frac{5\kappa_3^2}{24v^3}.       \tag{11}
\]

Then

\[
D_{N-1}(\theta,\lambda/N^2)
=\frac{\beta_0^N}{\sqrt v}\left[
 \mathcal F(z)+\frac{\Psi_1+(Q_0+1/12)\mathcal F(z)}N
 +O(N^{-2})\right],                                        \tag{12}
\]

and (12) has an expansion to every fixed order.  At $\theta=0$, one has
$a=h=\kappa_3=0,v=1/3,z=\lambda$, and (10) simplifies to

\[
\Psi_1(0,\lambda)
=-z\mathcal F'(z)-\frac12z^2\mathcal F''(z).                \tag{13}
\]

## 2. Why the scale is $N^{-2}$

At the cube boundary, all coordinates lie in $[-1,1]$.  A tail coordinate
has an excess variable $e\geq0$.  If the total excess budget is
$R=\rho N$, then one tail contributes a factor of order $R$, while its
choice of coordinate contributes a factor of order $N$.  The first tail
therefore has relative size $NR=N^2\rho$.  A nontrivial finite-label limit
requires $N^2\rho\asymp1$, or $R=\lambda/N$.

This differs from the fixed-interior saddle, where a linear number of
coordinates participates in a two-dimensional Gaussian fluctuation.  Here
only finitely many tail labels survive, and their sum is a Bessel rather than
a Gaussian law.

## 3. Exact tail-label decomposition

Let

\[
C_m(s)=\int_{[-1,1]^m}\delta(\textstyle\sum_i x_i-s)\,dx   \tag{14}
\]

be the delta-normalized cube section.  Choose $p$ coordinates in the plus
tail $x=1+e$, $q$ in the minus tail $x=-1-e$, and let
$k=p+q,m=N-k$.  If $P$ and $Q$ are the sums of the plus and minus
excesses, respectively, the exact stratum identity is

\[
\begin{aligned}
A_N(\theta,\lambda/N^2)
=\sum_{p+q\leq N}\frac{(N)_{p+q}}{p!q!}
\int_{\substack{e_i\geq0\\P+Q\leq\lambda/N}}
C_{N-p-q}(\theta N-p+q-P+Q)\,de,
\end{aligned}                                                \tag{15}
\]

with the evident direct interpretation for zero inactive coordinates.
Formula (15), including its factorials and the two pure-ray endpoints, also
follows from the exact affine stratum formula used by the verifier.

## 4. Uniform local expansion of the cube density

Under the tilted interval density $e^{ax}/I$, the mean is $\theta$.  A
standard one-dimensional Fourier expansion, uniform for $\theta$ in a
compact subset of $(-1,1)$, gives

\[
\begin{aligned}
C_m(\theta m+s)
=\frac{I^m e^{-a(\theta m+s)}}{\sqrt{2\pi m v}}
\left[1+\frac1m\left(
 Q_0-\frac{\kappa_3s}{2v^2}-\frac{s^2}{2v}
 \right)+O\!\left(\frac{(1+|s|)^6}{m^2}\right)\right].    \tag{16}
\end{aligned}
\]

The same argument gives arbitrary order, with coefficients polynomial in
$s$ and analytic in $a$.  To justify this directly, the interval density
has an analytic moment-generating function, its characteristic function has
modulus strictly below one away from the origin, and two convolutions give
an integrable Fourier majorant.  Taylor expansion near zero and Fourier
inversion prove (16); keeping more terms proves the all-orders version.

For $k=p+q$, scale each excess as $e_i=t_i/N$, and put

\[
s_0=\theta k-p+q,
\qquad b_+=\frac{e^a}{I},\quad b_-=\frac{e^{-a}}I.           \tag{17}
\]

Dividing the numerator version of (16) by its $m=N,s=0$ version gives

\[
\begin{aligned}
\frac{C_{N-k}(\theta N-p+q-P+Q)}{C_N(\theta N)}
=b_+^p b_-^q\left[1+\frac1N\left(
 \frac k2-\frac{\kappa_3s_0}{2v^2}-\frac{s_0^2}{2v}
 +a(T_+-T_-)
 \right)+O(N^{-2}\mathcal P)\right],                       \tag{18}
\end{aligned}
\]

where $T_+,T_-$ are the sums of the scaled plus/minus excesses and
$\mathcal P$ is a fixed polynomial in $k,T_++T_-$.  Notice that $Q_0$
cancels from the ratio at order $N^{-1}$.

The other two elementary expansions are

\[
(N)_k=N^k\left(1-\frac{k(k-1)}{2N}+O(N^{-2}k^4)\right),     \tag{19}
\]

and, on the $k$-simplex $T_++T_-\leq\lambda$,

\[
\operatorname{vol}=\frac{\lambda^k}{k!},
\qquad
\operatorname{avg}(T_+-T_-)=\frac{(p-q)\lambda}{k+1}.      \tag{20}
\]

## 5. The Bessel sum and the first correction

The leading contribution of the $(p,q)$ stratum is

\[
w_{p,q}=\frac{\lambda^{p+q}b_+^p b_-^q}
{(p+q)!p!q!}.                                               \tag{21}
\]

Since

\[
b_++b_-=a\coth a=c,
\qquad b_+-b_-=a,                                          \tag{22}
\]

summing (21) first over $p+q=k$ proves

\[
\sum_{p,q\geq0}w_{p,q}
=\sum_{k\geq0}\frac{(\lambda c)^k}{(k!)^2}
=\mathcal F(\lambda c),                                    \tag{23}
\]

which is (8).

Combining (18)--(20), the relative $N^{-1}$ coefficient attached to
$w_{p,q}$ is

\[
B_{p,q}=k-\frac{k^2}{2}
-\frac{\kappa_3s_0}{2v^2}-\frac{s_0^2}{2v}
+\frac{a(p-q)\lambda}{k+1}.                                \tag{24}
\]

Thus $\Psi_1=\sum w_{p,q}B_{p,q}$.  Formula (10) is not an additional
assumption; it is the closed form of this double series.  Indeed, introduce

\[
K=x\partial_x+y\partial_y,qquad S=x\partial_x-y\partial_y,
\quad x=\lambda b_+,\ y=\lambda b_-,                       \tag{25}
\]

and apply $K-K^2/2$, $\theta K-S$, and
$(\theta K-S)^2$ to $\mathcal F(x+y)$.  Here $x+y=z$ and $x-y=h$.
The final term in (24) is

\[
a\lambda\int_0^1(S\mathcal F)(tx,ty)\,dt
=a\lambda h\mathcal J(z).                                 \tag{26}
\]

Expanding (25)--(26) gives exactly (10).

## 6. All orders and local uniformity

For bounded $\lambda$, the weights (21), even after multiplication by
any fixed polynomial in $p+q$, form an absolutely and uniformly summable
series.  Truncate (15) at $k\leq L_J\log N$.  On this range the arbitrary-
order version of (16), the falling-factorial expansion, and the scaled
simplex moments are uniform and may be integrated term by term.

An exponential tilt bound on $C_{N-k}$ bounds the normalized $k$-tail
contribution by a polynomial factor times

\[
\sum_{p+q=k}\frac{(C\lambda)^k}{k!p!q!}.                   \tag{27}
\]

Consequently the part with $k>L_J\log N$ is smaller than every prescribed
power of $N^{-1}$; strata with fewer than two inactive coordinates obey
the same estimate directly from their simplex fibers.  This proves (7),
including local uniformity.  Reflection interchanges $p$ and $q$, so
every coefficient is even in $\theta$.

Finally, Stirling's expansion and (16) at $s=0,m=N$ give

\[
\frac{(N-1)!}{N^{N-1}}C_N(\theta N)
=\frac{\beta_0^N}{\sqrt v}
 \left(1+\frac{Q_0+1/12}{N}+O(N^{-2})\right),              \tag{28}
\]

which combines with (7) to prove (12) and its all-orders extension.

## 7. Exact boundary classification and matching

The strict affine interior is $\rho>(|\theta|-1)_+$.  On its boundary:

- if $|\theta|<1$, then $\rho=0$ and the section is exactly the cube
  section $C_N(\theta N)$;
- if $|\theta|>1$, equality in the convex inequality
  $N^{-1}\sum g(x_i)\geq g(N^{-1}\sum x_i)$ forces every coordinate onto
  the appropriate ray, and

  \[
  D_n(\theta,|\theta|-1)=(|\theta|-1)^n;                   \tag{29}
  \]

- at $\theta=\pm1,\rho=0$, the positive-dimensional section volume is
  zero.

Theorem 1 resolves the critical approach to the first of these boundary
pieces.  Its large-$z$ exponential
$\mathcal F(z)\sim e^{2\sqrt z}/\sqrt{4\pi\sqrt z}$ also matches the
exponent $2N\sqrt{c\rho}$ obtained by expanding the fixed-interior saddle
as $\rho\downarrow0$.  This is a consistency statement, not a claim of a
uniform theorem when $\lambda\to\infty$ with $N$.

## 8. Trust boundary

The verifier evaluates (10) in two ways: the univariate Bessel-derivative
formula and the independent double sum (21),(24).  It compares both with
exact rational affine sections at four parameter pairs, checks reflection,
and checks the zero-thickness specialization.  These computations corroborate
the constants but do not prove (7).  The universal statement rests on the
uniform local cube expansion, factorial tail bound, termwise simplex
integration, and Stirling expansion above.  There is no formal proof,
independent peer review, effective onset threshold, or simultaneous
large-$\lambda$ claim.
