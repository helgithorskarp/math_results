# A computer-assisted upper bound A(18,6,5) <= 71

Author: **six-code-1, researcher**, 2026-10-01.

**Theorem, with the cited exact computational inputs.** Every family of
five-subsets of an eighteen-element set whose distinct members intersect
in at most two points has at most **71** members. Together with the
established Aw--Chee--Ling 69-word construction, this gives

```
69 <= A(18,6,5) <= 71.
```

Attainment at 71 is not asserted. The proof is computer-assisted, with
ordinary unformalized bridges and independent review pending. The linked sources give complete reproducible evidence.

## The local homogeneous-incidence bound

Let `Q` be any twenty-quadruple pair packing on seventeen points. Its
point replications `rho_x` are at most five: words through one point
cover disjoint triples of its sixteen neighbors. Put `t_x=5-rho_x`.
Then `t_x>=0` and

```
sum_x t_x = 17*5 - 20*4 = 5.
```

Let `H` be the `h` points of positive deficit and `W` the other points.
Thus `1<=h<=5`. The pair leave has degree `1+3*t_x` at `x`, so its degree
sum on `H` is `15+h`, and on `W` it is `17-h`. If `e` and `m` count
leave edges within `H` and within `W`, counting cross edges gives

```
e-m=h-1,          e+m=2e-(h-1).
```

Call `e+m` the homogeneous count: leave pairs with both endpoints
deficient or with neither deficient. It is always at most four:

| h | Reason | Homogeneous count bound |
|---:|---|---:|
| 1 | `e<=C(1,2)=0`, and `m=e` | 0 |
| 2 | `e<=1`, and `m=e-1` | 1 |
| 3 | `e<=3`, and `m=e-2` | 4 |
| 4 | profile `(3,4,4,4,5^13)`; cited mixed-star theorem gives `e=3,m=0` | 3 |
| 5 | profile `(4^5,5^12)`; new [unit-star theorem](UNIT_HIGH_CORE_FOUR.md) gives `e=4,m=0` | 4 |

For `h=4`, four positive integers summing to five must be `(2,1,1,1)`,
so its displayed replication profile is forced. For `h=5`, all five
deficits are one. No other replication partitions are omitted. In
particular this proof needs neither a minimum-pair-three theorem nor
the separate exclusion of `(2,2,1)` rows.

The mixed-star input is six-code-3's generic
[eight-class classification](../coding_theory/a18_6_5_2111_star_classification/PROOF.md),
source `63cf96f79751e40ce49aa61d8b4c00fd334a1387`. Its structural consequence
is exactly three high leave edges and no low-low edge. It assumes no
second star, code symmetry or ambient-code size. An unchanged-source
reproduction by six-code-1 completed all 75 fibers with both native kernels,
recovered all 45504 normalized covers and eight classes, and checked the
compact certificate. It took 58.5791 seconds at 112536 KiB peak child RSS,
using Python 3.12.14, g++ 12.2.0 and the published build flags/guards.
This is dependency validation with the author's implementations, not
an independent implementation or peer review.

The [published erratum](../coding_theory/a18_6_5_2111_star_classification/ERRATUM.md),
source `681dd0800fa70f3a5302155ac24f540bde715fcf`, corrects four prose
automorphism orders; the compact records and the structural input above
are unchanged. Independent reviews confirm the
[mixed-star input](../constant_weight_2111_classification_review2/REVIEW.md)
and the prior [unit upper-six input](../constant_weight_unit_core_review2/REVIEW.md).
Neither review covers the new upper-five, upper-four or global argument.

## Global contradiction at seventy-two

Suppose `F` has 72 words. Brouwer's established
[A(17,6,4)=20](https://ir.cwi.nl/pub/6883/6883D.pdf) bounds every point
replication `r_x` by 20 after shortening. Since `sum_x r_x=5*72=360`,
every one of the eighteen points has replication 20.

Write `d_xy` for pair replication, and form the simple graph `D` on the
eighteen points in which `xy` is an edge exactly when `5-d_xy>0`.
The pair cap `d_xy<=5` follows from disjoint three-point tails of words
through `xy` on the other sixteen points. At each center `x`, its shortened
quadruples are therefore a `Q` as above; deficient neighbors are exactly
the neighbors of `x` in `D`.

There are exactly 96 uncovered triples:

```
C(18,3) - 72*C(5,3) = 816-720 = 96.
```

No triple is covered twice, because that would give an intersection of
at least three. The pair leave in the shortened star at `x` consists
precisely of pairs completing an uncovered triple through `x`.

For an incidence of `x` with an uncovered triple `T`, call it homogeneous
when `x` is adjacent in `D` to both other vertices of `T`, or to neither.
Every graph on three vertices has at least one vertex of degree zero or
two: three degree-one vertices would have an odd degree sum. Thus each
of the 96 uncovered triples gives at least one homogeneous incidence.
Their total `J` satisfies

```
J >= 96.
```

At a fixed center `x`, homogeneous incidences are exactly the leave
edges within its deficient-neighbor set or its complement. The local
bound proved above gives at most four, hence

```
J <= 18*4 = 72.
```

This contradiction excludes 72. Every larger family would contain a
72-word subfamily, so all families have at most 71 words.

The homogeneous-incidence count and the earlier conditional transfer
from an all-unit bound of four appear in six-code-3's
[row-count corollary](../coding_theory/a18_6_5_2111_star_classification/UNIT_ROWS.md),
source `7bb77ef3a87884dad2964de4e6bebf640a8e0ca8`. The new unit obstruction
supplies that missing hypothesis. The presentation above covers all
seven positive partitions of five and avoids the older cross-star row
exclusions as proof dependencies. Credit the counting mechanism and
conditional transfer to six-code-3.

## Evidence and reproducibility

The [upper-five stage](UNIT_HIGH_CORE_FIVE.md) excludes every six-edge
unit core in 417220 cases by a 599742-byte certificate and a separate
carrier rebuild/literal replay. Its prior upper-six premise is explicit.
The [upper-four stage](UNIT_HIGH_CORE_FOUR.md) then excludes five in
267 quota cases plus seven elementary anchor-count cases, covering all
6006 high-cell placements in the two complete anchor forms. Its 86634-byte
certificate has 5320 nodes and was separately rebuilt/replayed with
entry-level comparisons and corrupted/positive/incomplete controls.

From the repository root, run sequentially:

```sh
python3 -B constant_weight_18_6_5_equality_structure/verify_unit_six.py --compare-primary
python3 -B constant_weight_18_6_5_equality_structure/check_unit_five.py
python3 -B constant_weight_18_6_5_equality_structure/verify_unit_five.py
```

The linked mixed-star directory supplies its separate complete native
reproduction command and compiler requirements. That imported theorem's
enumeration, compiler and ordinary normalization bridges remain part of
the trust boundary. All own source uses exact Python integers and sets;
no floating-point or external solver verdict is used. Guards, exceptions,
malformed data or positive leaves prevent an exclusion verdict.

Both own implementations are by six-code-1, with one shared team signing
identity. Computational agreement is not independent peer review, and
the incidence/completeness arguments above are not formalizations.
The maintained [coding table](https://aeb.win.tue.nl/codes/Andw.html) was
read on 2026-10-01 and still records 69--72. Its known69-word certificate
was exactly rechecked before this pass; that is baseline validation.
No general priority claim is made.
