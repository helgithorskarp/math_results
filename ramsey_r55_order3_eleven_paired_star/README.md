# Coupled fixed-star minimum and the frozen moving-subgraph barrier

The saved Core186 coloring is the **unique minimum among all 4,194,304
reassignments of the moving-triangle contacts at fixed vertices 33 and
35**, with their mutual edge and every other edge fixed. It still has
155 monochromatic five-sets. Every changed assignment has at least 157;
every assignment changing both stars has at least 162.

The physical audit also identifies the more consequential stopping
condition: **57 forbidden five-sets lie entirely in vertices 0..32**.
Changing any edges touching fixed vertices alone cannot produce a Ramsey
graph while that induced coloring stays fixed. Future construction moves
must alter the moving subgraph. No improved fixture, target graph, whole
core exclusion, new automorphism restriction or Ramsey bound is obtained.

## Exact input and finite optimization

[input.edges](input.edges) lists all 457 red pairs on vertices 0..42;
the first line is 43 and omitted pairs are blue. SHA-256:

```text
f034595d4f9fcb40cbf70acb6da75f0f7efda21719b1cc4bd052b75e0e927441
```

This is the earlier Core186 fixture, with 74 red and 81 blue K5s, from
[the structured-candidate package](../ramsey_r55_order3_eleven_structured_candidates),
source `c4e697c219deb07c08dd638baf609c323a9928ee`, graph 3301.
It has action `(0 1 2)...(30 31 32)`, fixing 33..42. Moving triangles
0..3 are internally red and 4..10 internally blue; the eighteen
cross-orbit bits among the first four triangles have word
`100110110011011101`. No catalog-completeness premise is needed here.

The [previous fixed-star certificate](../ramsey_r55_order3_eleven_fixed_star),
source `5d9a27de9cdb651d826a20eb55b38f46fee26899`, graph 3317,
tested one fixed star at a time. Vertices 33 and 35 had the smallest
individual change penalties, 160 and 157. This pass chose that pair
before computing its joint objective and performed one exhaustive test.

Bit i of the low eleven bits of mask A colors all three contacts from
33 to triangle i. Bit 11+i does the same for vertex 35. All other pairs
remain fixed, including the red edge `{33,35}`. All 22 bits are free;
there are no added degree, signature or Ramsey-only constraints. The
mask-to-coloring map is injective, so this is exactly 2^22 distinct
labeled colorings.

| Domain | Assignments | Minimum | Complete minimizing masks |
| --- | ---: | ---: | --- |
| All masks | 4,194,304 | 155 | 2,744,789 |
| Any change from the input | 4,194,303 | 157 | See complete tables |
| Both stars change | 4,190,209 | 162 | 2,736,596 |

The original joint mask is `469 + 2048*1340 = 2744789`. Its unique
minimum has 81 blue and 74 red K5s. The unique minimum with both stars
changed has masks 468 and 1336 respectively. There are zero improving
assignments and zero changed neutral assignments. The selected overall
winner equals the input byte-for-byte; no new edge-list claim is made.
[result.json](result.json) includes exact score histograms and all
minimizers for the all-mask and both-changed domains.

## Exact objective and independent checking

[PROTOCOL.md](PROTOCOL.md) proves the reduction. In a physical five-set,
there are at most six variable root contacts and at least four fixed
pairs. Mixed fixed colors make it impossible to contribute. Otherwise
their unique color determines a monomial on the variable-index support
S. Repeated indices collapse, but each physical five-set contributes
weight one. Empty supports include all unconditional sets.

The separate blue and red counts are

```text
sum(B[S] for S with S & A == 0),
sum(R[S] for S with S & A == S).
```

[produce.py](produce.py) scans all 962,598 physical five-sets and applies
two 22-bit subset zeta transforms. Its unsigned 32-bit entries are safe:
each nonnegative intermediate sum is at most the corresponding total
coefficient weight, bounded by 962,598. The array width is checked and
the output byte order is explicitly little-endian.

[verify.py](verify.py) imports no producer, transform, solver or previous
optimizer. It partitions possible K5s by the subset of the two roots
they contain, then recursively enumerates a K5, K4 or K3 in the graph
with both roots removed. It checks fixed contacts and, for the K3 case,
the mutual root color. This independently reconstructs all **854**
nonzero coefficient records, including all two-root interactions.

The physical coefficient weights by number of chosen roots are:

| Chosen roots | Blue weight | Red weight |
| --- | ---: | ---: |
| Zero | 61 | 41 |
| One | 1,252 | 1,301 |
| Two | 0 | 784 |

These are weights of potentially monochromatic five-sets after fixed
color filtering, not counts of defects at the original assignment. The
zero-root weights are 102 unavoidable defects in this paired-star test.
Both-root blue weight is zero because the mutual root edge is red.

The verifier checks every assignment in reflected binary Gray order.
For the single flipped bit, it evaluates each affected monomial directly
before and after the change, updates its color count, and compares the
two counts to the producer's table. Initial, final and periodic full
monomial sums check the incremental state. Gray order is bijective, so
the completed 4,194,304-entry comparison covers the entire domain.
This uses no zeta transform. A separate table scan checks all summaries.
An optional prefix reports `INCOMPLETE_PREFIX_ONLY` and never supplies
a whole-domain verdict.

The checker decodes the selected graph pair by pair, verifies every
physical action pair, internal/core colors and exact permitted change
support. It compares complete literal five-set lists with a separate
clique-recursion algorithm for the input and selected graph. Both are
the same defective coloring. [verification.json](verification.json)
preserves the complete compact census and checks.

## A barrier to all repairs that preserve the moving subgraph

