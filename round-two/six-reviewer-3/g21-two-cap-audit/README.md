# Twelve-label capacity review

Actual six-reviewer-3, independent mathematical reviewer. Read [REVIEW.md](REVIEW.md) and the self-contained [PROOF.md](PROOF.md). The entire originalG20+5–12 capacity<=14 on closed[14/25,593/1000] is independently confirmed. This is conditional contact-mask mathematics; the remaining actual-pentagon branch and global Tammes15 optimum remain open.

Python3.11+ standard library only. Execute serially, with one mathematical child and existing1CPU/2GiB scope:

```bash
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
export BLIS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
export PYTHONDONTWRITEBYTECODE=1
python3 reproduce.py --output /tmp/g21-reviewer-cold.json
python3 audit.py --expected full.json --output /tmp/g21-reviewer-full.json
cmp full.json /tmp/g21-reviewer-full.json
python3 -O audit.py --expected full.json --output /tmp/g21-reviewer-full-O.json
cmp full.json /tmp/g21-reviewer-full-O.json
python3 validate.py --output /tmp/g21-reviewer-validation.json
python3 fetch_target.py --dest /tmp/g21-author-pinned
python3 reproduce.py --native /tmp/g21-author-pinned --output /tmp/g21-reviewer-late.json
```

The full independent record is129047 bytes, SHA256 `bc2c42008cc4e38f9b4b853bc34f7f55d72eaa6041cf7941ddbc75e8d7dd4b40`. `reproduce.py` cold-generates it in both modes and checks whole bytes. `validate.py` reruns nine mathematical damages per mode and generates contribution-local `full-O.json`; this redundant output is ignored. Its internal derived normal output has the same whole bytes as the published record. Do not substitute aggregate counts for whole comparisons.

[NATIVE-PINS.json](NATIVE-PINS.json) pins all24 original current-source files at `c21aeb8d07129e63f3ed181c2594aa01741faeb4`; `fetch_target.py` uses that immutable GitHub source, verifies every whole file before use, and retains it only at the requested scratch destination. The source is not vendored. Late comparisons are separate from the sealed primary proof. Native producer/checker commands are documented by the original packet.

[PRIMARY-SEAL.json](PRIMARY-SEAL.json) records the initial private derivation files before native access. The public primary `audit.py`, `validate.py`, `PROOF.md`, `full.json` preserve exactly those bytes. `full-O.json` was a redundant identical129047-byte copy and is not republished. Private preliminary `build.json` and detailed first-run `VALIDATION.json` remain local; their hashes are provenance, not extra unavailable proof inputs. [VALIDATION-SUMMARY.json](VALIDATION-SUMMARY.json) publishes their relevant actual execution results. [COLD-VALIDATION.json](COLD-VALIDATION.json), [NATIVE-VALIDATION.json](NATIVE-VALIDATION.json) and [LATE-COMPARISON.json](LATE-COMPARISON.json) supply complete bounded verification metadata. No proof corpus, solver input, float stream, private ledger, signing key or account metadata is a source requirement.

Original/optimized cold, native and late checks are serial with45-second external child guards, no increased resources. A guard, partial cover or failed child supplies no mathematical exclusion. All proofs remain ordinary and unformalized; runtime version and actual timings are in the validation metadata. Original proof was visible, so the review is not blind. Reused old own integer/Sturm/dual routines and prior sharpness are expressly credited in the review.
