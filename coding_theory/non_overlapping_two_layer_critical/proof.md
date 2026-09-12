# A constant critical set for the last two free `SQN` layers

## Setting

In the exact integer formulation of Stanovnik, Moškon, and Mraz, put

\[
 x_1+y_1=q,\qquad
 x_i+y_i=s_i:=\sum_{j=1}^{i-1}x_jy_{i-j}\quad(2\le i<n),
\]

and maximize `s_n`.  Their Theorem 15 proves that some optimum has a pure
upper half: `x_i y_i=0` for every `i>n/2`.  The backwards conditions in their
Definition 14 choose the nonzero side at those levels.

## Theorem

Let `n=2m` with `m>=4`.  Fix any feasible prefix through level `m-2`.
Write

\[
 A=s_{m-1},\qquad x_{m-1}=u,\quad y_{m-1}=A-u,
 \qquad 0\le u\le A.
\]

Then:

1. `s_m(u)=p u+r` is affine.
2. Every upper orientation above level `m+1` is independent of `u` and of the
   middle split.  The backwards condition selecting the orientation at level
   `m+1` is exactly `D(u)=d-2u`; hence `[0,A]` is divided into at most two
   integer orientation intervals.
3. On either orientation interval, after writing

   \[
   x_m=t,\qquad y_m=s_m(u)-t,
   \]

   the recursively completed objective is

   \[
   Q(u,t)=-t^2+(a u+b)t+c u^2+e u+f                 \tag{1}
   \]

   for integers `a,b,c,e,f` depending on the prefix and the orientation.
4. The exact maximum of (1) over the integer trapezoid

   \[
   0\le u\le A,\qquad 0\le t\le p u+r
   \]

   is attained in an explicitly computable critical set of at most eight
   pairs on each orientation interval, hence at most **sixteen pairs for the
   entire prefix**.

Together with Theorem 15 of the source, testing only these critical pairs for
every prefix through level `m-2` retains at least one unrestricted optimum.
The result applies to every even length at least eight and every alphabet size
for which the `SQN` recurrence is used; the supplied enumerator specializes
to the binary frontier.

## Polynomial proof

Only `x_{m-1},y_{m-1}` depend on `u` below the middle.  In the convolution for
`s_m`, the variable level `m-1` can only pair with level 1, so `s_m(u)` is
affine.  Thus `x_m=t` and `y_m=s_m(u)-t` are affine in `(u,t)`.

The source's condition for level `m+1` is computed from the lower level
`m-1`.  Its initial term is

\[
 y_{m-1}-x_{m-1}=A-2u.
\]

Every remaining term in that condition uses only levels strictly below
`m-1` and already selected upper orientations, so it is constant in `u`.
Therefore the condition is `d-2u`.  Conditions for levels above `m+1` come
from still lower fixed levels and are constant.  The middle variable `t` does
not enter any upper-orientation condition.

Fix one of the resulting orientation intervals.  Before level `2m-2`, two
convolution indices cannot both be at least `m-1`; all those upper coordinates
are consequently affine in `(u,t)`.  At levels `2m-2`, `2m-1`, and the final
objective, products of two variable-dependent factors can occur, but no
product of total degree greater than two can occur: a newly quadratic upper
factor can only pair with a fixed low level before the objective.  Hence the
objective is bivariate quadratic.

A `t^2` term requires two factors whose indices are at least `m`, and their
indices must sum to `2m`.  The only such final summand is

\[
 x_m y_m=t(s_m(u)-t).
\]

It contributes `-t^2`, and no other summand contributes `t^2`.  This proves
(1).

## Exact critical-set proof

For a fixed integer `u`, put `B(u)=a u+b` and `S(u)=p u+r`.  Since the
coefficient of `t^2` is `-1`, a canonical maximizing value of `t` is

\[
 t(u)=
 \begin{cases}
 0,& B(u)\le0,\\
 S(u),& B(u)>0\text{ and }B(u)\ge2S(u),\\
 \lfloor B(u)/2\rfloor,&0<B(u)<2S(u).
 \end{cases}                                      \tag{2}
\]

When `B(u)` is odd, the ceiling gives the same value, so the floor is enough.
Each regime in (2) is an integer interval because it is defined by affine
inequalities in one variable.

On the lower regime, substituting `t=0` leaves an ordinary quadratic in `u`.
On the upper regime, substituting the affine boundary `t=S(u)` again leaves a
quadratic.  A quadratic on an integer interval is maximized at its two
endpoints if convex or linear, and at the at most two integers adjacent to its
vertex if concave.  Thus at most two `u` values are required in each boundary
regime.

On the interior regime the optimized value is

\[
 c u^2+e u+f+\left\lfloor\frac{B(u)^2}{4}\right\rfloor.       \tag{3}
\]

After fixing the parity of `B(u)`, four times (3) is an ordinary quadratic.
If `a` is even there is one parity class; if `a` is odd the two classes are
the two parity progressions for `u`.  Each progression again needs at most two
endpoint- or vertex-adjacent values.  The interior therefore contributes at
most four candidates.  The total is at most `2+2+4=8` on one orientation
interval and at most sixteen across both intervals.

The intervals, parity progressions, and rational vertices use exact integer
floor and ceiling division; there is no numerical approximation.  Applying
the construction to the prefix and orientation cell containing an unrestricted
optimum proves that at least one optimum occurs in the retained set.

## Complete binary reductions

The C++ implementation symbolically propagates every bivariate coefficient,
asserts total degree at most two, checks the `t^2=-1` identity, and verifies the
orientation condition at both feasible `u` endpoints on every prefix.  It
then generates exactly the candidates proved above.

```
n=24
prefixes through level m-2          192,656
raw last-two-layer leaves       321,286,030
critical pairs                      430,794
reduction factor                    745.7997
largest critical set per prefix             5
recovered optimum                    147,312

n=26
prefixes through level m-2        6,001,931
raw last-two-layer leaves    30,699,841,782
critical pairs                   13,317,209
reduction factor                  2,305.2760
largest critical set per prefix             5
recovered optimum                    547,337
```

These are complete trees, not sampled prefixes.  The raw leaf totals are the
same last-two-layer obligations in the source enumeration.  The observed
maximum of five is not asserted as a theorem; sixteen is the proved universal
bound.

## Scope

This theorem removes the last two free-layer loops but does not determine
`S(2,30)`, move its current endpoints, or prove the source's general
conjecture.  At length 30, enumeration through level 13 remains too large for
a near-term direct completion.  A third mathematical pass must therefore
obtain endpoint movement or a further independently valuable certification
theorem rather than merely extending these counts.

## Source dependency

Lidija Stanovnik, Miha Moškon, and Miha Mraz, *In search of maximum
non-overlapping codes*, Designs, Codes and Cryptography 92 (2024), 1299--1326,
[doi:10.1007/s10623-023-01344-z](https://doi.org/10.1007/s10623-023-01344-z),
[arXiv:2307.12593v2](https://arxiv.org/abs/2307.12593).
