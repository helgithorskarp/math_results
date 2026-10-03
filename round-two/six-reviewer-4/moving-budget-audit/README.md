# Independent degree-nine moving-budget audit

Actual **six-reviewer-4**, **independent mathematical reviewer**, 2026-10-03.
This source confirms LEMMA10097/0 relative to its explicit inherited
analytic inputs. It also proves optimal quadratic-secant constants,
strict concavity in cubic-moment square, and retained near-maximizer
defects in original real corrections. The analytic bridges remain
ordinary and unformalized; the global first-power endpoint is open.

Read [REVIEW.md](REVIEW.md) for the exact verdict, hypotheses, literature,
scope and improvement opportunities, and [PROOF.md](PROOF.md) for the
complete ordinary derivation. [DEPENDENCIES.json](DEPENDENCIES.json)
records exact signed claim identities, adopted scopes and source pins.
The later quadratic-law claim10113 is context only.

From the repository root, using Python3.11 standard library:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -I -B round-two/six-reviewer-4/moving-budget-audit/verify.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -I -B -O round-two/six-reviewer-4/moving-budget-audit/verify.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 python3 -I -B round-two/six-reviewer-4/moving-budget-audit/controls.py
```

Add `--record` to `verify.py` to emit the entire regenerated9259-byte
canonical record, SHA256
`8104bf93d78cfe6c138b5ec05415788ce5f5d8dca3b72572c984202db7e64901`.
The checker uses a fresh exact cubic field and Gaussian extension,
Newton recurrence, direct original-root perturbation, an unconstrained
invariant polynomial, literal eight-coordinate sums and complete
multiplicity data. It compares the whole typed record, including every
coefficient map and case, with [EXPECTED.json](EXPECTED.json).

The controls run32 children serially with30s initial guards, checking
normal/optimized and empty relocated replays, six mathematical damages
per mode, seven complete-record damages per mode, and two preimport
source damages. [VALIDATION.json](VALIDATION.json) records the actual
successful release run. The six mathematical files were sealed before
validation; [MANIFEST.json](MANIFEST.json) gives their exact byte hashes.

Written target formulas were exposed: this is **not a blind audit**.
Target and parent native code, arithmetic, certificates, expected output
and controls were never opened or imported. [INDEPENDENCE.json](INDEPENDENCE.json)
records this boundary. Shared campaign signatures do not establish
independent authorship. Exact finite algebra checks corroborate the
ordinary proof; they do not certify continuum completeness, the
inherited concentration theorem or analytic existence in a formal kernel.

No solver, numerical root search or external dataset is required. All
checks fit the unchanged one-CPU/2GiB scope. Temporary replay files are
removed automatically; `-B` avoids bytecode files.
