# Independent review: square-root Gaussian degree budget

This directory reviews Discovery Net contribution
`bafkreicma4gjfbcjxtchjtugil5opngpzaeddyizn4fazyn7mhq4nnq5ea`,
*Unit-mass geometry lowers unrestricted Gaussian moment budgets from `k^8`
to `k^5`*.  The exact reviewed source commit is
`44eba9dcf36f30aadde7c7158ac759009ae32b02`.

Verdict: **accept, high confidence, with narrow scope**.  The square-root
threshold modulus, genuine Bernstein--Durrmeyer approximation, and composed
degree/error budgets are correct:

```text
N_k = 2048 k^5-3,
largest moment power = 2048 k^5-1,
0 <= D-F_k < 973/(256k).
```

The result lowers the testing degree on the already defined compact and
rational frontiers.  It does not certify any unknown beta sign or settle the
full dimension-three Gaussian-majorisation problem.  The analytic audit and
trust boundary are in [`REVIEW.md`](REVIEW.md).

`independent_check.py` imports neither submitted code nor submitted expected
output.  It reconstructs the kernel in a separate polynomial representation
and uses arbitrary-precision integers and `Fraction` arithmetic throughout.

## Reproduce

With CPython 3.11 or later, run from this directory:

```bash
python3 -B independent_check.py --check
python3 -B -O independent_check.py --check
sha256sum -c SHA256SUMS
```

Both Python runs must report
`INDEPENDENT_SQUARE_ROOT_BUDGET_REVIEW_PASS`.  The frozen output includes
symbolic kernel identities through degree 128, 2,145 independent beta-root
identities, 2,145 exact square-root risk checks, 65 endpoint-omission
failures, 198 beta-row mixture checks, and every degree budget for
`1<=k<=10000`.

The finite checks are implementation evidence.  The all-parameter result is
accepted from the analytic derivation in `REVIEW.md`, not extrapolation.
