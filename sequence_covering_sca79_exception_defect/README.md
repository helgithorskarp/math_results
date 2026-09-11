# Forced named-coordinate defect in the exact-nine branch of `SCA(5040;7,9)`

## Result

The
[`exact-nine branch reduction`](../sequence_covering_sca79_nine_asymmetry_branch/README.md)
shows that if a hypothetical `SCA(5040;7,9)` has exactly nine
coordinate-asymmetric ordered-pair links, those links form a directed cycle
cover and every point link is uniform.

This contribution quantifies how much named-coordinate structure every one of
the nine exceptional links must contain.

**Theorem.**  Let `E=P_wx` be any exceptional link in the exact-nine branch.
For an ordered composition `(a,b,c)` of seven, let

```text
T_E(a,b,c) = sum E(A,B,C),
```

where the sum is over all labelled partitions with
`(|A|,|B|,|C|)=(a,b,c)`, and put

```text
M(a,b,c) = multinomial(7;a,b,c).
```

Then

```text
T_E(a,b,c) = 560 (mod M(a,b,c)).                                (1)
```

Consequently every exceptional link is nonconstant on each of the 18
composition layers for which `M(a,b,c)` does not divide 560.  Define its
integral distance from coordinate symmetry on one layer by

```text
Delta_E(a,b,c)
  = min_(q in Z) sum_(|A|,|B|,|C|) |E(A,B,C)-q|.
```

Then

```text
sum_(a+b+c=7) Delta_E(a,b,c) >= 504.                            (2)
```

Across the nine exceptional links, at least 162 ordered-composition layers
are named-asymmetric and their total `L^1` defect is at least 4,536.

In particular, on the `(0,2,5)` layer the 21 cells are indexed by the
two-subsets of the seven unmarked symbols and have total `14 mod 21`.
Therefore the automorphism group of an exceptional link is not transitive on
two-subsets; it cannot be a 2-homogeneous permutation group on those seven
symbols.

This is a necessary condition on every remaining exact-nine cycle type.  It
does not construct or exclude those cycle covers, and it does not decide the
existence of the array.

## Proof of the congruence

Fix the exceptional edge `w->x` and positions `i<j`.  The corresponding
ordered composition is

```text
(a,b,c) = (i, j-i-1, 8-j),
```

and there are `M(a,b,c)` labelled cells in every ordered-pair link.

The other seven outgoing links `P_wy`, with `y != x`, are
coordinate-symmetric.  Their cell values may differ from link to link, but
within the chosen composition the contribution of each is an integer multiple
of `M(a,b,c)`.  Every row having `w` in position `i` has a unique symbol in
position `j`; hence

```text
d_i(w) = T_E(a,b,c) + M(a,b,c) * integer.                        (3)
```

The exact-nine reduction gives `d_i(w)=560` at every position.  Reducing (3)
modulo `M(a,b,c)` proves (1).  The incoming count at `x` gives the same
congruence independently.

## The exact defect certificate

For any integer `q`, the triangle inequality gives

```text
sum |E(A,B,C)-q| >= |T_E(a,b,c)-M(a,b,c)q|.
```

By (1), the right side is at least the distance from 560 to the nearest
multiple of `M(a,b,c)`.  The nonzero cases are:

| multinomial `M` | number of ordered compositions | `560 mod M` | defect per layer | contribution |
| ---: | ---: | ---: | ---: | ---: |
| 21 | 6 | 14 | 7 | 42 |
| 42 | 3 | 14 | 14 | 42 |
| 105 | 6 | 35 | 35 | 210 |
| 210 | 3 | 140 | 70 | 210 |
| **total** | **18** |  |  | **504** |

The complete ordered list is recorded in
[`DEFECT_BOUNDS.tsv`](DEFECT_BOUNDS.tsv).  Summing the 18 elementary bounds
proves (2), and multiplying by nine gives 4,536.

For `(0,2,5)`, a 2-homogeneous automorphism group would act transitively on
the 21 two-subsets and force all 21 integral cell values to be equal.  Their
total would then be divisible by 21, contradicting (1).

## Research boundary

Solver experiments were used only to probe stronger candidate lifts.  No
solver verdict enters this result.  In particular, bounded searches that did
not finish were discarded.  The published theorem consists solely of the
named-position conservation law (1) and its exact arithmetic consequences.

The defect bound gives a concrete presolve statistic for the next
three-symbol or common-path model: every exceptional edge must allocate at
least 504 units of variation across 18 specified named layers.  Models that
place asymmetry only in the `(0,2,5)` layer, or in any proper subset of these
18 layers, are now excluded for all eight cycle-cover types.

## Reproduction

From this directory, run

```sh
python3 verify.py | diff -u EXPECTED_OUTPUT.txt -
sha256sum -c SHA256SUMS
```

The checker uses only Python 3 standard-library exact integers.  It
reconstructs all 36 multinomial layers, verifies the 18-row certificate,
groups the four possible moduli, and recomputes the per-link and global defect
bounds from definition.
