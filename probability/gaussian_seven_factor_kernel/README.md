# A universal degree-nine Gaussian energy comparison

For every bounded probability law on R3, every 1-Lipschitz map and every
positive Gaussian variance, this packet proves the previously unsigned
beta inequality **b_(7,0)>=0**, strictly unless the map preserves all
support distances. With normalized moment gaps d_m, the new inequality is

    36d_2-84d_3+126d_4-126d_5+84d_6-36d_7+9d_8-d_9 >= 0.

The same conditional-kernel proof gives b_(j+7,j)>=0 for every j>=0,
every polarized weight coefficient, and an explicit lower bound proportional
to the actual mean distance loss. Together with R2, every beta row N<=7 is
signed. The full majorisation conjecture and new Kneser--Poulsen consequences
are not established here.

The mechanism is an exact finite-kernel integral of R2's matching polynomial,
followed by a PSD trace decomposition. Two explicit integer matrices, of
orders 42 and210, certify the two remaining homogeneous forms. Their PSD
certificates use exact annihilating polynomials and separate fraction-free
elimination. No floating eigenvalue or sampled parameter sign is a premise.

**Status:** author computer-assisted proof; independent mathematical review
and formalization pending. All hypotheses, normalizations, formulas and
computational trust boundaries are in [PROOF.md](PROOF.md).

Run from the repository root, with Python 3.11 or later and the standard library:

```sh
python3 probability/gaussian_seven_factor_kernel/certificate.py
python3 probability/gaussian_seven_factor_kernel/verify.py
python3 probability/gaussian_seven_factor_kernel/audit_recentring.py
```

Each command checks its complete output against [EXPECTED.json](EXPECTED.json)
and fails on a discrepancy. The first verifies both full matrix identities;
the second checks the polynomial coefficients, reciprocal symmetry and
independent PSD certificates; the third checks the derivative/recentering
normalization with exact square-free series. Normal and optimized
CPython 3.11.2 agree. The full replay takes well under one minute on the author
environment. [SHA256SUMS](SHA256SUMS) pins the compact source; no omitted large
dataset or solver is required. Provenance is in [SOURCES.md](SOURCES.md) and
[INPUTS.json](INPUTS.json).

For R2/R3/R5: the seven-factor rank-six kernel is now positive globally at
the author-proof level, so the three residual nine-replica patterns can be
removed from unknown sign obligations. Equation(22) gives a compressed
rational margin on the radius2l compact frontier. This does not remove the
remaining large-row entries, iterate the global defect 7/50 bound, or claim
that every polynomial curvature compares. Use the finite PSD identities as
the review target; no further geometric subclass is needed for this result.
