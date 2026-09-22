# Complete canonical Lucas `a=2` Schur positivity

All symmetric polynomials below are in **two variables** `q,t`. Put
`e1=q+t`, `e2=qt`, and define

\[
F_0=0,\qquad F_1=1,\qquad F_{n+1}=e_1F_n+e_2F_{n-1}.
\]

Write \(\binom nk_F=F_n!/(F_k!F_{n-k}!)\). For homogeneous polynomials
of the same degree, `A >=_S B` means that `A-B` has nonnegative rational
coefficients in the two-variable Schur basis. Multiplication by a
Schur-positive polynomial preserves this order.

## Theorem

Let `3 <= b <= c`, let `N=bc` be even, and put `d=N/2`. Then

\[
D_{b,c}:=\binom{d+2}{2}_F-\binom{b+c}{b}_F
\ \ge_S\ \frac{31}{960}e_2^3F_{N-5}.                     \tag{1}
\]

Consequently

\[
[s_{(N-r,r)}]D_{b,c}=0\quad(r=0,1,2),\qquad
[s_{(N-r,r)}]D_{b,c}>0\quad(3\le r\le N/2),              \tag{2}
\]

and the coefficient at `r=3` is exactly one. Thus the entire canonical
`a=2` cone of the Lucas Bergeron--Vessenes conjecture holds, with the sign
opposite to the displayed wide-minus-thin comparison. The degenerate case
`b=2` has `d=c` and difference zero.

The proof for **every `c>=11` is symbolic**. The remaining **26 pairs** with
`3<=b<=c<=10`, `bc` even, are certified by two small, independent exact
algorithms. No unproved Gaussian unimodality assertion is used.

## 1. Gaussian layers and Lucas transport

Let `B(n,k)` denote the degree-`k(n-k)` homogenization of the ordinary
Gaussian binomial. Equivalently,

\[
B(n,k)(q,1)={n\brack k}_q.
\]

The Gaussian product formula identifies `B(n,k)` with the factorial quotient
formed from the complete symmetric functions `h_(j-1)`. The ring involution
`tau(e1)=e1`, `tau(e2)=-e2` sends `h_(j-1)` to `F_j`: this follows directly
from `h_m=e1 h_(m-1)-e2 h_(m-2)`. It therefore sends `B(n,k)` to
`binom(n,k)_F` (in the fraction field, hence in the polynomial ring).

Write

\[
H=B(b+c,b)-B(d+2,2)
  =\sum_{i=0}^{d}u_i e_2^i h_{N-2i}.                     \tag{3}
\]

Indeed, `e2^i h_(N-2i)=s_(N-i,i)`. If `A_i` counts partitions of `i`
inside the `b` by `c` rectangle, with `A_(-1)=0`, first differences give

\[
u_i=A_i-A_{i-1}-\mathbf1_{2\mid i}\qquad(0\le i\le d).  \tag{4}
\]

For the thin rectangle the first difference is `1_(i even)` throughout this
range, because

\[
(1-q){d+2\brack2}_q=
\frac{(1-q^{d+1})(1-q^{d+2})}{1-q^2}.
\]

Since `D=-tau(H)`, (3) becomes

\[
D=\sum_{i=0}^{d}(-1)^{i+1}u_i e_2^iF_{N-2i+1}.         \tag{5}
\]

## 2. The positive prefix

Let `P_b(i)` count partitions of `i` with parts in `{2,...,b}`. The product
formula

\[
(1-q){b+c\brack b}_q
=\frac{\prod_{j=1}^{b}(1-q^{c+j})}
       {\prod_{j=2}^{b}(1-q^j)}
\]

implies

\[
u_i=P_b(i)-\mathbf1_{2\mid i}\qquad(0\le i\le c).       \tag{6}
\]

