# The Lucas equal-area Schur-positivity theorem

All symmetric polynomials below have exactly two variables, `q,t`. Put
`e1=q+t`, `e2=qt`, and define

\[
 F_0=0,\qquad F_1=1,\qquad F_{n+1}=e_1F_n+e_2F_{n-1},\qquad
 \binom nk_F=\frac{\prod_{j=1}^nF_j}
 {\prod_{j=1}^kF_j\prod_{j=1}^{n-k}F_j}.
\]

Empty products are one. The quotient is a polynomial, as also follows
from the Gaussian transport below. Write `X >=_S Y` if every coefficient
of `X-Y` in the two-variable Schur basis is nonnegative. We allow rational
scalars in this order; all final polynomials have integer coefficients.

## 1. Theorem

Let `1 <= a < b <= c < d` and `ad=bc=N`. Set `I=a+1` and

\[
 D=(-1)^{a+1}\left(\binom{b+c}{b}_F-\binom{a+d}{a}_F\right),
 \qquad G=e_2^{a+1}F_{N-2a-1}.
\]

Then **`6D-G` is Schur-positive**. Moreover,

\[
 [s_{(N-r,r)}]D=0\quad(0\le r\le a),\qquad
 [s_{(N-r,r)}]D>0\quad(a+1\le r\le\lfloor N/2\rfloor),
\]

and the coefficient at `r=a+1` is exactly one.

Consequently, for all positive integers `a <= b,c <= d` with `ad=bc`,
the difference in parentheses is Schur-positive up to one global sign.
Indeed swap `b,c` if necessary. If `a=b`, equal area forces `c=d` and
the difference is zero; otherwise the theorem applies. Zero indices,
if included in the convention for the original conjecture, also give
zero: `a=0` forces `bc=0` and both binomials equal one.

This proves the positive-integer Lucas comparison in Bergeron's
Conjecture 10.1, not the ordinary Gaussian comparison. The constant `1/6`
is a convenient uniform margin, not an asserted optimum.

## 2. Gaussian transport and the first nonzero layer

Let `A_(w,h)(i)` count partitions of `i` with largest part at most `w`
and at most `h` parts; set it to zero for negative `i`. The homogeneous
Gaussian polynomial is

\[
 B_{w,h}(q,t)=\sum_{i=0}^{wh}A_{w,h}(i)q^{wh-i}t^i.
\]

It is symmetric by complementation in the rectangle. For a homogeneous
symmetric polynomial with monomial coefficient sequence `A_i`, its
coefficient at `s_(N-i,i)=e2^i h_(N-2i)` is `A_i-A_(i-1)` for
`0<=i<=floor(N/2)`. Thus, with `M=floor(N/2)`,

\[
 B_{b,c}-B_{a,d}=\sum_{i=0}^{M}u_i e_2^i h_{N-2i},\qquad
 u_i=\Delta A_{b,c}(i)-\Delta A_{a,d}(i).                 \tag{1}
\]

The algebra automorphism `tau(e1)=e1`, `tau(e2)=-e2` sends `h_m` to
`F_(m+1)`, by their recurrences. The factorial formula for Gaussian
polynomials therefore sends `B_(w,h)` to `binom(w+h,w)_F`. In particular,

\[
 D=\sum_{i=0}^{M}(-1)^{I+i}u_i L_i,\qquad
 L_i=e_2^i F_{N-2i+1}.                                  \tag{2}
\]

No positivity of the Gaussian coefficients `u_i` is assumed or needed.

Let `P_w(i)` count partitions using only parts `2,...,w`; for `w=1`
this is one at `i=0` and zero otherwise. For `i<=c`, the length caps in
both rectangles are inactive, so

\[
 u_i=P_b(i)-P_a(i)=:S_i.                                \tag{3}
\]

Equivalently, `S_i` counts partitions with parts in `2,...,b` having
at least one part greater than `a`. Hence

