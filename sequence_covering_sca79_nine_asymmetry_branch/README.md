# Complete point-link reduction of the nine-asymmetry branch of `SCA(5040;7,9)`

## Result

For a hypothetical `SCA(5040;7,9)`, call an ordered-pair link `P_wx`
coordinate-symmetric when its count depends only on the sizes of the three
regions before `w`, between `w,x`, and after `x`.  The preceding
[`unrestricted asymmetry theorem`](../sequence_covering_sca79_unrestricted_pair_asymmetry/README.md)
shows that at least nine of the 72 links must be asymmetric.

This contribution completely determines the point-link layer when that bound
is tight.

**Theorem.**  If exactly nine ordered-pair links are coordinate-asymmetric,
then:

1. the asymmetric links form a directed cycle cover of the nine symbols;
2. every symbol has the uniform position vector `(560,...,560)`; and
3. every full point link is the uniform profile

   ```text
   F_w(S) = |S|! (8-|S|)! / 72.
   ```

Consequently the exact-nine branch has only eight asymmetric-support types up
to symbol relabelling, indexed by the partitions of nine into cycle lengths at
least two:

```text
9; 7+2; 6+3; 5+4; 5+2+2; 4+3+2; 3+3+3; 3+2+2+2.
```

There are 133,496 labelled supports (the derangements of nine symbols).  All
243,544 nonuniform symmetry-reduced point-link profiles are excluded at every
symbol in this branch.  More finely, the exceptional-edge congruences first
reduce the 1,695 position types to `(a,b)=(0,0)`; there are 949
symmetry-reduced full profiles over that position type, and the symmetric
boundary argument reduces those 949 to the single uniform profile.

This is a complete global reduction of the tight branch through the point-link
layer.  It does not eliminate the remaining cycle-cover branches or decide the
existence of the array.

## Why nine links form a cycle cover

The unrestricted theorem gives every symbol at least one outgoing and one
incoming asymmetric link.  If there are nine links total, all nine vertices
therefore have asymmetric indegree and outdegree exactly one.  The support is
the graph of a fixed-point-free permutation, hence a vertex-disjoint union of
directed cycles of lengths at least two.

Write `f(w)` for the unique asymmetric out-neighbour of `w`.

## Exceptional-edge congruence

Let `d_i(w)` be the number of rows with `w` in position `i`.  For positions
`i<j`, put

```text
M_ij = multinomial(7; i, j-i-1, 8-j).
```

Let `N_wx(i,j)` count rows with `w` in position `i` and `x=f(w)` in
position `j`.  The other seven outgoing links from `w` are
coordinate-symmetric, so each of their corresponding counts is divisible by
`M_ij`.  Summing over the symbol in position `j` gives

```text
N_wx(i,j) = d_i(w)  (mod M_ij).                                 (1)
```

The other seven incoming links at `x` are also coordinate-symmetric.  Summing
instead over the symbol in position `i` gives

```text
N_wx(i,j) = d_j(x)  (mod M_ij).                                 (2)
```

Thus every exceptional edge satisfies the named-coordinate compatibility

```text
d_i(w) = d_j(x)  (mod M_ij)       for all i<j.                  (3)
```

Every admissible point-position vector has the exact form

```text
d_i(a,b) = 560 + a u_i + b v_i,
u=(1,-7,21,-35,35,-21,7,-1,0),
v=(0,1,-7,21,-35,35,-21,7,-1).
```

The earlier complete point-link census contains exactly 1,695 admissible
integer pairs `(a,b)`.  The exact checker groups each tail type by the vector

```text
(d_i(a,b) mod M_ij)_(i<j)
```

and each head type by

```text
(d_j(A,B) mod M_ij)_(i<j).
```

Condition (3) holds exactly when these two signatures are identical.  All
1,695 tail signatures and all 1,695 head signatures are distinct.  Their two
sets have only one common member, occurring at

```text
(a,b)=(A,B)=(0,0).                                               (4)
```

This checks all `1,695^2` possible ordered type pairs without a solver or a
pairwise quadratic search.  Since every vertex lies on an exceptional edge,
(4) proves the uniform position-vector assertion.

## From uniform positions to the full uniform point link

The complete point-link parameterisation is

```text
F_w(S) = G_|S| + (-1)^(|S|+1)
                   (sum_(y in S) c_wy - a_w),                  (5)
```

where `b_w=sum_y c_wy-a_w`.  If `P_wx` is coordinate-symmetric, its boundary
with `x` after `w` shows that `F_w(S)` depends only on `|S|` whenever
`x` is not in `S`.  Applying this to singleton sets in (5) shows that the
seven coefficients `c_wy` with `y != w,x` are equal.

In the exact-nine branch, `w` has seven symmetric outgoing links.  Taking any
two distinct such links shows that all eight coefficients `c_wy` are equal.
Equation (4) gives `a_w=b_w=0`, while

```text
sum_y c_wy = a_w+b_w = 0.
```

Eight equal integer coefficients with zero sum all vanish.  Substitution in
(5) proves that `F_w=G` for every symbol.

## Reproduction and trust boundary

From this directory, run

```sh
python3 verify.py | diff -u EXPECTED_OUTPUT.txt -
sha256sum -c SHA256SUMS
```

The checker uses Python 3 standard-library exact integers.  It verifies the
SHA-256 digest of the earlier complete `RESULTS.tsv`, reconstructs the 1,695
types and all residue signatures, checks their unique intersection, recounts
the 949 profiles above `(0,0)` by an exact prefix-sum dynamic program, and
enumerates the eight cycle types and 133,496 labelled supports.  The trust
boundary is the previously published exhaustive point-link census and the
elementary reductions (1)--(5); no solver verdict or floating-point result is
used.
