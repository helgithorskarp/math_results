# Exact stacking number of every double star

Let $S_{a,b}$ be the tree obtained from the edge $xy$ by adjoining $a$ leaves
to $x$ and $b$ leaves to $y$, where $a\ge b\ge1$.  The result proved here is

$$
\operatorname{stack}(S_{a,b})=5a+3b+7.
$$

This verifies the Csernák--Soukup tree-stacking formula for every tree of
diameter three, an infinite family.  The parameter is the new stacking number
from Csernák and Soukup's 2026 paper, not cover pebbling or one of the several
cover-rubbling parameters that also use the word "stacking."

## Estimate

For a leaf on the $a$-side, the Csernák--Soukup estimate is

$$
1+2(a+1)+4(b+1)+1+(a+b-1)=3a+5b+7.
$$

For a leaf on the $b$-side it is $5a+3b+7$; roots at the two centers give
$2a+3b+4$ and $3a+2b+4$.  Hence the maximum is $5a+3b+7$.

## Constructive upper bound

Start with an arbitrary configuration.  From every leaf, move every available
pair to its center.  Let $X,Y$ be the resulting center piles and let $p\le a$,
$q\le b$ be the numbers of unit leaf residues.  If the original norm is $m$,

$$
m\le 2X+2Y+p+q. \tag{1}
$$

A unit leaf can be cleared at net cost one pebble from its center whenever the
center has at least two.  The reduced configuration is therefore stackable in
each of these three cases:

1. $X\ge p+1$, $Y\ge q+1$, and $X+Y\ge p+q+3$;
2. $X\le p$ and $Y\ge2(p+1-X)+q+2$;
3. $Y\le q$ and $X\ge2(q+1-Y)+p+2$.

In the second case, for example, make $p+1-X$ moves from $y$ to $x$, clear all
unit leaves, and obtain two center piles of total at least three.  Every
two-vertex configuration of norm at least three is stackable.

If none of the cases applies, then respectively

$$
\begin{aligned}
2X+2Y+p+q&\le3p+3q+4,\\
2X+2Y+p+q&\le5p+3q+6-2X,\\
2X+2Y+p+q&\le3p+5q+6-2Y.
\end{aligned}
$$

Since $p\le a$, $q\le b$, and $a\ge b$, every right-hand side is at most
$5a+3b+6$.  Equation (1) now proves that every configuration of norm
$5a+3b+7$ is stackable.

## Sharp non-stackable configuration

Put

$$
L=4a+2b+7
$$

pebbles on one leaf $z$ adjacent to $y$, put one pebble on every other leaf,
and leave the centers empty.  Its norm is $5a+3b+6$.

To see that it cannot stack, root a hypothetical successful move sequence at
its final support and count moves on every oriented edge.  A non-target unit
leaf contributes at most $-1$ pebble to its neighbor.  The heavy odd leaf
contributes at most

$$
(L-3)/2=2a+b+2.
$$

The branch consisting of an empty center with $a$ unit leaves contributes at
most $-2a-3$ across its parent edge: if $r\ge1$ moves leave the center for its
parent, the balance equations force at least $a+2r$ reverse moves, for net
contribution at most $r-2(a+2r)\le-2a-3$.

These bounds give final pile at most zero when the target is $x$ or $y$, an
$a$-side leaf, a non-heavy $b$-side leaf, or the heavy leaf $z$.  More
explicitly, the key effective totals are

$$
\begin{array}{c|c}
\text{target}&\text{upper bound on final pile}\\ \hline
y&(2a+b+2)-(b-1)-(2a+3)=0,\\
x&-a+a=0,\\
\text{$a$-side leaf}&1-1=0,\\
\text{other $b$-side leaf}&1-1=0,\\
z&L+2(-2a-b-2)-3=0.
\end{array}
$$

For the $x$ row, the whole $y$-branch contributes at most $a$: its leaf input
has the form $2a+3-3h$, and optimizing the final edge-flow count gives at most
$a$.  The same calculation after deleting the target leaf gives the two unit
leaf rows.  Thus no positive final pile is possible at any vertex, proving the
lower bound.

## Exact finite checks

`enumerate_double_stars.cpp` independently runs the complete parent/child
recurrence for non-stackable configurations.  It quotients by arbitrary
permutations of the leaves on either side (and by side exchange when $a=b$).
The default run checks all $S_{a,b}$ with $a+b\le8$, i.e. through order ten.

`verify_arithmetic.py` exhausts the integer case split used in the upper bound
for a configurable range of parameters and checks the lower-bound identities.
These programs are validation aids; the infinite-family theorem rests on the
proof above, not on extrapolation from the finite runs.

A fresh GCC 12.2.0 run checked all 16 parameter pairs through order ten.  The
same run under AddressSanitizer and UndefinedBehaviorSanitizer produced the
identical deterministic output.  Its SHA-256 is
`7753dd2a62fc05ddcd921c3b2b1a4cb55d0a103323227d1045c9c2b851b6baad`.
The Python 3.11.2 arithmetic output has SHA-256
`6c34695637a8622f164527e4260c552416f2e2949cc1f7e2735c429e26205481`.
Both logs belong under `/scratch` and are intentionally not committed.

```bash
g++ -std=c++20 -O3 -DNDEBUG -march=native \
  -Wall -Wextra -Wpedantic \
  enumerate_double_stars.cpp -o /scratch/enumerate_double_stars

/scratch/enumerate_double_stars 8 \
  > /scratch/double-star-enumeration.log

python3 verify_arithmetic.py \
  --exhaustive-max-a 10 --identity-max-a 1000
```

Source hashes:

```text
enumerate_double_stars.cpp  8a2e9eadaefebec163dcc2d5472231d8e6af8c4df52667186ef41108234ceb53
verify_arithmetic.py        465a669844a7eb3af9120bfb83bc1531b23f7269b5deb7417c2b04b5d33923b2
```

## Trust boundary and prior art

The proof uses exact integer inequalities and move-count balance equations.
The finite census depends on the recurrence, symmetry canonicalization, C++
standard-library behavior, and the compiler/runtime.  No floating-point
decision, randomized search, solver verdict, or external proof certificate is
used.

The searched primary source is T. Csernák and L. Soukup, *Stacking and clearing
in graph pebbling*, arXiv:2604.22341v1 (2026), which conjectures the tree formula
and verifies trees only through order seven.  Their companion repository was
inspected at commit `701cdd93dd19869a9b90947edd6361efd81cfc1f`.  Targeted
searches found work on double stars for different cover-rubbling parameters,
but no result for this stacking number.  The theorem is therefore apparently
new to the searched sources, not a literature-priority claim.
