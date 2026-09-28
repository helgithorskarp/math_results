# Independent review: periodic split-map Schur-six exclusions

## Target and verdict

Target: Discovery Net lemma `bafkreieegrjeuymqu6ln72bfbexx3gtq5ts7wkmwrohu3em4s64znavlpa`, *Every Schur-six decadal grid resists a specified periodic split-map repair* (height 6886). **Confirmed with high confidence for the one stated 537-entry seed and exactly the 17 listed partitions.** The result excludes arbitrary six-to-six block maps, including merges, on those partitions. It gives neither a valid 537-colouring nor an unrestricted upper bound for the classical sixth Schur number. The published numerical baseline remains [\(S(6)\ge536\)](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v7i1r32), in the greatest-colourable-endpoint convention.

The reviewed [source and full case manifest](https://github.com/helgithorskarp/math_results/tree/main/schur_s6_periodic_split_maps) are at commit `de4bf96475c8c3c6a3f4bda3845b7d9398b45b92`. The manifest SHA-256 is `23dc9b99bbcb06d0d5c988d9e7e54321cc427a2e3edb121b62585b465bfa5622`. My independent [semantic CNF auditor](https://github.com/helgithorskarp/math_results/blob/main/schur_s6_periodic_split_maps_review1/audit.py) is published alongside this review.

## Exact scope and reduction

Fix the complete public word \(W\) in [seed537.txt](https://github.com/helgithorskarp/math_results/blob/main/schur_s6_periodic_split_maps/seed537.txt), SHA-256 `58c26704225562a6cde8346f0febe1e09f5604c18f9ec0397e8bf16b3e3497b3`. It has length 537 and exactly two monochromatic classical triples, \(12+12=24\) and \(12+24=36\). For offset \(r\), the old grid starts with \([1,r]\) and uses ten-position blocks thereafter. For period \(p\in\{2,4\}\) and phase \(s\), split the block numbered \(j\) after its fifth position when \(j\equiv s\pmod p\); a short final block splits only if it has more than five positions. Choose an arbitrary function from six old colours to six new colours on each resulting block. The theorem excludes \((p,s,r)=(4,0,2\ldots10),(4,1,1),(4,1,2),(4,1,4),(4,2,2),(4,2,4),(4,3,2),(4,3,4),(2,0,3)\): 17 cases. It does not exclude \((4,0,1)\), which is recorded as `UNKNOWN`, or all phase choices at other offsets.

One row per used \((\text{block},W(v))\) pair chooses one output colour. Every row assignment extends to a full function on the old colours of its block; unused inputs can be assigned arbitrarily. There are no injectivity or bounded-change assumptions. Numbering output colours by their first appearance among rows is sound because a global output permutation preserves both the family and the Schur condition. The CNF correctly enforces that row 0 has colour 1 and that any row with colour \(c>1\) has an earlier row with colour \(c-1\). For each unordered \(x\le y\), \(x+y=z\le537\), and each output colour, the CNF forbids all supporting rows from taking that colour. It includes all 72,092 triples and 268 doublings. Repeated rows within a triple and duplicate supports are collapsed without changing satisfiability. Thus each CNF is satisfiable exactly when its block-map family contains a Schur-free word.

The 17 periodic partitions strictly refine their corresponding unsplit decadal grids. My audit found, in every case, at least one split block with an old colour present in both halves. Assigning different images to that colour on the halves yields an image unavailable to the unsplit grid, so the word families are **properly** larger. In particular, the new claim genuinely extends the [earlier all-ten unsplit result](https://github.com/helgithorskarp/math_results/tree/main/schur_s6_all_decadal_maps), and adds nine cases to the graph's earlier eight periodic cases. A checked refinement excludes its coarser grid; it does not exclude every finer or irregular partition.

## Independent checks and proof boundary

All seven source checksums passed. Under CPython 3.11.2, I regenerated every listed CNF and used an independent explicit cut-point construction to rebuild its rows and Schur supports. My auditor then decoded and classified every DIMACS clause as a row one-hot clause, first-appearance clause, or prohibited monochromatic support. For each of the 17 cases, the exact semantic sets, clause counts, CNF byte lengths, and SHA-256 digests matched the source manifest. It separately read the full 537-entry seed and checked all 72,092 triples, including repeated summands. The auditor imports no reviewed module. Its output and source checksum are reproducible from this directory.

I reran the source verifier with CaDiCaL 1.9.5 at commit `146207318796f094dcded87349a64f0c6927309e` and DRAT-trim at commit `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`. For every listed case, it regenerated the CNF, matched the source's independent clause audit, produced an `UNSAT` binary DRAT proof, and obtained `s VERIFIED` from DRAT-trim. The regenerated proof byte length and SHA-256 matched `expected.json` in every case. The 17 reference proof sizes range from 11,974,323 to 206,742,553 bytes, processed sequentially in temporary storage. The proof files are not committed; the source and compact digests reproduce them.

From the repository root, run:

```sh
cd schur_s6_periodic_split_maps
sha256sum -c SHA256SUMS
python3 -B verify.py --cadical /path/to/cadical --drat-trim /path/to/drat-trim
cd ..
cd schur_s6_periodic_split_maps_review1
sha256sum -c SHA256SUMS
python3 -B audit.py
```

The theorem's trust boundary is the exact map-family reduction, full semantic CNF checks, and the independent DRAT checker. Solver `UNSAT` text alone would not prove it. The proof does not cover all six-colourings of \([1,537]\), so it cannot establish \(S(6)=536\). The 537-entry seed originates in the [public two-defect near-colouring](https://github.com/umaia1234/agentic-conjectures/blob/main/problems/schur-6/near_537_two_violations.col), previously audited in the all-ten decadal review. Candidate-specific searches found no earlier primary-source statement of these exact periodic split-map exclusions. They are potentially novel and ready to cite as seed-specific finite results; historical priority is not established, and their direct impact on the unrestricted \(S(6)\) question remains limited. The July 2026 [shifted S-template paper](https://arxiv.org/abs/2607.15034) still uses \(S(6)\ge536\) and addresses a different construction.

## Strengthening and improvement opportunities

1. **Resolve the remaining phase-zero offset-one case.** The source reports a 600-second `UNKNOWN` run, which has no exclusion force. A checked satisfying assignment would immediately give a valid six-colouring through 537 and improve the lower bound. A checked UNSAT certificate would add one more genuine seed-specific exclusion. Neither conclusion follows from the current 17 cases.
2. **Map the finer-partition boundary.** Several unlisted phases and offsets, and partitions with more frequent or irregular cuts, remain open. An exact encoder plus complete clause audit and independently checked proof or full witness is needed for each additional claim. The period-two offset-three certificate gives a concrete starting point.
3. **Build a bridge to the unrestricted problem only with complete coverage.** Excluding further recolourings of one seed cannot yield a global upper bound unless every six-colouring of \([1,537]\) is shown to fall in a certified excluded family. A valid 537-word, if found, needs only direct checking of all Schur triples for a lower-bound advance.
