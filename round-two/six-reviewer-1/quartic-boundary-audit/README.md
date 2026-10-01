# Independent second-order Sendov boundary audit

Reviewer: six-reviewer-1, independent mathematical reviewer.

[REVIEW.md](REVIEW.md) confirms committed lemma8619 within its inherited boundary analytic premises. It also proves the sharp common-repair infimum in the fixed attaining family (between1.614 and1.615, soM=2 works) and global finite-optimizer joint coercivity with constant1/128. No global first-power theorem or effective annulus is claimed.

From the repository root, Python3.11 or newer, standard library only:

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B round-two/six-reviewer-1/quartic-boundary-audit/check.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 -I -B -O round-two/six-reviewer-1/quartic-boundary-audit/check.py
```

Both must pass380 independent exact checks,54 control profiles and six damaged-input tests, and match the full compact expected record. The optional `--author PATH/expected.json` checks the bridge to the unchanged author fixture. `--write` regenerates this reviewer's record and is a development option, not independent validation of a changed record.

The code proves finite algebraic identities and signs. The universal rates, compactness, disk containment and coercivity proof are ordinary arguments in the review. No runtime network access, external package, solver, large corpus or private input is needed.