For odd `i`, there is a map from partitions of `i+1` with parts in
`{2,...,b}`, other than the all-2 partition, to partitions of `i` with those
part bounds. Reduce the smallest part `r>2` by one. Each image has at most
two preimages: one may increase a 2 to 3; the only other possibility is to
increase its unique smallest part larger than two. In the latter case that
part must be unique, since it was newly created by lowering the source's
smallest non-2 part. Hence

\[
P_b(i+1)-1\le2P_b(i).                                    \tag{7}
\]

For a complete odd/even pair in (6), set `A=u_i`, `C=2u_i-u_(i+1)`.
Both are nonnegative. With `m=N-2i+1`, its contribution to (5) is

\[
e_2^i\{A(F_m-2e_2F_{m-2})+C e_2F_{m-2}\}.              \tag{8}
\]

All `F_j` are Schur-positive by their recurrence. Moreover, for `m>=3`,

\[
F_m-2e_2F_{m-2}
=(e_1^2-e_2)F_{m-2}+e_1e_2F_{m-3}
=s_{(2)}F_{m-2}+e_1e_2F_{m-3}\ge_S0.                    \tag{9}
\]

Thus every complete pair (8) is Schur-positive.

Assume now `c>=11`, and retain the prefix `0<=i<=11`. Its first three
coefficients vanish. Since `u_3=1`, its first nonzero block (`i=3,4`) is

\[
e_2^3F_{N-5}\quad(b=3),\qquad
e_2^3(F_{N-5}-e_2F_{N-7})\quad(b\ge4).                  \tag{10}
\]

Put `G=e2^3 F_(N-5)`. By (9), the second expression in (10) is at least
`G/2`; the first is `G`. The pairs `(5,6),(7,8),(9,10)` are nonnegative
by (8), and the remaining odd term at 11 is nonnegative by (6). Therefore

\[
\sum_{i=0}^{11}(-1)^{i+1}u_i e_2^iF_{N-2i+1}
\ge_S\frac12G.                                         \tag{11}
\]

This is the stable-window mechanism from the earlier graph result, included
here with its proof rather than imported as an unexplained dependency.

## 3. A uniform envelope for every later layer

Let `p(i)` be the unrestricted partition number. Since
`0<=A_i<=p(i)`, equation (4) gives, for `i>=2`,

\[
-p(i-1)-1\le u_i\le p(i).
\]

Appending a part 1 injects partitions of `i-1` into partitions of `i`.
The one-part partition `(i)` is outside that image when `i>=2`. Consequently
`p(i)>=p(i-1)+1`, so

\[
|u_i|\le p(i)\qquad(i\ge2).                              \tag{12}
\]

In particular, we do **not** need either unimodality of the Gaussian binomial
or positivity of its difference with the thin rectangle.

Iterating (9), for `3<=i<=d`, gives

\[
e_2^iF_{N-2i+1}\ \le_S\ 2^{3-i}G.                       \tag{13}
\]

This is an inequality in the Schur cone, not merely an inequality after
setting `q=t=1`. In particular, (12)--(13) bound any sign in the tail of
(5):

\[
\sum_{i=12}^{d}(-1)^{i+1}u_i e_2^iF_{N-2i+1}
\ \ge_S\ -8\left(\sum_{i=12}^{\infty}\frac{p(i)}{2^i}\right)G.
                                                               \tag{14}
\]

## 4. An exact rational tail budget

Euler's partition product, absolutely convergent at `1/2`, gives

\[
P(1/2):=\sum_{i\ge0}\frac{p(i)}{2^i}
=\prod_{j\ge1}(1-2^{-j})^{-1}.
\]

The elementary inequality `prod(1-x_j)>=1-sum x_j` for nonnegative `x_j`
applies to every finite tail and passes to its limit. Since
`sum_(j>=7) 2^(-j)=1/64`,

\[
P(1/2)\le
\frac{64}{63}\prod_{j=1}^{6}(1-2^{-j})^{-1}
=\frac{134217728}{38757285}<\frac{52}{15}.               \tag{15}
\]

For `0<=i<=11` the partition numbers are

