# The complete ordinary gamma-sign classification for odd cycles

All polynomials are over the rationals unless integrality is stated. A
gamma expansion of a palindromic polynomial of degree `d` means the basis
`t^j (1+t)^(d-2j)`, without a change of degree or basis.

## 1. Statement and notation

For `m = 2q+1 >= 3`, let

\[
 Q_m=\{x\in\mathbb R_{\ge0}^m:x_i+x_{i+1}\le1\quad(i\bmod m)\},\qquad
 F_m(t)=\sum_{n\ge0}|nQ_m\cap\mathbb Z^m|t^n.
\]

Put

\[
 H_m(t)=(1-t^2)^{m+1}F_m(t),\qquad
 R_m(t)=(1-t)^{m+1}(1+t)F_m(t).
\]

The known cancellation `H_m=(1+t)^m R_m` leaves a palindromic polynomial
`R_m` of degree `m-1`. We also recover this fact below. Define

\[
 R_{2q+1}(t)=(1+t)^{2q}G_q\!\left(\frac{t}{(1+t)^2}\right),\qquad
 G_q(x)=\sum_{j=0}^q g_{q,j}x^j.
\]

**Theorem.** For every `q >= 1`,

\[
 g_{q,j}>0\quad(0\le j<q),\qquad g_{q,q}=(-1)^q.       \tag{1}
\]

Consequently `H_m` is ordinary gamma-nonnegative if and only if
`m = 1 (mod 4)`. In its degree-`2m-1` gamma expansion, the coefficients
through `q` are those of `G_q`, and every coefficient above `q` is zero.
This theorem makes no assertion about real-rootedness.

For the proof, let `P_v` be the path polytope on `v >= 2` coordinates,
defined by nonnegativity and `x_i+x_(i+1) <= 1`. Write

\[
 E_v(t)=\sum_{n\ge0}|nP_v\cap\mathbb Z^v|t^n
       =\frac{W_v(t)}{(1-t)^{v+1}}.
\]

It is the chain polytope of the rank-one fence poset. Its numerator is
the descent polynomial of any natural labeling of that poset. For even
`v = 2q`, use the notation

\[
 W_{2q}(t)=(1+t)^{2q-2}A_q\!\left(\frac{t}{(1+t)^2}\right),\qquad
 A_q(x)=\sum_{j=0}^{q-1}a_{q,j}x^j.                     \tag{2}
\]

These identifications and the gamma-nonnegativity of `A_q` are prior
results: see Petersen--Zhuang, Theorem 2.5, with their normalization
`W_v=Z_v/t`. The specific combinatorial interpretation used next is
Brändén's Theorem 6.3. All coefficients with an index outside the stated
range are henceforth zero.

## 2. A growth injection for fence gamma coefficients

Label the minimal elements of the fence by distinct negative integers
and the maximal elements by distinct positive integers. This is a
canonical, natural labeling of a rank-one poset. Brändén's orbit theorem
says that `a_(q,j)` counts its linear extensions
`pi = pi_1 ... pi_(2q)` having `j` ordinary descents and **no double
descent in `0 pi 0`**. Here a double descent means three consecutive
letters `u > v > w`, including either boundary zero. The boundary
condition is essential.

The following inequality is the needed strengthening of mere
gamma-nonnegativity:

\[
 a_{q+1,j}\ \ge\ (j+1)a_{q,j}+(2q-2j+1)a_{q,j-1}
 \qquad(0\le j\le q).                                 \tag{3}
\]

To prove it, take the even fence with its right endpoint a maximal
element `v`. Extend the fence by a new minimal element `u` and a new
maximal element `w`, adding the relations `u < v` and `u < w`.
Choose the label of `u` smaller than every old label and the label of
`w` larger than every old label.

Given a canonical extension `pi` counted by `a_(q,k)`, first prepend
`u`. The resulting word is still free of double descents between its
boundary zeros: the old first letter is negative and is followed by a
larger letter, so replacing its left boundary zero by the smaller `u`
creates no double descent. The number of ordinary descents remains `k`.

Now insert `w` either:

* immediately before an old letter `pi_i` with `pi_i < pi_(i+1)`;
* or at the very end.

There are `2q-1-k` positions of the first kind and one of the second.
Each insertion is a linear extension of the extended fence, since `u`
is first and precedes both `v` and `w`. It has no double descent: `w`
is a peak, and the following old letter, if present, is followed by an
ascent. All other old comparisons remain harmless.

