# Complete P84 exclusion by choosing a heaviest remaining class

**Claim:** there is no partition of `[84]` into four eleven-element and four ten-element integer Sidon sets. Together with the [previous profile theorem](../p84_profiles/README.md), this gives

\[
81\le SR(8)\le84.
\]

Here an integer Sidon set has distinct unordered pair sums **including repeated summands**. The programs use points `0,...,83`; translation by one gives `[84]`. The lower bound comes from the known partition of `[80]`. This result closes the entire balanced P84 problem, including all 1,210 cases left after the preceding passes. It does not decide P83 or the exact value of SR(8). No external review, formalization, or literature-priority claim is made for this new computation.

## Exhaustive reduction

Use the symmetric integer weights `v` in [weights.txt](../p84_profiles/weights.txt). Their total is `W=15,685,948`. Every Sidon ten and eleven in `[84]` has weight at most `M=2,000,000`; the exact maxima are both `1,999,990`. The reproduction regenerates the complete ten and eleven catalogs and checks these maxima.

In a balanced partition the four elevens have total weight at least

\[
T=W-4M=7,685,948.
\]

The [canonical anchor reduction](../p84_global_cases/README.md) covers these four-eleven choices up to reflection. The 30,510 elevens form 15,255 reflection pairs. For each pair choose the smaller membership mask, order the pairs by decreasing weight and then by that mask, and put each representative immediately before its reflection. The least-ranked pair used in a partition determines its case; reflect the partition to contain the canonical member. Only 1,488 anchors satisfy `4v(A)>=T`. In case `j`, fix row `2j` and take the other three row IDs in increasing order above `2j`, with pairwise disjoint sets and total weight at least `T`. The mirror row `2j+1` remains allowed. Thus no balanced partition is omitted. Different four-eleven choices can have the same complement; all occurrences are retained.

There are **62,861,452** such anchored four-eleven packings. The new computation traverses all of them, including cases previously excluded. It does not depend on the earlier partial case exclusions or fractional certificates.

For one packing let `R` be its forty-point complement. Since each of the four elevens has weight at most `M`, `v(R)>=T` as well. Suppose `R` has a partition into four tens, ordered by nonincreasing weight. After choosing `4-k` of these tens, the heaviest remaining ten `B` satisfies

\[
\left\lceil\frac{v(D)}k\right\rceil\le v(B)\le U,
\]

where `D` is the remaining domain and `U` is the preceding chosen weight (initially `M`). Enumerate every ten `B` contained in `D` satisfying this interval and recurse on `D\B`. When `k=1`, check the remaining ten directly by the Sidon definition. This recursion is exhaustive: every partition has at least one ordering by nonincreasing class weight, and each next class in that ordering is at least the current average. Equal weights are allowed; they need not give unique search paths.

Only a truncated global ten catalog is needed. At depth `k>=2`,

\[
v(D)\ge T-(4-k)M.
\]

The smallest possible query threshold occurs at `k=2`, giving

\[
C=\left\lceil\frac{T-2M}{2}\right\rceil=1,842,974.
\]

Consequently every queried ten belongs to the complete catalog of **901,286** tens of weight at least `C`. The code checks the threshold at every query and fails if it falls below the catalog cutoff. The final ten is checked directly and need not belong to the truncated catalog. This is the compatibility constraint absent from the earlier point-weight relaxations: each chosen class must lie in the complement of all classes already chosen.

## Complete outcome and direct terminal checks

| Remaining classes at entry | Search calls | Admissible next-ten occurrences |
| --- | ---: | ---: |
| 4 | 62,861,452 | 4,048,536 |
| 3 | 4,048,536 | 11,698 |
| 2 | 11,698 | 2 |
| 1 | 2 | direct check |

