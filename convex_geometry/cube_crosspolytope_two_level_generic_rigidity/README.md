# Arbitrary-q rigidity of two-level resonances

This directory proves that every isolated missing wall for two-level active
weights \(1^p a^r\), \(0<a<1\), comes from a simple pole.

If a unit-supplier row and an \(a\)-supplier row resonate with common
residual pole multiplicity \(m\geq2\), cancellation of their leading hinge
coefficient always leaves a nonzero next coefficient.  More precisely, the
difference of their normalized next coefficients is

\[
-\frac{(m-1)\{q(1+a)^2-4a(i+\ell)\}}
{4X(q-m+1)(1+a)}<0.
\]

Consequently an isolated two-level wall disappears exactly when \(m=1\),
the earlier parity obstruction holds, the resonance has positive boundary,
and the explicit magnitude equation in [PROOF.md](PROOF.md) holds.  This is
an arbitrary-dimensional classification of collision-free cross-family
walls.  Special multirow subset-sum collisions are outside its scope.

## Reproduce

The independent checker needs only CPython 3.11 or later:

~~~sh
PYTHONDONTWRITEBYTECODE=1 python3 verify.py > actual-verification.json
diff -u EXPECTED_VERIFICATION.json actual-verification.json
~~~

The symbolic derivation pins SymPy 1.13.3:

~~~sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python derive.py > actual-derivation.json
diff -u EXPECTED_DERIVATION.json actual-derivation.json
sha256sum -c SHA256SUMS
~~~

Expected statuses are `TWO_LEVEL_GENERIC_RIGIDITY_VERIFIED` and
`TWO_LEVEL_GENERIC_RIGIDITY_DERIVED`.

The canonical output SHA-256 values are respectively
`337fa967c974f43e8e7fe5cc637d06aa4c7c7f41c56d05f7852b3b5e40a54c11`
and
`7c15b6ba693c9a8530032809b619414ceeeaee992974ac5d90d5345737e167da`.
