# The full difference body of the O'Donnell 15-point core is three-chromatic

This package exactly decides one source-new, cap-feasible Hadwiger--Nelson
construction.  Let `S` be the 15-point pentagonal core used in Paul
O'Donnell's 40-vertex unit-distance construction, in the exact realization
serialized in `certificate.json`.  Form the complete oriented difference body

`D = S-S = {p-q : p,q in S}`.

Exact collision merging leaves **171 distinct physical points**.  Complete
all-pairs reconstruction gives **560 unit edges**.  The graph is connected,
has no articulation vertex or bridge, and its degree-4 core is all 171
vertices.  Thus the operation is genuinely nonseparable and globally coupled,
not a one-point wedge or a union of independent gadgets.

Nevertheless, the complete strict unit graph is **exactly three-chromatic**.
The certificate contains a proper three-colour word and the explicit unit
5-cycle `0-4-14-21-38-0`.  A four-colour word therefore also exists, so this
graph is not a five-chromatic candidate and does not improve the 509-point
record.

## Exactness

Coordinates are coefficient vectors in `Q(t)`, where

`25 t^8 - 75 t^6 - 140 t^4 - 55 t^2 + 1 = 0`

and `t` is the unique root in
`[2.095109707686927, 2.095109707686928]`.  Rational interval arithmetic checks
that this interval isolates one root.  For every pair of physical points, the
verifier reduces the squared distance modulo the displayed polynomial and
then:

- recognizes a unit edge when the reduced polynomial is identically zero;
- rigorously excludes zero for every other squared-distance-minus-one
  polynomial on the root interval; and
- rigorously excludes zero squared distance between every two serialized
  physical points.

Accordingly all 14,535 unordered physical pairs are decided, not sampled.

## Reproduction

Only Python's standard library is required.

```bash
python3 verify.py
python3 controls.py
```

`produce.py --output certificate.json` regenerates the collision quotient,
complete graph, colour words, connectivity data and hashes.  `verify.py`
reconstructs them from the coordinate certificate and independently checks
the rational root/interval obligations.  `controls.py` confirms rejection of
four representative corruptions.

## Scope

This is a single exact negative construction boundary.  It closes only the
full oriented difference body of the displayed 15-point realization.  It does
not classify other O'Donnell graphs, alternate realizations, selected sums or
differences, rotated copies, enlargements, or arbitrary pentagonal sources.
The source and operation are retired here without an adjacent sweep.

