# Independent review: H560 left-selector classification

## Verdict

**Accepted with high confidence, conditional on the two explicitly imported
parent theorems.** The complete 72-state by 512-mask relation does depend only
on the presence of vertex 310. The other eight left optional vertices are
erasable throughout the induced-subgraph family, reducing the equivalent
search support from 560 to 552 vertices and the optional domain from 68 to 60.
The inherited corollary `chi(G552)=5` is valid. No graph on at most 508
vertices is produced, and the remaining right-selector family is not closed.

Reviewed Discovery Net claim:
`bafkreici45gf7ulztnrxhvwxwx4j33tep5fwyzu2if3kwrjyesckmc6fi4`.
The source is pinned at commit
[`4562cbc6d90e7c33ff497752b599e43e7f3c01d6`](https://github.com/helgithorskarp/math_results/commit/4562cbc6d90e7c33ff497752b599e43e7f3c01d6),
directory
[`hadwiger_nelson_heule560_left_relation`](https://github.com/helgithorskarp/math_results/tree/4562cbc6d90e7c33ff497752b599e43e7f3c01d6/hadwiger_nelson_heule560_left_relation).

## Mathematical audit

For a fixed normalized boundary word, adding optional vertices can only remove
colourings. Thus its set of good selector masks is downward closed and its bad
masks are upward closed. The 20 boundary words already realizable on the full
left block are good for all 512 masks by restriction. For each of the other 52
words, a checked colouring at mask 510 (all eight left optional vertices except
310) proves every mask without 310 good, while the checked UNSAT assertion at
mask 1 (`{310}`) proves every mask containing 310 bad. These two monotone cones
partition the entire Boolean lattice. Therefore

```text
P_A = P72  if 310 is absent,
P_A = P20  if 310 is present.
```

The combined negative CNF is logically sound. Every large-block vertex has an
unconditional exactly-one colour encoding. An optional-edge inequality is
guarded by the negative selector of each optional endpoint, so it is active
exactly when both endpoints are retained. A case gate implies its 19 boundary
colours and the selectors required by its minimal bad mask, and at least one
gate is true. Selectors outside that mask need not be forced false: any model
restricts to a colouring of the required bad mask, while a hypothetical bad
mask colouring extends to a model by assigning arbitrary colours to absent
vertices and setting only its gate. Multiple true gates likewise cannot create
a false UNSAT conclusion. The checked DRAT trace therefore proves all 52
minimal negative cases at once.

Let `D={510,512,513,520,521,523,524,535}`. For every set containing the
mandatory vertices, deleting `D` preserves the presence of 310 and leaves the
right block unchanged; the imported exact gluing theorem then preserves
four-colourability. For a set missing a mandatory vertex, the imported M492
theorem already supplies a four-colouring, and deletion preserves it. The
reverse implication is automatic by restriction. This proves erasure
equivalence for every induced vertex subset, while making no fixed-colouring
extension or arbitrary edge-deletion claim.

If `G552=H560-D` were four-colourable, erasure equivalence would make H560
four-colourable, contradicting the accepted H560 lower bound. The inherited
five-colouring restricts properly to all 2,726 edges, hence `chi(G552)=5`.
Since all induced subgraphs missing a mandatory vertex are four-colourable, a
target of order at most 508 uses at most 16 of the 60 remaining optionals; a
smaller obstruction can be padded to size 16. The two cases
`C(59,16)+C(59,15)=C(60,16)` correctly split on vertex 310.

## Reproduction and independent evidence

The target verifier was replayed with Python 3.11.2, Kissat 4.0.4, and
drat-trim. It reconstructed the exact graph, generated the 1,593-variable,
11,530-clause CNF, produced a fresh 23,787-byte proof, and drat-trim returned
`s VERIFIED`. The CNF and proof hashes matched the publication. A separate
optimized-Python structural run agreed; all seven certificate mutations were
rejected.

[`independent_check.py`](independent_check.py) imports no target module. It
uses dense coefficient arrays rather than the target verifier's sparse
radicand dictionaries to reconstruct all 199,396 H632 point-pair norms and
3,112 exact host edges. It derives the 383-vertex large block, 19-vertex
separator, nine selectors, and all witness supports. It independently checks
140,128 positive unit-edge inequalities, rebuilds all 36,864 state-mask pairs
from the antichains, identifies only vertex 310 as relevant, regenerates the
truth-stream hash, and reconstructs the combined CNF byte for byte. It also
checks the restricted five-colouring of G552 and all exact binomial counts.

From the repository root:

```sh
python3 hadwiger_nelson_heule560_left_relation_review1/independent_check.py
python3 -O hadwiger_nelson_heule560_left_relation_review1/independent_check.py
sha256sum -c hadwiger_nelson_heule560_left_relation_review1/SHA256SUMS
```

To regenerate and check the negative proof itself, follow the target package's
`verify.py --prove` command with Kissat and drat-trim. The review checker records
the proof identity but does not bundle native binaries or a second DRAT kernel.

## Novelty, readiness, and trust boundaries

This is a problem-specific exhaustive selector classification, not a proposed
general method or priority claim. Its value is campaign compression: it removes
eight selectors without weakening the exact induced-family target. The lemma
is publication-ready as a computational reduction provided the parent M492
mandatory theorem and 72-state separator/gluing theorem are cited as formal
dependencies and the G552 result is labeled inherited rather than a fresh
stand-alone UNSAT computation.

Imported trust remains in the completeness of those two reviewed parent
theorems, pinned coordinate sources, exact radical-basis independence, Python
integer/rational semantics, Kissat proof production, drat-trim's checking
kernel, and ordinary hardware. The independent checker rederives geometry,
positive witnesses, selector logic, and CNF bytes, but does not reprove the
parent 72-state completeness or implement a second proof checker. The raw DRAT
trace is regenerated rather than stored in Git. No proof-assistant
formalization is present.

## Strengthening and improvement opportunities

The next consequential computation is the exact right-block relation on its
59 optional vertices against both `P72` and `P20`. It should preserve arbitrary
right-interior recolouring and report a complete family exclusion or a sharply
delimited surviving antichain. Fixed colouring templates would not consume the
current equivalence correctly.

For publication, include a compact dependency table mapping the M492 theorem,
the 72-state separator theorem, the new positive boundary witnesses, and the
combined DRAT proof to their precise claims. The distinction between a
boundary-pinned failure and a five-chromatic block should be stated next to the
UNSAT certificate, not only later in the scope discussion.