Of these positions, exactly `k+1` preserve the number of descents.
There is one just after each of the `k` old descents, and the final
position is the additional one. Every old descent is followed by an
ascent because `0 pi 0` has no double descent; in particular the last
old letter cannot be the lower letter of an old descent. The other
`2q-2k-1` insertions increase the descent number by one.

Deleting the two named new letters recovers `pi` and the insertion
position, so all images are distinct, including images arising from
different values of `k`. Counting images with `j` descents proves (3).
The same injection works for any rank-one poset when a new minimal
element is attached below a chosen old maximal element and a new
maximal element is attached above the new minimal element.

Since `A_1=1`, (3) proves

\[
 a_{q,j}\ge1\quad(0\le j\le q-1),\qquad a_{q,0}=1.     \tag{4}
\]

For strict positivity at the new top index, the coefficient of
`a_(q,q-1)` in (3) with `j=q` is one. The equality at index zero also
follows from the constant term of an Ehrhart numerator.

## 3. An exact cycle--path identity

For `N >= 1`, let `M_N` be the symmetric matrix indexed by
`0,...,N-1` with entries `1_(r+s <= N-1)`, and set
`p_l(N)=tr(M_N^l)`. Closed-word counting gives

\[
 |nQ_m\cap\mathbb Z^m|=p_m(n+1).
\]

For `k=1,...,N`, put

\[
 \theta_k=\frac{(2k-1)\pi}{4N+2},\qquad
 \lambda_k=\frac{(-1)^{k-1}}{2\sin\theta_k},\qquad
 v^{(k)}_r=\cos((2r+1)\theta_k).
\]

Summing a cosine progression proves `M_N v^(k)=lambda_k v^(k)`.
The eigenvalues are distinct, and

\[
 \sum_{r=0}^{N-1}\cos^2((2r+1)\theta_k)=\frac{2N+1}{4}.
\]

Thus the squared first coordinate of the normalized eigenvector is

\[
 \frac{4\cos^2\theta_k}{2N+1}
   =\frac{4-\lambda_k^{-2}}{2N+1}.
\]

If `e_0` is the first coordinate vector and `1` is the all-ones vector,
then `M_N e_0=1`. A path with `m-1` coordinates therefore has count

\[
 |nP_{m-1}\cap\mathbb Z^{m-1}|
  =1^T M_{n+1}^{m-2}1
  =e_0^T M_{n+1}^{m}e_0
  =\frac{4p_m(n+1)-p_{m-2}(n+1)}{2n+3}.                \tag{5}
\]

This is an exact identity of integers, derived without an asymptotic
estimate. The only auxiliary case needed is `m-2=1`: define `Q_1` by
the loop inequality `2x <= 1`, so

\[
 F_1(t)=\frac1{(1-t)(1-t^2)},\qquad R_1(t)=1,
 \qquad G_0(x)=1.                                     \tag{6}
\]

The loop is used only as a recurrence initial condition, not as a
simple graph in the theorem.

Summing (5) over dilations gives

\[
 4F_m(t)=(2t\partial_t+3)E_{m-1}(t)+F_{m-2}(t).
\]

Substitute the denominator of `E_(m-1)` and multiply by
`(1-t)^(m+1)(1+t)`:

