# Proof of the nonlocal matching-cover theorem

Write `a=3m+epsilon`, where `epsilon` is `1` or `2`.  A path in `D(a,3)`
has a unique run form

```text
R^r U R^s U R^t U,
```

and is rational-Dyck exactly when

```text
r+s+t=a,    3r>=a,    3(r+s)>=2a.                 (1)
```

Sorting `(r,s,t)` gives a partition `(x,y,z)`, `x>=y>=z>=0`.  The complete
height-three Lagrange classification orders these partition fibres first by
increasing `z` and, within a fixed `z`, by increasing `y` (equivalently,
decreasing `x`).

## 1. The matching-score structure of one layer

Fix `z`.  The partitions in this layer are

```text
C_y = (a-y-z, y, z),    z <= y <= floor((a-z)/2).  (2)
```

Put `h=a-3y`.  The valid run orders in the fibre are exactly

```text
h>0:  C_y and P_y=(a-y-z,z,y),
h<0:  C_y and N_y=(y,a-y-z,z),                     (3)
```

with repetitions suppressed.  Since `gcd(a,3)=1`, `h` never vanishes.
In particular, the positive chamber is `y<=m`, and the negative chamber is
`y>=m+1`.

We use the complete adjacent-fibre orientation theorem.  Its relevant
consequences, with all inequalities strict when the displayed paths are
distinct, are:

```text
M(C_y) > M(C_(y+1));                               (4)

M(C_z) > M(P_(z+1));                               (5)

M(P_y) > M(P_(y+1))       for z<y<m;               (6)

M(N_(y+1)) < M(C_y)       for y>=m.                (7)
```

For completeness, these follow from the exact local formulas in that
theorem.  If `d=a-z-2y`, the canonical drop in (4) is

```text
2(F_(2d-4)F_(2z+3)+F_(2d-2)F_(2z+1)) > 0.         (8)
```

Equation (5) is the `e=y-z=0` boundary of the local comparison.  Equation
(6) is the alternative-to-alternative difference

```text
M(P_(y+1))-M(P_y)=-6F_(2d-4)F_(2z+1)<0,            (9)
```

and (7) is the low-`h` comparison

```text
M(N_(y+1))-M(C_y)=-2F_(2d-2)F_(2z+1)<0.           (10)
```

The decreasing run order `C_y` is also strictly below every distinct second
run order in its own fibre.  These relations identify the extremes of a
layer.  Its maximum is `C_z`, and its minimum is the canonical path in its
last fibre.  The same
adjacent-fibre theorem says that the minimum of layer `z` is strictly above
the maximum `C_(z+1)` of layer `z+1`.  Consequently the matching-score
intervals of distinct `z`-layers are disjoint and occur in decreasing order
as `z` increases.                                                     (11)

## 2. The candidate gap

Fix `0<=z<=m-1` and put `n=m-z>=1`.  The two paths in the theorem are

```text
X_z=C_(z+1)=(a-1-2z,z+1,z),
Y_z=P_m=(2m+epsilon-z,z,m).                         (12)
```

We now prove `M(Y_z)>M(X_z)` by a closed positive formula.  Put

```text
K_j = [[F_(2j+3),F_(2j+1)],
       [F_(2j+1),F_(2j-1)]],

q(r,s,t)=(K_r K_s K_t)_(2,1).                      (13)
```

Here `F_(-1)=1`; direct expansion of the continued-fraction word gives

```text
M(R^r U R^s U R^t U)=q(r,s,t).                     (14)
```

The within-fibre permutation gain at `y=m` is

```text
M(P_m)-M(C_m)
 = 2F_(2n)F_(2z+4n+2epsilon-1).                    (15)
```

Summing the canonical drops (8) from `y=z+1` through `m-1` gives

```text
(M(X_z)-M(C_m))/2
 = F_(2z+3) S_1 + F_(2z+1) S_2,                   (16)

S_1 = sum_(k=0)^(n-2) F_(2n+2epsilon+4k),
S_2 = sum_(k=0)^(n-2) F_(2n+2epsilon+2+4k),        (17)
```

where an empty sum is zero.  Fibonacci addition in (15) and subtraction of
(16) yield

```text
(M(Y_z)-M(X_z))/2 = F_(2z+1) A + F_(2z) B,         (18)

A = F_(2n)F_(4n+2epsilon-1)-2S_1-S_2,
B = F_(2n)F_(4n+2epsilon-2)-S_1.                   (19)
```

Let `L_j` denote the Lucas numbers.  Binet's formula, or a direct induction,
gives the every-fourth-index sum

```text
sum_(k=0)^(N-1) F_(r+4k)
 = (L_(r+4N-2)-L_(r-2))/5                         (20)
```

for even `r`.  The product identity

```text
5F_pF_q=L_(p+q)-(-1)^q L_(p-q)                    (21)
```

uses the standard extension `L_(-j)=(-1)^j L_j` when its final index is
negative.  It then simplifies (19) to

```text
5A = 4L_(6n+2epsilon-5)+3L_(2n+2epsilon-2),
B  = F_(6n+2epsilon-4).                            (22)
```

All indices in (22) are positive.  Substituting into (18) proves the exact
formula

```text
5(M(Y_z)-M(X_z))
 = 2F_(2z+1)(4L_(6n+2epsilon-5)+3L_(2n+2epsilon-2))
   +10F_(2z)F_(6n+2epsilon-4) > 0.                 (23)
```

## 3. Nothing lies in the gap

Relations (4), (6), and (7) show that every path in layer `z` belongs to one
of two score blocks:

```text
all C_y with y>=z+1 and all N_y have score <= M(X_z);
all P_y with z<=y<=m have score >= M(Y_z).          (24)
```

The first equalities occur only at `X_z`, and the second only at `Y_z`.
Indeed, the canonical branch is strictly decreasing, the positive
permutation branch is strictly decreasing toward `P_m`, and every negative
permutation has already fallen below an earlier canonical score.  Equation
(23) separates the two blocks.

By (11), every layer below `z` has all its scores above layer `z`, and every
layer above `z` has all its scores below layer `z`.  Hence no path anywhere
in `D(a,3)` has matching score strictly between `M(X_z)` and `M(Y_z)`, and
neither endpoint score has a tie.  Thus `X_z <_M Y_z` is a singleton-level
matching cover.

Finally, within layer `z`, the fibre of `X_z` has parameter `y=z+1`, while
the fibre of `Y_z` has parameter `y=m`.  Their distance in the complete
Lagrange chain is therefore

```text
m-(z+1)=m-z-1.                                     (25)
```

Taking `z=0` makes this distance tend to infinity with `a`, completing the
proof.
