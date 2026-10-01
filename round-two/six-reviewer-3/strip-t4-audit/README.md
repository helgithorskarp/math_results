# Independent T4 Heesch audit

Reviewer **six-reviewer-3**, independent mathematical reviewer. [REVIEW.md](REVIEW.md) verifies committed claim 8945: the specified nineteen-cell strip has exactly three complete coronas under all Euclidean motions and reflections and does not tile the plane. It also proves the all-stage-holes maximum is three and the stable 29-contact domain is the greatest fixed point of the precise pair-cover operator. No longer-strip, record or finite-five result is claimed.

From the repository root, with Python 3.11 and network access for the initial four immutable JSON downloads:

```sh
python3 round-two/six-reviewer-3/strip-t4-audit/fetch_inputs.py /tmp/t4-audit-inputs
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 python3 round-two/six-reviewer-3/strip-t4-audit/replay.py --input-dir /tmp/t4-audit-inputs
```

`fetch_inputs.py` reads [INPUTS.json](INPUTS.json) and validates all four commit-pinned byte hashes before writing. An existing differing file is never overwritten. The JSON data total 89,109 bytes and are the original public author's witnesses/certificates, not reviewer-generated discoveries. They are not duplicated in this package. Subsequent replay is offline. `replay.py` runs the independent [audit.py](audit.py) serially in normal and optimized Python with fixed 60-second child guards, compares the entire [EXPECTED.json](EXPECTED.json), and raises on any mathematical mismatch or incomplete job. Its one-model search guard is 100,000 visits. An incomplete run proves nothing.

A single independent run can retain full case evidence:

```sh
python3 round-two/six-reviewer-3/strip-t4-audit/audit.py --input-dir /tmp/t4-audit-inputs --output /tmp/t4-independent-evidence.json
```

[VALIDATION.json](VALIDATION.json) records two matching final independent runs, the separate normal-only original-reader baseline and primary-control crosscheck. Timings/RSS are observations; exact fingerprints and whole records are the comparison criteria. All checks use explicit exceptions and remain active under optimized Python.

The implementation independently generates isometries by cube-coordinate permutations, reconstructs 568 contacts by whole unit-edge alignment, checks topology by directed polygon-boundary cycles, derives conflicts from complete cell incidence, regenerates 293 early negative searches, recursively verifies 178 rejection DAGs/387 states, exhaustively enumerates 17 stars, and checks 29 positive pair witnesses plus the lower constructions. Ten damaged controls must reject. The ordinary continuous-motion and depth proofs are written in the review and remain unformalized; integer certificate validation alone does not certify them.

[SHA256SUMS](SHA256SUMS) covers every other file, including `.gitignore`. No large proof corpus, private operational state or credentials are included. The published original author's code was executed only for the separately identified baseline and is never imported by `audit.py`.
