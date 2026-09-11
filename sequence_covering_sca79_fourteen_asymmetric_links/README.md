# At least fourteen named-asymmetric pair links in `SCA(5040;7,9)`

## Result

Let `D` be the directed graph on the nine symbols of a hypothetical
`SCA(5040;7,9)`, with an arc for each ordered-pair link that is not invariant
under relabelling its other seven coordinates.

**Theorem.**  The graph `D` has at least fourteen arcs.

More precisely, no vertex of `D` has both indegree one and outdegree one.
Together with the previously proved positive minimum indegree and outdegree,
this forces at least fourteen asymmetric links.

The argument uses all five informative named immediate-successor layers,
not an automorphism restriction or an aggregate composition model.  It
strengthens the earlier
[`twelve-link capacity bound`](../sequence_covering_sca79_twelve_asymmetric_links/README.md)
and excludes every asymmetric-support graph with at most thirteen arcs.  It
does not decide whether the sequence covering array exists.

## Point-link coordinates

Fix a symbol `w`.  Its full point link has the exact integral form

```text
F_w(S) = G_|S| + (-1)^(|S|+1)
                   (sum_(z in S) c_z - a),                    (1)
```

where

```text
G = (560,70,20,10,8,10,20,70,560),
b = sum_z c_z - a.
```

Its position counts are

```text
d_i = 560 + a u_i + b v_i,                                   (2)
u=(1,-7,21,-35,35,-21,7,-1,0),
v=(0,1,-7,21,-35,35,-21,7,-1).
```

All parameters and cell counts are integers, and every `d_i` is
nonnegative.

## All named immediate-successor layers

Suppose `w` has a unique asymmetric out-neighbour `x`, and let `Y` be the
other seven symbols.  For a predecessor size `r` from two through six and
`y in Y`, let `q_y` be the common value of the coordinate-symmetric link
`P_wy` on its `(r,0,7-r)` layer.

For every `(r-1)`-subset `Z` of `Y`, the set `{x} union Z` is the complete
predecessor set of `w`.  Partitioning its rows by the unique immediate
successor gives

```text
sum_(y in Y minus Z) q_y
  = G_r + epsilon * (c_x + sum_(z in Z)c_z - a),               (3)

epsilon = (-1)^(r+1).
```

Compare two sets `Z` that exchange one symbol.  Equation (3) shows that

```text
q_y + epsilon*c_y = h_r                                      (4)
```

is independent of `y`.  Substitute (4) back into (3), use
`sum_(y in Y)c_y=a+b-c_x`, and cancel the named subset sum.  This gives the
exact integer identity

```text
(8-r) h_r = G_r + epsilon*b.                                  (5)
```

For `r=2,3,4,5,6`, respectively, (5) gives

```text
6 divides 20-b,
5 divides 10+b,
4 divides  8-b,
3 divides 10+b,
2 divides 20-b.
```

The simultaneous congruences are equivalent to

```text
b = 20  (mod 60).                                             (6)
```

Thus asymmetric outdegree one forces (6).  Reverse every permutation.  This
interchanges incoming and outgoing links, reverses the position vector, and
sends the position parameters `(a,b)` to `(-b,-a)`.  Therefore asymmetric
indegree one forces

```text
a = 40  (mod 60).                                             (7)
```

## A vertex cannot have both degrees one

If both degrees at `w` were one, write

```text
a = 40+60k,       b = 20+60l,               k,l integers.     (8)
```

Substitution into (2) gives, among the nine nonnegative position counts,

```text
d_2 = 420(3+3k-l),
d_3 = 420(-1-5k+3l),
d_4 = 420(3+5k-5l),
d_5 = 420(1-3k+5l),
d_6 = 420(1+k-3l).                                            (9)
```

Nonnegativity of `d_3,d_6` gives `k<=0`; equality would require the integer
`l` to equal `1/3`, so `k<=-1`.  The nonnegative combination

```text
d_5 + 5 d_2 = 420(16+12k)
```

gives `k>=-1`.  Hence `k=-1`.  Now `d_2>=0` gives `l<=0`, while
`d_5>=0` gives `l>=0`, so `l=0`.  But then

```text
d_4 = 420(3-5) = -840,
```

a contradiction.  No vertex has both directed degrees one.

## Global count

Write `|E(D)|=9+s`.  Let `p` be the number of vertices with outdegree at
least two and `q` the number with indegree at least two.  The total excess is
`s` on each side, so `p<=s` and `q<=s`.  Every vertex belongs to at least one
of these two high-degree sets, hence

```text
9 <= p+q <= 2s.
```

Thus `s>=5` and `|E(D)|>=14`.

Fourteen is sharp for this abstract degree argument.  The checker supplies a
simple loopless fourteen-arc graph with four high-outdegree vertices, five
high-indegree vertices, and no vertex having both degrees one.  A further
improvement must use more SCA information.

## Reproduction

From this directory, run

```sh
python3 verify.py | diff -u EXPECTED_OUTPUT.txt -
sha256sum -c SHA256SUMS
```

The Python 3 standard-library checker uses exact integers.  It reconstructs
the five congruences and their unique residue modulo 60, verifies every
coefficient in (9) symbolically by substitution, replays the inequality
certificate, and audits the sharp fourteen-arc graph fixture.

## Subsequent strengthening

The follow-up
[`constant-row and exact-23 obstruction`](../sequence_covering_sca79_twenty_four_asymmetric_links/README.md)
combines symmetric pair-link boundaries with the global point-flow balances.
It eliminates every support through 23 arcs and raises the unrestricted
lower bound to twenty-four coordinate-asymmetric ordered-pair links.
