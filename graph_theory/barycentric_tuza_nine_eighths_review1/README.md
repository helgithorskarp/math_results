# Independent review: 9/8 barycentric Tuza bound

This directory independently reviews
[`barycentric_tuza_nine_eighths`](https://github.com/helgithorskarp/math_results/tree/5b45335337fc3988dbddc016ca8b2b505beab7f5/graph_theory/barycentric_tuza_nine_eighths).

**Verdict: ACCEPT, high confidence.** The five signed-subcubic exceptions
are completely and correctly excluded: one would force a single boundary
edge, and the other four would normalize to nonorientable closed surfaces
below the sharp ten-facet minimum.

[REVIEW.md](REVIEW.md) enumerates every human premise, tests adversarial
small cases, separates finite corroboration from the universal proof, and
records three refinements: the Eulerian boundary obstruction, small closed
orientability, and the exact residue-sensitive ratio.

## Reproduce

CPython 3.11 or newer and the standard library suffice.

```bash
cd graph_theory/barycentric_tuza_nine_eighths_review1
PYTHONDONTWRITEBYTECODE=1 python3 verify_independent.py
PYTHONDONTWRITEBYTECODE=1 python3 -O verify_independent.py
sha256sum -c SHA256SUMS
```

The checker uses only exact finite-set and integer operations. It has no
solver, floating point, randomness, network input, third-party package,
external dataset, or omitted certificate.

## Files

- `REVIEW.md`: verdict, premise audit, refinements, limitations.
- `verify_independent.py`: independent exact checker.
- `expected.json`: frozen checker result.
- `SOURCES.md`: primary sources and dependency boundary.
- `SHA256SUMS`: integrity manifest.
