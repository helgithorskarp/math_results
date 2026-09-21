# The universal pre-numerator theorem

## Statement

Put `e1=q+t`, `e2=qt`, and define

\[
F_0=0,\qquad F_1=1,\qquad F_{n+1}=e_1F_n+e_2F_{n-1}.
\]

Let \(\left\{\begin{smallmatrix}n\\k\end{smallmatrix}\right\}_F\)
be the corresponding Lucas binomial.  Suppose

\[
3\le b\le c,\qquad 2\mid bc,\qquad d=bc/2,
\]

and set \(N=bc\) and

\[
D_{b,c}=
\left\{\begin{matrix}d+2\\2\end{matrix}\right\}_F-
\left\{\begin{matrix}b+c\\b\end{matrix}\right\}_F.
\tag{1}
\]

This is the forced-sign normalization of the canonical
\((a,b,c,d)=(2,b,c,bc/2)\) Lucas Bergeron--Vessenes comparison.

**Theorem.** For every admissible \((b,c)\),

\[
[s_{(N-r,r)}]D_{b,c}=0\quad(0\le r\le2),
\tag{2}
\]

and

\[
[s_{(N-r,r)}]D_{b,c}>0\quad(3\le r\le c).
\tag{3}
\]

In particular, \([s_{(N-3,3)}]D_{b,c}=1\).

## Gaussian layers

Let \(B(n,k)\) be the homogeneous two-variable lift of the Gaussian
binomial, and put

\[
H=B(b+c,b)-B(d+2,2).
\]

Every homogeneous symmetric polynomial of degree \(N\) has a unique
lower-half expansion

\[
H=\sum_{0\le i\le N/2}u_i e_2^i h_{N-2i},
\qquad
u_i=[q^i](1-q)H(q,1).
\tag{4}
\]

For \(n\ge0\), let

\[
P_b(n)=\#\{(m_2,\ldots,m_b)\in\mathbb N^{b-1}:
                 2m_2+\cdots+bm_b=n\}.
\tag{5}
\]

The product formula gives

\[
(1-q){b+c\brack b}_q
=\frac{\prod_{j=1}^{b}(1-q^{c+j})}
        {\prod_{j=2}^{b}(1-q^j)}.
\]

No numerator factor is active through degree \(c\).  Also \(c\le d\), so

\[
(1-q){d+2\brack2}_q
=\frac{(1-q^{d+1})(1-q^{d+2})}{1-q^2}
\]

has coefficient one at even degrees and zero at odd degrees throughout the
same range.  Consequently

\[
\boxed{u_i=P_b(i)-\mathbf1_{2\mid i}\qquad(0\le i\le c).}
\tag{6}
\]

In particular,

\[
u_0=u_1=u_2=0,\qquad u_3=1.
\tag{7}
\]

## The two-to-one partition map

For every odd \(n\ge1\),

\[
P_b(n+1)-1\le2P_b(n).
\tag{8}
\]

Indeed, view \(P_b(n+1)-1\) as counting the partitions of the even integer
\(n+1\) with parts in \(\{2,\ldots,b\}\), excluding the all-2 partition.
Given such a partition \(\lambda\), let \(r\ge3\) be its smallest part
larger than two and replace one copy of \(r\) by \(r-1\).  This produces a
partition \(\phi(\lambda)\) of \(n\) with the same allowed part bounds.

Fix an image \(\mu\).  A preimage with selected part \(r=3\), if it exists,
is uniquely obtained by changing one 2 into a 3.  A preimage with \(r>3\),
if it exists, is uniquely obtained by increasing the unique smallest part of
\(\mu\) larger than two; the defining minimality forces that part to occur
once.  These are the only two possible preimage types.  Thus every fibre of
\(\phi\) has size at most two, proving (8).

Combining (6) and (8), for every complete odd/even pair
\(i=2j+1,i+1\le c\),

\[
A_j:=u_{2j+1}\ge0,
\qquad
C_j:=2u_{2j+1}-u_{2j+2}\ge0.
\tag{9}
\]

## Lucas transport and positive adjacent blocks

Let \(\tau(e_1)=e_1\), \(\tau(e_2)=-e_2\).  The standard Lucas
anti-involution satisfies

\[
\tau(h_m)=F_{m+1},\qquad
\tau(B(n,k))=\left\{\begin{matrix}n\\k\end{matrix}\right\}_F.
\]

Equations (1) and (4) therefore give

\[
D_{b,c}=-\tau(H)
=\sum_i(-1)^{i+1}u_i e_2^iF_{N-2i+1}.
\tag{10}
\]

Pair the terms indexed by \(i=2j+1\) and \(i+1\).  If
\(m=N-2i+1\), their sum is

\[
e_2^i\left(A_jF_m-u_{i+1}e_2F_{m-2}\right)
=e_2^i\left(
A_j(F_m-2e_2F_{m-2})+C_je_2F_{m-2}
\right).
\tag{11}
\]

Both kernels in (11) are Schur-positive.  Schur positivity of every \(F_m\)
follows already from its recurrence in the Schur-positive generators
\(e_1,e_2\).  For the other kernel, write

\[
\ell(n,r)=[s_{(n-r,r)}]F_{n+1},
\]

with out-of-range values zero.  Two applications of the Lucas recurrence
and the one-box Pieri rule give

\[
[s_{(m-1-r,r)}](F_m-2e_2F_{m-2})
=\ell(m-2,r)+\ell(m-3,r-2)+\ell(m-4,r-2)\ge0.
\tag{12}
\]

Thus every complete block whose indices lie at most \(c\) is
Schur-positive.  If \(c\) is odd, its final unpaired term is
\(u_c e_2^cF_{N-2c+1}\), also Schur-positive.  Every term in (10) with
index greater than \(c\) is divisible by \(e_2^{c+1}\), so it cannot affect
a two-row Schur coefficient having second row at most \(c\).  Equations
(7), (9)--(12) prove nonnegativity in (2)--(3).

For strictness, the first block starts at \(i=3\).  Since

\[
u_4=\begin{cases}0,&b=3,\\1,&b\ge4,\end{cases}
\]

that block is respectively

\[
e_2^3F_{N-5}
\quad\text{or}\quad
e_2^3(F_{N-5}-e_2F_{N-7})=e_2^3e_1F_{N-6}.
\tag{13}
\]

In either case the monomial \(e_1^{N-6}\) occurs with coefficient one.
Repeated one-box Pieri gives a positive coefficient for every two-row shape
of degree \(N-6\) in \(e_1^{N-6}\); after multiplication by \(e_2^3\), the
block therefore has positive coefficient on every two-row shape whose second
row is at least three.  All remaining relevant blocks are nonnegative.  This
proves (3), and the coefficient at second-row size three is visibly one.

## Boundary and limitation

The threshold \(c\) is structural: degree \(c+1\) is where the first
numerator translate from \({b+c\brack b}_q\) enters (6).  The theorem makes
no sign assertion for \(r>c\).  Extending the result requires controlling
those translated restricted-partition layers, rather than merely increasing
a finite verification range.
