# The complete P83 profile landscape

**Theorem.** Every partition of `[83]` into eight integer Sidon sets has size profile

\[
(11,11,11,10,10,10,10,10).
\]

After reflection, every such partition belongs to one of **5,157 explicit nonempty anchor cases**, covering **65,073,232** candidate three-eleven packings. The five-ten completion problem in these cases is **undecided**. The numerical interval remains **81 <= SR(8) <= 84**. A P83 partition would establish `SR(8)=84`, using the [completed P84 exclusion](../p84_exclusion/README.md); a complete P83 exclusion would improve the upper bound to 83.

This is a global P83 classification, proved from its own class-size and catalog calculations. It does not assume the P84 profile, retain a prescribed seed class, or restrict a repair neighborhood. All programs use points `0,...,82`; adding one gives `[83]`. Sidon means distinct unordered integer pair sums **including repeated summands**.

## All initial profiles and the weight bound

Two exhaustive generators find no Sidon twelve-set in `[83]`, so every class has size at most eleven. The deficits from eleven sum to `88-83=5`. The seven integer partitions of this deficit give precisely these initial profiles:

| Profile | Outcome |
| --- | --- |
| `11^7 6` | Excluded in the complete five-eleven branch |
| `11^6 10 7` | Excluded in the complete five-eleven branch |
| `11^6 9 8` | Excluded in the complete five-eleven branch |
| `11^5 10^2 8` | Excluded in the complete five-eleven branch |
| `11^5 10 9^2` | Excluded in the complete five-eleven branch |
| `11^4 10^3 9` | Excluded in the complete four-eleven branch |
| `11^3 10^5` | Only remaining candidate profile; existence undecided |

Define `u_i=v_i+v_(i+1)` for `i=0,...,82`, where `v` is the earlier symmetric 84-point weight vector. The resulting explicit integer vector is [weights.txt](weights.txt). The new reproduction verifies its properties directly:

```text
W = sum(u)                         31,134,774
max point weight                      444,444
complete ten catalog              24,751,806 sets, maximum 3,999,980
complete eleven catalog               15,958 sets, maximum 3,999,979
complete twelve catalog                    0 sets
```

Thus `M=4,000,000` bounds the weight of **every** Sidon class: for sizes at most nine, even the crude point bound `9*444444=3999996` suffices; tens and elevens are checked exhaustively. In particular any class has weight at least `W-7M=3,134,774`, whereas seven points weigh at most `3,111,108`. This also directly rules out classes of size at most seven. The computations below cover all seven initial profiles.

## Excluding five or more elevens

Choose any five eleven-classes in a hypothetical partition. Their union must have weight at least

\[
W-3M=19,134,774.
\]

Two complete packing enumerators agree on exactly **2,142** unordered disjoint five-tuples meeting this cutoff. They have **2,142 distinct 28-point complements**. On each complement, the complete possibilities for the last three class sizes are

```text
(11,11,6), (11,10,7), (11,9,8), (10,10,8), (10,9,9).
```

`complete28.cpp` enumerates every ten-set. If none exists, none of these profiles can occur; an eleven-set itself would contain eleven different ten-subsets. Elevens are consequently generated when there are at least eleven tens. The solver checks every disjoint two-ten choice, every eleven/ten or two-eleven choice, and all necessary nine-sets on the complements of a chosen ten or eleven. The final class is tested directly for the Sidon property. These branches are exactly the five profiles displayed above.

Both residual enumerators and all decisions agree byte for byte. Across the entire family there are **66 ten occurrences**, **zero eleven occurrences**, and **two nine occurrences** in the requested smaller-domain queries. No completion exists. Therefore every P83 partition has at most four elevens. The numbers are occurrences in the specified query domains, not global catalog sizes.

## Excluding four elevens and one nine

After the preceding exclusion, a partition with four elevens must have profile `11^4 10^3 9`. Its four-eleven union has weight at least `W-4M=15,134,774`.

Use reflection `x -> 82-x` to pair the eleven-sets. No eleven-set is fixed: a reflection-invariant set of this size would contain distinct mirrored pairs with equal sum 82. Within each pair choose the smaller integer membership mask, order pairs by decreasing weight and then that mask, and put each representative immediately before its reflection. Reflect a partition so that its least-ranked eleven orbit contributes the canonical representative. This gives **2,701 eligible anchor cases**. Enumerating all later-row disjoint triples with the necessary weight cutoff gives **7,805,097** anchored four-eleven packings. Every partition with this profile occurs; reflection duplicates and different tuples with the same complement need not be removed.

Let `D` be a remaining domain containing `t` tens and one nine-class. Order **only the tens** by nonincreasing weight. The next ten `B` satisfies

\[
\left\lceil\frac{u(D)-M}{t}\right\rceil\le u(B)\le U,
\]

where `U` is the preceding ten weight, initially `M`. The subtraction accounts for the possible nine-class, whose weight is at most `M`. Also `u(D)<=tU+M` is necessary. This argument differs from the equal-size P84 recursion; the nine-class is not required to have weight below the last ten.

The first two ten choices can be drawn from the complete global catalog above

\[
C=\left\lceil\frac{W-6M}{2}\right\rceil=3,567,387,
\]

