# Terminal Book Ramsey cross-core audit

**six-reviewer-4**, independent mathematical reviewer. This package audits
the ordinary proof in LEMMA9685 for four explicitly prescribed terminal
cores under e(G)<=108, and proves two shorter weighted obstructions that
remain valid for larger fractional missing-set domains. It does not decide
R(B4,B7) or review the parent9631 finite forcing stage.

Read [REVIEW.md](REVIEW.md) for the verdict and trust boundaries, and
[CORE_PROOF.md](CORE_PROOF.md) for the self-contained ordinary derivation.

CPython3.12.14, standard library only. From the repository root:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 round-two/six-reviewer-4/cross-core-audit/verify.py
```

The wrapper runs normal and optimized audit/control children strictly
serially with 30-second guards. Expected output in each mode:
`COMPLETE_CONDITIONAL_CROSS_CORE_AUDIT`, whole record SHA256
`b8474cb24e4fefcc97cd6798b720b6b5af4c66259dcbbba4c107e9af9b432d71`.
The entire recomputed core SHA256 is
`c2ad15c84ee2a03b2f1afc4ca21f9592b27f2392bc0208368ecca826d4967e17`.

Four complete 8192-word domains have 43 columns each. Role record counts
are6/2/1/7/4/3. There are180/360 actual labelled endpoint assignments and
512/384 ordinary missing-set tuples. Both weighted separators have unit
gap. The expanded role domain sizes are18,2,5,5,2,2 for U and
10,1,13,13,18,13 for V. No external input is needed for these checks.

`audit.py` can emit the entire regenerated core to local scratch. Only
source, compact expected summary and hashes are published. Generated data
are ignored; no private ledger, native proof dump or external solver is
an input.

Optional late comparison against the independently pinned author's
`RESULTS.json` (source commit recorded in `AUTHOR_SOURCE.json`):

```sh
python3 round-two/six-reviewer-4/cross-core-audit/compare_author.py /path/to/pinned/RESULTS.json
```

That comparison verifies all172 complete column records,23 role records,
all tight-pair rules,15 listed physical spines and both complete896-tuple
failure histograms; eight semantic damages are rejected. It is separate
from the offline proof verifier. It was added only after the seven-file
own core/proof/control seal, which remains unchanged.

`FIRST_SEAL.json`, `PROVENANCE.json`, `AUTHOR_SOURCE.json` and
`VALIDATION.json` give the precise chronology, source pins and limitations.
The mathematical proof is ordinary and unformalized; code is corroboration.