\[
 4R_m=(1+t)\{2t(1-t)W'_{m-1}+[3+(2m-3)t]W_{m-1}\}
          +(1-t)^2R_{m-2}.                            \tag{7}
\]

Equation (7), starting at (6), also proves the polynomial cancellation
and palindromicity used in Section 1. Indeed substituting (2), and
`x=t/(1+t)^2`, gives

\[
 4G_q(x)=[3+8(q-1)x]A_q(x)
          +2x(1-4x)A'_q(x)+(1-4x)G_{q-1}(x).          \tag{8}
\]

The apparent degree-`q` terms involving `A_q` cancel, so the right side
has degree at most `q`. Equation (7) then constructs a palindromic
polynomial of degree `2q` with constant term one. Its coefficients are
integers by its definition from lattice counts, hence its gamma
coefficients are integers as well. In coefficient form, (8) reads

\[
 4g_{q,j}=(2j+3)a_{q,j}+8(q-j)a_{q,j-1}
                     +g_{q-1,j}-4g_{q-1,j-1}.        \tag{9}
\]

## 4. A simultaneous induction

We prove (1) together with the auxiliary bound

\[
 g_{q,j}\le a_{q+1,j}\quad(0\le j\le q).              \tag{10}
\]

The base is `G_1=1-x`, `A_1=1`, and `A_2=1+x`; it follows from
(8), or directly from the triangle and the four-vertex path. All base
claims hold. For every `q`, the constant term of (9) gives `g_(q,0)=1`.
The coefficient with `j=q` in (9) gives

\[
 g_{q,q}=-g_{q-1,q-1}=(-1)^q.                          \tag{11}
\]

For `1 <= j <= q-1`, assume the induction claims for `q-1`. The negative
term in (9) is bounded below using (10), giving

\[
 4g_{q,j}\ge(2j+3)a_{q,j}+[8(q-j)-4]a_{q,j-1}
                  +g_{q-1,j}.                        \tag{12}
\]

If `j <= q-2`, every term on the right is nonnegative and the first is
positive by (4). If `j=q-1`, its last term is at least `-1`, while the
first two terms are at least `2q+1` and `4`. Thus it is again positive.
This proves every required nonterminal sign.

To retain the upper bound, `g_(q-1,j-1)` is positive for
`1 <= j <= q-1`. Discard its negative multiple in (9), and apply (10)
to the other preceding-cycle coefficient:

\[
 g_{q,j}\le\frac{j+2}{2}a_{q,j}+2(q-j)a_{q,j-1}
        \le(j+1)a_{q,j}+(2q-2j+1)a_{q,j-1}
        \le a_{q+1,j}.                               \tag{13}
\]

The middle inequality uses nonnegativity, and the last is exactly (3).
At `j=0` the bound is equality. At `j=q`, (11) and (4) give
`g_(q,q) <= 1 <= a_(q+1,q)`. This completes the simultaneous induction.

## 5. Scope of the conclusion

The full width-one ordinary gamma-sign question is settled by (1).
Combining it with the previously published terminal-pair obstruction
for uniform block width `a >= 2` gives the following classification:

> For odd `m >= 3` and equal positive integer block width `a`, the fixed
> rational numerator `(1-t^2)^(am+1) F_(m,a)(t)` is ordinary
> gamma-nonnegative, in its palindromic degree `2a(m-1)+1`, exactly when
> `a=1` and `m=1 (mod 4)`.

The `a >= 2` exclusion is imported from the earlier parity package,
not proved anew here. No assertion is made about unequal widths,
alternative gamma-type bases, or the real-rootedness conjecture for
`G_q`. Unimodality of the width-one rational numerator was already
known. The argument is an unformalized proof using the cited
combinatorial orbit theorem; finite checks corroborate it but do not
prove its universal quantifiers or supply independent peer review.

## References

1. P. Brändén, *Actions on permutations and unimodality of descent
   polynomials*, Theorem 6.3 (canonical labels, boundary zeros, and
   gamma orbit representatives), [arXiv:math/0610185v4](https://arxiv.org/pdf/math/0610185).
2. T. K. Petersen and Y. Zhuang, *Zig-zag Eulerian polynomials*,
   Theorem 2.5 and Sections 5--6; their `Z_n/t` is our `W_n`,
   [arXiv:2403.07181v4](https://arxiv.org/html/2403.07181v4).
3. G. Hamano, T. Hibi and H. Ohsugi, *Ehrhart series of fractional
   stable set polytopes of finite graphs*, Theorem 3.1 and Example 3.3,
   [arXiv:1603.09613v2](https://arxiv.org/abs/1603.09613).
4. R. Ehrenborg, *The Ehrhart and face polynomials of the graph
   polytope of a cycle*, European Journal of Combinatorics 118 (2024),
   103906, [DOI](https://doi.org/10.1016/j.ejc.2023.103906).
   Cycle transfer and spectral enumeration are prior machinery; the
   elementary eigenvector calculation needed here is supplied above.
5. Jiang--Yang--Zhong, *Transfer Matrices and Ehrhart Theory for Path
   and Cyclic Block Polytopes*, Problem 4,
   [arXiv:2607.22008](https://arxiv.org/html/2607.22008).
   Its broader gamma-type wording should not be confused with the
   specific ordinary basis classified here.
6. Earlier campaign sources: [exact parity and uniform-width
   obstruction](../odd_cycle_block_parity/README.md),
   [spectral-to-gamma recurrence and conjecture](../odd_cycle_width_one_gamma/README.md),
   and [fixed-column asymptotics](../odd_cycle_gamma_fixed_columns/README.md).
   Their terminal sign, finite evidence, and fixed-column conclusions
   are prior results, not new claims of this package.
