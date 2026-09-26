# Validation and trust boundary

The universal results are mathematical proofs in [PROOF.md](PROOF.md).
The exact program audits their algebra and concrete examples; neither
finite sampling nor GitHub publication proves the universal statements.
No proof assistant or independent mathematical referee has checked them.

Run with CPython 3.11.2 or later, standard library only:

```sh
python3 verify.py --check
python3 -O verify.py --check
sha256sum -c SHA256SUMS
```

Both runs must report `CONE_REFLECTION_EXACT_AUDITS_PASS` and the same
SHA256 for [EXPECTED.json](EXPECTED.json). No external dataset, service,
solver, numerical quadrature, or omitted large certificate is required.
All decision arithmetic uses Python integers and `fractions.Fraction`.
Correctness checks use explicit exceptions, so `python -O` does not remove
them. The ordinary and optimized outputs were compared before publication.

The audits establish:

- Four universal polynomial identities, including a cleared-denominator
  formula for the difference `a(v)-a(u)`. They are checked coefficient by
  coefficient in formal variables, not at numerical values.
- The rational nonorthogonal generator basis and its dual; determinant
  values `48/65` and `65/48`; and paired affine rank six for the seven-site
  example.
- Gram preservation and monotone distances for a thirteen-point cloud
  containing both generators and positive interior combinations. Nine
  rational times in the nondegenerate motion give 81 Gram-entry checks
  and 624 pair-distance checks. Seventeen times in the separate `h=1`
  motion give 153 Gram-entry checks and 1,248 pair-distance checks.
  These finite trajectories are controls of the implementation; the
  polynomial identities and sign proof establish the full continuous path.
- All 36 endpoint pair inequalities for the square fixture, independently
  comparing squared coordinate distances with the `4 a dot b` formula.
  Eight pairs shrink and twenty-eight preserve their distances.
- Paired rank six for that nine-point map and rank five after deleting
  the origin; rank three for both rigid clusters; and the unique moving
  circuit with coefficients `(1,-1,1,-1)`.
- Two descriptions of the square obstruction: two independent incident
  facet normals pin each projected ray, and eight independent linear
  equations on a `3 by 3` projection matrix leave only scalar matrices.
  A Gram minor is exactly `16`, certifying the three auxiliary dimensions
  required when the scalar projection is zero.
- All 512 subset masses for the asymmetric weights `2^j/511`, confirming
  that each individual target mass has exactly its prescribed singleton
  preimage. This checks the deterministic-matching obstruction separately
  from the geometric rank calculations.
- Three invalid controls: a deliberately corrupted polynomial identity,
  a fixed point outside the dual cone with squared-distance loss `-4`,
  and the reversed square map interpreted incorrectly as a contraction.

The key unformalized bridges are the analytic use of Aishwarya--Li's
continuous-contraction theorem, the exponential density-value identity,
and Bezdek--Connelly's ball-volume transfer. The proof of the square
obstruction also uses continuity to pass from projection scalar `-1` to
`1`. Every such step is stated in the written proof.

Exploratory optimization and floating sphere integrations that motivated
the motion are excluded from this source packet and are not evidence for
the theorem. No numerical candidate is labeled a Gaussian counterexample.
