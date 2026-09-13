# Validation
Author-side validation on CPython 3.11.2, 2026-09-13 UTC:

- certificate production with CaDiCaL 1.9.5 completed for all three rows;
- normal solver-free verification returned `VERIFIED`;
- optimized (`python3 -O`) solver-free verification returned `VERIFIED`;
- three edge-breaking colour-word mutations were rejected;
- exact atom scans returned 11 Moser and 18 Golomb unit edges;
- every point, coincidence, isometry multiplier, and strict edge was rebuilt
  using rational arithmetic in the displayed field basis;
- JSON validation, bytecode compilation, manifest verification, and
  `git diff --check` passed before publication.

This is author-side exact computational evidence, not an independent review.
The certificate is positive: correctness rests on the small exact verifier,
Python integer/rational arithmetic, and SHA-256 collision resistance, not SAT
solver soundness.
