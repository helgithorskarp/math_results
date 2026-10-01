# Independent order-eight F617 audit

Author **six-reviewer-5**, independent mathematical reviewer.

[REVIEW.md](REVIEW.md) confirms the complete H8-invariant punctured-field seven-AP exclusion h8589. The independent implementation uses literal subgroup orbits, all AP reversal classes, complete clause multiset equality and signed-set positive-RUP replay. Every one of the seventeen case refutations is checked.

The review proves that a union of consecutive H8 cosets in the order defined by primitive element three is seven-AP-free exactly up to 18 cosets. The minimum AP-containing window is 19, with precisely 77 minimizing supports in one cyclic orbit. A conditional full affine-stabilizer refinement replaces the previously reviewed threshold 11 by 8, retaining the old order-at-least-eleven rigidity theorem. No interval construction or new unrestricted W bound follows.

Use CPython >=3.11, GCC, and a virtual environment with pinned proposal packages:

```bash
python3 -m venv /tmp/reviewer5-order8-env
/tmp/reviewer5-order8-env/bin/pip install -r round-two/six-reviewer-5/order8-template-review/requirements.txt
/tmp/reviewer5-order8-env/bin/python -B round-two/six-reviewer-5/order8-template-review/reproduce.py \
  --repository-root . --output-dir /tmp/reviewer5-order8-run
```

Choose fresh environment/output paths if those already exist. A sparse checkout must contain this directory and `round-two/six-vdw-2/order8-rigidity`. [INPUTS.json](INPUTS.json) pins the three author proposal files from source commit `9e470a87f252beba837e06a4e40278cba1953bc1`. The official drat-trim source is downloaded from a pinned commit and SHA256 checked; optional `--drat-source PATH` uses matching existing bytes. Altered inputs stop reproduction.

The runner generates and independently audits seventeen CNFs, proposes proofs with 50,000-conflict/30-second limits, converts within 25 seconds internally/30 externally, and runs all exact audits, RUP replays and controls in normal and optimized Python. All children run sequentially with one numerical thread. Timeout, UNKNOWN, malformed input or a failed check produces no mathematical exclusion. Solvers and conversion messages are untrusted proof proposals. Exact reference receipts are in [EXPECTED.json](EXPECTED.json); alternative generated trace counts can differ and need separate exact validation rather than a claim of matching the reference fixture.

Expected final status: `H8_EXCLUSION_AND_SHARP_COSET_INTERVAL_CLASSIFICATION_VERIFIED`. The recorded CPython 3.11.2/GCC 12.2.0 run took 86.31 seconds and peaked at 98,920 KiB child RSS, with largest stage 11.78 seconds. [VALIDATION.json](VALIDATION.json) records the complete measured run. Generated traces, CNFs, binaries and logs stay in the chosen local output directory.

[field.py](field.py) imports no author algebra. [rup.py](rup.py) reuses this reviewer's independently published signed-set RUP mechanism; [check.py](check.py) binds it to the complete new cases. [controls.py](controls.py) independently truth-classifies all 256 tiny clause families and rejects ten altered production inputs in both modes. Ordinary exact Python/runtime, strict decoding, the written finite-group/run-cover reductions and the attributed older rigidity theorem are the trust boundaries. No large proof corpus, private ledger or credential is published.
