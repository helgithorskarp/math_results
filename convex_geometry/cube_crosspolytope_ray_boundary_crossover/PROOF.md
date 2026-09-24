# Exact Legendre law at the ray boundary

## 1. Geometric statement

Let

\[
g(x)=(|x|-1)_+,
\qquad
A_N(\theta,\rho)=\int_{\mathbb R^N}
 \delta\!\left(\sum_i x_i-\theta N\right)
 \mathbf1_{\{\sum_i g(x_i)\leq\rho N\}}\,dx,              \tag{1}
\]

and, for $N=n+1$, set

\[
D_n(\theta,\rho)=\frac{n!}{N^n}A_N(\theta,\rho).           \tag{2}
\]

Thus $A_N$ is $1/\sqrt N$ times the Euclidean volume of the
corresponding affine section of $[-1,1]^N+\rho N B_1^N$.

**Theorem 1 (exact Legendre segment).**  Let $N\geq2$, $|\theta|>1$, and
$m=|\theta|-1$.  Throughout the complete first boundary segment

\[
m\leq\rho\leq m+\frac2N,                                  \tag{3}
\]

one has

\[
\boxed{
D_{N-1}(\theta,\rho)
=m^{N-1}P_{N-1}\!\left(\frac{2\rho}{m}-1\right),}         \tag{4}
\]

where $P_{N-1}$ is the Legendre polynomial.  Equivalently,

\[
\frac{A_N(\theta,\rho)}{A_N(\theta,m)}
=P_{N-1}\!\left(\frac{2\rho}{m}-1\right),
\qquad
A_N(\theta,m)=\frac{(mN)^{N-1}}{(N-1)!}.                  \tag{5}
\]

This is an exact finite-dimensional identity.  In particular, the normalized
section on this segment depends on the offset only through $\rho/m$ and is
unchanged by reflection of $\theta$.

For the boundary scaling

\[
\rho=m(1+z/N^2),\qquad z\geq0,                            \tag{6}
\]

write

\[
Q_N(z)=P_{N-1}(1+2z/N^2).                                 \tag{7}
\]

The geometric identity applies when $mz/N\leq2$.

## 2. Finite-$N$ Bessel bounds and monotonicity

Put

\[
\mathcal F(z)=\sum_{r=0}^{\infty}\frac{z^r}{(r!)^2}
=I_0(2\sqrt z),
\qquad K=z\frac d{dz}.                                    \tag{8}
\]

**Theorem 2 (monotone Bessel approximation).**  For every $N\geq2$ and
$z\geq0$,

\[
\boxed{
0\leq \mathcal F(z)-Q_N(z)
\leq \frac{K\mathcal F(z)}N
 +\frac{(K^3-K)\mathcal F(z)}{3N^2},}                     \tag{9}
\]

and

\[
\boxed{
Q_N(z)\leq \mathcal F((1-1/N)z)\leq\mathcal F(z).}       \tag{10}
\]

For $z>0$, the sequence is strictly increasing:

\[
Q_2(z)<Q_3(z)<\cdots<\mathcal F(z),                       \tag{11}
\]

and therefore converges to the Bessel function from below.  All inequalities
become equalities at $z=0$; the second inequality in (10) and the upper
comparison with $Q_N$ are strict for $z>0$.

## 3. Complete asymptotic recursion

Define

\[
L_0=z\partial_z^2+\partial_z-1,
\qquad L_2=z^2\partial_z^2+2z\partial_z.                  \tag{12}
\]

**Theorem 3 (all-order holonomic expansion).**  For every fixed $J\geq0$,

\[
Q_N(z)=\sum_{j=0}^J\frac{\Psi_j(z)}{N^j}+O(N^{-J-1})      \tag{13}
\]

locally uniformly for $z\in[0,\infty)$.  The entire coefficient functions
are determined recursively by

