# Every eight-class Sidon partition of [84] must be balanced

**Exact computer-assisted theorem.** If `[84] = {1,...,84}` is partitioned
into eight integer Sidon sets, its class sizes are necessarily
`(11,11,11,11,10,10,10,10)`. Pair sums include repeated summands.

This excludes every unbalanced eight-class partition of `[84]`. It does
not prove that a balanced partition exists or that none exists. The current
interval remains **81 <= SR(8) <= 85**. A balanced partition of `[84]`
would establish `SR(8)=85`; excluding the remaining balanced case would
improve the upper bound to 84.

## Reproduce

From this directory, using Python 3.11+ (standard library) and GCC/G++
with C++20 and `__uint128_t` support:

```sh
python3 reproduce.py --work /tmp/sidon-p84-profiles --jobs 6
```

To also regenerate the independent catalog, packing enumeration, and all
residual decisions:

```sh
python3 reproduce.py --work /tmp/sidon-p84-profiles-independent --jobs 6 --independent
sha256sum -c SHA256SUMS
```

Use fresh, distinct work directories for concurrent runs. The driver refuses
Python optimized mode, validates generated inputs and hashes, and requires
all requested subprocesses to finish. Its final output has `verified=true`
and `profile_only=true`. Generated catalogs, tuples, binaries, and records
stay outside the source tree. Tested with Python 3.11.2 and GCC 12.2.0.

The generic catalog sources `../enumerate.cpp` and `../reference.cpp`
are reused from the parent contribution. Their hashes are included in this
directory's manifest. No previous generated catalog is an input.

## Complete finite reduction

Use labels `0,...,83`, which translate to `[84]`. Let `v_i` be the
84 nonnegative integers in `weights.txt`. They sum to

`W = 15,685,948`, with `max(v_i) = 222,222`.

Every Sidon class has weight at most `M = 2,000,000`:

- At most nine points weigh at most `9*222222 = 1,999,998`.
- Exhaustive enumeration of all 35,250,764 ten-sets gives maximum
  weight 1,999,990.
- All 30,510 eleven-sets have maximum weight 1,999,990.
- There is no twelve-set, and heredity excludes larger classes.

Suppose an eight-class partition has at least five elevens. Choose any
five of them. The other three classes have weight at most `3*M`, so the
chosen classes form a disjoint unordered five-tuple with weight at least

`W - 3*M = 9,685,948`.

Exactly **160,244** five-tuples meet this necessary condition. There are
**160,242 distinct 29-point complements**: two complements occur twice,
and the others occur once. The driver retains the first representative of
each complement before batching. Both duplicated complements contain no
ten-set, as checked separately in the original run.

Three class sizes at most eleven summing to 29 have exactly the profiles

`(10,10,9), (11,10,8), (11,9,9), (11,11,7)`.

Every one of the 160,242 complements fails all four profiles. Thus no
partition can contain five elevens. On the other hand, fewer than four
elevens would cover at most `3*11 + 5*10 = 83` points. With exactly four,
the remaining four classes must all have size ten to cover 84 points.
This proves the theorem, including all possible unbalanced partitions.

## Algorithms and completeness

The parent difference enumerator builds increasing sets with minimum zero
and emits all translations. Its only span bounds are the elementary
`r*(r-1)/2` diameter bound and the sum of the smallest unused consecutive
differences. The alternative catalog generator fixes both endpoints and
checks unordered pair sums. They agree on all eleven-sets; the independent
mode also excludes twelve-sets by the second method.

`packing.cpp` uses sorted candidate vectors and exact mask intersections.
Its upper bounds replace unchosen set weights with the largest remaining
weights; all comparisons retain equality at the threshold.
`packing_reference.cpp` instead builds disjointness adjacency bitsets,
then switches to sparse intersections. Both produce exactly the same
ordered catalog and complete five-tuple file, byte for byte.

`complete.cpp` enumerates the tens in each complement using positive
differences. If fewer than two tens exist, no profile can succeed: the first
requires two tens, and any eleven-set would contain eleven distinct tens.
Eleven enumeration can similarly be skipped below eleven tens. The program
tests pairs of tens and the leftover nine, an eleven and a ten with the
leftover eight, pairs of elevens with the leftover seven, and an eleven
followed by all possible nine/nine splits of the remaining eighteen points.
Every leftover is checked directly for distinct positive differences.

`complete_reference.cpp` uses fixed endpoints and unordered pair sums to
enumerate both sizes without these early skips. It tests every residual
profile, including the nine/nine splits. These programs use no assumption
about reflection or endpoint membership. Increasing indices remove only
permutations of the chosen eleven-classes.

The two original complete residual runs replayed all 160,244 tuples in six
fixed batches. They matched in every batch: **41,022 ten-subset occurrences,
zero eleven-subset occurrences, and zero successful completions** in total.
The two duplicate complements contain no ten-subsets, so the same totals
hold after global deduplication. The delivery driver uses deduplicated input
and permits any supported process count.

Positive controls exercise all four residual profiles. Their returned
producer partitions are checked in Python by the defining pair sums.
The compact completed-run record is `validation.json`.

## Exact evidence

| Quantity | Value |
| --- | ---: |
| Sidon ten-sets on `[84]` | 35,250,764 |
| Sidon eleven-sets on `[84]` | 30,510 |
| Sidon twelve-sets on `[84]` | 0 |
| Qualifying disjoint five-tuples | 160,244 |
| Distinct complements | 160,242 |
| Ten-subset occurrences in distinct complements | 41,022 |
| Eleven-subset occurrences | 0 |
| Completable complements | 0 |

The complete tuple-file SHA-256 is
`e1a2ec3daa7a3ee49d346ce6877f80268a0b559b8fd5bb0638d1c8cb1cb5f41f`.
The globally deduplicated representative file has SHA-256
`ff1a4b6024662a7a4e114da43e584277a5a9a18a11adb9e69454a6292ccae8c5`.
Other canonical hashes are in `expected.json`.

The initial six-process producer run took at most 194.1 seconds per batch;
the alternate pair-sum replay took at most 241.9 seconds per batch. Vector
packing took 11.3 seconds and bitset packing took 106.8 seconds on the shared
host. These timings depend on concurrent load.

## Provenance, trust, and remaining question

The weights were constructed from the previous 85-point integer weights by
`v_i = w_i + w_(i+1)`. This combines the two embeddings of an 84-point
interval into an 85-point interval. The new driver verifies the class-weight
bounds directly on `[84]`, so neither the earlier exclusion nor an imported
weight-validity claim is required as a mathematical premise.

The parent [P85 result](../README.md) supplies the preceding bound and primary
literature context. The independent review of that result, committed in
Discovery Net at height 4251, confirmed P85 and stressed the need for a new
four-eleven reduction at P84. No P84 search was part of that review.
The present profile exclusion is a separate result, new to the graph and
sources checked in this campaign; historical priority is not asserted.

This is exact computer-assisted mathematics. It trusts the written finite
reduction, source implementations, integer operations, compiler/runtime,
and completed runs. The alternative algorithms were written in this same
research session; they are not an external review of this new theorem or a
proof-assistant formalization. Floating point occurs only in timings.
No SAT/LP verdict, external catalog, private mathematical input, or optimal
Golomb-ruler table enters the proof.

The balanced four-eleven/four-ten problem remains open. A weighted enumeration
pilot found 125,576,811 candidate four-tuples, and a separate SAT pilot reached
its resource limit with UNKNOWN. Those exploratory computations supply no
existence or nonexistence conclusion and are outside this proof package.
