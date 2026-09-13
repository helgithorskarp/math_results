# Exact barrier for an averaged order-44 deletion-moment approach

**No good44 was constructed and no physical order-44 class was excluded.**
The first pass of the order-44 deletion-lift trial failed its terminal gate.
This package preserves an exact reason to stop the tested moment approach.

One rational seven-vertex density vector simultaneously satisfies the
specified necessary systems for the parent at order 44 and the average of
all 44 good43 deletion cards. It also satisfies the exact degree-support
identity for degrees 19..24. The point has 464 positive coordinates and
denominator `2622999999963278`.

The exact checker verifies 3,401 strict scalar inequalities, 117 positive-
definite matrices, all 2,624 positive leading principal minors, and zero
degree-identity residual. Thus no conic combination of these particular
constraints can prove good44 nonexistence. This is a certificate about a
relaxation, not about realizability of a deck or a graph.

[METHOD.md](METHOD.md) derives the common-density deletion identity,
finite overlap coefficients, integer support constraints, and claim
boundary. [DEPENDENCIES.md](DEPENDENCIES.md) records provenance and the
graph/repository audit. No symmetry, degree profile, packing, selected
deletion type, or incomplete catalogue of known42 graphs is imposed.

## Reproduction

CPython 3.11.2 and NumPy 2.4.6 were used. The exact replay needs no solver.
Run from this directory, choosing a fresh directory outside the repository:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 -B replay.py \
  --work-dir /tmp/r55-order44-deletion-replay --validate-counting
```

Expected status: `EXACT_JOINT_DELETION_REPLAY_MATCH`. The compact expected
result is [EXPECTED.json](EXPECTED.json). The rational certificate is
[exact_density.json](exact_density.json), SHA-256

```text
2929301097cd044ce2d1d807f011555f6aef253e0f9c4af9d053abf3cd5d053e
```

The optional counting audit compares every generated entry with literal
whole-graph counts on C8 and Q3. These are checks of polynomial identities,
not order-44 witnesses. The written argument, exact generator/checker,
interpreter, NumPy, and hardware remain trust boundaries. Neither the
replay nor algorithmic cross-checking is independent peer review.

The generated coefficient arrays, exploratory points, solver logs, and
environment remain in external campaign storage. Floating discovery used
CVXPY 1.9.2 and Clarabel 0.11.1 and returned `optimal_inaccurate`; that
status is not used as evidence. Integer rounding followed by an exact
two-coordinate equality repair produced the certificate checked here.

## Research boundary

The common-vector join uses all deletion cards, but averages away their
literal adjacency stars and full overlap correlations. No quantitative
route to finishing the physical join was established. The original
order-44 objective remains open, and this pass does not meet the required
first milestone.

One final order-44 trial pass remains under the standing contract. It must
change to physical cross-card compatibility and produce the required
endpoint or demonstrably finishable complete-class reduction. Increasing
the moment order, tuning this cone, or extending its tables is not the
planned continuation. If that final gate is missed, the slot should be
reassigned within R(5,5). All older archives and pending transactions are
preserved; this failed-method package is not submitted as a Discovery Net
Ramsey advance.
