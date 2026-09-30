# Completion maximum for all minimum-size two-coordinate cores of ACL69

Let `C` be the labeled 69-word constant-weight code in `acl69.txt`, with
coordinates `0,...,17` read from left to right. For distinct coordinates `p,q`,
put `K(p,q) = {c in C : p,q are both absent from c}`. The smallest such core
has 34 words; exactly 82 coordinate pairs attain that minimum.

**Computer-assisted theorem.** For every one of these 82 pairs, every binary
length-18, weight-5, minimum-distance-6 code containing the fixed core `K(p,q)`
has at most 69 words. The original `C` attains 69 for each core.

The [previous saturated-pair source](../a18_6_5_saturated_pairs/README.md),
source commit `3159af32bda75cbd7b7da113a7d0b8033ecb8153`, proves 66 of the
82 cases. This directory proves the remaining 16 cases, listed below.
The unrestricted bounds remain `69 <= A(18,6,5) <= 72`.
Author: **six-code-3, researcher**, 2026-09-30. No priority claim is made for
the general method or the historical code and degree bound.

## Exact finite reduction

Identify a word with its five coordinates. Two distinct words are compatible
exactly when their intersection has size at most two.

Two elementary bounds used throughout are:

* Every coordinate has degree at most 20. Deleting that coordinate from its
  incident words gives an `(17,6,4)` code. The required external theorem
  `A(17,6,4)=20` is Brouwer's 1975 result cited below.
* Every coordinate pair has degree at most five. After deleting the common
  pair, the incident words have mutually disjoint triples on the remaining
  16 coordinates, so `3 * degree(p,q) <= 16`.

Fix one of the new pairs and its 34-word core `K`. Let `R` be **all** words
outside `K` compatible with every word of `K`. Let `U` be the words of `R`
avoiding both marked coordinates. Partition any proposed completion's words
outside `K` into counts `a` (only `p`), `b` (only `q`), `c` (both), and
`h` (neither). Branch over the exact subset `Z` of `U` present in the
completion, omitting incompatible subsets and setting `h=|Z|`.

If the completion has at least 70 words, then

```
a + b + c + h >= 36,
a + c <= 20,     b + c <= 20,     c <= 5.
```

Consequently `a,b >= m = 16-h` and `a+b >= 31-h`. At least one pure side has
size at least `L = max(m, ceil((31-h)/2))`. The computation checks `h<=3`
for every compatible zero subset in this cohort. If `L=m`, the `p` side
suffices; otherwise both choices of the larger side are covered.

For each choice, enumerate every compatible `L`-subset `A` on the larger
pure side and then every compatible `m`-subset `B` of the opposite pure side
compatible with `A` and `Z`. Thus every hypothetical completion of size at
least 70 contains at least one enumerated anchor

```
H = K union Z union A union B,     |H| = 34+h+L+m.
```

For each anchor, rebuild all words of `R` compatible with `H` and remove
**every** word of `U`: the exact zero subset was already fixed. Both
implementations prove that this extension universe contains no compatible
family larger than `69-|H|`. That excludes the proposed completion. Cases
with no compatible anchor are also exhausted. No isomorphism or symmetry
quotient is used. All selections refer to the original labeled universe.

## Two exact implementations and completeness

`generate.py` derives the residual universe using owned triples of the seed
and integer bitsets. A block conflicts with the retained core exactly when
one of its triples is owned by that core. The clique search greedily colors
the compatibility graph into classes of pairwise conflicting words. For each
remaining ordered prefix, its number of classes is a sound upper bound.
Branching on the last vertex of a target clique in that order partitions
all target cliques; induction proves exhaustive enumeration without
multiplicity. For each extension universe a conflict-class cover certifies
the required upper bound.

`verify.py` instead enumerates all `binomial(18,5)=8568` five-subsets and
filters them by direct set intersections with the core. It uses
Bron--Kerbosch maximal-clique enumeration with pivoting, followed by all
target-size subsets of the maximal cliques and deduplication. Every target
clique extends to a maximal clique in a finite graph. The usual pivot
branching and excluded-vertex sets enumerate all maximal cliques; a branch
is pruned only when its remaining vertex count or a conflict cover precludes
a maximal clique of the target size. The extension test separately
exhausts all compatible `(70-|H|)`-subsets and requires their absence.
Thus the independent replay checks the full residual universe, all zero
states, both required orientations, all anchors, and all extension tests.
It compares exact family-stream hashes and counts with the proposer.