```text
1, 1, 2, 3, 5, 7, 11, 15, 22, 30, 42, 56,
```

obtained, for example, by expanding the first eleven Euler factors through
degree 11. Their weighted sum is `1745/512`. Thus

\[
8\sum_{i\ge12}\frac{p(i)}{2^i}
<8\left(\frac{52}{15}-\frac{1745}{512}\right)
=\frac{449}{960}<\frac12.                               \tag{16}
\]

Combining (11), (14), and (16) proves (1) for every `c>=11`, because
`1/2-449/960=31/960`.

## 5. Complete finite boundary, not an extrapolation

The unhandled pairs are exactly

```text
c=4:  b=3,4
c=5:  b=4
c=6:  b=3,4,5,6
c=7:  b=4,6
c=8:  b=3,4,5,6,7,8
c=9:  b=4,6,8
c=10: b=3,4,5,6,7,8,9,10.
```

There is no admissible `c=3` pair. `verify.py` checks every Schur
coefficient of all 26 comparisons (612 coefficients in total; maximum
degree 100) and of `960D-31G`. Two mathematically different implementations
agree **entry by entry**:

1. `layers.py` builds the Gaussian polynomial by
   `[n,k]=[n-1,k]+q^(n-k)[n-1,k-1]`, then uses (3)--(5) and the one-box
   Pieri recurrence for the Schur coefficients of `F_m`.
2. `direct.py` builds `F_m(q,1)` from its defining recurrence, multiplies
   literal Lucas numerator and denominator factors, performs exact monic
   polynomial division (rejecting any remainder), subtracts the two
   quotients, and extracts Schur coefficients as consecutive differences
   of the resulting palindromic polynomial. It uses no Gaussian polynomial
   or Schur-Pieri implementation.

The smallest ratio of a positive-position coefficient of `D` to the
corresponding coefficient of `G` among these cases is `149/197`, at `(4,4)`.
In particular all exceed `31/960`. The ordered records, in increasing `c`
then increasing `b`, serialize as

```text
b|c|D_0,D_1,...,D_(bc/2)\n
```

and have SHA-256

```text
1e1751f231acf03752aa07866d11690eec18673233985e10c391462839d84910
```

This finite calculation completes (1). It is small enough to rerun directly
from source; there is no omitted search, solver certificate, or external
dataset. The universal part is the symbolic reduction to these 26 pairs,
not a numerical extrapolation from them.

## 6. Strictness, initial zeros, and scope

Equations (4)--(6) give `u_0=u_1=u_2=0` and `u_3=1` for every admissible
pair (the smallest pair is `(3,4)`). In (5), an index `i>r` cannot contribute
to `s_(N-r,r)`, so the first three coefficients vanish and the fourth is one.

The recurrence for `F_(N-5)` contains the term `e1^(N-6)` with coefficient
one, and all its other terms are elementary-positive, hence Schur-positive.
Repeated one-box Pieri gives a positive coefficient on every two-row shape
of size `N-6` in `e1^(N-6)`. Multiplication by `e2^3` shifts both row lengths
by three. Thus `G` has positive coefficient at every `3<=r<=N/2`, and (1)
proves the strict part of (2).

This settles the entire `a=2` cone, not the unrestricted comparison with
arbitrary `a>=3`. No claim of elementary positivity, real-rootedness, or a
closed combinatorial model for the final coefficients is made. The constant
`31/960` is a convenient certified margin, not an optimal one.

## Trust boundary

The universal proof uses elementary partition counting, the Gaussian product
identity, the two-variable Schur/Pieri identities, the explicitly proved
partition map, and an elementary convergent product estimate. The 26 finite
base cases additionally trust the two readable Python implementations,
arbitrary-precision integer/rational arithmetic, the interpreter, OS, and
hardware. There is no floating point, CAS, optimization solver, randomized
search, imported enumeration, or large certificate. The result has not been
formalized in a proof assistant or independently peer reviewed here.
