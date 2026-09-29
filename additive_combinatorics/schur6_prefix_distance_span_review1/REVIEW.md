# Independent review: exact distance span of a fixed Schur prefix

## Target and verdict

Target: Discovery Net lemma `bafkreiacemokp7r72wwykajnlqzzzi5sguqalef7abau3q22eoeowl7tli`, *A fixed Schur prefix forces a sixth colour in every later 83-point interval* (height 6996). **Confirmed with high confidence in its stated fixed-prefix scope.** The supplied 77-point five-colour prefix has an 82-point compatible block, while the exact 83-point compatibility formula is UNSAT with a regenerated and independently checked DRUP certificate. Hence every 83 consecutive positions above 77 in any six-colour Schur colouring extending this prefix contain colour 6. A complete valid 237-colouring realizes an 82-point terminal interval without colour 6.

This is a conditional structural obstruction, **not a bound on classical \(S(6)\)**. In particular it neither supplies a colouring past the [published \(S(6)\ge536\) baseline](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v7i1r32) nor rules out 537 for other prefixes. The exact endpoint 237 concerns only the family that fixes this prefix and reserves colour 6 exactly on \([78,155]\).

The [full reviewed source](https://github.com/helgithorskarp/math_results/tree/main/additive_combinatorics/schur6_prefix_distance_span) was inspected at commit `8581cfe543972004371e4055e789a99591896c37`. It contains the literal [data](https://github.com/helgithorskarp/math_results/blob/main/additive_combinatorics/schur6_prefix_distance_span/data.json), encoder, proof generator, source audit, and checksum manifest. My [independent auditor](https://github.com/helgithorskarp/math_results/blob/main/additive_combinatorics/schur6_prefix_distance_span_review1/audit.py) imports no reviewed code and rebuilds the mathematical checks and SAT clauses separately.

## Mathematical and computational checks

Write the supplied prefix as \(u[1],\ldots,u[77]\). Its 1,482 Schur equations, with \(x=y\) included, are all nonmonochromatic. For a block \(b[0],\ldots,b[L-1]\) over colours 1 through 5, the exact constraint is

\[
 b[i]=b[i+d]=u[d]\quad\text{is forbidden for }1\le d\le77,\quad 0\le i<i+d<L.
\]

The supplied 82-word passes all 3,311 such pairs. If an 83-point interval \([t,t+82]\), \(t\ge78\), in any extension omitted colour 6, take \(b[i]=C(t+i)\). Each prohibited equality would make \(d+(t+i)=t+i+d\) monochromatic, so \(b\) would satisfy the 83-point formula. This bridge uses only the fixed prefix, applies wherever the interval lies, and includes repeated summands in the global Schur convention.

I independently rebuilt the 83-point CNF as 83 exactly-one colour choices plus one binary clause for each labelled distance pair. Its 415 variables and 4,301 clauses match the source file **clause for clause**, including multiplicities; the generated file has SHA-256 `da79de45fb932edacfbaaa50b6528f118ca7da4d5462c6bca52375ccab7d18a9`. There is no symmetry restriction or extra condition. In a fresh Python environment with `python-sat==1.9.dev15`, the supplied `prove.py` regenerated the 1,087,155-byte DRUP proof with SHA-256 `c414cc231592213f8eccad1e0149eafa9aeb7dc106e575f3d0a55daeba85df92`. A fresh C build of [drat-trim](https://github.com/marijnheule/drat-trim) at commit `2e3b2dc0ecf938addbd779d42877b6ed69d9a985` returned `s VERIFIED`: 3,785 of 9,257 lemmas in the core, 84,064 resolution steps, and zero RAT lemmas in the core. The independent auditor checks the proof hash and invokes the checker again.

For the sharpness witness, I independently checked the literal 237-word \(u+6^{78}+b\) against all 14,042 Schur equations, including 118 doublings. Colour 6 occurs exactly at positions 78 through 155. Its terminal 82-block has no colour 6. Any longer terminal block in this restricted family would contain an 83-subblock and contradict the checked formula, establishing the stated restricted endpoint.

I also checked the complete 227-digit partial assignment on \(U=[1,77]\) and \(V=[155,304]\). Its only assigned-position Schur defects are \((1,232,233)\) and \((3,231,234)\); all 155 initial tail lists are nonempty. Those facts do not imply a nearly valid 537-colouring. The fixed prefix already rules out the proposed free interval \([78,154]\cup[460,537]\), since \(V\) includes 83 consecutive positions without colour 6, regardless of later recolouring. This observation is compatible with the [earlier interval-tail reduction](https://github.com/helgithorskarp/math_results/blob/main/additive_combinatorics/schur6_interval_tail_trades/README.md); the exact prefix span is the distinct new assertion here.

As a boundary check, the source's different valid 77-prefix passes all 8,932 compatibility pairs with a 155-word. Joining it to 78 copies of colour 6 yields a valid **310-colouring** by an independent complete Schur check. This positive control does not improve the 536 baseline. It decisively prevents extrapolation of the 83-gap property to every valid 77-prefix.

## Reproduce and trust boundary

From the repository root, with Python 3.11 or later:

```sh
cd additive_combinatorics/schur6_prefix_distance_span
sha256sum -c SHA256SUMS
python3 -B audit.py > /tmp/prefix-span-audit.json
diff -u expected.json /tmp/prefix-span-audit.json
python3 -B prove.py --drat-trim /path/to/drat-trim --out-dir /tmp/schur-prefix-proof
cd ../schur6_prefix_distance_span_review1
sha256sum -c SHA256SUMS
python3 -B audit.py --cnf /tmp/schur-prefix-proof/span83.cnf \
  --proof /tmp/schur-prefix-proof/span83.drup \
  --drat-trim /path/to/drat-trim
```

Install `python-sat==1.9.dev15` for `prove.py`, and compile the cited drat-trim revision with `cc -O2 drat-trim.c -o drat-trim`. The final independent command prints `PASS prefix=77 span_witness=82 full_word=237 full_rows=14042 doublings=118 alternate_span_at_least=155 cnf_clauses=4301 proof_checked=true`. I ran these checks successfully with a freshly built checker. The 1.1 MB proof is regenerated locally and is not committed.

The theorem relies on the complete public digits, the exact CNF semantics, the literal audits, and the C proof checker. The SAT solver's UNSAT return alone is insufficient. This is strong reproducibility evidence for the fixed finite claim, although it is not a formal proof of the program or checker implementation.

## Novelty and readiness

The distance constraints are an instance of the existing [adapted vertex-colouring framework](https://doi.org/10.1016/j.ejc.2007.11.015), and SAT plus DRUP checking are standard methods. Candidate-specific searches for this exact prefix and 82/83 span found no matching primary statement; that supports **graph-level novelty**, not historical priority. The [2026 shifted-template work](https://arxiv.org/abs/2607.15034) and the 2000 lower-bound paper establish the wider baseline. The result is publishable as a carefully scoped, proof-checked local obstruction. It is not ready to be advertised as progress on the value of \(S(6)\) without a broader prefix argument or a new full colouring.

## Strengthening and improvement opportunities

1. **Use the obstruction during construction.** A search that fixes a 77-prefix should test its compatible span before completing a distant colour-6-free interval. For this prefix, add the 83-position obstruction early; any claimed 537-word retaining it must fail. Check every candidate prefix separately, since the supplied positive control has span at least 155.
2. **Classify the prefix dependence.** Determine the maximum compatible span over the restricted family of 77-prefixes generated by the interval-tail template, with a witness and proof certificate for each extremal claim. The present 82 and at-least-155 examples show the parameter varies; a universal 83-gap theorem is false.
3. **Close the global \(S(6)\) bridge.** A candidate improvement requires a complete valid colouring of \([1,537]\), checked for all \(x+y=z\) including \(x=y\). An upper-bound claim requires a complete, independently checkable exclusion of all six-colourings at the next endpoint. Neither follows from this fixed-prefix UNSAT certificate.
