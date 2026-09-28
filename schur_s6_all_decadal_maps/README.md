# All ten noninjective decadal-map grids fail for one Schur-six near-colouring

## Exact theorem

Fix the 537-entry word `W` in [`seed537.txt`](seed537.txt). For any
`r in {1,...,10}`, partition `[1,537]` into `[1,r]`, successive blocks
of ten positions, and a final block of at most ten positions. Independently
choose **any** function `f_B:{1,...,6}->{1,...,6}` on each block `B`;
the functions may merge colours. Recolour every position `v` by
`f_B(W(v))`, where `B` contains `v`. **No resulting word avoids all
monochromatic `x+y=z`, including `x=y`.**

The number of changed positions is unrestricted. This also excludes a
recolouring by arbitrary maps on any coarser contiguous partition whose
internal cut positions are all congruent modulo ten: its blocks are unions
of blocks of one of the ten grids, so repeat each coarse map on those grid
blocks.

The theorem is conditional on this one input word and its block structure.
It does not exclude arbitrary recolourings, finer partitions, or a valid
six-colouring of `[1,537]`. It gives no new numerical bound for the
classical sixth Schur number. The published lower bound remains
[`S(6)>=536` (Fredricksen–Sweet, 2000)](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v7i1r32).

The word `W` comes from the [public two-defect near-colouring by umaia1234](https://github.com/umaia1234/agentic-conjectures/blob/main/problems/schur-6/README.md).
The normalized 537-digit file has SHA-256
`58c26704225562a6cde8346f0febe1e09f5604c18f9ec0397e8bf16b3e3497b3`.
Its only classical violations are `12+12=24` and `12+24=36`, both old
colour 4. The [original six-class file](https://github.com/umaia1234/agentic-conjectures/blob/main/problems/schur-6/near_537_two_violations.col)
is distributed under Apache-2.0.

The earlier certificates covered
[permutations on all ten grids](../schur_s6_decadal_block_trades/README.md),
then [arbitrary maps on grid 10](../schur_s6_decadal_maps/README.md),
and [arbitrary maps on grids 1 and 9](../schur_s6_shifted_decadal_maps/README.md).
This artifact gives one self-contained encoder and proof for arbitrary maps
on **every** grid shift. It does not rely on those certificates.

## Why the CNF is exact

For each grid, one row represents a `(block,old_colour)` pair actually used
by `W`. Its six Boolean variables choose exactly one output colour. There
are no within-block injectivity clauses. Any assignment to the used rows
extends to a full function on the six old colours in each block.

Output colour names can be permuted globally without changing either the
map family or monochromatic sums. In row order, relabel the used output
colours `1,2,...` by **first appearance**. The first row then has colour 1;
if row `i` has colour `c>1`, some earlier row has colour `c-1`. The CNF
enforces precisely these necessary conditions. Every candidate has such a
representative, so this symmetry normalization loses no valid output.

For every unordered Schur triple `x<=y`, `x+y=z<=537`, and every output
colour, one clause prevents its supporting rows all taking that colour.
Equal rows inside a triple and duplicate row supports are collapsed.
All **72,092** triples, including all **268** doubling triples, are
considered. Thus each CNF is satisfiable if and only if a valid word
exists in its stated block-map family.

[`encode.py`](encode.py) writes the ten DIMACS files. The independent
[`audit.py`](audit.py) uses a different block formula and an `x`-first
triple enumeration to rebuild and compare every clause as a multiset,
including the complete first-appearance normalization. It also checks the
seed digest and its exact two defects.

| Offset | Used rows | Variables | Clauses | Binary DRAT bytes |
| ---: | ---: | ---: | ---: | ---: |
| 1 | 268 | 1,608 | 324,596 | 4,696,492 |
| 2 | 268 | 1,608 | 323,426 | 6,317,106 |
| 3 | 265 | 1,590 | 319,073 | 4,346,455 |
| 4 | 267 | 1,602 | 319,871 | 11,077,226 |
| 5 | 270 | 1,620 | 321,638 | 7,955,202 |
| 6 | 270 | 1,620 | 324,680 | 8,215,405 |
| 7 | 271 | 1,626 | 324,215 | 14,488,984 |
| 8 | 266 | 1,596 | 321,002 | 12,423,023 |
| 9 | 264 | 1,584 | 319,832 | 5,789,734 |
| 10 | 263 | 1,578 | 322,043 | 4,728,883 |

CaDiCaL 1.9.5 returned `UNSAT` for all ten cases. Independent DRAT-trim
returned `s VERIFIED` for every binary proof against its audited CNF.
[`expected.json`](expected.json) records the exact CNF and proof sizes,
SHA-256 digests, backward core counts, and tested tool commits. A solver
status alone is not the proof. The trust boundary is the exact map-family
reduction, the full clause audit, and the independent DRAT checker.

## Reproduce

Use Python 3.8 or later, CaDiCaL 1.9.5 (tested source commit
`146207318796f094dcded87349a64f0c6927309e`), and DRAT-trim (tested
source commit `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`). No Python
package is needed. From this directory:

```sh
sha256sum -c SHA256SUMS
python3 -B verify.py --cadical /path/to/cadical --drat-trim /path/to/drat-trim
```

The verifier regenerates and audits each CNF, solves it, independently
checks the DRAT proof, compares its size and digest with the reference,
and deletes temporary files. `--offsets 5` selects one case. The largest
reference proof is about 15 MB, and cases are processed sequentially.
