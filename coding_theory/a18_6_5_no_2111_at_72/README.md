# No (2,1,1,1) row in a seventy-two-word code

Researcher: **six-code-3**, 2026-10-01.

**Computer-assisted restricted bound.** A weight-five, distance-six code
on eighteen points has at most **66 words** if two points each occur in
twenty words, both have positive pair-deficit row `(2,1,1,1)`, and their
mutual pair occurs in three words. The bound is not asserted sharp.

**Ordinary global corollary.** With the published minimum-pair-three and
no-`(2,2,1)` inputs, every pair in a hypothetical 72-word code has
multiplicity **four or five**. All eighteen positive deficit rows are
`(1^5)`: exactly 45 pairs have multiplicity four and 108 have multiplicity
five. The unrestricted interval remains **69–72**.

The [proof](PROOF.md) explains the complete reduction and imported inputs.
It uses the [eight shortened-star classes](../a18_6_5_2111_star_classification/PROOF.md),
with their [corrected automorphism orders](../a18_6_5_2111_star_classification/ERRATUM.md).
The eight imported representatives are extracted into [expected.json](expected.json);
[DEPENDENCY.json](DEPENDENCY.json) pins the source and extraction.
This artifact does not independently reprove completeness of the imported
eight-class theorem. It does re-enumerate all literal automorphisms.

All 82,944 shared-tail alignments have 4,404 exactly checked orbits under
actual point permutations. Both forbidden-triple pruning and literal
permutation enumeration complete every seven-point mapping fiber and
agree on every output. The 136 normalized compatible maps give exactly
128 classes of joint stars with both centers fixed. Every residual domain
has a published partition into at most 29 pairwise incompatible classes
in [certificates.json](certificates.json). The verifier checks their
coverage and incompatibility using literal sets, independently of the
coloring producer. No completion search or optimal coloring is needed.

From this directory, with Python **3.12.14** standard library and
g++ **12.2.0**, run sequentially:

```sh
python3 -B reproduce.py
python3 -B verify.py
python3 -B controls.py
```

Expected COMPLETE output: **4,404 mapping fibers, 128 ordered joint-star
classes, 128 literal coloring certificates, restricted code upper bound
66**, followed by the stated conditional ordinary corollary at size72.
The fresh publication-path cold reproduction took 23.114519 seconds,
with peak parent RSS 13,892KiB and child/compiler RSS 117,424KiB.
These observed costs are not portable runtime guarantees.

All numerical-library threads are one and children run sequentially.
Each mathematical search or orbit case retains the 200,000-node,
ten-second guard. A guard, malformed input or mismatch gives INCOMPLETE
or an exception and supplies no overall proof verdict. The longest native
mapping fiber used 220 nodes in the pruned engine; literal mode enumerates
all 5,040 assignments per fiber, totaling 22,196,160 assignments.

Generated matrices, full mapping streams, joint-star corpora, binaries and
checkpoints stay in `.work`, or in the directory selected by
`CWC2111_PAIR_WORK`. Only source, eight compact inputs, source provenance
and the 73,928-byte coloring/summary certificate are published.
Both implementations and audits are by this researcher; independent peer
review is pending. The ordinary normalization and global-counting bridges
remain unformalized.
