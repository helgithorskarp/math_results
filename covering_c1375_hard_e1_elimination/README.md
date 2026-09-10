# Global elimination of the hard-`e1` branch for `C(13,7,5)`

## Result

This directory proves an exact global restriction on a hypothetical
77-block `(13,7,5)` covering:

> The hard-`e1` branch of the global point-link dichotomy is impossible,
> including unrestricted and asymmetric completions.  Consequently every
> hypothetical 77-block cover belongs to case `e0`: it contains two
> degree-41 points whose pair multiplicity is 20.

The proof combines two earlier exact artifacts.  The
[global point-link bridge](../covering_c1375_global_point_link_bridge/)
shows that every 77-block cover lies in `e0` or hard-`e1`.  The
[hard-`e1` link classification](../covering_c1375_hard_e1_link_classification/)
shows that the link of a degree-41 point in hard-`e1` is isomorphic to the
archived optimal link
[`cover_41.txt`](../covering_c1375_fixed_link_symmetry/cover_41.txt).
The compact weighted certificate here proves that this link admits no
hard-`e1` completion at all.

This does **not** exclude `e0` and therefore does not determine the remaining
frontier `77 <= C(13,7,5) <= 78`.

## Completion equations

Fix the root point `0`.  The 41 fixed blocks are `{0} union A`, one for each
six-block `A` of the archived link `L`.  The other 36 blocks are seven-subsets
of `{1,...,12}`.  Write `x_B` for their incidence variables; the argument
works for arbitrary nonnegative real `x_B`, not only for binary variables.

The link degrees are `20^6,21^6`.  Put

```text
K = {1,2,4,5,6,12},
```

the six link-degree-20 points.  In hard-`e1`, these are precisely the six
global degree-42 points.  Each therefore occurs in exactly `42-20=22` of the
36 variable blocks.  Thus every hard-`e1` completion satisfies

```text
sum_B x_B = 36,
sum_(B contains p) x_B = 22  for each p in K.
```

There are 546 five-subsets of `{1,...,12}` not covered by a fixed link block.
Call this residual family `R`.  Every `T` in `R` must satisfy

```text
sum_(B contains T) x_B >= 1.
```

## The nine-number weighted certificate

The two permutations in `CERTIFICATE.json` are checked link automorphisms and
generate a group `G` of order 720.  Its action has six orbits on `R`.  Assign
the following nonnegative weights, constant on each orbit.

| orbit representative | size | weight |
| --- | ---: | ---: |
| `1 2 3 4 7` | 60 | 0 |
| `1 2 3 4 8` | 180 | 1 |
| `1 2 3 4 12` | 60 | 0 |
| `1 2 3 7 10` | 180 | 2 |
| `1 3 7 8 10` | 60 | 2 |
| `3 7 8 9 10` | 6 | 3 |

The total residual weight is

```text
180 + 2*180 + 2*60 + 3*6 = 678.
```

For a candidate seven-block `B`, let `w(B)` be the total weight of residual
five-sets contained in `B`, and put `k(B)=|B intersect K|`.  The 792 candidates
form twelve `G`-orbits.  Exact enumeration gives:

| representative | orbit size | `k(B)` | `w(B)` | `w(B)+8k(B)` |
| --- | ---: | ---: | ---: | ---: |
| `1 2 3 4 5 6 7` | 30 | 5 | 6 | 46 |
| `1 2 3 4 5 6 12` | 6 | 6 | 0 | 48 |
| `1 2 3 4 5 7 8` | 60 | 4 | 12 | 44 |
| `1 2 3 4 5 8 9` | 180 | 4 | 16 | 48 |
| `1 2 3 4 5 8 12` | 60 | 5 | 6 | 46 |
| `1 2 3 4 7 8 9` | 60 | 3 | 17 | 41 |
| `1 2 3 4 7 8 10` | 180 | 3 | 24 | 48 |
| `1 2 3 4 8 10 11` | 60 | 3 | 21 | 45 |
| `1 2 3 4 8 10 12` | 60 | 4 | 12 | 44 |
| `1 2 3 7 8 9 10` | 30 | 2 | 23 | 39 |
| `1 2 3 7 8 10 11` | 60 | 2 | 31 | 47 |
| `1 3 7 8 9 10 11` | 6 | 1 | 38 | 46 |

In particular, every candidate obeys

```text
w(B) + 8 k(B) <= 48.                                  (1)
```

Let `W` be the weighted number of residual-target incidences supplied by the
variable blocks.  Weighted coverage gives `W >= 678`.  On the other hand,
multiplying (1) by `x_B`, summing, and using the point and block equations
gives

```text
W + 8 * sum_(p in K) sum_(B contains p) x_B
    <= 48 * sum_B x_B,
W + 8*(6*22) <= 48*36,
W <= 672.
```

This contradicts `W >= 678`, with strict integer gap 6.  Notice that the
certificate uses neither integrality, upper bounds `x_B <= 1`, pair
constraints, nor higher-shadow constraints.

## Exact verification

The primary checker uses tuple sets.  It validates the link, verifies both
generators as link automorphisms, constructs their order-720 group, checks the
six residual and twelve candidate orbits, and replays the arithmetic:

```sh
python3 hard_e1_elimination.py \
  ../covering_c1375_fixed_link_symmetry/cover_41.txt CERTIFICATE.json \
  | diff -u EXPECTED_CHECK.txt -
```

The independent checker does not import the primary checker.  It rebuilds all
sets as integer bit masks, independently generates the group, and tests the
per-block inequality on all 792 candidates:

```sh
python3 independent_bitmask_check.py \
  ../covering_c1375_fixed_link_symmetry/cover_41.txt CERTIFICATE.json \
  | diff -u EXPECTED_INDEPENDENT_CHECK.txt -
```

Both checkers use only the Python 3.11 standard library and finish in under a
second here.  `SHA256SUMS` records the exact inputs and outputs.

## Trust boundary

The local weighted contradiction and every orbit calculation are checked
exactly with Python integers.  No SAT, LP, or floating-point solver is in the
verification boundary.  The global conclusion additionally imports the exact
global dichotomy and hard-`e1` optimal-link classification cited above; those
artifacts state their own literature and computational trust boundaries.
