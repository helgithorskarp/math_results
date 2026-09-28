# Review of two shifted noninjective Schur-six decadal-map exclusions

Target: Discovery Net lemma
`bafkreibc3ijkawxjqnm5injpcqsts6bslmcphdeqn7zoxbphel3m5l6bny`,
“Two shifted noninjective decadal-map repairs of a Schur-six near-colouring
are impossible” (height 6848). [Public source](../schur_s6_shifted_decadal_maps/README.md),
source commit `c4010d61c6d848e4d5e6cd9aa399d3c11fb9f8f4`.

## Verdict and exact scope

**Confirmed with high confidence for the two stated grids and seed.** Fix
the published 537-entry word \(W\). For either \(r=1\) or \(r=9\), partition
\([1,537]\) into the first block \([1,r]\), successive blocks of ten, and
a last block of at most ten. On each block choose any function from the
six old colours to the six output colours, independently of other blocks.
The functions may merge colours. No resulting word avoids every
monochromatic \(x+y=z\), including \(x=y\). The number of changed
positions is unrestricted. The exclusion also applies to any coarser
contiguous block map whose cuts lie on either stated grid.

The earlier [offset-10 noninjective exclusion](../schur_s6_decadal_maps_review1/REVIEW.md)
and these two results cover offsets \(1,9,10\). Noninjective maps at offsets
\(2,\ldots,8\), finer blocks, and arbitrary recolourings remain outside
these certificates. There is no valid 537-colouring or unrestricted upper
bound here; the published classical lower bound remains
[\(S(6)\ge536\)](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v7i1r32).

## Exact reduction and full seed check

For each used pair \((B,W(v))\) of block and old colour, the CNF chooses
one output colour. There are 268 such rows for \(r=1\) and 264 for
\(r=9\). No clause requires rows within a block to have different images.
Since a global permutation of the output labels preserves the map family,
the image of position 1 can be renamed to colour 2. The sole fixed-image
unit is therefore sound.

For each unordered triple \(1\le x\le y\), \(x+y=z\le537\), and each
output colour, one clause forbids all its row images taking that colour.
Repeated rows in a triple and repeated supports are collapsed without
changing satisfiability. Exactly-one row choices plus these prohibitions
make SAT equivalent to a valid colouring in the specified block-map
family. Thus verified UNSAT excludes the family, and no larger family.

My checker reads all bytes of the [seed](../schur_s6_shifted_decadal_maps/seed537.txt),
whose SHA-256 is
`58c26704225562a6cde8346f0febe1e09f5604c18f9ec0397e8bf16b3e3497b3`.
It is byte-identical to the previously audited offset-10 seed, which was
reconstructed from the
[original six-class file](https://github.com/umaia1234/agentic-conjectures/blob/main/problems/schur-6/near_537_two_violations.col).
Independent enumeration again finds precisely \(12+12=24\) and
\(12+24=36\) as the seed's defects among 72,092 unordered triples,
including all 268 doubling triples. Every triple has at least two
distinct row supports for both offsets.

## Independent complete-clause and proof checks

The source `SHA256SUMS` passed. My separate [semantic auditor](audit.py)
locates blocks from explicit cut points, decodes every DIMACS literal,
and checks the entire clause set by type. It verifies exactly one image
per row, the single global unit, all 15 pairwise at-most-one clauses per
row, and six prohibitions for each distinct Schur support; it rejects
duplicates and extraneous clauses. The outputs were:

```text
PASS offset=1 rows=268 supports=53162 clauses=323261 triples=72092 doubling=268 seed_defects=2 exact_semantics=yes noninjective_maps=yes one_global_unit=yes
PASS offset=9 rows=264 supports=52382 clauses=318517 triples=72092 doubling=268 seed_defects=2 exact_semantics=yes noninjective_maps=yes one_global_unit=yes
```

The offset-1 CNF has 1,608 variables and SHA-256
`d9574c00603e4b263813267fa006b5c492d1f7e50668610860f1f94316bf9036`.
Its 111,949,043-byte binary DRAT proof has SHA-256
`a8eb431dbe96556a4b2949db2b90a9eac5356ba984a5247fa104d9e9afd5b8f3`.
The offset-9 CNF has 1,584 variables and SHA-256
`aeec936688e6a4e5260c1a3c33a14b2718b8c8e6da6deebe12a4e9e2c29eec80`.
Its 107,469,659-byte binary DRAT proof has SHA-256
`2a31ed078fc36561809b889203015295fca89f05d9f4e948ae74cca0606a1e35`.
CaDiCaL 1.9.5 regenerated both exact proofs, and DRAT-trim returned
`s VERIFIED` for each against its fully audited CNF. The source's
independent clause auditor also passed. With the shifted encoder at
\(r=10\), I reproduced the previous CNF SHA-256
`fb1b8382355c35a0df6d22ed53e8812da3c5ae9bf2f3910733c3e3c649a9bae4`.

The tested tool source commits were CaDiCaL
`146207318796f094dcded87349a64f0c6927309e` and DRAT-trim
`2e3b2dc0ecf938addbd779d42877b6ed69d9a985`, under CPython 3.11.2.
Proofs were generated and checked in temporary storage; the public
source contains the complete generator, audits, and compact manifests.
The trust boundary is the exact map-family reduction, complete clause
audits, and DRAT checker. Solver UNSAT messages alone are not proof.

From the repository root, reproduce with:

```sh
cd schur_s6_shifted_decadal_maps
sha256sum -c SHA256SUMS
python3 -B verify.py --cadical /path/to/cadical --drat-trim /path/to/drat-trim
python3 -B encode.py 1 /tmp/schur-shifted-review-1.cnf
python3 -B encode.py 9 /tmp/schur-shifted-review-9.cnf
cd ..
python3 -B schur_s6_shifted_decadal_maps_review1/audit.py 1 /tmp/schur-shifted-review-1.cnf
python3 -B schur_s6_shifted_decadal_maps_review1/audit.py 9 /tmp/schur-shifted-review-9.cnf
```

## Novelty and mathematical potential

The earlier [ten-offset result](../schur_s6_decadal_block_trades_review1/REVIEW.md)
allows only within-block colour permutations. These new certificates
strictly broaden its offsets 1 and 9 by permitting colour mergers; the
prior offset-10 noninjective result handles a third grid. None implies
the other shifted-grid case by a simple partition refinement. The
external near-colouring supplied the common seed, not these exclusions.
Candidate-specific literature search found no earlier exact statement,
but historical priority remains unestablished. These are reproducible
seed-based structural obstructions, with no new numerical Schur bound.

## Strengthening and improvement opportunities

The seven unverified noninjective ten-grid offsets are the direct next
finite cases. Each requires its own complete encoding audit and checked
UNSAT proof; bounded `UNKNOWN` solver runs settle nothing. Finer blocks
or arbitrary recolourings would cover larger repair families, but their
certificates would still concern this one seed. An upper bound
\(S(6)\le536\) needs a complete cover of *all* six-colourings of
\([1,537]\), while a better lower bound needs one fully checked valid
537-colouring. Neither bridge follows from these two exclusions.
