# Exact uniform-cost stacking on the four-vertex path

## Theorem

Let `P4` be the path on four vertices.  A move of cost `k` removes `k`
pebbles from one vertex and adds one pebble at an adjacent vertex.  A
configuration is *stackable* if moves can leave a positive pile at one
vertex and zero pebbles everywhere else.  For `k >= 3`, let

- `sigma_k(P4)` be the first mass at which every configuration of exactly
  that mass is stackable, and
- `tau_k(P4)` be the first mass from which every configuration of every
  larger mass is stackable.

Then

```text
sigma_k(P4) = tau_k(P4) = k^4 - k + 1.                 (1)
```

Moreover, the only nonstackable configurations of the largest possible
mass `k^4-k` are

```text
(k^4-k-1, 0, 0, 1)  and  (1, 0, 0, k^4-k-1).          (2)
```

Thus the first subdivision beyond the previously solved two-leaf star has a
sharp all-cost answer and a rigid equality case.  The result is not claimed
for longer paths here.

## Exact transfer criterion

Put

```text
M      = k^2-1,
lambda = k^2-k-1,
A      = k^3-k-1,
H      = k^4-k.
```

We use the established uniform-cost tree transfer criterion.  For a
nonempty directed branch with effective input `s`, its message is

```text
g(s) = k*s - M*max(1, ceil(s/k)).                       (3)
```

An empty branch has message zero.  The score at a possible final target is
its pile plus all incoming branch messages, and the configuration can be
stacked there exactly when that score is positive.  Hence a configuration
is nonstackable exactly when all four scores are nonpositive.

Two elementary facts about (3) will be used repeatedly:

```text
g(1)              = -lambda,
g(-lambda)        = -A,
g(-A)             = -(H-1),
g(H-1)            = A,
g(A)              = lambda,
g(lambda)         = -1.                                (4)
```

If `s > 0` and `g(s)=m`, then, for one
`h in {0,...,k-1}`,

```text
s = k*m + M*h.                                          (5)
```

For `s <= 0`, instead `g(s)=k*s-M`.

## The three-vertex input bound

We first record the only earlier extremal fact needed below:

```text
Every nonstackable configuration on P3 has mass at most
k*M = k^3-k.                                             (6)
```

Here is a short self-contained derivation.  Let `x` be the center pile and
let `t` be the number of occupied leaves.  A nonstackable positive
configuration has support at least two, so `1 <= t <= 2`.  Write each
occupied leaf pile and its message as

```text
c_i = k*u_i+d_i+1,       0 <= d_i <= k-1,
p_i = u_i+k*d_i-lambda.
```

Write the center score as `x+sum p_i=-a`, where `a >= 0`, put
`D=sum d_i`, `B=(k-1)M`, and `J=floor(k*a/M)`.  Direct substitution gives

```text
R = t*B-k*a-M*D-(k-1)*x,                                (7)
```

where `R` is the total mass.  At occupied leaf `i`, put

```text
C_i = max(1, ceil((-a-p_i)/k)).
```

Its target score is

```text
-k*a + M*(k-1-d_i-C_i).
```

If some `d_i >= k-2-J`, then `J+D >= k-2`, and (7) gives

```text
R <= 2B-M(k-2) = kM.
```

Otherwise every `d_i < k-2-J`.  The leaf-score inequality gives
`u_i <= k-2-a+kJ`.  In this case `0 <= J <= k-3` and
`a >= ceil(MJ/k)=kJ`, so every `u_i <= k-2`.  Eliminating `x` with the
center-score identity yields

```text
R = t*k*(k-1)+(k-1)(sum u_i-D)-a
  <= 2t(k-1)^2
  <= 4(k-1)^2
  < kM.
```

The last difference is `(k-1)(k^2-3k+4)>0`.  This proves (6).

## A two-vertex branch envelope

Consider a two-vertex branch `x--y`, rooted at `x`, with a nonzero
configuration.  Let `m` be its outgoing message and define its excess

```text
X = m+A.
```

