# Independent review: core-branch line-graph signature bound

This directory independently reviews the universal theorem in
[`line_graph_signature_core_branch_bound`](https://github.com/helgithorskarp/math_results/tree/d425f7f0ef297d26c1dbcae5eb2fe2318dad84c0/graph_theory/line_graph_signature_core_branch_bound).

**Verdict: ACCEPT, high confidence.**  The proof is complete under its
stated hypotheses.  [REVIEW.md](REVIEW.md) enumerates the human premises,
tests the smallest adversarial cases, and distinguishes the universal proof
from finite corroboration.

The review also extracts the stronger bound

```text
s(L(G)) <= c(G)-1-delta(G),
delta(G)=eta(H)+|B(H) intersect R|+(-tau-|R|) >= 0,
```

using the contribution's own notation.  This gives a concrete sufficient
condition for the sharp conjecture and necessary conditions for equality in
the submitted `c-1` bound.

## Reproduce

CPython 3.11 or newer and the standard library suffice.

```bash
cd graph_theory/line_graph_signature_core_branch_bound_review1
PYTHONDONTWRITEBYTECODE=1 python3 verify_independent.py
PYTHONDONTWRITEBYTECODE=1 python3 -O verify_independent.py
sha256sum -c SHA256SUMS
```

The run takes several minutes on one CPU.  The checker uses exact rational
and integer arithmetic, no network input, floating point, randomness,
solver, or third-party package.

## Files

- `REVIEW.md`: verdict, premise audit, refinement, limitations.
- `verify_independent.py`: independent exact checker.
- `expected.json`: frozen checker result.
- `SOURCES.md`: primary sources and novelty boundary.
- `SHA256SUMS`: integrity manifest.