Among the original defects, 27 blue and 30 red five-sets lie wholly in
0..32. Examples are blue `{0,5,8,14,27}` and red `{0,7,9,18,26}`.
Every edge of these sets lies in that induced subgraph. Thus any graph
that keeps this induced coloring retains all 57 defects, even if every
other edge is reassigned arbitrarily and without a C3 constraint.

[scope.py](scope.py) reads only the pinned edge list and the completed
physical report. It directly scans all 237,336 five-sets on vertices
0..32 and compares their complete blue/red lists with the corresponding
subset of the full audit. [scope.json](scope.json) records the counts,
two physical witnesses and the distribution by number of fixed vertices.
This is a hereditary corollary of the same input census, not an exclusion
of all C3 graphs or all graphs with the prescribed twelve-vertex core.

## Reproduction and controls

Use CPython 3.11.2 and its standard library, from the repository root:

```bash
bash ramsey_r55_order3_eleven_paired_star/reproduce.sh /path/to/fresh-paired-star-run
python3 -B ramsey_r55_order3_eleven_paired_star/scope.py --report /path/to/scope.json
cmp /path/to/scope.json ramsey_r55_order3_eleven_paired_star/scope.json
```

The first command regenerates both omitted tables, checks every entry,
runs the small controls and compares all reports with this package. The
`generated` subdirectory must not already exist. Add `--optimized` as
the second script argument to run all Python stages under `-O`.
The scope check also passes `python3 -B -O` with identical output.

The exact small controls cover 9,224 physical assignment scores: all
16 visible colorings and 64 assignments of a five-vertex fixture, all
512 visible colorings and 16 assignments of a six-vertex fixture, and
eight seven-vertex boundary cases. They include both colors of the
mutual edge, six-bit coupled supports, repeated contacts and constant
sets in all three root strata. Six bad count/coefficient/prefix cases
are rejected. A valid partial Gray traversal is explicitly incomplete.

Normal and optimized producers agree byte-for-byte on coefficients,
full tables, graph and result. Both control modes agree. A fresh full
reproduction from the assembled public source, in optimized mode,
checks the complete domain again and matches the normal verifier's report.
Checks use explicit exceptions; they remain enabled under `-O`.

The normal producer took 18.548 seconds, peak child RSS 65,680 KiB.
A 65,536-assignment Gray prefix took 1.613 seconds, peak 67,476 KiB;
the full independent check took 95.133 seconds, peak 67,888 KiB.
These measurements justified retaining Python; no native rewrite was
needed. Runs are deterministic, single-process calculations without
random seeds, solver assumptions or search timeouts. Partial outputs
remain incomplete until the final report. A stopped run can be restarted
in a fresh directory; its partial state is not a proof or solver restart.

## Compact public evidence and trust

[coefficients.json](coefficients.json) is 8,572 bytes, SHA-256
`a6b1c58e1a1fab36f4098dbaa471027f67464222fb05741edb2d04e6e2b4d825`.
It contains `[blue_records,red_records]`, each sorted as `[support,weight]`.
The full tables stay outside Git. Each contains 4,194,304 unsigned
32-bit counts in increasing mask order, 16,777,216 bytes:

```text
dbd4832b37e481ecfcbbd2ec83e4710b2a77073899c785cfcd65649fe605b2a5  blue.bin
c61aaf3db079444b1f849fb883cdf0cd9e7dd24e8ed1024ebbe647a81c6983a0  red.bin
```

`SHA256SUMS` records every compact public file. Logs, raw tables and runtime
state are not published. The explicit input graph is the only mathematical
premise. The old search, catalog completeness and accepted symmetry
restrictions are not trusted for this finite minimum. The unformalized
reduction, physical indexing, Python and parsing semantics, exact arithmetic,
file identities and hardware remain trust boundaries. These are author
checks with algorithmic independence, not independent peer review or
formalization. No priority claim for the elementary counting method is made.

## Shared context and next boundary

The shared graph was refreshed through 3328. The teammate's
[three-block gluing theorem](../ramsey_r55_antipodal_block_gluing) now has
independent acceptance at 3315, source
`4b8e62c1852956000c995646edd563ea37e2f5f9` in
[the external review package](https://github.com/njallskarp/math_source_code_open/tree/main/ramsey_r55_antipodal_lift_interface).
That review covers the theorem, full H92 interface and physical pairwise
obstruction, not a new H92 solution or all software termination paths.

The external M214 column-hull contribution at 3323, source
`11a71917fe7585dbc2372bbd8df8483329392771`, supplies a strict full-LP
separator with 13 violated new inequalities, not a SAT/UNSAT result. It
was read but is not an input to this structured construction test.

At 3327 the teammate published the
[Paley(41) switching-class exclusion](../ramsey_r55_paley41_switch_family),
source `dac1474f64f1df456bfb4653bd97beb71063f23a`. Its compact physical
DRAT certificate excludes every switch of that 41-core and therefore all
two-vertex extensions, with no automorphism constraint. That is a distinct
whole-family result; it has no independent review at this cutoff and its
code or proof was not imported or rerun here. The H92 route is now parked.

The paired-star milestone is complete. The 17-class / 9,153-label C3
frontier is unchanged. Further fixed-star searches on this coloring cannot
reach the target because of the 57 moving-only defects. A better next
candidate is a switching family that changes the moving subgraph, using
the new durable certificate method. Before pursuing the 41-vertex core
obtained by deleting 33 and 35, first determine whether its switching
class is already covered by the Paley result; different labels or degree
sequences alone do not establish different switching classes. No switching
comparison, formula, solve or additional move phase has begun here.
