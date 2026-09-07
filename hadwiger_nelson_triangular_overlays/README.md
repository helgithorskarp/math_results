# Every pair of intersecting unit triangular lattices is four-colourable

An elementary residue argument colours the entire union of two unit
triangular lattices sharing a vertex, for **every** relative rotation. The
bound four is sharp, witnessed by the classical Moser spindle.

The exact computational gate takes the 253-point triangular patch
`P={a+b omega : a^2+ab+b^2<=67}`, where `omega=(1+i sqrt(3))/2`, and all
rotations `P union alpha P`. Every member has at most 505 vertices.

- There are 1,746 exceptional rotations: 1,350 give chromatic number three
  and 396 give chromatic number four.
- Every other rotation gives a 505-vertex, 1,404-edge three-chromatic graph.
- The independent checker evaluates 71,818,098 exact cross-pair norms and
  reconstructs all edges and coincidences.

These are rotation counts, not isomorphism-class counts. **No record
improvement was found.** The full theorem also closes every finite subset
of two intersecting unit triangular lattices, with no patch-size bound.

Read [PROOF.md](PROOF.md) for the proof, full census, completeness argument,
and exact scope. [EXPECTED.json](EXPECTED.json) gives compact expected
output; [VALIDATION.json](VALIDATION.json) records validation provenance.

## Reproduce

CPython 3.11.2, standard library only. From the repository root:

```sh
python3 hadwiger_nelson_triangular_overlays/produce.py --work /tmp/hn-triangular-overlays
python3 hadwiger_nelson_triangular_overlays/verify.py --work /tmp/hn-triangular-overlays
python3 hadwiger_nelson_triangular_overlays/controls.py --work /tmp/hn-triangular-overlays
```

The producer takes about half a second; the independent audit took 26–55
seconds in the recorded runs on a shared machine. The generated catalog is 459,196 bytes;
it and the run outputs stay outside the repository. Its SHA-256 is

```
92b06d19628c1da21472875ee22103888cdd01af4655258fb20e98219324a66b
```

The catalog has no external inputs and is regenerated from the definition.
The verifier imports no producer code and checks a Cartesian representation
with rational root parametrization and complete norm comparisons. Eighteen
deliberate corruptions are rejected. The seven-vertex sharpness benchmark
is checked against every assignment of three or four colours.

The all-lattice theorem is proved directly in the text; only the finite
census and its propagation witness depend on code. There is no solver,
floating-point, private-data, or externally imported certificate premise.
