# Complete q=3 missing-wall classification

This directory classifies every disappearing positive chamber candidate for a
cube--crosspolytope section with three pairwise distinct active normal weights.

The classification has three parts:

- a numerical wall is genuine exactly when the sum of its labeled derivative
  jumps is nonzero;
- every two-label disappearance belongs to one of four explicit rational
  one-parameter normal forms, with three isolated third-label exclusions;
- every three-label disappearance is one of two isolated algebraic orbits,
  up to coordinate permutation.

See [PROOF.md](PROOF.md) for the theorem and exact normal forms.

## Reproduce

The independent verifier uses CPython 3.11 or later and only the standard
library:

~~~sh
PYTHONDONTWRITEBYTECODE=1 python3 verify.py > actual-verification.json
diff -u EXPECTED_VERIFICATION.json actual-verification.json
~~~

The exhaustive symbolic derivation pins SymPy 1.13.3:

~~~sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python derive.py > actual-derivation.json
diff -u EXPECTED_DERIVATION.json actual-derivation.json
sha256sum -c SHA256SUMS
~~~

Expected statuses are `Q3_MISSING_WALL_CLASSIFICATION_VERIFIED` and
`Q3_MISSING_WALL_CLASSIFICATION_DERIVED`.
The canonical output SHA-256 values are respectively
`a4c4820c96a7f9bc0bf0ad62cd9d65fd370a3d618560e8d4355967959d86e968` and
`9e1416a2702df7ced6b81cad39783e09cd5ed25e7ded5f505d273945b687f138`.

The derivation performs exact subresultant elimination over
`QQ[a,b]` for all 64 possible three-label tail patterns.  The independent
checker uses integer Sturm sequences and rational interval arithmetic, tests
269 rational instances of the four two-label normal forms, and reconstructs
the original 27-halfspace polygon on both sides of four representative walls.
It also checks three exact polynomial divisibility certificates connecting the
isolated-root formulas to the remaining collision equation after the displayed
formula for (B) enforces the first one.

See [SOURCES.md](SOURCES.md) for dependencies, literature, novelty scope, and
the trust boundary.
