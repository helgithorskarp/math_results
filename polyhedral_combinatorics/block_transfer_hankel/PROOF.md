# Weighted path transfers and an exact Hankel determinant

## 1. Definitions and theorem

Let `N>=1`. For weights `w_0,...,w_{N-1}`, set

\[
H_{ij}=\mathbf1_{i+j<N},\qquad D=\operatorname{diag}(w_i),\qquad C=HD,
\qquad a_k=w^T C^k\mathbf1\quad(k\ge0).
\]

Equivalently, `a_k` sums `w_{r_0}...w_{r_k}` over height sequences
`0<=r_i<N` with `r_i+r_{i+1}<N`. Put

\[
v_j=\begin{cases}j/2&j\text{ even},\\N-1-(j-1)/2&j\text{ odd},\end{cases}
\quad W=\prod_iw_i,\quad
\delta=(-1)^{N(N-1)/2},\quad \varepsilon=(-1)^{N-1}.
\]

**Theorem.** The polynomial identity

\[
\boxed{\det(a_{s+i+j})_{0\le i,j<N}
=(\delta W)^s\prod_{j=0}^{N-1}w_{v_j}^{2j+1}}
\tag{1}
\]

holds for every integer `s>=0`, over any commutative ring. If all weights
are nonzero elements of a field, the following conclusions hold:

1. `F(y)=sum_{k>=0} a_k y^k` has reduced denominator
   `Q(y)=det(I-yC)`, normalized by `Q(0)=1`, of degree exactly `N`.
   Its minimal constant-coefficient recurrence order is `N`, even if the
   recurrence is required only eventually.
2. Define
   \[
   \alpha=\varepsilon/w_{v_{N-1}},\qquad
   \beta_j=(w_{v_{j-1}}w_{v_j})^{-1}\quad(1\le j<N).
   \]
   With `p_0(x)=1`, form the monic polynomials
   \[
   p_k(x)=(x-\alpha\mathbf1_{k=N})p_{k-1}(x)
          -\beta_{k-1}p_{k-2}(x),\quad 1\le k\le N,
   \tag{2}
   \]
   omitting the second term for `k=1`. Then
   \[
   Q(y)=p_N(y)/p_N(0).\tag{3}
   \]
3. The normalized polynomial `Q` determines the entire ordered nonzero
   vector `w`, by the explicit rational inverse in Section 5. This works
   in every characteristic, including two.

For positive real weights, (2) is a finite Jacobi orthogonal-polynomial
system. All `N` roots of `Q` are real, simple, nonzero, and occur as poles
of `F`. These are statements in the **length variable** `y`.

The inverse-Jacobi method is classical: see Holtz, equations (7)--(10)
and their subsequent reconstruction, and Holtz--Tyaglov, Section 1.4,
listed in [SOURCES.md](SOURCES.md). We prove all needed identities to make
the weighted path specialization independently checkable.

## 2. The inverse transfer is a path matrix

Let `R` reverse the coordinate order, and let `L` be the lower triangular
matrix of ones. Then `H=RL`. Its inverse is `BR`, where `B=L^{-1}` has
ones on the diagonal and minus ones on the first subdiagonal. Consequently

\[
\det H=\delta,\qquad C^{-1}=D^{-1}BR.\tag{4}
\]

The only nonzero entries of `BR` are `+1` on `i+j=N-1` and `-1` on
`i+j=N`. In the signed zigzag basis

\[
f_j=\sigma_j e_{v_j},\qquad \sigma_j=(-1)^{j(j-1)/2},
\]

the matrix of `C^{-1}` is tridiagonal, with all diagonal entries zero
except the last, equal to `alpha`, and with

\[
T_{j-1,j}=1/w_{v_{j-1}},\qquad
T_{j,j-1}=1/w_{v_j}\quad(1\le j<N).\tag{5}
\]

Indeed, the zigzag traversal alternately follows the two anti-diagonals;
the edge signs before conjugation alternate `+,-,+,-,...`, and
`sigma_{j-1}sigma_j=(-1)^{j-1}` removes them. The final loop comes from
`i+j=N-1` for odd `N`, and `i+j=N` for even `N`, giving `epsilon`.
These entrywise statements hold over any field.

Expanding the characteristic polynomial of each leading principal
tridiagonal block proves (2). Also

