# At least twenty-seven named-asymmetric pair links in `SCA(5040;7,9)`

## Result

Let `D` be the directed graph on the nine symbols of a hypothetical
`SCA(5040;7,9)`, with an arc for every ordered-pair link that is not invariant
under relabelling its other seven coordinates.

**Theorem.**  The graph `D` has at least twenty-seven arcs.

This eliminates the complete exact-24, exact-25, and exact-26 branches.  The
argument extends the
[`twenty-four-link theorem`](../sequence_covering_sca79_twenty_four_asymmetric_links/README.md)
by exhaustively distributing the next six degree-excess units among the
already classified constant point-link rows.  Global column and point
balances determine the one possible nonconstant row in each case, and exact
checking of all 256 named cells rules out every survivor.

This is an unrestricted structural bound, not a decision of the underlying
existence problem.  No automorphism restriction or solver verdict is used.

## Imported point-link structure

Every point link has unique integral coordinates

```text
F_w(S) = G_|S| + (-1)^(|S|+1)
                   (sum_(x in S)c_wx-a_w),                    (1)

G = (560,70,20,10,8,10,20,70,560),
b_w = sum_(x!=w)c_wx-a_w,
```

with nonnegative cells and `-18<=c_wx<=18`.  Its position vector is

```text
d_w=560*1+a_w*u+b_w*v,                                        (2)
```

where

```text
u=(1,-7,21,-35,35,-21,7,-1,0),
v=(0,1,-7,21,-35,35,-21,7,-1).
```

The nine point links satisfy the global path-flow balances

```text
sum_w a_w=0,
sum_(w!=x)c_wx=0 for every column x.                           (3)
```

Two distinct coordinate-symmetric outgoing or incoming pair-link boundaries
force all eight coefficients in a point-link row to be equal.  Thus a
nonconstant row has asymmetric indegree and outdegree at least seven and
consumes at least twelve combined degree-excess units.

For a constant row `c_wx=c`, define

```text
F_r(a,c)=G_r+(-1)^(r+1)(r*c-a).                               (4)
```

If its asymmetric outdegree is `k`, the named immediate-successor equations
give the necessary divisibilities

```text
(8-r) divides F_r(a,c) for r=k+1,...,6.                       (5)
```

Incoming degree applies (5) to the reversed parameters

```text
(a,c) -> (-(8c-a),-c).                                        (6)
```

The previous theorem exhausts the 249 nonnegative constant rows and proves
that each consumes at least two combined excess units.

## Shape of every branch with 24--26 arcs

Write

```text
|E(D)|=9+s
```

and let `K` be the number of nonconstant coefficient rows.  The established
degree costs give

```text
2s >= 12K+2(9-K).                                             (7)
```

If `K=0`, the column balances force all constant row values to be zero; (5)
then forces every asymmetric outdegree to be at least three, giving at least
27 arcs.  If `K>=2`, (7) gives at least 28 arcs.  Consequently every branch
with 24, 25, or 26 arcs has exactly one nonconstant row `h`.

Write its degrees as

```text
(outdegree(h),indegree(h))=(7+alpha,7+beta),
alpha,beta in {0,1}.                                          (8)
```

The other eight rows are constant.  If a peripheral row has degrees `(o,i)`,
record the exact option

```text
(o-1,i-1,a,c,b).
```

Equations (4)--(6) enumerate all allowed options from the same 249 profiles.
At `m` arcs the peripheral degree excess beyond its minimum value two totals

```text
2(m-23)-alpha-beta.                                           (9)
```

For `m=24,25,26`, this is at most six.  The verifier enumerates every
unordered multiset of eight options having the exact separate incoming and
outgoing totals.  Unordered enumeration is complete because the subsequent
constraints and the central point link depend only on the multiset of
peripheral `(a,c)` values; retaining labels could only repeat a case.

## Global lift and complete exact counts

For peripheral constant values `c_z`, the column balance at `h` and then at
each peripheral column gives

```text
sum_z c_z=0,       c_hz=c_z,       a_h+b_h=0.                  (10)
```

The first balance in (3) gives

```text
a_h=-sum_z a_z.                                                (11)
```

Thus each peripheral multiset determines the entire central point link.  The
complete exact enumeration has the following counts.  The middle columns
successively impose the separate degree totals, (10), nonnegative positions
from (2), and all 256 nonnegative cells from (1).

| arcs | degree/profile multisets | column-balanced | position-feasible | point-link feasible |
| ---: | ---: | ---: | ---: | ---: |
| 24 | 513 | 105 | 27 | **0** |
| 25 | 18,522 | 2,128 | 537 | **0** |
| 26 | 281,306 | 26,136 | 7,163 | **0** |

At 24 arcs all 27 position-feasible cases induce the same central signature

```text
(a_h,b_h)=(-8,8),
(c_hz)=(-6,-6,-6,-3,3,6,6,6),
```

whose four positive coordinates give the cell value `-21` found in the
previous exact-23 obstruction.  At 25 arcs there are 21 distinct central
signatures and at 26 arcs there are 48.  Even the largest minimum cell value
is negative:

```text
arcs 24: -21,
arcs 25:  -9,
arcs 26:  -9.
```

Therefore no branch with at most 26 asymmetric links survives the complete
named point-link constraints, proving the theorem.

## The first surviving point-flow frontier

At exactly 27 arcs the all-constant case is no longer excluded by degree
counting.  Equations (3) force every constant coefficient value to be zero,
and (5)--(6) force every vertex to have asymmetric degree `(3,3)`.  The only
constant profiles compatible with `(3,3)` and `c=0` are

```text
(a,c,b)=(-8,0,8),       (4,0,-4).
```

The global `a`-balance requires exactly three rows of the first type and six
of the second.  These profiles are nonnegative and satisfy the complete
point-flow balances.  They constitute the first surviving point-link
relaxation, not a pair-link or SCA construction.  The next phase must test
whether a 3-in/3-out asymmetric support can carry compatible named pair links.

## Reproduction

From this directory, run

```sh
python3 verify.py | diff -u EXPECTED_OUTPUT.txt -
sha256sum -c SHA256SUMS
```

The checker uses Python 3 standard-library exact integers only.  It rebuilds
the 249 constant profiles, generates the local degree options directly from
(5)--(6), enumerates every integer partition of the available excess,
checks each multiset through all global balances and all 256 central cells,
and verifies the exact-27 constant frontier.  Runtime is approximately ten
seconds on the publication machine; there is no external input, random
choice, floating point, solver, or bulky generated certificate.
