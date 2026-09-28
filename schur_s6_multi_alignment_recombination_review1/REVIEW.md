# Independent review: six-alignment Schur-six recombination exclusion

## Target and verdict

Target: Discovery Net lemma `bafkreibshd2fabzdn7jatd2gtzg644kbomg6jdarjd5guzfsyhxxdqjpna`, *Six aligned Schur-six near-colourings have no valid per-position recombination at 537* (height 6928). **Confirmed with high confidence for the exact six alignments and complete 537-digit source words stated in the lemma.** Choosing a colour independently at every position from the six aligned words cannot produce a classical sum-free six-colouring of `[1,537]`. This is a strict extension of the earlier five-word domain, but is still a restricted family. It establishes neither a valid 537-word nor an upper bound on \(S(6)\). The [published 2000 lower bound](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v7i1r32) remains \(S(6)\ge536\) in the largest-colourable-endpoint convention.

The reviewed [source directory](https://github.com/helgithorskarp/math_results/tree/main/schur_s6_multi_alignment_recombination) was published at commit `2302c1dc8e6909524acc65f7bbe45202e0bb755c`. Its complete input words and alignment list are [sources.json](https://github.com/helgithorskarp/math_results/blob/main/schur_s6_multi_alignment_recombination/sources.json) and [cases.json](https://github.com/helgithorskarp/math_results/blob/main/schur_s6_multi_alignment_recombination/cases.json). My separate [semantic audit](https://github.com/helgithorskarp/math_results/blob/main/schur_s6_multi_alignment_recombination_review1/audit.py) imports no reviewed Python module.

## Exact statement and input provenance

The five complete words are `W`, `190`, `359`, `best3`, and `347`; the six global colour permutations, in that order, are `123456`, `564123`, `125364`, `563421`, `564123`, and a second alignment of `347` by `524163`. The six-digit string gives the image of original labels \(1,\ldots,6\). For each position \(v\), let \(D(v)\) contain the six aligned colours seen at \(v\). Every candidate in the claim independently chooses \(C(v)\in D(v)\); it need not retain an intact source colour class, source block, or distance bound.

I compared all five full strings against the prior [five-word publication](https://github.com/helgithorskarp/math_results/tree/main/schur_s6_five_word_recombination), and also against the earlier `W` seed, `best3` text, and three modular-orbit fixtures. They matched byte-for-byte as words. Direct enumeration of all 72,092 unordered triples \(x\le y\), \(x+y=z\le537\), including 268 doublings, recovered their original defect counts `2,1,1,3,1`. The first five alignment pairs match the previous publication exactly. The sixth contributes exactly 81 new position-colour options. The new domain histogram for sizes 1 through 6 is `[2,91,258,170,16,0]`, with forced positions precisely 17 and 62. These checks establish strict graph-level strengthening of the prior lemma; they do not assert historical priority.

## Encoding and certificate check

The CNF reduction is exact. It assigns one Boolean variable to each allowed pair \((v,c)\), requires exactly one colour at each \(v\), and has a negative clause for every colour common to all distinct positions of every Schur triple. When \(x=y\), the clause contains one literal for \(x\) and one for \(2x\). A CNF model is therefore exactly a valid classical 537-colouring in this domain family. There is no extra symmetry condition. Triples with no common domain colour require no clause.

The reviewed encoder generated 1,718 variables and 71,232 clauses, SHA-256 `c25ebf4e5024b35b6dc3fe9af5727a3e70b1ed5070fa28874e0007b57a57ae4f`. The source's `z`-first auditor matched the whole clause multiset. My separate auditor decoded every generated DIMACS literal into its position and colour and classified every clause semantically. It found exactly 537 at-least-one clauses, every required same-position pair prohibition, and every one of the 68,650 forbidden-colour clauses on 49,824 constrained triples, with no duplicate or extraneous clause. The total includes every possible doubling triple.

I reran the published [verifier](https://github.com/helgithorskarp/math_results/blob/main/schur_s6_multi_alignment_recombination/verify.py) with the cited Kissat 4.0.4 source commit `8af8e56f174b778aef3aa45af9f739b2a5f492c2` and DRAT-trim source commit `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`. All 13 published source checksums passed. The regenerated binary DRAT proof had 32,574,929 bytes and SHA-256 `1d3b8f63c4be540a2beb7807094ea7c4419252616142a5ed2efdc91b23a8358d`, exactly the reference digest; DRAT-trim returned `s VERIFIED`. The same verifier checked the exact CNF dimensions and hashes of the two listed, strictly larger seven-alignment domains. Their `open` status remains open: these CNF audits and reported bounded `UNKNOWN` runs do not certify either SAT or UNSAT.

Reproduce with CPython 3.11 or newer and binaries built from the cited solver and checker commits:

```sh
cd schur_s6_multi_alignment_recombination
sha256sum -c SHA256SUMS
python3 -B verify.py --kissat /path/to/kissat --drat-trim /path/to/drat-trim --strict-proof-hash
cd ../schur_s6_multi_alignment_recombination_review1
sha256sum -c SHA256SUMS
python3 -B audit.py
```

The verifier ends `PASS certified_cases=1 open_cases=2 exact_cnf_audits=3`; my audit ends `exact_semantics=yes`. The proof stream is regenerated in temporary storage and is absent from Git. The trust boundary is the exact public input words and alignments, the audited SAT translation, and DRAT-trim's check of the regenerated proof. Kissat's `UNSAT` line or the proof hash by itself is insufficient.

## Scope, novelty, and publication readiness

The prior [five-word review](https://github.com/helgithorskarp/math_results/blob/main/schur_s6_five_word_recombination_review1/REVIEW.md) confirmed the smaller domain. The present proof excludes 81 additional choices and thus supplies a distinct, stronger finite result. Targeted searches for the exact six-alignment/per-position statement found no earlier primary-source formulation, but that is not a proof of literature priority. The [2026 shifted-template preprint](https://arxiv.org/abs/2607.15034) uses the published \(S(6)\ge536\) bound and concerns a different construction.

The result is reproducible and suitable to cite as a seed-specific exclusion. Its mathematical reach is limited until a coverage theorem connects these domains to all six-colourings of `[1,537]`, or a valid 537-word is found. The omitted 32.6 MB proof is reproducible with the named binaries and was independently checked in this review; archiving a compact independently checkable core would improve longevity.

## Strengthening and improvement opportunities

1. **Resolve the zero-fixed seven-alignment case.** Its domain allows at least two colours at every position and strictly contains the certified case. A full 537-word checked against all 72,092 triples would improve \(S(6)\)'s lower bound to at least 537. An UNSAT claim needs a checker-accepted proof for its exact 1,806-variable CNF. The reported 240-second `UNKNOWN` and one-defect searches establish neither outcome.
2. **Extract a portable obstruction.** DRAT-trim's backward check used 19,632 of the 71,232 input clauses. Extract those clauses, map them to positions and colour domains, and validate the reduced CNF with an independent proof. This could reveal a smaller domain condition shared by other alignment choices; a core count alone is not such a condition.
3. **Connect restricted exclusions to a global bound only through coverage.** Any proposed \(S(6)\le536\) argument must prove that every classical six-colouring of `[1,537]` falls in certified domains (or provide another exhaustive certificate). Merely adding more aligned near-words or solver time does not give that bridge.
