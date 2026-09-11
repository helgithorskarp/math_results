# Unrestricted named-coordinate asymmetry in `SCA(5040;7,9)` pair links

## Result

Let `X` be any hypothetical `SCA(5040;7,9)`, equivalently a
`PSCA(9,7,1)`.  For distinct symbols `w,x`, let

```text
P_wx(A,B,C)
```

count rows in which `w` precedes `x`, with the other seven named symbols split
into the sets before `w`, between `w,x`, and after `x`.  Call this link
coordinate-symmetric if its value depends only on `(|A|,|B|,|C|)`.

**Theorem.**  For every symbol `w`, at least one outgoing link `P_wx` and at
least one incoming link `P_xw` are not coordinate-symmetric.  Thus the
directed graph of asymmetric ordered-pair links has minimum indegree and
minimum outdegree at least one, and in particular contains at least nine of
the 72 directed links.  It must also contain a directed cycle.

Unlike the preceding
[`uniform-point-profile obstruction`](../sequence_covering_sca79_pair_link_symmetry_obstruction/README.md),
this theorem makes no assumption about which of the 1,695 admissible
point-position types occurs at any symbol.  It is a named-coordinate branch
reduction for the unrestricted open problem: every search or construction may
discard all cases whose asymmetric-link digraph has fewer than nine arcs or a
zero-indegree or zero-outdegree vertex.

The theorem is necessary, not sufficient, and does not decide whether the
array exists.

## Point-position moment form

Fix a symbol `w`, and write `d_i` for the number of rows having `w` in
position `i`, with positions numbered `0,...,8`.  The seven-sequence coverage
conditions fix the moments of degrees zero through six.  Their integral
solution is

```text
d_i = 560 + a u_i + b v_i,                                      (1)

u = (1,-7,21,-35,35,-21,7,-1,0),
v = (0,1,-7,21,-35,35,-21,7,-1),
```

for integers `a,b`.  This is also obtained directly from the complete point
link in
[`sequence_covering_sca79_point_link_flow`](../sequence_covering_sca79_point_link_flow/README.md).
Only (1), integrality, and `d_i >= 0` will be used below.

## Named-coordinate divisibility

Suppose, for a contradiction, that all eight outgoing links from `w` are
coordinate-symmetric.  Fix positions `i<j`.  A row with `w` in position `i`
and `x` in position `j` lies in a cell with region sizes

```text
(i, j-i-1, 8-j).
```

There are

```text
M_ij = multinomial(7; i, j-i-1, 8-j)                            (2)
```

named partitions of those sizes.  Coordinate symmetry makes all these cells
equal to one integer, so the number of such rows is divisible by `M_ij`.
Summing over the unique symbol `x` in position `j` shows that

```text
M_ij divides d_i.                                                (3)
```

For `i=0`, the least common multiple of (2) over `j=1,...,8` is
105.  For `i=1`, the corresponding least common multiple is 420.  Hence

```text
d_0 = 560+a             is divisible by 105,
d_1 = 560-7a+b          is divisible by 420.                    (4)
```

All integer solutions of (4) have the form

```text
a = -35 + 105k,
b =  35 + 315k + 420l                                   (k,l integers).
```

Substitution in the next three entries of (1) gives

```text
d_1 =  420(2-k+l),
d_2 = -420(1+7l),
d_3 =  420(6+7k+21l).                                          (5)
```

Nonnegativity of `d_2` gives `l <= -1`.  Nonnegativity of `d_3`
gives `k+3l >= 0`, while nonnegativity of `d_1` gives `k <= l+2`.
The last two inequalities imply

```text
-3l <= k <= l+2,
```

and therefore `-4l <= 2`.  This is impossible when the integer `l <= -1`.
Thus every symbol has an outgoing asymmetric pair link.

Reverse every permutation in `X`.  This preserves perfect seven-sequence
coverage and coordinate symmetry, while converting the incoming links at `w`
into outgoing links at `w` with the three regions reversed.  Applying the
same argument proves the incoming assertion.  Nine tails each require a
distinct outgoing arc, proving the lower bound of nine asymmetric links.

## What this eliminates

The previous 72-profile composition bundle used coordinate-symmetric links,
so it was already excluded by the special uniform-profile congruence
`21` not dividing `560`.  The argument above is stronger: changing the point
profiles cannot rescue an all-symmetric or sparsely asymmetric pair-link
model.  Named dependence among the seven unmarked symbols must occur around
every symbol on both sides.

This gives an immediate exact presolve rule for a global search.  If `D` is
the directed set of links permitted to carry named-coordinate perturbations,
then a necessary condition is

```text
minimum outdegree(D) >= 1,   minimum indegree(D) >= 1,   |D| >= 9.
```

In particular, every one of the

```text
sum_(r=0)^8 binom(72,r)
```

labelled choices with at most eight asymmetric ordered-pair links is excluded,
as is every larger choice having a source or sink isolated in `D`.
Moreover, a search may symmetry-break on a directed asymmetric cycle of
length between two and nine.

The subsequent
[`exact-nine branch reduction`](../sequence_covering_sca79_nine_asymmetry_branch/README.md)
shows that tightness forces the asymmetric links to form a directed cycle
cover and forces every full point link to be uniform.  Thus only eight support
types up to relabelling remain at the point-link layer.

## Reproduction

From this directory, run

```sh
python3 verify.py | diff -u EXPECTED_OUTPUT.txt -
sha256sum -c SHA256SUMS
```

The standard-library checker reconstructs all positional multinomial least
common multiples, verifies the symbolic congruence certificate, and audits all
1,695 point-position types in the earlier exact census as an independent
finite cross-check.  The proof itself is the integral argument (1)--(5), not
the census.
