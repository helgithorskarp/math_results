# A global divisibility obstruction for symmetric pair links in `SCA(5040;7,9)`

## Result

Let `X` be an integral multiset of 5040 permutations of nine symbols.  For a
symbol `w`, let its point link record the exact predecessor set of `w`.  Assume
that every point link has the uniform profile

```text
G_0,...,G_8 = 560,70,20,10,8,10,20,70,560.
```

For distinct symbols `w,x`, the ordered-pair link `P_wx(A,B,C)` counts rows in
which `w` precedes `x`, with the other seven symbols partitioned into the sets
before `w`, between `w,x`, and after `x`.

**Theorem.**  It is impossible for all 72 ordered-pair links to be invariant
under relabelling the other seven symbols.  More precisely, for every symbol
`w`, at least one outgoing link `P_wx` is not coordinate-symmetric, and at
least one incoming link `P_xw` is not coordinate-symmetric.  Consequently at
least nine ordered-pair links must break coordinate symmetry.

This applies in particular to the 72-profile bundle constructed in
[`sequence_covering_sca79_pair_link_kernel`](../sequence_covering_sca79_pair_link_kernel/README.md):
its 36 copies of `Q` and six copies of each of the six region relabellings of
`R` are all coordinate-symmetric.  No assignment of those profiles to named
ordered symbol pairs can be realized by a common multiset of permutation
paths.

The statement is a conditional obstruction to the uniform point-profile
branch.  It does not decide the existence of an `SCA(5040;7,9)` with
asymmetric point links.

The subsequent
[`unrestricted asymmetry theorem`](../sequence_covering_sca79_unrestricted_pair_asymmetry/README.md)
removes the uniform-profile hypothesis: the point-position moment form plus
named-coordinate divisibility forces at least one incoming and one outgoing
asymmetric link at every symbol for every hypothetical `SCA(5040;7,9)`.

## Proof

Fix `w` and count rows in which `w` is first and another specified symbol `x`
is fourth.  Such a row contributes to a cell

```text
P_wx(empty, B, C),   |B|=2, |C|=5.
```

There are exactly

```text
multinomial(7;0,2,5) = binom(7,2) = 21
```

labelled partitions with these region sizes.  If `P_wx` is invariant under
permuting the other seven symbol labels, all 21 cells have one common integral
value `q_wx`.  Hence the number of rows with `w` first and `x` fourth is
`21 q_wx`.

If all eight outgoing links from `w` had this symmetry, summing over the
unique symbol in fourth position would give

```text
number of rows with w first = 21 * sum_(x != w) q_wx.
```

The uniform point link instead gives `G_0=560` rows with `w` first.  This is a
contradiction modulo 21, since

```text
560 = 26 * 21 + 14.
```

Thus every symbol has an outgoing asymmetric link.  The same count, now
fixing the symbol in fourth position and summing over the first symbol, gives
an incoming asymmetric link at every symbol.  A directed graph on nine
vertices with positive outdegree at every vertex has at least nine arcs, so at
least nine of the 72 links are asymmetric.

Notice why the earlier global composition check does not see the obstruction.
For composition `(0,2,5)`, the Q/R bundle has aggregate cell value 240, and
`21 * 240 = 5040`, exactly the total number of rows.  The failure appears only
after resolving that total by the named symbol in first position: each of the
nine required subtotals is 560, which is not a multiple of 21.

## General conservation test

The proof uses no local pair-link equation.  If an integral family of
permutations has `m_i(w)` rows with symbol `w` in position `i`, and all links
from `w` are coordinate-symmetric on a region-size triple `(a,b,c)`
corresponding to positions `i<j`, then necessarily

```text
multinomial(n-2; a,b,c) divides m_i(w).
```

Failure of this divisibility forces named-coordinate asymmetry before any
higher link or internal-order calculation is attempted.  For the present
branch, `(n,a,b,c,m_i)=(9,0,2,5,560)` is already decisive.

## Reproduction

From this directory, run

```sh
python3 verify.py | diff -u EXPECTED_OUTPUT.txt -
sha256sum -c SHA256SUMS
```

The checker uses only the Python standard library.  It verifies the uniform
point-position counts, the divisibility certificate, the Q/R aggregate at
composition `(0,2,5)`, and the full list of positional multinomial divisors.
