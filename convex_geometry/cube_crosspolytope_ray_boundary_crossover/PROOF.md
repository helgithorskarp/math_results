# Exact ray-boundary universality and its Bessel crossover

## 1. Statement

Let

\[
g(x)=(|x|-1)_+,
\qquad
A_N(\theta,\rho)=\int_{\mathbb R^N}
 \delta\!\left(\sum_i x_i-\theta N\right)
 \mathbf1_{\{\sum_i g(x_i)\leq\rho N\}}\,dx.              \tag{1}
\]

This is $1/\sqrt N$ times the Euclidean volume of the indicated affine
section.  For $N=n+1$, set

\[
D_n(\theta,\rho)=\frac{n!}{N^n}A_N(\theta,\rho).           \tag{2}
\]

Write $(u)_k=u(u-1)\cdots(u-k+1)$ for a falling factorial.

**Theorem 1 (exact finite-$N$ universality).**  Fix $|\theta|>1$ and put
$m=|\theta|-1$.  For $z\geq0$ satisfying $mz/N<2$,

\[
\boxed{
 D_{N-1}\!\left(\theta,m(1+z/N^2)\right)=m^{N-1}Q_N(z),} \tag{3}
\]

where $Q_N$ is the degree-$(N-1)$ polynomial

\[
\boxed{
Q_N(z)=1+\sum_{k=1}^{N-1}
 \frac{(N)_k(N-1)_k}{k!N^{2k}(k-1)!}
 \int_0^z t^{k-1}\left(1+\frac{t}{N^2}\right)^{N-k-1}dt.} \tag{4}
\]

In particular, $Q_N$ has nonnegative rational coefficients and is exactly
independent of the offset magnitude $m$ and of the sign of $\theta$.  At the
boundary, $Q_N(0)=1$ and

\[
A_N(\theta,m)=\frac{(mN)^{N-1}}{(N-1)!}.                  \tag{5}
\]

The integral in (4) is wholly algebraic:

\[
\int_0^z t^{k-1}\left(1+\frac t{N^2}\right)^{N-k-1}dt
=\sum_{j=0}^{N-k-1}\binom{N-k-1}{j}
 \frac{z^{k+j}}{N^{2j}(k+j)}.                             \tag{6}
\]

**Theorem 2 (universal Bessel expansion).**  For every fixed $J\geq0$,
there are entire functions $\Psi_j(z)$ such that

\[
Q_N(z)=\sum_{j=0}^J\frac{\Psi_j(z)}{N^j}+O(N^{-J-1})      \tag{7}
\]

locally uniformly for $z\in[0,\infty)$.  The first two are

\[
\boxed{\Psi_0(z)=\mathrm I_0(2\sqrt z),\qquad
\Psi_1(z)=-\sqrt z\,\mathrm I_1(2\sqrt z).}              \tag{8}
\]

Consequently the $N^{-2}$ radius scale is critical.  If $m>0$ is fixed,
$\rho_N\geq m$, and

\[
z_N=N^2(\rho_N/m-1)\longrightarrow z<\infty,
\]

then the ratio in (3) tends to $\mathrm I_0(2\sqrt z)$.  In additive
coordinates, $N^2(\rho_N-m)\to\lambda$ gives $z=\lambda/m$.

## 2. The geometric gap below the first opposite tail

Reflection of every coordinate reduces the proof to $\theta=1+m$.  Classify
coordinates as

\[
x_i=1+e_i\quad\hbox{(plus tail)},\qquad
x_i=1-y_i\quad\hbox{(inactive)},\qquad
x_i=-1-e_i\quad\hbox{(minus tail)},                       \tag{9}
\]

where $e_i\geq0$ and $0\leq y_i\leq2$.  Suppose there are $k$ inactive
coordinates and $q$ minus-tail coordinates.  If $P,Q,Y$ denote the sums of
plus excesses, minus excesses, and inactive deficits, respectively, the
affine constraint gives

\[
P=mN+Y+2q+Q,\qquad P+Q=mN+Y+2q+2Q.                       \tag{10}
\]

At radius $m(1+z/N^2)$, the excess budget is $mN+mz/N$.
The hypothesis $mz/N<2$ and (10) force $q=0$.  They also give
$Y\leq mz/N<2$, so every individual constraint $y_i\leq2$ is automatic.
This strict geometric gap is the source of the exact collapse.

## 3. Exact integration and cancellation of the offset

