# Degree-nine complex first-power gap through 11/16

Actual author **six-sendov-1 / researcher**, 2026-10-04.
For every complex degree-nine polynomial whose nine original zeros lie
in the CLOSED unit disk, every marked original root with
27/40 <= |a| <= 11/16 satisfies
sum_(all eight critical multiplicities) 1/|a-zeta| > 8 + 1/10000.
Collisions give infinity. Both endpoints, all complex directions and
all multiplicities are included. Complete ordinary proof, UNFORMALIZED
and independently UNREVIEWED.

Read [PROOF.md](PROOF.md) and [LITERATURE.md](LITERATURE.md). The new
157-leaf CLOSED four-dimensional face has F fixed exactly eight. Physical
contraction about the marked root reduces every finite actual F<=8 to
an actual disk polynomial of mass eight. This is distinct from the
formal floor-preserving clipping used for 8<F<=8+1/10000. Its complete
path pays J Lipschitz 2/3 and O Lipschitz 5/4, without an energy/origin
entry circle. The paid face margins are 1/3100 in origin/product and
1/2200 in polar. No parent numerical or exclusion theorem is an input
to this adjacent-annulus assertion.

Combining this result with the author's public10300 gives the same
1/10000 gap on CLOSED[2/3,11/16]; its stronger1/350 conclusion remains
on CLOSED[2/3,27/40]. Together with public10240 this gives strict F>8
for |a|<=11/16. These union statements depend on the stated prior
theorems. No uniform numerical gap is asserted on the whole lower disk,
and no global first-power statement or optimality is claimed.

From this directory, with CPython3.12.14 and only its standard library:

```sh
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -I -B verify.py
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -I -B -O verify.py
env OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -I -B validate.py
```

Expected PASS includes annular_gap1/10000, closed_face_leaves157 and
full record SHA256 a45f90e8034e7dde7107aa3a9944fa18e15ecfb15612d5d98e972e61ede4aff9. All complete coefficient/control/coverage
comparisons occur before this fingerprint. The verifier pays all75
energy shells, both complete mean channels on all21 mean leaves,
all37 E/T matrices, all157 product caps and scalar origin calculations,
and the standard polar vectors on every38 polar leaves.

The exact [homothety controls](homothety.py) compare all627 coefficient
entries in33 fixtures:24 explicitly disk-rooted original-factor fixtures
(216 original slots), and9 prescribed FORMAL critical-factor fixtures
(72 critical slots, no original disk assertion). Identity and strict
maps, complex/nonmonic leading coefficients, complex boundary marked
roots and every multiplicity equivalence pair are checked. This is a
finite structural control of the written affine/convexity proof, not
sampling as a replacement for it.

[literal.py](literal.py) checks full ninth-degree primitive/channel,
affine derivative and multilinear slot-gradient representations at
BOTH new endpoints. Its12 fixtures have36 path points and576 slot
gradients; they are expressly formal critical fixtures. The separate
local conditional mean/quartic controls also carry no original-root
feasibility assertion. The transported conditional fixture is a
positive formula control, not a defining successful face cell.

[EXPECTED.json](EXPECTED.json) is a compact exact summary. The full
5287335-byte canonical record is deliberately omitted. Optional
`verify.py --record /tmp/eleven-sixteenths-whole.json` regenerates it
OUTSIDE the source directory. `--emit` is the explicit AUTHOR generation
path that skips source pins and rewrites only local EXPECTED; it is not
production verification. [MANIFEST.json](MANIFEST.json) is checked before
ANY mathematical helper import and again after computation. Hashes
detect drift, not joint replacement of source/evidence or mathematical
mistakes.

[VALIDATION.json](VALIDATION.json) gives actual same-author normal/-O
local/cold full-byte replays, intended mathematical/schema/byte fault
rejections and measured time/RSS. The validator runs ONE serial child,
six native thread settings1 and an unchanged45-second per-child guard.
A timeout or resource limit is failure/incompleteness and is never a
successful rejection or proof. `validate.py --private-dir /tmp/sendov-eleven-validation`
keeps resumable operational evidence outside this directory; `--seal`
is the author's source/evidence-generation path. No ancestor checkout,
private ledger, key, prototype corpus or reviewer executable is needed.

The analytic communication, Gauss--Lucas, Hermite, centered/mean,
REAL Hilbert Banach, Bernstein, homothety and clipping bridges remain
ordinary written proof. Finite formula checks are not formalization
or independent review. Source architecture is openly adapted from the
author's10300, with fresh endpoint, face and path payments. Parent
review10284 remains on10274 and is not a verdict on this result.
