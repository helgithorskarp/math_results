# Generic wall count and exact smoothness

This directory strengthens the global weighted ray-chamber formula for
cube--crosspolytope sections.  Under an explicit nonresonance condition, every
labeled candidate wall is genuine.  With `q` nonzero normal coordinates there
are exactly

\[
q\,2^{q-1}
\]

walls.  At each wall the delta-normalized section is exactly
\(C^{q-2}\), not \(C^{q-1}\), and the first derivative jump has a closed
nonzero product formula.  For `q = 1` the corresponding statement is a jump
in the section value.

The nonresonance condition is generic: its complement is a finite union of
proper algebraic hypersurfaces in every normalized parameter chart.  Thus the
classification holds on an open dense full-measure set of ray-side normals
and offsets.

See [PROOF.md](PROOF.md) for the theorem and proof.

## Reproduce

Using CPython 3.11 or later and only its standard library:

~~~sh
PYTHONDONTWRITEBYTECODE=1 python3 verify.py > actual.json
diff -u EXPECTED.json actual.json
PYTHONDONTWRITEBYTECODE=1 python3 -O verify.py > actual-optimized.json
diff -u EXPECTED.json actual-optimized.json
sha256sum -c SHA256SUMS
~~~

Expected status: `GENERIC_WALL_SMOOTHNESS_VERIFIED`.
Expected canonical-output SHA-256:
`ce74a664e41646b529c32eec8270cb159df6e2071999af9ea30c122a8fd8a926`.

The checker uses exact rational arithmetic.  It verifies the closed jump
coefficient at every one of 1,793 nonresonant labeled walls through eight
active coordinates.  An independent rational polygon engine reconstructs the
original 27-halfspace body and checks 33 walls for dense, signed, scaled, and
sparse three-dimensional normals.

See [SOURCES.md](SOURCES.md) for dependencies, literature, and the trust
boundary.
