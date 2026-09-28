# Certified noninjective decadal-map obstruction for classical Schur 6

## Exact claim

Let `W` be the 537-digit word in [`seed537.txt`](seed537.txt). Partition
`[1,537]` into the 53 blocks `[1,10]`, `[11,20]`, ..., `[521,530]`
and the final block `[531,537]`. For each block `B`, choose **any**
function `f_B:{1,...,6}->{1,...,6}`; it need not be injective or the same
on different blocks. Recolour each position `v` by `f_B(W(v))`, where `B`
contains `v`. No such output avoids every monochromatic `x+y=z`,
**including `x=y`**.

This strictly extends the regular-grid case of the earlier
[permutation-only block result](../schur_s6_decadal_block_trades/README.md):
old colour classes may now merge within each block. The number of changed
positions is unrestricted. The conclusion also covers coarser contiguous
block maps whose cuts are all multiples of ten, since one map can be
repeated on every constituent ten-position block.

The result remains conditional on `W` and this block structure. It neither
rules out arbitrary recolourings nor proves `S(6)<=536`. It supplies no
valid 537-colouring and changes no numerical bound.

`W` is the [public two-defect near-colouring by umaia1234](https://github.com/umaia1234/agentic-conjectures/blob/main/problems/schur-6/README.md),
normalized as a 537-digit word with SHA-256
`58c26704225562a6cde8346f0febe1e09f5604c18f9ec0397e8bf16b3e3497b3`.
Its only classical violations are `12+12=24` and `12+24=36`, both in
colour 4. The [original six-class file](https://github.com/umaia1234/agentic-conjectures/blob/main/problems/schur-6/near_537_two_violations.col)
is distributed under Apache-2.0. Both seed defects cross block boundaries,
so no original monochromatic triple is merely trapped inside one block.

## Exact reduction and certificate

There are 263 used `(block,old_colour)` rows. A Boolean variable for each
row and each possible new colour encodes its image. Exactly-one clauses
make every row choose one new colour; there are **no within-block
injectivity clauses**. A global permutation of output colour names
preserves sum-freeness and the map form, so any candidate can be renamed
to give integer 1 the original colour 2. One unit clause makes that
normalization. It is the only fixed output colour.

For every unordered Schur triple `x<=y`, `x+y=z<=537`, and each of six
new colours, a clause forbids all of its row images being that colour.
Repeated rows inside a triple and duplicate row supports are collapsed.
The original 72,092 triples, including all 268 doubling triples, are all
considered. A satisfying assignment of the resulting CNF is **equivalent**
to a valid colouring in the stated family. The CNF has 1,578 variables
and 320,733 clauses.

[`encode.py`](encode.py) generates the formula. The independent
[`audit.py`](audit.py) reconstructs and compares its complete clause
multiset from an `x`-first triple enumeration, validates the two seed
defects, and checks the absence of any original defect contained wholly
in a block. The DIMACS SHA-256 is
`fb1b8382355c35a0df6d22ed53e8812da3c5ae9bf2f3910733c3e3c649a9bae4`.

CaDiCaL 1.9.5 produced an 88,148,914-byte binary DRAT proof, SHA-256
`fe804ea32ec8681c0c59c77ff29d0954585f451c2d5bae61fa406e5fa2b55ba7`.
DRAT-trim independently returned `s VERIFIED`; its backward core used
53,863 original clauses and 1,132,625 proof lemmas. The proof is
regenerated in temporary storage during verification, then deleted. Its
size and hash, the CNF hash, and the tested tool commits are recorded in
[`expected.json`](expected.json). A different proof hash remains valid if
DRAT-trim verifies it against the fully audited CNF.

The mathematical trust boundary is the reduction to the exact map family,
the full clause audit, and the independent DRAT checker. A solver `UNSAT`
status alone would not establish this result.

## Reproduction

Use Python 3.8 or later, CaDiCaL 1.9.5 (tested source commit
`146207318796f094dcded87349a64f0c6927309e`), and DRAT-trim (tested
source commit `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`). No Python
package is required. From this directory:

```sh
sha256sum -c SHA256SUMS
python3 -B verify.py --cadical /path/to/cadical --drat-trim /path/to/drat-trim
```

Expected final output with the tested tools:

```text
PASS rows=263 supports=52754 clauses=320733 triples=72092 doubling=268 seed_defects=2 all_clauses_audited=yes
PASS noninjective_decadal_maps_unsat=yes drat_verified=yes reference_proof_match=yes proof_bytes=88148914
```

The proof needs roughly 90 MB of temporary disk space and took several
minutes to generate and check in the tested environment. Other shifts of
the ten-position grid and finer block maps have not been certified here.
The published frontier remains
`S(6)>=536` from [Fredricksen–Sweet (2000)](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v7i1r32).
