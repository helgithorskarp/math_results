# Certified periodic splits of Schur-six decadal map grids

## Exact statement

Fix the 537-entry word `W` in [`seed537.txt`](seed537.txt). For an offset
`r` from 1 to 10, begin with the blocks `[1,r]` and then successive
ten-position blocks, truncating the last block at 537. Number the blocks
after `[1,r]` by `j=0,1,...`. For period `p` and phase `s`, split every
block with `j congruent to s (mod p)` after its fifth position. A final
short block is split when it contains more than five positions. On every
resulting block `B`, choose an arbitrary
function `f_B:{1,...,6}->{1,...,6}` and recolour position `v` by
`f_B(W(v))`. The functions need not be injective and there is no limit on
the number of changed positions.

**No Schur-free recolouring exists for the following `(p,s,r)` cases:**

| Period `p` | Phase `s` | Offsets `r` |
| ---: | ---: | :--- |
| 4 | 0 | 2, 3, 4, 5, 6, 7, 8, 9, 10 |
| 4 | 1 | 1, 2, 4 |
| 4 | 2 | 2, 4 |
| 4 | 3 | 2, 4 |
| 2 | 0 | 3 |

Here Schur-free means
no monochromatic `x+y=z` in `[1,537]`, including `x=y`.

For every offset `r=1,...,10`, at least one listed `p=4` phase is excluded;
choose `s=1` for `r=1` and `s=0` otherwise. Each stated partition
strictly refines the corresponding ten-position grid. Thus these
certificates exclude larger families than the
[all-ten decadal-grid result](../schur_s6_all_decadal_maps/README.md) on
every offset. A `p=2,s=0,r=3` map can change colours independently on half
the ten-position blocks. This theorem remains conditional on `W` and
these partitions; it gives no new numerical bound for the classical sixth
Schur number. The published lower bound is
[`S(6)>=536` (Fredricksen–Sweet, 2000)](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v7i1r32).

The word `W` is the normalized [public two-defect near-colouring by
umaia1234](https://github.com/umaia1234/agentic-conjectures/blob/main/problems/schur-6/README.md).
Its SHA-256 is
`58c26704225562a6cde8346f0febe1e09f5604c18f9ec0397e8bf16b3e3497b3`.
The independent audit confirms its only violations are `12+12=24` and
`12+24=36`. The [original six-class
file](https://github.com/umaia1234/agentic-conjectures/blob/main/problems/schur-6/near_537_two_violations.col)
is distributed under Apache-2.0.

## Exact reduction and certificates

One row represents each `(block,old_colour)` pair used by `W`, and its six
Boolean variables choose exactly one new colour. Every choice of the rows
extends to a full function on old colours in each block. Global output
colour relabelling leaves the problem invariant. We select a representative
by numbering colours in order of first appearance among rows: row 0 has
colour 1, and if row `i` has colour `c>1`, an earlier row has colour `c-1`.
Every candidate has such a representative, so the clauses lose none.

For every unordered triple `x<=y`, `x+y=z<=537`, and every new colour, a
clause forbids all its supporting rows having that colour. Repeated rows
in a triple and duplicate row supports are collapsed. All 72,092 triples,
including 268 doubling triples, are covered. Therefore each CNF is
satisfiable exactly when its stated block-map family contains a valid word.

[`encode.py`](encode.py) constructs the CNF. The independent [`audit.py`](audit.py)
uses a different block formula and an `x`-first triple enumeration to
compare every clause as a multiset, including the palette normalization.
CaDiCaL 1.9.5 returned `UNSAT` on the cases in
[`expected.json`](expected.json), and independent DRAT-trim returned
`s VERIFIED` on each binary proof. The JSON records full dimensions, CNF
and proof SHA-256 digests, and proof-core counts. Proof files are generated
by the [`verify.py`](verify.py) script rather than committed.

The tested solver source was commit
`146207318796f094dcded87349a64f0c6927309e`; the tested checker was
DRAT-trim commit `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`.
From this directory, with Python 3.8 or later:

```sh
sha256sum -c SHA256SUMS
python3 -B verify.py --cadical /path/to/cadical --drat-trim /path/to/drat-trim
```

`--cases 2-3 4-10 4-1-1` selects three cases. Two-part keys use
`period-offset` and have phase zero; three-part keys use
`period-phase-offset`. The verifier regenerates each CNF,
checks every clause independently, solves it, verifies the resulting DRAT
proof, checks the recorded sizes and digests, and removes temporary files.
Different solver builds can produce a different valid proof digest; the
independent DRAT result is decisive. Some harder cases can take several
minutes; the manifest records any case-specific solver seed. The checked
cases are exactly those listed above. In particular, the `p=4,s=0,r=1`
case remained `UNKNOWN` after 600 seconds with solver seed 42. That
timeout has no mathematical implication; all other unlisted period,
phase, and offset choices have no conclusion here.
