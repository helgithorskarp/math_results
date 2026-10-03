# Independent F103 construction-family review

six-reviewer-4, independent mathematical reviewer. [REVIEW.md](REVIEW.md)
assesses LEMMA9886; [PROOF.md](PROOF.md) gives the independent proof and
sharper integer thresholds402m+1/403m. No unrestricted W bound, optimality
or feasible repair is asserted. The rule in every phase is arbitrary.

Standard-library CPython3.11.2 was used for the independent proof and
CPython3.12.14 for the target's exact source-only replay. From repository root:

```sh
python3 round-two/six-reviewer-4/pattern103-audit/verify.py --output /tmp/f103-independent-fresh
```

Use a new output directory. The runner sets six numerical thread variables
to1, executes one mathematical child at a time with30-second guards,
regenerates all13056 positive packs in both modes, checks all literal
original colors/lifts/free columns, and compares complete records and
corpus bytes with [EXPECTED.json](EXPECTED.json). Approximately three
minutes and tens of MiB suffice in the recorded environment; failure or
timeout is incomplete work, never a proof of mathematical nonexistence.
The additional cold copy hit its fixed240s overall guard after64 completed
records; see [COLD_STATUS.json](COLD_STATUS.json). It was not retried and
is not claimed as a full cold proof replay. The complete primary replay
and complete native mathematical comparisons passed.
Generated packs, child logs and runtime journals remain in the output
directory and are deliberately excluded from publication.

[SEAL.json](SEAL.json) pins the complete primary code/evidence before
target executable/certificate/expected access. The statement and ordinary
proof were exposed: this is not blind. `native_compare.py` is a separately
identified post-seal schema adapter with no native executable imports:

```sh
python3 round-two/six-reviewer-4/pattern103-audit/native_compare.py --target round-two/six-vdw-1/field-pattern-phase103 --mode phases
```

Its four modes are `base`, `affine`, `packs`, `phases`; each reconstructs
and compares the entire corresponding native expected mathematical record.
It uses the exposed target CSV and schema. It is not an input to the
independent primary proof. [VALIDATION.md](VALIDATION.md) records scope,
runtime, source checks, actual damages, and trust boundaries.
