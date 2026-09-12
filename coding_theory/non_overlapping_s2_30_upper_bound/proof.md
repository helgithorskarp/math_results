# A quadratic-box certificate for `S(2,30) <= 8,794,991`

## Result

Let `S(q,n)` be the maximum cardinality of a `q`-ary length-`n`
non-overlapping code.  Then

\[
                         S(2,30)\le 8,794,991.
\]

Together with the construction of size 7,555,935 reported by Stanovnik,
Moškon, and Mraz, this narrows the exact frontier to

\[
             7,555,935\le S(2,30)\le 8,794,991.
\]

The previous primary-source upper endpoint was the Levenshtein bound
13,390,727.  The new certificate lowers it by 4,595,736.

## Exact recurrence and upper-half reduction

The source converts the maximum problem to the integer recurrence

\[
 x_1+y_1=q,\qquad
 x_i+y_i=s_i:=\sum_{j=1}^{i-1}x_jy_{i-j}\quad(2\le i<n),
\]

with objective `s_n`.  Its Theorem 15 proves that some optimum is pure in the
upper half: `x_i y_i=0` for every `i>n/2`.  Definition 14 supplies backwards
conditions selecting the pure side once the lower half is fixed.

## General quadratic-box lemma

Let `n=2m`, choose a level `h<=m` satisfying

\[
                              3h>2m,
\]

and fix a feasible recurrence prefix through level `h-1`.  Leave the lower
levels `h,h+1,...,m` free, writing their left sizes as
`z_1,...,z_r`, where `r=m-h+1`.

For each free level, its total `s_i` is affine in the preceding free
variables.  Indeed, two variable-dependent factors have indices at least `h`
and hence cannot occur in a convolution whose target index is at most
`m<2h`.

At every later level, every coordinate and the final objective is a polynomial
of total degree at most two in `z_1,...,z_r`.  More generally, a degree-`d`
monomial can first occur only at a level at least `dh`: multiplication in a
convolution adds both polynomial degrees and word-length indices.  The
assumption `3h>2m=n` therefore excludes degree three through the objective.

The fixed prefix determines all upper orientations above level `2m-h`.
Orientations at levels `m+1,...,2m-h` correspond to the `r-1` non-middle free
lower levels and are not yet known.  Enumerating their `2^(r-1)` pure patterns
covers the pattern of the upper-half optimum guaranteed by the source.  For a
fixed pattern the objective has the exact form

\[
 Q(z)=C+\sum_i \ell_i z_i+\sum_i a_{ii}z_i^2
          +\sum_{i<j}a_{ij}z_i z_j.                         \tag{1}
\]

## Recursive box

Suppose the affine total at free level `i` is

\[
 s_i(z_1,\ldots,z_{i-1})=c_i+\sum_{j<i}b_{ij}z_j.
\]

Starting with no free variables, define recursively

\[
 H_i=c_i+\sum_{j<i}\max(0,b_{ij}H_j).                       \tag{2}
\]

If all earlier feasible variables satisfy `0<=z_j<=H_j`, then (2) is the
maximum of this affine expression over the enlarged box.  Since a feasible
split satisfies `0<=z_i<=s_i`, induction gives

\[
                    0\le z_i\le H_i
\]

for every true recurrence completion.  The nested feasible region is thus
contained in the independent integer box `prod_i [0,H_i]`.

## Exact quadratic box bound

For integers `a,l,H` with `H>=0`, let

\[
 M(a,l,H)=\max_{0\le z\le H,\ z\in\mathbb Z}(az^2+lz).
\]

This is computed exactly from the two endpoints when `a>=0`, and from the at
most two clipped integers adjacent to `-l/(2a)` when `a<0`.

For every integer point of the box, (1) satisfies

\[
 Q(z)\le C+\sum_i M(a_{ii},\ell_i,H_i)
       +\sum_{i<j}\max(0,a_{ij}H_iH_j).                    \tag{3}
\]

The diagonal-plus-linear term for each coordinate is bounded by its own exact
integer maximum.  Because all variables are nonnegative, a cross term is at
most `a_ij H_i H_j` when its coefficient is positive and at most zero when
its coefficient is nonpositive.  Summing these termwise inequalities proves
(3).  No concavity assumption is made.

Equations (2) and (3), maximized over every fixed prefix and unresolved pure
orientation pattern, give a rigorous unrestricted upper bound for the exact
recurrence.

## Complete length-30 certificate

For `n=30`, take `m=15`, `h=12`, and four free levels 12--15.  The degree
condition is `3h=36>30`.  The exact exhaustive subdivision is

```
canonical prefixes through level 11       6,001,931
unresolved pure orientation patterns              8
quadratic orientation branches            48,015,448
maximum bound from (3)                      8,794,991
positive cross coefficients encountered            0
```

The computation is partitioned by the canonical prefix ordinal modulo 12.
Eleven shards contain 500,161 prefixes and the last contains 500,160; their
sum is 6,001,931.  Every shard independently traverses the same canonical
prefix order and evaluates only its residue class.  The eight orientation
patterns on every evaluated prefix account for all 48,015,448 polynomial
branches.  `expected_n30.json` records all twelve local maxima and the unique
maximizing record.

The global maximum occurs in shard 2, at the prefix

```
L: 1 0 0 0 1 1 2 4 8 15 29
R: 1 1 1 1 0 0 0 0 0  0  0
```

with all three unresolved upper orientations assigned left, recursive box
highs `(56,108,208,401)`, and relaxed quadratic

\[
\begin{aligned}
3,354,322
&+16,856z_1+12,956z_2+8,666z_3+4,446z_4\\
&-22z_1^2-11z_2^2-3z_3^2-z_4^2\\
&-32z_1z_2-22z_1z_3-8z_1z_4\\
&-12z_2z_3-4z_2z_4-2z_3z_4.
\end{aligned}
\]

Applying (3) to this record gives 8,794,991.  Every other shard maximum is
smaller.  The absence of positive cross terms is reported evidence, not an
assumption of the algorithm; positive terms are handled by the last sum in
(3).

## Verification and scope

The optimized C++ enumerator uses exact signed and unsigned 128-bit integers,
asserts the affine and quadratic degree conditions, and fails visibly on an
invalid parameter, shard, bound, or degree.  The independent Python checker
reconstructs recurrence polynomials by interpolation rather than symbolic
propagation, exhausts complete smaller feasible trees, and checks the generic
box inequality directly.  The shard merger verifies disjoint coverage and all
compact expected fields.

This result is an upper bound, not an exact determination of `S(2,30)`.  It
does not assert that the relaxed maximizing box point is feasible, and it does
not prove the source's broader conjecture.  The remaining gap is 1,239,056.

## Primary source

Lidija Stanovnik, Miha Moškon, and Miha Mraz, *In search of maximum
non-overlapping codes*, Designs, Codes and Cryptography 92 (2024), 1299--1326,
[doi:10.1007/s10623-023-01344-z](https://doi.org/10.1007/s10623-023-01344-z),
[arXiv:2307.12593v2](https://arxiv.org/abs/2307.12593).
