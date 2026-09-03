# The distance-refined two-fixed-point conjecture for `Av(123)`

Let

\[
f^{(2)}_{n,d}(123)
=\#\{\pi\in S_n:\pi\text{ avoids }123,
\operatorname{Fix}(\pi)=\{a,a+d\}\text{ for some }a\}.
\]

A 123-avoider has at most two fixed points, so the two displayed fixed
points are automatically the complete fixed-point set.

This note proves the distance-refined formula conjectured by Birmajer, Gil,
Tirrell, and Weiner in the appendix of
[*Pattern-avoiding stabilized-interval-free permutations*](https://arxiv.org/abs/2306.03155).
It also gives a shorter ballot-number formula for the same quantity.

## Main theorem

Write \(n=2m+r\), where \(r\in\{0,1\}\), and let \(1\le d\le m\). Then

\[
\boxed{
f_{n,d}^{(2)}(123)
=\frac{\binom{n-d}{m}^{2}}{(n-d)^2}
\left[
\frac{\binom{2d}{d}d^3(1-r)}{4d-2}
+2\sum_{i=1}^{\lfloor(m+1)/3\rfloor}
\frac{
\binom{m}{i-r}\binom{m-d+r}{i}
\binom{2d-2}{2i-1+d-r}
}{
\binom{m+i}{m}\binom{m-d+i}{m-d+r}
}
\bigl(d^2-(2i-r)^2\bigr)
\right].
}
\tag{1}
\]

Thus the Birmajer--Gil--Tirrell--Weiner conjecture holds for every admissible
size and distance.

There is also a compact symmetric version. Put \(L=n-d-1\) and define

\[
B_L(t)=
\begin{cases}
\displaystyle
\binom{L}{(L-t)/2}-\binom{L}{(L-t)/2-1},
&0\le t\le L,\quad t\equiv L\pmod2,\\[1ex]
0,&\text{otherwise}.
\end{cases}
\]

Then

\[
\boxed{
f_{n,d}^{(2)}(123)
=\sum_{s=0}^{2d-2}
\binom{2d-2}{s}B_L(s)B_L(2d-2-s).
}
\tag{2}
\]

Here \(B_L(t)\) is the classical ballot number for nonnegative paths of
length \(L\) ending at height \(t\).

## A general Catalan-hook formula

For nonnegative \(j,x,y\), let \(H_{j,x,y}\) count the permutations
\(\sigma\in\operatorname{Av}_{j+x+y}(123)\) satisfying both conditions:

1. the values \(1,\ldots,x\) occur decreasingly among the first \(j+x\)
   positions;
2. the last \(y\) entries are greater than \(x\) and decreasing.

The key result is

\[
\boxed{
H_{j,x,y}=[z^j]C(z)^{x+y+1}
=\frac{x+y+1}{j+x+y+1}\binom{2j+x+y}{j},
}
\tag{3}
\]

where \(C(z)=1+zC(z)^2\) is the Catalan generating function. In particular,
the answer depends on \(x,y\) only through \(x+y\).

### Dyck-path proof of (3)

We use Krattenthaler's right-to-left-maximum bijection between
\(\operatorname{Av}_N(123)\) and Dyck paths of semilength \(N\). If the
right-to-left maxima, read from right to left, are

\[
m_1<m_2<\cdots<m_t=N
\]

and

\[
\sigma=w_t m_t w_{t-1}m_{t-1}\cdots w_1m_1,
\]

the corresponding Dyck word is

\[
U^{m_1}D^{|w_1|+1}
U^{m_2-m_1}D^{|w_2|+1}\cdots
U^{m_t-m_{t-1}}D^{|w_t|+1}.
\tag{4}
\]

Assume first that \(y\ge1\). The last \(y\) entries of \(\sigma\) are
decreasing exactly when they are all right-to-left maxima, which is equivalent
to \(w_1=\cdots=w_{y-1}=\varnothing\). They are all greater than \(x\)
exactly when \(m_1>x\). Once \(m_1>x\), every value in \([x]\) is a
non-right-to-left maximum. The non-right-to-left maxima of a 123-avoider occur
globally in decreasing order: two such entries \(u<v\) from left to right,
together with a later entry larger than \(v\), would form a 123. Consequently,
the hook conditions translate exactly into

- an initial ascent of length at least \(a=x+1\), and
- the first \(b=y-1\) descent runs having length one and each being followed
  by another ascent.

Let \(F_{a,b}(z)\) enumerate such Dyck paths by semilength. Write the first
\(b+1\) ascent-run lengths as

\[
a_1\ge a,\qquad a_2,\ldots,a_{b+1}\ge1,
\]

and put \(A=a_1+\cdots+a_{b+1}\). Immediately after these runs and the
intervening \(b\) singleton descents, the path is at height \(h=A-b\), and
the remaining suffix begins with a down-step. Its unique decomposition at the
successive first crossings of levels \(h-1,h-2,\ldots,0\) contains \(h\)
arbitrary Dyck excursions. It therefore contributes \(C(z)^h\). Hence

\[
\begin{aligned}
F_{a,b}(z)
&=\sum_{a_1\ge a\atop a_2,\ldots,a_{b+1}\ge1}
z^A C(z)^{A-b}\\
&=C(z)^{-b}
\frac{(zC(z))^a}{1-zC(z)}
\left(\frac{zC(z)}{1-zC(z)}\right)^b\\
&=z^{a+b}C(z)^{a+b+1},
\end{aligned}
\tag{5}
\]

using \((1-zC(z))^{-1}=C(z)\). Since \(a+b=x+y\), taking the coefficient
of \(z^{j+x+y}\) gives \([z^j]C(z)^{x+y+1}\).

If \(y=0<x\), reflect the permutation plot in the anti-diagonal:

\[
\tau_i=N+1-\sigma^{-1}(N+1-i).
\]

This preserves 123-avoidance and bijects the \((x,0)\) hook condition with
the \((0,x)\) condition, which was just counted. For \(x=y=0\), the answer
is simply \(C_j\). Finally, the standard Lagrange-inversion coefficient

\[
[z^j]C(z)^{q}
=\frac{q}{2j+q}\binom{2j+q}{j}
\]

with \(q=x+y+1\) yields the closed form in (3).

## Two-fixed-point grid decomposition

Fix the two points \(a<b=a+d\) and split positions and values before,
strictly between, and after them. The lower-left, central, and upper-right
cells of this \(3\times3\) grid are empty, and each of the four off-diagonal
middle strips is decreasing; otherwise one of the two fixed points completes
a 123 pattern.

Let \(x\) be the number of middle values before \(a\), let \(y\) be the
number of middle positions carrying values above \(b\), and let \(j,k\) be
the upper-left and lower-right corner sizes. Row and column counts give

\[
j=\frac{n-d-1-x-y}{2},\qquad k=n-2d-j.
\tag{6}
\]

There are \(\binom{d-1}{x}\) choices for the middle values in the left
strip and \(\binom{d-1}{y}\) choices for the middle positions in the upper
strip. Standardizing the northwest hook gives an
\(H_{j,x,y}\) object. Reverse-complementing and standardizing the southeast
hook gives an \(H_{k,d-1-x,d-1-y}\) object.

Conversely, these choices and two hook objects inflate uniquely. A 123 inside
one hook is excluded by definition. Across hooks the corner value bands are
oppositely ordered; each middle strip is decreasing; and the only potentially
increasing cross-strip pairs have neither a smaller predecessor nor a larger
successor in the required cell. Thus no cross-hook 123 is introduced. We have
the exact identity

\[
f^{(2)}_{n,d}(123)=
\sum_{\substack{0\le x,y<d\\j,k\in\mathbb Z_{\ge0}}}
\binom{d-1}{x}\binom{d-1}{y}
H_{j,x,y}H_{k,d-1-x,d-1-y},
\tag{7}
\]

with \(j,k\) as in (6).

Put \(s=x+y\), \(s'=2d-2-s\), and \(L=n-d-1\). Then

\[
2j+s=2k+s'=L,
\]

so (3) gives \(H_{j,x,y}=B_L(s)\) and
\(H_{k,d-1-x,d-1-y}=B_L(s')\). Vandermonde's identity

\[
\sum_{x+y=s}\binom{d-1}{x}\binom{d-1}{y}
=\binom{2d-2}{s}
\]

now turns (7) into the ballot sum (2).

## Identification with the conjectured expression

It remains to show that (2) is exactly (1), rather than merely another
enumeration. Set

\[
A=\frac{\binom{n-d}{m}}{n-d}.
\]

### Even size

For \(r=0\), pair the terms of (2) at

\[
s=d-1+2i,\qquad s'=d-1-2i.
\]

The central term \(s=s'=d-1\) satisfies \(B_L(d-1)=dA\), and therefore
equals

\[
A^2\frac{\binom{2d}{d}d^3}{4d-2}.
\]

For \(i\ge1\),

\[
B_L(d-1+2i)
=\frac{d+2i}{m+i}\binom{L}{m-d-i},
\]

\[
B_L(d-1-2i)
=\frac{d-2i}{m-i}\binom{L}{m-d+i}.
\]

Direct cancellation of factorials gives

\[
A^2
\frac{\binom mi\binom{m-d}i}
{\binom{m+i}m\binom{m-d+i}{m-d}}
=
\frac{\binom L{m-d-i}\binom L{m-d+i}}
{(m+i)(m-i)}.
\tag{8}
\]

Multiplying (8) by
\(2\binom{2d-2}{d-1+2i}(d^2-4i^2)\) yields exactly the paired
terms of (2). A nonzero pair requires
\(i\le m-d\) and \(2i\le d-1\), hence \(3i\le m-1\); the published upper
limit \(\lfloor(m+1)/3\rfloor\) includes every nonzero term, with any extras
killed by a binomial coefficient.

### Odd size

For \(r=1\), there is no central term. Pair

\[
s=d-2+2i,\qquad s'=d-2i,
\]

where \(i\ge1\). Now

\[
B_L(d-2+2i)
=\frac{d+2i-1}{m+i}\binom L{m-d+1-i},
\]

\[
B_L(d-2i)
=\frac{d-2i+1}{m-i+1}\binom L{m-d+i},
\]

and factorial cancellation gives

\[
A^2
\frac{\binom m{i-1}\binom{m-d+1}i}
{\binom{m+i}m\binom{m-d+i}{m-d+1}}
=
\frac{\binom L{m-d+1-i}\binom L{m-d+i}}
{(m+i)(m-i+1)}.
\tag{9}
\]

After multiplying (9) by
\(2\binom{2d-2}{d-2+2i}(d^2-(2i-1)^2)\), this is precisely the odd
summand in (1). A nonzero pair requires \(i\le m-d+1\) and \(2i\le d\),
so \(3i\le m+1\), giving exactly the stated upper limit. This completes the
proof of (1).

## Reproduction

The checker needs CPython 3.11 or later and only the standard library:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 verify.py
```

It performs the following exact checks:

1. It compares a recursive Catalan generator with literal permutation
   filtering and a literal three-index 123 test through size 8.
2. It enumerates every hook set through size 8, checks (3), checks the
   anti-diagonal bijection entry by entry, and checks the Dyck-path condition.
3. It compares (7), (2), and the literal source formula for every admissible
   \((n,d)\) through \(m=30\), then compares (2) with the source formula
   through \(m=200\).
4. It constructs all permutations from the two-hook grid and compares the
   complete sets with direct enumeration for every admissible \((n,d)\) and
   \(2\le n\le10\).

The last line is

```text
general_formula_check=PASS
```

The complete-set counts at distance four are \(20,90,380\) for
\(n=8,9,10\). The \((n,d)=(10,4)\) set digest is
`7080bb34fdf100be575a926af284f32b71e7c59e1967da6e05d35dad3c1bf4bd`.

All computations use exact Python integers, tuples, sets, and rational
numbers. There is no randomness, floating point, external data, solver, CAS,
or omitted certificate. The universal theorem rests on the written Dyck-path
and grid bijections and the displayed factorial identities; the finite
computation is corroborative.

## Sources and novelty scope

- D. Birmajer, J. B. Gil, J. O. Tirrell, and M. D. Weiner,
  *Pattern-avoiding stabilized-interval-free permutations*, Discrete
  Mathematics 348 (2025), 114329,
  [arXiv:2306.03155](https://arxiv.org/abs/2306.03155).
- C. Krattenthaler, *Permutations with restricted patterns and Dyck paths*,
  Advances in Applied Mathematics 27 (2001), 510--530,
  [arXiv:math/0002200](https://arxiv.org/abs/math/0002200).
- S. Elizalde, *Multiple pattern avoidance with respect to fixed points and
  excedances*, Electronic Journal of Combinatorics 11 (2004), R51,
  [arXiv:math/0311211](https://arxiv.org/abs/math/0311211).

Targeted searches found the source conjecture, Elizalde's earlier aggregate
two-fixed-point formula, and the already published graph-level proofs of the
fixed \(d=2\) and \(d=3\) slices, but no prior proof of the general
distance-refined formula or of (3). The novelty statement is therefore
search-relative, not a historical priority claim.
