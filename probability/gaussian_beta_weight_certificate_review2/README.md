# Independent review of the signed Gaussian beta cell

This directory independently reviews the claim at source commit
[`a006501b012a7084676d632df4d73af1fdd92a58`](https://github.com/helgithorskarp/math_results/commit/a006501b012a7084676d632df4d73af1fdd92a58),
Discovery Net reference
`bafkreihr7w5sdqcwo6k64atuo633zrulsazvkbrsfivwo4xm7cydegxfi4`.

Verdict: **accept with high confidence**, for the finite statement actually
made.  The review does not promote this local signed beta row to the full
dimension-three Gaussian-majorisation frontier.

Run from the repository root:

```sh
python3 probability/gaussian_beta_weight_certificate_review2/independent_interval_check.py
python3 -O probability/gaussian_beta_weight_certificate_review2/independent_interval_check.py
```

Both commands must reproduce `EXPECTED.json`.  The checker uses only the
Python standard library and does not import the submitted checker, bounds
code, fixture file, or expected output.  See `REVIEW.md` for the proof audit,
trust boundary, and limitations.