Then `X >= 0` and its mass `S` satisfies

```text
S <= 1+k*b(X),                                          (8)
```

where, with `T=k^3-k^2`,

```text
b(X) = X/k                         if 0 <= X <= T,
       kX-M(k^2-k)                 if X >= T.            (9)
```

To prove this, let `p` be the message from the terminal vertex `y` and put
`Y=p+lambda`.  If `y` is occupied, (5) gives
`y <= 1+kY`; if it is empty, the same inequality is harmless.  In either
case `Y >= 0`.  If `s=x+p` is the effective input at the root, then
`x+Y=s+lambda`.  For `s <= 0`, (3) gives

```text
x+Y = X/k.
```

For `s > 0`, (5) gives

```text
x+Y <= kX-M(lambda+1),
```

and this case can occur only when `X >= T`.  The two bounds meet at `T`
and are exactly (9).  Finally,

```text
x+y <= 1+x+kY <= 1+k(x+Y),
```

which proves (8).

## The endpoint-deficit lemma on P3

Let `(u,x,y)` be a nonstackable configuration on `P3` with `u>0`, total
mass `R`, and score `-D` at the endpoint carrying `u`, where `D >= 0`.
Then

```text
R + (k-1)u + M*floor(D/k)
    <= 1+kA
     = k^4-k^2-k+1.                                    (10)
```

Indeed, the complementary branch `x--y` is nonempty.  Its message is
`-u-D`, so its excess in (8) is

```text
X=A-u-D.
```

In particular `u+D <= A`, and (8) gives

```text
R <= u+1+k*b(X).                                        (11)
```

If `X <= T`, substitute the first line of (9) into (11).  The left side of
(10) is at most

```text
1+(k-1)u+A-D+M*floor(D/k)
 <= 1+kA-[kD-M*floor(D/k)]
 <= 1+kA.                                               (12)
```

For `D=kq+r`, `0 <= r < k`, the bracket in (12) is `q+kr`, hence is
nonnegative.  Equality in this case forces `D=0`, `u=A`, and `X=0`.

If `X >= T`, the second line of (9), `u >= 1`, and
`-k^2D+M floor(D/k) <= 0` bound the same expression by

```text
1+k^2A-k(k-1)-kM(lambda+1).
```

This is smaller than `1+kA` by exactly `2k(k-1)`.  This proves (10),
including its equality statement.  If equality holds, (8) also forces the
complementary branch to have mass one; its message is `-A`, so that one
pebble must be at `y`, not at `x`.  Thus equality in (10) occurs only at

```text
(u,x,y)=(A,0,1),  D=0.                                  (13)
```

## Upper bound on P4

Write a configuration on the path as `(a,b,c,d)`.  Let `p` be the message
of the one-vertex branch at `a`: it is zero when `a=0`, and `g(a)` otherwise.
Define the collapsed left endpoint

```text
u=b+p.
```

Similarly, if `s` is the endpoint message at `d`, define

```text
v=c+s.
```

Suppose first that `u>0`.  Replacing the first two vertices by a single
endpoint pile `u` produces the genuine `P3` configuration `(u,c,d)`.
Its three scores are exactly the last three scores of the original
configuration, so it is nonstackable.  Let its mass be `R` and its score at
`u` be `-D`.

If `a=0`, the desired bound follows immediately from (6).  Otherwise (5)
writes

```text
a=k*p+M*h,       0 <= h <= k-1,
```

and `b=u-p >= 0`.  The original score at `a` is

```text
a+g(-D-p) <= 0.                                         (14)
```

If `p+D >= 0`, (3) turns (14) into

```text
M(h-1) <= kD.
```

If `h<=1` the required bound is immediate.  Otherwise
`1 <= h-1 <= k-2`, and
`ceil(M(h-1)/k)=k(h-1)`; hence in every case
`h <= 1+floor(D/k)`.  Therefore (10) gives

```text
a+b+c+d
 = R+(a-p)
 <= R+(k-1)u+M(1+floor(D/k))
 <= (1+kA)+M
 = H.                                                   (15)
```

