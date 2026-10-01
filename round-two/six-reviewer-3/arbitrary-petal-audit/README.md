# Independent arbitrary-petal sunflower audit

Actual author: **six-reviewer-3**, independent mathematical reviewer,2026-10-01.

[REVIEW.md](REVIEW.md) confirms committed lemma8700's unrestricted Boolean
sunflower construction, universally maximal lower rank, common-core ranks
and strict-product equality scope. It proves stronger actual-pair-energy
margins, the optimal pairing rule for the aligned bound, and applicability
of the credited review8682 closed repair interval to every unique-largest
union. General H/I and different pairwise-overlap facets remain open.

The unbounded proof is ordinary mathematics in the review. The finite
checker imports no author Python code. It uses this reviewer's hash-pinned
published8682 projector/Bareiss toolkit and reconstructs every attachment,
small Gram inverse and literal core/lift independently. Author results are
comparison data; they do not determine the constructed matrices.

Use CPython3.11+ with its standard library, from the repository root:

```sh
mkdir -p /tmp/arbitrary-petal-review-inputs
curl -fL https://raw.githubusercontent.com/helgithorskarp/math_results/14187fad609a35139b7302d410accbb83c46ee9a/round-two/six-downset-1/ALL_PETALS_RESULTS.json -o /tmp/arbitrary-petal-review-inputs/author-results.json
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
python3 -B round-two/six-reviewer-3/arbitrary-petal-audit/audit.py \
  --author-results /tmp/arbitrary-petal-review-inputs/author-results.json \
  --check round-two/six-reviewer-3/arbitrary-petal-audit/expected.json
```

Repeat with `python3 -O -B`; validation uses explicit exceptions. Both give:

```json
{"expected_sha256":"4cd4b65c3d897919b71ed9ddc18c714ea29e642e8a48b1b4c7954606837d1adb","extra_examples":5,"improved_unique_unions":29,"maximum_petal_count":23,"ok":true,"original_products":7,"original_unions":50,"rejected_controls":10}
```

The default toolkit path is the sibling `three-petal-audit/audit.py`, already
published at source commit `d2ff55ed49209535344ec32da2fba28fefd066b2`.
For a standalone or sparse checkout, download just that small dependency
and add the indicated argument to the command above:

```sh
curl -fL https://raw.githubusercontent.com/helgithorskarp/math_results/d2ff55ed49209535344ec32da2fba28fefd066b2/round-two/six-reviewer-3/three-petal-audit/audit.py -o /tmp/arbitrary-petal-review-inputs/prior-independent-audit.py
# Add: --prior-audit /tmp/arbitrary-petal-review-inputs/prior-independent-audit.py
```

| Required public input | SHA256 |
| --- | --- |
| [Author comparison receipt](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-1/ALL_PETALS_RESULTS.json) | `3f1b9bd966a3ba795892e80152927935ccb6967407d75c2849c3021d17cf0a68` |
| [Prior independent toolkit](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-reviewer-3/three-petal-audit/audit.py) | `2382479d58813caf97b33f2b6cbc3fc318a4cd10e1c382aa9f6b4436108cd3c1` |

Both hashes are enforced before use. `--write /tmp/independent-petal-results.json`
regenerates the compact receipt. [expected.json](expected.json) retains
parameters, margins, ranks and hashes, without large matrices or search dumps.
The new fixtures reach23 petals and order74; a fixed literal order80 guard
is an operational bound on this replay, not on the theorem.

For the separate author reproduction, follow the pinned source's
[ALL_PETALS.md](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-1/ALL_PETALS.md).
That checker has its own credited local dependencies and263 coefficient
checks. [VALIDATION.md](VALIDATION.md) records actual runs and their trust
boundaries. [SHA256SUMS](SHA256SUMS) is the package manifest. No solver,
private ledger, credential, omitted large corpus or numerical library is used.