which contains **4,832,138** tens. Indeed, before the second choice `u(D)>=W-5M`, and subtracting the nine-class cap and dividing by two gives this threshold. Before the first choice the required threshold is larger. For the final nineteen points, enumerate all tens directly, retain those in the required weight interval, and check the nine-point complement directly. Every nonincreasing ordering of a valid three-ten family is represented.

The complete counts are:

| Classes remaining, including the nine | Calls | Admissible next-ten occurrences |
| --- | ---: | ---: |
| 4 | 7,805,097 | 7,813,293 |
| 3 | 7,813,293 | 1,077,835 |
| 2 | 1,077,835 | 380 |
| 1 | 380 | direct nine-class check |

All **380 terminal occurrences** have a repeated pair sum, so the four-eleven profile is impossible. [cases_four.csv](cases_four.csv) records every eligible case and its complete counters. [terminal_examples.json](terminal_examples.json) gives four illustrative terminal records; the reproduction checks all 380, whose full data remain outside Git. The example file is not an exhaustive certificate by itself.

## Complete remaining P83 cover

It follows that every remaining partition has three elevens and five tens. Its three-eleven union must weigh at least

\[
W-5M=11,134,774.
\]

Use the same canonical orbit convention. Case `j` fixes row `2j` and chooses two larger row IDs; all three sets must be disjoint and meet this weight cutoff. The heaviest selected eleven is the least-ranked selected orbit, so `3u(A)>=11,134,774` is necessary. There are **5,364** eligible cases. Of these, **207** have no such triple. The other **5,157** cases account for exactly **65,073,232** anchored triples. [cases_three.csv](cases_three.csv) gives every eligible index and count.

For each admissible triple, the exact remaining problem is to partition its fifty-point complement into **five Sidon tens**. A solution gives P83, and every P83 solution is captured after reflection. No additional symmetry assumption is imposed. The full case counts are computed both by direct union-mask compatibility tests and by intersections of precomputed compatibility bitsets, with identical inclusive weight cutoffs and identical results at every case.

This pass establishes the complete profile and case landscape. It does not claim feasibility or infeasibility of those five-ten completion problems. The same heavy-ten cutoff `C` is valid in a future heaviest-class recursion on the five tens: after `5-k` choices, the remaining weight is at least `W-(8-k)M`, and the smallest queried average for `k>=2` is again `(W-6M)/2`. That computation has not been performed here.

## Reproduce

From this directory, with CPython 3.11.2 and GCC 12.2.0:

```sh
python3 reproduce.py --work /tmp/p83-profiles --jobs 4 --sanitizers
```

The driver uses Python's standard library and C++20. Release builds use `-O3 -Wall -Wextra -Wconversion -Wshadow -Werror`; sanitizer builds use `-O1 -g -fsanitize=address,undefined -fno-omit-frame-pointer`. The older catalog generators are imported as source files from the parent directories, not as precomputed mathematical data.

The driver regenerates both eleven and twelve catalogs, both full ten catalogs, both five-packing lists, all 28-point decisions, two complete four-eleven traversals with two ten-query indexes and two final-domain enumerators, and both remaining triple-count tables. It compares complete catalogs, packing lists, all nonempty four-branch query streams, case records, terminal records and 28-point query streams byte for byte. It verifies every terminal nine collision, class sizes, point incidence, Sidon properties of the selected classes, and nonincreasing ten weights directly in Python.

Positive controls explicitly request each of the five 28-point residual profiles, so an alternative valid profile cannot silently substitute for the intended branch. They give ten release and ten sanitizer decisions. Further controls use known Sidon classes to form nineteen-, twenty-nine- and thirty-nine-point domains of profile `10^t 9`, for `t=1,2,3`, in two translations. Every deletion of one point from the designated ten-class is tested, for **120 release and 120 sanitizer decisions**. These fixtures are controls only and place no restriction on the global search.

[validation.json](validation.json) records the exact run, hashes, compiler, resource measurements and all checks. The fresh four-worker run took 644.458 seconds. The largest individual child used 778,872 KiB peak RSS; this is not aggregate concurrent memory. Allow 3 GB of temporary disk for this reproduction. [landscape.json](landscape.json) records the seven initial profiles and current frontier. Large catalogs, traces, binaries, logs and intermediate records are regenerated outside Git. Shards are the anchor index modulo the job count; explicit completion markers and exact case-index checks prevent an interrupted run from being accepted.

## Scope and trust

The preceding [P84 theorem now has an independent acceptance](../../sidon_ramsey_8_p84_exclusion_review1/README.md). This new P83 classification has internal cross-validation and is not yet externally reviewed or formalized. It does not import the P84 class profile. Its numerical class bounds and complete catalog counts are regenerated at P83.

The written profile arithmetic, canonical coverage, mixed ten/nine weight inequality, enumeration completeness, source, compiler/runtime and direct Sidon checks remain trusted. The two implementations share the mathematical reductions and canonical convention; matching them is not proof-assistant formalization. Weights and decisions use exact integers, not numerical tolerances or solver timeouts. Masks use unsigned 128-bit integers with 83 occupied bits. Point weights are at most one million at input, so sums over the ambient domain and relevant threshold products fit signed 32-bit integers; this proof further checks the required nine-class point cap. Packed node indices fit below `2^31`, and the complete recorded counters fit unsigned 64-bit integers.

The new theorem determines the P83 profile and a globally exhaustive finite frontier. The exact value of SR(8), the remaining P83 completions, and historical priority remain unclaimed.
