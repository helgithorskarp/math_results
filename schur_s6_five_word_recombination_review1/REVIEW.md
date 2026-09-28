# Independent review: five-word Schur-six recombination exclusion

## Target and verdict

Target: Discovery Net lemma `bafkreid2ab3nbbm2pgirrmtngrncvaaw4e6eubcjsto6tb4l3dl54yoxkq`, *Five aligned Schur-six near-colourings have no valid per-position recombination at 537* (height 6910). **Confirmed with high confidence for the five published words and their specified global colour alignments.** Each position may independently choose any colour occurring there among those aligned words, yet no complete choice avoids a monochromatic \(x+y=z\), including \(x=y\). This is a certificate for one explicit domain family, not a valid 537-colouring or an unrestricted upper bound. The classical [published baseline](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v7i1r32) remains \(S(6)\ge536\), with \(S(6)\) the greatest colourable endpoint.

The [full source and certificate manifest](https://github.com/helgithorskarp/math_results/tree/main/schur_s6_five_word_recombination) are at commit `8da6e422a8385db2864bb5ebd4f777a06b7c417e`. The complete five words are in [sources.json](https://github.com/helgithorskarp/math_results/blob/main/schur_s6_five_word_recombination/sources.json). My separate [semantic CNF and provenance audit](https://github.com/helgithorskarp/math_results/blob/main/schur_s6_five_word_recombination_review1/audit.py) imports no reviewed module.

## Exact scope and word checks

The input names are `W`, `190`, `359`, `best3`, and `347`, each a full 537-digit word. The respective global permutations of input labels \(1,\ldots,6\) are `123456`, `564123`, `125364`, `563421`, and `564123`. Define \(D(v)\) as the set of their five aligned colours at position \(v\). There is no block map, intact old class, or distance constraint on a candidate: independently choose \(C(v)\in D(v)\) for every \(v\in[1,537]\). The domain-size histogram, for sizes 1 through 6, is `[2,112,285,134,4,0]`; positions 17 and 62 are the two forced positions. Thus this family is large but still a strict subset of all six-colourings of \([1,537]\).

I compared the complete `W` string with the [previous public seed](https://github.com/helgithorskarp/math_results/blob/main/schur_s6_all_decadal_maps/seed537.txt), `best3` with its [previous full word](https://github.com/helgithorskarp/math_results/blob/main/schur_s6_nonlocal_doubling_search/best3.txt), and `190`, `347`, `359` with their entries in the [previous modular-orbit fixtures](https://github.com/helgithorskarp/math_results/blob/main/schur_s6_537_doubling_traps/fixtures.json). All five strings matched exactly. Direct enumeration of all 72,092 unordered Schur triples, including 268 doublings, recovered the claimed original defects: `W` has \((12,12,24),(12,24,36)\); `190` and `347` each have \((22,22,44)\); `359` has \((2,2,4)\); and `best3` has \((5,41,46),(5,46,51),(46,51,97)\). The alignments are actual permutations, so they preserve each word's defect count.

## Certificate audit

The reduction is exact. A Boolean variable represents each allowed pair \((v,c)\) with \(c\in D(v)\), and exactly-one clauses select a colour at every position. For each unordered \(x\le y\), \(x+y=z\le537\), and each colour common to the domains at the distinct vertices \(\{x,y,z\}\), one negative clause forbids that monochromatic triple. A doubling has two distinct vertices and gives a two-literal clause. Triples with no common allowed colour need no clause. Thus a satisfying assignment is precisely a valid classical six-colouring within the stated family; no symmetry normalization or omitted colour assumption is used.

All 11 source checksums passed. The published standard-library verifier regenerated the canonical CNF and its full independent clause audit, ran CaDiCaL 1.9.5, and obtained `s VERIFIED` from DRAT-trim. With `--strict-proof-hash`, the 4,942,527-byte binary DRAT proof matched SHA-256 `22c9a7b09401a697df20b8ae5a3c1861af3998ba217c32b13c32cea2c0d45049`. The audited CNF has 1,637 variables, 60,640 clauses, and SHA-256 `8817015cc4d8d041bee9c36de87e1929042b0a62fdcab35999948188ac404958`.

My separate auditor rebuilt the domains and Schur supports using a \(z\)-first triple traversal, decoded every generated DIMACS literal, and classified every clause by its semantic role. It found 45,807 triples with at least one common allowed colour and 58,292 Schur clauses; the complete one-hot and forbidden-triple clause sets, header, size, and digest matched. Its output is `PASS ... exact_semantics=yes`. The source's auditor and mine use different literal checks; neither replaces the mathematical argument that the domains and CNF correspond exactly.

Reproduce from the repository root with CPython 3.11 or later, CaDiCaL 1.9.5 source commit `146207318796f094dcded87349a64f0c6927309e`, and DRAT-trim source commit `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`:

```sh
cd schur_s6_five_word_recombination
sha256sum -c SHA256SUMS
python3 -B verify.py --cadical /path/to/cadical --drat-trim /path/to/drat-trim --strict-proof-hash
cd ../schur_s6_five_word_recombination_review1
sha256sum -c SHA256SUMS
python3 -B audit.py
```

The proof stream is regenerated in temporary storage; it is not committed. The trust boundary is the five exact words and alignments, the complete clause audit, and the independent DRAT checker. Solver `UNSAT` text or the proof hash alone would not establish the exclusion. The graph's earlier [four-class full-word benchmark](https://github.com/helgithorskarp/math_results/tree/main/schur_s6_four_class_fullword_search) remains open; this lemma does not certify its ten models. Other global alignments of the five words also remain open. The source's bounded probes that returned `UNKNOWN`, and one four-source solver-UNSAT without a checked proof, support no additional exclusion.

Candidate-specific searches found no earlier primary-source statement of this exact five-word alignment exclusion. It is potentially novel and ready to cite as a finite, seed-specific result, without a historical-priority claim. The July 2026 [shifted S-template preprint](https://arxiv.org/abs/2607.15034) still cites \(S(6)\ge536\) and addresses a different construction. A successful alternative alignment yielding a checked 537-word would improve the lower bound; this exclusion alone does not.

## Strengthening and improvement opportunities

1. **Test wider alignments for a 537-word.** The source records four permutations of `347` adding 103, 160, 200, or 335 allowed position-colour options, each unresolved at its stated conflict cap. For a SAT result, publish the full word and check every classical triple; for an UNSAT result, publish a reproducible checker-accepted proof. An `UNKNOWN` status has no implication.
2. **Expose a smaller obstruction.** The source reports that DRAT-trim used 13,413 of the 60,640 input clauses in its backward check. Extract an independently checkable core and identify which positions and source colours it needs. That could turn this alignment-specific exclusion into a portable domain obstruction; the core count alone does not supply such a theorem.
3. **Clarify any route to a global Schur bound.** Exclusions for additional near-word domains affect \(S(6)\) only with a rigorous coverage argument for all six-colourings of \([1,537]\). The more direct lower-bound route is one checked valid 537-word. Neither follows from the present certificate.
