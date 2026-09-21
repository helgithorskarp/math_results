# Bipartite parity sharpens clean-angulation reconstruction

For a clean bipartite `p`-angulation (`p` even), this directory proves the
exact face-defect identity

```text
(p+2)r-t = (1/2) sum_i (ell_i-(p+2)).
```

Here an alternative orientable rotation system has genus `h+r`, loses `t`
reference faces, and has non-reference face lengths `ell_i`. Consequently

```text
2r+1 <= t <= (p+2)r,
```

with equality on the right exactly when all new faces have length `p+2`.
Combining this parity gap with the existing missing-face decoder improves its
enumeration exponent from `2(p+1)r` to `(p+2)r`. In particular, clean
bipartite quadrangulations have `t <= 6r`, rather than the general `t <= 10r`.

The result is a structural theorem, not an inference from the computation.
`verify.py` independently enumerates all 256 labelled orientable rotation
systems of the cube. Direct face tracing verifies bipartite face parity, the
new identity, the equality case, and the complete `(r,t,face-length)` profile.

## Reproduce

Python 3.11 or later; standard library only:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 verify.py | diff -u EXPECTED_OUTPUT.json -
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v
sha256sum -c SHA256SUMS
```

## Files

- `THEOREM.md`: statement, proof, decoder consequence, literature boundary.
- `verify.py`: definition-level exact cube audit.
- `test_verify.py`: regression and rejection tests.
- `EXPECTED_OUTPUT.json`: frozen canonical audit output.
- `SHA256SUMS`: source manifest.

## Scope and trust boundary

The universal proof uses Euler's formula, parity of closed walks in a
bipartite graph, and the already stated clean-angulation reconstruction
argument. The checker audits conventions and boundary cases only. It uses no
solver, randomness, floating point, external data, or third-party package.
Embeddings are labelled rotation systems; graph automorphisms are not divided
out, and global reversal is counted separately.