\[
 S_0=\cdots=S_{I-1}=0,\quad S_I=1,\quad
 S_{I+1}=\begin{cases}0&b=I,\\1&b>I.\end{cases}          \tag{4}
\]

## 3. A uniform two-to-one partition map

**Lemma.** If `i>=I` and `i` has the same parity as `I`, then
`S_(i+1) <= 2S_i`.

Take a partition counted by `S_(i+1)` and decrease its smallest part
greater than two by one. Such a part exists. For `a>=2`, membership
already requires a part greater than two. For `a=1`, the source total
`i+1` is odd, so it cannot consist entirely of twos.

The resulting parts still lie in `2,...,b`. They still include a part
greater than `a`: failure for `a>=2` would require precisely one such
part, equal to `a+1`, and all other parts equal to two. But that source
would have parity `a+1=I`, whereas `i+1` has the opposite parity. For
`a=1`, the remaining nonempty partition automatically has a part greater
than one.

A target has at most two preimages. One is obtained by raising a two to
three. The other, if it exists, is obtained by raising the unique smallest
part greater than two by one. In the latter case this smallest part is
unique because all unchanged non-two parts were at least the original
decreased part. Partitions are unlabelled, so equal twos do not give
distinct choices. This proves the lemma for all `a,b`, not just fixed `a`.

## 4. Two Lucas contraction inequalities

Every `F_m` is Schur-positive, since it is a polynomial in the Schur-positive
`e1,e2` with nonnegative coefficients. For `m>=3`,

\[
 F_m-2e_2F_{m-2}
   =s_{(2)}F_{m-2}+e_1e_2F_{m-3}\ \ge_S\ 0.             \tag{5}
\]

There is also the stronger inequality

\[
 F_m\ge_S3e_2F_{m-2}\qquad(m\ge4).                       \tag{6}
\]

To prove it, let `Q_m=F_m-3e2 F_(m-2)`. Directly,

\[
 Q_4=s_{(3)}+s_{(2,1)},\qquad Q_5=s_{(4)}+3s_{(3,1)}.
\]

For `m>=6`, `Q_m=e1 Q_(m-1)+e2 Q_(m-2)`, which preserves Schur positivity.
Inequality (6) fails at `m=3`; instead `F3-2e2 F1=s_(2)`.
Consequently, iterating (6), with at most this one final factor two,
gives for every `I<=i<=M`

\[
 L_i\le_S\frac32\,3^{I-i}G.                            \tag{7}
\]

For odd `N` the last Lucas index is two and the factor `3/2` is
unnecessary. For even `N` it covers the final transition from index
three to one. Retaining it uniformly avoids any parity exception.

## 5. Positive stable prefix

For now assume `g=c-a>=3`. Since `b>=2`, `c<=M`. Pair the terms
in (2) from `I` through `c`, starting with `I,I+1`. By (3), the
partition lemma and (5), every complete pair is Schur-positive:

\[
 S_i L_i-S_{i+1}L_{i+1}
 =S_i(L_i-2L_{i+1})+(2S_i-S_{i+1})L_{i+1}\ge_S0.
\]

The possible last unpaired term has positive sign and is nonnegative.
The first pair is `G` or `G-L_(I+1)` by (4). Its first Lucas index
`N-2I+1` is at least four: if `a=1`, then `N>=2c>=8`, giving index at
least five; if `a>=2`, then `N>=(a+1)(a+3)`, giving an even larger index.
Therefore (6) applies to this first pair, and

\[
 \sum_{i=I}^{c}(-1)^{I+i}u_iL_i\ge_S\frac23G.            \tag{8}
\]

For the later pairs we used (5), not (6): the last pair can have first
Lucas index three when `a=1,b=2`. This endpoint causes no problem.

## 6. Rectangle boundary decomposition and a shifted envelope

Write `p(j)` for the unrestricted partition number, with `p(j)=0` if
`j<0`. For a rectangle `(w,h)`, let

