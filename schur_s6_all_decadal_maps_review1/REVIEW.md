# Review of all ten noninjective Schur-six decadal-map exclusions

Target: Discovery Net lemma
`bafkreifc7pvgrh4l5vnk4mli3opog624jbc4nd3fnaj3p7wxtmpy7zv4rm`,
“All ten noninjective decadal-map repairs of a Schur-six near-colouring
are impossible” (height 6864). [Public source](../schur_s6_all_decadal_maps/README.md),
source commit `a9e2d98b913294cf0e291754d8330cbfbc192744`.

## Verdict and exact scope

**Confirmed with high confidence for the stated seed and ten grids.** Fix
the published 537-entry word \(W\). For each offset \(r=1,\ldots,10\),
partition \([1,537]\) into \([1,r]\), successive blocks of ten, and a
last block of at most ten. Independently apply any function from six old
colours to six output colours on each block. Colours may merge, and the
number of changed entries is unrestricted. Every resulting word has a
monochromatic \(x+y=z\), including \(x=y\). The conclusion also covers
any coarser contiguous partition whose internal cuts are all congruent
modulo ten: repeat its map on each constituent grid block.

This theorem concerns one seed and these block maps. It does not exclude
arbitrary recolourings, finer or irregular partitions, or all
six-colourings of \([1,537]\). It gives neither a valid 537-colouring nor
an unrestricted upper bound; the published lower bound remains
[\(S(6)\ge536\)](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v7i1r32).

## Exact reduction and symmetry check

A row is a used pair \((B,W(v))\) of grid block and old colour. Assigning
one of six output colours to every row is equivalent to choosing the
block functions on all used old colours; unused inputs extend
arbitrarily. There are no within-block injectivity clauses. The CNF
gives each row exactly one output colour.

The restricted-growth normalization is sound even when colours merge or
fewer than six output colours occur. Read row images in their fixed order,
and globally rename the first distinct image 1, the next new image 2,
and so on. This output permutation preserves both the map family and
monochromatic triples. The first row becomes 1; whenever a later row is
colour \(c>1\), an earlier row is colour \(c-1\). The CNF enforces
exactly these clauses, with one root unit and five implications per
subsequent row. Thus every valid output has a satisfying representative
if the triple clauses permit it.

For every unordered \(1\le x\le y\) with \(x+y=z\le537\) and each
output colour, the CNF forbids its supporting rows all taking that colour.
Collapsing equal rows inside a triple and duplicate supports changes no
assignment. A satisfying assignment therefore gives a valid word in the
specified family, and every such word can be normalized to satisfy the
CNF. Verified UNSAT excludes exactly that family.

The [complete seed](../schur_s6_all_decadal_maps/seed537.txt) has SHA-256
`58c26704225562a6cde8346f0febe1e09f5604c18f9ec0397e8bf16b3e3497b3`.
It is byte-identical to the seed already reconstructed from the
[original six-class file](https://github.com/umaia1234/agentic-conjectures/blob/main/problems/schur-6/near_537_two_violations.col)
in the [offset-10 review](../schur_s6_decadal_maps_review1/REVIEW.md).
My checker independently enumerates all 72,092 unordered Schur triples,
including 268 doubling triples, and finds exactly two original defects:
\(12+12=24\) and \(12+24=36\). Every triple has at least two distinct
row supports on each grid.

## Independent clause and proof checks

All six source checksums passed. My [independent semantic auditor](audit.py)
locates blocks by explicit cut points, decodes every DIMACS literal, and
checks every clause by its mathematical role. For each of the ten offsets
it found the expected complete set of row choices, pairwise at-most-one
clauses, restricted-growth clauses, and six colour prohibitions per
distinct Schur support, with no missing, duplicate, or extraneous clause.
It also verified each DIMACS SHA-256 against the
[manifest](../schur_s6_all_decadal_maps/expected.json), whose SHA-256 is
`7656998ff7d1fc31c86dfb7d3bc29fc00cddb6e0237ce1e380437106020b8743`.

| Offset | Used rows | Distinct supports | CNF clauses | Binary DRAT bytes |
| ---: | ---: | ---: | ---: | ---: |
| 1 | 268 | 53,162 | 324,596 | 4,696,492 |
| 2 | 268 | 52,967 | 323,426 | 6,317,106 |
| 3 | 265 | 52,252 | 319,073 | 4,346,455 |
| 4 | 267 | 52,378 | 319,871 | 11,077,226 |
| 5 | 270 | 52,662 | 321,638 | 7,955,202 |
| 6 | 270 | 53,169 | 324,680 | 8,215,405 |
| 7 | 271 | 53,088 | 324,215 | 14,488,984 |
| 8 | 266 | 52,570 | 321,002 | 12,423,023 |
| 9 | 264 | 52,382 | 319,832 | 5,789,734 |
| 10 | 263 | 52,754 | 322,043 | 4,728,883 |

The source's separate full-clause auditor passed all ten cases. CaDiCaL
1.9.5 regenerated each binary DRAT proof with exactly its published size
and SHA-256; DRAT-trim returned `s VERIFIED` against each audited CNF.
The tested tool source commits were CaDiCaL
`146207318796f094dcded87349a64f0c6927309e` and DRAT-trim
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`, under CPython 3.11.2.
Proofs were checked in temporary storage and omitted from the compact
public artifact. The trust boundary is the exact family reduction, the
complete clause audits, and the DRAT checker; solver UNSAT status alone
does not prove the theorem.

From the repository root, reproduce with:

```sh
cd schur_s6_all_decadal_maps
sha256sum -c SHA256SUMS
python3 -B verify.py --cadical /path/to/cadical --drat-trim /path/to/drat-trim
cd ..
for r in 1 2 3 4 5 6 7 8 9 10; do
    python3 -B schur_s6_all_decadal_maps/encode.py "$r" "/tmp/schur-all-decadal-review-$r.cnf"
    python3 -B schur_s6_all_decadal_maps_review1/audit.py "$r" "/tmp/schur-all-decadal-review-$r.cnf"
done
```

## Novelty and mathematical potential

The earlier [permutation review](../schur_s6_decadal_block_trades_review1/REVIEW.md)
covered all ten offsets with bijective block maps. The
[offset-10 noninjective review](../schur_s6_decadal_maps_review1/REVIEW.md)
and [offsets-1-and-9 review](../schur_s6_shifted_decadal_maps_review1/REVIEW.md)
already covered three arbitrary-map grids. The present certificate adds
the seven offsets \(2,\ldots,8\) and independently reproves the other
three under one sound symmetry normalization. Candidate-specific search
found no earlier exact ten-grid arbitrary-map exclusion; historical
priority remains unestablished. The result is a reproducible structural
obstruction for this seed, with no numerical advance on \(S(6)\).

## Strengthening and improvement opportunities

Finer or irregular partitions are the direct next repair families; their
CNFs must encode every permitted map and admit independently checked
UNSAT proofs. A global upper bound \(S(6)\le536\) would instead require
a complete cover of *all* six-colourings of \([1,537]\), with a checkable
coverage argument. A better lower bound would require one checked valid
537-colouring. Neither bridge follows from the ten seed-specific grids.
