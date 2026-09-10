# Complete P83 exclusion: SR(8) <= 83

**Theorem.** There is no partition of `[83]` into eight integer Sidon sets. Consequently

\[
81\le SR(8)\le83.
\]

The archived [eight-ten partition of `[80]`](../p80_extension_barrier/partition80.txt) is checked directly, supplying the lower bound 81. The new computation excludes every partition with profile `11^3 10^5`. The [complete P83 profile theorem](../p83_profiles/README.md) is imported to pass from that profile to all eight-class partitions. P82 and the exact value of SR(8) remain undecided. This package preserves the earlier [P84 exclusion](../p84_exclusion/README.md), whose [independent review](../../sidon_ramsey_8_p84_exclusion_review1/README.md) accepted it.

This is an exact computer-assisted theorem with internal cross-validation. The P83 profile theorem and this new exclusion are not yet externally reviewed or formalized. No literature-priority claim is made. Points in code are `0,...,82`; adding one gives `[83]`. Sidon means distinct unordered integer pair sums **including repeated summands**.

## The complete domain

There are 15,958 Sidon eleven-sets in `[83]`. The symmetric integer weights `u` from the profile theorem have total

```text
W = 31,134,774
M =  4,000,000, a uniform class cap
```

The full P83 ten catalog has 24,751,806 sets and exact maximum weight 3,999,980. The eleven maximum is 3,999,979. This pass regenerates both full ten catalogs and the eleven catalog. The profile theorem supplies the exclusion of every other class-size profile; its explicit weights are imported as source data and checked at P83.

A hypothetical balanced partition's three-eleven union must have weight at least `W-5M=11,134,774`. Pair eleven-sets by reflection `x -> 82-x`; no eleven-set is fixed, since a fixed set of this size would contain different mirrored pairs with the same sum. Choose the smaller integer membership mask in each orbit. Order orbits by decreasing weight and then that mask, and place the representative immediately before its reflection.

Reflect the partition so that its least-ranked used orbit contains the representative. Case `j` fixes row `2j` and chooses two larger row IDs, requiring pairwise disjointness and the union-weight cutoff. Necessarily the anchor satisfies `3u(A)>=11,134,774`. The complete cover has **5,364 eligible anchors**, including **207 packing-empty** and **5,157 nonempty** cases, with exactly **65,073,232 anchored three-eleven packings**. Possible reflection duplicates do not affect exclusion. Neither a fixed seed nor a repair neighborhood restricts the domain.

Every fifty-point complement in this cover is now checked. The complete packing count in each case matches the prior [case ledger](../p83_profiles/cases_three.csv), so no formerly open P83 case is omitted.

## Heaviest-class compatibility

Let `R` be the fifty-point complement of a selected triple. Its weight is at least `W-3M=19,134,774`. Order its five hypothetical ten-classes by nonincreasing weight. On a remaining domain `D` with `k` tens, the next ten `B` must satisfy

\[
\left\lceil\frac{u(D)}k\right\rceil\le u(B)\le U,
\]

where `U` is the preceding class weight and initially `M`. Also `u(D)<=kU` is necessary. Enumerate every ten in this weight interval contained in `D`, remove it, and recurse. For `k=1`, check the final ten directly. Every partition admits such an ordering, including ties, so the recursion is exhaustive.

After `5-k` ten choices, the remaining weight satisfies

\[
u(D)\ge W-(8-k)M.
\]

Since `W-8M=-865,226`, the smallest necessary average for `k>=2` occurs at `k=2`. Thus every queried ten has weight at least

\[
C=\left\lceil\frac{W-6M}{2}\right\rceil=3,567,387.
\]

The complete catalog above `C` has **4,832,138 tens**. Every query checks that its lower threshold is at least this cutoff. The final ten is tested directly and need not belong to the heavy catalog. Cross-disjointness at every recursive choice supplies full compatibility among all eight classes.

## Complete outcome

| Tens remaining | Calls | Admissible next-ten occurrences |
| --- | ---: | ---: |
| 5 | 65,073,232 | 185,585,643 |
| 4 | 185,585,643 | 66,521,099 |
| 3 | 66,521,099 | 2,261,478 |
| 2 | 2,261,478 | 1,771 |
| 1 | 1,771 | direct Sidon check |

All **1,771 terminal occurrences** fail the Sidon test. They involve **1,644 distinct anchored three-eleven tuples**. The definition-level Python audit verifies every selected class, full point incidence, all class sizes, the exact weight inequalities at every choice, and an explicit pair-sum collision in the final ten.

