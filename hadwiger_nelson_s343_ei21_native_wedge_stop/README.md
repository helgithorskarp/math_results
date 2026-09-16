# The native S343--EI21 mixed support is a one-vertex four-colourable sum

This package decides one exact mixed-source whole composition for the strict
Hadwiger--Nelson sub-509 construction campaign.  Place the independently
reviewed 343-point opposed-B214 support and the independently reviewed
21-point EI21 contact source in their displayed native coordinate frames.
Their origins coincide; no additional rotation, reflection, translation,
phase, or parameter is introduced.

The complete collision-merged support has **363 distinct physical points**
and **1,821 strict unit edges**.  The origin is its unique mixed attachment:
there is no collision and no unit edge between any of the 342 private S343
points and the 20 private EI21 points.  Deleting the origin separates
components of orders 342 and 20.  A checked proper four-colour word, together
with the embedded Golomb graph, proves that the complete graph has chromatic
number exactly four.

This is therefore the separability stop required by the frozen one-placement
allocation.  It is not a five-chromatic graph, not a record candidate, and not
a theorem about other S343--EI21 placements.  In particular it does not
license rotations, translations, contact alignments, source deletions, lens
completions, EI21 flex roots, or nearby mixed-source variants.

## Exact verification

S343 is reconstructed exactly in the basis
`1,sqrt(3),sqrt(11),sqrt(33)` at denominator 36.  EI21 is reconstructed from
the published rational contraction certificate: its coordinates are the
unique real root inside an infinity box of radius `10^-25` about the supplied
rational midpoint.

The verifier uses outward rational enclosures for `sqrt(3)`, `sqrt(11)`, and
`sqrt(33)`.  It checks all **6,840** private cross pairs and proves that every
squared-distance interval excludes both zero and one.  The source verifiers
reconstruct all 58,653 S343 pairs and all 210 EI21 pairs.  Thus the proof
partitions and decides all

```text
binom(363,2) = 58,653 + 210 + 6,840 = 65,703
```

physical pairs.  The source positive words are palette-aligned at the common
origin and concatenated; the resulting 363-character word is checked on the
canonical 1,821-edge stream.  A direct `3^7` normalized census rejects every
three-colouring of the embedded ten-point Golomb graph.

## Reproduction

From the repository root, using CPython 3.11 or later and only the standard
library:

```sh
python3 -B hadwiger_nelson_s343_ei21_native_wedge_stop/verify.py
python3 -O -B hadwiger_nelson_s343_ei21_native_wedge_stop/verify.py
(cd hadwiger_nelson_s343_ei21_native_wedge_stop && python3 -B controls.py)
(cd hadwiger_nelson_s343_ei21_native_wedge_stop && sha256sum -c SHA256SUMS)
```

The source files and certificates are hash-pinned before import.  No SAT
solver, floating-point predicate, omitted trace, or numerical root finder is
used.  The exact interval reduction and Python's integer/Fraction semantics
remain trust boundaries.  This is author-side exact evidence; it is not an
independent review of the already reviewed source packages.
