# The published 1667-word `A(32,8,8)` code is 4-exchange-maximal

## Theorem and scope

Let `C` be the explicit 1667-word binary constant-weight `(32,8,8)` code in
[`incumbent_1667.txt`](incumbent_1667.txt).  If at most four words are removed
from `C`, it is impossible to add more words than were removed while retaining
weight eight and minimum Hamming distance eight.  Thus this named incumbent is
**4-exchange-maximal**.

Equivalently, every one-word improvement reached from this incumbent must
destroy at least five incumbent words before refilling.  This is an exact local
theorem about one code.  It does **not** prove `A(32,8,8)=1667` and does not rule
out a distant 1668-word code.

This strengthens the earlier [radius-two
certificate](../a32_8_8_two_exchange/README.md).  The incumbent was reported by
William Echols in [*New lower bounds for constant-weight codes via seeded
bit-swap tabu search*](https://arxiv.org/abs/2608.13906), establishing the
current lower bound `A(32,8,8) >= 1667`.  See [NOTICE.md](NOTICE.md) for source
and licensing provenance.

## Blocker reduction

Identify a word with its eight-point support.  For any weight-eight outsider
`x`, define

```text
B(x) = { i : |x intersect C[i]| >= 5 }.
```

After removing incumbent indices `R`, the word `x` is insertable exactly when
`B(x)` is a subset of `R`.  An improving radius-`r` exchange is therefore a set
of `r+1` pairwise compatible outsiders whose blocker union has size at most
`r`.

[`blocker_analysis.cpp`](blocker_analysis.cpp) exhausts all
`binom(32,8)=10,518,300` weight-eight words.  It finds:

```text
|B(x)|                 0       1       2       3       4
outsider count         0     158     636   1,562   3,695
cumulative count       0     158     794   2,356   6,051
```

Two independent complete universe scans agree entry for entry on both
[`low3_candidates.tsv`](low3_candidates.tsv) and
[`low4_candidates.tsv`](low4_candidates.tsv).  The five-subset-owner scan
reconstructs complete blocker sets; the direct scan compares words by popcount
and stops only after the relevant threshold is exceeded.  The full histogram
and blocker-incidence double count are in the expected analysis files.

## Radius three

For a removed triple `R`, the candidate pool is precisely the outsiders in
`low3_candidates.tsv` whose blocker sets lie in `R`.  Every possible compatible
four-set must use a blocker support of size at least two: otherwise four words
occupy three singleton buckets, forcing two compatible words in one bucket and
contradicting the already exhaustive radius-one result.

The program generates all 64,651 relevant removal triples.  Among them, 19,020
have at least four candidates.  None of the 722,417 candidate four-subsets is
pairwise compatible.  The optimized computation uses compatibility-prefix
pruning and reaches the same conclusion after 48,227 final-word tests.

[`verify_radius_three.py`](verify_radius_three.py) independently reconstructs
the removal triples as unions of blocker supports, checks every low candidate
directly against the incumbent, and tests all 722,417 four-subsets.

## Complete radius-four cover

Suppose five compatible outsiders had blocker union `R` of size four.  The
following exhaustive cases generate `R`:

1. One selected word has four blockers, so its support is `R`.
2. One has three blockers; adjoining the missing blocker from another selected
   word gives `R`.
3. There are at least two distinct two-blocker supports.  Their union either is
   `R`, or has size three and adjoining the missing active blocker gives `R`.
4. There is exactly one distinct two-blocker support and all remaining supports
   are singletons.  The two singleton supports outside that pair complete `R`.
5. If every support is a singleton, five candidates occupy only four buckets;
   the radius-one result again rules out compatibility.

[`enumerate_radius_four.cpp`](enumerate_radius_four.cpp) materializes exactly
this cover, with deduplication by packed named-coordinate four-sets:

```text
removal four-sets after 4- and 3-blocker cases:       2,018,499
after distinct two-blocker-pair cases:                3,883,999
complete removal four-set cover:                      7,359,226
pools having at least five candidate outsiders:       2,091,454
maximum candidate-pool size:                                 24
compatible-prefix five-word tests:                    3,624,774
valid five-word refills:                                      0
```

[`audit_radius_four_sets.py`](audit_radius_four_sets.py) independently rebuilds
the 7,359,226-set cover using Python tuples and packed integers.  It reproduces
every intermediate count.  The final C++ pass gathers every outsider whose
blocker support is a subset of each removed four-set and exhausts all
compatibility possibilities.

## Reproduction

Requirements are GCC with C++20 support, GNU Make, and Python 3.  The recorded
run used GCC 12.2.0 and Python 3.11 on one CPU core.

```bash
make check
```

This regenerates both low-blocker certificates by two complete universe scans,
replays the radius-three and radius-four decisions, and runs the independent
Python audits.  On the recorded machine, the optimized blocker scans each took
about 4--7 seconds, the radius-four C++ cover took 7.4 seconds, and the Python
cover audit took 10.4 seconds with peak RSS 564,284 KiB.  Generated state stays
under ignored `build/`.

For a complete AddressSanitizer/UndefinedBehaviorSanitizer replay:

```bash
make sanitize
```

The sanitizer builds reproduced every release artifact byte for byte.  Words
use 32 bits, blocker indices are below 1667, combinadic ranks are below
10,518,300, packed removal keys use at most 44 bits, and all enumeration counters
use unsigned 64-bit integers.

Expected outputs and hashes are included.  The independent-check boundary is
explicit: Python checks the incumbent, all 6,051 low-blocker records, all
radius-three compatibility tests, and the complete radius-four removal-set
cover.  The final 2,091,454-pool compatibility exhaustion is performed by the
audited and sanitizer-tested C++ enumerator.

## Construction-search consequence

The next admissible local improvement has radius at least five.  Exactly 7,769
additional outsiders have five blockers, giving 13,820 words at threshold five.
That is the appropriate input for targeted radius-five or larger
destroy-and-repair searches; continuing to use one- through four-word swaps on
this incumbent is provably futile.
