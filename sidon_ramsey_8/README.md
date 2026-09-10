# Exact upper bounds for the eighth Sidon–Ramsey number

**Current result: [the complete P84 exclusion](p84_exclusion/README.md) gives
81 <= SR(8) <= 84.** It checks every balanced P84 case by two complete
implementations and imports the independently reviewed profile theorem.
The original P85 proof is preserved below.

The [new P83 profile theorem](p83_profiles/README.md) proves that every P83
partition must have profile `11^3 10^5`. A complete global cover leaves
5,157 nonempty anchor cases and 65,073,232 three-eleven packings for the
five-ten completion problem, which remains undecided. The numerical bound
above is unchanged. The P84 exclusion has received an
[independent acceptance](../sidon_ramsey_8_p84_exclusion_review1/README.md).

This directory reproduces the computer-assisted upper bound **SR(8) <= 85**.
The Sidon–Ramsey number SR(r) is the smallest n for which `[n] = {1,...,n}`
cannot be partitioned into r Sidon sets.
Here a Sidon set has distinct unordered pair sums **including repeated
summands**, and addition is in the integers. Together with the published
lower bound, the resulting interval is **81 <= SR(8) <= 85**. This computation
does not determine the exact value.

The subsequent [P84 profile theorem](p84_profiles/README.md) shows that any
eight-class partition of `[84]` must have four eleven-element classes and
four ten-element classes. The balanced case is now excluded by the subsequent complete computation.

A [global case decomposition](p84_global_cases/README.md) now covers every
balanced P84 partition up to reflection. It excludes 64 packing-empty cases
and 213 further complete cases, at that stage leaving 1,211 explicitly indexed cases.
It supplies no additional numerical bound.

The subsequent [weight certificates](p84_weight_certificates/README.md)
excluded one more whole case, then leaving 1,210, and prove that a joint-eleven
point-weight relaxation is feasible in the largest remaining case.

A [seed extension obstruction](p80_extension_barrier/README.md) also rules out
extending either embedding of the published `[80]` partition to `[81]` while
retaining three seed classes. It covers all replacement class sizes and
does not change the numerical bounds.

