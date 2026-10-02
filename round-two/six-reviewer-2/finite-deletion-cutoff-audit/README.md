# Reproduce the independent finite deletion cutoff review

Actual agent **six-reviewer-2**, independent mathematical reviewer.
See [review](REVIEW.md) and [complete ordinary proof](PROOF.md).
The entire k5..24/all-q ansatz classification and original dual are confirmed,
with proved full-original-domain dual and any-positive-floor repair refinements.
General H/I and arbitrary-H exclusions remain open. Explicit credited premises
and unformalized bridges are in the proof. Compact source; no dense corpus.

Use CPython3.12.14 (standard library only). From this directory, normal and
optimized runs independently recompute every full phase and compare the entire
frozen record. One mathematical child at a time, unchanged60s internal/90s
outer guards, native threads1, original1CPU2GiB scope; no resource escalation.

```bash
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 BLIS_NUM_THREADS=1
python verify.py
python -O verify.py
sha256sum -c SHA256SUMS
```

Both report PASS, five phases and whole record SHA256
`18334a845e7c6e5c4806d17b5d8f148a736dc7a47d665c3715799f6e1b1fd17c`.
Every coefficient list and finite record is frozen; elimination stores complete
pivot-sequence digests and recomputes every pivot. Original full-pair baselines
have291661 positions, tuple exception73853 representative/member positions,
all20 semantic damages reject. A timeout or incomplete phase is no exclusion.

Optional postseal common-export comparison uses the byte-pinned original
[author EXPECTED](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-3/remaining-deletion-orders/EXPECTED.json),
SHA256c2bd27bc520c9afbb309239633acc6ae04f3c4c88f4e1614814d85152ee17590:

```bash
python compare.py --author-expected /path/to/original/EXPECTED.json
python -O compare.py --author-expected /path/to/original/EXPECTED.json
```

Both require whole COMPARISON equality and report
`655e26c3b7d14cf092de20c3f7a7cd1fdeb1ad8c869a5659260c4ded6aff6c85`.
No author functions are imported. This adapter and native replay are secondary;
primary proof/programs were sealed beforehand. [PROVENANCE](PROVENANCE.json)
records initial15-file seal and the one postseal proof disclosure correction,
with14 files unchanged. [VALIDATION](VALIDATION.json) records cold normal/O,
whole native replay, adapter and guards; [AUTHOR-INPUTS](AUTHOR-INPUTS.json)
records exact public14+6 file closure. No new graph commitment is implied by
this source alone; the campaign checkpoint records actual committed references.
