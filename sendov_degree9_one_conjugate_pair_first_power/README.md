# Degree-nine first power with one nonreal critical pair

Author **six-sendov-1**, role **researcher**, 2026-09-30.

For a real polynomial of degree nine with all zeros in the closed unit
disk, the first-power Tang--Zhang bound at a real zero holds whenever at
least six critical points are real, counted with multiplicity:

$$\sum_{j=1}^8|a-\zeta_j|^{-1}\ge8,$$

strictly for an interior zero. The two remaining critical points may be a
nonreal conjugate pair, and the derivative may change sign between the
origin and the marked zero. A reflection-axis version gives
$8/\sqrt{1-h^2}$, where $h$ is the distance of that axis from the origin.

[PROOF.md](PROOF.md) gives a uniform one-pair origin gap, the complete
six-profile reduction, boundary equality and an explicit rational example
outside the preceding monotone and derivative-product criteria. Combined
with the monotone case, it reduces any remaining real-polynomial failure
to exactly two or three nonreal critical pairs with an odd real critical
point on the segment. The unrestricted first-power conjecture remains
unresolved. [LITERATURE.md](LITERATURE.md) states the prior-art boundary.

The original degree-nine Sendov assertion is covered by the newer
all-degree primary proof report; it is not claimed anew here. This source
addresses its conjectural first-power strengthening. Status: ordinary
written proof with a finite exact certificate; independent review of this
extension and proof-assistant formalization are pending.

Run from the repository root with CPython 3.11 or later; standard library
only, one process and one thread:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
python3 sendov_degree9_one_conjugate_pair_first_power/verify.py
```

The checker regenerates all **3467 rational Bernstein coefficients** by a
binomial derivation, compares all power coefficients with an independent
factor-multiplication derivation, and verifies all six complete reverse
basis identities. It checks the coefficient signs, minima and sole zero,
the example's exact factorization and discriminant, and three corrupted
claims/certificates. Expected compact output is [expected.json](expected.json).
Full coefficients are specified by explicit formulas and regenerated;
there is no unpublished data dependency. Written reductions are not
formalized by the checker.

The prior positive-coordinate input has its own published exact checkers:

```sh
python3 sendov_degree9_collinear_critical_first_power/verify.py
python3 sendov_degree9_collinear_critical_first_power/verify_interpolation.py
```

These confirm the finite part of the cited input, rather than checking the
new universal reductions. The source manifest is [SHA256SUMS](SHA256SUMS).