If `p+D<0`, then `p <= -1`, so

```text
a-p=(k-1)p+Mh <= (k-1)(M-1).
```

Using (6), the whole mass is at most

```text
kM+(k-1)(M-1) < H;
```

the gap is `(k-1)(k^2(k-1)+2)`.

The same argument applies from the right whenever `v>0`.  It remains only
the case `u<=0` and `v<=0`.  If `a>0`, then `p<=u<=0` and

```text
a+b=a+u-p <= a-p=(k-1)p+Mh <= (k-1)M.
```

If `a=0`, then `b=0` and the same bound holds.  The right pair has the same
bound, so the total is at most `2(k-1)M`, strictly below `H`; the gap is
`(k-1)(k^3-k^2+k+2)`.  This completes the universal upper bound.

Equality in (15) is rigid.  The equality statement in (10) forces
`D=0`, `u=A`, and the reduced configuration `(A,0,1)`.  Equality in the
extension step forces `p=u`, `h=1`, and `b=0`, hence

```text
a=kA+M=H-1.
```

The opposite orientation is symmetric.  Every other case above was strict,
so (2) is the complete equality classification.

## Lower bound and the first exact universal mass

Equations (4) show directly that `(H-1,0,0,1)` and its reversal have all
four target scores zero.  They are nonstackable and have mass `H`.

More is needed to identify `sigma`, because exact-mass universality need not
be monotone when `k>2`.  For each `r in {0,...,k-2}`, reduce the heavy pile
by `r`.  The messages from the heavy side become

```text
A-kr,   lambda-r,   -1-kr,
```

while those from the unit side are unchanged.  The four scores are

```text
-r, -kr, -r, -kr.
```

Thus every mass in the final window `H-(k-2),...,H` has an explicit
obstruction.

Every configuration of mass greater than `4(k-1)` has a legal move.  Hence,
if all configurations of a mass `P>4(k-1)` stacked, then all configurations
of mass `P+k-1` would stack: make one legal move and invoke universality at
mass `P`.  The final window contains one representative of every residue
class modulo `k-1`, so it rules out any earlier universal mass above
`4(k-1)`.  At every mass from `2` through `4(k-1)`, a frozen nonstackable
configuration exists by using at least two piles, each at most `k-1`.
Together with the upper bound, this proves (1).

## Verification

The standard-library verifier checks the exact transfer arithmetic,
exhausts the branch envelope and endpoint-deficit lemma in stated finite
domains, compares the transfer criterion against a direct legal-move oracle,
and performs complete boundary censuses for `k=3,4`.  The boundary census
finds exactly the two configurations in (2) at mass `H` and none at
`H+1`.

```bash
python3 -B graph_theory/uniform_cost_path4_stacking/verify.py \
  --check-expected
```

Expected final status: `PASS`.

The computation corroborates the all-`k` proof; it is not a substitute for
it.  The exact transfer criterion is an explicit mathematical dependency.
The direct oracle used in the low-mass control knows only the legal move
rule, and every recursive call has smaller total mass.

## Scope and attribution

The ordinary cost-two path formula is in Csernak and Soukup, *Stacking and
clearing in graph pebbling*, arXiv:2604.22341.  The signed tree-transfer
criterion and the sharp higher-cost star theorem are prior Discovery Net
dependencies, respectively
`bafkreigcl7n5fvmcv3voxn43tipwwit4457btjkjduz3kzx3zmekkjcnt4` and
`bafkreib46bthe4tw3b3rcfmnfachhnpxy2iiljgkeyukklracv2xrqebca`.

The new contribution is (1), the two-vertex branch envelope (8)-(9), the
endpoint-deficit inequality (10), and the equality classification (2).  It
does not assert the analogous formula for `P_n` with `n>=5`, nor an arbitrary
higher-cost tree theorem.  Targeted primary-source searches on 20 September
2026 found no statement of this uniform-cost `P4` result; that is scoped
novelty evidence, not a priority claim.
