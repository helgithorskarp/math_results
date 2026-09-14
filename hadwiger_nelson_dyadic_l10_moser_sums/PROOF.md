# Geometry, phase completeness, and positive interface certificate

All square roots in the physical coordinates are positive. Let
`F=Q(sqrt(2),sqrt(3),sqrt(5),sqrt(11))` and represent its elements in the basis

```text
1, sqrt(2), sqrt(3), sqrt(6), sqrt(5), sqrt(10), sqrt(15), sqrt(30),
sqrt(11), sqrt(22), sqrt(33), sqrt(66), sqrt(55), sqrt(110), sqrt(165), sqrt(330).
```

Independence follows from the independent square classes of the four primes.
A point has 32 rational coefficients: first its real coordinate, then its
imaginary coordinate. Equality of coefficient vectors is physical equality.
Every graph uses all unit pairs between distinct points.

## Atoms and colour lower bounds

The coordinates and their ordering are in README.md. The exact unit edges of
the ten-point atom are

```text
01 04 07 08 15 16 19 23 24 26 29 35 37 38 45 69 78.
```

Here `ab` means the unordered pair of labels `a,b` in `0,...,9`.
The diamonds with opposite pairs `(0,3)` and `(1,2)` force those pairs equal
in any three-colouring. Edge `01` makes the two resulting colours different.
Vertices 4 and 5 each see those same two colours, so both must take the third
colour, contradicting edge `45`. The enumerated four-colour patterns give
the reverse bound. The Moser atom has its usual eleven checked edges; its
two diamonds force the common apex and both far tips equal in three colours,
contradicting the edge between the tips. Thus both atoms are four-chromatic.

Exact finite addition produces `P=L+M`, with 64 distinct points and 212
complete unit edges. The labels of `P` are the lexicographically sorted
32-coefficient vectors. The Moser labels retain their displayed order.

## All phases in the stated class

For nonzero differences `a,b`, let `A=|a|^2`, `B=|b|^2`, and
`c=conjugate(a)*b`. If `|v|=1`, expansion gives

```text
|a+vb|^2 = A+B+c*v+conjugate(c)*conjugate(v).
```

Multiplication by `v` shows that the contact equation is

```text
c*v^2+(A+B-1)*v+conjugate(c)=0.
```

Since `|c|^2=AB`, its two roots for positive
`Delta=4AB-(A+B-1)^2` are exactly

```text
v=(-S +/- i sqrt(Delta))/(2c),   S=A+B-1.
```

Each root has norm one because `S^2+Delta=4AB`.
For the specified class, `A,B` are rational and `Delta=5r^2` with nonzero
rational `r`. Exact rational square-root tests therefore suffice to decide
membership. Enumerating the complete nonzero difference sets, filtering
rational norms, considering all 94*22 retained pairs and both signs, and
deduplicating exact coefficient pairs `(x,y)` for `v=x+y sqrt(5)` produces
28 phases. The output is sorted by that coefficient pair, not by a numerical
angle. Each phase occurs for two ordered difference pairs. This is an exact
finite-loop claim with the displayed formulas and the code as its certificate.
It does not assert that other contact phases satisfy the rational-norm guard.

The radical `sqrt(5)` is outside
`K0=Q(i,sqrt(2),sqrt(3),sqrt(11))`, by square-class independence, and `y` is
nonzero. Hence `v` is outside `K0`. If `p+vm=p'+vm'` with `p,p' in P` and
`m,m' in M`, then `m != m'` would put `v=(p-p')/(m'-m)` in `K0`.
Otherwise `p=p'`. Thus all 448 addresses are distinct physical points.
Address `7*i+j` denotes `P[i]+v*M[j]` in every phase.

## Complete physical unit edges

For each phase, both implementations reconstruct all address coordinates.
After clearing a common denominator `d`, a difference has real coefficient
rows `x,y`. In the square-free basis, the rational coefficient of
`|x+i y|^2` is

```text
sum_j r_j*(x_j^2+y_j^2).
```

A unit edge requires this to equal `d^2`. This is only a necessary filter;
the nonconstant coefficients must also vanish. They are computed both by
bit-indexed multiplication and by the independent identity

```text
sqrt(r)*sqrt(s)=gcd(r,s)*sqrt(r*s/gcd(r,s)^2).
```

All 100,128 unordered address pairs are scanned per phase; the two complete
edge streams are compared entrywise. Across 28 phases, the rational filter
retains 92,688 pairs, and the exact edges have histogram
`2202:12, 2216:16`. No modular or numerical sieve is trusted. The Cartesian
edges contribute 2,188, so the two physical types have 14 and 28 additional
edges. These counts do not classify their graph isomorphism types.

## Complete source-interface extension

Every proper colouring can be globally renamed so that the colours on a
chosen unit triangle are `0,1,2`. Exhausting all assignments on the remaining
vertices and normalizing each row by order of first appearance gives exactly
178 patterns for `L` and 16 for `M`. The checker uses triangles `(0,7,8)` and
`(0,1,2)` respectively. This enumerates all four-colour patterns up to colour
permutation; it is not a selected class of algebraic or additive colourings.

Each certificate entry consists of a phase mask and a 448-colour word. Two
bits encode each colour; in byte `b` the colours occupy bit pairs 0–1, 2–3,
4–5, 6–7 in address order. A phase mask uses bit `k` for exact phase `k`.
The checker validates every indicated edge inequality. It then restricts
the word to each marked atom and normalizes the restriction. For every
source pattern, the union of masks of matching words must contain all 28
phases. This proves surjectivity of each restriction map separately.

The certificate has 717 words and verifies 5,880 source-pattern/phase pairs
through 12,994,800 edge inequalities. Any unnormalized proper source colouring
is a colour permutation of a covered pattern, and the same permutation of
its extension gives the desired full colouring. In particular each complete
physical graph is four-colourable. It contains the marked Moser atom, so its
chromatic number is exactly four. Every subgraph is also four-colourable.

No assertion about simultaneous prescriptions on multiple atoms follows from
the separate surjectivity statements. Nor may one interpret the producer's
abstract union of several address-edge lists as a single plane realization.
That supergraph is used only to find words reusable across different physical
graphs, and all final evidence is checked against the individual exact graphs.

The argument is an exact computer-assisted result about this specified finite
class. It yields neither an unrestricted vertex lower bound nor a new
five-chromatic construction.