\[
\det(I-yC)=\frac{\det(C^{-1}-yI)}{\det C^{-1}}
=\frac{p_N(y)}{p_N(0)},
\]

proving (3). In particular `p_N(0)` is nonzero. Notice that the `p_k`
in (2) belong to a fixed `N`-dimensional system; this is not a claim that
the systems for different `N` share one fixed orthogonality measure.

For positive real weights, let

\[
S=D^{1/2}HD^{1/2},\qquad u=(\sqrt{w_0},...,\sqrt{w_{N-1}})^T.
\]

Then `a_k=u^T S^k u`. If `U` has columns `f_j`, the real symmetric
matrix `J=U^T S^{-1}U` has terminal diagonal `alpha` and positive
off-diagonals

\[
c_j=\sqrt{\beta_j}\quad(1\le j<N).\tag{6}
\]

This is the Jacobi matrix for (2). Its endpoint is cyclic: an eigenvector
whose first coordinate vanishes has every coordinate zero by successive
rows of its eigenvalue equation. Symmetry then implies that all
eigenvalues are simple. They are nonzero since `J` is invertible.

## 3. Proof of the full Hankel product

First assume positive real weights. Write `A=J^{-1}` and `u'=U^Tu`.
As `Ue_0=e_0` and `Se_0=sqrt(w_0)u`, we have

\[
u'=Ae_0/\sqrt{w_0},\qquad a_k=(u')^TA^ku'.\tag{7}
\]

Let

