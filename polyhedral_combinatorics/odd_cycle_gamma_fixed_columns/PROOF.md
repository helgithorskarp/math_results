# Fixed-column Perron dominance for odd-cycle gamma coefficients

## 1. The finite coefficient formula

For `N >= 1`, let

\[
A_N=(\mathbf 1_{r+s\le N-1})_{0\le r,s<N},\qquad
p_m(N)=\operatorname {tr}(A_N^m).
\]

The adjacent spectral-to-gamma theorem proves that, for odd
`m = 2q+1` and `0 <= j <= q`,

\[
\gamma_{m,j}=
\sum_{n=0}^j c_{j-n}(m,j)p_m(n+1),                       \tag{1}
\]

where

\[
c_r(m,j)=[t^r](1-t)^{m+2}(1+t)^{2j+1-m}.                \tag{2}
\]

For fixed `j,r`, this is a polynomial in `m` of degree at most `r`.  Indeed,

\[
(1-t)^{m+2}(1+t)^{2j+1-m}
=(1-t)^2(1+t)^{2j+1}
 \exp\!\left(m\log {1-t\over1+t}\right),               \tag{3}
\]

and extracting a fixed power of `t` from the formal series gives the claim.
The two leading coefficients needed below are

\[
c_0(m,j)=1,\qquad c_1(m,j)=2j-2m-1.                    \tag{4}
\]

## 2. An explicit C-finite annihilator

Write

\[
\chi_N(X)=\det(XI-A_N).
\]

Cayley--Hamilton, followed by taking traces, says that the sequence
`m -> p_m(N)` is annihilated by `chi_N(E)`, where `E f(m)=f(m+1)`.
More generally, if a sequence is a linear combination of terms
`lambda^m` and `a(m)` is a polynomial of degree at most `d`, then their
product is annihilated by the corresponding characteristic polynomial to
the power `d+1`.  This also follows directly by repeatedly applying
`E-lambda` to `a(m)lambda^m`.

Define `g_j(m)` for all nonnegative `m` by the right side of (1), using
the polynomial interpretation of (2).  The summand with `N=n+1` has a
polynomial multiplier of degree at most `j+1-N`.  Hence

\[
\boxed{
Q_j(E)g_j=0,
\qquad
Q_j(X)=\prod_{N=1}^{j+1}\chi_N(X)^{j+2-N}.}             \tag{5}
\]

This is an explicit, generally nonminimal, constant-coefficient recurrence.
Its order is

\[
\deg Q_j=\sum_{N=1}^{j+1}N(j+2-N)=\binom{j+3}{3}.       \tag{6}
\]

On admissible odd indices, `g_j(m)=gamma_{m,j}` by (1).

## 3. The spectral hierarchy

The eigenvalues of the real symmetric matrix `A_N` are

\[
\lambda_{N,k}=
{(-1)^{k-1}\over
 2\sin((2k-1)\pi/(4N+2))},\qquad 1\le k\le N.           \tag{7}
\]

For completeness, these are obtained by substituting the elementary sine
solutions in `A_N v=lambda v`; equivalently, they are the reciprocal roots
of the Chebyshev determinant recurrence

\[
D_{N+2}(z)=(2-z^2)D_N(z)-D_{N-2}(z),\qquad
D_N(z)=\det(I-zA_N),                                    \tag{8}
\]

with `D_0=1`, `D_1=1-z`, `D_2=1-z-z^2`, and
`D_3=1-2z-z^2+z^3`.

The Perron root is therefore

\[
\rho_N=\lambda_{N,1}={1\over2\sin(\pi/(4N+2))}.        \tag{9}
\]

It is strictly increasing in `N`.  All other eigenvalues of `A_N` have
modulus at most

\[
\sigma_N={1\over2\sin(3\pi/(4N+2))}<\rho_N.            \tag{10}
\]

Consequently

\[
p_m(N)=\rho_N^m+O_N(\sigma_N^m).                        \tag{11}
\]

Two elementary angle comparisons sharpen the hierarchy.  For `j >= 2`,

\[
\sigma_{j+1}<\rho_{j-1},\qquad \sigma_j<\rho_{j-1};    \tag{12}
\]

for example, the first is equivalent (all angles lie in `(0,pi/2)`) to
`pi/(4j-2) < 3pi/(4j+6)`, which is exactly `j>3/2`.

## 4. Perron dominance and the first correction

Separate the terms `n=j` and `n=j-1` in (1), and use (4):

\[
\gamma_{m,j}=p_m(j+1)-(2m-2j+1)p_m(j)
 +\sum_{n=0}^{j-2}c_{j-n}(m,j)p_m(n+1).                 \tag{13}
\]

For fixed `j >= 2`, equations (3), (11), and (12) show that the final sum,
together with the non-Perron parts of the first two traces, is

\[
O_j(m^j\rho_{j-1}^m).                                   \tag{14}
\]

Since `rho_{j-1}<rho_j`, this is `o(m rho_j^m)`.  Thus

\[
\boxed{
\gamma_{m,j}=\rho_{j+1}^{\,m}
 -(2m-2j+1)\rho_j^{\,m}
 +o(m\rho_j^{\,m})}                                    \tag{15}
\]

as `m` tends to infinity through admissible odd values.

When `j=1`, equation (13) has no final sum, `p_m(1)=1`, and the other
eigenvalue of `A_2` has modulus less than one.  Hence (15) holds in that
case as well.

Dividing (15) first by `rho_{j+1}^m` and then subtracting from its leading
term gives

\[
\lim_{\substack{m\to\infty\\m\ {\rm odd}}}
 {\gamma_{m,j}\over\rho_{j+1}^m}=1,
\qquad
\lim_{\substack{m\to\infty\\m\ {\rm odd}}}
 {\rho_{j+1}^m-\gamma_{m,j}\over m\rho_j^m}=2.         \tag{16}
\]

The first limit proves that, for every fixed `j`, there is an `M_j` such
that `gamma_{m,j}>0` for every odd `m >= M_j`.  This is an eventual theorem,
not a uniform positivity claim: the proof supplies no common control when
`j` grows with `m`.

## 5. Scope and source boundary

Hamano--Hibi--Ohsugi prove symmetry and unimodality of the rational Ehrhart
numerator for fractional stable-set polytopes, while Steingrimsson gives the
signed-permutation triangulation of the doubled polytope.  The recent cyclic
block-polytope problem asks for stronger positivity structure.  The present
argument uses the exact cycle transfer formula from the adjacent source and
adds the C-finite/Perron bridge above.  A bounded primary-source search found
no matching fixed-column gamma theorem; this is a scoped literature statement,
not a claim of exhaustive priority.

The result does not prove full gamma positivity for lengths `1 mod 4`, nor
real-rootedness.  It instead localizes any possible failure of interior
positivity to gamma indices that escape to infinity with `m`.
