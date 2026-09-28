# Certified shifted decadal-map exclusions for Schur six

## Exact result

Fix the 537-entry six-colour word [`seed537.txt`](seed537.txt). For either
`r=1` or `r=9`, partition `[1,537]` into the first block `[1,r]`, successive
ten-position blocks, and a final block of at most ten positions. On each
block `B`, independently choose **any** function
`f_B:{1,...,6}->{1,...,6}`; it may merge colours. Recolour position `v`
as `f_B(W(v))`. Every resulting word has a monochromatic `x+y=z`,
**including `x=y`**.

These two grid shifts are distinct from the previously certified
[`r=10` noninjective grid](../schur_s6_decadal_maps/README.md). Together,
the three results exclude arbitrary block colour maps on offsets `1,9,10`.
The earlier [ten-offset permutation result](../schur_s6_decadal_block_trades/README.md)
allows every shift but requires a permutation on each block. The present
result permits merging old colours on the two stated shifts and places no
limit on the number of changed positions. Every coarser contiguous block
map whose cut positions lie on one of these grids is also excluded.

This is a fixed-seed, grid-restricted exclusion. Offsets `2,...,8` with
noninjective maps, arbitrary recolourings, and the existence of a valid
537-colouring are **not** settled here. No numerical Schur bound changes.
The published classical lower bound remains
[`S(6)>=536` (Fredricksen–Sweet, 2000)](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v7i1r32).

The word `W` is the [public two-defect near-colouring by umaia1234](https://github.com/umaia1234/agentic-conjectures/blob/main/problems/schur-6/README.md),
normalized with SHA-256
`58c26704225562a6cde8346f0febe1e09f5604c18f9ec0397e8bf16b3e3497b3`.
Its only classical violations are `12+12=24` and `12+24=36`, both in
old colour 4. The [original six-class file](https://github.com/umaia1234/agentic-conjectures/blob/main/problems/schur-6/near_537_two_violations.col)
is distributed under Apache-2.0.

## Exact reduction and proof checks

A row is a `(block,old_colour)` pair used by `W`. Each row chooses one of
six output colours, with no injectivity clauses. A global permutation of
output labels makes the image of `W(1)=2` equal to 2, so one unit clause
provides a sound symmetry normalization. For every unordered Schur triple
`x<=y`, `x+y=z<=537`, and output colour, one clause forbids all supporting
rows taking that colour. Repeated rows and duplicate supports are
collapsed. Every one of the 72,092 triples, including 268 doublings, is
considered. The CNF is satisfiable if and only if a valid word exists in
the stated family.

[`encode.py`](encode.py) generates the CNFs. The separate [`audit.py`](audit.py)
uses an `x`-first enumeration and a different block formula to compare
the complete clause multiset; it also checks the word and its two defects.

| Offset | Used rows | Variables | Clauses | Binary DRAT bytes | DRAT-trim |
| ---: | ---: | ---: | ---: | ---: | :--- |
| 1 | 268 | 1,608 | 323,261 | 111,949,043 | `s VERIFIED` |
| 9 | 264 | 1,584 | 318,517 | 107,469,659 | `s VERIFIED` |

CaDiCaL 1.9.5 produced both binary DRAT proofs. Independent DRAT-trim
verified them against the fully audited CNFs. The precise CNF/proof sizes,
SHA-256 digests, backward core counts, and tested tool commits are in
[`expected.json`](expected.json). A solver `UNSAT` message alone is not the
certificate. The mathematical trust boundary is the row-map reduction,
complete clause audit, and independent proof checker.

The encoder at `r=10` also reproduces the previously published CNF
SHA-256 `fb1b8382355c35a0df6d22ed53e8812da3c5ae9bf2f3910733c3e3c649a9bae4`
byte for byte. That is a cross-check of the shifted-grid implementation;
its proof is in the earlier artifact.

For orientation, the same audited encoder was also run at each offset
`2,...,8` with CaDiCaL `-q --sat --seed=20260928 -t 300`. Every one returned
`UNKNOWN`. Those bounded runs supply no exclusion; their incomplete traces
are absent from the certificate manifest.

## Reproduce

Use Python 3.8 or later, CaDiCaL 1.9.5 (tested commit
`146207318796f094dcded87349a64f0c6927309e`), and DRAT-trim (tested
commit `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`). No Python package
is required. From this directory:

```sh
sha256sum -c SHA256SUMS
python3 -B verify.py --cadical /path/to/cadical --drat-trim /path/to/drat-trim
```

`verify.py` regenerates each CNF, audits every clause, runs the solver,
checks its proof independently, and deletes temporary files. It compares
proof hashes for the tested versions, while accepting a different verified
proof from another compatible build. Use `--offsets 1` or `--offsets 9`
to check one case. Each proof needs about 110 MB of temporary storage and
several minutes to generate and check.
