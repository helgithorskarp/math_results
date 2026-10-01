# Independent all-rank uniform H audit

Actual author: **six-reviewer-3**, independent mathematical reviewer,2026-10-01.

[REVIEW.md](REVIEW.md) confirms the complete scoped claims in8660 and8722:
the unique stable-order sparse centered constructor and residual criterion,
capped maximal-rank H at every integer \(r\ge2,n\ge8r\), and finite products.
It extends the credited rank-five closed repair mechanism8648 to that linear
range, for every rational
\(0<t\le2/[(n-2)(n-3)(2n-1)]\), with a strictly positive quantitative upper
gap at the endpoint. General H/I and all stable-order cap feasibility remain open.

The unbounded proof is ordinary unformalized mathematics in the review.
[audit.py](audit.py) independently solves the complete affine constraint
system and checks exact blocks, quotients, residuals, projected gaps, literal
matching lifts, full matrix hashes, repairs and negative controls. It imports
no author code. Public hash-pinned receipts are entrywise comparisons, not
inputs to the affine constructor or hidden proof assumptions.

Use Python3.11+ with its standard library. From the repository root, retrieve
the three small public comparison receipts into a scratch directory. The commits
below pin the reviewed versions; direct main reader links are provided separately.

```sh
mkdir -p /tmp/uniform-h-review-inputs
curl -fL https://raw.githubusercontent.com/helgithorskarp/math_results/912163895633d4cc34d1ee515fd230e31442ba4e/round-two/six-downset-2/eventual_uniform/RESULTS.json -o /tmp/uniform-h-review-inputs/quadratic.json
curl -fL https://raw.githubusercontent.com/helgithorskarp/math_results/912163895633d4cc34d1ee515fd230e31442ba4e/round-two/six-downset-2/eventual_uniform/BASELINE.json -o /tmp/uniform-h-review-inputs/rank-five.json
curl -fL https://raw.githubusercontent.com/helgithorskarp/math_results/8b110533913a22fd2d52955e3e20770fbc369cf8/round-two/six-downset-2/linear_uniform/RESULTS.json -o /tmp/uniform-h-review-inputs/linear.json
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
python3 -B round-two/six-reviewer-3/eventual-uniform-audit/audit.py \
  --author-results /tmp/uniform-h-review-inputs/quadratic.json \
  --baseline /tmp/uniform-h-review-inputs/rank-five.json \
  --linear-results /tmp/uniform-h-review-inputs/linear.json \
  --check round-two/six-reviewer-3/eventual-uniform-audit/expected.json
```

Repeat the last command with `python3 -O -B`. Explicit exception checks remain
active in optimized Python. Both modes produce:

```json
{"expected_sha256":"98e6dca1cd4057a072630c75dbae105c6afc1fc78b6139eb441f041c0bc6b64a","linear_cases":33,"literal_orders":[11,42,163],"ok":true,"original_cases":28,"quadratic_corroboration_cases":30,"rejected_controls":11}
```

The linear source's additional original-index matrix orders are11 and137.
Every reported rational radius is compared entrywise; the compact receipt
retains hashes rather than repeating all those fractions. The30 quadratic
corroboration cases are a superseded exploratory estimate, not a new range
claim. No sampled case supplies the proof of the infinite quantifiers.

| Public comparison input | SHA256 |
| --- | --- |
| [Quadratic RESULTS.json](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/eventual_uniform/RESULTS.json) | `5635bf2e94f88b8d6f47e7ff1e1a61b6282ff31a1f07af02d73caf554f79cc88` |
| [Rank-five BASELINE.json](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/eventual_uniform/BASELINE.json) | `3bd48141e92a017cb175666bd9783b8d66cd1648fa6e3832367d5f9640665428` |
| [Linear RESULTS.json](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/linear_uniform/RESULTS.json) | `c4c04361e2831a4ad1c00d36906c04051ae1ba330435aab7a4d7597cfb6a30e9` |

Author inputs remain in their original directories. For separate author
reproduction, their [quadratic README](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/eventual_uniform/README.md)
and [linear README](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/linear_uniform/README.md)
give the source-pinned commands. [VALIDATION.md](VALIDATION.md) records our
actual independent and separate author replays. [SHA256SUMS](SHA256SUMS)
is the package manifest. No solver, CAS, private ledger, credential, cache,
raw enumeration dump or large proof corpus is required or published.
