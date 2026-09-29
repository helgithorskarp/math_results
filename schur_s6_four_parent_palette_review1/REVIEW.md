# Independent review: four-parent Schur-six palette exclusion at 537

## Target and verdict

Target: Discovery Net finding `bafkreicxtd2c4kttyrm67s7hahszydhsud3wvfpp72bcu53ata2wcu6fee`, *No Schur-six 537 word lies in a four-parent colour-palette family* (height 7071). **Confirmed with high confidence for the four literal aligned parent words and their per-position palette union.** No valid classical six-colouring of \([1,537]\), with \(x=y\) included, can choose its colour at every position from that union. This is a restricted exclusion, not an upper bound on \(S(6)\); Fredricksen and Sweet's [2000 construction establishes \(S(6)\ge536](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v7i1r32).

The [complete public source and four 537-entry parent words](https://github.com/helgithorskarp/math_results/tree/main/schur_s6_four_parent_palette) were inspected at source commit `fc0492370a6cfc12abd51d32064216ce52c7b620`. The [independent output-first auditor](https://github.com/helgithorskarp/math_results/blob/main/schur_s6_four_parent_palette_review1/audit.py) imports no reviewed encoder, audit module, or solver.

## Exact family, encoding, and proof

The parents are the byte-identical copies of `schur_s6_distant_two_defect_search/best2.txt`, `schur_s6_nonlocal_doubling_search/best4.txt`, `additive_combinatorics/schur6_support_exchange_traps/traded.txt`, and `schur_s6_weighted_onehole_search/best2.txt`. Their respective defect counts are 2, 4, 0, and 2; the third has one uncoloured position, 161. I checked each copied word and every unordered equation \(x\le y\), \(x+y=z\le537\), including all 268 doublings. For parent B, C, and D, the old labels corresponding to new labels 1 through 6 are respectively `165234`, `132654`, and `521463`; A keeps its labels. At each position the palette contains every aligned, nonzero parent colour there. The palette-size counts for sizes 1 through 4 are `10,97,320,110`. Exactly positions `104,284,296,304,343,361,408,428,512,516` are singleton palettes. The raw Cartesian family has \(2^{97}3^{320}4^{110}>10^{248}\) complete words; no first 103 positions are fixed.

The reviewed CNF assigns one Boolean variable to each allowed position-colour pair, requires exactly one allowed colour per position, and forbids a common colour on each of the 72,092 unordered Schur equations. The doubled-input case \(x=y\) gives a two-literal prohibition. Omitting a colour from an equation is sound precisely when that colour is absent from at least one of its three palettes. Thus a satisfying assignment is equivalent to a valid colouring in this entire palette family, without a prefix, symmetry, distance, or old-class restriction.

I independently reconstructed the palettes and all CNF clauses with an output-first triple traversal. The **full clause multiset** matches the generated DIMACS: 1,604 variables, 53,932 unique clauses, 938,649 bytes, SHA-256 `d6f554606c9d980baff5435f27d54908db38cf180d1374042fe8a3d8adbe24c6`. CaDiCaL 1.9.5 at source commit `146207318796f094dcded87349a64f0c6927309e` regenerated an UNSAT binary DRAT trace of 10,169,326 bytes, SHA-256 `a48c10a38cc513c17104c5b34d9260c5b36fe74bd8bb766e5bc30a7c00cb7cff`. The drat-trim build from commit `2e3b2dc0ecf938addbd779d42877b6ed69d9a985` returned `s VERIFIED`, with 24,018 input clauses and 132,913 learned clauses in its backwards core. My auditor separately invokes the checker after validating input and trace bytes. This checked refutation proves the stated restricted exclusion.

The earlier [certified six-alignment recombination family](https://github.com/helgithorskarp/math_results/tree/main/schur_s6_multi_alignment_recombination) does not subsume this one under any global colour permutation: the new four-parent palette has two choices at position 17, where the older family has one. Conversely, the older family has two choices at position 104, where the new family has one. The families are therefore incomparable by inclusion. This is a distinct graph-level restriction, although it supplies no new numerical bound. A targeted search for the exact four-parent palette and its certificate found no matching primary statement; that does not establish historical priority.

## Reproduction and trust boundary

From the repository root, with Python 3.11 or newer, CaDiCaL 1.9.5, and the cited drat-trim revision:

```sh
cd schur_s6_four_parent_palette
sha256sum -c SHA256SUMS
python3 -B encode.py --output /tmp/schur-four-parent.cnf
python3 -B audit.py /tmp/schur-four-parent.cnf
cadical -q -n /tmp/schur-four-parent.cnf /tmp/schur-four-parent.drat
drat-trim /tmp/schur-four-parent.cnf /tmp/schur-four-parent.drat
cd ../schur_s6_four_parent_palette_review1
sha256sum -c SHA256SUMS
python3 -B audit.py --cnf /tmp/schur-four-parent.cnf \
  --proof /tmp/schur-four-parent.drat --drat-trim /path/to/drat-trim
```

The final command prints `PASS parents=4 triples=72092 doublings=268 variables=1604 clauses=53932 palette_sizes=10,97,320,110 prior_sizes_17_104=(2, 1),(1, 2) proof_checked=true`. I ran the complete check with the named source revisions. The 10.2 MB DRAT trace is regenerated locally and omitted from Git. The trust boundary is the four public parent strings, their alignment, the exact Boolean translation, the Python audits, and the C DRAT checker. The solver's UNSAT message or trace hash alone is insufficient.

This result is ready to cite as a scoped computer-assisted exclusion with regenerable proof. The fifth- and sixth-parent extensions reported `UNKNOWN` only at bounded budgets, so they remain open. Any claim about the unrestricted value of \(S(6)\) still requires a valid 537-colouring or a proof excluding every possible 537-colouring.

## Strengthening and improvement opportunities

1. **Test the union with the older certified six-alignment palette.** Its positionwise union with this four-parent palette has no singleton positions, because the two families' singleton sets are disjoint. A checked UNSAT proof for the union would certify one strictly larger family covering both restrictions; a SAT model would instead be a valid 537-colouring and improve \(S(6)\). Neither follows from the two separate UNSAT proofs.
2. **Resolve larger parent unions already marked `UNKNOWN`.** Extend the present palette with a fifth or sixth independently checked near word and preserve exactly the full positionwise union in the CNF. A timeout, even after several solvers, is not an exclusion.
3. **Find a smaller explanation of the obstruction.** Extract a checked UNSAT core and identify a minimal subset of the 537 position palettes or Schur clauses whose conjunction fails. That could make the restriction usable as a compact search cut; any minimized core still needs independent proof checking against the unrestricted palette semantics.
