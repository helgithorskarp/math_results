# Degree-nine complex first-power gap through 7/10

six-sendov-1 / researcher. Ordinary author proof, unformalized and
independently unreviewed as a new child.

For every complex degree-nine polynomial with all nine original zeros
in the closed unit disk, every marked zero satisfying
`11/16 <= |a| <= 7/10` has

    sum_(all eight critical multiplicities) 1/|a-zeta_j| > 8+1/10000.

Collisions give infinity. Both marked endpoints and arbitrary complex
directions and multiplicities are included. The adjacent assertion uses
no previous numerical exclusion as a premise.

The union `F>8+1/10000` on closed `[2/3,7/10]` explicitly uses10322 and
10300 for the older bands; strict `F>8` throughout `|a|<=7/10` additionally
uses10240. There is no numerical uniform whole-lower-disk gap, global
FIRST theorem, sharp radius or optimized gap. Independent review10334
confirmed the earlier10322 annulus and improved its gap to1/8800; that
verdict does not review this child.

[PROOF.md](PROOF.md) supplies the full ordinary analytic argument.
[LITERATURE.md](LITERATURE.md) credits published generic inputs and prior
methods. In particular the high-order contour coefficients are published
Roos/Han--Niles-Weed prior art, not a new generic theorem here.

Copy this whole compact directory and use CPython3.11+ (tested3.12.14):

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B verify.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B -O verify.py
python3 -I -B validate.py --private-dir /tmp/sendov-seven-tenths-validation
```

The validator sets all six native thread settings1 for each child, runs
one serial child at a time and uses a fixed45-second per-child guard.
Timeout, memory failure or incomplete validation is not a mathematical
rejection or proof of nonexistence. No external package or solver is needed.

The default checker verifies whole local source pins BEFORE importing any
mathematical helper, parses exact compact input schemas, and recomputes
every complete defining coefficient/control representation before any
minimum, hash or whole expected fixture comparison. ValueError gates
remain active under optimized Python. Source/manifest/fixture validation
provides reproducibility controls, not a formalization or independent review.

Complete data:76 initial closed entry shells,16 cuts,92 rectangles/108
nodes;156 face cuts,157 closed leaves/313 nodes/depth13. Defining roles
are141 retained-mean origin,15 joint-energy polar,1 standard polar.
Both282 whole mean channels retain all seven orders,1974 full9x10
matrices,282 full10x10 cleared matrices and every degree8/9 control;
all15 joint13x19 matrices and93 standard polar vectors are recomputed.
Fresh physical homothety, both literal endpoints and complete formal
clipping path/convex norm controls are included.

Compact [EXPECTED.json](EXPECTED.json) records exact counts and the entire
regenerated mathematical-record hash. [MANIFEST.json](MANIFEST.json)
pins every source/input byte; [VALIDATION.json](VALIDATION.json) records
actual full local/cold normal/optimized positives and specific semantic,
entry, face, fixture and source rejection gates. The full approximately
8.7MB coefficient record is regenerated, never shipped. Optional
`--record /tmp/seven-tenths-record.json` writes it outside this source.
The explicit author-generation route `--emit` bypasses source/expected
pins; it is not production verification.

Communication identities, Gauss--Lucas, Hermite interpolation, mean and
Bernstein inequalities, affine disk contraction, clipping differentiation
and the external REAL Hilbert Banach norm identity are ordinary analytic
trust boundaries written in the proof. The finite checker tests their
exact algebraic representations and closed coverage, not those theorems
in a proof assistant. No ancestor/private/reviewer executable, record,
tree or expected fixture is a runtime input.
