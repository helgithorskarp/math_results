# Exact equal-pair gate for two small plane unit-distance sources

This package proves a compositional negative result for two exact physical
four-chromatic sources below the 255-point half-budget:

- the aligned 143-point heptagon–Moser sum; and
- every one of the 205 exact physical quotient graphs representing all
  rotations of the Golomb rotational self-sum, with orders 46–100.

For each graph, a finite list of proper four-colourings separates every two
distinct physical vertices. Hence **no pair is forced equal in every proper
four-colouring**. The same is true in every subgraph, by restricting the
separating colourings. None of these supports or their subgraphs can therefore
serve as a forced-equal half in the usual two-half spindle construction.

This does not rule out other terminal relations, unions with new cross edges,
larger assemblies, arbitrary supports, or a sub-509 five-chromatic graph. It
is a construction gate, not a global Hadwiger–Nelson bound. No five-chromatic
graph is produced.

## Exact physical scope

The heptagon–Moser graph is reconstructed in the exact degree-24 coordinate
field of its source package. It has 143 distinct points and 512 strict unit
edges. Fourteen saved rows distinguish all 143 vertex signatures.

For the Golomb source, the package reconstructs the complete exact
line–circle event census from the existing independent verifier. Collision
pairs are contracted before any colouring is interpreted, and unit pairs are
then mapped to the physical quotient. The 205 cases have orders 46–100 and
141–372 edges. In total, 2,902 saved rows are used, at most 22 for any case.
Every row is checked directly on every physical edge; signature uniqueness
checks all physical pairs, not a selected terminal list.

The exact source result proves that these 205 event graphs cover every unit
rotation, including the generic case and the conjugate roots of irreducible
quadratic events. This package imports that finite exact reconstruction rather
than restating its polynomial proof. Dependency byte hashes are fixed in both
the generator and verifier.

## Reproduce

The theorem checker uses Python 3.11 or later and the standard library only:

```sh
python3 verify.py
python3 -O verify.py
python3 controls.py
cmp <(python3 verify.py) expected.json
sha256sum -c SHA256SUMS
```

To regenerate the positive certificate, install the pinned optional solver in
an external virtual environment and write to a fresh path:

```sh
python3 -m venv /tmp/hn-small-equal-pair-env
/tmp/hn-small-equal-pair-env/bin/pip install -r requirements.txt
/tmp/hn-small-equal-pair-env/bin/python build_certificate.py \
  --output /tmp/hn-small-equal-pair-certificate.json
cmp /tmp/hn-small-equal-pair-certificate.json certificate.json
```

CaDiCaL is used only to discover colour rows. Soundness of a SAT status is not
a theorem premise: the standard-library verifier reconstructs the exact
graphs, checks every saved word directly, and proves separation by comparing
the complete colour signatures. Four malformed-certificate controls are
rejected.

## Construction consequence and provenance

If a four-colourable graph has marked vertices forced equal, two suitably
placed copies can contradict a unit bridge between their other marked
vertices. To fit below 509 without additional overlaps, such a half must have
at most 254 vertices. Both sources here were therefore credible small-gadget
candidates; the separating bases close that particular mechanism.

The exact geometry and all-rotation reduction are inherited from the sibling
packages `hadwiger_nelson_heptagon_moser_sum` and
`hadwiger_nelson_golomb_rotation_sum`. Their own theorem scopes remain
unchanged. The current smallest published five-chromatic plane unit-distance
comparison remains Parts' 509-vertex graph; this package does not improve it.

The broader floating search that motivated this gate—including EI17 circle
completion and one-collision H21 assemblies—is deliberately omitted because
it is not exact evidence. No claim about those numerical families is made
here. Author-side verification is complete; independent external review is
pending.

The Discovery Net receipt is recorded in `DISCOVERY_RECEIPT.json`. The stale
ledger did not index the contribution: it is accepted for broadcast, not
committed, and must not be resubmitted solely because it remains absent.