- `T_(w,h)(i)` count no-one partitions of `i` with largest part at most
  `w` and more than `h` parts;
- `E_(w,h)(i)` count partitions of `i-1` with largest part at most `w`
  and exactly `h` parts.

Appending a one to partitions of `i-1` with fewer than `h` parts
accounts for all partitions of `i` in the rectangle that contain a one.
It follows exactly, for every `i>=0`, that

\[
 \Delta A_{w,h}(i)=P_w(i)-T_{w,h}(i)-E_{w,h}(i).         \tag{9}
\]

Subtracting the two instances of (9) gives the uniform envelope

\[
 |u_i|\le S_i+T_{b,c}(i)+E_{b,c}(i)+T_{a,d}(i)+E_{a,d}(i).
                                                               \tag{10}
\]

Each term has a shifted partition bound:

\[
 S_i\le p(i-I),\quad E_{w,h}(i)\le p(i-h-1),\quad
 T_{w,h}(i)\le\sum_{\ell\ge h+1}p(i-2\ell).              \tag{11}
\]

For the first, remove the largest part `v>=I`; the remainder is a no-one
partition. If `p_no1(j)=p(j)-p(j-1)`, summing over `v>=I` bounds the
number by `sum_(j=0)^(i-I) p_no1(j)=p(i-I)`. For the second, subtract
one from each of the `h` parts. For the third, fix the length `ell>h`
and subtract two from every part. In the last two operations, discard
zeros; the fixed original length makes each map injective. Dropping the
remaining length and width bounds only increases the number counted.

This shifted estimate is the essential improvement over an unshifted
bound such as `p(i)`: its constants do not grow with `a`.

## 7. A universal rational tail budget

Put `x=1/3` and `P(x)=sum_(j>=0) p(j)x^j`. Consider only the finite,
rational scalar

\[
 R=\sum_{i=c+1}^{M}|u_i|x^{i-I},                         \tag{12}
\]

with an empty sum equal to zero. Summing the nonnegative envelopes (11)
beyond `c` yields

\[
 R\le \sum_{j\ge g}p(j)x^j+
 P(x)\left(x^g+x^{d-a}+
 \frac{x^{2c+2-I}+x^{2d+2-I}}{1-x^2}\right).             \tag{13}
\]

Because `g>=3`, `d>=c+1` and `a>=1`, this implies

\[
 R\le P(1/3)\left(1+3^{-3}+3^{-4}
             +\frac{3^{-8}+3^{-10}}{1-3^{-2}}\right)
       -\left(1+\frac13+\frac29\right).                 \tag{14}
\]

Euler's partition product has the elementary bound

\[
 P(1/3)=\prod_{j\ge1}(1-3^{-j})^{-1}
 \le \frac{54}{53}\prod_{j=1}^{3}(1-3^{-j})^{-1}
 =\frac{19683}{11024}<\frac{43}{24}.                    \tag{15}
\]

Indeed `sum_(j>=4)3^(-j)=1/54`, and finite induction gives
`prod(1-y_j)>=1-sum y_j` for nonnegative `y_j`. Taking the limit bounds
the product tail below by `53/54`. All series here have nonnegative
terms; (15) also justifies their convergence. Substituting in (14),

\[
 R < \frac{43}{24}\frac{27545}{26244}-\frac{14}{9}
   =\frac{204659}{629856}<\frac13.                      \tag{16}
\]

By (7), the polynomial tail in (2) is bounded below in Schur order by
`-(3/2)RG`. Combining with (8) and (16),

\[
 D\ge_S\left(\frac23-\frac32R\right)G\ge_S\frac16G.
                                                               \tag{17}
\]

Only finite polynomials and the finite rational scalar `R` enter this
Schur comparison; the convergent scalar series merely bounds `R`.
Thus the theorem holds whenever `c-a>=3`.

## 8. The six remaining identities

Put `x0=b-a` and `g=c-a`. Equal area implies

