# An infinite counterexample to the proposed three-color restricted Schur formula

For every integer $k\ge2$,

$$S_3(k;2)\ge k(k+1)(k+2)-2.$$

This gives a negative answer to Open Question 6.2 in Collier Gaiser,
[*Restricted generalized Schur numbers*, arXiv:2608.08789v1](https://arxiv.org/html/2608.08789v1#S6).
The question asks whether $S_3(k;2)=k^3+3k^2+k-1$ for all sufficiently large
$k$. Our lower bound exceeds that expression by $k-1$ for every $k\ge2$.
It does not establish the exact value of $S_3(k;2)$.

The construction extends the six intervals in Gaiser's Proposition 6.1 by
one red interval of length $k-1$. We prove the stronger assertion that the
resulting coloring avoids every monochromatic sum of $k$ summands that are
not all equal. We also determine the unique maximal extension of the
published prefix when its colors are held fixed.

## Convention

Write $[a,b]=\{a,a+1,\ldots,b\}$ for integer endpoints. The restricted
generalized Schur number $S_3(k;\ell)$ is the **least forcing integer** $n$
such that every three-coloring of $[1,n]$ has a monochromatic solution

$$x_1+\cdots+x_k=y$$

with exactly $\ell$ distinct values among the summands. All variables are
positive integers and repetitions among summands are allowed. Since
$k\ge2$, the sum $y$ is larger than each summand; thus the solution has
$\ell+1$ distinct values including $y$. This agrees with Gaiser's
definition. Existence for $2\le\ell\le k$ is his Theorem 2.4.

A coloring of $[1,n]$ avoiding such solutions proves $S_3(k;\ell)\ge n+1$.
When $\ell=2$, the forbidden equations can equivalently be written
$a x+(k-a)z=y$ with $1\le a<k$ and $x<z$.

## Construction and theorem

Fix an integer $k\ge2$ and put

$$L=k^2+2k,\qquad U=kL=k^3+2k^2,$$
$$F=k^3+3k^2+k-1,\qquad Q=F+k-1=k(k+1)(k+2)-2.$$

Color $[1,Q-1]$ by the following consecutive intervals:

| Name | Interval | Color |
| --- | --- | --- |
| $R_1$ | $[1,k]$ | red |
| $B_1$ | $[k+1,k^2+k]$ | blue |
| $R_2$ | $[k^2+k+1,L-1]$ | red |
| $G$ | $[L,U]$ | green |
| $R_3$ | $[U+1,U+k-1]$ | red |
| $B_2$ | $[U+k,F-1]$ | blue |
| $R_4$ | $[F,Q-1]$ | red |

All seven intervals are nonempty for $k\ge2$ and partition the specified
integer interval. The first six are exactly the construction in Gaiser's
Proposition 6.1 on $[1,F-1]$; $R_4$ is the extension established here.

**Theorem 1.** This coloring has no monochromatic solution
$x_1+\cdots+x_k=y$ whose summands are not all equal. Consequently,

$$S_3(k;\ell)\ge Q\qquad(2\le\ell\le k),$$

and the same lower bound holds for the least integer forcing a
monochromatic solution with at least two distinct summand values.

**Proof.** Take $k$ summands of one color, not all equal, and write $s$ for
their sum. We show that $s$ is outside that color's class.

If the summands are green, each is at least $L$. Nonconstancy and
integrality give $s\ge kL+1=U+1$, beyond all green integers.

If the summands are blue and all lie in $B_1$, then

$$k^2+k+1\le s\le k(k^2+k)=k^3+k^2<U+k.$$

The lower inequality uses nonconstancy. Thus $s$ is above $B_1$ and below
$B_2$. If at least one blue summand lies in $B_2$, then

$$s\ge (U+k)+(k-1)(k+1)=F,$$

which is above all blue integers.

For red summands there are six exhaustive cases.

1. If one lies in $R_4$, then
   $s\ge F+(k-1)\cdot1=Q$.
2. Suppose no summand lies in $R_4$, and at least two lie in $R_3$.
   Then $s\ge2(U+1)+(k-2)\cdot1=2U+k>Q-1$, since
   $2U+k-(Q-1)=k^3+k^2-k+3>0$.
3. Suppose exactly one summand lies in $R_3$ and at least one lies in
   $R_2$, with none in $R_4$. Then
   $$s\ge(U+1)+(k^2+k+1)+(k-2)\cdot1=Q+2.$$
4. Suppose exactly one summand lies in $R_3$ and the remaining $k-1$
   summands lie in $R_1$. Then
   $$U+k\le s\le(U+k-1)+(k-1)k=F-k\le F-1,$$
   so $s\in B_2$.
5. Suppose every summand lies in $R_1\cup R_2$ and at least one lies
   in $R_2$. Then
   $$L=(k^2+k+1)+(k-1)\le s\le k(L-1)=U-k,$$
   so $s\in G$.
6. If all summands lie in $R_1$, nonconstancy gives
   $k+1\le s\le k^2-1$, so $s\in B_1$.

In every case the sum is either a different color or larger than $Q-1$.
This proves the avoidance statement. Any solution with exactly
$\ell\ge2$ distinct summand values has nonconstant summands, giving all
the stated lower bounds. $\square$

**Corollary 2.** The equality in Open Question 6.2 fails for every
$k\ge2$, and in particular cannot hold eventually.

**Proof.** By Theorem 1, $S_3(k;2)\ge Q=F+k-1>F$. $\square$

## Exact extension of the published prefix

**Theorem 3.** Among colorings avoiding monochromatic solutions with
exactly two distinct summand values, Gaiser's fixed coloring of
$[1,F-1]$ has a unique extension to $[1,Q-1]$: every integer of
$[F,Q-1]$ is red. It has no extension to $[1,Q]$.

**Proof.** Let $t\in[F,Q]$. Two equations using only summands in the
original prefix prevent $t$ from being blue or green.

For blue, set

$$b=t-(k-1)(k+1),\qquad t=(k-1)(k+1)+b.$$

Here $k+1\in B_1$ and

$$U+k\le b\le U+2k-1\le F-1,$$

so $b\in B_2$ and $b>k+1$. The last inequality holds because
$F-1-(U+2k-1)=k^2-k-1>0$. The summands have exactly two values.

For green, set

$$g=t-(k-1)L,\qquad t=(k-1)L+g.$$

Here

$$L<2L-k-1\le g\le2L-2\le U,$$

so both $L$ and $g$ are distinct green integers in the original prefix.
These bounds hold for every $k\ge2$.

Thus every $t\in[F,Q]$ would have to be red in any avoiding extension.
Theorem 1 shows that assigning red on $[F,Q-1]$ succeeds. At $Q$, however,

$$Q=(k-1)\cdot1+F$$

has exactly two distinct red summand values, so red is forbidden as well.
No color is possible at $Q$. $\square$

This is a maximality statement **with the original prefix fixed**. It is
not an upper bound for all three-colorings and does not imply
$S_3(k;2)=Q$.

## Boundary example and validation

At $k=2$, the construction colors $[1,21]$ with

$$R=\{1,2,7,17,21\},\quad
B=[3,6]\cup[18,20],\quad G=[8,16].$$

The next integer $22$ is forbidden in all colors, respectively by
$1+21$, $3+19$, and $8+14$. This example illustrates the fixed-prefix
claim; no global optimality is asserted even in this smallest case.

The universal proof above uses only exact integer inequalities. The
accompanying code provides finite validation, not the basis for
extrapolating the theorem. A separate auditor enumerates attainable sums
by summand count and number of distinct values (capped at two), without
importing the construction or its interval case split. It is compared
against literal multiset enumeration on small arbitrary sets. A second
check enumerates the equations with exactly two summand values directly.
The source also validates the extension witnesses and rejection controls;
see [README.md](README.md) for commands and precise coverage.

There is no solver, floating-point, external-data, or omitted-certificate
dependency in the proof or public verification. This proof has not been
formalized in a proof assistant or independently reviewed by another
researcher. Gaiser's earlier lower bound remains valid. The present result
answers his proposed eventual equality negatively; it does not change
the leading cubic asymptotic scale of that lower bound or determine a
replacement exact formula.