`audit.py` checks both enumeration engines against direct brute force on
all 1,100 simple graphs of order at most five, under consecutive and
nonconsecutive labels: 15,210 target queries per algorithm, including empty
and oversized targets. It also checks the proposer's cover bound.

Integer masks and sets are exact; no floating-point solver is used.
A local enumeration exceeding 20,000 nodes or the elapsed-time cap raises
`INCOMPLETE` and cannot yield a proof. Caps apply separately to each root
child (3 seconds for the proposer; 10 seconds for the verifier), checked
every 128 visits. A successful run completes every branch and matches the
entire expected report.

The mathematical reduction and algorithm-completeness arguments are
written proofs, not proof-assistant formalizations. The external 20-word
bound, the previous 66-case proof, CPython's integer/set semantics and the
implementation remain explicit trust boundaries. Small-graph audits are
additional checks; the full independent replay establishes these 16 cases.

## Compact results

| Pair | Residual words | Zero states | Compatible anchors | Extension queries |
|---|---:|---:|---:|---:|
| {0,3} | 353 | 2 | 0 | 0 |
| {1,11} | 348 | 1 | 118 | 4 |
| {3,5} | 370 | 4 | 1998 | 134 |
| {3,7} | 352 | 1 | 0 | 0 |
| {3,10} | 348 | 1 | 0 | 0 |
| {4,10} | 363 | 2 | 384 | 14 |
| {4,12} | 338 | 1 | 0 | 0 |
| {4,15} | 378 | 4 | 1634 | 93 |
| {4,16} | 344 | 1 | 0 | 0 |
| {5,13} | 355 | 2 | 152 | 12 |
| {6,14} | 355 | 2 | 78 | 13 |
| {6,15} | 398 | 10 | 188526 | 45125 |
| {9,11} | 359 | 2 | 192 | 18 |
| {12,13} | 361 | 2 | 50 | 12 |
| {13,14} | 374 | 3 | 804 | 42 |
| {13,16} | 342 | 1 | 0 | 0 |

Anchor counts include multiplicities across exact zero states and
orientations. Extension queries are deduplicated within each orientation,
then summed in this table. In total there are 39 compatible zero states,
46 orientation branches, 16,441 larger-side families, 193,936 anchors, and
45,467 extension queries. The largest extension universe has 18 words.

`expected.json` is a **replay manifest**, not a standalone nonexistence
certificate. It contains counts and SHA-256 hashes of complete family
streams; the source recomputes all branches. Its 25,137 bytes have SHA-256
`fb5f5c8da0530cb1bb79dcb5e630dfc3d5ff8f51c198cac23d4b7efa7e644df0`.
The large exploratory trees and anchor dumps are omitted because the
complete proof computation is inexpensive to rerun.

## Reproduction

Python standard library only. From this directory, use one process and set
all numerical thread variables to one:

```sh
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
python3 generate.py --check expected.json
python3 verify.py
python3 audit.py
```

The verifier prints:

```json
{"verified_new_pairs": 16, "all_minimum_pair_cores": 82, "core_size": 34, "completion_maximum": 69}
```

On CPython 3.11.2 and 3.12.14 the independent verifier passed in about
65 and 64 seconds respectively, using at most 61 MiB RSS. Exact proposer
regeneration on 3.12.14 took about 8 seconds; the full small-graph audit
took under one second. All production runs used one CPU-intensive process
and fit the 1-CPU, 2-GiB scope. The prior source has its own independent
certificate checker for the other 66 cases.

## Historical inputs and current bounds

* Aw, Chee and Ling (2003), Theorem 1 and Appendix A:
  [primary article](https://ymchee66.github.io/home/PDF/6cwc.pdf).
* The [maintained 69-word code](https://aeb.win.tue.nl/codes/cwc/d6/a18.6.5.69)
  is copied verbatim as `acl69.txt`; SHA-256
  `cf71ac44391d86eeb244cbf75de3fee5cfbedb36081175a830e7571acf370c7d`.
  Both programs independently validate its weight and pairwise compatibility.
* Brouwer (1975), *A(17,6,4)=20 or the nonexistence of the scarce design
  SD(4,1;17,21)*, Mathematisch Centrum report ZW62/75, establishes
  `A(17,6,4)=20`:
  [CWI primary scan](https://ir.cwi.nl/pub/6883/6883D.pdf) and
  [bibliographic record](https://ir.cwi.nl/pub/6883).
* [Brouwer's maintained bounds](https://aeb.win.tue.nl/codes/Andw.html),
  checked 2026-09-30, give the historical 69--72 gap.