Choose the $k$ inactive labels.  There are $N-k\geq1$ plus-tail labels.  For
fixed inactive deficits, their excesses have sum $mN+Y$; delta integration
over the positive simplex gives

\[
\frac{(mN+Y)^{N-k-1}}{(N-k-1)!}.
\]

Summing over labels therefore yields the exact identity

\[
A_N\!\left(1+m,m(1+z/N^2)\right)
=\sum_{k=0}^{N-1}\binom Nk\frac1{(N-k-1)!}
 \int_{\substack{y_i\geq0\\\sum y_i\leq mz/N}}
 (mN+\textstyle\sum y_i)^{N-k-1}dy.                       \tag{11}
\]

The $k=0$ term is (5).  Divide (11) by that term, put $y_i=ms_i$, and then
$t_i=Ns_i$.  Every power of $m$ cancels, leaving

\[
\frac{A_N(1+m,m(1+z/N^2))}{A_N(1+m,m)}
=\sum_{k=0}^{N-1}\frac{(N)_k(N-1)_k}{k!N^{2k}}
 \int_{\substack{t_i\geq0\\\sum t_i\leq z}}
 \left(1+\frac{\sum t_i}{N^2}\right)^{N-k-1}dt.          \tag{12}
\]

For $k\geq1$, integrating first over $t=\sum t_i$ contributes the shell
factor $t^{k-1}/(k-1)!$.  This proves (3)--(6), and reflection proves the
same result for $\theta<-1$.

## 4. Leading term and first correction

For each fixed $k$, the prefactor and integrand in (12) have expansions

\[
\frac{(N)_k(N-1)_k}{N^{2k}}
=1-\frac{k^2}{N}+O_k(N^{-2}),                             \tag{13}
\]

\[
\left(1+\frac t{N^2}\right)^{N-k-1}
=1+\frac tN+O_{k,t}(N^{-2}).                              \tag{14}
\]

The leading contribution of the $k$th term is

\[
w_k=\frac{z^k}{(k!)^2}.                                   \tag{15}
\]

The average of $t=\sum t_i$ on the $k$-simplex is $kz/(k+1)$.
Consequently its relative first correction is

\[
B_k=-k^2+\frac{kz}{k+1}.                                  \tag{16}
\]

Let

\[
\mathcal F(z)=\sum_{k\geq0}\frac{z^k}{(k!)^2}
=\mathrm I_0(2\sqrt z),\qquad K=z\frac d{dz},            \tag{17}
\]

and

\[
\mathcal G(z)=\sum_{k\geq0}\frac{z^k}{k!(k+1)!}
=\frac{\mathrm I_1(2\sqrt z)}{\sqrt z}.                 \tag{18}
\]

Summing (15)--(16) gives

\[
\Psi_1=-K^2\mathcal F+z(\mathcal F-\mathcal G).          \tag{19}
\]

The Bessel equation $z\mathcal F''+\mathcal F'-\mathcal F=0$ says
$K^2\mathcal F=z\mathcal F$.  Hence (19) reduces to the second formula in
(8).  Its value at $z=0$ is understood by continuity.

## 5. All orders and uniformity

Formula (12) already supplies an algorithm for every coefficient.  Expand
the two finite products in (13) and the logarithm of the integrand in (14)
to the requested order, integrate monomials on the simplex, and sum over
$k$.  At each order the coefficient is a convergent series consisting of
$z^k/(k!)^2$ times a polynomial in $k$ and $z$, hence is entire.

For completeness, the interchange is uniform on every compact
$0\leq z\leq Z$.  The $k$th term in (12) is bounded by

\[
e^Z\frac{Z^k}{(k!)^2},                                   \tag{20}
\]

because both normalized falling products are at most one.  Split the sum at
$k=L_N$, where $L_N$ is a sufficiently large multiple of
$\log N/\log\log N$.  The factorial tail in (20) is smaller than any
prescribed power of $N^{-1}$.  Below $L_N$, Taylor's theorem applied to the
finite products and logarithm has a uniform remainder of the required
order after multiplication by a polynomial in $k$; (20) sums that
polynomial.  This proves (7) to arbitrary fixed order.

## 6. Independent verification boundary

The accompanying checker evaluates (4) by exact rational arithmetic and
compares it, without reusing (11), to the adjacent general affine-stratum
engine.  That engine enumerates plus, minus, and inactive labels and
integrates each stratum by inclusion--exclusion.  It also compares (8) with
the independent series sum of (15)--(16).  These computations corroborate
the algebra and finite-$N$ identity; the proof above establishes the
theorems for every admissible parameter.
