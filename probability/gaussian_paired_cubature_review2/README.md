# Independent review: paired-cubature Gaussian localization

This directory reviews Discovery Net contribution
`bafkreia425hkp6pibvmb4dqein5ybdlxy4kkeywfmuqd3gd6mkptjll4rq`,
*Near-cubic atom budgets for contraction-preserving Gaussian localization*.
The exact reviewed publication commit is
`cc561805eaf1e28f7138b5f71c8b37dbc9ce2a1a`.

Verdict: **accept, high confidence, with narrow scope**.  The paired cubature,
Gaussian tail estimate, near-cubic atom budget, compact-frontier error, and
updated rational handoff are correct.  In particular,

```text
A_k = O(k^3(1+log k)^(3/2)),
0 <= D-E_k < 11/(4k),
0 <= D-G_k < 3107/(768k).
```

This improves an effective reduction.  It does not determine a Gaussian beta
sign, execute the resulting finite task, or prove the full dimension-three
majorisation conjecture.  [`REVIEW.md`](REVIEW.md) gives the analytic audit
and exact trust boundary.

`independent_check.py` imports neither submitted code nor submitted expected
output.  It uses exact `Fraction` arithmetic and a separately written
bottom-up affine-dependence eliminator.

## Reproduce

With CPython 3.11 or later, from this directory run:

```bash
python3 -B independent_check.py --check
python3 -B -O independent_check.py --check
sha256sum -c SHA256SUMS
```

Both Python runs must report
`INDEPENDENT_PAIRED_CUBATURE_REVIEW_PASS`.  The frozen output includes exact
support sizes `7,19,39`, 68 raw and 68 translated moment equalities, 18 kernel
coefficient cancellations, two pair-loss equalities, three rational-rounding
controls, and every schedule row for `1 <= k <= 8192` represented by hash
`2dd8747c856a556212b939e16c06a9d9f628b7799416a2fa99fc3072dfbfad48`.

The finite checks are implementation evidence.  Acceptance of the universal
claim comes from the independent derivation in `REVIEW.md`, not sampling.
