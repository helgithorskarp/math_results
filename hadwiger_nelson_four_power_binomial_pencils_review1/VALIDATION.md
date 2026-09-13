# Validation record

Date: 2026-09-13 UTC.

Environment:

```text
CPython 3.11.2
SymPy 1.14.0
python-flint 0.8.0
```

The review used a fresh generated certificate in
`/scratch/hn-a5-binomial-complete-review.20260913.mjShrDMG/roots.json`.
That scratch file is not part of the publication artifact.

## Completed runs

- Target producer, eight workers: PASS in 239.674 seconds; 1,404 pairs,
  1,539 components, 4,320 real parameters; 8,605,469 bytes; certificate
  SHA-256 `b2e970417d8ed72882305a0d64d2c3992e0fa38478b67bcbd1c2d8dd641ff095`.
- Target full verifier, eight workers, `--check-expected`: PASS.  It checked
  all unshifted `x`-projection fibres, all component/event substitutions,
  every pencil section, all real-root counts, collision quotients, unit-edge
  hashes, and colour witnesses.
- Independent audit, eight workers: PASS.  It regenerated the finite
  classification and event inventory, eliminated `x`, checked all reverse
  `y`-projection fibres, reconstructed every physical graph, and matched the
  target concurrency and physical transcript hashes.
- Independent negative controls: all six intended corruptions rejected.
- Target controls, boundaries, cache audit, fibre controls, classification,
  corollary, and source pins under optimized Python: PASS.
- Target `SHA256SUMS`: all 28 listed entries passed.

The independent reverse projection found three nonlinear nonrational fibres
across three pairs, compared with 69 fibres across 57 pairs in the target's
opposite projection.  Both covers account for the same 1,539 components and
2,956 pair-component incidences.

The optional full target `--literal-distances` replay was not run.  Complete
physical coverage instead comes from the independent definition-level graph
builder, which partitions and expands all 29,403 digit-label pairs.  Target
controls additionally compare literal and cached complete edge lists on one
degree-23 injective component and four collision fixtures.

No review computation remains running at this checkpoint.  The generated
certificate and the older no-binomial audit scratch directory were preserved.
