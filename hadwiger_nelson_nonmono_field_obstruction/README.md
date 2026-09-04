# Field obstruction closes the two-overlap Parts gadget route

**Every two-overlap composition of Parts' archived 159- and 214-vertex
nonmonochromatic gadgets is four-colorable, with no denominator restriction.**
The same holds for any number of these gadgets added successively with at
least two overlaps per addition.

Their complex coordinates lie in `E = Q(sqrt(-3),sqrt(-11))`. A classical
residue-field coloring mechanism, described by David Speyer in Polymath16,
extends to an explicit four-coloring of all of `E`. Two overlaps force both
the orthogonal multiplier and translation of a placed gadget into `E`.
[PROOF.md](PROOF.md) gives a self-contained proof, including nonintegral
2-adic coordinates and a finite integer algorithm for the coloring.

This subsumes the earlier 159/159, 159/214, and 214/214 two-overlap censuses,
whose sizes total 8,216,200 placements. The theorem does not depend on those
counts. No graph improving the 509-vertex record is produced. Higher
denominators in this family cannot produce one; future constructions must
escape the field obstruction, for example by allowing at most one overlap.

The method itself is prior work; no novelty claim is made for residue-field
coloring. The contribution is its explicit implementation and application to
the research team's entire two-overlap gadget route.

## Verify

From this directory, with Python 3.11 or later:

```bash
python3 verify.py > /tmp/parts-field-check.json
cmp expected.json /tmp/parts-field-check.json
sha256sum -c SHA256SUMS
```

Only the Python standard library is needed. `verify.py` checks:

- compatible lifts of `sqrt(33)` through 80 binary digits;
- 625 exact unit translations, including points with even denominators,
  and 3,750 changes of coefficient representation;
- membership of all 373 archived points in the claimed field, the 646 and
  977 strict component edges, and the explicit coloring on every edge;
- eight mixed placement samples, covering rotations and reflections with
  denominators 1, 2, 6, and 12, rebuilding every strict unit edge;
- the seven-point, eleven-edge Moser spindle and all 2,187 three-color
  assignments, which certify the lower bound four for this field.

`coloring.py` contains the general rational-coordinate algorithm. The sample
geometry checker uses the separate coefficient equation for squared distance
rather than calling the field multiplication routine. No SAT solver or
floating-point decision is used.

## Inputs, provenance, and trust

The two small coordinate inputs are reused from
`../hadwiger_nelson_nonmono159_214_lowden2/points159.tsv` and `points214.tsv`.
Their provenance is recorded in that directory's `SOURCE.md`, and both are
pinned here by SHA-256. The eight transforms in `samples.json` were selected
from the earlier mixed overlap-at-least-20 artifact; they are supplementary
checks, not a completeness certificate for the infinite theorem.

The proof's trust boundary is ordinary, unformalized mathematics, including
the explicit binary lifting construction and the parity norm argument.
Finite checks trust CPython's arbitrary-precision integers and `Fraction`,
plus the pinned coordinate transcription. No large generated files or
external solver artifacts are required. Tested with CPython 3.11.2.

For primary sources and exact attribution, see the final section of
[PROOF.md](PROOF.md). The record benchmark remains the Parts 509-vertex graph,
also identified in the introduction to
[Haugland's August 2026 paper](https://arxiv.org/html/2608.04542v4).