An [external end-to-end review](https://github.com/njallskarp/math_source_code_open/tree/main/sidon_ramsey_8_independent_review)
accepts the P85 upper bound with stated computational trust limitations,
after replaying this package and implementing a separate full verifier.

The previous upper bound located in the literature audit is 86, in
Espinosa-García and Pellicer, *Update on Sidon–Ramsey numbers*, Discrete
Applied Mathematics 378 (2026), 120–124:
[journal](https://doi.org/10.1016/j.dam.2025.07.002),
[open manuscript](https://arxiv.org/abs/2309.08553).
The manuscript's Table 2 records the lower bound 81 and Theorem 4.1 gives
the upper bound 86. Searches repeated on 2026-09-10 located no intervening
improvement. The upper-bound computation here uses no published enumeration
as an input.

## Reproduce

Requirements: Python 3.11 or later, its standard library, and GCC/G++ with
the `__uint128_t` extension and C++20 support. Tested with Python 3.11.2
and GCC 12.2.0. No SAT, LP, scientific-Python, or external dataset dependency
is needed to verify the result.

From this directory:

```bash
python3 reproduce.py --work /tmp/sidon-sr8-proof --jobs 6
```

To also replay the alternative enumerators, packing implementation, and
every residual decision:

```bash
python3 reproduce.py --work /tmp/sidon-sr8-independent --jobs 6 --independent
```

Use distinct work directories for concurrent runs. Both commands start a
fresh proof computation and require every requested stage to finish. The
final output contains `"verified": true` and `"bound": "SR(8) <= 85"`.
Generated catalogs, tuples, binaries, detailed outputs, and completion
records stay in the explicitly supplied work directory.

## Finite reduction

The programs use `0,...,84`; translating all points by one gives `[85]`.
For integers, distinct unordered pair sums including diagonals are
equivalent to distinct positive differences between distinct elements.
Indeed, a repeated positive difference rearranges to a nontrivial pair-sum
equality, including a three-term progression when the pairs meet.

1. There are **56,110** eleven-element Sidon sets in this interval and
   **no twelve-element Sidon set**. Thus every class has size at most 11.
   Eight classes covering 85 points must include at least five classes of
   size 11: with at most four, their total size is at most
   `4*11 + 4*10 = 84`.
2. Assign the 85 nonnegative integer weights in `weights.txt` to the
   points in order. Their sum is **7,899,969** and their maximum is 111,111.
   Every Sidon set has weight at most **M = 1,000,000**. For sets of size at
   most nine this follows from `9*111111 = 999999`. Exhaustive enumeration
   gives maximum weight **999,996** for size ten and **999,995** for size
   eleven. Larger Sidon sets do not exist.
3. Select any five eleven-element classes from a hypothetical partition.
   The other three classes have total weight at most `3*M`. Therefore the
   selected five are disjoint and have total weight at least
   **4,899,969**. Exhaustive enumeration gives exactly **130,780** unordered
   choices satisfying these conditions.
4. The complement of each choice has 30 points. Its only possible sorted
   class-size profiles are **(10,10,10)**, **(9,10,11)**, and **(8,11,11)**.
   The programs enumerate its ten- and eleven-element Sidon subsets and
   test every possible completion of each profile. Every choice fails.

These steps exclude every eight-class partition. No balance assumption,
reflection assumption, restriction on endpoint membership, or heuristic
restriction is imposed on a possible partition.

## Completeness and program roles

`enumerate.cpp` builds increasing lists with minimum zero, then emits every
translation into the interval. The used-positive-difference bitset is exact.
After appending `x`, a later point `y` is removed precisely when `y-x` is an
old difference or `y-a` is a newly created difference for a selected point
`a`. The new differences among `x` and older points are mutually distinct
because all those points precede `x`.

Two necessary span bounds prune the search. An `r`-point Sidon set has
`r(r-1)/2` distinct positive differences, so its diameter is at least that
number. Also, the remaining consecutive gaps must be different unused
positive differences; their sum is at least the sum of the smallest
available such differences. Neither bound assumes tabulated optimal ruler
lengths. `reference.cpp` instead fixes both endpoints and checks unordered
sums, using only the elementary diameter bound. Their eleven-set catalogs
agree entry for entry, and both exclude twelve-point sets.

`reproduce.py` orders the eleven-sets by decreasing weight, breaking ties
by their integer subset mask. `packing_reference.cpp` enumerates increasing
index tuples with pairwise disjoint masks. It prunes only when the sum of
the largest remaining candidate weights cannot reach the threshold. Its
additional individual-candidate bound replaces each unchosen weight by an
upper bound from the sorted candidate list. `packing_weighted.cpp` supplies
an alternative implementation using adjacency bitsets and sparse
intersections. Their complete tuple files agree byte for byte.

`complete.cpp` uses exact positive-difference enumeration on each residual
set. For three tens it checks two disjoint tens and tests their complement
in the catalog of tens. Color permutation symmetry allows the first ten
to contain the least residual point and the second to contain the least
remaining point. For profiles containing elevens it tests each possible
eleven/ten or eleven/eleven pair and checks the remaining nine or eight
directly. An eleven-set contains eleven distinct ten-subsets, which
justifies skipping the eleven enumeration when fewer than eleven tens
exist. Fewer than three tens also immediately excludes every profile.

`residual_reference.cpp` independently fixes endpoints for each candidate
ten or eleven and checks pair sums, then tests the three size profiles
without the producer's least-point normalization. Positive controls cover
all three profiles; returned producer partitions are checked directly in
Python using unordered sums, including diagonals.

## Compact expected evidence

| Quantity | Exact value |
| --- | ---: |
| Ten-element Sidon subsets of `[85]` | 49,479,804 |
| Eleven-element Sidon subsets of `[85]` | 56,110 |
| Twelve-element Sidon subsets of `[85]` | 0 |
| Qualifying disjoint five-tuples | 130,780 |
| Distinct 30-point residuals | 130,780 |
| Ten-subset occurrences across these residuals | 1,487,970 |
| Eleven-subset occurrences across these residuals | 26 |
| Residuals admitting three Sidon classes | 0 |

“Occurrences” counts a subset again when it belongs to a different
residual. The weight-filtered tuples and all residuals are distinct.

Expected SHA-256 hashes of regenerated text files:

```text
41bc844293638556ad1896f5ad3593a3181c24e1edba7aea8d73c1aeca4051ab  sets85_11.txt
29f50fe15a092b6b1a8270dcbe7c6f4714b6e21cd3d9ea3fe71831af8d96f907  ordered_sets.txt
3ac309d39a65e7853042b50a8d11d4203821ed19ba13a952a107befc369d7122  packings.txt
```

The default producer's residual computations took about 318 seconds with
six processes in the initial run. The graph-free packing computation took
1.61 seconds; the alternative bitset implementation took about 162 seconds
and allocated 394 MB for adjacency. Timings depend on concurrent host load.
The separate pair-sum replay completed all 130,780 residual decisions in
six batches, with a maximum batch time of 664 seconds. Each batch matched
the producer's counts of ten- and eleven-subsets and admitted no completion.
The compact run record is `validation.json`.

## Trust boundary and calibration note

This is exact computer-assisted mathematics, not a proof-assistant
formalization or external peer review. It trusts the stated finite
reductions, source implementations, compiler/runtime, and completed runs.
The alternative computations were written and run in the same research
session; they supply computational cross-checks, not independent authorship.
Arithmetic involving the theorem is integral. `__uint128_t` holds the point
and difference masks; the sum-based programs use two such words. All shifts
are below the word width. Counts and scaled weight sums fit their stated
64-bit types in the supported ranges. Floating-point values appear only in
elapsed-time reporting in the verifier programs.

The weights were discovered using LP cutting planes, with SciPy 1.17.1 and
its HiGHS backend, then rounded downward to integers. Their validity is
checked by complete integer enumeration; the floating-point optimizer is
outside the proof's trust boundary. The source and the 85-entry weight
vector suffice to regenerate the evidence. Exhaustive dumps and local
checkpoints are intentionally outside this repository.

A calibration discrepancy is recorded rather than silently accepted:
the open manuscript reports 195 nine-element Sidon sets in `[50]` containing
both endpoints. Both the difference enumerator and the separate Python
pair-sum enumeration in `check_enumeration.py` give **192**, agreeing on
every set. Reflection has no fixed point on such Sidon sets, so that count
must be even. This note concerns the cited manuscript's numerical example;
it is not an assertion about every version of the paper. The manuscript's
96-set control for eight points in `[38]` and its 102,484-set count for
eleven points in `[86]` reproduce as stated.
