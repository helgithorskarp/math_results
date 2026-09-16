# Full hendecagon spindle round: exact four-colour stop

This package decides one frozen bottom-up Hadwiger--Nelson construction.  It
does **not** produce a five-chromatic graph and does not improve the published
509-point record.

The source is the exact braced regular hendecagon in Shibuya's
`rigid_hendecagon()` construction.  That 41-point support uses four rotations
of a seven-point, 11-edge four-chromatic spindle.  Before any colouring test,
the construction here was frozen as its full cyclic completion: retain the
unit-side regular hendecagon and the two auxiliary points, and include all
eleven rotations of the same seven-point spindle under the displayed
`zeta_11^(-4)` action.  This is a single natural symmetry completion, not a
scan over rotation subsets or phases.

The declared cap route is already complete.  Its 90 formal addresses merge
exactly to **88 distinct physical points**.  Reconstructing every unit pair
gives **187 edges**.  The graph is connected and has no articulation vertex or
bridge, so the result is not explained by a separable one-point attachment.

## Complete-input decision

One seven-point spindle is distinguished as the source.  It is
four-chromatic and has exactly 16 proper four-colourings up to global colour
permutation.  On the same collision-merged 88-point complete unit graph:

```text
source colourings blocked       0
source colourings surviving    16
```

`certificate.json` contains a literal proper 88-vertex extension for every
canonical source colouring.  The verifier checks every word against all 187
physical unit edges.  Thus the completion is exactly four-chromatic and its
projection onto the complete source-colouring relation is universal.  It
fails the predeclared forcing gate and is retired without testing nearby
rotation subsets, phases, related polygons, or larger closures.

This is an exact scoped negative result, not a theorem about arbitrary braced
hendecagon compositions.

## Exact arithmetic and reproduction

All coordinates lie in the cyclotomic field `Q(q)`, where `q` is a primitive
66th root of unity.  `model.py` implements this field as rational polynomials
modulo `Phi_66`, of degree 20.  Coordinate equality, collision merging,
complex conjugation and squared-distance-one tests are exact rational
operations; there is no floating-point tolerance.

Only CPython 3.11+ and the standard library are required:

```sh
python3 -B verify.py
python3 -B controls.py
python3 -O -B verify.py
python3 -O -B controls.py
```

The controls test the cyclotomic relation, root-of-unity order, conjugation,
and rejection of corrupted colouring certificates.  `SHA256SUMS` pins all
files used by the verification.

## Evidence boundary

This is author-side reproducible evidence, not independent review and not a
formal proof-assistant artifact.  The source coordinate formulas come from
the MIT-licensed Shibuya project at pinned commit
[`218097c`](https://github.com/Parcly-Taxel/Shibuya/blob/218097c9971db2b60ab94a0b8dae20d76741cc43/shibuya/graphs/bracepoly.py#L123-L149).
The field formulas in this package are a self-contained exact translation of
that code followed by the one frozen full cyclic completion.