\[
\boxed{
L_0\Psi_j=-\Psi_{j-1}-L_2\Psi_{j-2},}                    \tag{14}
\]

where $\Psi_{-1}=\Psi_{-2}=0$, together with

\[
\begin{aligned}
&\Psi_0(0)=1,\quad \Psi_j(0)=0\quad(j\geq1),\\
&\Psi_0'(0)=1,\quad\Psi_1'(0)=-1,
 \quad\Psi_j'(0)=0\quad(j\geq2).                        \tag{15}
\end{aligned}
\]

The first three terms are

\[
\boxed{\begin{aligned}
\Psi_0(z)&=I_0(2\sqrt z),\\
\Psi_1(z)&=-K\mathcal F(z)=-\sqrt z\,I_1(2\sqrt z),\\
\Psi_2(z)&=\frac{z\mathcal F(z)-(2z+1)K\mathcal F(z)}6.
\end{aligned}}                                           \tag{16}
\]

This both makes every order constructive and supplies the new explicit
$N^{-2}$ coefficient.

## 4. The geometric gap and exact integral

Reflection reduces the proof of Theorem 1 to $\theta=1+m$.  Classify
coordinates as

\[
x_i=1+e_i\quad\hbox{(plus tail)},\qquad
x_i=1-y_i\quad\hbox{(inactive)},\qquad
x_i=-1-e_i\quad\hbox{(minus tail)},                       \tag{17}
\]

where $e_i\geq0$ and $0\leq y_i\leq2$.  Suppose there are $k$ inactive
coordinates and $q$ minus-tail coordinates.  If $P,Q,Y$ are the sums of plus
excesses, minus excesses, and inactive deficits, the affine constraint and
radial cost give

\[
P=mN+Y+2q+Q,
\qquad P+Q=mN+Y+2q+2Q.                                   \tag{18}
\]

The extra budget in (6) is $mz/N$.  When $mz/N<2$, (18) forces $q=0$ and
$Y\leq mz/N<2$, so all individual bounds $y_i\leq2$ are automatic.  At the
endpoint $mz/N=2$, every newly possible minus-tail stratum has $Q=Y=0$ and
hence zero $(N-1)$-dimensional section measure.  Thus the same formula holds
through equality.

Choose the $k$ inactive labels.  Delta integration over the remaining
$N-k\geq1$ positive excesses gives

\[
A_N(1+m,m(1+z/N^2))
=\sum_{k=0}^{N-1}\binom Nk\frac1{(N-k-1)!}
 \int_{\substack{y_i\geq0\\\sum y_i\leq mz/N}}
 (mN+\textstyle\sum y_i)^{N-k-1}dy.                       \tag{19}
\]

The $k=0$ term is the boundary value in (5).  Divide by it, substitute
$y_i=ms_i$ and then $t_i=Ns_i$, and integrate first over
$t=\sum_i t_i$.  This yields

\[
Q_N(z)=1+\sum_{k=1}^{N-1}
 \frac{(N)_k(N-1)_k}{k!N^{2k}(k-1)!}
 \int_0^z t^{k-1}\left(1+\frac t{N^2}\right)^{N-k-1}dt, \tag{20}
\]

where $(u)_k$ is a falling factorial.  This proves exact offset cancellation
before any asymptotic limit is taken.

## 5. Vandermonde collapse to a Legendre polynomial

Expand the integrand in (20).  For $1\leq r\leq N-1$, its $z^r$
coefficient is

\[
\frac{(N-1)_r}{r!N^{2r}}
 \sum_{k=1}^r\binom Nk\binom{r-1}{k-1}.                  \tag{21}
\]

Vandermonde's identity gives

\[
\sum_{k=1}^r\binom Nk\binom{r-1}{k-1}
=\binom{N+r-1}{r}.                                       \tag{22}
\]

Consequently

\[
Q_N(z)=\sum_{r=0}^{N-1}\frac{(N-1)_rN^{\overline r}}
{(r!)^2N^{2r}}z^r
={}_2F_1(1-N,N;1;-z/N^2),                                \tag{23}
\]