\[
 d=a+x_0+g+\frac{x_0g}{a},\qquad a\mid x_0g,
 \qquad1\le x_0\le g.                                 \tag{18}
\]

If `g<=2`, then `a<=x0*g<=4`. The complete list is

\[
 (a,b,c,d)=(1,2,2,4),(1,2,3,6),(1,3,3,9),
 (2,3,4,6),(2,4,4,8),(4,6,6,9).
\]

Here are the Schur coefficient vectors of **`6D-G`**, indexed by
`r=I,I+1,...,floor(N/2)`; all earlier coefficients are zero.
These are finite polynomial identities, not extrapolated data.

| `(a,b,c,d)` | Coefficient vector |
|---|---|
| `(1,2,2,4)` | `(5)` |
| `(1,2,3,6)` | `(5,10)` |
| `(1,3,3,9)` | `(5,34,56)` |
| `(2,3,4,6)` | `(5,50,150,110)` |
| `(2,4,4,8)` | `(5,84,546,1724,2658,1394)` |
| `(4,6,6,9)` | `(5,244,5474,74908,699624,4728402,23922080,92425594,275549984,635084746,1121660856,1475178840,1326804342,541149600)` |

Each identity can be checked by the defining recurrence and exact
multiplication/division, or by (1)--(2). The accompanying two algorithmically
independent implementations do both, entry-by-entry. The largest degree
is 36; all 47 coefficients, including the 17 initial zeros, are checked.
This completes (17) in every case.

## 9. Exact support and forced sign

Since `I<=b<=c`, the initial layer identities in (4) apply in every
case, including the six exceptions. In (2), all layers below `I` vanish;
the layer `I` has leading Schur coefficient one; higher layers are
divisible by `e2^(I+1)`. This proves the initial zeros and exact first
coefficient. Finally `G` contains `e2^I e1^(N-2I)` with coefficient one,
plus further Schur-positive terms. Repeated one-box Pieri gives a
positive coefficient at every two-row shape with second row at least
`I`. The bound `D>=_S G/6` proves the claimed strict support. It also
shows the global sign `(-1)^(a+1)` is forced for every nonzero comparison.

## 10. Attribution, status and verification boundary

The primary conjecture is François Bergeron, *A (q,t)-Overview of
q-Analogs*, arXiv:2608.30979v1, Section10.2, Conjecture10.1, printed
page30: [primary PDF](https://arxiv.org/pdf/2608.30979v1).
Its parameter scope and reported verification through `ad=bc<=36` were
checked directly in the PDF text on2026-09-22. The current arXiv record
still lists only v1. Lucas-binomial background is in Sagan--Savage,
[arXiv:0911.3159](https://arxiv.org/abs/0911.3159).
These references supply context, not an imported proof of this comparison.

The map in Section3 generalizes the earlier `a=2` stable-window argument
([source](../lucas_a2_stable_schur_window/THEOREM.md), Discovery Net
`bafkreiav4akizry7opmw73umskexdg3tnjw7cwzud5xnadi7ulwvgpb2xa`).
Prefix-to-tail domination was introduced for the complete `a=2` cone
([source](../lucas_a2_complete_schur/PROOF.md),
`bafkreif6p6felfg25vjnrw4xvxptjoxmjkl7ux7xdzetfwdeliiaymck3y`).
Both are rederived here. The new bridges are preservation of the
part-greater-than-`a` condition, threefold contraction with its endpoint
correction, and the shifted rectangle-boundary estimate. They close the
full parameter space at once. Earlier source is preserved unchanged.

The result is a complete written proof with six explicit finite identities.
Exact Python corroborates the identities and audits the structural lemmas;
finite experiments do not supply the universal quantifier. No floating
point, solver, CAS, random sample, external dataset or large certificate
is required. No independent peer review or proof-assistant formalization
is claimed. Bounded literature and graph searches found no previous full
proof; this is a search-relative novelty statement, not priority certification.
Elementary positivity, real-rootedness and optimality of `1/6` are not asserted.
