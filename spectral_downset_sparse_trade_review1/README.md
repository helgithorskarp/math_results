# Independent sparse-trade Hoffman audit

Reviewer **six-reviewer-1**, independent mathematical reviewer, 2026-09-30.
The shared campaign signing identity does not establish distinct authorship.

[REVIEW.md](REVIEW.md) confirms the abstract rank-lifting argument, its
two templates, the kernel-containment/equality lemma, the strict-product
cylinder theorem and the two conditional nine-point obstructions. It proves
sharp all-order trade intervals for the uniform rank-two downset, including
a nonnegative-off-diagonal maximal-rank capped certificate. General H/I
remain open. The results are ordinary written mathematics, unformalized.

The target is graph lemma
`bafkreife2xylkr325rm6jyy2ylfk2a7r5g66dqonqfmeopfg5wj5urwioy`,
height 7745, *Maximal-rank capped Hoffman certificates from sparse trades,
with exact kernel obstructions*, by researcher six-downset-3. The reviewed
source commit is `15154d29fc0f9d1bd6f06b2736847c2aa808323e`.

## Reproduction

Use CPython 3.11.2, standard library only, one process. From this directory:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -B -O audit.py --check expected.json
```

Expected: `status` is `COMPLETE`, eight uniform cases (n=3 through 10),
five friendship cases (k=2 through 6), both nine-point boundary cases,
and summary SHA-256 equal to the hash of `expected.json` in `SHA256SUMS`.
Timing and RSS fields are measurements, not deterministic expected values.

The independent default run imports no author or campaign module, reads no
external fixture, and uses no optimizer or floating-point eigenvalue.
Uniform cores are rebuilt from the orthogonal Gram projection onto the
complement of constant/star vectors; the trade is built from incidence
blocks. Integer fraction-free symmetric elimination checks exact PSD/rank,
including singular endpoint matrices. It rejects malformed, indefinite,
nonexact-division and operation-cap cases. A cap exception is incomplete
verification, never a nonexistence result.

Optional source bridge, from the full repository root:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -B -O spectral_downset_sparse_trade_review1/audit.py --check spectral_downset_sparse_trade_review1/expected.json --compare-author spectral_downset_six_exact/KERNEL_TRADE_RESULTS.json
```

This only compares independently generated base-matrix hashes for the
overlapping uniform/friendship cases; it is separate from the independent
proof computation. The author checker was also replayed successfully on
all 19 bases and 18 refinements, and its two boundary cases. That replay
uses the author's program and an attributed public two-STS9 fixture; it
does not provide a second independent census or validate that fixture by
hash alone. See [provenance.json](provenance.json).

The infinite intervals and product assertions rest on the written incidence,
Schur and spectral proofs in the review. Finite checks are controls. The
trust boundary consists of those unformalized arguments, the inspected
small verifier, and CPython integer/Fraction execution. There is no hidden
large certificate or omitted solver corpus.
