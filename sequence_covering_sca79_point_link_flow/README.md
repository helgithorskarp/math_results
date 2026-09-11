# Complete global point-link relaxation for `SCA(5040;7,9)`

## Result

This directory solves, in closed form, the complete one-point marginal
relaxation of the open `SCA(5040;7,9)` problem.  It does **not** decide whether
the sequence covering array exists.

For every distinguished symbol, all 256 counts indexed by the set of symbols
preceding it are parameterised by nine integers.  For all nine distinguished
symbols at once, the resulting `9*256` counts are globally realisable by a
multiset of 5040 permutations if and only if ten explicit linear balance
conditions hold.  Thus the global point-link relaxation reduces to 81 integer
parameters, local subset-sum inequalities, and ten balances.

An exhaustive exact census, independently reproduced by two algorithms, gives:

| object, modulo relabelling of the other eight symbols | count |
| --- | ---: |
| admissible full point-link profiles | 243,545 |
| induced symbol-position types | 1,695 |
| types surviving position moments plus separate deletions | 1,769 |
| types newly excluded by the full point link | 74 |

The open status of `SCA(5040;7,9)` is recorded by Gentle, Horsley and Wanless,
[*Excess Coverage Arrays and Levenshtein's Conjecture*](https://arxiv.org/abs/2411.17145)
(Designs, Codes and Cryptography, 2025,
[DOI 10.1007/s10623-025-01722-9](https://doi.org/10.1007/s10623-025-01722-9)).
The position-moment and deletion-compatibility results extended here are from
Gentle and Wanless,
[*On Perfect Sequence Covering Arrays*](https://arxiv.org/abs/2202.01960)
(Annals of Combinatorics, 2022,
[DOI 10.1007/s00026-022-00610-6](https://doi.org/10.1007/s00026-022-00610-6)).

## The local point-link theorem

Let `V` have nine symbols and let `X` be a hypothetical
`PSCA(9,7,1)`, equivalently an `SCA(5040;7,9)`.  Fix `w in V`.  For
`S subseteq V\{w}`, define

```text
F_w(S) = number of permutations in X whose set of symbols before w is S.
```

Choose six of the other eight symbols and prescribe which `r` of those six
precede `w`.  There are `r!(6-r)!` orders of the seven chosen symbols with
that split around `w`, and perfect coverage uses each order once.  Therefore
every two-dimensional face of `F_w` has the prescribed sum

```text
r! (6-r)!.
```

Put

```text
G_s = s! (8-s)! / 72
    = (560,70,20,10,8,10,20,70,560)_s.
```

Then `G_|S|` has the required face sums.  The difference
`E_w(S)=F_w(S)-G_|S|` has sum zero on every two-face.  Multiplying by
`(-1)^|S|` turns this condition into vanishing second finite differences, so
the result is an affine function on the Boolean cube.  Consequently there
are unique integers `a_w` and `c_wx` for `x != w` such that

```text
F_w(S) = G_|S| + (-1)^(|S|+1) * (sum_{x in S} c_wx - a_w).       (1)
```

Conversely, every integer family in (1) has the required two-face sums.  It is
a valid local point link exactly when its 256 displayed values are
nonnegative.  Pairing cells which differ only in coordinate `x` shows

```text
-18 <= c_wx <= 18.                                               (2)
```

Indeed the tight paired base sums at subset sizes three and four are both 18.

## Position distributions and deletions

Let `d_w(j)` count occurrences of `w` in position `j`, positions numbered
from zero.  Summing (1) over all `j`-subsets gives

```text
d_w = 560*1 + a_w*u + b_w*v,
b_w = sum_{x != w} c_wx - a_w,

u = (1,-7,21,-35,35,-21,7,-1,0),
v = (0,1,-7,21,-35,35,-21,7,-1).                                (3)
```

The vectors `u,v` span the integer nullspace of the moments of degrees zero
through six.  If symbol `x` is deleted, the distribution of `w` on the eight
remaining positions is

```text
630*1 + c_wx*(1,-7,21,-35,35,-21,7,-1).                         (4)
```

Thus the eight deletion parameters in a row satisfy

```text
sum_{x != w} c_wx = a_w + b_w.                                  (5)
```

Equations (1) and (5) are the promised bridge: they retain the joint
compatibility of all eight deletions around `w`, information lost if (4) is
tested separately for each deleted symbol.

## The global flow theorem

View the Boolean lattice of subsets of `V` as a directed graph.  Give the edge

```text
S -> S union {w}
```

multiplicity `F_w(S)`.  A permutation is exactly a path from the empty set to
`V`, adding its symbols in order.

Write

```text
A = sum_w a_w,
C_x = sum_{w != x} c_wx.
```

For every nonempty proper `T subset V`, substitution in (1) gives

```text
inflow(T) - outflow(T) = (-1)^|T| * (sum_{x in T} C_x - A).       (6)
```

The source outflow is `5040+A`.  It follows from (6), first at the source and
then at the singleton subsets, that the edge multiplicities are a flow of
value 5040 if and only if

```text
sum_w a_w = 0,                                                    (7)
sum_{w != x} c_wx = 0 for every x in V.                           (8)
```

Every nonnegative integral flow in this acyclic graph decomposes into unit
source-to-sink paths.  Hence (1), nonnegativity, (7), and (8) are not merely
necessary: they exactly characterise the collections of point links realised
by some multiset of 5040 permutations.  The multiset obtained this way need
not have perfect seven-sequence coverage; that remaining correlation is the
unresolved part of the original problem.

## Exact census

For one point, relabel the other symbols so that
`c_1 <= ... <= c_8`.  For fixed sorted `c`, all 256 inequalities reduce to
eight extremal ones.  At even size `s`, the largest `s`-subset sum must be at
most `a+G_s`; at odd size, the smallest `s`-subset sum must be at least
`a-G_s`.  The fast enumerator visits all
`multiset(37,8)` sorted tuples from (2) and the complete resulting interval of
`a` values.

The independent Python checker instead fixes `a` and `sum(c_i)` and counts
nondecreasing tuples by dynamic programming over prefix sums.  It also
recomputes the larger 1,769-type relaxation directly from (3), (4), the
Gentle--Wanless deletion inequalities, and (5).  The two methods agree on all
counts and on the complete lists in [`RESULTS.tsv`](RESULTS.tsv).

## Reproduction

The recorded run used GCC 12.2 and Python 3.11.  No external package or solver
is required.

```sh
g++ -O3 -std=c++17 enumerate_fast.cpp -o enumerate_fast
./enumerate_fast > regenerated.tsv
diff -u RESULTS.tsv regenerated.tsv
python3 verify.py RESULTS.tsv
```

Both programs use exact integers.  The C++ program directly checks all 256
cells of every accepted profile and all two-face identities on a basis.  The
Python program uses a different state space and recurrence, then independently
recomputes the deletion-only comparison.  The mathematical trust boundary is
the Boolean-cube derivation and elementary integral-flow decomposition above;
there is no solver-infeasibility claim.

## Next milestone

The next layer is the ordered-pair link.  Fixing an ordered pair of symbols
produces an exact ternary excess array of strength five on the seven remaining
symbols.  Its marginal projections are the point-link parameters here.  An
exact classification or a certified obstruction for those compatible pair
links would add the first correlations not captured by the complete
one-point flow relaxation.