\[
K=[u',Au',...,A^{N-1}u'],\quad
E=[e_0,Ae_0,...,A^{N-1}e_0],\quad
V=[e_0,Je_0,...,J^{N-1}e_0].
\]

The tridiagonal support shows that `V` is upper triangular, with diagonal
entry `c_1...c_j` in column `j`. Hence

\[
\det V=\prod_{j=1}^{N-1}c_j^{N-j}.\tag{8}
\]

The columns of `J^{N-1}E` are those of `V` in reverse order, so

\[
\det E=\delta(\det J)^{-(N-1)}\det V,
\qquad K=AE/\sqrt{w_0}.
\]

Since `det A=det C=delta W`, it follows that

\[
(\det K)^2
=W^{2N}w_0^{-N}\prod_{j=1}^{N-1}\beta_j^{N-j}
=\prod_{j=0}^{N-1}w_{v_j}^{2j+1}.\tag{9}
\]

For the last equality, `w_{v_0}=w_0` has exponent
`2N-N-(N-1)=1`; each interior `w_{v_j}` has exponent
`2N-(N-j)-(N-j-1)=2j+1`; and the last has exponent `2N-1`.
For `N=1` the expression is directly `w_0`.

The Hankel matrix in (1) equals `K^T A^s K`. Taking determinants gives
(1) for positive weights. Both sides of (1), for fixed `N,s`, are
polynomials with integer coefficients in the weights. Their equality on
the positive real orthant proves equality in `Z[w_0,...,w_{N-1}]`.
Specialization proves (1) over every commutative ring, including at zero
weights. The inverse formulas and nonvanishing conclusions, however,
require nonzero weights over a field.

## 4. Minimal denominator and positive spectral weights

Over a field with nonzero weights, (1) is nonzero for every shift `s`.
The resolvent identity gives

\[
F(y)=\frac{w^T\operatorname{adj}(I-yC)\mathbf1}{Q(y)},
\qquad\deg Q=N,
\]

and Cayley--Hamilton provides a recurrence of order `N`. Any recurrence
of order `r<N` valid from some index onward would, at a sufficiently
large shift, express columns `r,...,N-1` of the Hankel matrix as
combinations of its first `r` columns. This contradicts (1). Cancellation
in the fraction would likewise give a recurrence of smaller order.
Thus the displayed fraction is reduced and the order is minimal even
eventually. Any representation `a_k=b^TM^kc` of dimension less than `N`
would give a smaller recurrence and is also impossible.

For positive real weights, put

\[
m(y)=e_0^T(J-yI)^{-1}e_0.
\]

The resolvent identity and (7) give

\[
m(0)=w_0,\qquad
F(y)=\frac{m(y)-w_0}{w_0y}.\tag{10}
\]

At `y=0` the expression is interpreted by its removable limit. Successive
Schur complements give the Jacobi continued fraction

\[
m(y)=\cfrac{1}{-y-\cfrac{\beta_1}{-y-\cfrac{\beta_2}{
\ddots-\cfrac{\beta_{N-1}}{\alpha-y}}}}\quad(N\ge2),\tag{11}
\]

and `m(y)=1/(alpha-y)` if `N=1`. If `(theta_r,z_r)` are the normalized
real eigenpairs of `J`, and `lambda_r=theta_r^{-1}`, then (7) yields

\[
F(y)=\sum_{r=1}^N\frac{A_r}{1-\lambda_ry},\qquad
A_r=\frac{\lambda_r^2 z_r(0)^2}{w_0}>0.\tag{12}
\]

All roots of `Q` are therefore simple real visible poles. The measure
here need not be supported on the positive half-line; we use a Jacobi,
not a positive-half-line Stieltjes, interpretation. The leading
principal characteristic polynomials `p_0,...,p_{N-1}` are orthogonal
for the endpoint spectral measure of `J`; `p_N` vanishes on its support.

## 5. Recovering the ordered weights

This is the parity reconstruction of the classical inverse-Jacobi
problem, applied to the explicit parameters in (5). Suppose `Q` is
known to come from nonzero weights over a field. Divide it by its leading
coefficient to obtain the monic polynomial `p_N`. Then

\[
\alpha=-[x^{N-1}]p_N(x)\ne0.\tag{13}
\]

For `k<N`, recurrence (2) gives only powers of the parity of `k` in
`p_k`. Let `opp_N` select coefficients whose degrees have parity opposite
to `N`. For `N>1`,

\[
p_{N-1}=-\operatorname{opp}_N(p_N)/\alpha.\tag{14}
\]

Selection of coefficients uses no division by two and remains valid in
characteristic two. For `k=N,N-1,...,2`, compute

\[
r_k=(x-\alpha\mathbf1_{k=N})p_{k-1}-p_k
    =\beta_{k-1}p_{k-2}.
\]

The nonzero leading coefficient of `r_k` is `beta_{k-1}`; divide by it to
recover the next monic polynomial. Finally recover the weights backwards:

\[
w_{v_{N-1}}=\varepsilon/\alpha,\qquad
w_{v_{j-1}}=1/(\beta_jw_{v_j})\quad(j=N-1,...,1).\tag{15}
\]

For `N=1`, (13) and the first formula in (15) suffice. These formulas
prove injectivity of `w -> Q` on nonzero ordered weight vectors. We do
not claim a classification of the image among arbitrary polynomials.

When `N` is known, the first `2N` counts also determine the weights: solve
the nonsingular Hankel system

\[
\sum_{j=0}^{N-1}b_j a_{i+j}=-a_{i+N}\quad(0\le i<N).
\]

Its solution is the unique order-`N` recurrence, giving
`Q(y)=1+b_{N-1}y+...+b_0y^N`, then apply (13)--(15).

## 6. Path-block Ehrhart specialization and limits

Take integers `a>=1,q>=0`. A block is a vector of `a` nonnegative
integer coordinates of sum at most `q`. Adjacent block sums must add to
at most `q`. The one-block convention is the simplex of sum at most `q`.
There are

\[
w_j=\binom{j+a-1}{a-1}
\]

blocks of sum `j`, so the lattice count of `m` blocks is
`L_m^(a)(q)=a_{m-1}` with `N=q+1`. The compression itself is prior art
(Jiang--Yang--Zhong, Theorem 1.1). Equation (1) now supplies an explicit
nonzero determinant for `det(L_{s+i+j+1}^(a)(q))`. Therefore the visible
denominator of their Theorem 1.3 is always reduced in characteristic zero,
and their length recurrence has exact minimal order `q+1` for every
width. Formula (2) supplies the finite orthogonal-polynomial description
asked for in the length-direction portion of their Problem 3, uniformly
in `a`. It does not identify these polynomials with a named classical
family or claim a closed-form spectrum for arbitrary weights.

The theorem concerns a fixed dilation and varying number of blocks.
It makes no claim about gamma-positivity, the real-rootedness of an
Ehrhart `h*`-polynomial, or odd-cycle numerator unimodality. Unit weights
already have explicit older transfer and continued-fraction formulas.
General Jacobi inversion and moment-rank theory are also prior art.
Zero weights are allowed in the polynomial identity only; the exact
minimal order in their presence is not classified here. Finite audits
corroborate identities but do not prove their universal quantifiers.