where $N^{\overline r}=N(N+1)\cdots(N+r-1)$.  The standard
hypergeometric representation

\[
P_n(x)={}_2F_1(-n,n+1;1;(1-x)/2)                         \tag{24}
\]

turns (23) into (7), proving Theorem 1.

## 6. Coefficient factorization and the global bounds

Write the coefficient in (23) as $c_{N,r}z^r/(r!)^2$.  For
$0\leq r\leq N-1$,

\[
\begin{aligned}
c_{N,r}
&=\prod_{j=1}^r(1-j/N)(1+(j-1)/N)\\
&=\prod_{j=1}^r\left(1-\frac1N-\frac{j(j-1)}{N^2}\right). \tag{25}
\end{aligned}
\]

Set $c_{N,r}=0$ for $r\geq N$.  Every factor in (25) lies in $[0,1]$,
increases strictly with $N$, and is at most $1-1/N$.  Coefficientwise
comparison immediately proves (10), (11), and the first inequality in (9).

For the quantitative remainder, put

\[
a_j=\frac1N+\frac{j(j-1)}{N^2}.
\]

The elementary product inequality
$1-\prod_j(1-a_j)\leq\sum_j a_j$ gives, for $r<N$,

\[
1-c_{N,r}\leq\frac rN+\frac{r^3-r}{3N^2}.                \tag{26}
\]

For $r\geq N$, the same bound remains true because its first term is at
least one.  Multiply (26) by $z^r/(r!)^2$ and sum.  This is precisely (9).

## 7. Differential equation and asymptotic coefficients

The Legendre equation for degree $N-1$, after the substitution
$x=1+2z/N^2$, becomes the exact equation

\[
\left(z+\frac{z^2}{N^2}\right)Q_N''
+\left(1+\frac{2z}{N^2}\right)Q_N'
-\left(1-\frac1N\right)Q_N=0.                            \tag{27}
\]

Also

\[
Q_N(0)=1,
\qquad Q_N'(0)=1-1/N.                                    \tag{28}
\]

Inserting (13) into (27) and comparing powers of $N^{-1}$ proves the
recursion (14)--(15).

The product (25) independently gives

\[
c_{N,r}=1-\frac rN
-\frac{r(r-1)(2r-1)}{6N^2}+O_r(N^{-3}).                  \tag{29}
\]

Summing (29) against $z^r/(r!)^2$ gives

\[
\Psi_1=-K\mathcal F,
\qquad
\Psi_2=-\frac{2K^3-3K^2+K}{6}\mathcal F.                \tag{30}
\]

Since $L_0\mathcal F=0$, one has $K^2\mathcal F=z\mathcal F$ and
$K^3\mathcal F=z\mathcal F+zK\mathcal F$.  This reduces (30) to (16).

For arbitrary order, expand the finite product (25).  At each power of
$N^{-1}$ its coefficient is a polynomial in $r$, so $\Psi_j$ is a polynomial
in $K$ applied to $\mathcal F$ and is entire.  Uniformity on $0\leq z\leq Z$
follows by splitting at a sufficiently large multiple of
$\log N/\log\log N$: below the cutoff Taylor remainders are uniform after a
polynomial weight in $r$, while above it the majorant $Z^r/(r!)^2$ is smaller
than any prescribed power of $N^{-1}$.  This proves (13) to every fixed
order.

## 8. Verification boundary

The checker evaluates (20), (23), and the Legendre three-term recurrence by
distinct exact-rational paths.  It verifies the transformed differential
equation coefficientwise, compares the result with the general affine
plus/minus/inactive stratum engine (including the endpoint in (3)), checks
monotonicity and both Bessel bounds, and compares the explicit first two
corrections with independent 80-digit series.  These computations corroborate
the identities; the written argument proves them for all stated parameters.
