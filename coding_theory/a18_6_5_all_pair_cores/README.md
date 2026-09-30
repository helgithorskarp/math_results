# All two-coordinate cores of ACL69 have completion maximum 69

Author: **six-code-3, researcher**, 2026-09-30.

Let `C` be the explicitly labeled 69-word Aw--Chee--Ling code in `acl69.txt`,
with coordinates `0,...,17` read from left to right. For each unordered pair
`{p,q}`, let `K(p,q)` contain the words of `C` avoiding both coordinates.

**Computer-assisted theorem.** Every binary length-18, weight-5,
minimum-distance-6 code containing any of the 153 fixed cores `K(p,q)`
has at most 69 words. The seed attains 69 in every case.

**Consequence for arbitrary larger codes.** If `F` is any code with these
parameters and `|F|>=70`, then the omitted seed family `D=C\F` has transversal
number at least three: no two coordinates meet every word of `D`.
Indeed, such a pair would imply `K(p,q) subset F`, contradicting the theorem.
A transversal with zero or one coordinate can be extended to a pair, so these
are excluded as well. Replacement words are arbitrary five-subsets.
The unrestricted bounds remain `69 <= A(18,6,5) <= 72`.

## Complete coverage and dependencies

The partition of all 153 pairs is:

| Pair cohort | Count | Retained words | Source |
|---|---:|---:|---|
| All minimum-size cores | 82 | 34 | [Earlier 82-case source](../a18_6_5_minimum_pair_cores/README.md) |
| Pairs containing coordinate 17 | 17 | 38--43 | [Original 35-core source](../a18_6_5_coordinate_cores/README.md) |
| Remaining pairs, proved here | 54 | 35--37 | This directory |

The two earlier source commits are, respectively,
`ce1b17f1762b639d912ad6893170b4fdafee72dc` and
`7b4ddf424ca0a1edbc8803e9e1b21ea321bfa1bc`. Their statements and independent
checkers supply the first 99 cases. The all-pair theorem also implies every
singleton-core bound, because each singleton core contains a pair core. This directory checks the census and
proves all remaining 54 cases: 35 cores of size 35, 18 of size 36, and one
of size 37. Together these results cover every pair, without a symmetry quotient.

Every coordinate in any `(18,6,5)` code has degree at most 20: deleting that
coordinate from its incident words yields an `(17,6,4)` code. The imported
external theorem `A(17,6,4)=20` is Brouwer's 1975 result cited below.
Every coordinate pair has degree at most five, because its incident words
have mutually disjoint complementary triples on 16 other coordinates.

## Prescribed-total anchor reduction

Fix a remaining pair and its core `K` of size `k`. Enumerate **all** words
outside `K` compatible with it, obtaining `R`. Let `U` be the words of `R`
avoiding both marked coordinates. Branch over the exact subset `Z` of `U`
present in a proposed completion, skipping incompatible subsets; set `h=|Z|`.

Suppose a completion has at least 70 words. Outside `K`, let `a,b,c,h` count
words containing only `p`, only `q`, both, and neither. The degree bounds give

```
a+b+c+h >= 70-k,
a+c <= 20,       b+c <= 20,       c <= 5.
```

Thus both pure counts satisfy `a,b >= m=max(0,50-k-h)`, and
`a+b >= 65-k-h`. Define `T=max(2*m,65-k-h)`. Some thresholds `i,j>=m` with
`i+j=T` satisfy `i<=a,j<=b`: take `i=min(a,T-m)`, then `j=T-i`.
The computation checks every ordered threshold pair, taking the side with the
larger threshold first to reduce work. The corresponding orientation is explicit;
ties use `p` first. No possible pure-count distribution is omitted.

For every compatible family `A` of the first threshold size, enumerate every
compatible family `B` of the opposite threshold size compatible with `A` and
`Z`. The full anchor `H=K union Z union A union B` has size `k+h+T`.
All compatible zero subsets in this cohort have `h<=4`; consequently every
anchor has **exactly 65 words**. This prescribed total is stronger than choosing
only a sufficiently large side and the individual minimum on the other side.

Rebuild the entire extension universe compatible with `H`, removing all zero
words because the exact subset was already fixed. Every such universe has
compatible-family size at most four. Therefore no completion containing the
anchor can reach 70. Every hypothetical completion contains an enumerated
anchor, which proves the exclusion. Empty anchor branches are exhausted too.
All labels remain those of the original code.

## Exact proposer and independent checker

`generate.py` derives the residual universe by owned triples of the seed,
uses integer bitsets, enumerates target cliques by ordered branching and
proper coloring, and bounds extension cliques by conflict-class covers.
If such a cover were insufficient, it would run a complete five-clique search;
all production covers sufficed. The ordered branching partitions target
cliques by their last vertex in the current color order. A remaining prefix
has at most as many compatible words as color classes, which justifies pruning.
Induction gives exhaustive coverage without duplicates.

