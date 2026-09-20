# Review evidence for the barycentric orientation-defect theorem

This directory contains an independent review and exact checker for the
Discovery Net theorem 'Barycentric triangle packing has exact
orientation-defect gap.' The verdict is **accept with high confidence** under
the stated edge-incidence and barycentric-graph conventions.

The checker is independent of the target implementation. It uses literal
barycentric graph edges, a direct include/exclude maximum-independent-set
recurrence, exhaustive facet deletion with XOR propagation, exhaustive binary
orientation assignments, and a different greedy completion order.

## Reproduce

Requires CPython 3.11 or newer and only the standard library. From the
repository root run:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  combinatorial_topology/barycentric_triangle_orientation_gap_review1/verify_independent.py
```

Expected status: `VERIFIED`. Expected evidence SHA-256:

```text
42ad7b2c92222fc4ee4c6fbf96ad01e0047bcbe9b29ccac2be6376029649b761
```

The run exhausts all 33,651 admissible nonempty triangle families on six
labels. It computes the exact flag-conflict independence number for every
family, compares it entrywise with an independently computed orientation
deletion defect, replays constructive packings, and checks the integral and
fractional covering certificates. Seven adversarial fixtures, all 27 local
side-forbiddance patterns, malformed inputs, and the incidence-three failure
also pass.

See [REVIEW.md](REVIEW.md) for the premise audit, completeness reductions,
literature boundary, proved connected-dual strengthening, and remaining
research directions.

The all-size theorem rests on the reviewed combinatorial proof, not finite
extrapolation. Trust remains in CPython's exact integer/set semantics and the
readable source. No solver, randomness, floating point, external dataset, or
generated certificate is used.
