# Middle-layer quadratic compression for even-length non-overlapping codes

## Setting

For integers `q >= 2` and `n >= 2`, the integer formulation `SQN(q,n)` of
Stanovnik, Moškon, and Mraz is

\[
 S(q,n)=\max \sum_{i=1}^{n-1}x_i y_{n-i},
\]

where

\[
 x_1+y_1=q,\qquad
 x_i+y_i=s_i:=\sum_{j=1}^{i-1}x_jy_{i-j}\quad(2\le i<n),
\]

`x_1,y_1` are positive integers, and all other variables are nonnegative
integers.  The source's Theorem 15 proves that some optimum has
`x_i y_i=0` whenever `i>n/2`, and gives backwards sign conditions that select
the nonzero side at those upper levels.

## Theorem

Let `n=2m` be even.  Fix any feasible lower prefix

\[
 (x_i,y_i)_{1\le i<m}
\]

and fix any orientation at each upper level `m<i<2m`: at level `i`, either
`x_i=s_i,y_i=0` or `x_i=0,y_i=s_i` will be used.  Put

\[
 s_m=\sum_{j=1}^{m-1}x_jy_{m-j},\qquad
 x_m=t,\quad y_m=s_m-t,quad 0\le t\le s_m.
\]

Complete the upper levels recursively with the fixed orientations.  Then the
resulting objective is

\[
 Q(t)=-t^2+Bt+C
\]

for integers `B,C` depending on the fixed prefix and orientations, but not on
`t`.

Consequently the maximum over integer `0<=t<=s_m` occurs at at most two
values: the integers nearest `B/2`, clipped to the interval.  Explicitly, it
is enough to test

\[
 T(B,s_m)=
 \begin{cases}
 \{0\},&B\le0,\\
 \{s_m\},&B\ge2s_m,\\
 \{\lfloor B/2\rfloor,\lceil B/2\rceil\},&0<B<2s_m,
 \end{cases}
\]

after removing a duplicate when `B` is even.

Combining this with the upper-half reduction of Stanovnik, Moškon, and Mraz,
the middle loop in their complete even-length `SQN` algorithm may be replaced
globally by one exact quadratic and at most two vertex candidates for every
lower prefix.  No possible optimum is lost.

## Proof

Represent each quantity depending on `t` as a polynomial.  All layers below
`m` are constant, while

\[
 x_m=t,\qquad y_m=s_m-t
\]

are affine.

We first prove inductively that `s_i`, `x_i`, and `y_i` are affine in `t` for
every `m<i<2m`.  Suppose this is known below level `i`.  In

\[
 s_i=\sum_{j=1}^{i-1}x_jy_{i-j},
\]

the two positive indices in a summand add to `i<2m`.  They therefore cannot
both be at least `m`.  At most one factor in every product depends on `t`, and
that factor is affine by the induction hypothesis.  Hence `s_i` is affine.
The fixed orientation assigns this affine expression to one of `x_i,y_i` and
zero to the other, preserving the claim.

Now consider the objective at level `2m`:

\[
 Q(t)=\sum_{j=1}^{2m-1}x_jy_{2m-j}.
\]

The central summand is

\[
 x_my_m=t(s_m-t)=-t^2+s_mt.
\]

Every other summand has one index below `m` and one above `m`, so it is a
constant times an affine polynomial.  Thus no other quadratic term occurs,
and `Q(t)=-t^2+Bt+C` with integer coefficients.

Finally,

\[
 Q(t+1)-Q(t)=B-2t-1.

The difference strictly decreases with `t`, so the integer maximum is attained
at the one or two integers nearest the real vertex `B/2`, unless the vertex is
outside `[0,s_m]`, in which case the nearest endpoint is optimal.  This gives
the displayed candidate set.

It remains to connect the fixed-orientation statement to unrestricted `SQN`.
Theorem 15 of the source ensures that some unrestricted optimum has pure upper
levels.  Its backwards condition for an upper index `i>m` uses only lower
sizes with indices at most `2m-i<m` and already selected orientations at larger
upper indices.  Descending induction therefore shows that the selected upper
orientation pattern is independent of the middle split `t`; a zero condition
may be resolved by either fixed convention without changing the objective.
Apply the quadratic result to that pattern and the lower prefix of an optimum.
Replacing its middle value by a member of `T(B,s_m)` cannot decrease its score,
so at least one unrestricted optimum survives the compression.  This proves
completeness.

## Auditable finite reduction

The published branch procedure explicitly loops over all `s_m+1` feasible
middle values after fixing a prefix through level `m-1`.  The theorem replaces
that interval by one symbolically propagated quadratic and at most two integer
vertex candidates.  This applies to every lower prefix, including asymmetric
ones and prefixes that do not lead to an optimum.

The supplied C++ enumerator implements the symbolic propagation.  For each
upper convolution it also asserts that the quadratic coefficient vanishes,
and at the objective it asserts that the coefficient is exactly `-1`.  It
reports both the number of leaves in the original middle loop and the number
of retained vertex candidates.

The complete binary length-24 tree gives

```
lower prefixes                 6,001,931
original middle-loop leaves  321,286,030
retained vertex candidates     6,706,281
reduction factor             47.9082266
recovered optimum               147,312
```

Thus this is a global exhaustive reduction, not a sample or a local branch
census.  The length-24 optimum agrees with the independently published exact
table.  The Python checker separately enumerates every middle value on every
binary prefix through length 20, checks every second difference is `-2`, and
confirms that the retained vertex values give the same optimum.

The optional complete binary length-26 run gives an adjacent scaling check:

```
lower prefixes                   321,286,030
original middle-loop leaves   30,699,841,782
retained vertex candidates       321,286,030
reduction factor                95.5529930
recovered optimum                   547,337
elapsed seconds                     893.775
```

The length-26 optimum again agrees with the published exact table.  This
larger run is not required by the default verification suite or by the proof.

## Scope

The theorem does not determine `S(2,30)` and does not prove the source's
Conjecture 1.  It removes exactly the middle-layer interval from every
even-length branch.  Further reductions of one or more earlier lower layers
are still needed to make complete length-30 enumeration near-term.

## Source dependency

The `SQN` formulation and upper-half reduction are from:

Lidija Stanovnik, Miha Moškon, and Miha Mraz, *In search of maximum
non-overlapping codes*, Designs, Codes and Cryptography 92 (2024), 1299--1326,
[doi:10.1007/s10623-023-01344-z](https://doi.org/10.1007/s10623-023-01344-z),
[arXiv:2307.12593v2](https://arxiv.org/abs/2307.12593).
