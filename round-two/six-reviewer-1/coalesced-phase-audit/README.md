# Coalesced phase audit

Independent reviewer **six-reviewer-1** confirms9039's complete local complex
phase/slack theorem, credits the earlier wider polynomial result7290 and its
uniform extension/review7328/7362, and proves the origin-plus-critical-disk
relaxation fails at its threshold as well as below it. This is not a polynomial
counterexample or a global first-power theorem. See [REVIEW.md](REVIEW.md).

Use CPython3.12.14 (Python3.11+ syntax), SymPy1.14.0 and mpmath1.3.0.
Install the pinned dependencies in an isolated environment, then from repository root:

```sh
env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
 python3 -I -B round-two/six-reviewer-1/coalesced-phase-audit/check.py
```

Repeat with `-O` before the script. An isolated package directory can instead be
passed with `--vendor /absolute/path/to/packages`. The checker uses a fixed90s
POSIX alarm and fails explicitly on changed evidence or an unpinned SymPy.
`--record /path/outside/repository/result.json` optionally writes the full record.
`--author-expected /path/to/original/expected.json` optionally compares every
shared original coefficient list. That comparison is corroboration; the
independent derivation imports no author source or formula hints.

Expected: PASS;64 full matrix entries,72 original positive Bernstein
coefficients,10 coefficients certifying the negative threshold quartic,
22 further coefficients bounding it strictly between-1/50 and-1/100,
five mathematical damage rejections and four internal fixture rejections.
Record SHA256 `78dc65c39c8d412865efa74d45aa44bcc6b84acad085af2cfc6b62c4a3befd8b`.
Runtime and memory are reported separately and are not part of the record.
Local runs take about4–10s of checker wall time, peak below67MiB, one job/thread.

`derive.py` uses exact simultaneous phase jets and exact fourth-order primitive
products over rational fields. `expected.json` is compact evidence, not an
input that defines the result; it is regenerated and compared in full.
`SHA256SUMS` covers the other source files. Ordinary analytic proof bridges
and classical Gauss–Lucas remain outside the computational checker and are
written in the review. No theorem-prover kernel, full transverse quartic
classification, effective neighborhood or historical priority is claimed.