`verify.py` independently constructs all `binomial(18,5)=8568` five-subsets,
filters them using direct intersections with the core, enumerates maximal
cliques by Bron--Kerbosch pivoting, and takes all target-size subsets of those
cliques with deduplication. Every target clique extends to a maximal clique.
The pivot branches and excluded-vertex sets give exhaustive maximal-clique
coverage; cardinality and conflict-cover pruning omit only branches unable
to reach the target. All extension universes are separately tested for five
compatible words. Threshold pairs are generated independently by testing
all count pairs in `{0,...,20}^2`. It matches every report entry and canonical
family-stream hash with the proposer.

Both programs reuse a computed opposite-family list only for identical
candidate sets and a fixed threshold within one branch. The cache is cleared
at 256 entries. Deduplicating identical extension universes also preserves
coverage. These are exact memoizations; their keys are integers in the proposer
and frozen sets in the checker. They do not identify nonidentical states.

The two algorithms were independently implemented by this researcher;
this is algorithmic validation, not a claim of an independent peer review.
`audit.py` checks both enumeration engines against brute force on every
simple graph of order at most five: 1,100 graphs, two labelings per graph,
15,210 target queries per engine, including empty and oversized targets.

Local search caps are 20,000 nodes per root child, with elapsed-time checks
every 128 visits (3 seconds for the proposer, 10 seconds for the checker).
Exceeding a cap raises `INCOMPLETE`; it never certifies absence. Every production
branch completed. All arithmetic and compatibility checks are exact integers
or finite sets; no numerical solver is used.

## Reproduction and compact evidence

Python standard library only. From this directory, use one process:

```sh
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
python3 generate.py --check expected.json
python3 verify.py
python3 audit.py
```

Both production scripts print one progress record per completed pair.
The verifier's final line is:

```json
{"verified_new_pairs":54,"all_pair_cores":153,"completion_maximum":69,"omitted_seed_transversal_lower_bound":3}
```

The replay covers 217 compatible zero subsets, 590 ordered threshold branches,
305,348 first-side families, 2,901,000 anchors counted with multiplicities,
and 496,319 extension queries deduplicated within each threshold branch.
The largest extension universe has 15 words. Every proposer query had a
cover by at most four conflict classes, and every independent five-clique test found none.

`expected.json` is a replay manifest containing counts and full family-stream
hashes, **not a standalone nonexistence certificate**. It has 175499
bytes and SHA-256 `6dafdbc5c9e82e86f627cd92e2cd1f751ad82f970f1fc57f5b591327e1a4d7f1`. Both programs recompute the full finite
proof; the omitted exploratory trees and anchor dumps are unnecessary.
All public files are compact source, the historical seed and this manifest.

The complete independent replay on CPython 3.11.2 took 677.89 seconds
(about 11.3 minutes), with peak RSS 68,936 KiB (under 68 MiB). Exact proposer
regeneration on CPython 3.12.14 took 87.05 seconds with 40,648 KiB RSS.
The full small-graph audit took 0.50 seconds. Each run used one CPU-intensive
process and numerical thread variables set to one, within the 1-CPU, 2-GiB
scope. No CPU-intensive job remains running.

## Primary literature and trust boundaries

The historical seed is Aw, Chee and Ling (2003), Theorem 1 and Appendix A:
[primary article](https://ymchee66.github.io/home/PDF/6cwc.pdf).
The [maintained plain code](https://aeb.win.tue.nl/codes/cwc/d6/a18.6.5.69)
is copied verbatim; SHA-256
`cf71ac44391d86eeb244cbf75de3fee5cfbedb36081175a830e7571acf370c7d`.
Both programs independently check its binary format, uniqueness, weights,
and pairwise minimum distance six. This reproduces the historical lower bound.

Brouwer (1975), *A(17,6,4)=20 or the nonexistence of the scarce design
SD(4,1;17,21)*, Mathematisch Centrum report ZW62/75:
[CWI primary scan](https://ir.cwi.nl/pub/6883/6883D.pdf) and
[bibliographic record](https://ir.cwi.nl/pub/6883). This universal theorem is
imported and is not independently reproved by the finite computation.

[Brouwer's maintained bounds](https://aeb.win.tue.nl/codes/Andw.html), checked
2026-09-30, retain the unrestricted 69--72 gap. No priority claim is made for
the general methods or historical inputs. The finite classification and its
transversal consequence have the explicitly stated scope above.

The written reduction and enumeration-completeness arguments are unformalized.
The imported degree theorem, previous 99 cases, CPython's exact integer/set
semantics and execution remain trust boundaries. Publishing source is provenance;
the complete checks and mathematical reduction establish the restricted theorem.
