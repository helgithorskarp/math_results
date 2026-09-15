# Exact closure of the two-distance carrier by all unit lenses

## Result

Let `P` be the certified 114-point two-distance graph from
`hadwiger_nelson_weighted_rotation_residue_obstruction`: 379 pairs have
squared distance 1 and 156 pairs have squared distance `4/3`, and the graph
using both classes is five-chromatic.  For every `4/3` pair `p,q`, this package
adds both intersections of the unit circles centred at `p` and `q`:

```text
(p+q)/2 +/- (sqrt(2)/2) R_90(q-p).
```

Exact collision merging gives **426 distinct plane points**.  Reconstructing
all pairs gives **1,499 strict unit edges**: 379 source--source, 624
source--lens, and 496 lens--lens edges.  Thus this is a substantially coupled
whole support, not just 312 degree-two additions.

The complete physical graph nevertheless has chromatic number exactly four.
The supplied 426-digit word proves the upper bound.  The lower bound is already
carried by a seven-point, eleven-edge induced core on physical vertex indices
`236,240,326,327,328,397,399`; the checker exhausts its `3^7` colour words.

More sharply, for **each of the 156 original `4/3` pairs individually**, the
package supplies and checks a proper four-colouring in which that pair's two
source endpoints have the same colour.  So the all-lenses operation does not
even turn any one missing carrier edge into an unconditional four-colour
inequality.  This statement does not assert that every simultaneous pattern,
or every four-colouring of the 379-edge source unit graph, extends.

This is a scoped exact stop, not a five-chromatic unit-distance construction
and not progress on the 509-vertex record.

## A second cheap normalization stop

A plane Möbius map changes distances by

```text
|f(p)-f(q)| = C |p-q| / (r_p r_q),
```

where `r_p` is the distance from `p` to the pole (with the affine case obtained
as a limit).  Normalizing all carrier edges would therefore require
`r_p^2 r_q^2 = K |p-q|^2`.  Carrier cycle
`63--0--62--94--63` has squared-distance labels `1,1,4/3,1` in order.
Alternating the four product equations gives both
`r_63^2/r_62^2=1` and `r_63^2/r_62^2=3/4`, a contradiction.  The checker
reconstructs this exact labelled cycle.  This only excludes a single global
Möbius normalization of this fixed carrier.

## Reproduction

From this directory, Python 3.11 or later suffices to check the exact field
arithmetic, collision merge, complete all-pairs edge reconstruction, the
four-colour word, all 156 equality-extension words, and the seven-point
non-three core:

```bash
python3 -B verify.py
python3 -B controls.py
```

To emit the exact coordinates, complete edge list and ordinary three-colour
CNF into a new scratch directory:

```bash
python3 -B verify.py --emit-dir /tmp/hn-lens-closure
```

The coordinate format has eight rational coefficients for each Cartesian
coordinate, in the basis indexed by products of `sqrt(2)`, `sqrt(3)` and
`sqrt(11)`.  Generated bulk files are deliberately not committed.

Any DIMACS solver that returns a standard `v`-line model and exit status 10 can
regenerate alternative checked positive witnesses:

```bash
python3 -B certify.py --solver /path/to/kissat --output /tmp/certificate.json
```

The SAT solver is not trusted by `verify.py`; only the explicit positive words
are retained.  The non-three lower bound is checked directly without a solver
or proof-trace checker.
