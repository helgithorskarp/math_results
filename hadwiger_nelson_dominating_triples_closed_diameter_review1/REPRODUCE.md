# Reproduction

Requirements: CPython 3.11 or later, standard library only. From the
repository root, run:

```sh
python3 -B hadwiger_nelson_dominating_triples_closed_diameter_review1/independent_audit.py \
  --check-expected
python3 -O -B hadwiger_nelson_dominating_triples_closed_diameter_review1/independent_audit.py \
  --check-expected
sha256sum -c hadwiger_nelson_dominating_triples_closed_diameter_review1/SHA256SUMS
```

The independent checker imports no target code and does not parse the target
certificate. It hashes three reviewed target files, reconstructs the exact
distance-three leaf graph, solves its parity equations independently, checks
all normalized exceptional and unit-anchor placements, and derives the sharp
Moser spindle directly from `u`, `v`, and `rho` in
`Q(sqrt(3),sqrt(11))`.

The trust boundary is CPython integer and `Fraction` arithmetic, SHA-256,
inspection of the exhaustive loops, the elementary geometry in the written
review, and linear independence of the squarefree-radical basis. The
continuum theorem is not reduced to a finite certificate: its passage from
circle orbits to all support vertices remains a human-checked proof step.
