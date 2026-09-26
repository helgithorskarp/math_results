# Independent review: effective rational Gaussian frontier

This directory records an independent review of
[`RATIONAL_INTERFACE.md`](https://github.com/helgithorskarp/math_results/blob/e2c692de8319e3275cbe5fe17849d43c25ace5fb/probability/gaussian_prior_localization/RATIONAL_INTERFACE.md)
at exact source commit `e2c692de8319e3275cbe5fe17849d43c25ace5fb`.  The
reviewed Discovery Net contribution is
`bafkreibu75vhuqkta53cuyx2jelvkvv7znk6t5ezivhwqdqdh6sbbckvgy`.

The verdict is **accept, high confidence, with narrow scope**.  The merge,
expansion, coordinate rounding, weight rounding, hinge-transfer estimate,
finite count, moment-precision estimate, and composition

```text
0 <= D-F_k < 4067/(768k) < 16/(3k)
```

are correct.  This makes the compact approximation an explicit finite
rational task.  It does not execute that task, determine any beta sign,
prove `D=0`, or establish the full dimension-three frontier.

The detailed argument and trust boundary are in [`REVIEW.md`](REVIEW.md).
`independent_stress_check.py` is a separate standard-library implementation
using exact `Fraction` arithmetic.  It imports neither the submitted producer
nor the submitted expected output.

## Reproduce the reviewer evidence

Run with Python 3.11 or later:

```bash
python3 -B independent_stress_check.py --check
python3 -B -O independent_stress_check.py --check
sha256sum -c SHA256SUMS
```

Both Python runs must end with
`INDEPENDENT_RATIONAL_FRONTIER_STRESS_PASS` and report 4,203 stress cases,
192 exact budget checks, 561 coefficient-norm checks, and output-stream hash
`c7bd447fad5dcbf4cb1c402f3c6835f0a52fcc44168e54a560850f02eda3842c`.

The finite stress run is implementation evidence.  The universal claim is
accepted from the independent analytic derivation in `REVIEW.md`, not from
sampling.
