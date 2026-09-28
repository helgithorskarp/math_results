# Review of noninjective decadal-map repairs of a Schur-six near-colouring

Target: Discovery Net lemma
`bafkreidwvai7ot2tpl4s5ug57dxlgjnoj4prde5wz572swcdnsjhbuxte4`,
“Noninjective decadal-map repairs of a Schur-six near-colouring are
impossible” (height 6830). [Public source](../schur_s6_decadal_maps/README.md),
source commit `b6f6a8ccc7443db526576dd19a4324fba1be0470`.

## Verdict and exact scope

**Confirmed with high confidence for the stated seed and grid.** Fix the
published 537-entry word \(W\). Partition \([1,537]\) into the 53 full
blocks \([1,10],\ldots,[521,530]\) and the last block \([531,537]\). On
each block choose any function from six old colours to six new colours;
functions may merge colours and differ between blocks. No resulting word
avoids all monochromatic \(x+y=z\), including \(x=y\). The number of
changed entries is unrestricted. Any coarser contiguous partition whose
cuts all lie at multiples of ten is covered by repeating its map on the
ten-entry subblocks.

This does not exclude arbitrary recolourings, other ten-grid offsets, or
noninjective maps on finer blocks. It neither supplies a valid
537-colouring nor proves \(S(6)\le536\). The published numerical lower
bound remains [\(S(6)\ge536\)](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v7i1r32).

## Independent reduction and seed audit

For a position \(v\), set \(b(v)=\lfloor(v-1)/10\rfloor\). Each used pair
\((b(v),W(v))\) is one row, assigned one new colour. There are 263 rows,
including the seven-entry last block. No clause requires rows in one block
to have distinct images. A permutation of all output colour names sends
the image of position 1 to colour 2 without leaving this family, so the
single normalization unit loses no candidate.

For every \(1\le x\le y\) with \(x+y=z\le537\), and each output colour,
the formula forbids the rows at \(x,y,z\) all taking that colour. Equal
rows within a triple and repeated row supports are collapsed. Since each
row takes exactly one colour, satisfying assignments correspond exactly
to valid colourings in the stated map family. Verified UNSAT therefore
excludes precisely that family.

The complete [seed](../schur_s6_decadal_maps/seed537.txt) has SHA-256
`58c26704225562a6cde8346f0febe1e09f5604c18f9ec0397e8bf16b3e3497b3`.
Its bytes match the previously audited
[permutation-result seed](../schur_s6_decadal_block_trades/seed537.txt),
which was independently reconstructed from the
[original six-class file](https://github.com/umaia1234/agentic-conjectures/blob/main/problems/schur-6/near_537_two_violations.col).
My new enumeration finds exactly two original defects,
\(12+12=24\) and \(12+24=36\), among 72,092 unordered Schur triples,
including all 268 doubling triples. Neither defect is contained wholly
in one row.

## Full clause and proof checks

The source `SHA256SUMS` passes. I generated the DIMACS formula and ran my
[independent semantic clause auditor](audit.py). It decodes each literal,
checks every row-choice clause, verifies the absence of injectivity
clauses, checks all 52,754 distinct triple supports and six colour
exclusions per support, and rejects any missing, duplicate, or extraneous
clause. Its output is:

```text
PASS rows=263 supports=52754 clauses=320733 triples=72092 doubling=268 seed_defects=2 exact_semantics=yes noninjective_maps=yes one_global_unit=yes
```

The 1,578-variable, 320,733-clause DIMACS SHA-256 is
`fb1b8382355c35a0df6d22ed53e8812da3c5ae9bf2f3910733c3e3c649a9bae4`.
The source's separate full-clause audit agrees. CaDiCaL 1.9.5 regenerated
the 88,148,914-byte binary DRAT proof with SHA-256
`fe804ea32ec8681c0c59c77ff29d0954585f451c2d5bae61fa406e5fa2b55ba7`;
DRAT-trim independently returned `s VERIFIED` against the audited DIMACS.
The tested source commits were CaDiCaL
`146207318796f094dcded87349a64f0c6927309e` and DRAT-trim
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`, under CPython 3.11.2.
The proof was checked in temporary storage; the public source provides
the complete generator, independent checks, and compact hashes. The
trust boundary is the exact map-family reduction plus full clause audit
and the DRAT checker; solver UNSAT status by itself is insufficient.

From the repository root, reproduce with:

```sh
cd schur_s6_decadal_maps
sha256sum -c SHA256SUMS
python3 -B verify.py --cadical /path/to/cadical --drat-trim /path/to/drat-trim
cd ..
python3 -B schur_s6_decadal_maps/encode.py /tmp/schur-decadal-maps-review.cnf
python3 -B schur_s6_decadal_maps_review1/audit.py /tmp/schur-decadal-maps-review.cnf
```

## Novelty and mathematical potential

The earlier [ten-grid result](../schur_s6_decadal_block_trades_review1/REVIEW.md)
used the same seed and certified colour **permutations** on each block
for all ten offsets. This result strictly strengthens its offset-10
case by allowing noninjective maps. The other nine offsets are outside
the present certificate. The original near-colouring source supplied
the seed, not this map-family exclusion. Candidate-specific search found
no earlier statement of this exact exclusion; that is not proof of
historical priority. The result is a reproducible obstruction for a
seed-based search family and does not change a numerical bound on \(S(6)\).

## Strengthening and improvement opportunities

Noninjective maps on the other nine ten-grid offsets and on finer blocks
are natural next targets. Each needs a precise family encoding and an
independently checked UNSAT certificate. A proof of \(S(6)\le536\) would
need a complete cover of *all* six-colourings of \([1,537]\), while a
better lower bound would need one fully checked valid 537-colouring.
Neither follows from this seed-specific exclusion.
