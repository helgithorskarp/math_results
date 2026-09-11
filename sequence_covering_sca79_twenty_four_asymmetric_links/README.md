# At least twenty-four named-asymmetric pair links in `SCA(5040;7,9)`

## Result

Let `D` be the directed graph on the nine symbols of a hypothetical
`SCA(5040;7,9)`, with an arc `w->x` when the ordered-pair link `P_wx` is not
invariant under relabelling its other seven coordinates.

**Theorem.**  The graph `D` has at least twenty-four arcs.

This eliminates the complete exact-fourteen branch requested as the next
global frontier, together with every support having fifteen through
twenty-three arcs.  The proof combines named pair-link boundaries, the full
point-link flow balances, a 249-profile exact local classification, and a
single final negative point cell.  It makes no automorphism assumption and
uses no solver verdict.

The theorem strengthens the
[`fourteen-link bound`](../sequence_covering_sca79_fourteen_asymmetric_links/README.md).
It is still a necessary condition and does not decide whether the sequence
covering array exists.

## Point-link facts used

For each symbol `w`, the exact point-link theorem writes

```text
F_w(S) = G_|S| + (-1)^(|S|+1)
                   (sum_(x in S)c_wx-a_w),                    (1)

G = (560,70,20,10,8,10,20,70,560),
b_w = sum_(x!=w)c_wx-a_w.
```

All parameters are integral, every cell in (1) is nonnegative, and
`-18<=c_wx<=18`.  The position vector is

```text
d_w = 560*1 + a_w*u + b_w*v,                                  (2)
u=(1,-7,21,-35,35,-21,7,-1,0),
v=(0,1,-7,21,-35,35,-21,7,-1).
```

For all nine point links together, the exact path-flow balances are

```text
sum_w a_w = 0,
sum_(w!=x)c_wx = 0                  for every x.               (3)
```

## Symmetric boundaries force constant rows

If `P_wx` is coordinate-symmetric, its boundary with `x` after `w` makes
`F_w(S)` depend only on `|S|` for all `S` not containing `x`.  In (1), this
forces the seven coefficients `c_wz`, `z!=w,x`, to be equal.  Two distinct
symmetric outgoing links therefore force all eight entries in row `w` to be
equal.  The same statement holds for two symmetric incoming links, either by
the other pair-link boundary or by reversing all rows.

Consequently a nonconstant coefficient row has

```text
outdegree_D(w) >= 7,        indegree_D(w) >= 7.                (4)
```

Relative to the positive minimum degrees, such a vertex consumes at least
twelve units of combined degree excess.

## Immediate-successor divisibilities for a constant row

Now suppose row `w` is constant:

```text
c_wx = c              for every x!=w.
```

Then its point cells depend only on size,

```text
F_r(a,c) = G_r + (-1)^(r+1)(r*c-a),                            (5)
```

and `b=8c-a`.  If `w` has exactly `k` asymmetric outgoing links, place all
`k` exceptional successors before `w` and choose an additional named subset
of the symmetric successors.  Partitioning rows by the immediate successor,
then exchanging one selected symmetric symbol, gives the necessary
divisibilities

```text
(8-r) divides F_r(a,c)       for r=k+1,...,6.                  (6)
```

For indegree `l`, reverse the permutations.  The constant-row parameters
become

```text
(a,c) -> (-(8c-a),-c),                                        (7)
```

so (6) applies with `k=l` to the transformed pair.

There are only 249 nonnegative integral constant-row profiles.  Indeed
`-18<=c<=18`, while the empty and singleton cells allow the safe finite range
`-560<=a<=88`; checking all nine values in (5) leaves 249 pairs.  Applying
(6)--(7) gives the complete low-degree classification:

| `(outdegree,indegree)` | surviving `(a,c,b)` |
| --- | --- |
| `(1,1)` | none |
| `(2,1)` | none |
| `(1,2)` | none |
| `(2,2)` | none |
| `(3,1)` | `(-20,-6,-28)`, `(-20,-3,-4)` |
| `(1,3)` | `(4,3,20)`, `(28,6,20)` |

The verifier reconstructs all 249 profiles and every entry of this table
directly.  This is an exhaustive use of the closed form (5), not a sample or
an optimisation result.

Thus every constant row consumes at least two units of combined degree
excess.  At equality it has degree type `(3,1)` or `(1,3)` and is one of the
four displayed profiles.

## First global count: at least twenty-three arcs

Write

```text
|E(D)|=9+s
```

and let `K` be the number of nonconstant coefficient rows.  The total
combined indegree and outdegree excess is `2s`.  By (4) and the constant-row
classification,

```text
2s >= 12K + 2(9-K) = 18+10K.                                 (8)
```

If `K=0`, every coefficient row is constant, say with value `c_w`.  The
column balances (3) give

```text
sum_(w!=x)c_w=0       for every x,
```

which forces every `c_w=0`.  For `c=0`, the exact classification from (6)
has no profile of outdegree one or two.  Hence every vertex would have
outdegree at least three and `|E(D)|>=27`.

If `K>=1`, (8) gives `s>=14` and `|E(D)|>=23`; if `K>=2`, it already gives
at least 28 arcs.  Therefore the only remaining support below twenty-four
arcs has exactly 23 arcs and exactly one nonconstant row.

## The complete exact-23 branch

Equality in (8) determines the entire degree and local-profile pattern.
There is one nonconstant vertex `h` with degree `(7,7)`.  Of the other eight
vertices, four have degree `(3,1)` and four have degree `(1,3)`.

Write `gamma_z` for the common coefficient in constant peripheral row `z`.
The column balances (3), first at column `h` and then at each peripheral
column, give

```text
sum_z gamma_z=0,        c_hz=gamma_z,        a_h+b_h=0.         (9)
```

Among the four `(3,1)` rows, let `i` use `gamma=-6`; the other `4-i` use
`gamma=-3`.  Among the four `(1,3)` rows, let `j` use `gamma=6`; the other
`4-j` use `gamma=3`.  The first equation in (9) gives `i=j`.

The peripheral `a`-sum is `-64+24j`.  The first balance in (3) therefore
gives

```text
a_h=64-24j,        b_h=-a_h.                                  (10)
```

Checking the five possibilities `j=0,...,4` in the exact position vector
(2), only `j=3` is nonnegative.  It forces

```text
a_h=-8, b_h=8,
(c_hz)_z = (-6,-6,-6,-3,6,6,6,3)       up to ordering.        (11)
```

Take `S` to be the four coordinates with positive coefficients.  Then
`|S|=4` and their sum is 21.  Equation (1) gives the named point cell

```text
F_h(S) = G_4 - (21-(-8)) = 8-29 = -21,                         (12)
```

contradicting nonnegativity.  Exact 23 is impossible.  Together with the
preceding count, this proves `|E(D)|>=24`.

## Reproduction

From this directory, run

```sh
python3 verify.py | diff -u EXPECTED_OUTPUT.txt -
sha256sum -c SHA256SUMS
```

The checker uses only Python 3 standard-library exact integers.  It verifies
the local classification entry by entry, the excess calculation, all global
balance cases in the exact-23 branch, and the final negative named cell.  No
solver, floating point, external catalogue, or large generated artifact is
used.
