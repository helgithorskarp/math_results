# Proof of the upper-coatom theorem

Write `F_0=0`, `F_1=1`, and `F_(m+1)=F_m+F_(m-1)`.  A path is below the
diagonal when every prefix `v` satisfies

```text
a * #U(v) <= b * #R(v).
```

Both `A` and `B` satisfy this condition.  Every path starts with `R` and ends
with `U`; the latter follows because a final `R` would leave the prefix
`(a-1,b)`, which is above the diagonal.

## Matching order

We use the block merger of Apruzzese--Cong.  If

```text
w = S1 R U^u R^r U S2,
w' = S1 R^(r+1) U^(u+1) S2,
```

then `M(w')>=M(w)`.  The inequality is strict unless `S1` is empty or is the
one-letter word `U`.  Geometrically the replacement pushes the intervening
subpath down and to the right, so it preserves membership in `D(a,b)`.

If a path has at least six blocks, apply the merger to its first `U`-block
and the following `R`-block.  Its first `R`-block has length at least two,
since the prefix ending at the first `U` must satisfy `a<=b r_1` and `a>b`.
Thus `S1=R^(r_1-1)` is nonempty, and the score increases strictly.  Repeating
reduces the problem to a four-block path

```text
w = R^r1 U^u1 R^r2 U^u2,
r1+r2=a,  u1+u2=b,  r1>=2.
```

For this path, Equation (3.1) of Apruzzese--Cong, with the all-one prefix and
suffix continuants evaluated as Fibonacci numbers, gives

```text
M(H)-M(w)
 = 2 F_(2u1) F_(2r2)
     (F_(2r1-1) F_(2u2-2) + F_(2r1-2) F_(2u2)).       (1)
```

The elementary identity

```text
F_(2x) F_(2y)
 = F_(2(x+y-1)) + F_(2x-2) F_(2y-2)                  (2)
```

holds for positive `x,y`.  In particular,

```text
F_(2x) F_(2y) >= F_(2(x+y-1)),                       (3)
```

with equality exactly when `x=1` or `y=1`.

For completeness, (2) follows by expanding `F_(2x)=F_(2x-1)+F_(2x-2)`:
the difference between its left side and its final product is
`F_(2x-1)F_(2y)+F_(2x-2)F_(2y-1)`, which is
`F_(2x+2y-2)` by the Fibonacci addition formula.

Dropping the first nonnegative summand in parentheses in (1), regrouping,
and applying (3) twice gives

```text
(M(H)-M(w))/2
 >= (F_(2u1) F_(2u2)) (F_(2r2) F_(2(r1-1)))
 >= F_(2b-2) F_(2a-4).                               (4)
```

For `A`, equality holds in (4), so

```text
M(H)-M(A) = 2 F_(2b-2) F_(2a-4).                     (5)
```

Equality in (4) first requires `u2=1`, because the discarded term is zero
only then.  It then requires `r2=1` or `r1=2`.  The first choice gives `A`.
The second would require the prefix endpoint `(2,b-1)` to satisfy

```text
a(b-1) <= 2b.                                         (6)
```

For `b>=3`, this contradicts `a>=b+1`.  For `b=2`, coprimality and (6) force
`a=3`, when the alleged second case is again `A`.  Hence `A` uniquely
maximizes `M` among all nonmaximum four-block paths.  Every path with more
blocks was strictly increased on reduction to four blocks, so `A` is the
unique matching coatom.

## Lagrange order

For positive integers `c_1,...,c_m`, define

```text
X(c_1,...,c_m)
 = [0; overline(1^(2(c_1-1)),2, ..., 1^(2(c_m-1)),2)].
```

We use the standard alternating lexicographic rule: if two positive simple
continued fractions first differ at partial quotient `j`, then at odd `j`
the smaller digit gives the larger value, while at even `j` the larger digit
gives the larger value.  This applies unchanged to unequal periodic strings.

The following concentration inequality is immediate from that rule:

```text
X(p,q,r,s) <= X(p+r-1,1,1,q+s-1),                    (7)
```

with equality exactly when `q=r=1`.  Indeed, if `r>1`, after the common
`2(p-1)` initial ones the left string has `2` while the right string still
has `1`; this is the odd position `2p-1`.  If `r=1` and `q>1`, the strings
agree through the following `2`, after which the left has `1` and the right
has `2`; this is the even position `2p`.  If `q=r=1`, the periodic strings
are identical.

The coefficient period `(2,C(w))` is the cyclic run encoding of the path:
every path block of length `c` contributes `2(c-1)` ones, followed by a `2`
at the transition.  At a transition between adjacent blocks, the corresponding
candidate in the maximum formula for `L` is `2` plus the two `X`-values read
in the two cyclic directions.

First suppose `w` has at least six blocks.  Choose a transition attaining
`L(w)`.  There are at least three blocks of each step type, so its adjacent
`R`- and `U`-block lengths are at most `a-2` and `b-2`.  In each cyclic
direction, compare its `X`-value with the corresponding value at the
`(a-1,b-1)` transition of the candidate cyclic block word

```text
(a-1,b-1,1,1).
```

The candidate begins with a strictly longer even run of ones.  At the first
difference it has `1` where the original has `2`, at an odd position, so each
candidate `X`-value is strictly larger.  Therefore `L(w)<L(A)`.

It remains to consider four blocks.  Cyclically label their lengths
`(x,y,z,t)`, with `x,z` of one step type and `y,t` of the other, so that the
chosen transition between `x` and `y` attains `L(w)`.  Then

```text
L(w) = 2 + X(y,z,t,x) + X(x,t,z,y).
```

Apply (7) to both terms:

```text
X(y,z,t,x) <= X(y+t-1,1,1,x+z-1),
X(x,t,z,y) <= X(x+z-1,1,1,y+t-1).
```

Their sum is the value at the large-block transition of the cyclic word
`(a-1,b-1,1,1)`, up to exchanging `a` and `b`; it is therefore at most
`L(A)`.  Both inequalities are equalities exactly when `z=t=1`.  Hence
equality requires the cyclic block lengths to be `(a-1,b-1,1,1)` up to
dihedral symmetry.

A linear path in `D(a,b)` begins with an `R`-block.  Of the four possible
assignments of the two `R`-lengths `{a-1,1}` and two `U`-lengths `{b-1,1}`,
the two beginning with `RU` violate the diagonal condition at `(1,1)` because
`a>b`.  The remaining paths are precisely `A` and `B`.  Their cyclic block
words are dihedrally equivalent, so `L(A)=L(B)`.  They coincide exactly for
`b=2`.  This proves the Lagrange-coatom classification.