Neither final ten is Sidon. [terminal_checks.json](terminal_checks.json) gives the canonical row IDs of both four-eleven packings, the three explicit ten-classes, the final residual, its weight, and an explicit repeated pair sum. They occur in anchor cases 2 and 23. Independently, both corresponding forty-point complements are fully enumerated by two older ten generators and decided by two ordinary exact-cover searches; these also find no completion. [cases.csv](cases.csv) records all 1,488 cases, including the 64 with no qualifying packing.

## Reproduction and validation

From this directory, with CPython 3.11.2 and GCC 12.2.0:

```sh
python3 reproduce.py --work /tmp/p84-exclusion --jobs 4 --sanitizers
```

The Python driver uses only the standard library. Compilation uses C++20, `-O3 -Wall -Wextra -Wconversion -Wshadow -Werror`. The sanitizer build uses `-O1 -g -fsanitize=address,undefined -fno-omit-frame-pointer`. The parent source files referenced by the driver are part of this repository.

The driver performs these complete comparisons:

- Generate all 35,250,764 tens by the existing difference-based and fixed-endpoint pair-sum enumerators. Check the exact maximum weight; compare the complete sorted binary catalogs byte for byte. Filter both catalogs at `C` and compare the resulting 901,286-set catalogs byte for byte.
- Regenerate all elevens, verify the existing raw-catalog hash, construct the canonical orbit order, and verify its hash.
- Traverse all four-eleven packings twice: fixed-depth loops with union masks, and recursive filtering of compatible candidates. Compare every case count with the earlier complete case ledger.
- Query tens by two different representations: a binary radix tree with subtree intersections and maximum weights; and weight-ordered point-incidence bitsets. Both produce the exact numerical-mask order. Compare the entire streams of nonempty query catalogs byte for byte, together with the per-case call counts and terminal records.
- Test weighted recursion against a definition-level Python exact-cover search on every indicated subset of `[12]`, with block sizes three and four. Every returned witness is checked directly. Repeat these controls under sanitizers and reject malformed catalog inputs.
- Verify four positive controls, from two translations of four classes of the published P80 partition, using both query methods. These are controls only; they do not restrict the P84 search.

The fresh reproduction completed in **369.345 seconds** with four workers. The largest single child process used **1,106,860 KiB** peak RSS; this is not an aggregate concurrent-memory measurement. Each method produced 219,886,336 bytes of nonempty query records across its four shards. The exhaustive small controls cover 2,356 domains per method (4,712 release decisions and 4,712 sanitizer decisions). Four additional high-bit positive controls passed with the sanitizer binary; their separate replay command and scope are recorded in [validation.json](validation.json). The compact run record is that same file. Large full catalogs, query traces, executables, and logs are regenerated in the external work directory and are omitted from Git. Individual shard records and explicit completion markers are written there; an interrupted shard or a positive P84 witness prevents successful validation. Shards are the anchor indices modulo `--jobs`, and their disjoint union is all 1,488 cases.

## Trust boundary

This is an exact computer-assisted theorem, conditional on the imported profile theorem that every P84 partition is balanced. That profile theorem and the canonical anchor reduction received an independent review in [the prior review directory](../../sidon_ramsey_8_p84_global_cases_review1/README.md). The new exclusion has internal cross-validation, not an external review.

The written heaviest-class argument, catalog completeness, exhaustive packing traversal, query implementations, compiler/runtime, and direct Sidon checks remain the computational trust boundary. Both implementations share the mathematical heaviest-class recursion and the canonical orbit convention; matching runs are not proof-assistant formalization. Integer weights, comparisons, and search decisions use exact arithmetic; elapsed times alone use floating point. There is no LP tolerance, solver timeout, or heuristic completeness premise.

Membership masks use 128 unsigned bits, of which only 84 are occupied. Pair sums are at most 166. Point weights are at most one million, so all sums and threshold products fit signed 32-bit integers. Node indices are checked to fit below `2^31`. The observed search counters are far below `2^64`; the complete packing counts and emitted query records provide independent size checks. Every published claim is about the finite domain that was completely checked.