As a separate check, combine the fourth chosen ten and the final ten at every terminal occurrence. Their **1,754 distinct twenty-point domains** are each checked for an unrestricted two-ten partition by both complete older subset generators and two point-based exact-cover branch orders. They agree on **4,040 ten occurrences** and find no completion. This check uses neither the global heavy cutoff nor the heaviest-class order.

[cases.csv](cases.csv) records all eligible cases. `packings` is also the number of five-ten root calls. `calls4`, `calls3`, `calls2`, `calls1` are the successive admissible ten-choice counts; equivalently each is the number of calls at the indicated remaining-class count. Every final Sidon decision is false. [terminal_examples.json](terminal_examples.json) contains four illustrative terminal certificates. It is not the complete terminal evidence by itself; the driver regenerates and audits all terminal records outside Git.

## Reproduce and check

From this directory, with CPython 3.11.2 and GCC 12.2.0:

```sh
python3 reproduce.py --work /tmp/p83-exclusion --jobs 6 --workers 8 --sanitizers
```

Use the Python standard library and C++20. Release flags are `-O3 -Wall -Wextra -Wconversion -Wshadow -Werror`; sanitizer builds use `-O1 -g -fsanitize=address,undefined -fno-omit-frame-pointer`. The driver regenerates the actual catalog inputs, performs both complete sweeps, compares their records, and runs the independent terminal checks. It fails on a witness, incomplete shard, missing case, differing trace, failed assertion, malformed input, or nonzero worker exit. It imports the P83 profile theorem rather than rerunning that theorem's separate proof; its reproduction command remains available in the linked package.

The methods differ in both packing traversal and subset querying: fixed-depth union-mask loops plus a radix subset tree, versus recursive compatible-candidate filtering plus weight-ordered point-incidence bitsets. They agree on all case counters and the complete byte streams of every nonempty query, including all candidate sets. All **8,044,688,696 query-trace bytes per method** match, as do every terminal record and the unrestricted twenty-point catalogs and decisions.

Definition-level controls test all 2,356 selected small domains per query method, giving **4,712 release and 4,712 sanitizer decisions**, including negative cases and direct checks of all positive witnesses. Four positive fifty-point decisions per build test actual five-ten partitions in two translations, including the top ambient bit. Four positive twenty-point decisions per build check the supplemental unrestricted solver. These positive fixtures impose no restriction on the exclusion search.

The executed proof run was staged: the complete sweeps consumed catalog files already validated in the profile pass, while this pass independently regenerated both full ten catalogs and the eleven catalog. Those regenerated files match the sweep inputs entrywise. The C++ traversal source was frozen and its inputs hashed before verification. The two sweeps together took **1544.701 seconds** with six shards per method and eight simultaneous workers. Fresh ten-catalog generation and checking took **389.159 seconds** in parallel with the sweeps. These are separate overlapping phase measurements, not a claim of a second sequential end-to-end replay. The public driver provides the complete ordered reproduction.

Allow 25 GB temporary disk for the recorded six-shard run; large catalogs, traces, executables, logs and intermediate records stay outside Git. [validation.json](validation.json) records the exact counters, hashes, controls, timings and evidence scope. [expected.json](expected.json) fixes the expected mathematical outcome, and [SHA256SUMS](SHA256SUMS) covers the compact package. The deterministic shard rule is `anchor_index mod jobs`; every case is included exactly in its assigned shard.

## Trust and remaining scope

The imported profile theorem, written canonical cover and heaviest-class argument, catalog completeness, subset-query code, compiler/runtime, and direct Sidon definitions remain trusted. The two implementations share the mathematical reduction and orbit convention. All proof arithmetic is integral. No numerical tolerance, solver verdict, timeout or sampled result is used as exclusion evidence. Benchmarks helped select execution parameters and are not proof premises.

Masks use unsigned 128-bit integers with 83 occupied bits. Input point weights are between zero and one million. Relevant sums and threshold products fit signed 32-bit integers. Root packings are bounded by `binom(15958,3)<2^40`; every recursive choice emits a trace entry, and the complete recorded trace lengths bound those counters far below `2^64`. Packed catalog indices are checked below `2^31`. Floating-point elapsed times do not participate in any mathematical decision.

The result closes every P83 case and improves the campaign upper bound from 84 to 83. The existence question at P82, the exact value of SR(8), and historical priority remain open here.
